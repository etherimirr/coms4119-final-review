#!/usr/bin/env python3
"""lec16 全中文重写 + 修正页码对齐（45 页）。

PDF 实际页内容：
  p1-6: ECN + TCP fairness + 论文列表
  p7-9: Network Layer 章节封面 + roadmap
  p10-12: services + 两功能 + DP vs CP
  p13-14: Per-router + SDN CP
  p15-16: Service model 表
  p17: Best-effort 反思
  p18: roadmap (重复)
  p19-20: Router architecture (2 张图)
  p21-22: Input port functions
  p23: Destination-based forwarding
  p24-28: LPM (5 页)
  p29-30: Switching fabrics 概念 + 三类
  p31: Switching via memory
  p32: Switching via bus
  p33-34: Switching via interconnection
  p35: Input port queuing (HOL)
  p36-37: Output port queuing
  p38: Buffer Management
  p39: FCFS
  p40: Priority
  p41: Round Robin
  p42: WFQ
  p43-44: Network Neutrality
  p45: ISP 电信 vs 信息服务
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec16:1": {
  "title": "ECN — 显式拥塞通知（接 lec14 末尾）",
  "summary": "TCP 部署常用『网络辅助』拥塞控制。路由器在 IP 头的 ToS 字段用 **2 个 bit** 标记拥塞。Receiver 通过 ACK 中的 ECE bit 把信号回传给 sender。这是 IP（标 ECN bit）和 TCP（CWR/ECE header bit）双层协作。",
  "key_points": [
    "路由器在 IP ToS 字段用 2 bit 标 congestion",
    "策略由 network operator 决定怎么标",
    "拥塞信号通过 receiver 经 ACK 回传",
    "Receiver 在 ACK 中 ECE bit=1",
    "**IP + TCP 双层协作**",
    "Sender 见 ECE=1 → cwnd 减半，但**没真丢包**"
  ],
  "explanation": "### 为什么要 ECN\n传统 TCP 必须等到路由器 buffer 满 → 丢包 → 重传，才知道拥塞。这浪费：\n1. queue 满了延迟已经很大\n2. 重传消耗带宽\n3. 反应时机晚\n\nECN 让路由器在 queue 长度超过阈值时（还没满）就标记包。Receiver 通过 ACK 把信号回传 sender。Sender 提前减速 → 队列降回稳态。\n\n### IP + TCP 协作\n- **IP 层**：ECN 字段（ToS 低 2 bit），路由器标 `ECN=11` 表示拥塞\n- **TCP 层**：ACK header 的 ECE bit + next packet 的 CWR bit（确认收到 ECE）\n\n### 协商\nECN 双方都要支持才能用。建连时 SYN 的 ECE+CWR 都设 1 表示『我支持 ECN』。\n\n### 考点\n『ECN 是什么？谁参与？为什么有用？』必答 IP+TCP 双层 + 不靠丢包减半。"
},

"lec16:2": {
  "title": "TCP 公平性 — 目标",
  "summary": "**公平性目标**：如果 K 个 TCP session 共享同一个 bottleneck link（带宽 R），每个 session 应该平均拿到 R/K。\n\n图：2 个 TCP connection 共享一个 router 的 capacity R。",
  "key_points": [
    "K 个 TCP 共享 bottleneck R",
    "理想：每个拿 R/K",
    "AIMD 是否能实现？（下一页论证）"
  ],
  "explanation": "**公平性 ≠ 一定平等**。它定义为『在相同条件下平均收敛到等量份额』。下一页用几何论证 AIMD 在理想条件下能做到。"
},

"lec16:3": {
  "title": "TCP 公平吗？— AIMD 几何论证",
  "summary": "**答**：在理想假设下 yes。前提：(1) 相同 RTT；(2) session 数固定；(3) 都长期处于 congestion avoidance。\n\n**论证**：2 个 TCP 共享 R bottleneck。AIMD 在 (x1, x2) 平面上轨迹：加法增（沿 45° 同步往效率线走）+ 乘法减（沿原点缩，比例不变但差距缩 0.5）→ **螺旋收敛到 x1 = x2**。",
  "key_points": [
    "前提 1：相同 RTT",
    "前提 2：session 数不变",
    "前提 3：长期都在 CA（不反复 slow start）",
    "几何：AI 走 45° + MD 沿原点缩 → 收敛到 x1 = x2"
  ],
  "explanation": "### 几何论证细节\n2 个 user，x 轴 = user 1 吞吐，y 轴 = user 2 吞吐。\n\n- **公平线**：x = y\n- **效率线**：x + y = R\n\n**AIMD 轨迹**：\n1. AI：两 user 同时 +Δ → 沿 45° 走 → 触效率线\n2. MD：两 user ×0.5 → 沿原点向下缩\n3. AI：又沿 45° 走\n4. 反复\n\n**关键观察**：\n- AI 不改变 |x − y|（同时加同量）\n- MD 让 |x − y| ×0.5（按比例缩）\n- 所以 |x − y| → 0，即收敛到 x = y\n\n### 为什么只 AIMD 行\n- **AIAD**：加法增 + 加法减都不改差距 → 不收敛公平\n- **MIMD**：乘法增 + 乘法减保持比例不变 → 也不收敛\n- **只有 AIMD**：AI 不改差距 + MD 按比例缩差距 → 唯一收敛到公平\n\n### 考点\n『为什么 AIMD 收敛公平？』必答画 (x1, x2) 坐标系 + AI/MD 轨迹 + 差距收敛。"
},

"lec16:4": {
  "title": "公平性现实 — UDP 和并行 TCP 破坏",
  "summary": "**UDP 的不公平**：多媒体 app 常用 UDP 而不是 TCP，因为不想被 CC 限速。UDP 发送 constant rate，能忍受丢包。\n\n**并行 TCP 的不公平**：浏览器可以开多条并行 TCP。例：链路速率 R，已有 9 条 TCP。新 app 只开 1 条 → 拿 R/10；新 app 开 11 条 → 拿 R/2。\n\n**没有 Internet 警察** 强制公平。",
  "key_points": [
    "**UDP**：不做 CC，多媒体 app 用它",
    "**并行 TCP**：浏览器开多条抢更多",
    "K 条并行 vs 1 条 → 自己拿 K/(K+1) 份额",
    "**没有 Internet 警察**"
  ],
  "explanation": "### UDP 不公平的真实例\n- Skype、Zoom、Netflix 视频流大量用 UDP\n- 不受 TCP CC 限速，可以一直推\n- 跟旁边的 TCP 流一起跑 → UDP 占更多\n\n### 并行 TCP 不公平的真实例\n- Chrome 浏览器对同一 host 默认开 6 条并行 TCP\n- 每条独立跑 AIMD\n- 6 条 + 别人 1 条 = 别人只能拿 1/7\n- 现代 HTTP/2 把多请求 multiplex 到 1 条 TCP，减少这种 abuse\n\n### 考点\n『TCP 公平性在现实中成立吗？』答：不一定。UDP 不做 CC、并行 TCP 抢多份 都破坏公平。"
},

"lec16:5": {
  "title": "TCP — 仍是 active research topic（1）",
  "summary": "TCP CC 仍是热门研究方向。课件给参考 URL：[cpham.perso.univ-pau.fr/TCP/](http://cpham.perso.univ-pau.fr/TCP/)。",
  "key_points": ["参考资料页面"]
},

"lec16:6": {
  "title": "TCP — 仍是 active research topic（2，论文列表）",
  "summary": "近年 TCP CC 相关论文示例：\n- TCP ex Machina: Computer-Generated CC（SIGCOMM 2013）\n- Recursively Cautious CC（NSDI 2014）\n- PCC（NSDI 2015）\n- Principles for Internet Congestion Management（SIGCOMM 2024）\n- CCAnalyzer（SIGCOMM 2024）\n- CClinguist（SIGCOMM 2025）\n- LeoCC：卫星 CC（SIGCOMM 2025）\n\n... 也许还有你未来的论文 :)",
  "key_points": ["TCP CC 学术上仍在快速演进", "鼓励学生看论文"]
},

"lec16:7": {
  "title": "CSEE4119 — 进入 Network Layer Data Plane 章节",
  "summary": "新章节封面：**Network Layer – Data Plane**。Xia Zhou 讲，引用 Kurose-Ross 教材。\n\nNetwork Layer 是 OSI L3，提供端到端 packet 投递。本章先讲 data plane（forwarding，怎么转发），下一章（lec18-19）讲 control plane（routing，路径怎么算）。",
  "key_points": [
    "新章节：Network Layer Data Plane",
    "Data plane = forwarding（单 router，硬件 ns 级）",
    "Control plane = routing（全网，软件 ms 级）",
    "本章只讲 data plane"
  ]
},

"lec16:8": {
  "title": "Move on to Network Layer — 协议栈定位",
  "summary": "协议栈进入 L3：\n```\nL7 应用层 (HTTP, FTP, DASH, DNS)\nL4 传输层 (TCP, UDP)\nL3 网络层 (IP)              ← 这里\nL2 数据链路层 (Ethernet, 802.11, PPP)\nL1 物理层 (光纤, 铜线, 无线, PSTN)\n```",
  "key_points": [
    "Network layer = L3",
    "**唯一协议：IP**",
    "下面 L2：Ethernet / 802.11 / PPP",
    "上面 L4：TCP / UDP"
  ]
},

"lec16:9": {
  "title": "Network Layer Data Plane — 子章节路线图",
  "summary": "本章议程：\n1. Network layer overview（DP + CP）\n2. **What's inside a router** — input ports, switching fabric, output ports, buffer management, scheduling\n3. **IP**：datagram 格式、地址、NAT、IPv6\n4. **Generalized forwarding, SDN**\n5. **Middleboxes**",
  "key_points": [
    "Network layer overview",
    "Router 内部架构",
    "IP 协议",
    "Generalized forwarding + SDN",
    "Middleboxes"
  ]
},

"lec16:10": {
  "title": "Network 层服务和协议",
  "summary": "Transport segment 从 sender 送到 receiver：\n- **Sender 端**：encapsulate segments 进 datagram，传给链路层\n- **Receiver 端**：deliver segments 给传输层\n- **每台 Internet 设备都跑 IP 层**（hosts + routers）\n- **Router**：检查所有过它的 IP datagram 的 header；把 datagram 从 input port 移到 output port 沿端到端路径前进",
  "key_points": [
    "Sender：封装 segment → datagram",
    "Receiver：解封 datagram → 上层",
    "每个 Internet 设备都跑 IP",
    "Router：看 header，input port → output port"
  ]
},

"lec16:11": {
  "title": "两个核心 network 层功能 — Forwarding vs Routing ⭐",
  "summary": "**Forwarding**（数据面）：把 packet 从 router 的 input link 移到合适的 output link。\n**Routing**（控制面）：决定 packet 从 source 到 destination 的路径。\n\n**旅行类比**：forwarding = 通过单个交叉路口；routing = 出发前规划整段路线。",
  "key_points": [
    "**Forwarding**：单 router 内，input port → output port",
    "**Routing**：全网，source → dest 路径决策",
    "类比：forwarding = 过路口；routing = 规划行程",
    "Routing 算法决定 forwarding table 的内容"
  ],
  "explanation": "### 这是 network layer 最核心的概念分离\n\n**Forwarding（数据面）**：\n- 时间尺度：ns 级硬件\n- 范围：单个 router 内\n- 输入：packet header\n- 输出：哪个 output port\n\n**Routing（控制面）**：\n- 时间尺度：ms 级软件\n- 范围：全网\n- 输入：网络拓扑 + 链路代价\n- 输出：每 router 的 forwarding table\n\n**两者协作**：routing 算出 table → forwarding 用 table 转发。\n\n### 考点\n『Forwarding vs Routing 区别？』必答两者层级 + 时间尺度 + 范围。"
},

"lec16:12": {
  "title": "Data Plane vs Control Plane — 两种 CP 结构 ⭐",
  "summary": "**Data plane**：本地，per-router 功能；决定 input port 到达的 datagram 怎么转到 output port（基于 header 字段值）。\n\n**Control plane**：网络级 logic；决定 datagram 怎么在 routers 间路由（source → destination 全程）。\n\n**两种 control plane 方法**：\n1. **传统 routing 算法**：跑在每个 router 里\n2. **SDN（软件定义网络）**：跑在（远程）server 上",
  "key_points": [
    "**Data plane**：per-router，基于 header",
    "**Control plane**：网络级 logic",
    "**方法 1（传统）**：每 router 自己跑路由算法",
    "**方法 2（SDN）**：远程 server 集中算",
    "两种方法都给 data plane 提供 FT"
  ],
  "explanation": "### 核心区别（再次强调）\n\n| | Data Plane | Control Plane |\n|---|---|---|\n| 范围 | 单 router | 全网 |\n| 时间 | ns（硬件） | ms（软件） |\n| 内容 | 用 FT 转发 | 算 FT |\n| 谁执行 | router 硬件 | router 软件 / SDN controller |\n\n### 两种 CP 模式\n\n**模式 1 — 传统**：每 router 跑自己的路由算法（OSPF/BGP），算法之间互相通信，分布式协调。\n\n**模式 2 — SDN**：远程 controller 集中算，下发到所有 router 执行。\n\n### SDN 的取舍\n- 优势：易管理 + 易编程 + 全局优化\n- 劣势：单点风险（实际分布式 controller 缓解）\n\n### 考点（用户特别强调的概念页）\n必答 DP vs CP 区别 + 两种 CP 结构。"
},

"lec16:13": {
  "title": "Per-router Control Plane（传统模式）",
  "summary": "**传统模式**：每个 router 里都有独立的 routing algorithm 组件，它们在 control plane 互相通信、协调。\n\n图示：每个 router 里 control plane（routing algorithm，软件）和 data plane（local forwarding table，硬件）。",
  "key_points": [
    "传统 router 内部：routing algorithm + local FT",
    "Algorithms 之间互相通信",
    "Software (CP) + hardware (DP)",
    "经典分布式模式"
  ]
},

"lec16:14": {
  "title": "Software-Defined Networking（SDN）Control Plane（新模式）",
  "summary": "**SDN 模式**：远程 controller 计算并安装所有 router 的 forwarding table。Routers/switches 只执行 FT，不自己算路由。\n\n图：Remote Controller → 控制所有 router 的 CA（Control Agent）。",
  "key_points": [
    "Remote controller 全局视图",
    "Controller 算 FT 然后下发",
    "Routers 退化为 'dumb pipe'（只跑 DP）",
    "详见 lec20"
  ]
},

"lec16:15": {
  "title": "Network 层服务模型 — 表",
  "summary": "**对比不同网络架构的 QoS 保证**：\n\n| 架构 | 服务模型 | 带宽 | 丢包 | 顺序 | 时序 |\n|---|---|---|---|---|---|\n| **Internet** | best effort | 无 | 不保 | 不保 | 不保 |\n| **ATM** | Constant Bit Rate | 恒定 | 保 | 保 | 保 |\n| **ATM** | Available Bit Rate | 保证最小 | 不保 | 保 | 不保 |\n| **Internet** | IntServ Guaranteed (RFC 1633) | 保 | 保 | 保 | 保 |\n| **Internet** | DiffServ (RFC 2475) | 可能 | 可能 | 可能 | 不保 |",
  "key_points": [
    "**Internet best-effort**：什么都不保证",
    "**ATM CBR**：固定速率",
    "**ATM ABR**：保证最小带宽",
    "**IntServ**：完整 QoS 保证",
    "**DiffServ**：分类 QoS（标记 packet）"
  ],
  "explanation": "### Internet best-effort 的含义\n- 不保证 packet 一定到达\n- 不保证带宽\n- 不保证顺序\n- 不保证延迟\n\n**这就是 Internet 的本质 service model**。\n\n### ATM（Asynchronous Transfer Mode）\n1990 年代的替代方案，提供 QoS 保证。复杂，最终没赢过 IP + best-effort。\n\n### IntServ vs DiffServ\n- **IntServ**：per-flow 资源预留。复杂，每 router 要维护每 flow 的状态，难扩展。\n- **DiffServ**：类别化 QoS（packet 打 tag），扩展性好，部分采用。"
},

"lec16:16": {
  "title": "Network 层服务模型 — 完整表（复习）",
  "summary": "同上一页，把 5 种服务模型的 QoS 保证完整列出。",
  "key_points": ["重复表 — 5 种 service model 对比"]
},

"lec16:17": {
  "title": "Best-Effort 服务的反思",
  "summary": "**为什么 Internet 选 best-effort**：\n\n1. **Simplicity of mechanism**：简单 → 广泛部署、广泛采用\n2. **为什么 packet-switching**：bursty 流量不浪费 + 同链路多路复用\n3. **为什么 best-effort**：简单（无需 BW 预留）+ 容易在故障下生存\n\n**结论**：It's hard to argue with success of best-effort service model.",
  "key_points": [
    "Simplicity → 广泛部署",
    "Packet-switching：bursty 高效 + 多路复用",
    "Best-effort：简单 + 容错",
    "事实证明它成功了"
  ],
  "explanation": "### 核心 wisdom\n不要为 99% 用例不存在的功能（如严格 QoS）增加复杂度。Internet 的成功在于『差不多够用，但极简、极开放、极可扩展』。\n\n### 对比 ATM\nATM 当年承诺更好的 QoS，但复杂度高，最终败给 IP + best-effort。\n\n### End-to-end argument 应用\n复杂功能（如可靠传输 = TCP）放到端，不放进网络中间。这就让网络中间能保持简单。"
},

"lec16:18": {
  "title": "Network Layer Data Plane Roadmap — 进入 router 内部",
  "summary": "目录回顾：接下来讲 'What's inside a router' — input ports, switching fabric, output ports, buffer management, scheduling。",
  "key_points": ["进入 router 架构详讲"]
},

"lec16:19": {
  "title": "Router 架构概览（high-level）",
  "summary": "**Generic router 高层视图**：\n\n- **Routing processor**：routing + management，**控制面**（软件，ms 时间尺度）\n- **High-speed switching fabric**：连 input ports 和 output ports\n- **Forwarding data plane**：硬件，**ns 时间尺度**\n- **Router input ports** ← packet 进\n- **Router output ports** → packet 出",
  "key_points": [
    "Routing processor（软件，ms）：CP",
    "Switching fabric + ports（硬件，ns）：DP",
    "Input ports + Output ports",
    "两个时间尺度：ms vs ns"
  ]
},

"lec16:20": {
  "title": "Router 架构类比（火车站）",
  "summary": "Analogy 视图：\n- **Station manager** = routing & management（控制面）\n- **Roundabout（转盘）** = forwarding data plane\n- **Entry stations** → **roundabout** → **exit roads**",
  "key_points": [
    "Manager（CP）= 火车站长（规划调度）",
    "Roundabout（DP）= 转盘（实际通过）",
    "类比帮助理解 CP/DP 分离"
  ]
},

"lec16:21": {
  "title": "Input Port 功能（1）— Lookup + Forwarding",
  "summary": "**Input port 三阶段**：\n\n1. **Line termination + 物理层**：bit-level 接收\n2. **链路层协议**（receive）：例如 Ethernet\n3. **Lookup / forwarding / queueing**：去中心化 switching\n   - **Match + action**：FT 存在 input port memory 里\n   - 用 header 字段值 lookup output port\n   - **目标**：line-speed 处理\n   - Input port queueing：如果 datagram 到达比 fabric 转发快",
  "key_points": [
    "Input port 三阶段：物理 → 链路 → lookup",
    "Lookup 在 input port memory（FT cache）",
    "目标：line speed",
    "Decentralized switching（每 port 自己查表）",
    "**Match + action** 抽象"
  ],
  "explanation": "### Decentralized switching\n每个 input port 有自己的 FT 副本，独立查表。避免单点瓶颈。\n\n### Line speed 要求\n10 Gbps Ethernet 上 packet 间隔几十 ns，input port 必须在这个时间内完成 lookup → output port 决策。所以硬件实现（ASIC/TCAM）。"
},

"lec16:22": {
  "title": "Input Port 功能（2）— Destination vs Generalized Forwarding",
  "summary": "两种 forwarding 模式：\n\n1. **Destination-based forwarding**（传统）：仅基于 **destination IP address** 转发\n2. **Generalized forwarding**：基于 **任意 header 字段集合**（L2/L3/L4 多字段）转发",
  "key_points": [
    "Destination-based：只看 dst IP",
    "Generalized：任意 header 字段（SDN / OpenFlow）",
    "两种都是 'match + action'"
  ],
  "explanation": "### Destination-based 是历史\n古典 router 只按 dst IP 转发。\n\n### Generalized 是现代\nSDN/OpenFlow 让一台设备能做 router + firewall + NAT + load balancer 等多种事（用同一个 flow table）。详见 lec20。"
},

"lec16:23": {
  "title": "Destination-Based Forwarding",
  "summary": "传统 router 按 dst IP 范围分。例：3 个 link interface (0, 1, 2, 3)，每个负责一段 dst IP 范围。\n\n**Q**：但如果 ranges 不整齐（不连续，不对齐 2 的幂）怎么办？\n**A**：下一页讲 Longest Prefix Matching。",
  "key_points": [
    "FT: dst IP range → interface",
    "Ranges 可能不整齐（CIDR）",
    "→ Longest Prefix Matching"
  ]
},

"lec16:24": {
  "title": "Longest Prefix Matching — 概念 ⭐",
  "summary": "**LPM**：查 forwarding table 时，**选匹配前缀位数最长的那条 entry**。\n\n表例（来自课件）：\n- `11001000 00010111 00010***` ******** → Link 0\n- `11001000 00010111 00011000` ******** → Link 1\n- `11001000 00010111 00011***` ******** → Link 2\n- otherwise → Link 3",
  "key_points": [
    "多条 rule 匹配时 → 选最长前缀的",
    "通配符 `*` 在 rule 里",
    "Examples 在后面几页"
  ]
},

"lec16:25": {
  "title": "LPM 例 1 — match 第一条规则",
  "summary": "Packet dst = `11001000 00010111 00010110 10100001`。\n\n比较：第一条规则前缀 `11001000 00010111 00010***`（高 27 位的 24 位 + 3 位）。packet 前 24 位匹配，位 25-27 = `010`（packet 第三段 00010110 的前 3 位）== `010` ✓ → **匹配 Rule 0**。\n\n→ **Link 0**。",
  "key_points": [
    "Packet: 11001000.00010111.00010110.10100001",
    "Rule 0 前缀 `00010***` 第 25-27 位 = 010",
    "Packet 第 25-27 位也是 010 → match!",
    "**→ Link 0**"
  ]
},

"lec16:26": {
  "title": "LPM 例 1 — 详细匹配标注",
  "summary": "标记『match!』在表上：Rule 0（00010***）的前 24 位 + 3 位 010 都跟 packet 一致 → 匹配。\n\n这是 5 张 LPM 例图中的第 2 张。",
  "key_points": [
    "图示『match!』在表的 Rule 0 旁",
    "前 24 位 + 3 位通配前 = 完全匹配",
    "→ Link 0"
  ]
},

"lec16:27": {
  "title": "LPM 例 2 — 第二个 packet",
  "summary": "Packet dst = `11001000 00010111 00011000 10101010`。\n\n比较多条规则：\n- Rule 0（00010***）：位 25-27 应为 010，packet 是 110 → **不匹配**\n- Rule 1（00011000）：位 25-32 = 00011000，packet 是 00011000 → **匹配**（/32）\n- Rule 2（00011***）：位 25-27 = 011，packet 是 110，**第 4 位**？位 25-27 = 110 != 011，实际：packet 第三段是 00011000，位 25-27 = 000，rule 2 是 011，**应该不匹配**。\n\n等等，让我重看：packet 第三段是 `00011000`，前 3 位 = `000`。Rule 2 `00011***` 前 5 位 = `00011`，packet 前 5 位是 `00011` → **匹配** /27。\n\n所以 **Rule 1 (/32) > Rule 2 (/27)** → Link 1。",
  "key_points": [
    "Packet 第三段 = 00011000",
    "Rule 1 完全匹配 packet (/32)",
    "Rule 2 (/27) 也匹配前 27 位",
    "**选最长 → Rule 1 → Link 1**"
  ]
},

"lec16:28": {
  "title": "LPM 例 2 — 详细匹配标注",
  "summary": "标记『match!』在表上：Rule 1 完全匹配（/32）；Rule 2 也匹配（/27）；选 **最长前缀** Rule 1 → **Link 1**。",
  "key_points": [
    "Rule 1 (/32) 完全匹配 → 最长",
    "→ Link 1",
    "这是 LPM 的核心选择规则"
  ],
  "explanation": "### LPM 选择规则（必背）\n1. 列出所有匹配的 rule\n2. 选**有效前缀位数最多**的那条\n3. 这就是 'longest prefix match'\n\n**易错**：很多人误以为 rule 顺序决定（first match），其实是 longest match。"
},

"lec16:29": {
  "title": "Switching Fabrics — 概念",
  "summary": "**Switching fabric**：把 packet 从 input link 转到合适的 output link。\n\n**Switching rate**：fabric 每秒能转的 packet 数。常用 input/output line rate 的倍数衡量。**N 个 input port：需要 fabric rate 是 line rate 的 N 倍才不会堵**。\n\n图：N 个 input → high-speed switching fabric → N 个 output。",
  "key_points": [
    "Fabric 把 input → output",
    "Switching rate ≥ N × line rate 才不堵",
    "三类 fabric（下一页）"
  ],
  "explanation": "**为什么要 N 倍 line rate**：所有 N 个 input port 满速进来，fabric 必须能同时处理 N × R 的总速率。否则 input port 会排队（HOL blocking 也跟这有关）。"
},

"lec16:30": {
  "title": "Switching Fabrics — 三大类",
  "summary": "Switching fabric 三大类：\n\n1. **Memory**（第一代 router）：CPU 控制，包过 memory 两次\n2. **Bus**：共享 bus 连所有 ports\n3. **Interconnection network**（Crossbar / Clos）：多级开关网，现代高端",
  "key_points": [
    "**Memory**：1980s-90s 第一代",
    "**Bus**：共享总线",
    "**Interconnection**：现代（Crossbar, Clos）"
  ]
},

"lec16:31": {
  "title": "Switching via Memory — 第一代 router",
  "summary": "**First generation routers**：传统计算机，switching 由 CPU 直接控制。Packet 复制到系统 memory。\n\n**速度受限于 memory bandwidth**：每个 datagram 需要 **2 次 bus crossing**（input → memory，memory → output）。",
  "key_points": [
    "1980s-90s 第一代 router",
    "CPU 控制 switching",
    "Packet 过 memory 两次",
    "速度限于 memory bandwidth",
    "现已淘汰"
  ],
  "explanation": "### 为什么 2 次 bus crossing\n1. Input port → memory（写入）\n2. Memory → output port（读出）\n\n每个 packet 进出 memory 都消耗 bus 带宽 → 总带宽减半。\n\n### 慢的原因\n早期 router throughput 不高，主要瓶颈是 memory bus。"
},

"lec16:32": {
  "title": "Switching via a Bus — 共享总线",
  "summary": "**Datagram 通过共享 bus 从 input port memory 直接到 output port memory**。\n\n**Bus contention**：switching 速度限于 bus 带宽。\n\n**例**：32 Gbps bus, Cisco 5600 — 足够 access router 使用。",
  "key_points": [
    "共享 bus 连所有 input/output ports",
    "Bus contention 是瓶颈",
    "32 Gbps Cisco 5600 适合 access router",
    "更高速时不够"
  ]
},

"lec16:33": {
  "title": "Switching via Interconnection Network",
  "summary": "**Crossbar、Clos networks** 等互联网络最初为连接多处理器中的处理器而开发。\n\n**Multistage switch**：n×n 大 switch 由多级小 switch 组成。\n\n**利用并行**：\n- 入口处把 datagram 切成定长 cell\n- Cells 经 fabric 传输\n- 出口处把 datagram 重组\n\n例：3×3 crossbar；8×8 multistage switch 由小 switch 组成。",
  "key_points": [
    "Crossbar / Clos networks",
    "Multistage：大 switch 由小 switch 组成",
    "Datagram → cells → switch → reassemble",
    "高度并行",
    "现代高端 router 用这种"
  ]
},

"lec16:34": {
  "title": "Switching via Interconnection — 多 fabric plane 并行",
  "summary": "**Scaling**：多个 switching planes 并行。**Speedup, scaleup via parallelism**。\n\n**Cisco CRS router**：\n- 基本单元：8 个 switching planes\n- 每 plane：3 级互联网络\n- **总 switching capacity 可达 100s Tbps**",
  "key_points": [
    "多个 fabric planes 并行",
    "Cisco CRS：8 planes × 3-stage",
    "**100s Tbps switching capacity**",
    "顶级 ISP backbone router"
  ]
},

"lec16:35": {
  "title": "Input Port Queuing — HOL Blocking ⭐",
  "summary": "**如果 switch fabric 比 input port 加起来慢 → input 排队**。**Queueing delay 和 input buffer overflow loss**。\n\n**Head-of-the-Line (HOL) blocking**：队头的 datagram 阻碍后面的人前进。\n\n例：output port 竞争 → 只有一个红色 datagram 能转过去，后面的 datagram 即使去其他 output 也卡住。",
  "key_points": [
    "Fabric 慢 → input 排队",
    "**HOL blocking**：队头堵 → 后面动不了",
    "Output port contention 引发",
    "解药：VOQ（virtual output queue）"
  ],
  "explanation": "### 经典例\nInput port 队列：[红→outputA, 绿→outputB, 蓝→outputC]。如果 outputA 此时 busy（另一个 input 也想发到 A），红色队头被堵 → 绿和蓝（其实可以同时发到 B 和 C）卡在红色后面 → **HOL blocking**。\n\n### 解药：VOQ\nInput port 为每个 output port 分开维护队列。这样不同 output 不互相阻塞。\n\n### 考点\n『HOL blocking 是什么？怎么解？』必答：队头堵后面 + VOQ。"
},

"lec16:36": {
  "title": "Output Port Queuing — 概念",
  "summary": "**Output port** 处理：switch fabric → datagram buffer → link layer protocol (send) → line termination → R。\n\n**Buffering 必要**：当 datagram 从 fabric 来得比 link 发送速率快。\n\n**Drop policy**：buffer 满了丢哪个？\n**Scheduling discipline**：哪个 queued datagram 先发？涉及 priority + network neutrality。",
  "key_points": [
    "Fabric 比 link 快 → output 排队",
    "Buffering 必要",
    "Drop policy 决定丢哪个",
    "Scheduling 决定先发哪个"
  ]
},

"lec16:37": {
  "title": "Output Port Queuing — 第二张图",
  "summary": "图示：t 时刻多个 packet 从 input 到 output；one packet time later 还有 packet 在排队。\n\n**Buffering when arrival rate via switch exceeds output line speed**。\n**Queueing delay 和 output port buffer overflow loss**。",
  "key_points": [
    "Arrival > output line speed → 排队",
    "Buffer 溢出 → 丢包",
    "Output port 是丢包主要原因之一"
  ]
},

"lec16:38": {
  "title": "Buffer Management — Drop + Marking",
  "summary": "**Buffer management 两件事**：\n\n**Drop**：buffer 满时丢哪个？\n- **Tail drop**：丢新到的\n- **Priority**：按 priority 丢/挪\n\n**Marking**：哪些 packet 标记表示拥塞？**ECN, RED**",
  "key_points": [
    "Drop policy: tail drop / priority",
    "**Marking**：ECN, RED 提前打标",
    "缓冲耗尽时的策略"
  ],
  "explanation": "### Drop policies\n- **Tail drop**：最简单，buffer 满就丢新到的\n- **Priority drop**：优先丢低优先级 packet（DSCP marking）\n\n### Marking 策略\n- **ECN**（Explicit Congestion Notification）：不丢，给 packet 打 mark → sender 看到后减速 → 避免实际丢包\n- **RED**（Random Early Detection）：buffer 还没满就开始随机丢，提前给 sender 信号"
},

"lec16:39": {
  "title": "Packet Scheduling — FCFS",
  "summary": "**Packet scheduling**：决定下一个发哪个 packet 出 link。\n\n选项：\n- **First Come First Served (FCFS)** = FIFO\n- Priority\n- Round Robin\n- Weighted Fair Queueing\n\n**FCFS**：packet 按到达 output port 的顺序发。也叫 First-in-first-out。",
  "key_points": [
    "FCFS = FIFO",
    "按到达顺序发",
    "最简单",
    "Real world：银行排队"
  ]
},

"lec16:40": {
  "title": "Scheduling — Priority",
  "summary": "**Priority scheduling**：\n- Arriving traffic 按字段（如 header）分类\n- 优先级队列各自排\n- **从最高优先级队列**发（如果有 packet）\n- **同优先级内 FCFS**",
  "key_points": [
    "按 header 字段分类（如 DSCP）",
    "**最高优先级先发**",
    "同优先级内 FCFS",
    "风险：低优先级饿死"
  ],
  "explanation": "### 例\nVoIP 流量优先级高 → 总是优先于 web 流量。\n\n### 风险\n高优先级可能 starve 低优先级。需要 admission control 限制高优先级流量。"
},

"lec16:41": {
  "title": "Scheduling — Round Robin (RR)",
  "summary": "**Round Robin scheduling**：\n- Arriving traffic 按 class 分类\n- Server 循环扫描每个 class queue\n- 每轮从每个 class 发一个 packet（如有的话）",
  "key_points": [
    "循环扫描 classes",
    "每轮：每 class 发一个 packet",
    "Classes 平等",
    "简单 + 公平"
  ]
},

"lec16:42": {
  "title": "Scheduling — Weighted Fair Queueing (WFQ)",
  "summary": "**WFQ**：RR 的泛化。每 class i 有权重 w_i，每循环得到 **加权服务时间**。\n\n$$\\text{Class } i \\text{ 份额} = \\frac{w_i}{\\sum_j w_j}$$\n\n**每 traffic class 的最小带宽保证**。",
  "key_points": [
    "WFQ = 加权 RR",
    "Class i 份额 = w_i / Σw_j",
    "保证最小带宽 / class",
    "QoS-aware router 用"
  ],
  "explanation": "### 直觉\nWFQ 是 RR 的泛化 — 每轮服务每个 class 但量不一样大。\n\n### 例\n3 个 class，weights = [1, 2, 3]。每循环 class 1 发 1 个 packet，class 2 发 2 个，class 3 发 3 个。长期看 class i 占 w_i / Σ 的带宽。\n\n### 最小带宽保证\n只要 class i 有流量，至少拿到 w_i / Σw_j 的带宽。\n\n### 考点\n给 weights 算 share。"
},

"lec16:43": {
  "title": "Sidebar — Network Neutrality 概念",
  "summary": "**什么是 network neutrality？**\n\n1. **技术层面**：ISP 怎么分配资源。Packet scheduling、buffer management 是机制。\n2. **社会 / 经济原则**：保护言论自由 + 鼓励创新 + 鼓励竞争。\n3. **法律：规则和政策**。\n\n不同国家对 net neutrality 有不同 'takes'。",
  "key_points": [
    "技术：ISP 怎么分配资源",
    "社会：言论自由 + 创新 + 竞争",
    "法律：规则执行",
    "各国 'takes' 不同"
  ]
},

"lec16:44": {
  "title": "Network Neutrality — 2015 FCC Order",
  "summary": "**2015 年美国 FCC Order on Protecting and Promoting an Open Internet**：三条 'clear, bright line' 规则：\n\n1. **No blocking** — 『shall not block lawful content, applications, services, or non-harmful devices, subject to reasonable network management.』\n\n2. **No throttling** — 『shall not impair or degrade lawful Internet traffic on the basis of Internet content, application, or service, or use of a non-harmful device, subject to reasonable network management.』\n\n3. **No paid prioritization** — 『shall not engage in paid prioritization.』",
  "key_points": [
    "FCC 2015 三大原则：",
    "① No blocking — 不能阻断合法内容",
    "② No throttling — 不能限速合法流量",
    "③ No paid prioritization — 不能付费插队",
    "subject to 'reasonable network management'"
  ]
},

"lec16:45": {
  "title": "ISP — 电信服务还是信息服务？",
  "summary": "**ISP 是『电信服务』还是『信息服务』提供商**？这从监管角度极重要。\n\n**美国 1934 年和 1996 年电信法**：\n- **Title II**：对电信服务施加 'common carrier duties' — 合理价格、不歧视、必须监管\n- **Title I**：信息服务：无 common carrier 义务（不监管），但 FCC 有 'authority necessary in execution of functions'",
  "key_points": [
    "**Title II**（电信）：受监管，必须公平不歧视",
    "**Title I**（信息）：少监管",
    "ISP 想被 Title I 不受约束",
    "Title II / I 分类是 net neutrality 关键斗争点"
  ],
  "explanation": "### 政治背景\nISP（Comcast、AT&T、Verizon）想根据流量收费（如『付钱给我才能高速访问 Netflix』）。用户和内容提供商（Netflix、Google）反对。\n\nFCC 监管来回切换：2015 严管（Title II）→ 2017 松绑（Title I）→ 2024 再严。\n\n### Title II vs Title I\n- **Title II 电信服务**：像电话公司一样监管。必须『公平、无歧视』。FCC 可以严格管价格、行为。\n- **Title I 信息服务**：像 web 公司，少监管。ISP 可以自由定价 / 限速。\n\n### 考点\n『FCC 2015 三大原则？』必背 no block / no throttle / no paid prioritization。"
},

}

def main():
    data = json.loads(DETAIL.read_text())
    overwritten = 0
    for key, val in NEW.items():
        if key in data:
            old = data[key]
            if 'important' in old:
                val['important'] = old['important']
            data[key] = val
            overwritten += 1
        else:
            data[key] = val
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"lec16 ZH rewrite: overwrote {overwritten}")

if __name__ == "__main__":
    main()
