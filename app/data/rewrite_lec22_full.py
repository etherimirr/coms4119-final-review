#!/usr/bin/env python3
"""Full per-page rewrite for lec22 (BDP quiz + ARP + Switch + VLAN + Wireless intro, 31 pages)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec22:1": {
  "title": "Quiz — Bandwidth-Latency Product (BDP)",
  "summary": "题目（接 lec21:30）：30 Kbps 60m + 4 Mbps 3km。声速 1.5 km/s，光速 3×10⁸ m/s。**答**: BDP ≈ **2400 bits**。\n\n**步骤**:\n- 平均带宽 = min(30 Kbps, 4 Mbps) = 30 Kbps\n- 段 1 prop = 60m / 1.5km/s = 40 ms\n- 段 2 prop = 3km / 3×10⁸ m/s = 0.01 ms\n- 单程 ≈ 40 ms, RTT = 80 ms\n- **BDP = 30 Kbps × 80 ms = 2400 bits**",
  "key_points": [
    "BDP = bandwidth × RTT",
    "Bottleneck = min(各段)",
    "勿忘 RTT = 2 × 单程",
    "BDP = 2400 bits ≈ 300 byte"
  ],
  "explanation": "**意义**：管道里能同时容纳 2400 bit。Sender 滑动窗口至少 2400 bit 才能填满管道（不浪费带宽）。\n\n**联想题型**：\n- 给 BDP 反推 RTT 或带宽\n- 算需要多大窗口才能利用率 100%"
},

"lec22:2": {
  "title": "Who Am I — DHCP 拿 IP",
  "summary": "**Dynamic Host Configuration Protocol (DHCP)**: host 加入网络时广播『我要 IP』，server 应答给一个。\n\n**Why dynamic**: 移动设备到处跑，每个网络的 IP 段不同，不能硬编码。",
  "key_points": [
    "DHCP: 动态配置 IP",
    "Process: broadcast 'I need IP' → server 'have 1.2.3.4'",
    "支持移动设备 + 复用地址 + plug-and-play"
  ]
},

"lec22:3": {
  "title": "DHCP — 还能给什么",
  "summary": "DHCP 不只给 IP，还给：(a) **Temporary IP address**；(b) **Local DNS name server**；(c) **Gateway router (first-hop router) IP**；(d) **Netmask** (用来判断目的是否本子网)。所有这些都广播过程中给。",
  "key_points": [
    "(a) Temp IP address",
    "(b) Local DNS server",
    "(c) Gateway router (first-hop) IP",
    "(d) Netmask",
    "全部 + lease 时长"
  ],
  "explanation": "**为什么 4 样必给**：\n- **IP**: 自己身份\n- **Gateway**: 跨子网包要交给 router；不知道 router IP 就跨不出去\n- **DNS server**: 浏览器输 google.com 要解析\n- **Netmask**: 判断目的 IP 是否本子网 → 决定 ARP 谁\n\n**没 netmask 会怎样**：host 看到 dst 1.2.3.4，不知是否同子网。试直接 ARP 1.2.3.4 → 如果在别的子网，本地广播没人回 → 永远连不上。\n\n**考点**：『DHCP server 返回什么？』必背 4 样 + lease。"
},

"lec22:4": {
  "title": "The Need of Address Resolution",
  "summary": "**Problem**: 网卡只懂 MAC，不懂 IP。要发 IP packet，必须先把 dst IP 翻译成 dst MAC。\n\n**例**: 1.2.3.53 host 要发包给 1.2.3.156 (DNS server)。Frame 在 LAN 上传，需要 dst MAC，但 packet 里只有 dst IP。",
  "key_points": [
    "Adapters 只懂 MAC",
    "Need: dst IP → dst MAC translation",
    "这就是 ARP 的作用"
  ],
  "explanation": "**为什么 adapter 不懂 IP**：\n- 网卡处理 L2 frame（看 MAC）\n- IP 在 L3（packet inside frame）\n- 网卡只负责把 frame 在 LAN 上传，不解析里面的 IP\n\n**所以 sender 在 L3 → L2 时必须知道**：这个 IP 对应哪个 MAC（同 LAN 内）。下页 ARP 解决。"
},

"lec22:5": {
  "title": "Who Are You — ARP",
  "summary": "**Address Resolution Protocol (ARP)**: 已知 IP，问『谁的 MAC 是这个 IP？』。\n\n**流程**: 广播 'Who has 1.2.3.6?' → 目标节点 unicast 回 '0C-C4-11-6F-E3-98 has 1.2.3.6!'。",
  "key_points": [
    "Broadcast 'Who has IP X?'",
    "目标节点 unicast 回应",
    "其他节点忽略"
  ],
  "explanation": "**ARP 是 L2 协议**：广播只在同一 LAN 内。\n\n**详细流程**：\n1. Host A 想发包给 IP 1.2.3.6（同子网）\n2. A 查自己 ARP 表，没找到\n3. A 广播 ARP request：『Who has 1.2.3.6?』，目的 MAC 是 FF:FF:FF:FF:FF:FF（广播）\n4. LAN 上所有节点收到\n5. 只有 IP=1.2.3.6 的节点 B 回应 ARP reply：『I'm at MAC 0C-C4-...』，**unicast 给 A**\n6. A 把 (1.2.3.6, 0C-C4-...) 存进 ARP 表，TTL 几分钟"
},

"lec22:6": {
  "title": "ARP — Table + Cache",
  "summary": "每节点维护 **ARP table**: (IP address, MAC address, TTL) 三元组。发包先查表；命中直接发；不命中才广播 ARP request。**Soft state**: TTL 到期清除，自动重学。",
  "key_points": [
    "ARP table: (IP, MAC, TTL)",
    "查表命中直接用",
    "未命中 → 广播 query",
    "Cache 带 TTL → soft state",
    "TTL 到期自动清"
  ],
  "explanation": "**为什么 cache**：每次发包都广播 ARP，**链路上一半都是 ARP 流量**。Cache 让常用 IP 的 MAC 直接命中。\n\n**Soft state 优点**：\n- 不需显式注销\n- 过期自动清，容错（对方换了网卡会自动修复）\n\n**典型 TTL**：Linux 默认 60 秒；Mac 默认 20 分钟。\n\n**例**：\n1. A 想发给 1.2.3.156\n2. 查 ARP 表：没命中\n3. 广播 'Who has 1.2.3.156?'\n4. 1.2.3.156 (即 DNS server) 回应 '58-23-D7-FA-20-B0'\n5. A cache 并发包\n\n**考点**：『ARP 流程？为什么 reply 是 unicast 而不是 broadcast？』答：reply unicast 给原 sender 即可（已知 sender MAC，从 request 里看到）。"
},

"lec22:7": {
  "title": "ARP — Cross-Subnet（找的是 first-hop router）",
  "summary": "**关键陷阱**: 当目的 IP **不在本子网** 时，host 用 ARP 解析的是 **first-hop router 的 MAC**，不是终点 IP 的 MAC。\n\n**例**: 1.2.3.48 要发给 5.6.7.x。\n1. 1.2.3.48 用 netmask 判断 5.6.7.x 不在本子网\n2. 1.2.3.48 ARP first-hop router (1.2.3.19) 的 MAC\n3. 包封装：dst MAC = router MAC, dst IP = 5.6.7.x\n4. Router 收到后解 frame，看 dst IP，再做下一跳决策",
  "key_points": [
    "目的不同子网 → ARP **first-hop router**，**不是终点 IP**",
    "Host 怎么知道目的不在本子网？→ 用 netmask 判断（DHCP 给的）",
    "Host 怎么知道 first-hop router IP？→ 也是 DHCP 给的 (gateway)",
    "**Frame 沿路 MAC 变化，IP 不变（端到端语义）**"
  ],
  "explanation": "**Frame 沿路 MAC 变化**：\n```\nA (1.2.3.48) → R (1.2.3.19) → R' → B (5.6.7.x)\n\n段 A→R:\n  src MAC = A's MAC\n  dst MAC = R's LAN-side MAC\n  src IP  = 1.2.3.48\n  dst IP  = 5.6.7.x  ← 不变\n\n段 R→R':\n  src MAC = R's WAN-side MAC\n  dst MAC = R's next-hop MAC\n  src IP  = 1.2.3.48  ← 不变\n  dst IP  = 5.6.7.x   ← 不变\n```\n\n**IP 始终不变**（端到端语义），**MAC 每跳变**（链路层 hop-by-hop）。\n\n**考点（高频，期中考过）**：『1.2.3.48 要发包给 5.6.7.8，它 ARP 谁？』答：先用 netmask 算出 5.6.7.8 不在本子网，所以 ARP **自己 default gateway**（1.2.3.19）的 MAC，**不是 5.6.7.8 的 MAC**。",
  "gotcha": "**最容易错**：以为 ARP 直接找终点 MAC。永远记得 ARP 是 L2，跨 L2 必须经 router。"
},

"lec22:8": {
  "title": "Key Ideas — Broadcasting, Caching, Soft state",
  "summary": "ARP + DHCP 三大共通设计思想：\n\n(1) **Broadcasting**: 用广播做初步发现（前提：广播域有限）；\n(2) **Caching**: 学到的存起来减少 overhead；\n(3) **Soft state**: TTL 到期自动清，容错。",
  "key_points": [
    "**Broadcasting**: 初次发现, 广播域有限",
    "**Caching**: 存学到的, 减少 overhead",
    "**Soft state**: TTL → 自动清, 容错"
  ],
  "explanation": "**这三条是 Internet 协议设计的通用范式**：\n- DHCP 广播 Discover；ARP 广播 query → broadcasting\n- ARP 缓存 IP→MAC；DNS 缓存域名解析 → caching\n- 都带 TTL，到期重学 → soft state\n\n**Soft state vs Hard state**：\n- Hard state: 必须显式注册 / 注销（如 TCP 连接）\n- Soft state: 到期自动清，更容错，是 Internet 设计哲学之一"
},

"lec22:9": {
  "title": "802.3 Ethernet Standards",
  "summary": "Many different Ethernet standards. Common: MAC protocol + frame format. Different: 速度（2 Mbps ~ 80 Gbps）和物理介质（fiber, cable）。\n\n命名规则：100BASE-TX, 100BASE-T2, 100BASE-FX, 100BASE-T4, 100BASE-SX, 100BASE-BX。",
  "key_points": [
    "Common: MAC + frame 格式 (同所有 802.3)",
    "Different: 速度 + 物理介质",
    "100BASE-TX: 双绞铜线 100 Mbps",
    "100BASE-FX: 光纤 100 Mbps",
    "速度: 2 Mbps - 80 Gbps"
  ],
  "explanation": "**命名规则**：`[Speed]BASE-[Media]`：\n- 100 = 100 Mbps\n- BASE = baseband signaling\n- TX = Twisted pair, X 表示某种编码\n- FX = Fiber\n\n**实际不太考具体型号**，知道有多种速度 + 介质即可。"
},

"lec22:10": {
  "title": "Switches",
  "summary": "**Switch** = link-layer device。**Store, forward** Ethernet frames。**Examine** incoming frame's MAC address，**selectively forward** to one-or-more outgoing links。**Plug-and-play, self-learning**：不需要配置。",
  "key_points": [
    "Switch = L2 device",
    "Store + forward Ethernet frames",
    "Look at dst MAC → 选 outgoing link(s)",
    "Plug-and-play + self-learning",
    "无需配置"
  ],
  "explanation": "**vs Hub**:\n- Hub (老旧): 所有 port 同一 collision domain，物理层广播\n- Switch: 每 port 独立 collision domain，按 MAC 智能转发\n\n**现代 Ethernet** 几乎全是 switched，hub 基本绝迹。"
},

"lec22:11": {
  "title": "Switch — Multiple Simultaneous Transmissions",
  "summary": "**Hosts 各自 dedicated 直连 switch**。Switches buffer packets。Ethernet 协议在每条 incoming link 上跑：\n- **无碰撞**（点对点）\n- **全双工**（同时收发）\n- 每 link 独立 collision domain\n\n**Limit**: A → A' 和 C → A' 不能同时（同目的 A'）。",
  "key_points": [
    "每 host 跟 switch dedicated 直连",
    "Switch buffer packets",
    "**无碰撞**, **全双工**",
    "每 link 独立 collision domain",
    "Same dst → 不能并发（在 switch 内排队）"
  ],
  "explanation": "**switched Ethernet 大幅提升性能**：原本所有 host 共享一根线（总线），现在每对 host-switch 是独立链路，多对话并发，速度乘以并发数。\n\n**唯一限制**：同一时刻只有一个 frame 进入 switch 某 port，所以 A→A' 和 C→A' 同时 → switch 在 A' 输出 port 上排队。"
},

"lec22:12": {
  "title": "Switch — Forwarding Table",
  "summary": "**Q**: switch 怎么知道 A' 可达 interface 4, B' 可达 interface 5？\n\n**A**: 每 switch 有 **switch table**，entry = (host MAC, interface, timestamp)。像 routing table，但靠 self-learning 填。",
  "key_points": [
    "Switch table entry: (MAC, port, TTL)",
    "类似 routing table 但自学填",
    "下一页讲 self-learning"
  ]
},

"lec22:13": {
  "title": "Switch — Self Learning",
  "summary": "**自学习** 流程：\n\n1. **Frame 到达**: switch 看 src MAC + 来自哪个 port → 学到『这个 MAC 经那个 port』\n2. **记录 entry**: (src MAC, in-port, TTL)\n3. **Forward**:\n   - Dst MAC 在表 → 单口发\n   - Dst MAC 不在表 → **flood**（除入口外所有 port）\n4. **TTL 到期自动清**\n\n**Plug-and-play**: 不需要配置。",
  "key_points": [
    "Frame in → 学 (src MAC, port)",
    "Dst MAC 在表 → 单口发",
    "Dst MAC 不在表 → flood",
    "TTL 自动清",
    "Plug-and-play"
  ],
  "explanation": "**完整 timeline 例**（必背）：\n\n```\nA → A' 第一次 (假设 A 在 port 1, A' 在 port 4)\n\nt=1: A 发 frame (src=A, dst=A')\n     Switch 收到 frame 从 port 1\n     学：(A, 1, TTL=60)\n     查 dst=A'：不在表 → flood 到 port 2, 3, 4, 5, 6\n\nt=2: A' 收到，回 frame (src=A', dst=A)\n     Switch 收到 frame 从 port 4\n     学：(A', 4, TTL=60)\n     查 dst=A：在表（port 1）→ 单口发到 port 1\n\nt=3 之后: A → A' 都不再 flood，直接走 port 4\n```\n\n**为什么这样设计**：\n- frame 的 src MAC 是『免费信息』\n- Switch 看到 frame 从 port 1 进来，就知道 src 那个 host 可以通过 port 1 到达\n- 不需要任何配置，纯自动学习\n\n**考点（高频）**：『给一个 frame 序列，画每步 switch table 长什么样』。"
},

"lec22:14": {
  "title": "VLAN — 概念 + 动机",
  "summary": "**Q: 大 LAN scale + 用户移动怎么办**？\n\n**单 broadcast domain 问题**：\n- Scaling: 所有 L2 广播 (ARP, DHCP, unknown MAC) 跨整个 LAN\n- Efficiency, security, privacy issues",
  "key_points": [
    "大 LAN 的广播问题",
    "ARP + DHCP 广播跨全 LAN",
    "效率 + 安全 + 隐私问题",
    "→ VLAN 解决"
  ],
  "explanation": "**问题数字**：\n- 1000 个 host 各每分钟 1 个 ARP → 每秒 ~17 个广播 + DHCP + IPv6 NDP + mDNS\n- 加起来广播流量呛网络\n\n**安全/隐私**：广播到所有 host → 任何 host 都能监听（promiscuous mode）→ 攻击面大\n\n**解药 VLAN**：把大 LAN 切成多个虚拟 LAN，**每 VLAN 是独立广播域**。"
},

"lec22:15": {
  "title": "VLAN — 行政场景",
  "summary": "另一动机：用户搬办公室。例：CS 用户搬到 EE 部门，物理插 EE switch，但希望保留 CS LAN 访问权限。\n\n**Administrative issue**: 物理位置 ≠ 逻辑归属。",
  "key_points": [
    "CS 用户搬到 EE 物理位置",
    "希望仍在 CS LAN（用 CS 内部服务器、文件夹）",
    "VLAN: 物理位置 vs 逻辑归属 解耦"
  ]
},

"lec22:16": {
  "title": "Port-based VLAN — 配置",
  "summary": "**Port-based VLAN**: switch ports 划分到多个 VLAN，每个 VLAN 等效一台独立 switch。例: 一台 16-port switch，port 1-8 = VLAN A (EE), port 9-15 = VLAN B (CS)。",
  "key_points": [
    "Port-based: 按 switch port 划分 VLAN",
    "MAC-based VLAN: 按 endpoint MAC 划分（替代）",
    "例: port 1-8 → VLAN A, port 9-15 → VLAN B",
    "一台物理 switch 当多台逻辑 switch 用"
  ],
  "explanation": "**配置方式**：通过 switch management software 配置 'port X belongs to VLAN Y'。\n\n**MAC-based VLAN**：替代方案，按 endpoint MAC 划分。优点：用户搬位置后 VLAN 跟着 MAC 跑（不依赖物理 port）。"
},

"lec22:17": {
  "title": "Port-based VLAN — 特性",
  "summary": "**Features**:\n(a) **Traffic isolation**: VLAN A 的 frame 进不了 VLAN B（包括广播）。\n(b) **Dynamic membership**: port 可以随时重分配 VLAN。\n(c) **Forwarding between VLANs**: 通过 router（就像独立 switch 之间）。",
  "key_points": [
    "**Traffic isolation**: 跨 VLAN 隔离",
    "**Dynamic membership**: port 可重分配",
    "**Cross-VLAN**: 必须经 router",
    "实际: 厂商卖 switch + router 一体设备"
  ],
  "explanation": "**为什么跨 VLAN 必须 router**：\n- VLAN 划分在 L2，router 在 L3\n- Switch 看 frame 的 VLAN tag 后只在同 tag 内转发\n- 跨 VLAN = frame 进到一个新 L2 域，需要 L3 设备解包 → 重新封装 → 发到新 VLAN\n\n**VLAN trunk**：两台 switch 之间的链路要承载多个 VLAN 流量时，frame 加 **802.1Q tag**（VLAN ID + Pri）→ trunk link。\n\n**考点**：『为什么 VLAN？』答：隔离 + 安全 + 灵活。『跨 VLAN 怎么通？』→ router。"
},

"lec22:18": {
  "title": "Router vs Switch — 对比表",
  "summary": "都是 store-and-forward。区别：\n\n| | Router | Switch |\n|---|---|---|\n| 层 | L3 (network) | L2 (link) |\n| 看 | dst IP | dst MAC |\n| 表来源 | 路由算法 (OSPF/BGP) | 自学习 |\n| 范围 | 跨网 | 单 LAN |\n| TTL | −1 | 不动 |\n| 失败处理 | drop + ICMP | flood |",
  "key_points": [
    "都 store-and-forward",
    "Router: L3, IP, 跑路由算法, 跨网, 减 TTL",
    "Switch: L2, MAC, 自学习, 单 LAN, 不动 TTL"
  ],
  "explanation": "**一句话区分**：\n- 看到『跨子网』『跨网络』→ router\n- 同一 LAN 内点对点 → switch\n\n**还有这些区别**：\n- Router 必须解 frame → IP → 看 dst IP → 重新封 frame；耗时\n- Switch 直接看 frame 的 dst MAC，转发；更快\n\n**考点**：『Router vs Switch 对比？』必背全表。\n『跨 VLAN 通信用什么？』→ router。\n『同 LAN 内 host 通信？』→ switch（实际经过 switch）。"
},

"lec22:19": {
  "title": "Wireless Physical Layer & MAC — 章节封面",
  "summary": "进入无线章节。Xia Zhou 教，2026 年 4 月 9 日。本章 = wireless physical layer + wireless MAC protocols。",
  "key_points": ["新章节，4/9 开课"]
},

"lec22:20": {
  "title": "My Goals (Xia 老师)",
  "summary": "教学目标：(1) 让你掌握**无线通信基础物理** + **无线 MAC 协议**；(2) 介绍**前沿研究**让你看到 wireless networking 的有趣方向。",
  "key_points": [
    "Goal 1: 基础物理 + MAC 协议",
    "Goal 2: 前沿研究 (interesting)",
    "(教学目标 page，非考点)"
  ]
},

"lec22:21": {
  "title": "Wireless Networks — 三层范围",
  "summary": "按地理范围划分：\n- **WPAN (Personal Area)**: Bluetooth, Zigbee, RFID — 米级\n- **WLAN (Local Area)**: WiFi (802.11), mesh — 数十米\n- **WWAN (Wide Area)**: Cellular networks, WiMAX — 公里\n\n**Centralized networks** for tight control and seamless connectivity.",
  "key_points": [
    "**WPAN**: Bluetooth, Zigbee, RFID — 米级",
    "**WLAN**: WiFi 802.11, mesh — 数十米",
    "**WWAN**: Cellular, WiMAX — 公里",
    "Centralized vs decentralized control"
  ]
},

"lec22:22": {
  "title": "Radio Propagation 101 — 章节小标题",
  "summary": "下面几页讲无线信号怎么传播，为后续 MAC 设计铺垫。",
  "key_points": ["子章节过渡"]
},

"lec22:23": {
  "title": "If We Could See WiFi Signals (1)",
  "summary": "Artist 可视化 WiFi 信号图片（Gizmodo 文章）。激励：信号在空气里到处弹，不像电缆那样『一条线走到底』。",
  "key_points": ["可视化激发", "Source: gizmodo.com"]
},
"lec22:24": { "title": "WiFi Visualizations (2)", "summary": "继续可视化 WiFi 信号。" },
"lec22:25": { "title": "WiFi Visualizations (3)", "summary": "继续可视化 WiFi 信号。" },
"lec22:26": { "title": "WiFi Visualizations (4)", "summary": "继续可视化 WiFi 信号。" },

"lec22:27": {
  "title": "What Happens After We Cut the Wire?",
  "summary": "拔掉网线后，信号在空气里到处飞。要解决的物理问题：path loss（衰减）+ 多路径 + 干扰。",
  "key_points": [
    "无线 ≠ 有线（一根管子）",
    "信号到处反射、衍射、散射",
    "需建模 path loss"
  ]
},

"lec22:28": {
  "title": "Just Consider the Direct Path — Free-Space Pathloss",
  "summary": "**自由空间路径损耗** 公式：\n$$\\text{Signal power loss} = \\left(\\frac{4\\pi d}{\\lambda}\\right)^2 = \\left(\\frac{4\\pi d f}{c}\\right)^2$$\n\nd = 距离, λ = 波长, f = 频率, c = 光速。**Higher frequency (shorter wavelength) has higher signal loss.**",
  "key_points": [
    "Free-space pathloss = (4πd/λ)² = (4πdf/c)²",
    "d = 距离, λ = 波长, f = 频率, c = 光速 3×10⁸",
    "**频率高 → 波长短 → loss 大**"
  ],
  "explanation": "**直觉**：点光源辐射到球面，球面积 4πd² → 单位面积功率 ∝ 1/d² → 距离 ×2，功率 ÷4 = **-6 dB / 加倍距离**。\n\n**为什么频率高 loss 大**：天线有效面积 ∝ λ²，高频 λ 小 → 天线接同样能量需要更大物理面积（或牺牲距离）。\n\n**5GHz vs 2.4GHz**：5GHz 衰得快，距离短但带宽宽；2.4GHz 衰得慢，距离远但带宽窄 + 拥挤。"
},

"lec22:29": {
  "title": "Pathloss — 频段对比表",
  "summary": "三个 WiFi 频段对比：\n\n| Freq | Range | BW | Wavelength |\n|---|---|---|---|\n| 900 MHz | 902-928 MHz | 26 MHz | 0.33 m / 13.1\" |\n| 2.4 GHz | 2.4-2.4835 GHz | 83.5 MHz | 0.125 m / 4.9\" |\n| 5 GHz | 5.15-5.35 GHz | 200 MHz | 0.06 m / 2.4\" |",
  "key_points": [
    "900 MHz: λ=0.33m, BW=26 MHz",
    "2.4 GHz: λ=0.125m, BW=83.5 MHz",
    "5 GHz: λ=0.06m, BW=200 MHz",
    "频率↑ → 波长↓ → loss↑，但 BW↑"
  ]
},

"lec22:30": {
  "title": "Pathloss with α — 实际环境",
  "summary": "自由空间公式只在外太空准确。**General case**: loss ∝ d^α (path loss component)。α 典型值：\n\n| Environment | α |\n|---|---|\n| Free space | 2 |\n| Urban area cellular | 2.7-3.5 |\n| Shadowed urban cell | 3-5 |\n| Obstructed in building | 4-6 |\n| Obstructed in factories | 2-3 |",
  "key_points": [
    "Real env: loss ∝ d^α",
    "α 描述衰减速度",
    "Free space: α=2",
    "Urban: α=2.7-3.5",
    "Indoor obstacle: α=4-6"
  ],
  "explanation": "**α 物理意义**：α=2 表示『每加倍距离 -6 dB』，α=4 表示『每加倍 -12 dB』，衰得快。\n\n**实际 vs 理论**：自由空间公式假设无障碍。现实有墙、地面、家具，每反射 / 衍射吃掉一些能量 → α 比 2 大很多。\n\n**应用**：lec23:9 用 PL(d) = PL(d₀) + 10α · log(d/d₀) + X 计算实际 pathloss。\n\n**考点**：『为什么室内 WiFi 衰得比公式快？』α 大。"
},

"lec22:31": {
  "title": "The Physics of Radio Propagation — 三种传播现象",
  "summary": "下一章 lec23 开头详讲三种传播现象（反射、衍射、散射）。",
  "key_points": ["章节过渡, 引入 lec23"]
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
    print(f"lec22 rewrite: overwrote {overwritten}, added {new}")

if __name__ == "__main__":
    main()
