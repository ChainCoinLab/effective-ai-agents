# 03. 保存多轮对话上下文

[返回专题首页](README.md)

本节在上一节基础上只增加一个能力：保存多轮对话上下文。

Claude Messages API 是无状态的。模型不会自动记住上一次请求。想让它知道历史对话，就必须在每次请求时把完整的 `messages` 数组重新发过去。

## 本节任务

让程序能理解连续对话：

```text
> 我叫小明，请记住
好的，我记住了，你叫小明。
> 我叫什么？
你叫小明。
```

上一节做不到这个效果，因为每次请求只发送当前输入。本节要把历史消息保存到 Agent 里。

## 和上一节相比新增什么

上一节的 Agent 只有配置：

```go
type Agent struct {
	APIKey string
	Client *http.Client
}
```

本节新增 `Messages`：

```go
type Agent struct {
	APIKey   string
	Client   *http.Client
	Messages []Message
}
```

每次用户提问时：

1. 把用户输入 append 到 `Messages`。
2. 把完整 `Messages` 发给 Claude。
3. 从响应里取 `content[0].text`。
4. 把 Claude 回答也 append 到 `Messages`。

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
		Client:   &http.Client{Timeout: 30 * time.Second},
		Messages: []Message{},
	}, nil
}

func (a *Agent) Ask(input string) (string, error) {
	a.Messages = append(a.Messages, Message{
		Role:    "user",
		Content: input,
	})

	body := ClaudeRequest{
		Model:     "claude-sonnet-4-5",
		MaxTokens: 512,
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

	answer := result.Content[0].Text
	a.Messages = append(a.Messages, Message{
		Role:    "assistant",
		Content: answer,
	})

	return answer, nil
}

func main() {
	agent, err := NewAgent()
	if err != nil {
		panic(err)
	}

	fmt.Println("Go Agent 已启动。输入 exit 或 quit 退出，输入 history 查看当前 messages。")

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
		if input == "history" {
			printHistory(agent.Messages)
			continue
		}

		answer, err := agent.Ask(input)
		if err != nil {
			fmt.Println("error:", err)
			continue
		}

		fmt.Println(answer)
	}
}

func printHistory(messages []Message) {
	for i, msg := range messages {
		fmt.Printf("%d. %s: %s\n", i+1, msg.Role, msg.Content)
	}
}
```

## 运行

```bash
export ANTHROPIC_API_KEY="你的 API Key"
go run main.go
```

输入示例：

```text
> 我叫小明，请记住
好的，我记住了，你叫小明。
> 我叫什么？
你叫小明。
> history
1. user: 我叫小明，请记住
2. assistant: 好的，我记住了，你叫小明。
3. user: 我叫什么？
4. assistant: 你叫小明。
```

## 本节请求 JSON 的变化

第一轮请求：

```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 512,
  "messages": [
    {
      "role": "user",
      "content": "我叫小明，请记住"
    }
  ]
}
```

第二轮请求：

```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 512,
  "messages": [
    {
      "role": "user",
      "content": "我叫小明，请记住"
    },
    {
      "role": "assistant",
      "content": "好的，我记住了，你叫小明。"
    },
    {
      "role": "user",
      "content": "我叫什么？"
    }
  ]
}
```

关键点：不是 Claude 自动记住了你，而是 Go 程序把历史消息重新发了一遍。

## 整个流程

```text
用户输入
  ↓
append user 到 agent.Messages
  ↓
把完整 messages 发给 Claude
  ↓
Claude 返回 JSON
  ↓
读取 content[0].text
  ↓
append assistant 到 agent.Messages
  ↓
打印结果
  ↓
下一轮继续携带完整 messages
```

## 本节学到什么

这一节把命令行循环升级成了真正的多轮对话。区别在于：

- 02 节：每轮请求只有当前输入。
- 03 节：每轮请求都携带完整历史 `messages`。

这就是 Agent 里最基础的短期上下文管理。

[上一节：02. 扩展成命令行循环](02-cli-loop.md)

