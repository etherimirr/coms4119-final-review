#!/usr/bin/env python3
"""Full per-page rewrite for lec18 (IPv6 + Control Plane + Dijkstra + DV, 54 pages)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec18:1": {
  "title": "IPv6 — 动机",
  "summary": "IPv6 主要动机：32-bit IPv4 地址空间快用完。额外动机：40 byte 固定 header 加速 router 处理，加 flow label 给『flow』提供网络层处理依据。",
  "key_points": [
    "初始动机：32-bit IPv4 地址空间已分完",
    "次要动机：加速 forwarding（40 byte 固定 header）",
    "次要动机：让 network layer 能区分『flow』（flow label）"
  ],
  "explanation": "**IPv4 用完的来由**：32 位 = 43 亿地址，按理够用。但早期分配低效（IBM 一家拿了 1600 万），加上移动设备 + IoT 爆炸，2011 年 IANA 把最后一段 IPv4 给了 RR。\n\n**Header 简化加速**：IPv4 header 是变长（20-60 byte），路由器要根据 hlen 解析。IPv6 固定 40 byte，硬件实现更简单更快。\n\n**Flow label**：让 router 能根据 flow（一系列相关 packets）做特殊处理（如 QoS）。"
},

"lec18:2": {
  "title": "IPv6 Datagram 格式",
  "summary": "32 bit 行宽。字段：Ver(4)、Priority(8)、Flow Label(20)、Payload Length(16)、Next Header(8)、Hop Limit(8)，然后 128 bit Src + 128 bit Dst。**没有** header checksum、fragmentation 字段、options（用 next-header 链替代）。",
  "key_points": [
    "**Priority**: 区分流之间的优先级",
    "**Flow Label**: 标识同一 'flow' 的 packets（语义未完全定）",
    "**128-bit src/dst**（vs IPv4 的 32-bit）",
    "**Next Header**: 替代 IPv4 options，链式 header",
    "**Hop Limit**: 替代 IPv4 TTL",
    "**Payload Length**: 替代 IPv4 total length 中 header 部分",
    "**没有 checksum**（让 L2 CRC + L4 checksum 兜底）",
    "**没有 fragmentation**（端到端处理，end-to-end principle）"
  ],
  "explanation": "**vs IPv4 关键变化**：\n\n| | IPv4 | IPv6 |\n|---|---|---|\n| 地址 | 32 b | 128 b |\n| Header | 20-60 B 变长 | **40 B 固定** |\n| Header checksum | 有 | **无** |\n| Fragmentation by router | 是 | **否（仅端可分片）** |\n| Options | header 内 | next-header 链 |\n| Flow label | 无 | 有 |\n\n**Next Header 链**：取代 IPv4 options。例如 `Next Header=6` 表示后面是 TCP；如果有 IPsec 扩展头，链式串联。\n\n**Hop Limit = TTL**：名字变了但语义一样（每跳 −1，到 0 丢）。\n\n**为什么禁止路由器分片**：让中间路由器更简单。Sender 用 Path MTU Discovery 主动探测路径 MTU，自己负责分小。"
},

"lec18:3": {
  "title": "IPv6 设计哲学",
  "summary": "三大原则：(1) 不处理问题，留给端 — 去除 fragmentation, checksum；(2) 简化处理 — 新 options 机制（next-header），去掉 hlen；(3) 通用 flow label — 不绑特定语义，提供灵活性。引用 1984 年 end-to-end argument 经典论文。",
  "key_points": [
    "**Don't deal with problems: leave to ends** — 去除 fragmentation, checksum",
    "**Simplify handling** — next-header 机制，去掉 header length",
    "**Provide general flow label** — 不绑语义",
    "Cite: End-to-End Argument in Systems Design (1984)"
  ],
  "explanation": "**End-to-end argument 简述**：网络中间节点应该保持简单，复杂功能放在端点。例如：可靠交付不能由 router 保证（每跳保证也救不了端到端失败），所以由 TCP 在端处理。\n\nIPv6 直接反映这个原则：\n- Fragmentation：端做（避免中间路由器干太多事）\n- Checksum：端做（TCP/UDP 已经做了，IP 重复浪费）\n- Options：变成可选 next-header 链，path 上不一定每个 router 都解析\n\n**考点**：『为什么 IPv6 去掉 checksum？』答：(1) TCP/UDP 已有；(2) 每跳 TTL 变要重算 checksum，浪费 CPU；(3) end-to-end principle。"
},

"lec18:4": {
  "title": "IPv4 → IPv6 过渡 — Tunneling",
  "summary": "不能让全网一夜换 IPv6（『no flag days』）。现实：v4 和 v6 路由器混合存在。解药：**tunneling** — IPv6 packet 作为 IPv4 packet 的 payload 穿过 v4-only 网段。",
  "key_points": [
    "Cannot upgrade all routers simultaneously (no flag days)",
    "Mixed IPv4 + IPv6 routers coexist",
    "**Tunneling**: IPv6 datagram carried as payload in IPv4 datagram",
    "Tunneling 在 4G/5G 也广泛使用"
  ],
  "explanation": "**类比**：你寄国际包裹给纽约朋友，但本地邮政只到曼哈顿。你把包裹装进一个曼哈顿的『中转包裹』寄到中转站，中转员工不知道内里是什么，照常按曼哈顿地址投递。\n\n**网络对应**：\n- 你（A，IPv6 router）想把 v6 packet 发给 F（也是 v6）\n- 中间经过 C、D（只懂 v4）\n- A 把整个 v6 packet 塞进一个 v4 packet（payload），src/dst 写 v4 router 的地址\n- C、D 看到 v4 packet 照常路由\n- 到达终点附近的 v4/v6 双栈 router 后，剥掉外层 v4，里面 v6 packet 继续传"
},

"lec18:5": {
  "title": "Tunneling 详图 (1) — Ethernet 直连两个 IPv6 router",
  "summary": "两个 IPv6 router (A 和 B) 通过 Ethernet 直连。Frame 链路层载 IPv6 datagram。正常情况。",
  "key_points": [
    "A 和 B 都是 v6 router",
    "Ethernet frame 承载 IPv6 datagram 作为 payload",
    "这是『正常』场景，没有 tunneling"
  ],
  "explanation": "**对照组**：这页给出『没有 tunneling 时的正常情况』，作为下一页 tunneling 的对照。\n\n图示：A → IPv6 datagram → B，封装在 Ethernet frame 里。没有任何特殊处理。"
},

"lec18:6": {
  "title": "Tunneling 详图 (2) — IPv4 网络间穿越",
  "summary": "现实场景：A 和 B 都是 IPv6 router，但中间是 IPv4-only 网络（C, D）。A 把 v6 packet 塞进 v4 packet，C, D 当 v4 包处理，B 端剥掉外层 v4 还原 v6 packet。",
  "key_points": [
    "A 是 v6 router，B 是 v6 router",
    "中间 C, D 是 v4-only",
    "A → 包装 v6 包进 v4 包 → 发给 B",
    "C, D 只看 v4 header",
    "B 拆掉 v4 header，恢复 v6 packet"
  ],
  "explanation": "**这就是 tunneling**。Tunnel = 一条逻辑链路（A 到 B），但物理上经过 v4 网络。\n\n**A 端封装**：\n```\n[IPv4 hdr: src=A.v4, dst=B.v4]  ← 外层\n[IPv6 hdr: src=A.v6, dst=F.v6]  ← 内层\n[TCP/UDP hdr + data]\n```\n\n**B 端解封**：剥掉外层 IPv4 header → 内层是 v6 packet → 继续按 v6 处理。"
},

"lec18:7": {
  "title": "Tunneling — 逻辑视图 vs 物理视图",
  "summary": "两种视角的对比：逻辑视图 A-B-E-F 全是 IPv6 直连；物理视图 A-B-C-D-E-F，B-E 之间用 IPv4 tunnel 穿越。tunnel 内每跳 IPv6 packet 都包在 IPv4 里。",
  "key_points": [
    "**逻辑视图**: A—B === E—F (B 和 E 直连 IPv6)",
    "**物理视图**: A—B—C—D—E—F (C 和 D 只看 v4)",
    "B → E 段：每个 packet 都是『v6 in v4』",
    "Header 嵌套：外层 v4，内层 v6，最内是 TCP/UDP"
  ],
  "explanation": "**Header 嵌套**：\n- A → B 段：纯 IPv6 packet\n- B → E 段（tunnel 内）：IPv4 header 包 IPv6 packet 包 TCP/UDP + data\n- E → F 段：纯 IPv6 packet\n\n**关键 src/dst**（v6 部分）：\n- Source 写 A 的 v6 地址（end-to-end，不变）\n- Destination 写 F 的 v6 地址（end-to-end）\n\n**关键 src/dst**（v4 外层，仅在 tunnel 内）：\n- Source 写 B 的 v4 地址\n- Destination 写 E 的 v4 地址\n\n**考点**：『画 tunnel 中 packet 的 header 结构』。"
},

"lec18:8": {
  "title": "IPv6 采用率（早期 2026）",
  "summary": "Google 统计：~46-49% 的客户端通过 IPv6 访问 Google 服务（2026 初）。NIST: 43% 美国政府域名支持 IPv6。",
  "key_points": [
    "Google 客户端 IPv6 比例：~46-49% (2026)",
    "NIST: 43% 美政府域名 IPv6 capable (2026)",
    "URL: google.com/intl/en/ipv6/statistics.html"
  ],
  "explanation": "**采用率慢的原因**：NAT 缓解了 IPv4 短缺；改协议代价大；ISP 设备升级慢；老应用兼容性。\n\n但 Google 数据显示已经接近一半，移动网络（4G/5G）推动比较快。"
},

"lec18:9": {
  "title": "IPv6 采用率（续）— 为什么 25 年了还没全换",
  "summary": "IPv6 标准 1998 年出来，25 年了部署仍不到一半。回顾这 25 年应用层翻天覆地（WWW、社交媒体、流媒体、游戏、远程办公），网络层为什么这么慢？",
  "key_points": [
    "IPv6 标准 1998 年出来",
    "25 年应用层巨变：WWW, 社交, 流媒体, 游戏, telepresence",
    "Network layer 改协议为什么这么慢？"
  ],
  "explanation": "**应用层 vs 网络层**：\n- 应用层：你装新软件就行，几小时部署\n- 网络层：要全网设备 + ISP + OS 配合，几十年\n\n**根本原因**：网络层是 'narrow waist'（一切应用都依赖 IP），改它要全网协调。NAT 给了一个『差不多够用』的妥协方案，反而降低了换 IPv6 的紧迫感。\n\n**例：HTTP 演进**：HTTP/1.0 → 1.1 → 2 → 3，每代只是浏览器和 server 更新就行，几年内大部分用户都在用 HTTP/3 了。\n\n**Network 层困境**：要等 ISP 升级、host OS 升级、router 升级，缺一不可。"
},

"lec18:10": {
  "title": "CSEE4119 — Network Control Plane 章节封面",
  "summary": "进入 Network Layer 控制面章节。Xia Zhou 老师。引用 Kurose-Ross 教材。",
  "key_points": [
    "进入 control plane（路由）章节",
    "前面 lec16-17 是 data plane (forwarding)，现在讲 control plane (routing)",
    "本章重点：LS, DV, OSPF, BGP, SDN, ICMP, SNMP"
  ]
},

"lec18:11": {
  "title": "Network Layer 控制面路线图",
  "summary": "本章议程：(1) 介绍；(2) 路由协议（link state, distance vector）；(3) intra-ISP routing: OSPF；(4) routing among ISPs: BGP；(5) SDN control plane；(6) ICMP；(7) network management (SNMP/NETCONF/YANG)。",
  "key_points": [
    "Routing 算法概念（LS vs DV）",
    "Intra-AS（OSPF）",
    "Inter-AS（BGP）",
    "SDN 控制面",
    "ICMP（错误报告）",
    "Network 管理（SNMP / NETCONF / YANG）"
  ],
  "explanation": "**学习路径**：先建直觉（LS 大嘴 vs DV 悄悄话）→ 详讲算法（Dijkstra, BF）→ 实际协议（OSPF in AS, BGP between ASes）→ 现代替代（SDN）→ 配套机制（ICMP, network mgmt）。"
},

"lec18:12": {
  "title": "Network 层 两功能（复习）",
  "summary": "Forwarding (data plane) + Routing (control plane)。两种控制面结构：(a) per-router control 传统，(b) logically centralized control (SDN)。",
  "key_points": [
    "**Forwarding**: data plane, per-router",
    "**Routing**: control plane, network-wide",
    "Per-router control: 每 router 跑路由算法",
    "Logically centralized: SDN, controller 远程管理"
  ],
  "explanation": "**这是 lec16/17 已讲过的概念**，但重要到 lec18 开头要再强调一次。\n\n**两种 control plane 演进**：\n1. **传统**: 每个 router 独立跑路由算法（OSPF/BGP），自己填 FT\n2. **SDN**: 远程 controller 集中算所有 FT，下发"
},

"lec18:13": {
  "title": "Per-router Control Plane（传统）",
  "summary": "每个 router 单独跑路由算法（OSPF/BGP），算法间互相交换 routing message 协调。Router 内部：控制面跑路由算法（软件 ms 级）+ 数据面查 FT 转发（硬件 ns 级）。",
  "key_points": [
    "每 router 自跑路由算法",
    "Algorithm 间互相 exchange routing messages",
    "Control plane = 软件，ms 级",
    "Data plane = 硬件，ns 级"
  ],
  "explanation": "**经典模型**：路由器是『一体机』，里面同时跑 control + data。CP 软件部分跟同 AS 的其他路由器协调，DP 硬件部分负责快速转发。"
},

"lec18:14": {
  "title": "SDN Control Plane（现代）",
  "summary": "SDN：把 control plane 抽到远程 controller。Controller 全局视图计算所有路由器的 FT，通过 OpenFlow 等协议下发。Router 退化为只执行 FT 的 'dumb pipe'。",
  "key_points": [
    "Remote controller 计算 FT",
    "通过 OpenFlow 下发到 router",
    "Router 退化为 commodity hardware",
    "Northbound API: 应用 → controller",
    "Southbound API: controller → switch"
  ],
  "explanation": "**SDN 卖点**：\n- 中央算法易实现（不用分布式协议复杂度）\n- 全局视图能做更好的优化\n- 硬件商品化降低成本\n- 开放 API 鼓励创新\n\n**详见 lec20**。"
},

"lec18:15": {
  "title": "Control Plane Roadmap（重复目录）",
  "summary": "节点：进入 routing protocols 部分。",
  "key_points": ["章节过渡，无新内容"]
},

"lec18:16": {
  "title": "What is Routing? — Jon Postel 引言",
  "summary": "引用 Jon Postel (RFC 791 作者) 经典：『name 告诉我们要找什么；address 告诉我们在哪；route 告诉我们怎么去。』Routing = 找路径的过程。",
  "key_points": [
    "**Name** = what we seek（语义身份）",
    "**Address** = where it is（位置）",
    "**Route** = how to get there（路径）",
    "Jon Postel, RFC 791 author"
  ],
  "explanation": "**三层概念分清楚**：\n- Name 例：`www.columbia.edu`（人类可读）\n- Address 例：`128.59.65.180`（机器可路由）\n- Route 例：从我家 → ISP → tier-1 → Columbia 网络 → 终端\n\n**DNS** 把 name 翻成 address；**routing** 把 address 翻成 route。"
},

"lec18:17": {
  "title": "Routing Protocols 目标",
  "summary": "Routing protocol 的任务：在路由器网络中，从发送 host 到接收 host 找『好』路径。Path = router 序列。『好』可以是 least cost / fastest / least congested。Routing 是 networking 经典挑战之一。",
  "key_points": [
    "Goal: find 'good' paths from src host to dst host",
    "Path = sequence of routers",
    "'Good' = least cost, fastest, least congested",
    "Routing 是 networking 'top-10' 经典挑战"
  ],
  "explanation": "**Cost 可以是任意 admin 想优化的指标**：\n- 跳数（每条边 cost=1）\n- 链路延迟（ms）\n- 链路带宽倒数\n- 经济成本（跨大西洋链路贵）\n- 拥塞水平（动态）\n\n**注意**：cost 是 admin 定义的，不是 'objective'。不同 AS 用不同 cost。"
},

"lec18:18": {
  "title": "Graph Abstraction — 节点、边、cost",
  "summary": "把网络抽象为图 G=(N,E)。N = router 集合，E = 链路集合。c(a,b) = a 到 b 直连的代价；不直连为 ∞。例图：u-v-w-x-y-z 6 节点。",
  "key_points": [
    "G = (N, E) 图",
    "N = router 集合",
    "E = 链路集合",
    "c(a, b) = a 到 b 直连代价；不直连为 ∞",
    "Cost 由 network operator 定义"
  ],
  "explanation": "**例图**（lec18 用的标准例）：\n```\n      5\n   v ──── w  \n  /│    /│\\\n 2│ 3  / │ 5\n  │  /  1│\n  u ────  z\n  │\\    │\n  1│ 2  │ 2\n  │  \\  │\n  x ─── y\n     1\n```\n邻接矩阵：c(u,v)=2, c(u,x)=1, c(v,w)=3, c(v,x)=2, c(w,x)=3, c(w,y)=1, c(w,z)=5, c(x,y)=1, c(y,z)=2\n\n**重要假设**：cost 非负（否则 Dijkstra 不工作）。"
},

"lec18:19": {
  "title": "两种路由方法论 — Big Mouth vs Whisper",
  "summary": "(1) **Big Mouth (Link State)**: 把自己知道的 link state 广播给所有 node → 每 node 有全局视图 → 算最短路径。(2) **Whisper (Distance Vector)**: 只跟邻居说自己的 'distance to others' → 每 node 局部视角 → 根据邻居更新自己。",
  "key_points": [
    "**LS (Big mouth)**: broadcast 全网，全局视图，每 node 自己算",
    "**DV (Whisper)**: 只跟邻居说，局部视图，渐进收敛"
  ],
  "explanation": "**记忆抓手**：\n- LS = 大嘴巴，把自己直连的链路状态广播给所有人 → 每个 node 拥有完整 graph → 自己跑 Dijkstra 算 shortest path\n- DV = 悄悄话，只跟邻居说 'I think I can reach X at distance D' → 邻居根据邻居们的发言更新自己的估计 → 迭代收敛\n\n**典型协议**：\n- LS: OSPF, IS-IS\n- DV: RIP（已淘汰），BGP（path-vector，DV 变种）"
},

"lec18:20": {
  "title": "路由算法分类 — 4 个维度",
  "summary": "两条独立维度：(1) 全局 (LS) vs 分布 (DV)；(2) 静态 (慢变) vs 动态 (响应快)。LS 是全局集中，DV 是分布迭代。Static = 拓扑变得慢；Dynamic = 周期更新或事件驱动。",
  "key_points": [
    "**Global**: 所有 router 有 complete topology + link cost info → LS",
    "**Decentralized**: 迭代，跟邻居换信息 → DV",
    "**Static**: routes 变得慢",
    "**Dynamic**: 周期 / 事件驱动更新"
  ],
  "explanation": "现代 Internet 路由几乎都是 dynamic（链路坏了能很快切到备份）。Static 路由偶尔在企业内部某些固定段使用。"
},

"lec18:21": {
  "title": "Control Plane Roadmap — 进入 LS 部分",
  "summary": "目录过渡，下面正式进入 link state routing 详讲。",
  "key_points": ["章节过渡"]
},

"lec18:22": {
  "title": "Link State Routing — Step 1: 本地链路状态",
  "summary": "每个 node 先建立自己的 local link state = 我直连哪些邻居 + 各 link 的代价。例：N1 列出 (N1,N2), (N1,N4), (N1,N5)。",
  "key_points": [
    "每个 node 先建本地 link state",
    "Link state = 该 node 直连的邻居 + 各 link cost",
    "这是 LS 算法第一步，纯本地，不广播"
  ],
  "explanation": "**类比**：你先列出你自己直接认识的朋友 + 关系深度。"
},

"lec18:23": {
  "title": "Link State Routing — Step 2: Flooding",
  "summary": "每个 node 把自己的 local link state **flood** 给整个网络（其他 router 收到后继续转发给邻居）。最终每个 node 都收到所有 link states。",
  "key_points": [
    "Node flood 自己的 link state",
    "邻居收到后继续 forward（除入端口）",
    "用 sequence # + age 防重复",
    "最终所有 node 都有所有 link states"
  ],
  "explanation": "**Flooding 实现细节**：\n- LSA (Link State Advertisement) 带 sequence #\n- Node 收到 LSA：如果是新的（seq 更大）→ 接受 + 转发；否则丢\n- 防止 broadcast storm + 旧 LSA 反复回灌\n\n**复杂度**：O(n²) — 每个 node 的 LSA 都要 flood 到全网 (n 个节点)，n 个 node × O(n) flooding = O(n²)。"
},

"lec18:24": {
  "title": "LS — Step 3, 4: 全网拓扑 + Dijkstra",
  "summary": "每个 node 收到所有 link states 后，组装出完整 graph → 跑 Dijkstra 算到所有其他 node 的最短路径 → 填本地 FT。",
  "key_points": [
    "Step 3: 每 node 学到 entire network topology",
    "Step 4: 跑 Dijkstra 算最短路径",
    "结果：每 node 的 FT = 到所有 dst 的下一跳"
  ],
  "explanation": "**所有 node 看到的 graph 应该是一致的**（前提：LSA 没丢/没错）。所以每 node 跑 Dijkstra 得到的结果一致，路由就连贯。\n\n**与中央算法的区别**：虽然每 node 自己算，但因为输入一致，结果一致 — 等价于一个集中算法分布执行。"
},

"lec18:25": {
  "title": "Dijkstra 算法 — 概念 + 符号",
  "summary": "集中式但每 node 自己跑（输入是 link state）。计算单 source 到所有其他 node 的最短路径。符号：N' = 已知最优代价的节点集；D(v) = 当前估算 src 到 v 的代价；p(v) = src 到 v 路径上 v 的前驱。",
  "key_points": [
    "**N'**: 已知最优代价的节点集合",
    "**D(v)**: 当前估计的 src 到 v 的最小代价",
    "**p(v)**: 路径上 v 的前驱（用于回溯路径）",
    "**c(x,y)**: x 直连到 y 的代价（不直连 = ∞）"
  ],
  "explanation": "**Dijkstra 的核心数据结构**：\n- N': 集合，已确定最优代价的 node\n- D(v): 数组（每 v 一项），当前估算的从 src 到 v 的最优代价\n- p(v): 数组（每 v 一项），最优路径中 v 的前驱（反推路径用）\n\n**N' 增长是单调的**：一旦 node 加入 N'，到它的最短距离就确定了。"
},

"lec18:26": {
  "title": "Dijkstra 算法 — 完整伪代码",
  "summary": "伪代码：Init N'={u}, 对所有 v 邻居 D(v)=c(u,v) 否则 ∞。Loop: 取 N' 外 D 最小的 w 加入 N'，relax w 的邻居 → D(v)=min(D(v), D(w)+c(w,v))。直到所有 node 在 N'。",
  "key_points": [
    "Init: N' = {u}; 对每个 v: D(v) = c(u,v) if direct else ∞",
    "Loop until all nodes in N':",
    "  ① find w not in N' s.t. D(w) is min",
    "  ② add w to N'",
    "  ③ for each v adjacent to w, v not in N':",
    "     D(v) = min(D(v), D(w) + c(w,v))"
  ],
  "explanation": "**逐字解读**：\n\n1. **初始化**：自己 u 加入 N'；对每个其他 node v，如果直连则 D(v)=cost，否则 ∞\n2. **每一轮**：\n   - 找 N' 外距离最小的 w（greedy choice）\n   - 把 w 加入 N'\n   - 更新 w 的所有邻居：新路径『u → w → v』可能比『现有 D(v)』更短\n\n**关键不变量**：每一轮选的 w 一定是最短距离已经确定。原因：D(w) 是 N' 外最小，从 N' 内出发到 w 的任何路径都至少经过另一个 N' 外的中间点 z，但 D(z) ≥ D(w)（z 也在 N' 外，w 是 min），所以经 z 到 w 不可能更短。\n\n**复杂度**：n 轮，每轮线性找 min + 线性 relax → O(n²)。Heap 实现 O(n log n + m log n)。\n\n**消息复杂度**：每 router flood 一次 LSA，O(n) 链路传播，n 个 router → O(n²)。"
},

"lec18:27": {
  "title": "Dijkstra 例 — Step 0 (Init)",
  "summary": "Source = u。Init: N'={u}, D(v)=2, D(w)=5, D(x)=1, D(y)=∞, D(z)=∞。",
  "key_points": [
    "N' = {u} （只有 u 自己）",
    "D(v) = 2 (u-v 直连)",
    "D(w) = 5 (u-w 直连)",
    "D(x) = 1 (u-x 直连)",
    "D(y) = ∞ (u 不直连 y)",
    "D(z) = ∞ (u 不直连 z)"
  ],
  "explanation": "**初始表**（看图）：\n```\nStep  N'    D(v)  D(w)  D(x)  D(y)  D(z)\n 0    u     2     5     1     ∞     ∞\n```\n直接看图，u 直连 v(2), w(5), x(1)。y, z 不直连，所以 ∞。"
},

"lec18:28": {
  "title": "Dijkstra 例 — Step 1: 选 x",
  "summary": "Loop 第一轮。N' 外的 D 最小：D(v)=2, D(w)=5, D(x)=1, D(y)=∞, D(z)=∞ → x 最小 (1)。加入 N' = {u, x}。",
  "key_points": [
    "找 N' 外 D 最小：x (D=1) 最小",
    "Add x to N' → N' = {u, x}",
    "下一步 relax x 的邻居"
  ],
  "explanation": "**Greedy 选择**：每轮选 N' 外距离最小的，加进来。这一步选 x。"
},

"lec18:29": {
  "title": "Dijkstra 例 — Step 1 (cont.): relax x 的邻居",
  "summary": "x 的邻居：v(2), w(3), y(1)。对每个邻居 v 不在 N'：D(v) = min(D(v), D(x) + c(x,v))。结果：D(v)=min(2, 1+2)=2 不变；D(w)=min(5, 1+3)=4 更新；D(y)=min(∞, 1+1)=2 更新。",
  "key_points": [
    "x 邻居：v, w, y（不在 N'）",
    "D(v) = min(2, 1+2) = 2 不变",
    "D(w) = min(5, 1+3) = 4 ← 更新（经 x 更短）",
    "D(y) = min(∞, 1+1) = 2 ← 更新"
  ],
  "explanation": "**Relax 操作**：对 x 的每个 N' 外邻居 v，看『u → x → v』是否比『u 当前到 v』更短。\n- v：经 x 是 1+2=3，原有 2 → 不更新\n- w：经 x 是 1+3=4，原有 5 → 更新为 4\n- y：经 x 是 1+1=2，原有 ∞ → 更新为 2\n\n更新后：\n```\nStep  N'    D(v)  D(w)  D(x)  D(y)  D(z)\n 1    ux    2     4     —     2     ∞\n```"
},

"lec18:30": {
  "title": "Dijkstra 例 — Step 2: 选 y",
  "summary": "N' 外 D 最小：D(v)=2, D(w)=4, D(y)=2, D(z)=∞。**v 和 y 并列最小 (=2)**。按某种顺序（如字母序）选其中一个。这页选 y。N' = {u, x, y}。",
  "key_points": [
    "N' 外 min：v 和 y 并列 2",
    "选 y（演示先选 y；如果先选 v 结果一样）",
    "Add y to N' → {u, x, y}"
  ],
  "explanation": "**Tie-breaking**：当多个 node D 值并列最小时，选哪个都不影响最终结果（最短距离不变），只是迭代顺序不同。这页演示先选 y。"
},

"lec18:31": {
  "title": "Dijkstra 例 — Step 2 (cont.): relax y 的邻居",
  "summary": "y 邻居：x（已在 N'，跳过）, w, z。Relax: D(w)=min(4, 2+1)=3 更新；D(z)=min(∞, 2+2)=4 更新。",
  "key_points": [
    "Relax y 的邻居 w 和 z",
    "D(w) = min(4, 2+1) = 3 ← 更新",
    "D(z) = min(∞, 2+2) = 4 ← 更新"
  ],
  "explanation": "**经 y 的新路径**：\n- u → x → y → w = 1+1+1 = 3（比之前的 4 短）\n- u → x → y → z = 1+1+2 = 4（之前是 ∞）\n\n更新后：\n```\nStep  N'    D(v)  D(w)  D(y)  D(z)\n 2    uxy   2     3     —     4\n```"
},

"lec18:32": {
  "title": "Dijkstra 例 — Step 3: 选 v",
  "summary": "N' 外 D 最小：D(v)=2, D(w)=3, D(z)=4。v 最小。加入 N' = {u, x, y, v}。",
  "key_points": [
    "v 是 N' 外 D 最小 (=2)",
    "Add v to N' → {u, x, y, v}"
  ]
},

"lec18:33": {
  "title": "Dijkstra 例 — Step 3 (cont.): relax v 的邻居",
  "summary": "v 邻居：u(已在), x(已在), w(N' 外)。D(w) = min(3, 2+3) = 3 不变（经 v 是 5，比已有 3 长）。",
  "key_points": [
    "v 只有 w 邻居不在 N'",
    "D(w) = min(3, 2+3) = 3 不变"
  ],
  "explanation": "经 v 到 w 是 2+3=5，不如已有的 3（经 x-y-w）短。所以不更新。"
},

"lec18:34": {
  "title": "Dijkstra 例 — Step 4: 选 w",
  "summary": "N' 外：w (3), z (4)。w 最小 (3)。加入 N' = {u, x, y, v, w}。",
  "key_points": [
    "w 最小 (D=3)",
    "Add w → {u, x, y, v, w}"
  ]
},

"lec18:35": {
  "title": "Dijkstra 例 — Step 4 (cont.): relax w 的邻居",
  "summary": "w 邻居：v(已在), x(已在), y(已在), z(N' 外)。D(z) = min(4, 3+5) = 4 不变（经 w 是 8，比已有 4 长）。",
  "key_points": [
    "Only z is outside N'",
    "D(z) = min(4, 3+5) = 4 不变"
  ]
},

"lec18:36": {
  "title": "Dijkstra 例 — Step 5: 选 z + 完成",
  "summary": "最后一个 N' 外节点 z (D=4)。加入 N'。N' = {u, x, y, v, w, z} = 全集。算法终止。",
  "key_points": [
    "z 加入 N'，N' = 全集",
    "算法结束"
  ]
},

"lec18:37": {
  "title": "Dijkstra 例 — 最终完整表",
  "summary": "完整的 5 步表 + 每步 D, p。最终所有 D 都是从 u 出发的最短距离：D(v)=2, D(w)=3, D(x)=1, D(y)=2, D(z)=4。",
  "key_points": [
    "5 步完成",
    "最终距离：D(v)=2, D(w)=3, D(x)=1, D(y)=2, D(z)=4",
    "前驱 p 信息可以反推最短路径"
  ],
  "explanation": "**完整表**（看 PPT）：\n```\nStep  N'      D(v)  D(w)  D(x)  D(y)  D(z)\n 0    u       2,u   5,u   1,u   ∞     ∞\n 1    ux      2,u   4,x   —     2,x   ∞\n 2    uxy     2,u   3,y   —     —     4,y\n 3    uxyv    —     3,y   —     —     4,y\n 4    uxyvw   —     —     —     —     4,y\n 5    uxyvwz  —     —     —     —     —\n```\n\n表中 p(v) 记录最优路径的前驱。"
},

"lec18:38": {
  "title": "Dijkstra — 最短路径树 + Forwarding Table",
  "summary": "结果：(a) 从 u 出发的最短路径树（show 每条边）；(b) u 的 forwarding table — 每个 dst 经哪个第一跳出去。\n- u → v 直连 → next hop (u,v)\n- u → x 直连 → next hop (u,x)\n- u → y/w/z 都经 x → next hop (u,x)",
  "key_points": [
    "**最短路径树**: 从 u 出发，每条边代表一段最优路径",
    "**Forwarding table**: dst → next hop",
    "u 到 v 直连 → next hop = (u, v)",
    "u 到 x 直连 → next hop = (u, x)",
    "u 到 y, w, z 都经 x → next hop = (u, x)"
  ],
  "explanation": "**FT 怎么填**：跟着最短路径树看每个 dst 在树上的第一条边，那就是 next hop。\n\n注意：FT 不存『整条路径』，只存『next hop』。因为每跳的 router 自己再查自己的 FT，逐跳决策。这就是 hop-by-hop forwarding。"
},

"lec18:39": {
  "title": "Dijkstra — 复杂度",
  "summary": "时间：n 轮 × n 比较 = O(n²)；heap 实现 O((n+m) log n)。消息：每 router broadcast 一次 LSA × O(n) 链路 = O(n²) link crossings。",
  "key_points": [
    "Time: n iterations, n comparisons each → O(n²)",
    "Better: heap implementation O(n log n)",
    "Messages: each router broadcasts its LSA, O(n) link crossings per broadcast, n routers → O(n²) total link crossings"
  ],
  "explanation": "**时间 O(n²)**：每轮线性找 D 最小的节点（O(n)），总共 n 轮。可优化为 O(n log n) 用 heap。\n\n**消息 O(n²)**：每个 router 都要 flood 它的 LSA 给所有人。Flooding 一次需要 O(n) 链路传输（每条边走一次）。n 个 router 各 flood 一次 → O(n²) 总链路传输。\n\n**实际优化**：增量更新（只在链路变化时重新 flood），缓存 LSA 列表，等等。"
},

"lec18:40": {
  "title": "Dijkstra — 震荡问题",
  "summary": "当 link cost 跟流量相关时，Dijkstra 可能震荡。例：4 节点环形，cost = 流量。一个轮次大家走 path A → A 拥挤 cost 升 → 大家切到 path B → B 拥挤 → 切回 A → 循环。",
  "key_points": [
    "Link cost depends on traffic → routes oscillate",
    "Example: 4 节点 a-b-c-d-a 环，cost = 流量",
    "Round 1: cost 不均匀 → 所有 traffic 集中某路径",
    "Round 2: 那条变贵 → traffic 切到另一条",
    "Round 3: 反过来 → 震荡"
  ],
  "explanation": "**为什么震荡**：所有 router 同时根据当前 cost 做 greedy choice，会同步切换。\n\n**解药**：\n- 用静态 cost（不跟流量挂钩）\n- 用更平滑的 cost 更新（EWMA 平均）\n- 错开更新时间，避免同步切换\n\n现代 ISP 多用静态 cost，因此震荡很少见。"
},

"lec18:41": {
  "title": "两种方法论 — 进入 Distance Vector",
  "summary": "回顾两种方法论：LS（已讲完）+ DV（接下来讲）。重申『Big mouth' vs 'Whisper'』直觉。",
  "key_points": ["章节过渡，进入 DV"]
},

"lec18:42": {
  "title": "Time for a Game — 课堂游戏",
  "summary": "Xia 老师设计的课堂游戏：『谁带的现金最多？规则：只跟左右邻居说话，3 分钟后我随机叫一个人回答。』模拟 DV 信息传播。",
  "key_points": [
    "规则：只跟邻居说",
    "不能远距离喊话/手势",
    "3 分钟后随机抽人答全网最大现金"
  ],
  "explanation": "**游戏对应 DV**：\n- 每人代表一个 router\n- '现金' = 某个共享的全网最大值\n- 只能跟左右邻居说话 = DV 的局部交换\n- 信息会从产生地向两端扩散 → 类似 DV 收敛\n\n3 分钟后大部分人应该都知道全网最大值。这就是 BF 收敛的直觉。"
},

"lec18:43": {
  "title": "Distance Vector — Bellman-Ford 方程",
  "summary": "DV 核心数学：D_x(y) = min over all neighbors v of [c(x,v) + D_v(y)]。直觉：『我到 y 最短』= '我先到某邻居 v 的代价' + 'v 估计的到 y 的距离'，对所有邻居 v 取 min。",
  "key_points": [
    "**BF equation**: D_x(y) = min_v∈N(x) { c(x,v) + D_v(y) }",
    "min 取自 x 的所有邻居 v",
    "c(x,v) = x 直连 v 的代价",
    "D_v(y) = v 估算到 y 的距离（v 告诉 x 的）"
  ],
  "explanation": "**逐项理解**：\n- 我（x）到 y 的最短距离\n- 等于：在我的所有邻居 v 中找一个『先到 v 再继续』总代价最小的\n- 'c(x,v)' 是固定的（拓扑给的）\n- 'D_v(y)' 是 v 自己估计的到 y 的距离，由 v 告诉我（v 发 DV 给 x）\n\n**例**：邻居 B 说『我到 y 是 5』，c(x,B)=2 → 我经 B 到 y = 2+5=7。邻居 C 说『我到 y 是 4』，c(x,C)=4 → 我经 C 到 y = 4+4=8。我取 min(7, 8) = 7 → D_x(y)=7，存在 DV。\n\n**与 Dijkstra 对比**：Dijkstra 集中算（一个 node 自跑全图）；BF 分布式迭代（每 node 跟邻居换信息）。两者最短距离结果一致（前提：非负权）。\n\n**Final Q4 直接考这个**。"
},

"lec18:44": {
  "title": "Distance Vector Table — 数据结构",
  "summary": "每个 router 维护一个 distance table（矩阵），行=目的 node，列=经哪个邻居。dist_v(x, y) = x 经邻居 v 到 y 的代价。每行取 min 得到 DV（distance vector，发给邻居的）。",
  "key_points": [
    "Distance table：行=目的，列=经哪个邻居",
    "Entry: 经该邻居到该目的的代价",
    "DV = 每行取 min（最优经哪个邻居）",
    "DV 是 sent to neighbors"
  ],
  "explanation": "**例**（A 的视角）：\n```\n           via B  via C\n     B      0     ∞\n     C      ∞     0\n     D      ?     ?\n```\n（数字示意，不是实际值）\n\n**DV 是『每行 min 的结果』**：A 告诉邻居『我到 B = 2, 到 C = 3, 到 D = 4』，但 A 内部还知道这些数字是『经哪个邻居达成的』。\n\n**例**：D_A(B) = min(dist_B(A,B), dist_C(A,B), ...)。"
},

"lec18:45": {
  "title": "Distance Vector — 初始化",
  "summary": "Init: 每 node 只知道直连邻居 + 直连代价。对非直连的目的，所有邻居列都填 ∞。然后每 node 按行 min 形成初始 DV，发给邻居。",
  "key_points": [
    "Init: 只填直连邻居",
    "非直连目的：所有列填 ∞",
    "每 node 按行 min → 初始 DV",
    "发 DV 给邻居"
  ],
  "explanation": "**例**（A 直连 B(5), C(6), D(8)）：\n```\n           via B  via C  via D\n     B      5     ∞     ∞\n     C      ∞     6     ∞\n     D      ∞     ∞     8\n     E      ∞     ∞     ∞    (A 不直连 E，所有都是 ∞)\n```\nA 的初始 DV：B=5, C=6, D=8, E=∞。发给邻居 B、C、D。"
},

"lec18:46": {
  "title": "DV — Init 例（4 节点）",
  "summary": "图示 4 节点 A, B, C, D。A 的初始 distance table 填好。",
  "key_points": [
    "Concrete init example",
    "A directly connected to B(5), C(6)",
    "A's table reflects direct neighbors only"
  ]
},

"lec18:47": {
  "title": "DV — 发送 DV 给邻居",
  "summary": "每 node 把自己当前的 DV（不是整个 table）发给所有邻居。例：A 把 DV = (B=5, C=6, D=∞) 发给 B 和 C。",
  "key_points": [
    "Send DV (not whole table) to all neighbors",
    "DV = 每行的 min",
    "邻居根据收到的 DV 用 BF 公式更新自己"
  ]
},

"lec18:48": {
  "title": "DV — 邻居用 BF 更新自己",
  "summary": "B 收到 A 的 DV (A→B=5, A→C=6, A→D=∞)。B 用 BF 算『B 经 A 到各目的的距离』：B 经 A 到 C = c(B,A) + D_A(C) = 5+6 = 11。B 更新自己 distance table 经 A 的列。",
  "key_points": [
    "B 收到 A 发来的 DV",
    "对每个 dst y，算 dist_B(A, y) = c(B,A) + D_A(y)",
    "更新自己的 distance table 的『经 A』那列",
    "DV 行 min 重算，如有变化，再发给所有邻居"
  ],
  "explanation": "**循环过程**：\n1. B 收到 A 的新 DV\n2. B 重算 distance_table[B, *, via A]\n3. B 重算 DV[B] = 每行 min\n4. 如果 DV 变了，B 把新 DV 发给所有邻居（包括 A）\n5. 邻居收到 → 重复\n\n**收敛**：在静态非负权拓扑下，会在 O(diameter) 轮内收敛。"
},

"lec18:49": {
  "title": "DV — 核心循环",
  "summary": "每节点：等待 (local link cost 变化 / 邻居 DV 消息) → 用 BF 重算 DV → 如果 DV 变了，通知邻居。**迭代、异步、自停**。",
  "key_points": [
    "Wait for local link cost change or neighbor DV msg",
    "Recompute DV using BF",
    "If DV changed → notify neighbors",
    "Iterative, asynchronous, self-stopping"
  ],
  "explanation": "**Self-stopping**: 收敛后无消息流动 — 因为没人 DV 变，没人发新消息。\n\n**Asynchronous**: 不需要全网同步 round；某个 link cost 变就触发局部更新，自然传播。"
},

"lec18:50": {
  "title": "DV Algorithm — 异步、自停（详图）",
  "summary": "图示每个节点的事件驱动循环：(a) 本地 link cost 变化时触发；(b) 邻居 DV 消息到达时触发。Distributed = 每节点只通知自己 DV 变了的邻居；no notification, no action。",
  "key_points": [
    "Event-driven: link change OR neighbor DV",
    "If DV unchanged after recompute → don't notify",
    "Distributed: 只通知必要邻居"
  ]
},

"lec18:51": {
  "title": "DV — Link Cost 变化（好消息传得快）",
  "summary": "拓扑：x-y-z，cost x-y 从 4 变 1。x 和 y 同时检测到，重算 DV 并通知 z。z 的 DV 几轮内更新。例：D_y(x) 从 4 变 1；D_z(x) 经 y 从 5 变 2。",
  "key_points": [
    "x-y cost 从 4 变 1（变小 = 好消息）",
    "x 和 y 立刻检测并更新 DV",
    "通知邻居 z",
    "z 几轮内收敛到正确值"
  ],
  "explanation": "**好消息传得快**：链路变便宜时，每节点立刻发现自己有更短路径，立刻更新 DV 并通知邻居。新值层层传播，几轮（diameter 步）就全网知道。"
},

"lec18:52": {
  "title": "DV — Count-to-Infinity (CTI)",
  "summary": "**坏消息传得慢**。X-Y cost 从 4 变 60。Y 检测到，但 Y 的 DV 还有 'Y 经 Z 到 X = 6' 的旧记录（Z 之前发来的）。Y 选 min(60, 6) = 6（错的！）。Y 告 Z，Z 算自己经 Y 到 X = 1+6=7，又传给 Y，Y 算 1+7=8... 慢慢爬到正确值。",
  "key_points": [
    "Link cost 变贵（坏消息）",
    "Y 用 Z 之前给的 stale 信息 → 错误估计",
    "Y 和 Z 互相用对方 stale 值，每轮 +1",
    "缓慢爬到真实代价（如 60）",
    "RIP 用 16 表示 ∞，避免无限循环"
  ],
  "explanation": "**完整故事**（X-Y-Z 三节点）：\n\nT=0: x-y=4, y-z=1, z 直连 x 不直连。\n- D_y(x) = 4（直连）\n- D_z(x) = 5（经 y）\n\nT=1: x-y 变成 60。Y 检测到。\n- 但 Y 知道『Z 说 Z→X=5』（Z 之前的 DV）\n- Y 算：min(60 直连, 1+5 经 Z) = 6 → DV 错了，发给 Z\n\nT=2: Z 收到『Y→X=6』\n- Z 重算：min(经 Y = 1+6 = 7) = 7 → DV 错了，发给 Y\n\nT=3: Y 收到『Z→X=7』\n- Y 算：min(60, 1+7=8) = 8 → 发给 Z\n\n... 每轮 +1 +1 直到 50+ 才接近真实代价 60。\n\n**RIP 解决**：定义 16 = ∞，所以最多迭代 16 轮就停。\n\n**Poison reverse**（下页）：更好的解。"
},

"lec18:53": {
  "title": "DV — Poison Reverse",
  "summary": "改进：Z 经 Y 到 X，Z 主动告诉 Y『我（Z）到 X = ∞』（撒谎，但有目的）。这样 Y 不会再用 Z 作 fallback，CTI 破解。**只解 2 节点环**，3+ 节点环仍可成环。",
  "key_points": [
    "Rule: if Z routes to X through Y, Z advertises 'Z→X = ∞' to Y",
    "Y 不会用 Z 作 fallback",
    "Solves 2-node loops（如 x-y-z）",
    "Does NOT solve 3+ node loops"
  ],
  "explanation": "**回到上面的例**：\n- Z 经 Y 到 X，Z 告诉 Y 'Z→X = ∞'\n- Y 现在算：min(60 直连, 1+∞ 经 Z) = 60 → 正确收敛\n\n**3+ 节点失败例**：A-B-C-D 4 节点环，D 是目的。如果 A-D 链路坏，可能 A→B→C→D 这条路径还在，但消息在 A、B、C 间互推 stale 值，poison reverse 解不了。\n\n**实际**：RIP 用 split horizon（不告诉邻居走它的路径）+ hop limit 16 来限制 CTI 危害。"
},

"lec18:54": {
  "title": "LS vs DV — 全面对比",
  "summary": "三大维度对比：(1) 消息复杂度 LS O(n²) flooding，DV 邻居间不定；(2) 收敛速度 LS 快但可能震荡，DV 慢且可能 CTI；(3) 错误鲁棒性 LS 错只本地影响，**DV 错全网传染（black-hole）**。",
  "key_points": [
    "**Messages**: LS O(n²) flood; DV neighbor only, varies",
    "**Speed**: LS 快可能震荡; DV 慢，可能 CTI",
    "**Robustness**:",
    "  LS: router 报错 link cost → 本地受影响",
    "  DV: router 报错 path cost → 错误传染全网（'black-holing'）"
  ],
  "explanation": "**完整对比表**（必背）：\n\n|  | LS | DV |\n|---|---|---|\n| 视角 | 全局 | 局部 |\n| 算法 | Dijkstra | Bellman-Ford |\n| 消息 | O(n²) flood | 邻居间 |\n| 收敛 | 快 | 慢、可能 CTI |\n| 震荡 | 可能（流量依赖时）| 较少 |\n| 错误鲁棒 | 本地化（一个 router 报错代价只影响计算）| **全网传染**（一个 router 报错距离，其他 router 受影响）|\n| 例 | OSPF, IS-IS | RIP (废)，BGP 是变种 |\n\n**Black-holing**：DV 下，一个 router 谎报『我到 X 是 1』（其实是 ∞）→ 其他 router 学到『经它 1 跳到 X』→ 大量流量过它 → 它 drop → 流量黑洞。\n\n**LS 错误**：单个 router 错报 link state 只影响计算（它声称的那条链路）；其他 router 在 graph 上少算这条边，结果略不准但不会全网瘫痪。\n\n**为什么 BGP 用 path vector 而非 LS**：inter-AS 时 LS 要求暴露内部拓扑，违反 AS 自治 + 隐私。Path vector 只告诉对方『我能到 X，路径是 [...]』，不暴露内部细节。\n\n**考点**：『LS 和 DV 优缺点？为什么 BGP 不用 LS？』"
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
    print(f"lec18 rewrite: overwrote {overwritten}, added {new}")

if __name__ == "__main__":
    main()
