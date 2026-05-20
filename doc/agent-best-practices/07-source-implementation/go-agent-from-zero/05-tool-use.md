# 05. 增加 tool use

[返回专题首页](README.md)

本节在前面 Agent 的基础上只增加一个能力：让 Claude 可以请求调用一个本地工具。

这一节不接真实数据库，也不做 MCP。先实现一个最小本地工具 `get_time`，让模型在需要当前时间时返回 `tool_use`，Go 执行工具，再把 `tool_result` 发回 Claude，让 Claude 生成最终回答。

## 本节任务

输入：

```text
现在几点？
```

期望流程：

```text
用户问时间
  ↓
Claude 返回 tool_use: get_time
  ↓
Go 执行本地 getTime()
  ↓
Go 把 tool_result 发回 Claude
  ↓
Claude 返回自然语言答案
```

## 和上一节相比新增什么

请求体新增 `tools`：

```json
{
  "tools": [
    {
      "name": "get_time",
      "description": "Get current local time",
      "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  ]
}
```

响应内容可能不再只是 `text`，还可能出现：

```json
{
  "type": "tool_use",
  "id": "toolu_...",
  "name": "get_time",
  "input": {}
}
```

## 本节要理解的关键点

Claude 不会直接执行 Go 函数。Claude 只会返回“我想调用哪个工具，以及参数是什么”。

真正执行工具的是你的 Go 程序：

```text
Claude 提出 tool_use
Go 检查 tool name
Go 执行本地函数
Go 把结果作为 tool_result 发回 Claude
```

## 核心 JSON 结构

第一次请求带上工具定义：

```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 512,
  "tools": [
    {
      "name": "get_time",
      "description": "Get current local time",
      "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": "现在几点？"
    }
  ]
}
```

如果 Claude 决定用工具，返回的 assistant message 里会包含 `tool_use`。

第二次请求要把两段内容都带上：

1. Claude 上一轮返回的 `tool_use`。
2. Go 执行工具后的 `tool_result`。

```json
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_...",
      "content": "2026-05-20 12:30:00"
    }
  ]
}
```

## 完整 main.go

```go
package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

const endpoint = "https://api.anthropic.com/v1/messages"

type TextContent struct {
	Type string `json:"type"`
	Text string `json:"text,omitempty"`
}

type ToolUseContent struct {
	Type  string          `json:"type"`
	ID    string          `json:"id,omitempty"`
	Name  string          `json:"name,omitempty"`
	Input json.RawMessage `json:"input,omitempty"`
}

type ToolResultContent struct {
	Type      string `json:"type"`
	ToolUseID string `json:"tool_use_id"`
	Content   string `json:"content"`
}

type Message struct {
	Role    string      `json:"role"`
	Content interface{} `json:"content"`
}

type Tool struct {
	Name        string                 `json:"name"`
	Description string                 `json:"description"`
	InputSchema map[string]interface{} `json:"input_schema"`
}

type ClaudeRequest struct {
	Model     string    `json:"model"`
	MaxTokens int       `json:"max_tokens"`
	Tools     []Tool    `json:"tools,omitempty"`
	Messages  []Message `json:"messages"`
}

type ClaudeResponse struct {
	ID         string           `json:"id"`
	Type       string           `json:"type"`
	Role       string           `json:"role"`
	ContentRaw []json.RawMessage `json:"content"`
	StopReason string           `json:"stop_reason"`
}

type Agent struct {
	APIKey string
	Client *http.Client
}

func NewAgent() (*Agent, error) {
	apiKey := os.Getenv("ANTHROPIC_API_KEY")
	if apiKey == "" {
		return nil, errors.New("missing ANTHROPIC_API_KEY")
	}

	return &Agent{
		APIKey: apiKey,
		Client: &http.Client{Timeout: 30 * time.Second},
	}, nil
}

func getTime() string {
	return time.Now().Format("2006-01-02 15:04:05")
}

func (a *Agent) call(messages []Message) (*ClaudeResponse, error) {
	body := ClaudeRequest{
		Model:     "claude-sonnet-4-5",
		MaxTokens: 512,
		Tools: []Tool{
			{
				Name:        "get_time",
				Description: "Get current local time",
				InputSchema: map[string]interface{}{
					"type":       "object",
					"properties": map[string]interface{}{},
					"required":   []string{},
				},
			},
		},
		Messages: messages,
	}

	payload, err := json.Marshal(body)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest(http.MethodPost, endpoint, bytes.NewReader(payload))
	if err != nil {
		return nil, err
	}
	req.Header.Set("content-type", "application/json")
	req.Header.Set("x-api-key", a.APIKey)
	req.Header.Set("anthropic-version", "2023-06-01")

	resp, err := a.Client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	raw, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return nil, fmt.Errorf("claude api error: status=%d body=%s", resp.StatusCode, string(raw))
	}

	var result ClaudeResponse
	if err := json.Unmarshal(raw, &result); err != nil {
		return nil, err
	}
	return &result, nil
}

func (a *Agent) Ask(input string) (string, error) {
	messages := []Message{
		{Role: "user", Content: input},
	}

	first, err := a.call(messages)
	if err != nil {
		return "", err
	}

	var assistantContent []interface{}
	var toolUse *ToolUseContent

	for _, raw := range first.ContentRaw {
		var probe struct {
			Type string `json:"type"`
		}
		if err := json.Unmarshal(raw, &probe); err != nil {
			return "", err
		}

		if probe.Type == "text" {
			var text TextContent
			if err := json.Unmarshal(raw, &text); err != nil {
				return "", err
			}
			assistantContent = append(assistantContent, text)
			if first.StopReason != "tool_use" {
				return text.Text, nil
			}
		}

		if probe.Type == "tool_use" {
			var tool ToolUseContent
			if err := json.Unmarshal(raw, &tool); err != nil {
				return "", err
			}
			assistantContent = append(assistantContent, tool)
			toolUse = &tool
		}
	}

	if toolUse == nil {
		return "", errors.New("no text and no tool_use returned")
	}

	var toolOutput string
	switch toolUse.Name {
	case "get_time":
		toolOutput = getTime()
	default:
		return "", fmt.Errorf("unknown tool: %s", toolUse.Name)
	}

	messages = append(messages, Message{
		Role:    "assistant",
		Content: assistantContent,
	})
	messages = append(messages, Message{
		Role: "user",
		Content: []ToolResultContent{
			{
				Type:      "tool_result",
				ToolUseID: toolUse.ID,
				Content:   toolOutput,
			},
		},
	})

	second, err := a.call(messages)
	if err != nil {
		return "", err
	}

	for _, raw := range second.ContentRaw {
		var text TextContent
		if err := json.Unmarshal(raw, &text); err == nil && text.Type == "text" {
			return text.Text, nil
		}
	}

	return "", errors.New("empty final answer")
}

func main() {
	agent, err := NewAgent()
	if err != nil {
		panic(err)
	}

	answer, err := agent.Ask("现在几点？")
	if err != nil {
		panic(err)
	}

	fmt.Println(answer)
}
```

## 整个流程

```text
用户输入
  ↓
Go 发送 messages + tools
  ↓
Claude 返回 tool_use
  ↓
Go 执行 getTime()
  ↓
Go 发送 tool_result
  ↓
Claude 生成最终回答
  ↓
Go 打印最终回答
```

## 本节学到什么

tool use 的本质不是“模型执行工具”，而是：

```text
模型决定要调用工具
程序负责真正执行工具
程序把执行结果交回模型
模型基于结果继续回答
```

下一节继续升级：把这个“模型思考 -> 行动 -> 观察 -> 再回答”的过程整理成 ReAct 循环。

[上一节：04. 把阻塞 JSON 响应改成流式输出](04-streaming-output.md) · [下一节：06. ReAct Agent](06-react-loop.md)

