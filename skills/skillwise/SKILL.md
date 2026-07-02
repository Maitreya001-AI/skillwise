---
name: skillwise
description: skillwise 工具箱的统一显式入口。仅在用户明确提及 skillwise 工具箱本身时相关。
disable-model-invocation: true
allowed-tools: Bash(python3:*) Bash(ls:*) Read Grep
---

# /skillwise — 工具箱的显式入口

**What this is.** skillwise 工具箱的显式入口：给它一个技能路径、一段需求、或一批语料，它依据可观察证据把你送进正确的那扇门（evaluate / improve / write / seek），然后退出。它不编排后续工作。它填的缺口：关于工具箱自身的 Σ（生命周期状态 → 四扇门的映射、裁决产物的识别约定）加一组 φ 路由判据；显式调用时用户即路由器（THEORY §2 消费点），本技能替代的是"翻 README 自学四扇门"。

**先探测。** 对 `$ARGUMENTS` 运行 `python3 scripts/probe.py "$ARGUMENTS"`，得到 `state` 与 `evidence`。探测先于路由是依赖顺序（THEORY §3 第 1 格：无法路由尚未分类的状态）。裁决产物的识别约定已编译进探针——它只认 `<skill-dir>/wise-eval.json`（evaluate-skill 的钉死落盘位置），不做模糊猜测。

**路由判据表。** 各行是状态到门的映射判据，不是执行步骤；命中即移交：

| 证据组合 | 门 | 理由 |
|---|---|---|
| `exists_with_verdict` | **improve-skill** | 已有裁决，下一步是修（裁决为 nogap 时 improve 的入口自会退役它，不归本入口管） |
| `exists_no_verdict` | **evaluate-skill** | 存在但无裁决——先要裁决 |
| `no_path` / `path_not_found`，且输入含语料形态（轨迹、日志、对话记录、成批样例文件） | **seek-skill** | 目标须从语料中发现 |
| `no_path` / `path_not_found`，且输入是规格形态（描述想要什么的文字） | **write-skill** | 目标已给定 |
| 请求文本的动词信号（"为什么不触发"→裁决；"改/修"→改进；"做一个"→写） | 佐证 | 与文件证据冲突时，**文件证据优先**（可观察 > 转述） |

**平局规则（先于提问适用）：**

- 规格与语料同时在场 → **seek-skill**（seek 可把规格当先验消费；write 不能消费语料）。
- `path_not_found` → 在移交语中明确说明"路径未解析"，再按剩余输入的形态走 seek/write 行。

**残差问题（至多一个）。** 仅当判据表与平局规则均无法唯一裁决时（典型：空手 `/skillwise` 且无任何输入），问恰好一个问题，选项即未决的分支："已有技能要处理，还是要新技能？新技能的话，手上是需求描述还是一批语料？"得到回答后移交。不进行第二轮追问；仍无法裁决则如实说明缺什么证据并停止。（§6 seam 定理：判据用尽处归人；判据未用尽处不问。）

**移交格式与停止。** 移交是一行带证据的陈述 + 调用目标技能：

```
路由：<门> —— 依据：<evidence 逐条>。
```

随后调用目标技能（插件安装下名称可能带命名空间，如 `skillwise:evaluate-skill`），把路径/输入原样交给它。**移交即本技能职责终点**：不监督、不串联下一扇门、不复述目标技能的做法。（γ 自约束；违反即长成 §3 排除的 procedure。）

**done_when**：输出了带 ≥1 条可观察证据的路由行并完成一次移交；或至多一个残差问题后完成移交；或如实声明证据不足并停止。三者之一，别无其他出口。
