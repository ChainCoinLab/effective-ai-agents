# Agent Engineering Best Practices Guide

Language: [中文](guide.zh.md) | [English](guide.en.md)

This guide links core agent engineering practices by functional module. Each practice has a dedicated page with the rule, rationale, optimization points, verification method, and references.

## How To Use

- Scan this file to find the relevant module.
- Open the linked practice file for `Rule`, `Why`, `Optimize`, and `Verify`.

## 00. LLM And Agent Foundations

| Topic | Core Idea | File |
| --- | --- | --- |
| Foundation overview | LLMs are probabilistic prediction machines; AI engineering wraps them in controllable, testable, recoverable systems. | [00](00-llm-basics/README.md) |
| LLM history | From statistical language models, CNNs, RNNs, and attention to Transformers. | [00.1](00-llm-basics/llm-history.md) |
| Agent history | From prompt optimization to context, memory, tools, roles, recovery, and long-running execution. | [00.2](00-llm-basics/agent-history.md) |
| Transformer principles | Explains tokens, vectors, position encoding, Q/K/V, attention, and next-token prediction. | [00.3](00-llm-basics/transformer-principles.md) |
| Context replay and memory | Multi-turn chat replays context on every turn; the model does not own persistent memory. | [00.4](00-llm-basics/memory-context-replay.md) |
| Capability boundaries | Explains context dependence, context overload, lost-in-the-middle risk, jagged capability, randomness, and role-prompt bias. | [00.5](00-llm-basics/capability-boundary.md) |

## 01. Prompt And Instruction

| No. | Practice | Core Rule | File |
| --- | --- | --- | --- |
| 01 | Define success before writing prompts | Define acceptance criteria before writing instructions. | [01](01-prompt-instruction/01-define-success-before-prompt.md) |
| 02 | Manage prompts as code | Prompts need versioning, review, regression tests, rollback, and length control for long-lived rules. | [02](01-prompt-instruction/02-manage-prompts-as-code.md) |
| 03 | Convert business SOPs into executable steps | Turn workflows into executable steps, but do not put detailed procedures in global rules. | [03](01-prompt-instruction/03-convert-sop-to-executable-steps.md) |
| 04 | Give the model a clear exit path | Allow refusal, clarification, or fallback when information is insufficient. | [04](01-prompt-instruction/04-give-clear-exit-path.md) |
| 05 | Make outputs machine-checkable | Outputs should be validated by schemas, parsers, or rules. | [05](01-prompt-instruction/05-machine-checkable-output.md) |
| 06 | Separate instructions, context, and user input | Prevent user input or external context from overriding system rules. | [06](01-prompt-instruction/06-separate-instructions-context-input.md) |
| 07 | Use a few high-quality examples | Examples should cover normal, boundary, refusal, and failure cases. | [07](01-prompt-instruction/07-use-few-high-quality-examples.md) |
| 08 | Split prompts by task | Separate prompts make behavior easier to test; prompts guide working memory and do not rewrite long-term parameters. | [08](01-prompt-instruction/08-split-prompts.md) |

## 02. Context Engineering And RAG

| No. | Practice | Core Rule | File |
| --- | --- | --- | --- |
| 09 | More context is not always better | Control context priority, source, length, and freshness. | [09](02-context-rag/09-context-is-not-more-is-better.md) |
| 10 | Optimize retrieval and generation separately | Evaluate retrieved evidence before evaluating the final answer. | [10](02-context-rag/10-separate-retrieval-and-generation-quality.md) |
| 11 | Design chunks for the task | Chunking should follow document structure and user tasks. | [11](02-context-rag/11-chunk-strategy-serves-task.md) |
| 12 | Separate retrieval and generation chunks | Small chunks can retrieve; larger chunks can support synthesis. | [12](02-context-rag/12-retrieval-and-generation-chunks-can-differ.md) |
| 13 | Make RAG optimization observable | Use Context Recall, Faithfulness, first-turn resolution, chunk IDs, and confidence signals to locate bottlenecks. | [13](02-context-rag/13-add-cited-evidence-to-rag.md) |
| 14 | Define an empty-retrieval policy | Empty retrieval should clarify, broaden, fallback, or refuse. | [14](02-context-rag/14-empty-retrieval-policy.md) |
| 15 | Defend against context injection | External documents must not override system instructions or permissions. | [15](02-context-rag/15-context-injection-defense.md) |
| 16 | Deduplicate and compress context | Remove repeated, irrelevant, and template-heavy content. | [16](02-context-rag/16-deduplicate-and-compress-context.md) |
| 17 | Use summary, index, and cache-friendly layout for long context | Long tasks need summaries, indexes, stable prefixes, and dynamic message layers. | [17](02-context-rag/17-long-context-summary-and-index-layers.md) |
| 18 | Make context construction observable | Log query, top-k, rerank scores, injected passages, and cache hits. | [18](02-context-rag/18-observable-context-construction.md) |

## 03. Memory And State

| No. | Practice | Core Rule | File |
| --- | --- | --- | --- |
| 19 | Manage memory for long-running tasks | Long-task memory should keep context fresh, make old memories searchable, preserve evidence, and support recovery. | [19](03-memory-state/19-memory-context-state-boundaries.md) |
| 20 | Define a memory write policy | Store only stable, explicit, authorized facts or preferences. | [20](03-memory-state/20-memory-write-policy.md) |
| 21 | Make memory updateable and deletable | Corrections, revocation, and privacy deletion must work. | [21](03-memory-state/21-memory-update-delete.md) |
| 22 | Store source and timestamp with memory | Memory needs source, time, confidence, and scope. | [22](03-memory-state/22-memory-source-timestamp.md) |
| 23 | Avoid sensitive long-term memory by default | Privacy data, secrets, and business data should not be persisted by default. | [23](03-memory-state/23-sensitive-info-memory.md) |
| 24 | Manage task state deterministically | Workflow progress, approvals, and tool results should not live only in text. | [24](03-memory-state/24-deterministic-task-state.md) |

## 04. Tools And Multi-Agent Systems

| No. | Practice | Core Rule | File |
| --- | --- | --- | --- |
| 25 | Keep tool interfaces small and clear | Each tool should do one kind of action with stable inputs and outputs. | [25](04-tools-agents/25-small-clear-tool-interfaces.md) |
| 26 | Describe when not to use a tool | Tool docs must include both use cases and non-use cases. | [26](04-tools-agents/26-tool-description-when-not-to-use.md) |
| 27 | Let the application enforce permissions | The model proposes intent; deterministic code enforces permissions and audit. | [27](04-tools-agents/27-intent-vs-permission.md) |
| 28 | Confirm high-risk actions | Publishing, payment, deletion, and configuration changes need confirmation. | [28](04-tools-agents/28-confirm-high-risk-actions.md) |
| 29 | Agent tool-call reliability solution | Use a layered engineering chain for tool definition, selection, validation, confirmation, recovery, and result checks. | [29](04-tools-agents/29-agent-tool-reliability-solution.md) |
| 30 | Prefer workflows before autonomous agents | Fixed flows and long-text loops should be workflowed before agents handle dynamic judgment. | [30](04-tools-agents/30-workflow-before-agent.md) |
| 31 | Define multi-agent ownership boundaries | Each agent needs clear input, output, and responsibility. | [31](04-tools-agents/31-multi-agent-boundaries.md) |
| 32 | Multi-agent systems need verification | More roles are not the goal; independent verification is. | [32](04-tools-agents/32-multi-agent-test-verification.md) |
| 33 | Pass structured handoff context | Handoffs should include goal, evidence, constraints, and open checks. | [33](04-tools-agents/33-structured-handoff-context.md) |
| 34 | Make agent traces replayable | Tool inputs, outputs, and key decisions must be traceable and reproducible. | [34](04-tools-agents/34-replayable-agent-traces.md) |
| Topic | Large-scale Skill coexistence solution | Use registries, routing, retrieval, conflict handling, and dynamic assembly to manage many Skills. | [Topic](04-tools-agents/large-scale-skill-engineering.md) |

## 05. Testing, Evaluation, And Verification

| No. | Practice | Core Rule | File |
| --- | --- | --- | --- |
| 35 | Extend the testing pyramid for AI systems | Combine unit tests, component evals, end-to-end evals, and production monitoring. | [35](05-evaluation-verification/35-extended-test-pyramid.md) |
| 36 | Cover real and boundary cases in eval data | Eval sets need normal, long-tail, failure, and attack cases. | [36](05-evaluation-verification/36-eval-data-real-boundary.md) |
| 37 | Test the process, not only the final answer | Test retrieval for RAG, traces for agents, and format for prompts. | [37](05-evaluation-verification/37-test-intermediate-process.md) |
| 38 | Calibrate LLM-as-judge | Judge models must be aligned with human standards. | [38](05-evaluation-verification/38-calibrate-llm-as-judge.md) |
| 39 | Tie eval metrics to business risk | Higher-risk domains need stricter thresholds and more human review. | [39](05-evaluation-verification/39-metrics-bind-business-risk.md) |
| 40 | Regress every output-affecting change | Prompt, model, knowledge base, and tool changes all need regression tests. | [40](05-evaluation-verification/40-run-regression-on-changes.md) |
| 41 | Include negative and attack cases | Cover hallucination, injection, privilege escalation, and data leakage. | [41](05-evaluation-verification/41-counterexample-attack-samples.md) |
| 42 | Classify failures, not just failure rates | Failure taxonomy turns incidents into actionable fixes. | [42](05-evaluation-verification/42-failure-taxonomy.md) |
| 42A | Separate test-driven and goal-driven observability | Test-driven observation checks whether the chain follows design; goal-driven observation checks whether the design serves the goal. | [42A](05-evaluation-verification/42A-observability-test-goal-driven.md) |

## 06. Feedback And Iteration

| No. | Practice | Core Rule | File |
| --- | --- | --- | --- |
| 43 | Feed production feedback into engineering | User feedback, traces, complaints, and retries should improve the system. | [43](06-feedback-iteration/43-production-feedback-engineering-loop.md) |
| 44 | Close the loop from failure to fix | Failures need triage, root cause, fix, regression, rollout, and monitoring. | [44](06-feedback-iteration/44-failure-to-improvement-loop.md) |
| 45 | Feedback is not always training | Decide whether to change prompts, RAG, tools, product, data, or model. | [45](06-feedback-iteration/45-feedback-not-direct-training.md) |
| 46 | Turn human review into eval standards | Review labels should become eval cases or rubrics. | [46](06-feedback-iteration/46-human-review-to-eval-standards.md) |
| 47 | Monitor quality, cost, latency, and safety together | Do not let one satisfaction metric hide cost, cache hit rate, latency, or risk. | [47](06-feedback-iteration/47-online-metrics-quality-cost-latency-safety.md) |
| 48 | Use gradual rollout | Prompt, model, and agent-policy changes should be released gradually. | [48](06-feedback-iteration/48-gradual-rollout.md) |
| 49 | Prefer explainable failure over lucky success | Systems should expose uncertainty and next recovery steps. | [49](06-feedback-iteration/49-explainable-failure-over-lucky-success.md) |
| 50 | Codify team practices | Standards should cover prompts, tools, evals, traces, safety, and release. | [50](06-feedback-iteration/50-team-standards.md) |
