# 02. 扩展成命令行循环

[返回专题首页](README.md)

本节在上一节基础上只增加一个能力：让程序进入命令行循环，用户可以连续输入问题。

注意：这一节还不保存多轮上下文。每次输入都会单独调用一次 Claude，模型看不到前面问过什么。保存上下文放到下一节。

## 本节任务

把上一节的一次性调用：

```text
启动程序 -> 问一个问题 -> 打印答案 -> 程序结束
```

改成循环调用：

```text
启动程序 -> 输入问题 -> 打印答案 -> 继续输入问题 -> 输入 exit 退出
```

## 和上一节相比新增什么

只新增命令行循环：

```go
scanner := bufio.NewScanner(os.Stdin)
for {
	fmt.Print("> ")
	if !scanner.Scan() {
		break
	}

	input := strings.TrimSpace(scanner.Text())
	if input == "exit" || input == "quit" {
		break
	}

	answer, err := agent.Ask(input)
	// 打印 answer
}
```

`Agent.Ask` 仍然和上一节一样：每次只把当前用户输入发给 Claude。

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

		answer, err := agent.Ask(input)
		if err != nil {
			fmt.Println("error:", err)
			continue
		}

		fmt.Println(answer)
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
> 用一句话解释什么是 Agent
Agent 是一个能根据目标自主调用模型、工具或流程来完成任务的软件执行单元。
> Go 语言适合写 Agent 吗？
适合，因为 Go 的并发、网络库和部署体验都很适合构建稳定的 Agent 后端服务。
> exit
```

## 整个流程

```text
程序启动
  ↓
创建 Agent
  ↓
进入 for 循环
  ↓
读取一行用户输入
  ↓
调用 agent.Ask(input)
  ↓
HTTP POST /v1/messages
  ↓
解析 content[0].text
  ↓
打印结果
  ↓
回到下一轮输入
```

## 本节学到什么

这一节只是在上一节外面包了一层循环。Agent 的调用方式没有变，仍然是：

```text
一次用户输入 -> 一次 Claude 请求 -> 一次 Claude 回答
```

所以这一节能连续聊天，但还不是多轮对话。因为每次请求的 `messages` 里只有当前这次用户输入。

下一节继续在这个基础上改：把每一轮的 user 和 assistant 消息保存下来，下次请求时把完整 `messages` 一起发给 Claude。

[上一节：01. 调用 API 实现最小 Agent](01-api-call.md) · [下一节：03. 保存多轮对话上下文](03-multi-turn-context.md)

