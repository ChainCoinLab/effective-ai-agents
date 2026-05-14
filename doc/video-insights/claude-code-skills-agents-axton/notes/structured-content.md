# Claude Code: 从零搭建你的 AI 工作团队（Skills + Agents）

来源: https://www.bilibili.com/video/BV1eADaBME5z  
作者: 回到Axton  
时长: 20:27  
处理方式: 已下载完整视频和音频，使用本地 `faster-whisper` 完整转写，结合关键帧补充画面信息。

## 已获取素材

- 原始视频: `../source.mp4`
- 原始音频: `../audio.m4a`
- 完整转写: `transcript.txt`
- 术语清洗转写: `transcript.cleaned.txt`
- 时间轴字幕: `transcript.srt`
- 分段 JSON: `transcript.json`
- 关键帧目录: `../frames/`

## 一句话概括

这是一套用 Claude Code 搭建“个人 AI 工作团队”的实操教程：先把稳定流程沉淀成 Skills，再创建具备明确职责的 Agents，让 Agent 按 Skill 执行内容审查、微信公众号发布、社交内容改写等任务。

## 核心观点

1. Skill 是“标准操作手册”，用于把人的经验、判断标准、流程和输出格式固定下来。
2. Agent 是“团队成员”，负责在合适场景调用一个或多个 Skill 执行任务。
3. 正确顺序是先设计流程，再创建 Agent；不要一开始就给 Agent 一个宽泛目标让它自行发挥。
4. 复杂任务应由 Agent 串联多个 Skills 形成流水线，简单任务可以只靠 Agent 的系统提示词完成。
5. Claude Code 可以在桌面端、终端、Cursor 等编辑器里使用；教程选择 Cursor 是为了同时展示项目文件结构和 Claude 对话界面。

## 内容结构

### 0:00-1:14 开场与目标

作者提出目标：搭建一个 AI 团队，覆盖信息筛选、内容审查、多平台发布等全流程。视频要从零搭建两个核心对象：

- `Skills`: 给 AI 的标准操作手册。
- `Agents`: 有明确职责的 AI 团队成员，知道何时使用什么 Skill。

作者说明即使不懂编程也可以跟着做，因为操作主要在 Cursor 里的 Claude Code 插件中完成，不需要手写代码。

### 1:14-2:32 Claude Code 使用方式与项目结构

Claude Code 有三种使用方式：

- 桌面端 App。
- 终端窗口。
- Cursor 等编辑器内插件。

教程项目名为 `my-ai-team`，基础结构包括：

- `context/`: 基础资料，例如写作风格、审查标准、发布规范。
- `templates/`: 模板。
- `articles/`: 等待处理的文章。
- `skills/`: 后续创建的 Skills。
- `agents/`: 后续创建的 Agents。

`context/` 是 AI 团队理解用户偏好、标准和业务背景的基础。

### 2:32-4:04 初始化 `CLAUDE.md` 与安装官方 Skills

第一步是在 Claude Code 对话框输入 `/init`，生成 `CLAUDE.md`。作者把它比作 AI 团队的“入职手册”：Claude 每次打开项目会话时会读取它，了解项目背景、规则和偏好。

随后通过 `/plugin` 添加 Anthropic 官方 Skill 仓库，并安装 `skill-creator`。这个 Skill 用来帮助创建和优化自定义 Skills。安装后需要重启 Claude Code 才能生效。

术语说明：视频里提到的 plugin 和 skill 在当前语境里基本指同类机制。

### 4:04-8:05 创建 `content-review` Skill

第一个 Skill 是内容审查 Skill。目标是接收一篇文章，用两个不同模型从不同角度审查，再合并成一份报告。

设计原因：

- 同一个模型审查自己的输出容易有系统性盲区。
- 不同模型交叉检查能发现更多问题。
- Claude 负责逻辑和结构。
- Gemini 通过 Gemini CLI 负责事实准确性和风格一致性。

作者先准备 `context/review-standards.md`，里面包含审查维度，例如：

- 逻辑是否自洽。
- 事实是否可验证。
- 语气是否一致。
- 是否有 AI 味过重的表达。

创建 Skill 的提示词大意：

```text
根据 context/review-standards.md 里的审查标准，
帮我创建一个 Claude Code Skill，叫 content-review。
这个 Skill 接受一篇文章：
先用 Claude 从逻辑和结构维度审查；
再用 Gemini CLI 从事实准确性和风格一致性维度审查；
最后汇总两边发现，输出一份审查报告。
把 Skill 创建在 skills/content-review 目录下。
```

生成后的 `skills/content-review/SKILL.md` 定义了：

- 触发条件。
- 审查流程。
- 输出格式。
- Claude 与 Gemini 的分工。
- 最终报告合并方式。

### 6:32-8:05 测试 `content-review`

作者用 `articles/sample-newsletter-draft.md` 测试新 Skill。执行后 Skill 同时启动 Claude 分析和 Gemini 调用，最后生成审查报告。

示例结果中：

- Claude 发现结构问题、比喻矛盾、结尾缺乏可执行 takeaway。
- Gemini 发现泛化断言缺少来源、部分表达过于绝对、术语使用需要调整。

作者强调：这说明 Skill 的价值在于提前设计分工，让 AI 按照设计执行，而不是把所有判断都交给一个模型。

### 8:05-9:35 创建 `wechat-publish` Skill

第二个 Skill 是微信公众号发布 Skill。它不只是处理文本，而是要通过外部工具执行发布动作，因此需要 MCP。

MCP 在视频中的解释是：AI 与外部工具之间的桥梁。

作者已经配置好 Make 的 MCP 服务，并通过 `/mcp` 检查连接状态。Make 的 MCP 在线后，Claude Code 可以直接调用 Make 上的工作流，不需要手动到 Make 后台点击运行。

创建 Skill 的提示词大意：

```text
帮我创建一个 Skill，叫 wechat-publish。
它接收一篇 Markdown 格式的定稿文章，
通过 MCP 调用 Make 的微信公众号发布 Scenario，
自动完成发布。
把 Skill 创建在 skills/wechat-publish 目录下。
```

生成后的流程包括：

1. 读取并校验文章。
2. 组装文章元数据。
3. 请求用户确认。
4. 调用 MCP/Make。
5. 报告发布结果。

### 9:35-10:55 为什么先做 Skill 再做 Agent

作者用创业公司类比解释顺序：

- 不应该直接招一个 CEO 然后只给目标“赚 100 万”，让它自己看着办。
- 正常做法是创始人先把业务流程跑通，明确哪些环节需要判断、哪些是执行、标准是什么。
- 把这些流程写下来，就是 Skill。
- 再招人来按流程干活，就是 Agent。

结论：

```text
先订流程，再配人。
Skill 是流程，Agent 是执行者。
```

### 10:55-14:00 创建 `publisher` Agent

第一个 Agent 是发布运营 Agent，负责把一篇定稿文章从审查推进到发布。

创建方式：

1. 打开终端。
2. 进入 Claude Code。
3. 输入 `/agents`。
4. 创建新的 Agent。
5. 选择项目级创建。
6. 选择手动配置。

配置项包括：

- 名称: `publisher`
- 职责: 发布运营 Agent。
- 工作流程: 先用 `content-review` 做质量审查，通过后再用 `wechat-publish` 发布到微信公众号。
- 触发条件: 用户要求发布、审查并发布、把文章推送到公众号等。
- 工具权限: 演示中默认全选，作者提醒实际使用应只给必要权限。
- 模型: 默认 Sonnet。
- 颜色: 绿色。
- Memory 范围: 当前项目。

保存后会在 `.claude/agents/` 下生成 `publisher.md`。作者还手动修改 Agent 的 frontmatter，加入它需要加载的 Skills，并确保名称和文件名一致，避免混淆。

### 14:00-15:40 测试 `publisher` Agent

作者让 `publisher` Agent 把 newsletter 草稿发布到微信公众号。

执行链路：

1. Agent 被触发。
2. 先调用 `content-review` Skill 做质量审查。
3. 审查通过后调用 `wechat-publish` Skill。
4. `wechat-publish` 通过 Make MCP 调用微信公众号发布 Scenario。
5. 文章进入微信公众号草稿箱。

示例文章标题为“从消费智能到编排智能：AI 时代的工作方式”。作者强调这只是测试 newsletter，不是正式内容。

这个测试证明：Agent 可以根据设定先审查，再发布，而不是直接执行最终动作。

### 15:40-17:40 创建 `demo-social-voice` Agent

第二个 Agent 是社交互动 Agent，用来说明不是所有 Agent 都需要 Skill。

它的职责是把长内容转换成适合社交媒体传播的短内容，例如推文。这个 Agent 不装备任何 Skill，只依靠 Claude 的基础能力和系统提示词。

配置项包括：

- 名称: `demo-social-voice`
- 职责: 社交互动 Agent。
- 系统提示词: 负责把长内容转换成社交传播短内容。
- 触发条件: “写条推文”“帮我发个推”“把这篇转成推文”等。
- 模型: Sonnet。
- Memory 范围: 当前项目。

作者用 newsletter 草稿测试它，生成一条推文。创建后如果 Agent 没被立即识别，需要刷新或重新加载。

### 17:40-19:18 扩展成完整 AI 工作团队

作者总结两种 Agent 配置：

- `publisher`: 装备两个 Skills，走“审查 -> 发布”的完整流水线。
- `demo-social-voice`: 不装备 Skill，只靠系统提示词完成简单改写任务。

扩展方式：

- 内容策划 Agent: 配选题分析、脚本创作 Skills。
- 视觉设计 Agent: 配图、封面图 Skills。
- 多平台发布 Agent: 配不同平台发布 Skills。

作者自己的系统中有 12 个 Agent，覆盖：

- 信息筛选。
- 内容策划。
- 视频制作。
- 视觉设计。
- 多平台发布。

它们各自有职责、Skills 和协作规则。完整系统可以一条命令启动，自动筛选本周 AI 重点新闻，查知识库中的历史观点，写 newsletter，自动配图，并通过 MCP 一键发布到微信公众号。过程中作者只介入一次。

### 19:18-20:27 进一步学习路径

作者推广自己的书《重构个体：AI 时代如何打造个人竞争力》。他强调视频讲的是操作层面，但真正有效的系统还需要四个能力：

- 心智: 判断工作流哪里该用 AI，哪里不该用。
- 架构: 设计能随工具变化而替换的蓝图。
- 提示词: 与 AI 精准沟通，让输出稳定可靠。
- 系统: 把能力组装成真正跑起来的工作系统。

最后预告下一期会讲“从旁观者到架构师”的 AI 使用段位。

## 可复用操作清单

### 准备项目

```text
my-ai-team/
  context/
    review-standards.md
    style-guide.md
    publish-config.md
  templates/
  articles/
  skills/
  agents/
```

### 初始化项目上下文

在 Claude Code 对话框输入：

```text
/init
```

生成 `CLAUDE.md`，作为项目级说明和规则入口。

### 安装基础 Skill

在 Claude Code 中通过 plugin/skills 机制添加 Anthropic 官方 Skill 仓库，并安装：

```text
skill-creator
```

安装后重启 Claude Code。

### 创建内容审查 Skill

关键输入：

```text
根据 context/review-standards.md 创建 content-review Skill。
Claude 审查逻辑和结构。
Gemini CLI 审查事实准确性和风格一致性。
合并输出审查报告。
目录: skills/content-review
```

### 创建微信公众号发布 Skill

前置条件：

- 已配置 Make 工作流。
- Claude Code 已连接 Make MCP。
- `/mcp` 能看到 Make 服务在线。

关键输入：

```text
创建 wechat-publish Skill。
接收 Markdown 定稿文章。
通过 MCP 调用 Make 微信公众号发布 Scenario。
输出发布结果。
目录: skills/wechat-publish
```

### 创建发布 Agent

在终端 Claude Code 中输入：

```text
/agents
```

配置：

```text
name: publisher
role: 发布运营 Agent
workflow:
  1. 使用 content-review 审查文章
  2. 审查通过后使用 wechat-publish 发布到微信公众号
model: Sonnet
memory: project
skills:
  - content-review
  - wechat-publish
```

### 创建社交改写 Agent

```text
name: demo-social-voice
role: 社交互动 Agent
workflow:
  - 把长内容改写成适合社交媒体传播的短内容
skills: 无
```

## 适合落地的系统设计模式

### 模式一：审查型 Skill

适用于文章、脚本、方案、PRD、代码审查。

结构：

```text
输入材料 -> 多维度审查 -> 合并问题 -> 按严重程度输出报告
```

关键是把审查标准写进 `context/`，不要只靠模型临场判断。

### 模式二：发布型 Skill

适用于微信公众号、X、LinkedIn、飞书、Notion、WordPress 等平台。

结构：

```text
读取内容 -> 校验格式 -> 组装元数据 -> 用户确认 -> 调用外部工具 -> 回报结果
```

关键是通过 MCP 或 API 连接外部平台，并在真正发布前加入确认环节。

### 模式三：流水线 Agent

适用于复杂任务，例如“审查并发布文章”。

结构：

```text
Agent 触发 -> Skill A 审查 -> 条件判断 -> Skill B 发布 -> 结果回报
```

### 模式四：轻量 Agent

适用于简单改写、摘要、社交文案、标题生成。

结构：

```text
Agent 触发 -> 系统提示词约束 -> 直接输出
```

不需要为每个小任务都创建 Skill。

## 关键判断准则

- 流程稳定、会重复执行: 做成 Skill。
- 需要明确角色、触发条件和长期职责: 做成 Agent。
- 需要调用外部工具或平台: 用 MCP/API，并封装为 Skill。
- 任务简单、一次性、没有复杂流程: 只用 Agent 或普通 Claude 对话即可。
- 涉及发布、删除、付款等外部动作: 必须加入用户确认。

## 本视频的最终结论

Claude Code 的 Skills + Agents 不是为了“让 AI 更自由”，而是为了让 AI 更可控。先把人的流程、标准和边界写成 Skill，再让 Agent 承担角色并调用 Skill，才能把一次性对话升级成可复用的工作系统。

