#!/usr/bin/env python3
"""Deepen lec18 (IPv6 + Routing intro + Dijkstra + Distance Vector)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec18:1": {
  "title": "IPv6 — 为什么要它 ⭐",
  "summary": "IPv4 32 位地址快用完；同时简化 header 加速路由 + 加 flow label。",
  "key_points": [
    "**初始动机**：32 位地址不够用（已分完 2011 年）",
    "**额外动机**：40 字节固定 header 加速路由器处理",
    "**额外**：flow label 给 QoS / 流区分"
  ],
  "explanation": "### IPv4 不够用的根本原因\n32 位地址理论上 2³² ≈ 43 亿。看似很多，但：\n- 历史上分配低效（Class A 给了一家公司 1600 万地址）\n- 移动设备每个都要 IP\n- IoT 上 PB 级别设备数\n\n→ 2011 年 IANA 把最后一段 IPv4 给了区域注册商，从此官方层面 IPv4 用完了。NAT 暂时缓解了痛苦。\n\n### IPv6 不只是『更多地址』\n顺便重新设计：\n- 去掉 IPv4 的累赘（checksum, fragmentation, options）\n- 加 flow label 支持流级别处理\n- 加固定 40 byte header，硬件路由器更好处理\n\n### 部署慢的原因\nIPv4 + NAT 的方案太好用，缺乏强动力换 IPv6。2026 年 Google 统计客户端 IPv6 比例 ~49%。"
},

"lec18:2": {
  "title": "IPv6 Datagram 格式 ⭐",
  "summary": "128-bit 地址；40 B 固定 header；去掉 checksum/fragmentation/options。",
  "key_points": [
    "Version, Priority, Flow Label",
    "Payload Length",
    "Next Header（替代 options 链）",
    "Hop Limit（替代 TTL）",
    "Src/Dst 128 bit",
    "**Payload**"
  ],
  "explanation": "### vs IPv4 的关键变化\n\n| | IPv4 | IPv6 |\n|---|---|---|\n| 地址 | 32 b | 128 b |\n| Header | 20-60 B 变长 | **40 B 固定** |\n| Header checksum | 有 | **无** |\n| Fragmentation by router | 是 | **否**（只在端） |\n| Options | header 内 | next-header 链 |\n| Flow label | 无 | 有 |\n\n### 为什么去掉 header checksum\n- TCP/UDP 已有 checksum\n- Ethernet/数据链路有 CRC\n- IPv4 的 checksum 每跳要重算（因为 TTL 变了），耗 CPU\n→ 重复了，去掉省事\n\n### 为什么禁止路由器分片\n碎片化让中间路由器干太多事，违反 end-to-end principle。改成 sender 自己确保不超过 MTU（用 path MTU discovery）。"
},

"lec18:3": {
  "title": "IPv6 Design Philosophy — End-to-End Principle",
  "summary": "把问题留给端 → 去 frag、去 checksum；统一 options；保留 flow label。",
  "explanation": "### End-to-end argument (1984 classic paper)\n网络中间节点应该尽量简单，复杂功能放在端节点。\n\n例：可靠交付不能由中间路由器保证（即使每跳保证，端到端也可能失败），所以让 TCP 在端到端层面处理。\n\nIPv6 设计直接反映了这条原则：\n- Fragmentation：端做\n- Checksum：端做（TCP/UDP）\n- 路由器只处理 forwarding"
},

"lec18:4": {
  "title": "IPv4 → IPv6 过渡 — Tunneling",
  "summary": "不能一夜换 → IPv6 包封装进 IPv4 包穿越 IPv4 网。",
  "key_points": [
    "No flag days（不能一刀切）",
    "Tunneling = packet in packet",
    "4G/5G 等也大量用 tunneling"
  ]
},

"lec18:5": {
  "title": "Tunneling 详图 (1)",
  "summary": "Ethernet 上 IPv6 router 直接互通时，直接发 IPv6 frame，正常工作。"
},

"lec18:6": {
  "title": "Tunneling 详图 (2)",
  "summary": "IPv4 网络作为 tunnel：IPv6 datagram 作为 payload 塞进 IPv4 datagram。"
},

"lec18:7": {
  "title": "Tunneling 逻辑 vs 物理视图 ⭐",
  "summary": "逻辑上 B-E 像直连 IPv6；物理上 IPv6 包穿过 C、D 的 IPv4 网络。",
  "key_points": [
    "逻辑视图：A(v6) — B(v6/v4) === E(v6/v4) — F(v6)",
    "物理视图：A-B-C-D-E-F，C/D 只看 IPv4 header",
    "B→E 段：IPv6 packet 作为 IPv4 payload",
    "C、D 完全不知道里面装的是 IPv6"
  ],
  "explanation": "### Header 嵌套\nA→F 通信，B→E 段的实际 packet 长这样：\n\n```\n[IPv4 header: src=B, dst=E][IPv6 header: src=A, dst=F][TCP/UDP][data]\n```\n\nC、D 路由器只看外层 IPv4 header，对它来说就是个普通 IPv4 包。E 收到后剥掉 IPv4 header，看到 IPv6 packet，再交给 IPv6 处理。\n\n### 类比\n你寄一个真包裹给纽约的朋友，但邮政只到曼哈顿，所以你把它装进一个曼哈顿的包裹寄到中转站。中转站员工不知道里面是什么，照样按曼哈顿地址投递。"
},

"lec18:8": {
  "title": "IPv6 采用率",
  "summary": "Google 统计：46-49% 客户端用 IPv6 (2026)。"
},

"lec18:9": {
  "title": "IPv6 采用率（续）",
  "summary": "25 年部署，为什么这么慢？NAT 缓解了 IPv4 短缺压力 + 缺乏商业驱动。"
},

"lec18:10": {
  "title": "Network Control Plane — 章节封面",
  "summary": "进入路由协议。"
},

"lec18:11": {
  "title": "Control Plane Roadmap",
  "summary": "LS / DV / OSPF / BGP / SDN / ICMP / SNMP-NETCONF。"
},

"lec18:12": {
  "title": "Network Layer 两功能（复习）",
  "summary": "Forwarding (data plane) vs Routing (control plane)."
},

"lec18:13": {
  "title": "Per-router Control Plane（传统）",
  "summary": "每个 router 独立跑路由算法填自己的 FT。"
},

"lec18:14": {
  "title": "SDN Control Plane（现代）",
  "summary": "Remote controller 算 FT 下发。"
},

"lec18:15": { "title": "Control Plane Roadmap（重）" },

"lec18:16": {
  "title": "What is Routing? — Jon Postel 引言",
  "summary": "『Name 指 what；Address 指 where；Route 指 how』。"
},

"lec18:17": {
  "title": "Routing Protocols 目标",
  "summary": "找『好』路径。好 = 低 cost / 快 / 不堵 / 可靠。"
},

"lec18:18": {
  "title": "Graph Abstraction — 节点、边、cost ⭐",
  "summary": "G = (N, E)，c(a,b) = 直连代价；不连 = ∞。",
  "explanation": "### 抽象\n- N = 节点（router）\n- E = 边（链路）\n- c(a, b) = 链路代价（admin 定义：可基于距离、带宽、cost、congestion 等）\n\n### Cost 的语义\nCost 可以是任何 admin 想优化的指标：\n- 跳数（每条 = 1）\n- 链路延迟\n- 链路带宽倒数\n- 经济成本（跨大西洋链路贵）\n\n### 重要假设\n- 对称（c(a, b) = c(b, a)）？不一定，可能有向\n- 非负？路由算法通常假设（Dijkstra 要求）"
},

"lec18:19": {
  "title": "两种方法论 — Big Mouth vs Whisper ⭐",
  "summary": "**LS = 大嘴**（广播全网）→ 全局视角；**DV = 悄悄话**（只跟邻居）→ 局部视角。",
  "key_points": [
    "**LS**: 每节点广播 (flood) 自己的 link state → 所有节点知道全图 → 跑 Dijkstra",
    "**DV**: 每节点只跟邻居交换 DV → 渐进收敛 → 跑 Bellman-Ford"
  ],
  "explanation": "### 记忆抓手\n- **LS 大嘴**: 把自己知道的（链路状态）告诉所有人\n- **DV 悄悄话**: 只跟身边邻居说自己的『到各处的距离估计』\n\n### 各自的视角\n- LS: 每节点持有完整 graph → 自己算最短路径\n- DV: 每节点只持有『我到每个目的的最短距离估计』，靠邻居交换迭代收敛\n\n### 代表协议\n- LS: OSPF, IS-IS\n- DV: RIP (已废)，BGP（path vector 是 DV 变种）"
},

"lec18:20": {
  "title": "路由算法分类",
  "summary": "Global (LS) vs Decentralized (DV)；Static vs Dynamic。"
},

"lec18:21": { "title": "Control Plane Roadmap — 进入 LS" },

"lec18:22": {
  "title": "Link State Routing — Step 1 本地链路状态",
  "summary": "每个 node 先维护『我直连哪些邻居以及代价』。"
},

"lec18:23": {
  "title": "Link State Routing — Step 2 Flooding ⭐",
  "summary": "每节点把自己的 link state 通过 flooding 发给全网。",
  "key_points": [
    "Node 把自己的 link state（邻居 + 代价）广播",
    "收到的邻居把它转发出去（除了来的方向）",
    "用 sequence number + age 防重复",
    "最终所有节点都收到所有 link state"
  ],
  "explanation": "### Flooding 效率\n朴素 flooding 每条边发 O(n²) 次（每个 link state 沿每条边传一次，n 个节点）。\n\n更聪明的 flooding（OSPF 用的）只在新 LSA 时转发，避免重复 → O(n × E) ≈ O(n²) 但常数小很多。"
},

"lec18:24": {
  "title": "LS — Step 3, 4: 全网拓扑 → Dijkstra",
  "summary": "每个节点拥有完整 graph 后，跑 Dijkstra 算到所有目的的最短路径。"
},

"lec18:25": {
  "title": "Dijkstra — 概念 + 符号",
  "summary": "集中式但每个 node 自己跑（输入是 link state）。",
  "key_points": [
    "**c(x, y)**: 直连代价",
    "**D(v)**: 当前估计的『从源到 v』最小代价",
    "**p(v)**: 前驱节点（用于恢复路径）",
    "**N'**: 已知最优代价的节点集合"
  ]
},

"lec18:26": {
  "title": "Dijkstra 伪代码 ⭐⭐",
  "summary": "Init N'={u}，D(v)=c(u,v) or ∞；Loop: 取 D 最小的 w 加入 N'，relax 邻居。",
  "key_points": [
    "Init: N' = {u}; for v ≠ u: D(v) = c(u, v) if adjacent else ∞",
    "Loop:",
    "  w = argmin_{v ∉ N'} D(v)",
    "  add w to N'",
    "  for each v adjacent to w, v ∉ N':",
    "    D(v) = min(D(v), D(w) + c(w, v))",
    "Until N' = all nodes"
  ],
  "formula": "$$D(v) = \\min(D(v), D(w) + c(w, v))$$",
  "explanation": "### 工作原理（intuition）\nDijkstra 是『波纹扩散』：\n- 从 source 出发，每次扩展到『最近但还没加入的节点』\n- 加入后，看是否能通过它更新到其他节点的距离\n- 重复\n\n### 关键不变量\n**一旦加入 N'，到它的最短距离就定了**。后面更新不再改它。\n\n这要求 **链路代价非负**（负权会让后到的路径反而更短，破坏不变量）。\n\n### 复杂度\n- 朴素：每轮找 min O(n)，n 轮 → O(n²)\n- Heap 实现：每次 extract-min O(log n)，n 轮 + m 次 relax → O((n+m) log n)\n- 对稠密图 O(n²) 更好；稀疏图 heap 版更好\n\n### 跟 BF 对比\nDijkstra 假设非负权 + 贪心；BF 允许负权（但 4119 没用过），所有边 relax n-1 轮。"
},

# Pages 27-38 are step-by-step Dijkstra examples — keep brief
"lec18:27": { "title": "Dijkstra 例 — Step 0 (Init)", "summary": "N'={u}；D(v)=2, D(w)=5, D(x)=1, D(y)=∞, D(z)=∞。"},
"lec18:28": { "title": "Dijkstra 例 — Step 1 选 x", "summary": "D 最小是 x (1)，加入 N'。" },
"lec18:29": { "title": "Dijkstra 例 — Step 1 relax", "summary": "Relax x 邻居：D(v)=min(2, 3)=2; D(w)=min(5, 4)=4; D(y)=min(∞, 2)=2。" },
"lec18:30": { "title": "Dijkstra 例 — Step 2 选 y", "summary": "D 最小是 y (2)，加入 N'。" },
"lec18:31": { "title": "Dijkstra 例 — Step 2 relax", "summary": "Relax y 邻居：D(w)=min(4, 3)=3; D(z)=min(∞, 4)=4。" },
"lec18:32": { "title": "Dijkstra 例 — Step 3 选 v", "summary": "D 最小是 v (2)，加入 N'。" },
"lec18:33": { "title": "Dijkstra 例 — Step 3 relax", "summary": "Relax v 邻居：D(w)=min(3, 5)=3 不变。" },
"lec18:34": { "title": "Dijkstra 例 — Step 4 选 w", "summary": "D 最小是 w (3)，加入 N'。" },
"lec18:35": { "title": "Dijkstra 例 — Step 4 relax", "summary": "Relax w 邻居：D(z)=min(4, 8)=4 不变。" },
"lec18:36": { "title": "Dijkstra 例 — Step 5 选 z 完成", "summary": "N'={u,x,y,v,w,z} = 全集。" },
"lec18:37": { "title": "Dijkstra 例 — 最终表", "summary": "完整 5 步表 + 各 D, p 值。" },

"lec18:38": {
  "title": "Dijkstra — 最短路径树 + 转发表 ⭐",
  "summary": "结果是从 source u 的最短路径树 + 对应 forwarding table。",
  "key_points": [
    "最短路径树：从 u 出发，每条边代表一段最短路径",
    "Forwarding table：到每个目的，下一跳走哪个邻居（即第一条边）",
    "u 到 v 直连 → next hop = (u, v)",
    "u 到其他全部经 x → next hop = (u, x)"
  ]
},

"lec18:39": {
  "title": "Dijkstra 复杂度 ⭐",
  "summary": "O(n²) 朴素，O(n log n) heap。每节点 broadcast 自己 link state → 消息 O(n²)。",
  "key_points": [
    "时间：每轮检查 n 节点，n 轮 → O(n²)",
    "Heap 实现 O((n+m) log n)",
    "消息：每节点 flood 一次 link state，每次 O(n) 链路传 → 总 O(n²)"
  ]
},

"lec18:40": {
  "title": "Dijkstra 震荡问题",
  "summary": "当 link cost 跟流量相关时，路由可能震荡。",
  "explanation": "### 场景\n4 个节点环形，A、B、C、D 都想往某节点发流量。如果链路 cost = 当前流量：\n- 一开始大家走某路径\n- 路径变拥挤 → cost 升 → 大家切到另一路径\n- 那条变拥挤 → 又切回来\n- 反复震荡\n\n### 解药\n- 用静态 cost（不跟流量挂钩）\n- 或者用更平滑的 cost 更新（EWMA）\n- 或者只在 cost 大幅变化时才触发更新"
},

"lec18:41": { "title": "两种方法论复习 — 进入 DV" },

"lec18:42": {
  "title": "Time for a Game — DV 直觉演示",
  "summary": "课堂游戏：『只跟邻居说话，找最多现金的人』。模拟 DV。",
  "explanation": "**游戏规则**：教室里每人代表一个 router，只能跟左右邻居说话（不能广播、不能手势），3 分钟内找出『谁现金最多』。\n\n**对应 DV**：每个 router 把『我知道的最大值』告诉邻居，邻居更新自己的最大值再传播。最终最大值会扩散到全网。\n\n这就是 BF 收敛的直觉。"
},

"lec18:43": {
  "title": "Distance Vector — Bellman-Ford 方程 ⭐⭐",
  "summary": "D_x(y) = min over neighbors v of [c(x, v) + D_v(y)]。",
  "formula": "$$D_x(y) = \\min_{v \\in N(x)} \\{ c(x, v) + D_v(y) \\}$$",
  "key_points": [
    "min 取自所有邻居 v",
    "c(x, v) = 直连代价",
    "D_v(y) = v 估算到 y 的距离",
    "Iterative：邻居发新 DV → 自己更新 → 自己 DV 变了告诉邻居",
    "**异步、自停**：稳定后没新 update 就不再发"
  ],
  "explanation": "### 直觉\n『我到 y 多远？』= 『先到任意邻居 v 的代价，加上 v 自己估算的到 y 的代价，取最小』。\n\n这条公式是动态规划的经典应用（Bellman-Ford 的核心）。\n\n### 例\n邻居 B 告诉 x：『我到 y 是 5』。\nc(x, B) = 2。\n那么经 B 到 y = 2 + 5 = 7。\n\n邻居 C 告诉 x：『我到 y 是 4』。\nc(x, C) = 4。\n经 C 到 y = 4 + 4 = 8。\n\nx 取 min(7, 8) = 7 → 把这个值放进自己的 DV。如果跟自己原来的值不同 → 告诉所有邻居。\n\n### 跟 Dijkstra 的关系\nDijkstra 集中式贪心；BF 分布式迭代。两者最优路径相同（前提是非负权）。BF 的优势：不需要全图，每节点只跟邻居说话。"
},

"lec18:44": {
  "title": "Distance Vector Table — 数据结构 ⭐",
  "summary": "每节点维护一张表：行=目的，列=经哪个邻居。DV = 每行 min。",
  "key_points": [
    "Distance table dist_v(x, y) = x 经邻居 v 到 y 的代价",
    "DV = 每行的 min（最优经哪个邻居）",
    "邻居发来的『我到 y 是多少』就是它的 DV[y]"
  ]
},

"lec18:45": {
  "title": "DV — 初始化",
  "summary": "只填直连邻居的列；其他经邻居到非直连目的都是 ∞。"
},

"lec18:46": {
  "title": "DV — Init 例 (4 节点)",
  "summary": "A 直连 B(5), C(6), D(8)；A 的初始 DV: B=5, C=6, D=8。"
},

"lec18:47": {
  "title": "DV — 发送 DV 给邻居",
  "summary": "每节点把自己的 DV（不是整个表）发给所有邻居。"
},

"lec18:48": {
  "title": "DV — 邻居用 BF 更新 ⭐",
  "summary": "邻居 v 发来 DV：x 用 BF 算 dist_v(x, y) = c(x, v) + D_v(y)，更新自己的表。",
  "explanation": "### 例\nB 发自己的 DV 给 A：『B 到 C = 1, B 到 D = ∞, B 到 A = 5』\n\nA 用 BF 更新：\n- A 经 B 到 C = c(A,B) + D_B(C) = 5 + 1 = **6**\n- A 经 B 到 D = c(A,B) + D_B(D) = 5 + ∞ = ∞\n\nA 自己的 distance_table 经 B 列更新：(C=6, D=∞)\nA 的 DV: 每行 min。"
},

"lec18:49": {
  "title": "DV Algorithm — 核心 loop",
  "summary": "周期性发自己的 DV；收到邻居的 DV 就更新；DV 变就通知。"
},

"lec18:50": {
  "title": "DV — 异步、自停",
  "summary": "Iterative + 异步：本地链路 cost 变或邻居 DV 来就触发。DV 不变 → 不通知 → 停。"
},

"lec18:51": {
  "title": "DV — Link Cost 变（好消息传得快）",
  "summary": "Y-X 从 4 变 1：好消息几轮内全网知道。",
  "explanation": "### 直觉\nY 检测到 cost ↓ → 立刻更新自己的 DV（D_Y(X) 变小）→ 告诉邻居 → 邻居更新 → 全网在 O(diameter) 轮内收敛。"
},

"lec18:52": {
  "title": "DV — Count-to-Infinity ⭐⭐",
  "summary": "链路涨价时坏消息传得慢，可能两 router 互推 +1 +1 直到 ∞。",
  "key_points": [
    "X-Y 从 4 变 60",
    "Y 当前 DV: 经 Z 到 X = 6（用 Z 之前给的值）",
    "但 Z 当前 DV: 经 Y 到 X = 4+1 = 5（基于过期的 X-Y=4）",
    "Y 把 6 告诉 Z；Z 把 5 告诉 Y；互相参考过期信息",
    "每轮代价 +1 +1 ... 直到达到 max (RIP 用 16=∞)"
  ],
  "explanation": "### 完整故事\n\n场景：网络 X-Y-Z-...-W，原本 X-Y cost = 4，X 到 W 的最短路径经过 Y。\n\nT=0: Z 的 DV 说『我到 X = 5（经 Y）』；Y 的 DV 说『我到 X = 4（直连）』。\n\nT=1: X-Y 链路代价从 4 变成 60。Y 检测到，更新自己：『直连 X = 60』。但 Y 也看到 Z 之前发的『Z 到 X = 5』，所以 Y 算『经 Z 到 X = c(Y,Z) + 5 = 1 + 5 = 6』。Y 选 min(60, 6) = **6**。Y 把『Y 到 X = 6』告诉 Z。\n\nT=2: Z 收到『Y 到 X = 6』。Z 之前是『Z 经 Y 到 X = 1+4 = 5』，现在变成『Z 经 Y 到 X = 1+6 = 7』。Z 更新自己 DV: 『Z 到 X = 7』。告诉 Y。\n\nT=3: Y 看到『Z 到 X = 7』。重算『Y 经 Z 到 X = 1+7 = 8』。Y 的 DV：min(60, 8) = 8。告诉 Z。\n\nT=4: Z 算『Z 经 Y 到 X = 1+8 = 9』...\n\n每轮 +2，直到达到某个上限（比如 60，意识到直连 60 也比绕圈强）。RIP 用 16 表示 ∞，所以 RIP 网络直径不能超过 15。\n\n### 为什么慢\n核心问题：Y 和 Z 互相用对方过期的信息推自己 → 形成局部环 → 每轮缓慢逼近真实代价。\n\n### 解药\nPoison reverse（下页）+ split horizon。"
},

"lec18:53": {
  "title": "DV — Poison Reverse ⭐",
  "summary": "Z 经 Y 到 X → Z 告诉 Y 自己到 X 是 ∞（避免 Y 拿 Z 当 fallback）。",
  "key_points": [
    "如果『我经你到 X』，我就告诉你『我到 X = ∞』",
    "这样你不会再用我做 fallback",
    "破 2 节点环",
    "**不能破 3+ 节点环**"
  ],
  "explanation": "### 工作机制\n回到上一页的例子：Z 当前路径『经 Y 到 X』。Z 主动告诉 Y：『Z 到 X = ∞』（说谎，但有目的）。\n\n这样当 Y 算『Y 经 Z 到 X』时，得到 1 + ∞ = ∞，不会选 Z。Y 只能用『Y 直连 X = 60』，正确收敛。\n\n### 局限\n3 节点环：Y, Z, W 都互相 poison reverse 处理，但 4 个节点的环就破不掉。这是 DV 的根本局限。\n\n### Split horizon\n弱版 poison reverse：『从你那学到的，不告诉你』。不主动说 ∞，但也不会把循环信息传回去。\n\n### 考法\n『poison reverse 解决什么？』『能完全解决 CTI 吗？』必答：不能，只解 2 节点环。"
},

"lec18:54": {
  "title": "LS vs DV 完整对比 ⭐⭐⭐",
  "summary": "Message complexity, 收敛速度, 鲁棒性 — 三大维度。",
  "key_points": [
    "**消息**: LS O(n²) flood；DV 仅邻居间",
    "**收敛**: LS 快但可能震荡；DV 慢且可能 CTI",
    "**错传**: LS 错只影响本地；DV 错全网传染（黑洞效应）"
  ],
  "explanation": "### 完整对比表（必须能默写）\n\n|  | LS | DV |\n|---|---|---|\n| 视角 | 全局 | 局部 |\n| 算法 | Dijkstra | Bellman-Ford |\n| 消息 | O(n²) flood | 邻居间 |\n| 收敛 | 快 | 慢、可能 CTI |\n| 震荡 | 可能（流量依赖时）| 较少 |\n| 错误鲁棒 | 本地化（一个 router 报错代价只影响计算）| **全网传染**（一个 router 报错距离，其他 router 受影响）|\n| 例 | OSPF, IS-IS | RIP (废)，BGP 是变种 |\n\n### 黑洞效应\nDV 下，一个 router 谎报『我到 X 是 1』（其实是 ∞）→ 其他 router 学到『经它 1 跳到 X』→ 大量流量过它 → 它直接 drop → 流量黑洞。\n\nLS 下，单个 router 错报 link state 也会影响别人，但**它只能错报自己的链路**（不能假装别人的链路），影响范围有限。\n\n### 考法（高频）\n『LS 和 DV 各自优缺点？』必背全 6 行。\n\n『为什么 BGP 用 path vector 不用 LS？』→ Inter-AS 不能让别人看到自己内部拓扑（隐私 + 安全 + scale）。"
},

}

def main():
    data = json.loads(DETAIL.read_text())
    data.update(NEW)
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"updated {len(NEW)} entries; total now {len(data)}")

if __name__ == "__main__":
    main()
