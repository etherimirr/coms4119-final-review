#!/usr/bin/env python3
"""Full per-page rewrite for lec16 (TCP fairness recap + Network Layer DP, 45 pages)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec16:1": {
  "title": "ECN — Explicit Congestion Notification（lec14 末尾延续）",
  "summary": "**ECN**: TCP 部署常用 network-assisted CC。Router 在 IP header (ToS field) 用 **2 个 bit** 标记 congestion。Congestion 信号通过 destination 携带回 sender (ACK 中 ECE=1)。涉及 IP (ECN bit marking) 和 TCP (CWR / ECE header bit) 两层协作。",
  "key_points": [
    "Router 在 IP ToS field 用 2 bit 标 congestion",
    "Policy 决定 marking (by network operator)",
    "Congestion indication 传到 destination",
    "Receiver 在 ACK segment 中设 ECE bit (Echo)",
    "**IP + TCP 双层协作**",
    "Sender 见 ECE=1 → 减半 cwnd 但不丢包"
  ],
  "explanation": "**为什么 ECN**：loss-based TCP 必须等到 buffer 满 → 丢包 → 重传。这浪费：(1) Queue 满了延迟大；(2) 重传消耗带宽；(3) 反应晚。\n\nECN 让 router 在 queue 长度超阈值时（还没满）就标记包。Receiver 通过 ACK 把信号传回 sender。Sender 提前减速 → 队列降回稳态。\n\n**IP + TCP 协作**:\n- IP 层: ECN 字段 (ToS 低 2 bit)\n- TCP 层: ACK header ECE bit + next packet CWR bit (确认收到 ECE)\n\n**协商**: ECN 双方必须支持。建连时 SYN 的 ECE+CWR 都设 1 表示『I support ECN』。\n\n**部署**: Linux 默认开 ECN（被动响应）。\n\n**考点**：『ECN 是什么？谁参与？为什么有用？』必背 IP+TCP 双层 + 无丢包减半。"
},

"lec16:2": {
  "title": "TCP Fairness — 目标",
  "summary": "**Fairness goal**: 如果 K 个 TCP sessions 共享同一个 bottleneck link of bandwidth R，每个 should have average rate R/K。\n\n例图：2 个 TCP connection 共享 capacity R 的 bottleneck router。",
  "key_points": [
    "K 个 TCP session 共享 bottleneck R",
    "理想: 每个 R/K",
    "AIMD 是否能实现这一目标？(下页)"
  ]
},

"lec16:3": {
  "title": "TCP 是否 Fair？— AIMD 几何论证",
  "summary": "**Q: Is TCP fair？** **A: Yes, under idealized assumptions**: (a) same RTT; (b) fixed number of sessions; (c) only in congestion avoidance phase。\n\n**论证**: 2 个 TCP 共享 R bottleneck。AIMD: additive increase 给 slope 1（throughput 同步增）；multiplicative decrease 按比例缩。两步交替 → 螺旋收敛到 equal bandwidth share。",
  "key_points": [
    "TCP fair under idealized assumptions",
    "Assumption 1: **same RTT**",
    "Assumption 2: fixed # sessions",
    "Assumption 3: 长期都在 congestion avoidance",
    "Geometric: AI 走 45° + MD 沿原点缩 → 收敛到公平线"
  ],
  "explanation": "**几何论证 (经典)**：\n\n2 个 user，x 轴 = user 1 throughput，y 轴 = user 2 throughput。\n\n- **Equal bandwidth share line**: x = y\n- **Loss line**: x + y = R\n\n**AIMD 动作**:\n- AI: 两 user throughput 同步 +Δ → 沿 45° 走\n- MD: 两 user throughput ×0.5 → 沿原点向下缩\n\n**轨迹**: 走 45° → 触 loss line → 缩 0.5 → 又走 45° → ...\n\n**关键观察**: MD 沿原点缩 → 比例保持，但 x-y 差距按比例缩小。AI 不改变差距。MD 反复执行 → 差距渐近 0 → **收敛到 x=y (公平线)**。\n\n**Why only AIMD**: \n- AIAD: 加法增 + 加法减都不改差距 → 不收敛\n- MIMD: 比例增 + 比例减 → 比例保持但不公平\n- **唯独 AIMD**: AI 不改差距 + MD 按比例缩差距 → 收敛\n\n**考点**: 『为什么 AIMD 收敛公平？』必答几何论证。"
},

"lec16:4": {
  "title": "Fairness — UDP 和 Parallel TCP 破坏公平",
  "summary": "**Fairness, UDP**: 多媒体 app 常用 UDP 而非 TCP（不想被 CC throttle）。UDP 发常速率，容忍包丢。**没有 Internet police** 管这事。\n\n**Fairness, Parallel TCP**: 浏览器可以开多个 parallel TCP connection 给同 host。例: link R, 9 现有 connections。新 app 1 TCP → 拿 R/10；新 app 11 TCPs → 拿 R/2。",
  "key_points": [
    "**UDP**: 多媒体 app 不被 CC throttle",
    "**Parallel TCP**: 开 N 条抢 N/M 份额",
    "**没 Internet police** 强制 fair",
    "实际 fairness 是『最佳努力』"
  ],
  "explanation": "**UDP 不公平例**: \n- Skype, Zoom, Netflix 多媒体用 UDP\n- 不受 CC 限制，可以一直 push\n- 跟旁边的 TCP 一起跑，UDP 抢更多带宽\n\n**Parallel TCP**: \n- 浏览器（如 Chrome）对同一 host 默认开 6 个 parallel 连接\n- 每个连接是独立 TCP，独立 AIMD\n- 6 个一起跟 1 个对手抢，比例 6:1\n- 现代 HTTP/2 把多请求 multiplex 到 1 个 TCP（减少这种 abuse）\n\n**考点**: 『TCP fairness 是否在实际成立？』→ 不一定，UDP 和 parallel TCP 都破坏。"
},

"lec16:5": {
  "title": "Bottom Line — Active Research Topic",
  "summary": "TCP CC 是 active research topic。给出 URL: http://cpham.perso.univ-pau.fr/TCP/。",
  "key_points": ["参考资料 page"]
},

"lec16:6": {
  "title": "Bottom Line — 论文列表",
  "summary": "近期 TCP 相关论文示例:\n- TCP ex Machina: Computer-Generated CC (SIGCOMM 2013)\n- Recursively Cautious CC (NSDI 2014)\n- PCC (NSDI 2015)\n- Principles for Internet Congestion Management (SIGCOMM 2024)\n- CCAnalyzer (SIGCOMM 2024)\n- CClinguist (SIGCOMM 2025)\n- LeoCC: 卫星 CC (SIGCOMM 2025)\n\n... and maybe your future paper :)",
  "key_points": ["TCP CC 仍是 active research", "学术界仍在改进"]
},

"lec16:7": {
  "title": "CSEE4119 — Network Layer Data Plane 章节封面",
  "summary": "新章节: **Network Layer – Data Plane**。Xia Zhou 教，引 Kurose-Ross 教材。\n\nNetwork Layer 是 OSI L3，提供端到端 packet delivery。本章先讲 data plane (forwarding)，下一章 (lec18-19) 讲 control plane (routing)。",
  "key_points": [
    "新章节: Network Layer Data Plane",
    "Data plane = forwarding (per-router, hardware ns)",
    "Control plane = routing (network-wide, software ms)",
    "本章只讲 data plane"
  ]
},

"lec16:8": {
  "title": "Move on to Network Layer",
  "summary": "协议栈进入 L3：\n\n- L7 App (HTTP, FTP, DASH, DNS)\n- L4 Transport (TCP, UDP)\n- **L3 Network (IP)** ← here\n- L2 Data Link (Ethernet, 802.11, PPP)\n- L1 Physical (optical, copper, radio, PSTN)",
  "key_points": [
    "Network layer = L3",
    "Single protocol: **IP**",
    "下面 L2: Ethernet/802.11/PPP",
    "上面 L4: TCP/UDP"
  ]
},

"lec16:9": {
  "title": "Network Layer Data Plane Roadmap",
  "summary": "本章议程：\n\n(1) Network layer overview (DP + CP)\n(2) What's inside a router (input ports, switching, output ports, buffer mgmt, scheduling)\n(3) IP: Internet Protocol (datagram format, addressing, NAT, IPv6)\n(4) Generalized Forwarding, SDN\n(5) Middleboxes",
  "key_points": [
    "Network layer overview",
    "Router internals",
    "IP protocol",
    "Generalized forwarding + SDN",
    "Middleboxes"
  ]
},

"lec16:10": {
  "title": "Network-Layer Services and Protocols",
  "summary": "**Transport segment** 从 sender 到 receiver。\n\n- **Sender**: 把 segments **encapsulate** 进 datagrams, 传给 link layer\n- **Receiver**: deliver segments 给 transport layer protocol\n- **每 Internet 设备都有 network layer protocols** (hosts, routers)\n- **Routers**: examine header fields in all IP datagrams passing through; move datagrams from input ports to output ports along end-end path",
  "key_points": [
    "Sender: encapsulate segment → datagram",
    "Receiver: deliver segment → upper layer",
    "每 Internet 设备都跑 IP layer",
    "Router: 看 header，input port → output port"
  ]
},

"lec16:11": {
  "title": "Two Key Network-Layer Functions — Forwarding vs Routing",
  "summary": "**Forwarding** (data plane): move packets from router's input link to appropriate router output link。**Routing** (control plane): determine route taken by packets from source to destination。\n\n**类比 trip**: forwarding = process of getting through single interchange; routing = process of planning trip from source to destination。",
  "key_points": [
    "**Forwarding**: single router, input → output port",
    "**Routing**: network-wide, source → dest",
    "Analogy: forwarding = pass intersection; routing = plan trip",
    "Routing algorithms 决定 forwarding table 内容"
  ],
  "explanation": "**这是 network layer 最重要的概念分离**。\n\n**Forwarding (data plane)**: \n- 速度: ns 级硬件\n- 范围: 单 router 内\n- 输入: packet header\n- 输出: 哪个 output port\n\n**Routing (control plane)**: \n- 速度: ms 级软件\n- 范围: 全网\n- 输入: 网络拓扑 + link cost\n- 输出: 每 router 的 forwarding table\n\n**两者协作**: routing 算出 table → forwarding 用 table 转发。\n\n**考点**：『Forwarding vs Routing？』必答两者层级 + 时间尺度 + 范围。"
},

"lec16:12": {
  "title": "Data Plane vs Control Plane — 两种 control plane 结构",
  "summary": "**Data plane**: local, per-router function; determines how datagram on input port forwards to output port (based on header values).\n\n**Control plane**: network-wide logic; determines how datagram routes among routers along end-end path.\n\n**Two control-plane approaches**:\n(1) Traditional routing algorithms: implemented in routers\n(2) Software-defined networking (SDN): implemented in (remote) servers",
  "key_points": [
    "**Data plane**: per-router, based on header values",
    "**Control plane**: network-wide logic",
    "**Approach 1 (传统)**: 每 router 跑 routing algorithm",
    "**Approach 2 (SDN)**: remote server 集中算",
    "两者都构造 FT 给 data plane 用"
  ],
  "explanation": "**核心区别再强调一次**：\n\n| | Data Plane | Control Plane |\n|---|---|---|\n| 范围 | 单 router | 全网 |\n| 时间 | ns (硬件) | ms (软件) |\n| 内容 | 用 FT 转发 | 算 FT |\n| 谁运行 | router 硬件 | router 软件 / SDN controller |\n\n**两种 CP 模式**：\n1. **传统**: 每 router 跑自己的路由算法（OSPF/BGP），互相通信，分布式协调\n2. **SDN**: 远程 controller 集中算，下发到所有 router\n\n**SDN 优势**: 易管理 + 易编程 + 全局优化。\n**SDN 劣势**: 单点（实际分布式 controller 缓解）。\n\n**考点**: 用户特别强调的概念页 — 必答 DP vs CP 区别 + 两种 CP 结构。"
},

"lec16:13": {
  "title": "Per-router Control Plane",
  "summary": "**传统模式**: individual routing algorithm components in each and every router interact in the control plane。Routing algorithm 在 control plane (软件)，FT lookup 在 data plane (硬件)。",
  "key_points": [
    "传统 router 内部: routing algorithm + FT",
    "Algorithms 间互相通信",
    "Software 算法 (CP) + hardware 转发 (DP)",
    "经典模式"
  ]
},

"lec16:14": {
  "title": "Software-Defined Networking (SDN) Control Plane",
  "summary": "**SDN 模式**: remote controller computes, installs forwarding tables in routers。Routers 只执行 FT，不自己算。\n\n图: Remote Controller → 控制每 router 的 CA (Control Agent)。",
  "key_points": [
    "Remote controller 算 FT",
    "下发到每 router",
    "Routers 退化为 'dumb pipe' (DP only)",
    "详见 lec20"
  ]
},

"lec16:15": {
  "title": "Network-Layer Service Model — 表",
  "summary": "**比较网络架构的 QoS 保证**:\n\n| Architecture | Service Model | BW | Loss | Order | Timing |\n|---|---|---|---|---|---|\n| **Internet** | best effort | none | no | no | no |\n| **ATM** | Constant Bit Rate | Const rate | yes | yes | yes |\n| **ATM** | Available Bit Rate | Guaranteed min | no | yes | no |\n| **Internet** | Intserv Guaranteed (RFC 1633) | yes | yes | yes | yes |\n| **Internet** | Diffserv (RFC 2475) | possible | possibly | possibly | no |",
  "key_points": [
    "**Internet best-effort**: 无任何保证",
    "**ATM CBR**: 固定速率",
    "**ATM ABR**: 保证最小",
    "**IntServ**: QoS 保证",
    "**DiffServ**: 可能保证（marking）"
  ],
  "explanation": "**Internet best-effort 的含义**：\n- 不保证 packet 一定到达\n- 不保证带宽\n- 不保证顺序\n- 不保证延迟\n\n**ATM (Asynchronous Transfer Mode)**: 1990s 替代方案，提供 QoS。复杂，最终没赢过 IP+best-effort。\n\n**IntServ**: per-flow QoS reservation。Scalability 问题 (router 要为每 flow 记状态)。\n\n**DiffServ**: 类别化 QoS（packet 打 tag），更可扩展，部分采用。"
},

"lec16:16": {
  "title": "Service Model — 完整表 (复习)",
  "summary": "(同上表，完整列出 5 个 service model 的 QoS 保证)。",
  "key_points": ["重复表 — 5 个 service model 对比"]
},

"lec16:17": {
  "title": "Reflections on Best-Effort Service",
  "summary": "**为什么 Internet 选 best-effort**:\n\n(1) **Simplicity of mechanism** allowed Internet to be widely deployed adopted。\n\n(2) **Why packet-switching?** 无 BW waste upon bursty traffic; allow multiplexing over same set of links。\n\n(3) **Why best-effort?** Simpler (no BW reservation); easier to survive failures。\n\n**结论**: It's hard to argue with success of best-effort service model。",
  "key_points": [
    "Simplicity → widespread deployment",
    "Packet-switching: bursty 不浪费 + multiplex",
    "Best-effort: 简单 + 容错",
    "事实证明: 'success' argument"
  ],
  "explanation": "**核心 wisdom**: 不要为 99% 用例不存在的功能（如 strict QoS）增加复杂度。Internet 赢就赢在『差不多够用，但极简、极开放、极可扩展』。\n\n**对比**: ATM 当年承诺更好的 QoS，但复杂度高，最终被 IP+best-effort 打败。"
},

"lec16:18": {
  "title": "Network Layer Data Plane Roadmap — 进入 router 内部",
  "summary": "目录: 接下来讲 'What's inside a router' — input ports, switching, output ports, buffer mgmt, scheduling。",
  "key_points": ["进入 router 架构详讲"]
},

"lec16:19": {
  "title": "Router Architecture Overview — High-Level",
  "summary": "**High-level view of generic router**:\n\n- **Routing processor**: routing, management — control plane (软件), ms 级\n- **Forwarding data plane** (硬件), ns 级\n- **High-speed switching fabric**: 连 input + output ports\n- **Input ports** ← packets in\n- **Output ports** ← packets out",
  "key_points": [
    "Routing processor (软件, ms): CP",
    "Switching fabric + ports (硬件, ns): DP",
    "Input ports + Output ports",
    "两个时间尺度: ms vs ns"
  ]
},

"lec16:20": {
  "title": "Router Architecture — 类比 (火车站)",
  "summary": "Analogy view: \n- **Station manager**: routing & management (control plane)\n- **Roundabout**: forwarding data plane\n- **Entry stations** → **roundabout** → **exit roads**",
  "key_points": [
    "Manager (CP) = 火车站长 (规划调度)",
    "Roundabout (DP) = 转盘 (实际通过)",
    "类比帮助理解 CP/DP 分离"
  ]
},

"lec16:21": {
  "title": "Input Port Functions (1) — Lookup + Forwarding",
  "summary": "**Input port** 三阶段:\n\n1. **Line termination** + physical layer: bit-level reception\n2. **Link layer protocol** (receive): e.g. Ethernet\n3. **Lookup, forwarding, queueing**: decentralized switching\n   - **Match plus action** (FT 在 input port memory)\n   - 用 header field values lookup output port\n   - **目标**: complete input port processing at 'line speed'\n   - Input port queueing: if datagrams arrive faster than fabric rate",
  "key_points": [
    "Input port 三阶段: physical → link → lookup",
    "Lookup 在 input port memory (FT cache)",
    "Goal: line speed processing",
    "Decentralized switching (每 port 自己查表)",
    "**Match plus action** abstraction"
  ],
  "explanation": "**Decentralized switching**: 每 input port 有自己的 FT 复本，独立查表。避免单点瓶颈。\n\n**Line speed**: 10 Gbps Ethernet 上 packet 间隔几十 ns，input port 必须在这个时间内完成 lookup → output port 决策。所以硬件实现（ASIC/TCAM）。"
},

"lec16:22": {
  "title": "Input Port Functions (2) — Destination vs Generalized Forwarding",
  "summary": "两种 forwarding 模式:\n\n(1) **Destination-based forwarding** (传统): forward based only on **destination IP address**。\n\n(2) **Generalized forwarding**: forward based on **any set of header field values** (L2/L3/L4 多字段)。",
  "key_points": [
    "Destination-based: 只看 dst IP",
    "Generalized: 看任意 header 字段 (SDN/OpenFlow)",
    "两种都是 'match + action'"
  ],
  "explanation": "**Destination-based 是历史**: 古典 router 只按 dst IP 转发。\n\n**Generalized 是现代**: SDN/OpenFlow 让一台设备能做 router + firewall + NAT + load balancer 等多种 box 的事（用同一个 flow table）。详见 lec20。"
},

"lec16:23": {
  "title": "Destination-Based Forwarding",
  "summary": "传统 router: forwarding table 按 dst IP 范围分。例: 3 个 link interface (0, 1, 2, 3)，每个负责一段 dst IP 范围。\n\n**Q: 但 ranges 不整齐怎么办？** → 下页 Longest Prefix Matching。",
  "key_points": [
    "Forwarding table: dst IP range → interface",
    "Ranges 可能不整齐 (CIDR)",
    "→ Longest Prefix Matching (LPM)"
  ]
},

"lec16:24": {
  "title": "Longest Prefix Matching — 概念",
  "summary": "**Longest prefix match**: when looking for forwarding table entry for given dst address, **use longest address prefix that matches dst address**。\n\nTable 例:\n- 11001000 00010111 00010*** ********  → Link 0\n- 11001000 00010111 00011000 ********  → Link 1\n- 11001000 00010111 00011*** ********  → Link 2\n- otherwise → Link 3",
  "key_points": [
    "Multiple matching rules → 选 longest",
    "通配符 * 在 rule 中",
    "Examples: 11001000.00010111.00010110.10100001 → which interface?",
    "11001000.00010111.00011000.10101010 → ?"
  ]
},

"lec16:25": {
  "title": "LPM 例 1 — match!",
  "summary": "Packet dst = 11001000.00010111.00010110.10100001\n\nCompare with rules:\n- 11001000.00010111.00010***.******** (Link 0) → **位 25-27 = 011, rule 是 010 → 不匹配**\n\n等等，再看：实际匹配标识：第一条规则 (Link 0) 的前缀是 `11001000 00010111 00010***`，packet 前 27 位是 `11001000 00010111 00010110` (高 27 位的最后 3 位 = 110)。Rule 的最后 3 个 * 是通配，所以前 24 位 + 接下来 3 位 = 110 不约束。**匹配**！\n\n→ **Link 0**.",
  "key_points": [
    "Packet: 11001000.00010111.00010110.10100001",
    "Rule 0 (Link 0): 11001000.00010111.00010*** (/27)",
    "前 24 位匹配 + 高 3 位（位 25-27）= 010 == 010 ✓",
    "**Match!**",
    "→ Link 0"
  ]
},

"lec16:26": {
  "title": "LPM 例 1 — 详细匹配标注",
  "summary": "把匹配过程画出来:\n- 11001000 00010111 **00010***  ******** = rule 0\n- 11001000 00010111 **00010110** 10100001 = packet\n\n前 24 位 11001000 00010111 一致，位 25-27 = 010 一致。后 5 位（包含 4 位通配 + 后 1 位）不约束。\n\n所以 packet 匹配 rule 0，去 **Link 0**.",
  "key_points": [
    "前 24 位 = 11001000.00010111 一致",
    "位 25-27 = 010 == 010 ✓",
    "Rule /27 prefix 完全匹配",
    "→ Link 0"
  ]
},

"lec16:27": {
  "title": "LPM 例 2 — 第二个 packet",
  "summary": "Packet dst = 11001000.00010111.00011000.10101010\n\n比较多个 rules:\n- Rule 0 (00010***): 前 24 位匹配，位 25-27 = 011，rule 是 010 → 不匹配\n- Rule 1 (00011000): 前 24 位匹配，位 25-32 = 00011000 == 00011000 ✓ **匹配** (/32)\n- Rule 2 (00011***): 前 24 位匹配，位 25-27 = 011 == 011 ✓ **匹配** (/27)\n\n**多个 matching → 选 longest prefix**: Rule 1 (/32) > Rule 2 (/27) > otherwise (/0)\n\n→ **Link 1**.",
  "key_points": [
    "Packet: ...00011000.10101010",
    "Rule 1 (/32) 匹配",
    "Rule 2 (/27) 也匹配",
    "**Choose longest**: /32 > /27",
    "→ Link 1"
  ]
},

"lec16:28": {
  "title": "LPM 例 2 — 详细匹配标注",
  "summary": "Packet 11001000.00010111.**00011000**.10101010 完全匹配 Rule 1 (11001000.00010111.00011000.********), Rule 1 是 /32 但实际 /24 (注意 *)。等价于 /24 完全匹配。\n\n实际课件细节: Rule 1 是 'first 24 bits = 11001000.00010111.00011000'，第二个 8 位段是 `00011000`，所以是 /24。Packet 满足。",
  "key_points": [
    "Rule 1 完全匹配 packet (/24)",
    "选 longest prefix → Link 1"
  ]
},

"lec16:29": {
  "title": "Longest Prefix Matching — TCAM + 实际意义",
  "summary": "**Why LPM**: 后面学 addressing 时会发现 LPM 是 IP 寻址自然结构。\n\n**Often performed using ternary content addressable memories (TCAMs)**:\n- Content addressable: present address to TCAM → retrieve address in **one clock cycle**, regardless of table size\n- Cisco Catalyst: ~1M routing table entries in TCAM",
  "key_points": [
    "LPM 在 IP 层级寻址下自然",
    "**TCAM**: ternary content addressable memory",
    "支持 0/1/* 三种值",
    "O(1) lookup with wildcards",
    "Cisco: ~1M entries"
  ],
  "explanation": "**为什么 TCAM**:\n- 普通 RAM 只存 0/1，要查 LPM 必须串行扫描多 entries\n- TCAM 支持通配符 *，并行匹配所有 entries\n- 一个时钟周期完成 lookup, regardless of table size\n\n**缺点**: 贵 + 耗电 + 容量有限。\n\n**容量**: Cisco 高端路由器 ~1M TCAM entries，刚好覆盖 BGP 全表 (~100 万)。\n\n**考点**: 『LPM 为什么 TCAM？』答: 并行匹配带通配符的 entries，O(1)。"
},

"lec16:30": {
  "title": "Switching Fabrics — 概念",
  "summary": "**Switching fabric**: transfer packet from input link to appropriate output link。\n\n**Switching rate**: rate at which packets transfer from inputs to outputs。常 measured as multiple of input/output line rate。**N inputs: switching rate N times line rate desirable**。",
  "key_points": [
    "Fabric 把 input 转给 output",
    "Switching rate ≥ N × line rate 才不堵",
    "三类: memory / bus / interconnection (下页)"
  ]
},

"lec16:31": {
  "title": "Switching Fabrics — 三类",
  "summary": "**Three major types of switching fabrics**:\n\n1. **Memory** (1st gen routers)\n2. **Bus** (shared bus)\n3. **Interconnection network** (Crossbar, Clos)",
  "key_points": [
    "**Memory**: 早期 routers",
    "**Bus**: 共享 bus",
    "**Interconnection**: 现代高端 (Crossbar, Clos)"
  ]
},

"lec16:32": {
  "title": "Switching via Memory",
  "summary": "**First generation routers**: traditional computers with switching under direct control of CPU. Packet copied to system's memory. Speed limited by memory bandwidth (**2 bus crossings per datagram**).",
  "key_points": [
    "1st gen routers (1980s-90s)",
    "Switching by CPU 控制",
    "Packet 过 memory 两次",
    "速度 limited by memory BW",
    "现已淘汰"
  ],
  "explanation": "**为什么 2 次 bus crossings**:\n1. Input port → memory (write)\n2. Memory → output port (read)\n\n每个 packet 进出 memory 都消耗 bus 带宽 → 总带宽减半。\n\n**慢**: 早期 routers throughput 不高，主要瓶颈是 memory bus。"
},

"lec16:33": {
  "title": "Switching via a Bus",
  "summary": "**Datagram from input port memory to output port memory via shared bus**. \n\n**Bus contention**: switching speed limited by bus bandwidth. **32 Gbps bus, Cisco 5600**: sufficient for access routers。",
  "key_points": [
    "共享 bus 连所有 input/output ports",
    "Bus contention 是瓶颈",
    "32 Gbps Cisco 5600 适合 access router",
    "更高速时不够"
  ]
},

"lec16:34": {
  "title": "Switching via Interconnection Network",
  "summary": "**Crossbar, Clos networks, other interconnection nets** initially developed to connect processors in multiprocessor。\n\n**Multistage switch**: n×n switch from multiple stages of smaller switches。\n\n**Exploiting parallelism**:\n(a) Fragment datagram into fixed length cells on entry\n(b) Switch cells through fabric\n(c) Reassemble datagram at exit\n\n例: 3×3 crossbar; 8×8 multistage switch built from smaller switches。",
  "key_points": [
    "Crossbar / Clos networks",
    "Multistage: 大 switch 由小 switch 组成",
    "Fragment datagram → cells → switch → reassemble",
    "高度并行",
    "现代高端 router 用这种"
  ]
},

"lec16:35": {
  "title": "Switching via Interconnection — 多 fabric planes",
  "summary": "**Scaling**: 多个 switching planes 并行。**Speedup, scaleup via parallelism**。\n\n**Cisco CRS router**:\n- 基本单位: **8 switching planes**\n- 每 plane: 3-stage interconnection network\n- **Up to 100s Tbps switching capacity**",
  "key_points": [
    "多个 fabric planes 并行",
    "Cisco CRS: 8 planes × 3-stage",
    "**100s Tbps switching capacity**",
    "顶级 ISP backbone router"
  ]
},

"lec16:36": {
  "title": "Input Port Queuing — HOL Blocking",
  "summary": "**If switch fabric slower than input ports combined → queueing may occur at input queues**. Queueing delay + loss due to input buffer overflow!\n\n**Head-of-the-Line (HOL) blocking**: queued datagram at front of queue prevents others in queue from moving forward。\n\n例: output port contention. 队头 red datagram 等输出，绿和蓝包卡在后面动不了。",
  "key_points": [
    "Fabric 慢 → input 排队",
    "**HOL blocking**: 队头堵后面动不了",
    "Output port contention 导致",
    "下页讲怎么解（VOQ）"
  ],
  "explanation": "**经典例**: input port 队列 [红→outputA, 绿→outputB, 蓝→outputC]。如果 outputA 此时 busy（另一个 input 也想发到 A），红色队头被堵 → 绿和蓝（其实可以同时发到 B 和 C）卡在红后面 → **HOL blocking**。\n\n**解药**: VOQ (Virtual Output Queue) — input port 为每个 output port 分开维护队列。这样不同 output 不互相阻塞。"
},

"lec16:37": {
  "title": "Output Port Queuing",
  "summary": "**Datagram buffer at output port**: switch fabric → buffer → link layer protocol (send) → line termination → R。\n\n**Buffering required when datagrams arrive from fabric faster than link transmission rate**。Drop policy: which datagrams to drop if no free buffers? Scheduling discipline: priority among queued datagrams。",
  "key_points": [
    "Fabric 快于 link rate → output 排队",
    "Buffering 必要",
    "Drop policy 决定丢哪个",
    "Scheduling 决定先发哪个",
    "Priority scheduling 涉及 network neutrality"
  ]
},

"lec16:38": {
  "title": "Output Port Queuing — 第二张图",
  "summary": "图示 packets more from input to output at time t, vs one packet time later。**Buffering when arrival rate via switch exceeds output line speed**。**Queueing (delay) + loss due to output port buffer overflow!**",
  "key_points": [
    "Arrival > output line speed → 排队",
    "Buffer 溢出 → 丢包",
    "Output port 是丢包主要原因之一"
  ]
},

"lec16:39": {
  "title": "Buffer Management",
  "summary": "**Buffer management**:\n\n**Drop policy** — which packet to add/drop when buffers full:\n- **Tail drop**: drop arriving packet\n- **Priority**: drop/remove on priority basis\n\n**Marking** — which packets to mark to signal congestion (**ECN, RED**)",
  "key_points": [
    "Drop policy: tail drop / priority",
    "**Marking**: ECN, RED 提前打标",
    "缓冲区耗尽时的策略"
  ],
  "explanation": "**Tail drop**: 最简单，buffer 满了就丢新来的。\n\n**Priority drop**: 优先丢低优先级 packet (DSCP marking)。\n\n**ECN** (Explicit Congestion Notification): 不丢，给 packet 打 mark → sender 看到后减速 → 避免实际丢包。\n\n**RED** (Random Early Detection): buffer 还没满就开始随机丢，提前给 sender 信号。"
},

"lec16:40": {
  "title": "Packet Scheduling: FCFS",
  "summary": "**Packet scheduling**: deciding which packet to send next on link。\n\nVarieties:\n- **First Come First Served (FCFS)** = FIFO\n- Priority\n- Round Robin\n- Weighted Fair Queueing\n\n**FCFS**: packets transmitted in order of arrival to output port。Also known as First-in-first-out (FIFO)。",
  "key_points": [
    "FCFS = FIFO",
    "Packets 按到达顺序发",
    "最简单",
    "Real world: 银行排队"
  ]
},

"lec16:41": {
  "title": "Scheduling — Priority",
  "summary": "**Priority scheduling**:\n- Arriving traffic classified (by any header field), queued by class\n- Send packet from **highest priority** queue that has buffered packets\n- **FCFS within priority class**",
  "key_points": [
    "Classify by header fields (e.g. DSCP)",
    "**Highest priority first**",
    "FCFS within same priority",
    "Risk: low-priority starve"
  ],
  "explanation": "**Example**: VoIP 流量优先级高 → 总优先于 web 流量。\n\n**Risk**: 高优先级可能 starve 低优先级。需要 admission control 限制高优先级流量。"
},

"lec16:42": {
  "title": "Scheduling — Round Robin (RR)",
  "summary": "**Round Robin (RR) scheduling**:\n- Arriving traffic classified, queued by class\n- Server **cyclically, repeatedly scans class queues**, sending one complete packet from each class (if available) in turn",
  "key_points": [
    "Cyclic scan classes",
    "Each round: one packet per class",
    "Classes 平等",
    "简单 + 公平"
  ]
},

"lec16:43": {
  "title": "Scheduling — Weighted Fair Queueing (WFQ)",
  "summary": "**WFQ**: generalized Round Robin。Each class i has weight w_i, gets weighted amount of service in each cycle:\n\n$$\\text{Class } i \\text{ share} = \\frac{w_i}{\\sum_j w_j}$$\n\n**Minimum bandwidth guarantee** per traffic class.",
  "key_points": [
    "WFQ = RR 的加权版",
    "Class i share = w_i / Σw_j",
    "Min BW guarantee per class",
    "Used in QoS-aware routers"
  ],
  "explanation": "**直觉**: WFQ 是 RR 的泛化 — 每轮服务每个 class 但量不一样大。\n\n**例**: 3 个 class, weights = [1, 2, 3]。每循环 class 1 发 1 packet, class 2 发 2, class 3 发 3。长期 class i 占 w_i/Σ 带宽。\n\n**Min BW 保证**: 只要 class i 有流量，至少拿到 w_i/Σw_j 的带宽。\n\n**考点**: 给 weights 算 share。"
},

"lec16:44": {
  "title": "Sidebar — Network Neutrality 概念",
  "summary": "**What is network neutrality?**\n\n(1) **Technical**: how ISP shares/allocates resources。Packet scheduling, buffer management are mechanisms。\n\n(2) **Social, economic principles**: 保护 free speech, encouraging innovation, competition。\n\n(3) **Enforced legal rules and policies**。\n\nDifferent countries have different 'takes' on network neutrality.",
  "key_points": [
    "Technical: ISP 怎么分配资源",
    "Social: 言论自由 + 创新 + 竞争",
    "Legal: 法规执行",
    "各国 'takes' 不同"
  ]
},

"lec16:45": {
  "title": "Network Neutrality — 2015 FCC Order",
  "summary": "**2015 US FCC Order on Protecting and Promoting an Open Internet**: three 'clear, bright line' rules:\n\n(1) **No blocking** — 'shall not block lawful content, applications, services, or non-harmful devices.'\n\n(2) **No throttling** — 'shall not impair or degrade lawful Internet traffic.'\n\n(3) **No paid prioritization** — 'shall not engage in paid prioritization.'\n\n**ISP: telecommunications or information service?**\n\n- **Title II** (telecommunications): 'common carrier' duties, reasonable rates, non-discrimination, **regulated**\n- **Title I** (information services): no common carrier duties, **not regulated**",
  "key_points": [
    "FCC 2015 三大原则:",
    "① No blocking",
    "② No throttling",
    "③ No paid prioritization",
    "**Title II** vs **Title I** 分类决定监管",
    "ISP 想被 Title I 不受约束"
  ],
  "explanation": "**Network Neutrality 的政治背景**：\n- ISP（Comcast、AT&T、Verizon）想根据流量收费（如『付钱给我才能高速访问 Netflix』）\n- 用户和内容提供商（Netflix、Google）反对\n- FCC 监管来回切换：2015 严管（Title II）→ 2017 松绑（Title I）→ 2024 再严\n\n**Title II vs Title I**:\n- **Title II 电信服务**: 像电话公司一样监管。必须『公平、无歧视』。FCC 可以严格管价格、行为。\n- **Title I 信息服务**: 像 web 公司，少监管。ISP 可以自由定价 / 限速。\n\n**考点**: 『FCC 2015 三大原则？』必背 no block / no throttle / no paid prioritization。"
},

}

def main():
    data = json.loads(DETAIL.read_text())
    overwritten = 0
    new = 0
    for key, val in NEW.items():
        if key in data:
            old = data[key]
            if 'important' in old:
                val['important'] = old['important']
            data[key] = val
            overwritten += 1
        else:
            data[key] = val
            new += 1
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"lec16 rewrite: overwrote {overwritten}, added {new}")

if __name__ == "__main__":
    main()
