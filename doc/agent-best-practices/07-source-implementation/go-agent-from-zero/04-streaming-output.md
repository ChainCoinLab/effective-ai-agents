# 04. 把阻塞 JSON 响应改成流式输出

[返回专题首页](README.md)

本节在前面命令行 Agent 的基础上只增加一个能力：把一次性返回的 JSON，改成流式输出。

前面几节的调用方式是：请求发出后一直等待，Claude 生成完整回答后，Go 再解析 JSON，最后一次性打印 `content[0].text`。

这一节改成：请求里加 `stream: true`，Go 读取 SSE 事件，收到一段 `text_delta` 就立刻打印一段。

## 本节任务

输入：

```text
写三句话解释 Go 为什么适合做 Agent 后端
```

输出效果：

```text
Go 的网络库稳定，适合封装 API 调用。
Go 的并发模型简单，适合同时处理多个任务。
Go 编译成单个二进制文件，部署 Agent 服务很方便。
```

区别是：这三句话不是等全部生成完再一次性出现，而是边生成边打印。

## 和上一节相比新增什么

请求体新增：

```json
{
  "stream": true
}
```

Go 结构体新增：

```go
Stream bool `json:"stream,omitempty"`
```

响应解析从：

```go
json.Unmarshal(raw, &result)
return result.Content[0].Text, nil
```

改成：

```go
逐行读取 SSE
遇到 content_block_delta
取 delta.text
立刻 fmt.Print(text)
```

## 流式请求 JSON

```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 512,
  "stream": true,
  "messages": [
    {
      "role": "user",
      "content": "写三句话解释 Go 为什么适合做 Agent 后端"
    }
  ]
}
```

## SSE 里真正有用的事件

Claude 会返回一串 SSE 事件。我们这一节只关心 `content_block_delta`：

```text
event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Go 的网络库稳定"}}
```

真正要打印的是：

```text
delta.text
```

## 完整 main.go

```go
package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
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
	Stream    bool      `json:"stream,omitempty"`
	Messages  []Message `json:"messages"`
}

type StreamDelta struct {
	Type string `json:"type"`
	Text string `json:"text"`
}

type StreamEvent struct {
	Type  string      `json:"type"`
	Delta StreamDelta `json:"delta"`
}

type Agent struct {
	APIKey   string
	Client   *http.Client
	Messages []Message
}

func NewAgent() (*Agent, error) {
	apiKey := os.Getenv("ANTHROPIC_API_KEY")
	if apiKey == "" {
		return nil, errors.New("missing ANTHROPIC_API_KEY")
	}

	return &Agent{
		APIKey:   apiKey,
		Client:   &http.Client{Timeout: 60 * time.Second},
		Messages: []Message{},
	}, nil
}

func (a *Agent) AskStream(input string) (string, error) {
	a.Messages = append(a.Messages, Message{Role: "user", Content: input})

	body := ClaudeRequest{
		Model:     "claude-sonnet-4-5",
		MaxTokens: 512,
		Stream:    true,
		Messages:  a.Messages,
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

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		raw, _ := io.ReadAll(resp.Body)
		return "", fmt.Errorf("claude api error: status=%d body=%s", resp.StatusCode, string(raw))
	}

	var answer strings.Builder
	scanner := bufio.NewScanner(resp.Body)
	scanner.Buffer(make([]byte, 1024), 1024*1024)

	for scanner.Scan() {
		line := scanner.Text()
		if !strings.HasPrefix(line, "data: ") {
			continue
		}

		data := strings.TrimPrefix(line, "data: ")
		var event StreamEvent
		if err := json.Unmarshal([]byte(data), &event); err != nil {
			continue
		}

		if event.Type == "content_block_delta" && event.Delta.Type == "text_delta" {
			fmt.Print(event.Delta.Text)
			answer.WriteString(event.Delta.Text)
		}
	}
	fmt.Println()

	if err := scanner.Err(); err != nil {
		return "", err
	}

	text := answer.String()
	a.Messages = append(a.Messages, Message{Role: "assistant", Content: text})
	return text, nil
}

func main() {
	agent, err := NewAgent()
	if err != nil {
		panic(err)
	}

	fmt.Println("Go Agent 已启动。输入 exit 或 quit 退出。")

	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Print("> ")
		if !scanner.Scan() {
			break
		}

		input := strings.TrimSpace(scanner.Text())
		if input == "" {
			continue
		}
		if input == "exit" || input == "quit" {
			break
		}

		if _, err := agent.AskStream(input); err != nil {
			fmt.Println("error:", err)
		}
	}
}
```

## 整个流程

```text
用户输入
  ↓
Go 拼 ClaudeRequest，并设置 stream=true
  ↓
HTTP POST /v1/messages
  ↓
Claude 持续返回 SSE
  ↓
Go 逐行读取 data
  ↓
遇到 text_delta 就打印 delta.text
  ↓
把完整 answer 保存回 messages
```

## 本节学到什么

这一节没有改变 Agent 的思考能力，只改变响应方式：

- 非流式：等完整 JSON 返回后再显示。
- 流式：一边接收 SSE，一边打印 `text_delta`。

下一节继续加能力：让模型不只是回答文本，而是能提出工具调用请求。

[上一节：03. 保存多轮对话上下文](03-multi-turn-context.md) · [下一节：05. 增加 tool use](05-tool-use.md)

