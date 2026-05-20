# 01. 调用 API 实现最小 Agent

[返回专题首页](README.md)

本节只完成一个小任务：用 Go 发起一次 HTTP 请求，调用 Claude 大模型，并把模型回答打印出来。

这一节不做循环聊天、不保存上下文、不接数据库、不接 MCP，也不使用 SDK。先看清楚一次大模型调用的 JSON 长什么样、哪些字段必传、返回结果在哪里取。

## 本节任务

输入：

```text
用一句话解释什么是 Agent
```

输出：

```text
Agent 是一个能根据目标自主调用模型、工具或流程来完成任务的软件执行单元。
```

## 最小请求 JSON

Go 程序最终要发给 Claude 的请求体：

```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 256,
  "messages": [
    {
      "role": "user",
      "content": "用一句话解释什么是 Agent"
    }
  ]
}
```

最小调用只需要三个 body 字段：

- `model`：调用哪个 Claude 模型。
- `max_tokens`：最多生成多少 token。
- `messages`：本次对话消息，最少要有一条 `user` 消息。

`system` 不是这一节的必传字段。先不加，等单次调用跑通后再进入后面的学习点。

## 必传字段

| 位置 | 字段 | 必传 | 示例 |
| --- | --- | --- | --- |
| Header | `x-api-key` | 是 | 从 `ANTHROPIC_API_KEY` 环境变量读取 |
| Header | `anthropic-version` | 是 | `2023-06-01` |
| Header | `content-type` | 是 | `application/json` |
| Body | `model` | 是 | `claude-sonnet-4-5` |
| Body | `max_tokens` | 是 | `256` |
| Body | `messages` | 是 | `[{"role":"user","content":"..."}]` |
| Body.messages[] | `role` | 是 | `user` |
| Body.messages[] | `content` | 是 | 用户输入文本 |

## Go 里的 JSON 定义

```go
type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type ClaudeRequest struct {
	Model     string    `json:"model"`
	MaxTokens int       `json:"max_tokens"`
	Messages  []Message `json:"messages"`
}

type ContentBlock struct {
	Type string `json:"type"`
	Text string `json:"text"`
}

type ClaudeResponse struct {
	ID      string         `json:"id"`
	Type    string         `json:"type"`
	Role    string         `json:"role"`
	Content []ContentBlock `json:"content"`
}
```

这里只定义当前闭环要用的字段。Claude 实际响应里还有 `model`、`stop_reason`、`usage` 等字段，第一步先不用。

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

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type ClaudeRequest struct {
	Model     string    `json:"model"`
	MaxTokens int       `json:"max_tokens"`
	Messages  []Message `json:"messages"`
}

type ContentBlock struct {
	Type string `json:"type"`
	Text string `json:"text"`
}

type ClaudeResponse struct {
	ID      string         `json:"id"`
	Type    string         `json:"type"`
	Role    string         `json:"role"`
	Content []ContentBlock `json:"content"`
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

func (a *Agent) Ask(input string) (string, error) {
	body := ClaudeRequest{
		Model:     "claude-sonnet-4-5",
		MaxTokens: 256,
		Messages: []Message{
			{Role: "user", Content: input},
		},
	}

	payload, err := json.Marshal(body)
	if err != nil {
		return "", err
	}

	req, err := http.NewRequest(http.MethodPost, endpoint, bytes.NewReader(payload))
	if err != nil {
		return "", err
	}

	req.Header.Set("content-type", "application/json")
	req.Header.Set("x-api-key", a.APIKey)
	req.Header.Set("anthropic-version", "2023-06-01")

	resp, err := a.Client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	raw, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return "", fmt.Errorf("claude api error: status=%d body=%s", resp.StatusCode, string(raw))
	}

	var result ClaudeResponse
	if err := json.Unmarshal(raw, &result); err != nil {
		return "", err
	}
	if len(result.Content) == 0 {
		return "", errors.New("empty response content")
	}

	return result.Content[0].Text, nil
}

func main() {
	agent, err := NewAgent()
	if err != nil {
		panic(err)
	}

	answer, err := agent.Ask("用一句话解释什么是 Agent")
	if err != nil {
		panic(err)
	}

	fmt.Println(answer)
}
```

## 运行

```bash
export ANTHROPIC_API_KEY="你的 API Key"
go run main.go
```

## Claude 返回的 JSON

Claude 返回的完整 JSON 大概长这样：

```json
{
  "id": "msg_...",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Agent 是一个能根据目标自主调用模型、工具或流程来完成任务的软件执行单元。"
    }
  ],
  "model": "claude-sonnet-4-5",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 18,
    "output_tokens": 32
  }
}
```

真正要打印的回答内容在：

```text
content[0].text
```

所以 Go 代码最后返回：

```go
return result.Content[0].Text, nil
```

## 整个流程

```text
用户输入
  ↓
Go 拼 ClaudeRequest
  ↓
json.Marshal 变成 JSON
  ↓
HTTP POST /v1/messages
  ↓
Claude 返回 JSON
  ↓
json.Unmarshal 解析 ClaudeResponse
  ↓
读取 content[0].text
  ↓
打印结果
```

## 本节学到什么

这一节的 Agent 本质是四步：

1. 接收用户输入。
2. 把输入包装成 Claude API 需要的 JSON。
3. 调用大模型。
4. 从返回 JSON 里取出答案。

下一节在这个基础上加一个能力：不要只问一次，而是让命令行进入循环，可以连续提问。

[下一节：02. 扩展成命令行循环](02-cli-loop.md)

