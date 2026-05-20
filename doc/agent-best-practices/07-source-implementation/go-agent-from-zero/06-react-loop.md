# 06. ReAct Agent

[返回专题首页](README.md)

本节在 tool use 的基础上只增加一个能力：把一次工具调用整理成 ReAct 循环。

ReAct 的核心不是某个框架，而是一种执行节奏：

```text
Reason -> Act -> Observe -> Reason -> Final
```

在 Claude Messages API 里，对应关系是：

- `Reason`：Claude 根据用户任务判断下一步。
- `Act`：Claude 返回 `tool_use`。
- `Observe`：Go 执行工具并返回 `tool_result`。
- `Final`：Claude 基于工具结果输出最终答案。

## 本节任务

输入：

```text
请计算 12 * 8 + 5
```

期望流程：

```text
Claude 选择 calculator 工具
Go 执行 calculator
Go 返回 tool_result
Claude 输出最终答案：101
```

## 和上一节相比新增什么

上一节只处理一个固定工具 `get_time`。

本节改成一个通用循环：

```go
for step := 0; step < maxSteps; step++ {
	response := callClaude(messages)
	if response 有 text 且 stop_reason != tool_use {
		return final answer
	}
	if response 有 tool_use {
		执行工具
		append tool_result
		continue
	}
}
```

这就是最小 ReAct Agent。

## 工具定义

本节只定义一个工具：`calculator`。

```json
{
  "name": "calculator",
  "description": "Calculate a simple arithmetic expression",
  "input_schema": {
    "type": "object",
    "properties": {
      "expression": {
        "type": "string",
        "description": "Arithmetic expression, for example: 12 * 8 + 5"
      }
    },
    "required": ["expression"]
  }
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
	"go/ast"
	"go/parser"
	"go/token"
	"io"
	"net/http"
	"os"
	"strconv"
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
	System    string    `json:"system,omitempty"`
	Tools     []Tool    `json:"tools,omitempty"`
	Messages  []Message `json:"messages"`
}

type ClaudeResponse struct {
	Role       string            `json:"role"`
	ContentRaw []json.RawMessage `json:"content"`
	StopReason string            `json:"stop_reason"`
}

type Agent struct {
	APIKey string
	Client *http.Client
	Tools  []Tool
}

func NewAgent() (*Agent, error) {
	apiKey := os.Getenv("ANTHROPIC_API_KEY")
	if apiKey == "" {
		return nil, errors.New("missing ANTHROPIC_API_KEY")
	}

	return &Agent{
		APIKey: apiKey,
		Client: &http.Client{Timeout: 30 * time.Second},
		Tools:  []Tool{calculatorTool()},
	}, nil
}

func calculatorTool() Tool {
	return Tool{
		Name:        "calculator",
		Description: "Calculate a simple arithmetic expression",
		InputSchema: map[string]interface{}{
			"type": "object",
			"properties": map[string]interface{}{
				"expression": map[string]interface{}{
					"type":        "string",
					"description": "Arithmetic expression, for example: 12 * 8 + 5",
				},
			},
			"required": []string{"expression"},
		},
	}
}

func (a *Agent) call(messages []Message) (*ClaudeResponse, error) {
	body := ClaudeRequest{
		Model:     "claude-sonnet-4-5",
		MaxTokens: 512,
		System:    "You are a ReAct agent. Use tools when calculation is needed. After observing tool results, give the final answer.",
		Tools:     a.Tools,
		Messages:  messages,
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

func (a *Agent) Run(input string) (string, error) {
	messages := []Message{{Role: "user", Content: input}}
	const maxSteps = 4

	for step := 0; step < maxSteps; step++ {
		response, err := a.call(messages)
		if err != nil {
			return "", err
		}

		assistantContent, finalText, toolUses, err := parseContent(response.ContentRaw)
		if err != nil {
			return "", err
		}

		messages = append(messages, Message{Role: "assistant", Content: assistantContent})

		if response.StopReason != "tool_use" {
			return finalText, nil
		}

		var toolResults []ToolResultContent
		for _, toolUse := range toolUses {
			output, err := executeTool(toolUse)
			if err != nil {
				output = "tool error: " + err.Error()
			}
			toolResults = append(toolResults, ToolResultContent{
				Type:      "tool_result",
				ToolUseID: toolUse.ID,
				Content:   output,
			})
		}

		messages = append(messages, Message{Role: "user", Content: toolResults})
	}

	return "", errors.New("max steps reached")
}

func parseContent(raws []json.RawMessage) ([]interface{}, string, []ToolUseContent, error) {
	var assistantContent []interface{}
	var finalText string
	var toolUses []ToolUseContent

	for _, raw := range raws {
		var probe struct {
			Type string `json:"type"`
		}
		if err := json.Unmarshal(raw, &probe); err != nil {
			return nil, "", nil, err
		}

		switch probe.Type {
		case "text":
			var text TextContent
			if err := json.Unmarshal(raw, &text); err != nil {
				return nil, "", nil, err
			}
			assistantContent = append(assistantContent, text)
			finalText += text.Text
		case "tool_use":
			var tool ToolUseContent
			if err := json.Unmarshal(raw, &tool); err != nil {
				return nil, "", nil, err
			}
			assistantContent = append(assistantContent, tool)
			toolUses = append(toolUses, tool)
		}
	}

	return assistantContent, finalText, toolUses, nil
}

func executeTool(tool ToolUseContent) (string, error) {
	switch tool.Name {
	case "calculator":
		var input struct {
			Expression string `json:"expression"`
		}
		if err := json.Unmarshal(tool.Input, &input); err != nil {
			return "", err
		}
		value, err := evalArithmetic(input.Expression)
		if err != nil {
			return "", err
		}
		return strconv.FormatFloat(value, 'f', -1, 64), nil
	default:
		return "", fmt.Errorf("unknown tool: %s", tool.Name)
	}
}

func evalArithmetic(expression string) (float64, error) {
	expr, err := parser.ParseExpr(expression)
	if err != nil {
		return 0, err
	}
	return evalNode(expr)
}

func evalNode(node ast.Expr) (float64, error) {
	switch n := node.(type) {
	case *ast.BasicLit:
		return strconv.ParseFloat(n.Value, 64)
	case *ast.BinaryExpr:
		left, err := evalNode(n.X)
		if err != nil {
			return 0, err
		}
		right, err := evalNode(n.Y)
		if err != nil {
			return 0, err
		}
		switch n.Op {
		case token.ADD:
			return left + right, nil
		case token.SUB:
			return left - right, nil
		case token.MUL:
			return left * right, nil
		case token.QUO:
			return left / right, nil
		default:
			return 0, fmt.Errorf("unsupported operator: %s", n.Op)
		}
	case *ast.ParenExpr:
		return evalNode(n.X)
	default:
		return 0, fmt.Errorf("unsupported expression")
	}
}

func main() {
	agent, err := NewAgent()
	if err != nil {
		panic(err)
	}

	answer, err := agent.Run("请计算 12 * 8 + 5")
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
Reason: Claude 判断是否需要工具
  ↓
Act: Claude 返回 tool_use(calculator)
  ↓
Observe: Go 执行 calculator 并返回 tool_result
  ↓
Reason: Claude 读取观察结果
  ↓
Final: Claude 给出最终答案
```

## 本节学到什么

ReAct 不是神秘框架。最小实现就是一个循环：

```text
调用模型
如果模型要用工具，就执行工具
把工具结果发回模型
直到模型给最终答案
```

后续再继续扩展，可以把这个循环接到文件读写、数据库查询、MCP 工具、代码执行和多 Agent 协作。

[上一节：05. 增加 tool use](05-tool-use.md)

