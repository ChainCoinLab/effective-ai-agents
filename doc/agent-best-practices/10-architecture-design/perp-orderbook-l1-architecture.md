# 高并发订单簿永续合约专用 L1 架构设计

本文的目标不是罗列区块链、订单簿和永续合约的所有知识点，而是回答一个具体问题：

```text
如果要设计一条支持高并发、带订单簿撮合、面向永续合约交易的专用 L1，
哪些能力必须进入链本身，哪些可以放在链外服务，区块内执行顺序应该如何设计？
```

核心结论先放在前面：

- 专用 L1 的价值不只是提高 TPS，而是把最终性、排序、撮合、保证金、资金费率、清算和行情事件变成同一个可重放状态机。
- MVP 更适合选择 `Cosmos SDK + CometBFT + 自研订单簿/永续合约模块`，先完成确定性撮合和风控闭环，再逐步增强公平排序和订单隐私。
- 区块执行主线应该是：先固定本区块使用的价格状态，也就是指数价、标记价和市场状态；再优先处理撤单、补保证金、reduce-only 平仓等降风险交易；然后撮合普通订单、提交仓位和保证金变化、执行清算，最后输出事件和状态根。
- 订单簿可以先用验证者内存结构承载热路径，但它不能只是本地内存。每个 resting order 必须能从 committed state、快照、事件和 root 中恢复。
- 共识解决的是“提交后不回滚”，不自动解决“提交前是否公平排序”。MEV 防护必须在订单参数、mempool、区块执行、清算和监控层分层设计。
- 前端、K 线、WebSocket、Indexer 只能重建和展示状态，不能决定链上订单优先级、成交结果或清算状态。

## 文档关系

配套文档：

- [分阶段执行路线](./perp-orderbook-l1-staged-execution.md)：回答先做哪一层、后做哪一层，每个阶段牺牲什么、验证什么、补什么。
- [验证测试方案](./perp-orderbook-l1-verification.md)：回答如何证明确定性、撮合、保证金、预言机、清算、MEV、性能和共识故障处理真的达标。

<style>
.perp-page-guide {
  margin: 24px 0 32px;
  padding: 14px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f8fafc;
  font-size: 14px;
  line-height: 1.45;
}
.perp-page-guide__title {
  margin: 0 0 10px;
  color: #111827;
  font-size: 13px;
  font-weight: 700;
}
.perp-page-guide ol {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.perp-page-guide a {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #374151;
  text-decoration: none;
}
.perp-page-guide a:hover {
  color: #111827;
  text-decoration: underline;
}
.perp-page-guide__num {
  color: #111827;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}
.perp-page-guide__label {
  min-width: 0;
}
.perp-page-anchor {
  display: block;
  position: relative;
  top: -76px;
  visibility: hidden;
}
@media (min-width: 1280px) {
  .perp-page-guide {
    position: fixed;
    top: 96px;
    right: 16px;
    z-index: 20;
    width: 56px;
    max-height: calc(100vh - 128px);
    margin: 0;
    padding: 10px 8px;
    overflow: auto;
    background: rgba(248, 250, 252, 0.96);
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  }
  .perp-page-guide__title {
    margin-bottom: 8px;
    text-align: center;
  }
  .perp-page-guide ol {
    display: block;
  }
  .perp-page-guide li + li {
    margin-top: 6px;
  }
  .perp-page-guide a {
    position: relative;
    justify-content: center;
    width: 38px;
    height: 30px;
    border-radius: 6px;
  }
  .perp-page-guide a:hover,
  .perp-page-guide a:focus {
    background: #eef2ff;
    text-decoration: none;
  }
  .perp-page-guide__label {
    position: absolute;
    right: 46px;
    max-width: 180px;
    padding: 6px 8px;
    border-radius: 6px;
    background: #111827;
    color: #fff;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transform: translateX(6px);
    transition: opacity 0.16s ease, transform 0.16s ease;
  }
  .perp-page-guide a:hover .perp-page-guide__label,
  .perp-page-guide a:focus .perp-page-guide__label {
    opacity: 1;
    transform: translateX(0);
  }
}
@media (min-width: 1680px) {
  .perp-page-guide {
    right: 28px;
    width: 236px;
    padding: 14px 16px;
  }
  .perp-page-guide__title {
    text-align: left;
  }
  .perp-page-guide li + li {
    margin-top: 7px;
  }
  .perp-page-guide a {
    justify-content: flex-start;
    width: auto;
    height: auto;
    border-radius: 0;
  }
  .perp-page-guide a:hover,
  .perp-page-guide a:focus {
    background: transparent;
    text-decoration: underline;
  }
  .perp-page-guide__label {
    position: static;
    max-width: none;
    padding: 0;
    background: transparent;
    color: inherit;
    opacity: 1;
    transform: none;
    transition: none;
  }
}
@media (max-width: 700px) {
  .perp-page-guide ol {
    grid-template-columns: 1fr;
  }
}
</style>

<nav class="perp-page-guide" aria-label="本文导引">
  <p class="perp-page-guide__title">本文导引</p>
  <ol>
    <li><a href="#perp-section-1"><span class="perp-page-guide__num">01</span><span class="perp-page-guide__label">设计目标和边界</span></a></li>
    <li><a href="#perp-section-2"><span class="perp-page-guide__num">02</span><span class="perp-page-guide__label">一笔订单的问题</span></a></li>
    <li><a href="#perp-section-3"><span class="perp-page-guide__num">03</span><span class="perp-page-guide__label">总体架构</span></a></li>
    <li><a href="#perp-section-4"><span class="perp-page-guide__num">04</span><span class="perp-page-guide__label">交易模型</span></a></li>
    <li><a href="#perp-section-5"><span class="perp-page-guide__num">05</span><span class="perp-page-guide__label">区块执行</span></a></li>
    <li><a href="#perp-section-6"><span class="perp-page-guide__num">06</span><span class="perp-page-guide__label">撮合和订单簿</span></a></li>
    <li><a href="#perp-section-7"><span class="perp-page-guide__num">07</span><span class="perp-page-guide__label">永续风控</span></a></li>
    <li><a href="#perp-section-8"><span class="perp-page-guide__num">08</span><span class="perp-page-guide__label">MEV 和公平排序</span></a></li>
    <li><a href="#perp-section-9"><span class="perp-page-guide__num">09</span><span class="perp-page-guide__label">共识和路线</span></a></li>
    <li><a href="#perp-section-10"><span class="perp-page-guide__num">10</span><span class="perp-page-guide__label">Indexer 和行情</span></a></li>
    <li><a href="#perp-section-11"><span class="perp-page-guide__num">11</span><span class="perp-page-guide__label">风险和验证</span></a></li>
    <li><a href="#perp-section-12"><span class="perp-page-guide__num">12</span><span class="perp-page-guide__label">落地路线</span></a></li>
  </ol>
</nav>

<span id="perp-section-1" class="perp-page-anchor"></span>

## 1. 设计目标和边界

### 1.1 要解决的核心问题

订单簿永续合约不是“把一个撮合引擎放到链上”这么简单。它的难点在于，成交结果和风险状态高度耦合：

```text
订单输入
  -> 排序和最终性
  -> 价格快照
  -> 撤单、过期和撮合
  -> 仓位、保证金、PnL 和手续费
  -> funding index
  -> 清算和坏账处理
  -> 事件、快照和状态根
```

只要其中一个环节无法被所有节点确定性重放，系统就会出现以下问题：

- 同一笔订单在不同节点上成交结果不同。
- 做市商撤单和 taker 吃单的优先级不清楚。
- 清算使用了错误价格，导致错误爆仓。
- 索引器盘口和真实撮合状态不一致。
- 节点重启或新验证者加入后无法恢复订单簿。
- 用户看到成交、撤单或清算成功，后续又因为重组而消失。

因此，这条 L1 的目标不是追求抽象意义上的最高吞吐，而是让高频订单流、撮合状态和永续风控在同一套确定性规则下运行。

### 1.2 MVP 应该优先保证什么

MVP 的主次顺序应该是：

| 优先级 | 能力 | 为什么优先 |
| --- | --- | --- |
| P0 | 快速确定性最终性 | 成交、撤单和清算不能像普通概率最终性链那样长期等待确认 |
| P0 | 确定性撮合 | 所有验证者必须从同一区块和同一前置状态得到同一成交序列 |
| P0 | 保证金和清算闭环 | 永续合约的资金安全主要取决于风险引擎 |
| P0 | 价格快照和市场状态 | 清算、PnL 和杠杆检查必须使用有效标记价 |
| P0 | 可恢复订单簿 | 内存订单簿只是热索引，不能成为唯一真相 |
| P1 | 撤单和补保证金保护 | 没有撤单可靠性，就很难吸引做市商提供深度 |
| P1 | 索引器和行情服务 | 用户和做市商需要可信读模型，但它不能决定链上状态 |
| P1 | MEV 监控和基础缓解 | 先限制最坏结果，再做复杂公平排序 |
| P2 | 加密 mempool、commit-reveal、频繁批量拍卖 | 有价值，但不应阻塞确定性撮合和风控闭环 |

不要在 MVP 阶段把所有目标一次做满。更合理的路线是：

```text
先保证成交和风控可重放
  -> 再保证订单簿可审计和可恢复
  -> 再增强公平排序、订单隐私和更复杂的抗 MEV 机制
```

### 1.3 不适合放在第一阶段的目标

以下能力不是不重要，而是不应该压过主线：

- 全链上存储每一个价格档和每一笔 resting order。
- 一开始就实现阈值加密 mempool。
- 一开始就采用频繁批量拍卖替代连续 CLOB。
- 自研全新 BFT 共识。
- 把 K 线、行情聚合或前端缓存当成链上状态的一部分。
- 只追求理论 TPS，而忽略撤单延迟、状态恢复和清算安全。

<span id="perp-section-2" class="perp-page-anchor"></span>

## 2. 用一笔订单说明系统必须回答什么

假设 BTC-PERP 当前指数价和标记价都是 70,000 USDC。Bob 已经在订单簿上挂出一笔卖出 BTC-PERP 的限价单，Alex 现在想买入 BTC-PERP 做多。

```text
市场：BTC-PERP
当前价格：70,000 USDC

Bob 的 resting order：
  方向：卖出 / 做空 BTC-PERP
  类型：限价单
  价格：70,000 USDC
  数量：1 BTC

Alex 的新订单：
  方向：买入 / 做多 BTC-PERP
  类型：限价单
  最高可接受价格：70,100 USDC
  数量：1 BTC
  杠杆：10x
  保证金资产：USDC
```

这看起来只是一笔普通下单，但系统必须连续回答：

- Alex 的签名、nonce、订单参数是否合法？
- 10x 杠杆下，Alex 的可用保证金是否足够？
- Alex 的订单进入系统后，先进入哪个队列？
- 在还没进区块前，谁能看到 Alex 的订单，谁能影响排序？
- 如果 Bob 同时提交撤单，Bob 的撤单和 Alex 的吃单谁先执行？
- 如果订单成交，是按 Alex 的 70,100 成交，还是按 Bob 的 70,000 成交？
- 成交后 Alex 的多头仓位、Bob 的空头仓位、保证金、手续费和 funding index 如何更新？
- 如果 BTC 从 70,000 快速跌到 63,000，Alex 是否会被清算？
- 这笔成交是否会因为区块回滚而消失？
- 索引器、前端盘口和 K 线服务如何重建这笔成交？

这组问题就是架构主线。一个合理的订单簿永续 L1，必须给出确定、可重放、可审计的答案。

### 2.1 这笔订单的关键答案

- 如果 Bob 的 70,000 USDC 卖单在撮合前仍然有效，Alex 的买单应以 Bob 的 maker price 70,000 USDC 成交，而不是以 Alex 可接受的最高价 70,100 USDC 成交。
- 如果 Bob 的卖单是上一区块已经存在的 resting order，且 Bob 在同一区块提交撤单，MVP 建议让 Bob 的撤单先于 Alex 的普通 taker 撮合执行。
- 成交、撤单和清算只有进入 CometBFT committed block 后，才应该被前端、风控和对账系统视为最终状态。
- 清算和保证金检查使用有效标记价，不使用最后成交价。最后成交价主要用于成交历史、K 线和行情展示。
- Gateway / RPC 可以做准入、限流和转发，但不能决定最终交易顺序、订单优先级或成交结果。
- Indexer 和行情服务只能根据链上事件、状态 root 和快照重建展示状态，不能反向决定链上状态。

### 2.2 基础术语

| 术语 | 简短解释 |
| --- | --- |
| resting order | 已经挂入订单簿、等待被其他订单吃掉的挂单 |
| maker / taker | maker 提供盘口流动性，taker 吃掉盘口流动性 |
| index price | 来自外部现货或综合市场的参考价格 |
| mark price | 用于保证金、未实现 PnL 和清算的风控价格 |
| 价格快照 | 区块执行前固定下来的一组价格和市场状态，例如 index price、mark price、Normal/ProtectOnly 状态；本区块后续风控和清算都基于这组固定输入 |
| 保护类交易 | 优先降低风险或保护既有状态的交易，例如撤单、批量撤单、补保证金、reduce-only 平仓 |
| app hash / root | 应用状态承诺值，用来证明所有节点执行后得到同一状态 |
| sequence | 协议内确定性分配的序号，不能依赖某个 Gateway 的本地时间 |
| ProtectOnly | 市场保护状态，只允许撤单、补保证金、减仓和平仓等降风险操作 |

<span id="perp-section-3" class="perp-page-anchor"></span>

## 3. 总体架构：专用 L1 应该把哪些规则下沉到链里

### 3.1 为什么普通智能合约很难同时满足这些要求

把完整 CLOB 永续交易放在通用链智能合约上，会遇到结构性限制：

| 需求 | 通用链合约的限制 |
| --- | --- |
| 高频下单和撤单 | 每次操作都消耗通用链资源，成本高且延迟不可控 |
| 做市商批量改单 | gas、区块容量和 mempool 拥堵会直接影响报价可靠性 |
| 可控排序规则 | 底层链排序规则通常不是为交易所订单簿设计的 |
| 撤单保护 | 很难要求底层区块提议者按交易所规则优先处理撤单 |
| 快速最终性 | 取决于底层链，不一定适合成交确认 |
| 风控热路径 | 订单、仓位、保证金、价格、清算都在高频路径上 |
| 订单簿状态 | 大量 resting orders 会造成昂贵状态增长 |
| 协议级 anti-MEV | 很难修改底层交易传播、mempool 和区块构建逻辑 |

所以问题不是“智能合约能不能写永续合约”，而是：

```text
如果目标是专业订单簿永续交易，
通用链合约很难同时满足成本、延迟、排序控制、撤单保护、风控热路径和可验证撮合。
```

专用 L1 的价值是把这些约束下沉为链本身的规则：

- 共识最终性服务成交确认。
- mempool 和交易准入服务订单流。
- 区块执行状态机服务撮合、保证金、资金费率和清算。
- 状态存储围绕订单簿快照、root 和可恢复性优化。
- 治理参数围绕市场风险和交易安全设置。
- 后续可以逐步加入加密 mempool、批量拍卖或公平排序。

### 3.2 推荐的系统分层

```text
Trader / Market Maker / Liquidator
  -> Client SDK / API
  -> RPC / Gateway
       - 签名和格式预检
       - rate limit / spam control
       - 私有订单流或做市商专线
  -> Mempool / Block Proposal
       - 候选交易传播
       - 基础费用和准入
       - 可能存在排序和审查风险
  -> CometBFT Consensus
       - 提议、投票、提交
       - committed block 提供最终交易序列
  -> ABCI Application State Machine
       - Oracle / Price
       - Protection Queue
       - Matching Engine
       - Position / Margin / Funding
       - Liquidation / Insurance / ADL
       - Event / Root / Snapshot
  -> Indexer / Market Data
       - L2 / L3 orderbook read model
       - trades / ticker / funding / candles
       - WebSocket / REST
```

这张图的重点是边界：

- Gateway 是入口，不是最终排序者。
- 共识给出最终区块，不直接保证公平排序。
- 应用状态机决定撮合、仓位、保证金、清算和 root。
- Indexer 是读模型，不是写模型。

### 3.3 模块从订单流程推导出来

| 流程环节 | 需要的模块 |
| --- | --- |
| 用户签名订单 | Account、Auth、Order Type、Nonce |
| RPC/Gateway 接收 | API、Rate Limit、Spam Control |
| mempool 等待 | Mempool、Fee、MEV Monitoring |
| 共识定序 | CometBFT、Validator、Slashing |
| 价格更新 | Oracle、Market Status、Circuit Breaker |
| 风险预检 | Margin、Position、Market Param |
| 撤单和过期 | Orderbook、Order State Machine |
| 撮合 | Matching Engine、Orderbook Data Structure |
| 成交后更新 | Position、Margin、Fee、Funding |
| 清算 | Liquidation、Insurance Fund、ADL |
| 输出事件 | Event、Indexer、Market Data API、Kline Service |
| 订单簿展示 | Orderbook Read Model、Snapshot Service、WebSocket API |
| 参数调整 | Governance、Risk Parameter Management |
| 跨链资产 | IBC/Bridge、Asset Registry |

核心依赖关系：

```text
Consensus 决定交易序列何时最终确定
Mempool 影响交易进入序列前的风险
Oracle 决定风险检查和清算价格
Matching 依赖 Orderbook、Margin、Position、Market
Liquidation 依赖 Oracle、Margin、Position、Insurance Fund
Indexer 只能重建状态，不能决定状态
Governance 可以改参数，但必须有延迟和风控约束
```

<span id="perp-section-4" class="perp-page-anchor"></span>

## 4. 交易模型：用户提交的是带约束的订单意图

普通转账交易表达的是“从 A 转给 B 多少资产”。永续合约订单表达的是带约束的交易意图：

```text
只有在价格约束、保证金约束、订单有效期、市场状态和风控规则都满足时，
系统才允许它进入撮合或挂入订单簿。
```

### 4.1 订单至少需要包含的字段

```text
market_id
account_id / subaccount_id
side: buy | sell
order_type
price 或 protection_price
quantity
time_in_force
post_only
reduce_only
expire_height
client_order_id
nonce
signature
```

这些字段不是业务装饰，而是防止错误成交、状态歧义和 MEV 放大的基础。

### 4.2 需要支持的订单类型

| 类型 | 含义 | 为什么需要 |
| --- | --- | --- |
| Limit | 指定最高买价或最低卖价 | 用户控制成交价格，可挂单 |
| Market | 立即按盘口成交 | 用户表达立即成交意图 |
| IOC | 立即成交，未成交部分取消 | 常用于吃单 |
| FOK | 要么全部成交，要么全部取消 | 避免部分成交风险 |
| GTC | 未成交部分继续挂单 | 常规做市和限价交易 |
| Post-only | 只做 maker，会立即成交则拒绝或取消 | 做市商避免误吃单 |
| Reduce-only | 只减仓，不允许增仓 | 平仓、止损和风控常用 |
| Trigger / Conditional | 到达触发条件后转成普通订单 | 止盈止损 |
| Liquidation order | 清算流程生成或清算者提交 | 处理危险仓位 |

市价单不能设计成“没有价格上限的订单”。在链上订单簿里，市价单应该转换成带保护价格的 IOC 限价单：

```text
Market Buy  -> IOC Limit Buy with max_price
Market Sell -> IOC Limit Sell with min_price
```

这样既保留“立即成交”的体验，也避免订单簿被抽空时出现极端成交价。

### 4.3 交易分类和多队列

为了支持高并发和保护性交易，系统不能只记录“这是一笔交易”。交易进入状态机后，需要先按类型分类：

| 分类 | 示例 | 进入队列 |
| --- | --- | --- |
| OracleTx | price update、index update、mark price update | Oracle Queue |
| ProtectionTx | cancel、batch cancel、deposit margin、reduce-only close | Protection Queue |
| NormalOrderTx | limit、market、IOC、FOK、GTC、post-only | Normal Order Queue |
| LiquidationTx | liquidate、partial liquidation、ADL | Liquidation Queue |
| SystemTx | funding index update、fee settlement、parameter activation | System Queue |

核心原则：

```text
交易先分类，再入队。
队列内按确定性 sequence 串行。
不同市场和不同队列可做并行预检。
所有并行结果通过确定性屏障合并。
```

### 4.4 序列号体系

序列号不能由 Gateway 随意分配。Gateway 可以记录接收时间、做限流、提前拒绝明显无效的交易，也可以把 `client_order_id` 原样转发给链；但进入状态根和撮合优先级的序号，必须由共识后的区块执行状态机确定性生成。

| 序列号 | 作用 | 分配位置 |
| --- | --- | --- |
| `tx_sequence` | 区块内原始交易序号，用于审计输入 | committed block 的交易数组位置 |
| `queue_sequence` | 交易进入具体队列后的序号 | 状态机按交易类型分类后生成 |
| `market_sequence` | 同一市场内的处理序号 | 状态机按市场和队列规则生成 |
| `order_sequence` | resting order 在订单簿里的时间优先级 | 订单真正变成 resting order 时递增 |
| `trade_sequence` | 成交事件序号 | 成交事件写出时递增 |
| `oracle_sequence` | 价格更新序号 | Oracle Queue 提交有效价格更新时生成 |
| `liquidation_sequence` | 清算执行序号 | Liquidation Queue 确认执行清算时生成 |

因此，所有节点只要看到同一个 committed block 和同一个前置状态，就会推导出同一批 sequence。

### 4.5 账户 nonce 与保护队列

保护队列优先，不等于可以任意打破同一个账户自己的交易顺序。比较保守的 MVP 规则是：

```text
先按 committed block 得到 tx_sequence
再按 tx_sequence 校验同一账户 nonce 是否连续
然后把交易分类到不同队列
队列优先级只改变跨账户、跨交易类型的执行阶段
同一账户内部仍受 nonce 依赖约束
```

例如同一个账户在同一区块里提交三笔交易：

```text
nonce 10: cancel order A
nonce 11: deposit margin
nonce 12: open new position
```

状态机可以在保护阶段处理撤单和补保证金，再让普通开仓进入撮合，因为这没有违反该账户的 nonce 顺序。

如果顺序反过来：

```text
nonce 10: open new position
nonce 11: deposit margin
```

那么 `deposit margin` 不能被提前拿来“拯救”前一笔开仓。`open new position` 必须按 nonce 10 当时的状态做保证金检查；如果当时保证金不足，它就应该失败或被拒绝。

所以“撤单、补保证金、reduce-only 优先”的真实含义是：

- Bob 的保护类交易可以优先于 Alex 的普通 taker 订单。
- 同一个账户自己的 nonce 顺序仍然是交易依赖关系。
- 如果未来要让保护类交易绕过普通 nonce，需要引入独立 `protection_nonce`、显式依赖和更复杂的重放规则；这不适合 MVP。

### 4.6 订单状态机

订单不能只用“存在/不存在”表示。它需要明确状态机：

```text
Created
  -> Accepted
  -> Resting
  -> PartFilled
  -> Filled

Accepted
  -> Rejected

Resting / PartFilled
  -> Cancelled
  -> Expired
```

关键转换：

| 转换 | 条件 |
| --- | --- |
| Created -> Accepted | 签名、nonce、market、tick size、lot size、过期高度校验通过 |
| Accepted -> Rejected | 保证金不足、价格非法、post-only 会成交、reduce-only 会增仓 |
| Accepted -> Resting | GTC 限价单未完全成交，剩余部分挂入订单簿 |
| Accepted -> Filled | IOC/FOK/可成交限价单全部成交 |
| Accepted -> PartFilled | 部分成交，剩余数量继续处理 |
| Resting -> Cancelled | 用户撤单、批量撤单或系统风控撤单 |
| Resting -> Expired | 超过 `expire_height` |

这一步引出第一个架构要求：订单操作必须可重放。所有节点看到同样的订单输入和同样的状态，必须得到同样的订单状态变化。

<span id="perp-section-5" class="perp-page-anchor"></span>

## 5. 区块执行：多队列并行预检，确定性屏障提交

一个区块内不能简单按交易数组逐条执行，也不能把 Oracle 更新、普通下单、撤单、补保证金和清算全部塞进同一个队列。它们对状态的影响不同，优先级不同，MEV 风险也不同。

更合理的是多队列执行模型：

```text
Oracle Queue
  价格更新、指数价、标记价、市场风险状态

Protection Queue
  撤单、批量撤单、补保证金、reduce-only 平仓

Normal Order Queue
  新开仓限价单、市价单、IOC、FOK、GTC、post-only

Liquidation Queue
  清算交易、协议内置清算动作、ADL 动作

System Queue
  funding index 更新、费用结算、治理参数生效、市场状态切换
```

### 5.1 执行总流程

```text
BeginBlock
  -> 固定点处理系统参数和到期 funding index 更新
  -> 更新共识时间和区块高度

Parallel Admission
  -> Oracle Queue: 校验 oracle 签名、source、timestamp
  -> Protection Queue: 校验撤单、补保证金、reduce-only
  -> Normal Order Queue: 校验普通订单签名、nonce、market、tick、lot
  -> Liquidation Queue: 校验 liquidator、目标账户、市场

Barrier 1: Price Snapshot
  -> Oracle Queue 串行提交价格更新
  -> 生成 index price、mark price、market status
  -> 输出 price root

Parallel Risk Precheck
  -> Protection Queue: 检查账户和订单存在性
  -> Normal Order Queue: 检查保证金、杠杆、position cap、OI cap
  -> Liquidation Queue: 扫描候选危险账户

Barrier 2: Protection Commit
  -> 串行提交撤单、批量撤单、补保证金、reduce-only 平仓
  -> 移除过期订单
  -> 输出 protection events

Parallel Match By Market
  -> BTC-PERP Normal Order Queue 串行撮合
  -> ETH-PERP Normal Order Queue 串行撮合
  -> SOL-PERP Normal Order Queue 串行撮合
  -> 不同市场之间可并行

Barrier 3: Trade Commit
  -> 确定性合并所有市场成交
  -> 更新仓位、保证金、手续费、open interest
  -> 按规则结算被触达账户的 funding payment
  -> 输出 trade root、position root、margin root

Parallel Liquidation Check
  -> 按市场并行检查危险账户
  -> 生成清算候选集合

Barrier 4: Liquidation Commit
  -> 按确定性清算队列执行部分清算、保险基金、ADL
  -> 输出 liquidation events

EndBlock
  -> 输出订单簿 root、风险指标和事件 root
  -> 提交 app hash
```

这里的“并行”不是任意乱序执行，而是按依赖关系分阶段并行：

- Oracle Queue 可以和其他队列的签名、nonce、费用、基础格式校验并行。
- Oracle Queue 的价格结果必须在风险检查和清算前形成确定性快照。
- Protection Queue 和 Normal Order Queue 可以并行完成基础校验，但同一市场内要先应用撤单和补保证金，再撮合普通订单。
- 不同市场的 Normal Order Queue 可以并行执行，但同一市场同一价格队列内必须串行。
- Liquidation Queue 可以并行扫描候选账户，但清算执行要按确定性顺序提交。
- System Queue 的 funding、参数切换和市场状态更新要在明确 block boundary 生效。

### 5.2 为什么撤单要单独讨论

撤单不是普通操作，它决定做市商是否愿意提供深度。

做市商挂单后，市场价格可能快速变化。如果做市商提交撤单，但区块提议者故意延迟撤单，再让 taker 吃掉旧报价，做市商会受到系统性伤害。

这会导致：

- 做市商扩大价差。
- 订单簿深度下降。
- 用户市价单滑点变大。
- 市场更容易被操纵。

MVP 建议采用以下规则：

```text
对于上一区块已经存在的 resting order：
  同一区块内先处理撤单和过期，再处理新的 taker 撮合。

对于同一区块内新挂出的 resting order：
  不享受“历史挂单撤单优先”，按本区块确定性顺序处理。
```

这不是没有代价。taker 可能看到盘口后提交订单，但执行时 maker 已撤单，成交率会下降。

取舍如下：

| 方案 | 好处 | 代价 |
| --- | --- | --- |
| 严格按区块交易顺序 | 简单 | 撤单审查风险高 |
| 历史挂单撤单优先 | 保护做市商，提升长期深度 | taker 短期成交率下降 |
| 批量拍卖 | 降低插队和撤单审查影响 | 改变连续订单簿体验 |

对高并发 CLOB 永续来说，早期更合理的是折中方案：

```text
历史 resting order 的撤单优先。
补保证金和 reduce-only 保护优先。
同一区块新挂单不享受撤单优先。
所有撤单、成交和过期都输出可审计事件。
```

### 5.3 Alex 和 Bob 在执行流程中的结果

回到开头的例子：

```text
Bob 的卖出挂单：NormalOrderTx -> Resting -> order_sequence = 1001
Alex 的买入订单：NormalOrderTx -> Normal Order Queue -> queue_sequence = 2101
Bob 的撤单请求：ProtectionTx -> Protection Queue -> queue_sequence = 3101
Oracle 的价格更新：OracleTx -> Oracle Queue -> oracle_sequence = 4001
```

如果 Bob 的卖单是历史 resting order，且 Bob 的撤单在本区块内有效：

```text
Barrier 1: 更新价格快照
Barrier 2: 先提交 Bob 撤单
Parallel Match By Market: Alex 买单找不到 Bob 的卖单
结果：Alex 可能继续吃其他卖单，或未成交部分按 TIF 处理
```

如果 Bob 没有撤单，或撤单无效：

```text
Barrier 1: 更新价格快照
Barrier 2: 无有效撤单移除 Bob 的订单
Parallel Match By Market: Alex 买单 crossing Bob 卖单
结果：按 maker price 70,000 USDC 成交
```

这就是为什么必须先定义队列和屏障，再讨论撮合细节。否则同一笔订单在不同读者心里会有不同执行顺序。

<span id="perp-section-6" class="perp-page-anchor"></span>

## 6. 撮合引擎和订单簿状态

撮合引擎的目标不是“尽量快地撮合”，而是在所有节点上用同样输入得到同样结果。

### 6.1 基础撮合规则

核心规则：

- 买单按价格从高到低。
- 卖单按价格从低到高。
- 同一价格档按 `order_sequence` 从小到大。
- 市价单先转换成带保护价的 IOC 限价单。
- IOC 未成交部分取消。
- FOK 先模拟可成交数量，不满足则整单拒绝。
- GTC 未成交部分进入订单簿。
- post-only 如果会立即成交则拒绝或取消。
- reduce-only 在成交前后都不能增加风险。
- 单笔订单最多吃掉的订单数和价格档数量必须有上限。

简化伪流程：

```text
for market in deterministic_market_order:
  apply_cancel_and_expire_phase(market)

  for order in deterministic_order_sequence:
    validate_order(order)

    if order.type == MARKET:
      order = convert_to_protected_ioc_limit(order)

    if order.time_in_force == FOK:
      simulate_fill_or_reject(order)

    while order.remaining > 0 and crosses_book(order):
      maker = best_opposite_order(market)
      trade = execute_at_maker_price(order, maker)
      update_order_remaining(order, maker)
      update_position_margin_fee(trade)

    handle_unfilled_by_time_in_force(order)
```

### 6.2 链上、链下和验证者内存订单簿的区别

这里需要区分三个阶段：

| 阶段 | 订单簿存放 | 撮合执行 | 是否作为最终方案 |
| --- | --- | --- | --- |
| 原型阶段 | 中心化服务内存 | 链下撮合、链上或本地结算 | 只用于快速验证 |
| MVP 阶段 | 验证者内存索引 + committed state / snapshot / root | 验证者在区块执行状态机中撮合，可重放 | 推荐初期方案 |
| 成熟阶段 | 全链上应用状态 | 全链上订单簿和确定性撮合 | 长期目标 |

MVP 阶段说“验证者内存订单簿”，不是指中心化链下撮合。更准确地说：

```text
订单簿热数据结构在验证者节点内存中维护。
撮合由验证者在执行 committed block 时运行。
输入来自共识提交的交易队列。
输出包括成交事件、仓位变化、保证金变化和各类 root。
任意节点从创世状态和区块数据重放，应能得到相同结果。
```

这里最容易误解的是“内存”两个字。内存订单簿只能是执行时的数据结构，不能是唯一真相。否则节点重启后就无法知道哪些 resting order 仍然有效。

更准确的恢复模型应该是：

```text
committed app state / orderbook snapshot
  -> 验证 orderbook root
  -> 重建内存里的价格档和 FIFO 队列
  -> 回放快照之后的区块事件或状态变更
  -> 继续执行新区块
```

因此，即使 MVP 不把每个价格档都设计成昂贵的全链上 KV 状态，也必须满足：

- 每个 resting order 有规范化表示，能从状态快照或事件日志恢复。
- 每个区块提交 orderbook root，周期性输出可验证快照。
- 新节点可以通过 state sync 下载快照、校验 root，再回放后续区块。
- 验证者重启后重建的是内存索引，不是重新发明订单簿状态。
- 如果只依赖未承诺的本地内存，撮合结果就不可重放，也无法安全加入新验证者。

### 6.3 高并发来自哪里

订单簿 L1 的高并发不能只靠“把区块变大”。主要性能来源应该是：

- 市场级并行：BTC-PERP、ETH-PERP、SOL-PERP 等市场可以在屏障之间并行撮合。
- 队列级并行预检：签名、nonce、market 参数、基础费用和订单格式可并行校验。
- 队内严格串行：同一市场、同一价格档、同一账户依赖必须保持确定性。
- 有界撮合循环：单笔订单最多吃多少 price levels、多少 maker orders 必须有上限。
- 批量操作：做市商批量下单、改单、撤单需要协议级支持和费用控制。
- 热索引 + 可验证快照：内存价格档负责速度，root 和快照负责恢复与审计。
- 读写分离：前端盘口、K 线和 WebSocket 由 Indexer 服务，不拖慢共识执行。

### 6.4 撮合引擎必须检查的不变量

```text
订单剩余数量 >= 0
maker 减少数量 == taker 成交数量
成交价必须满足 maker/taker 价格约束
post-only 不得产生 taker 成交
reduce-only 不得增加绝对风险敞口
同一价格档 order_sequence 严格递增
手续费入账总额 == maker fee + taker fee + protocol fee
每个市场 trade root 可由事件重建
```

典型风险和解决方式：

| 问题 | 风险 | 解决方式 |
| --- | --- | --- |
| 非确定性执行 | app hash 分叉 | 使用定点整数、显式排序 key、确定性数据结构 |
| 同价位队列错误 | queue jumping | `order_sequence` 单调递增，同价位严格 FIFO |
| 市价单无保护 | 极端价格成交 | 市价单转成带保护价的 IOC 限价单 |
| FOK/IOC 语义错误 | 用户策略被破坏 | FOK 先模拟，IOC 剩余必须取消 |
| post-only 误成交 | 做市商费用和风险失控 | crossing 时拒绝或取消，规则固定 |
| reduce-only 增仓 | 风控失效 | 成交前后都检查仓位方向和绝对风险 |
| 撮合循环过长 | 区块执行超时 | 限制单笔订单最大撮合订单数和 price levels |
| 并行市场合并错误 | 多节点 root 不一致 | 每个市场输出 trade root，再按 market id 确定性合并 |
| 索引器不一致 | 用户看到假深度或错误价格 | 输出 orderbook delta、snapshot root，索引器对账 |

<span id="perp-section-7" class="perp-page-anchor"></span>

## 7. 永续合约风险系统

成交不是终点。对永续合约来说，成交之后真正的风险才开始。

成交事件至少应包含：

```text
maker_order_id
taker_order_id
market_id
price
quantity
maker_fee
taker_fee
trade_sequence
```

成交后必须同步更新：

- 仓位大小。
- 开仓均价。
- 已实现 PnL。
- 未实现 PnL。
- 保证金占用。
- 可用保证金。
- funding index / funding payment。
- 市场 open interest。
- 手续费和返佣。

### 7.1 价格系统：index price、mark price、last trade price 要分开

在现货订单簿里，成交价通常已经足够重要。但永续合约至少有四类价格：

| 价格 | 使用位置 | 作用 |
| --- | --- | --- |
| 订单价格 | 下单和撮合 | 决定限价单是否 crossing |
| 成交价 | 撮合输出 | 决定开仓均价、已实现 PnL、手续费 |
| 指数价 | 外部市场参考 | 衡量合约是否偏离现货 |
| 标记价 | 风控和清算 | 计算未实现 PnL、保证金率和清算 |

关键原则：

- 清算不得只使用最后成交价。
- 标记价不能依赖单一过期价格源。
- 价格过期或偏离过大时，不应该继续允许高风险开仓。

一个适合 MVP 的标记价形成方式可以是：

```text
valid_external_prices = 过滤过期价格和离群价格后的多源现货价格
index_price = weighted_median(valid_external_prices)

impact_bid / impact_ask = 用固定名义金额扫本地订单簿得到的影响买价/卖价
impact_mid = midpoint(impact_bid, impact_ask)
premium = TWAP(clamp((impact_mid - index_price) / index_price, -premium_cap, premium_cap))

raw_mark_price = index_price * (1 + premium)
mark_price = clamp(raw_mark_price, index_price * (1 - max_deviation), index_price * (1 + max_deviation))
```

这个模型里：

- `index_price` 来自外部市场，用来抵抗本地订单簿被短时操纵。
- `impact_mid` 来自本地订单簿，但要用固定名义金额计算，避免只看最优一档造成噪音。
- `premium` 用 TWAP 平滑，避免一个区块内的瞬时偏离直接触发清算。
- `mark_price` 有偏离上限；价格源过期或偏离过大时，市场进入 Degraded 或 ProtectOnly。
- `last_trade_price` 不参与清算触发，只作为行情和成交历史使用。

市场状态可以分成：

| 价格状态 | 允许操作 |
| --- | --- |
| Normal | 正常下单、撤单、撮合、清算 |
| Degraded | 限制大额开仓、降低杠杆、提高保证金 |
| ProtectOnly | 只允许撤单、补保证金、减仓和平仓，暂停增仓 |

### 7.2 保证金和仓位

保证金检查至少要覆盖：

- 初始保证金。
- 维持保证金。
- 可用余额。
- 仓位价值。
- 杠杆上限。
- 单账户 position cap。
- 市场 open interest cap。
- reduce-only 是否真的降低风险。
- 逐仓 / 全仓边界。

基础公式可以简化为：

```text
position_value = abs(position_size) * mark_price
initial_margin_required = position_value * initial_margin_rate
maintenance_margin_required = position_value * maintenance_margin_rate

unrealized_pnl = position_size * (mark_price - entry_price) / entry_price
equity = collateral + unrealized_pnl - funding_payment
margin_ratio = equity / position_value
```

实现上必须使用定点整数和明确舍入规则，不能使用浮点数。

### 7.3 资金费率

资金费率让永续合约价格向指数价格靠拢：

```text
premium_index = (mark_price - index_price) / index_price
funding_rate = interest_rate + premium_index
funding_payment = position_size * funding_rate
```

风险：

- 大户短时间操纵 open interest。
- 价格短时偏离导致 funding 异常。
- funding 未封顶导致极端扣款。
- funding index 更新时间点不明确，导致不同节点结算不同。

缓解：

- funding rate 封顶。
- 使用 TWAP premium。
- 使用时间加权 open interest imbalance。
- 单账户仓位上限和市场 open interest 上限。
- market-level funding index 在固定 block boundary 更新。
- 账户级 funding payment 在开仓、平仓、增减仓、清算等触达仓位时结算。

### 7.4 清算和坏账处理

当账户权益低于维持保证金，系统必须清算：

```text
equity = collateral + unrealized_pnl - funding_payment
margin_ratio = equity / position_value
```

清算状态：

```text
Healthy
  -> Warning
  -> Liquidatable
  -> Liquidating
  -> Healthy 或 BadDebt
```

清算原则：

- 使用有效标记价触发，不能只用最后成交价。
- 大仓位采用部分清算。
- 清算奖励要足够，但不能鼓励恶意触发。
- 补保证金和 reduce-only 平仓应在保护阶段优先处理。
- 坏账先由保险基金吸收。
- 保险基金不足才进入 ADL 或社会化损失。

亏损吸收顺序：

```text
账户剩余保证金
  -> 清算罚金
  -> 保险基金
  -> ADL
  -> 社会化损失
```

清算引擎必须检查的不变量：

```text
清算只能基于有效标记价
清算前账户 margin_ratio < maintenance_margin
部分清算后账户要么恢复健康，要么进入下一轮清算/坏账流程
清算奖励 <= 规则上限
坏账必须进入保险基金或 ADL，不得静默消失
保险基金余额变化必须有事件
ADL 排序必须确定
清算事件必须能重建账户仓位和余额变化
```

典型风险和解决方式：

| 问题 | 风险 | 解决方式 |
| --- | --- | --- |
| 使用错误价格触发清算 | 小额成交操纵爆仓 | 清算只使用有效标记价 |
| 预言机价格过期 | 错误清算或坏账扩大 | stale price 拒绝清算，进入 ProtectOnly |
| 预言机偏离 | 利用价格差套利 | 多源价格、偏离阈值、熔断和治理恢复 |
| 清算级联 | 价格冲击、保险基金耗尽 | 部分清算、动态保证金、清算节流、只减仓模式 |
| 清算抢跑 | MEV 过高、网络拥堵 | 确定性清算队列、清算拍卖或协议内置清算 |
| 补保证金被审查 | 恶意爆仓 | Protection Queue 中补保证金优先于普通开仓和清算执行 |
| 清算奖励异常 | 用户损失扩大或无人清算 | 奖励封顶，并设置 keeper 激励 |
| 坏账处理不清楚 | 协议资产不守恒 | 明确 waterfall，并输出事件 |
| ADL 排序争议 | 用户认为系统不公平 | ADL 排名公式公开，事件可审计 |

<span id="perp-section-8" class="perp-page-anchor"></span>

## 8. MEV 和公平排序：共识不是万能解

订单被 RPC 或 Gateway 接收后，不会立刻成为最终状态。它通常会先进入 mempool，等待区块提议者打包。

此时订单还是“未最终确定的意图”：

```text
Alex 已经签名
节点可能已经看到
但它还没有进入最终区块
也还没有确定执行顺序
```

这就是 MEV 的来源。只要有人能提前看到订单，或者影响订单进入区块的顺序，就可能获利。

### 8.1 订单簿永续中的典型 MEV

| 攻击 | 发生位置 | 影响 |
| --- | --- | --- |
| 抢跑 | 看到 Alex 的买单后先提交自己的买单 | Alex 成交变差，攻击者占便宜 |
| Sandwich | 在 Alex 的订单前后插入订单 | Alex 承担额外滑点 |
| Queue jumping | 同价位订单中插到其他订单前面 | 破坏价格-时间优先 |
| 撤单审查 | 延迟做市商撤单 | 旧报价被恶意成交 |
| 补保证金审查 | 延迟用户补保证金交易 | 用户被恶意清算 |
| 清算抢跑 | 抢先提交清算交易 | 清算收益被垄断 |
| 预言机更新抢跑 | 在价格更新前后插入订单 | 利用价格延迟套利 |
| Spam | 大量小订单塞满区块 | 正常撤单、补保证金、清算被挤出 |

订单簿永续的 MEV 比 AMM 更敏感，因为订单队列本身就是价值。谁先进入同一个价格档，谁就可能先成交。

### 8.2 先区分最终性和公平性

文档必须区分两个概念：

```text
最终性：提交后不回滚。
公平性：提交前和区块内排序不被滥用。
```

CometBFT 适合解决最终性；公平排序还需要在应用层、mempool 层和协议规则里继续设计。

共识不能自动解决：

- 提议者是否抢跑。
- 提议者是否调整交易顺序。
- 某个 RPC 是否提前泄露订单。
- 撤单是否被故意延迟。
- 补保证金交易是否被审查。

### 8.3 MVP 的 MEV 防护重点

MVP 不应该追求“一次性消灭 MEV”。更现实的目标是限制最坏结果，并让攻击可复现、可监控、可缓解。

推荐 MVP 方案：

```text
保护类交易单独成队列
限价单和市价保护价
expire_height，默认可以从 20 blocks 起步
历史 resting order 撤单优先
补保证金和 reduce-only 保护
最小订单价值和动态费用
单账户 position cap 和市场 OI cap
多源价格、偏离检测和 ProtectOnly
MEV 攻击仿真和异常排序监控
```

这些机制不能隐藏订单意图，但能减少用户被极端滑点、撤单审查、错误清算和 spam 攻击放大的损失。

### 8.4 长期可以增强的公平排序方案

| 层级 | 方案 | 主要解决 | 代价 |
| --- | --- | --- | --- |
| 订单参数层 | 限价、保护价、滑点上限、expire_height | 限制最坏成交结果 | 不能隐藏订单意图 |
| 账户风控层 | reduce-only、position cap、open interest cap | 防止 MEV 扩大成系统风险 | 限制部分策略自由度 |
| 交易准入层 | 最小订单价值、动态费用、速率限制、批量操作限额 | spam 和状态膨胀 | 可能提高小用户成本 |
| 订单传播层 | 私有 RPC、做市商专线、订单流加密 | 降低订单提前泄露 | 可能引入中心化入口 |
| mempool 层 | 加密 mempool、commit-reveal、阈值加密 | 降低抢跑和 sandwich | 延迟、复杂度和 liveness 风险 |
| 区块构建层 | inclusion list、proposer commitment、跨验证者接收证明 | 降低审查和选择性打包 | 需要改共识或 P2P 协议 |
| 区块执行层 | 撤单优先、批量撮合、频繁批量拍卖、统一清算价 | 降低插队和撤单审查伤害 | 改变连续订单簿体验 |
| 清算层 | 确定性清算队列、清算拍卖、部分清算、ADL 规则 | 降低清算抢跑和坏账扩大 | 清算流程更复杂 |
| 预言机层 | 价格更新保护窗口、多源价格、偏离熔断、只减仓模式 | 降低预言机更新抢跑 | 极端行情下可能暂停增仓 |
| 监控治理层 | MEV 指标、异常排序检测、审查证明、验证者惩罚 | 发现和约束长期作恶 | 很多排序作恶难以完全证明 |

commit-reveal、阈值加密 mempool 和频繁批量拍卖都很有价值，但它们会改变延迟、流动性可见性和 liveness 假设。更适合作为强化阶段或特定市场试点，而不是 MVP 的前置条件。

<span id="perp-section-9" class="perp-page-anchor"></span>

## 9. 共识和技术路线

### 9.1 订单簿 L1 选择共识时看什么

订单簿 L1 选择共识机制时，不能只看 TPS。更关键的是：

| 维度 | 为什么重要 |
| --- | --- |
| 消息轮次 | 决定一个区块从提议到最终提交需要几轮网络交互 |
| 消息结构 | 决定通信复杂度，是 all-to-all 投票还是 leader 聚合 QC |
| 最终性类型 | 是确定性最终性，还是 optimistic / probabilistic 确认 |
| 最终确认块数 | 成交显示为最终状态前，需要等几个区块或几个投票证书 |
| view change / leader failure | 提议者失效时是否复杂、是否影响撮合连续性 |
| 工程生态 | 是否有成熟 Appchain 框架、状态机接口、验证者工具 |

对永续订单簿来说，最理想的是：

```text
少量消息轮次
  + 明确的确定性最终性
  + 提交后不需要等待很多后续确认块
  + 应用状态机能确定性执行撮合、保证金、清算
```

### 9.2 为什么 MVP 推荐 Cosmos SDK + CometBFT

本文档初期建议：

```text
Cosmos SDK + CometBFT + 自研订单簿/永续合约模块
```

原因不是 CometBFT 在所有理论指标上最优，而是它在以下方面最平衡：

- 一个 committed block 即可作为订单簿最终状态。
- 消息轮次和状态机边界容易解释。
- Cosmos SDK/ABCI 适合开发主权 Appchain。
- 账户、治理、验证者、IBC 和节点工具链成熟。
- 团队可以先把真正难的撮合、MEV、清算和订单簿展示做出来。

限制也要讲清楚：

- 默认 mempool 和排序不等于公平排序，需要自定义设计。
- 高性能订单簿模块需要自研。
- 验证者经济安全、做市流动性和跨链资产安全要单独解决。
- 如果使用 ABCI++ 等扩展点优化提案和校验，也必须保证最终状态机确定性。

### 9.3 其他技术路线如何定位

| 目标 | 更合适的选择 |
| --- | --- |
| 快速构建专用 Appchain | Cosmos SDK + CometBFT |
| 理解 BFT 理论基准 | PBFT |
| 极致吞吐和 optimistic 执行模型 | Tower BFT 类路线 |
| 大验证者集合和线性通信 | HotStuff / HotStuff 系 |
| 研究低延迟 BFT 提交 | Fast-HotStuff |
| 强 runtime 定制或 Polkadot 生态 | Substrate |

如果团队已经有 Substrate 经验，或者明确要接入 Polkadot 共享安全，可以重新评估 Substrate。否则，MVP 阶段不建议为了共识研究牺牲订单簿和风控交付速度。

<span id="perp-section-10" class="perp-page-anchor"></span>

## 10. Indexer、行情和前端展示

交易前端不应该直接依赖验证者内存结构来展示盘口。即使订单簿最初在验证者内存中执行，也需要独立的读模型：

```text
区块事件 / 状态 root / 订单簿快照
  -> Indexer
  -> Orderbook Read Model
  -> Market Data API
  -> WebSocket / REST
  -> 前端盘口、成交历史、K 线
```

索引器需要消费：

- order accepted / rejected。
- order rested。
- order cancelled。
- order expired。
- trade executed。
- position updated。
- funding index updated。
- liquidation event。
- market status changed。
- orderbook root / trade root / position root。

行情服务至少需要提供：

| 服务 | 数据来源 | 用途 |
| --- | --- | --- |
| L2 Orderbook | order rest/cancel/trade events、订单簿快照 | 展示买卖盘深度 |
| L3 Orderbook | 完整订单事件，可选权限开放 | 做市商对账和高阶策略 |
| Trades | trade_sequence 和成交事件 | 最近成交、成交明细 |
| Kline/Candles | 成交事件按时间窗口聚合 | 1m、5m、15m、1h K 线 |
| Ticker | 最新成交价、指数价、标记价、24h 量 | 市场列表 |
| Funding | funding rate、next funding time | 永续合约展示 |
| Liquidation Feed | 清算事件 | 风控和市场透明度 |

K 线服务不是共识模块，不能反过来决定链上状态。它是索引器基于成交事件生成的派生数据：

```text
trade_sequence
  -> open / high / low / close / volume
  -> candle_1m、candle_5m、candle_1h
```

早期验证者内存订单簿阶段，也必须输出足够的订单簿 delta 和周期性快照，否则前端盘口、做市商对账和历史重建都会不可靠。

<span id="perp-section-11" class="perp-page-anchor"></span>

## 11. 风险分布和验证重点

### 11.1 风险如何沿流程分布

| 流程 | 风险 |
| --- | --- |
| 用户签名 | 参数错误、过期高度太长、保护价缺失 |
| RPC/Gateway | 订单泄露、限流不足、中心化订单流 |
| mempool | 抢跑、插队、撤单审查、spam |
| 共识 | 停机、网络分区、超过三分之一投票权作恶 |
| 价格更新 | 预言机过期、偏离、单点价格源 |
| 风险预检 | 保证金计算错误、杠杆绕过 |
| 撤单阶段 | 撤单审查、批量撤单性能瓶颈 |
| 撮合阶段 | 非确定性、队列错误、部分成交错误 |
| 成交后 | PnL 错误、手续费错误、funding index 错误 |
| 清算 | 清算抢跑、级联清算、坏账扩大 |
| 索引 | 前端展示和链上状态不一致 |
| 治理 | 参数突变、市场上线错误、升级风险 |

### 11.2 每个区块后应该检查的不变量

```text
app hash 在多节点执行后完全一致
每个市场 orderbook root 可由快照和事件重建
总抵押资产守恒
手续费入账守恒
保险基金变动可解释
用户余额不能非法为负
open interest 与仓位汇总一致
long OI / short OI 与市场统计一致
realized PnL + unrealized PnL 计算一致
funding payment 多空相互抵消，除非协议明确收取费用
reduce-only 不增加风险敞口
max leverage 不可绕过
position cap 不可绕过
market open interest cap 不可绕过
清算坏账不得静默消失
```

更完整的测试方案见 [验证测试方案](./perp-orderbook-l1-verification.md)。

<span id="perp-section-12" class="perp-page-anchor"></span>

## 12. 推荐落地路线

主架构的落地顺序应该服务于风险和复杂度，而不是服务于概念完整性。

```text
阶段 0：链下撮合，链上或本地结算原型
  -> 验证订单类型、做市 API、保证金、PnL、资金费率和清算公式

阶段 1：验证者内存订单簿 + 链上确定性结算
  -> committed block 中包含订单操作
  -> 验证者在区块执行状态机中撮合
  -> 提交成交事件、仓位变化、保证金变化和 root
  -> 这是最重要的 MVP 阶段

阶段 2：订单承诺和撮合证明上链
  -> 提高撮合过程透明度
  -> 让审计节点和挑战者可重放验证

阶段 3：全链上订单簿 + 确定性撮合
  -> 最大化透明度
  -> 所有节点完整重放订单簿状态

阶段 4：公平排序和订单隐私增强
  -> inclusion list、commit-reveal、阈值加密 mempool、频繁批量拍卖
```

更详细的阶段设计见 [分阶段执行路线](./perp-orderbook-l1-staged-execution.md)。

## 附录 A：共识机制简要比较

### A.1 PBFT：经典 BFT 的基准

PBFT 的正常路径可以简化为：

```text
client request
  -> primary pre-prepare
  -> replicas prepare
  -> replicas commit
  -> reply / execute
```

它提供了确定性最终性的理论基础，容忍 `n = 3f + 1` 中的 `f` 个拜占庭节点。问题是 prepare 和 commit 阶段通常需要多节点互相广播，验证者集合变大后通信成本高，view change 也更复杂。因此 PBFT 适合理解 BFT，不适合作为现代订单簿 Appchain 的直接工程首选。

### A.2 Tendermint/CometBFT：MVP 更现实的路线

CometBFT/Tendermint BFT 的简化流程是：

```text
height H
  -> propose block
  -> prevote
  -> precommit
  -> commit
  -> application executes block
```

一个高度的区块拿到超过 2/3 precommit 后即可提交。应用层可以把该区块中的成交、撤单和清算视为最终状态，不需要像 PoW 一样等待多个后续区块降低重组概率。

它对订单簿的价值是：最终性语义清楚，ABCI 状态机边界清楚，Cosmos SDK 生态已经覆盖账户、治理、验证者和 IBC 等基础设施。限制是：共识只保证提交后的最终性，不自动保证 mempool 公平；提议者仍可能排序、审查或延迟交易，所以还需要应用层和 mempool 层的 MEV 防护。

### A.3 Solana Tower BFT：高吞吐但最终性语义不同

Solana 的 Tower BFT 使用 PoH 作为共享时钟，验证者对 fork 持续投票，并通过 lockout 机制让反复切换 fork 的成本越来越高。

```text
leader 按 PoH 顺序产出 entries / blocks
  -> validators 处理并投票
  -> votes 形成 stake-weighted confirmation
  -> lockout 随后续投票加深
  -> 达到 finalized 条件
```

它很适合 Solana 的高吞吐执行模型，但订单簿如果把成交、撤单和清算都按 finalized 处理，就需要等待更深确认；如果只按 optimistic / confirmed 展示，就要接受回滚和状态修正风险。它的价值主要是提醒：吞吐和最终性语义需要明确取舍。

### A.4 HotStuff：线性消息结构和链式提交

HotStuff 用 leader 聚合投票形成 QC，降低通信复杂度，并让 view change 更简单。

```text
leader propose
  -> replicas vote
  -> leader aggregates QC
  -> next proposal carries QC
  -> three-chain commit
```

经典 HotStuff 通常使用 three-chain commit rule：一个块不是自己拿到 QC 就立即提交，而是在后续连续 certified blocks 形成三链后提交祖先块。它适合更大的验证者集合和自研共识路线，但如果目标是先验证订单簿、MEV、清算和行情展示闭环，Cosmos SDK/CometBFT 更快。

### A.5 Fast-HotStuff：降低提交链长度的研究路线

Fast-HotStuff 试图把 classic HotStuff 的 three-chain 提交优化为 two-round / two-chain 风格，以降低延迟。

| 维度 | Classic HotStuff | Fast-HotStuff |
| --- | --- | --- |
| 提交规则 | three-chain | two-chain / two-round 目标 |
| 延迟 | 更高 | 更低 |
| view change | 线性、优雅 | 仍追求高效 view change |
| 工程成熟度 | 已被多条链借鉴 | 更偏研究和专项实现 |

它的低延迟目标很吸引订单簿系统，但不应替代 Cosmos/CometBFT 作为 MVP 路线。更合理的定位是后续共识升级或自研路线评估。
