# 12. Transformer 如何一步步形成

[返回本章](README.md)

![Transformer block 的组成](../assets/diagrams/transformer-block-stack.svg)

图解导读：Transformer 可以从序列模型对比、QKV 机制、逐 token 生成三个角度一起理解。

## 核心问题

为什么现代大模型基本建立在 Transformer 上？

上一节讲了 Attention：模型可以让 token 直接参考上下文里的相关 token。但只有 Attention 还不够。一个能训练到很深、能生成文本、能利用大规模数据的语言模型，还需要表示输入、表达位置、组合多种关系、增加非线性能力，并且让训练过程稳定。

Transformer 的价值不只是“用了 attention”。它是一套把这些需求拼成可扩展神经网络的架构。

## 推导线索

```text
文本先被切成 token
→ token id 需要变成向量，也就是 token embedding
→ 序列还需要位置信息，也就是 position embedding / position encoding
→ token 之间通过 Self-attention 建立关系
→ 单一注意力视角不够，所以引入 multi-head attention
→ 只混合上下文还不够，所以加入 FFN 做逐位置非线性变换
→ 网络变深后容易难训，所以加入 residual connection
→ 激活尺度需要稳定，所以加入 LayerNorm / RMSNorm
→ 生成任务不能偷看未来 token，所以加入 causal mask
→ 多个 block 堆叠后形成 decoder-only 语言模型
```

## Transformer block 的整体图景

直觉层看，Transformer block 像一轮“读上下文、思考加工、保持稳定”的循环：

```text
输入 token 表示
  → Self-attention：和上下文交换信息
  → residual + norm：保留原信息并稳定数值
  → FFN：对每个位置做更强的非线性加工
  → residual + norm：再次保留并稳定
  → 输出给下一层
```

很多现代 decoder-only 模型使用 pre-norm 变体，顺序更接近：

```text
x
→ x + SelfAttention(Norm(x))
→ x + FFN(Norm(x))
→ 下一层
```

不同模型会在细节上变化，例如用 LayerNorm 或 RMSNorm，用绝对位置编码或 RoPE，用不同激活函数或 FFN 结构。但核心思想一致：Attention 负责跨 token 交流，FFN 负责逐 token 加工，残差和归一化负责让深层堆叠可训练。

先把一个 block 里的主要组件放在同一张表里，后面再逐个展开。这样可以看到 Transformer 不是单个技巧，而是一组互相补位的结构。

| 组件 | 主要职责 | 解决的问题 | 缺少时的风险 |
| --- | --- | --- | --- |
| token embedding | 把 token id 变成向量 | 让离散符号可计算 | 模型无法处理文本符号 |
| Position embedding / encoding | 注入顺序信息 | 区分相同 token 的不同位置 | “我喜欢你”和“你喜欢我”难以区分 |
| Self-attention | 跨 token 汇总上下文 | 建立指代、引用、依赖关系 | 只能靠局部或压缩状态 |
| Multi-head attention | 并行捕捉多种关系 | 同时处理语法、实体、格式等线索 | 单一视角表达不足 |
| FFN / MLP | 对每个位置做非线性加工 | 增强组合和抽象能力 | 只做信息混合，表达力受限 |
| Residual connection | 保留输入并叠加变化量 | 支撑深层信息和梯度传递 | 深层网络更难训练 |
| LayerNorm / RMSNorm | 稳定激活尺度 | 控制深层数值波动 | 训练不稳定、梯度难优化 |
| Causal mask | 屏蔽未来 token | 保持自回归训练目标成立 | 训练时会偷看答案 |

这张表也解释了为什么只说“Transformer 等于 Attention”是不够的：Attention 负责上下文交流，但可训练、可生成、可扩展还依赖其他组件。

初学者先掌握这几个核心组件就够了：token embedding、position embedding / encoding、Self-attention、multi-head attention、FFN、residual connection、normalization、causal mask。后面出现的 RoPE、RMSNorm、SwiGLU、MQA / GQA、MoE、FlashAttention 等，是现代模型的常见变体或优化，先知道它们在改进位置表示、归一化、FFN、KV cache 或计算效率即可，不影响本节主线。

## token embedding：把离散符号变成连续向量

模型不能直接计算汉字、英文单词或代码字符。文本会先被 tokenizer 切成 token，再映射成 token id。embedding 层把每个 id 查表成一个向量。

直觉层看，embedding 像给每个 token 发一张“可学习的身份证”。训练开始时，这张身份证基本是随机的；训练过程中，模型会调整它，让语义、语法、格式或用法相近的 token 在向量空间里形成有用关系。

机制层看，embedding 表本质上是一个矩阵：

```text
token id → embedding table 查表 → token vector
```

形式层上，如果词表大小是 `V`，向量维度是 `d_model`，embedding 表就是一个 `V x d_model` 的参数矩阵。输入序列长度为 `n` 时，模型得到一个 `n x d_model` 的向量序列。

工程层上，tokenizer 和 embedding 会影响成本与能力。切分方式决定同一段文本会变成多少 token；token 越多，上下文成本越高，attention 计算也越贵。词表设计还影响多语言、代码、数字、特殊格式和工具调用协议的处理效果。

## Position embedding：让模型知道顺序

Self-attention 本身不天然知道 token 顺序。如果不加入位置信息，“我喜欢你”和“你喜欢我”在纯集合意义上包含相同 token，但意义完全不同。

直觉层看，位置编码是在告诉模型：每个 token 不只是“是什么”，还要知道“在哪里”。语言里的先后顺序会决定主谓宾、因果、引用范围、代码作用域和对话轮次。

机制层上，常见方式包括：

- 绝对位置编码：给第 1、2、3 个位置分别提供位置向量，再与 token embedding 结合。
- 相对位置思想：让模型更关注 token 之间的距离和相对顺序。
- RoPE：通过旋转位置嵌入把位置信息融入 Q / K，使 attention 分数能感知相对位置。

形式层不必背复杂公式，但要抓住一点：位置不是独立模块最后再解释结果，而是参与 attention 计算本身。尤其在 RoPE 这类方法里，位置会影响 query 和 key 的匹配方式，从而影响“该看谁”。

工程层上，位置编码影响上下文长度扩展。模型训练时见过的长度、位置方法的外推能力、RoPE scaling 等技术，都会影响长上下文是否稳定。工程上不能只看模型宣称的最大窗口，还要评估它在长距离引用、靠后信息使用和多文档干扰下的实际表现。

## Self-attention：让 token 交换上下文信息

在 Transformer block 中，Self-attention 让每个 token 根据当前上下文更新自己的表示。它不是生成最终答案的唯一部分，但它负责把“我是谁”和“我周围有什么”结合起来。

这里可以回看 Q/K/V：Transformer block 里的 Self-attention 正是靠 Query 去匹配 Key，再按权重汇总 Value。

![QKV 注意力机制示例](../assets/diagrams/qkv-apple-example.svg)

直觉层看，每个位置都在问：为了理解我，前后哪些位置重要？在 decoder-only 生成模型里，因为要预测下一个 token，每个位置只能看自己和更早的位置，不能看未来。

机制层上，Self-attention 先从输入表示生成 Q、K、V，再计算权重并汇总 V。这个过程可以对整段序列并行做矩阵计算。

形式层上，标准 attention 的核心仍是：

```text
softmax(QK^T / sqrt(d)) V
```

如果是生成模型，还会加入 causal mask，把未来位置的分数屏蔽掉：

```text
第 t 个位置只能关注 1...t
不能关注 t+1...n
```

工程层上，attention 是上下文能力和计算成本的中心。长上下文、批量推理、KV cache、显存占用、延迟优化都与它有关。推理时常保存过去 token 的 K / V，生成新 token 时复用它们，这就是 KV cache 能加速自回归生成的原因。

## Multi-head attention：同时看多种关系

单个 attention 头只能在一个表示子空间里计算相关性。语言关系却有很多种：指代、句法、实体、格式、段落边界、代码依赖、引用来源、任务指令等。Multi-head attention 的做法是并行使用多个头，让它们从不同角度建立关系。

直觉层看，它像一个团队同时读同一段文本：有人关注代词指向，有人关注语法结构，有人关注数字和单位，有人关注代码变量。最后把这些观察合并起来，交给下一层继续处理。

机制层上，模型会把表示投影到多个 Q / K / V 子空间，每个头单独计算 attention，然后把各头结果拼接并再投影回模型维度。

形式层可以简化为：

```text
head_1 = Attention(Q1, K1, V1)
head_2 = Attention(Q2, K2, V2)
...
输出 = Linear(concat(head_1, head_2, ...))
```

工程层上，头数、每头维度和分组方式会影响质量、速度和显存。现代模型还可能使用 MQA / GQA 等变体，减少推理时 KV cache 的大小。对应用开发者来说，不一定要调这些底层参数，但要理解模型上下文能力、推理成本和部署吞吐背后有这些结构约束。

## FFN：逐位置的非线性加工

Attention 负责从其他 token 汇入信息，但如果只有 attention，模型主要是在做加权混合，表达能力不够。Transformer block 里还会加入 Feed Forward Network，通常简称 FFN 或 MLP。

直觉层看，attention 像“读资料”，FFN 像“对读到的资料做加工”。每个位置在吸收上下文后，需要判断、转换、组合和抽象，这需要非线性能力。

机制层上，FFN 对每个 token 位置独立应用同一组小网络。常见结构是先把维度扩张，再经过激活函数，然后投影回原维度：

```text
x → Linear(up) → activation → Linear(down)
```

现代模型常用 GELU、SwiGLU 等激活和门控变体。虽然 FFN 不直接在不同 token 之间通信，但它处理的是已经经过 attention 汇总的上下文表示，所以仍然能加工上下文信息。

形式层上，FFN 是逐位置函数：

```text
for each token position:
  y_i = FFN(x_i)
```

工程层上，FFN 往往占据 Transformer 参数量和计算量的大头之一。扩大 FFN 维度能提升模型容量，但也增加训练和推理成本。MoE 模型则把 FFN 扩展成多个专家，每个 token 只路由到部分专家，以增加参数容量同时控制单次计算量。

## Residual connection：让深层网络保留信息

Transformer 要变强，通常需要堆很多层。深层网络的难点是：每一层都可能改变表示，如果信息在某层被破坏，后面很难恢复；梯度也可能在反向传播中变得不稳定。

Residual connection 的直觉很简单：每个模块不要完全重写输入，而是在输入上加一个改动。

```text
输出 = 输入 + 模块计算出的变化量
```

机制层看，残差连接给信息和梯度提供了更直接的通路。某一层如果暂时学不到有用变换，也可以接近“什么都不改”，让模型继续训练。

形式层上，Transformer block 常见结构是：

```text
x = x + attention_result
x = x + ffn_result
```

工程层上，没有残差连接，训练很深的 Transformer 会困难得多。残差让模型可以堆叠更多层，而更多层意味着更强的组合能力：浅层学局部模式，中层组合语义和结构，高层适配任务和生成目标。

## LayerNorm / RMSNorm：稳定每层的数值尺度

深层网络训练时，激活值的尺度会不断变化。某些层输出过大或过小，都可能让训练不稳定。Normalization 的作用是把表示的数值范围拉回到更可控的状态。

直觉层看，它像每一层之间的“校准”。不是改变句子内容，而是让信号的尺度更稳定，方便下一层继续处理。

机制层上，LayerNorm 会对每个 token 的隐藏维度做归一化，再通过可学习参数调整尺度和偏移。RMSNorm 是一种更简化的变体，常见于现代大模型，它主要按均方根尺度归一化，计算更省。

形式层上，重要的是归一化通常发生在隐藏维度上，而不是跨 batch 统计。这适合变长文本和自回归生成场景。

工程层上，Norm 的位置也重要。早期 Transformer 常见 post-norm：

```text
x = Norm(x + Sublayer(x))
```

很多大模型使用 pre-norm：

```text
x = x + Sublayer(Norm(x))
```

Pre-norm 往往让深层训练更稳定。对应用开发者来说，这解释了为什么“看似只是结构小差异”的模型架构会显著影响可训练规模和推理稳定性。

## Causal mask：生成时不能偷看未来

语言模型预训练的常见目标是预测下一个 token。训练时，一段文本的真实后续已经在数据里。如果模型在预测第 `t+1` 个 token 时能看到它后面的 token，就相当于考试偷看答案，训练目标会失效。

Causal mask 的作用是限制每个位置只能关注自己和过去位置。

```text
位置 1：只能看 1
位置 2：可以看 1, 2
位置 3：可以看 1, 2, 3
位置 4：可以看 1, 2, 3, 4
```

机制层上，mask 会在 softmax 前把未来位置的 attention 分数设为不可用，使这些位置的权重变成 0。

工程层上，causal mask 让训练可以并行。虽然生成时必须一个 token 一个 token 往后采样，但训练时可以把整段文本一次送入模型，让每个位置同时学习预测下一个 token。这是 decoder-only 模型能在海量文本上高效训练的重要原因。

decoder-only 模型的生成约束可以用下面这张表串起来。它们共同保证模型在训练和推理时都遵守“只基于前文预测后文”的规则。

| 约束 | 具体做法 | 为什么必要 | 工程影响 |
| --- | --- | --- | --- |
| 只能看过去 | 使用 causal mask 屏蔽未来位置 | 防止训练时偷看答案 | 训练可并行，但生成仍要逐 token |
| 输出接回上下文 | 每生成一个 token 就追加到序列 | 下一步要条件化在已生成内容上 | 早期错误会影响后续生成 |
| 上下文窗口有限 | 超出窗口的 token 不能直接参与计算 | attention 只能处理当前输入序列 | 需要检索、摘要或历史裁剪 |
| 结束要有条件 | EOS、stop sequence、max tokens | 否则自回归循环会持续生成 | 产品要设置停止和超时策略 |
| 概率要被解码 | greedy、temperature、top_p 等策略选 token | 模型输出的是分布，不是最终文本 | 不同任务要配置不同采样策略 |

理解这些约束后，decoder-only 的很多工程现象就不再神秘：它强在统一生成，也受限于逐 token、有限窗口和概率解码。

## 为什么 decoder-only 适合生成

Transformer 最初有 encoder 和 decoder 两部分。Encoder 适合理解完整输入，decoder 适合在已有上下文下逐步生成输出。现代通用大语言模型多采用 decoder-only 架构：只保留带 causal mask 的 decoder 堆叠，用统一的“预测下一个 token”目标训练。

直觉层看，生成文本本来就是从左到右不断续写。用户 Prompt、系统指令、工具结果、历史对话和模型已生成内容，都可以拼成同一条 token 序列。模型只需要反复回答一个问题：在目前这些 token 后面，下一个最可能或最合适的 token 是什么？

机制层上，decoder-only 模型的每一层都是 masked Self-attention + FFN。它不需要单独的 encoder 输出作为交叉注意力来源，所有条件都放在同一上下文窗口里。

形式层上，自回归生成可以写成：

```text
P(整段文本) = P(t1) * P(t2 | t1) * P(t3 | t1,t2) * ...
```

模型每一步只预测下一个 token 的概率分布。采样策略再从这个分布里选出实际 token，形成回答。

工程层上，decoder-only 的统一性很重要。预训练、指令微调、对话、代码补全、工具调用、多轮 Agent 轨迹，都可以表示成“给定前文，预测后文”。这降低了训练和产品形态之间的结构差异，也让同一基础模型可以适配很多任务。

## 为什么 Transformer 支撑大规模训练

Transformer 能成为大模型主干，不只是因为效果好，还因为它能被高效扩大。

从结构演进上看，Transformer 相比 CNN / RNN 的关键优势在于：既能建模序列关系，又更适合并行训练和长距离依赖。

![CNN、RNN 和 Transformer 的差异](../assets/diagrams/cnn-rnn-transformer-comparison.svg)

第一，它把序列计算组织成大矩阵运算。Embedding、attention、FFN 都能很好地利用 GPU / TPU 的并行能力。相比 RNN 的强时间步依赖，Transformer 更适合大批量训练。

第二，它有稳定的深层堆叠方式。Residual connection、LayerNorm / RMSNorm、合适的初始化和优化器，让模型可以堆到几十层、上百层，并在海量数据上持续吸收模式。

第三，它的训练目标简单统一。Next-token prediction 不需要人工给每段文本标任务标签，只要有大量文本就能形成监督信号。架构和目标函数配合起来，支撑了预训练规模化。

第四，它能通过规模获得更强泛化。参数量、数据量和计算量增大后，模型能记住更多模式，也能组合出更复杂的能力。Scaling law 之所以重要，是因为 Transformer 提供了一个能稳定吃下更多计算的结构。

第五，它适配工程优化。KV cache、FlashAttention、张量并行、流水线并行、量化、稀疏专家、推理批处理等优化，都是围绕 Transformer 的规律发展出来的。

同一套组件在训练和推理阶段承担的重点并不完全一样。下面这张表能帮助把“模型结构”和“部署系统”联系起来。

| 组件或机制 | 训练阶段的作用 | 推理阶段的作用 | 工程关注点 |
| --- | --- | --- | --- |
| embedding 和 tokenizer | 把海量文本统一成 token 序列 | 控制输入输出 token 成本 | 多语言、代码、特殊格式的切分质量 |
| Causal mask | 让整段文本并行学习 next-token loss | 维持生成时不能看未来 | 训练并行和推理自回归之间的差异 |
| Self-attention | 学习上下文关系和长距离依赖 | 读取 Prompt、历史和工具结果 | 上下文长度、首 token 延迟、显存 |
| KV cache | 训练中通常不是核心优化 | 复用历史 K / V，加速逐 token 生成 | 长对话显存、吞吐和批处理 |
| FFN / MLP | 提供大部分参数容量和非线性表达 | 影响每步生成计算量 | 模型大小、量化、MoE 路由 |
| Norm 和 residual | 稳定深层训练 | 保持深层推理数值稳定 | 架构变体会影响模型质量 |
| 输出头和采样 | 计算词表 logits 和损失 | 从概率分布选 token | temperature、top_p、schema 约束 |

这也是为什么应用工程既要理解架构，也要理解推理系统：同一个 Transformer，训练瓶颈和上线瓶颈往往不同。

## 它解决什么，又解决不了什么

Transformer 解决了几个核心问题：

- 用 embedding 把离散 token 变成可学习向量。
- 用位置信息保留顺序。
- 用 Self-attention 建立上下文关系。
- 用 multi-head 捕捉多种关系。
- 用 FFN 增强非线性表达。
- 用 residual 和 normalization 让深层训练稳定。
- 用 causal mask 支撑自回归生成。

但它也有边界。

第一，标准 attention 的长上下文成本高。上下文越长，显存和计算压力越大，延迟也会上升。

第二，它不天然拥有外部记忆。上下文窗口外的信息不会自动被访问，需要 RAG、数据库、工具、记忆系统或重新输入。

第三，它不保证事实性和可验证性。架构能学习模式，但不能确保每次生成都真实、最新、可追溯。

第四，它不自动完成可靠规划。复杂 Agent 任务还需要任务分解、状态管理、工具调用、错误恢复和评估机制。

第五，它对数据和训练目标敏感。模型学到什么，很大程度上取决于预训练数据、后训练数据、偏好优化和系统提示约束。

## 工程小结

理解 Transformer 会影响实际系统设计。

做 Prompt 和上下文编排时，要记住模型看到的是一条 token 序列。系统指令、开发者约束、用户问题、检索片段、工具结果和历史对话的顺序、距离、格式都会影响生成。

做长文档问答时，要考虑 attention 成本和长上下文稳定性。把所有资料塞进去不一定最优；更可靠的方式通常是检索、重排、压缩、引用标记和答案校验一起做。

做实时产品时，要关注 KV cache、输出长度、并发批处理和模型尺寸。生成越长，逐 token 解码时间越明显；上下文越长，首 token 延迟通常越高。

做模型选择时，要区分架构能力和产品能力。两个模型都叫 Transformer，并不代表上下文长度、工具调用、指令跟随、代码能力、数学能力和事实可靠性相同。

做 Agent 时，要把 Transformer 当成强大的上下文模式引擎，而不是完整操作系统。外部状态、权限、工具结果、重试策略和验证逻辑仍然需要工程系统来承接。

## 连接到下一节

现在结构有了：token embedding、position embedding、Self-attention、multi-head attention、FFN、residual、normalization、causal mask 共同组成 decoder-only Transformer。

下一步要问：这些参数一开始只是随机数。模型如何从海量文本中学会语言、知识、推理格式、代码模式和任务习惯？这会引出预训练、损失函数、反向传播、优化器和 scaling law。

Transformer 最终服务的仍然是逐 token 生成：结构让模型能更好处理上下文，输出层再把隐藏表示变成下一个 token 的概率分布。

![大模型 next-token 预测循环](../assets/diagrams/next-token-loop.svg)
