#!/usr/bin/env python3
"""Deepen lec21 (Data Link Layer + ALOHA/CSMA/CD/Ethernet)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec21:1": {
  "title": "Quiz — Distance Vector 收敛轮数",
  "summary": "3 节点 (A-B-D，环路有 C) 跑 DV，问几轮收敛 + 各节点距离表。",
  "key_points": [
    "每节点维护 distance table（行=目的，列=经哪个邻居）",
    "初始：只填直连邻居的代价；非邻居 = ∞",
    "每轮：邻居发 DV → 收方用 BF 更新 → DV 变了 → 通知邻居",
    "收敛轮数 ≈ 最短路径树最大跳数 - 1（理想条件）"
  ],
  "explanation": "### 这页要传达的核心方法\nDV 题型每年都考。固定流程：\n\n1. **画图**：所有边 + 代价\n2. **写初始 DV table**：每节点行=目的，列=经哪个邻居；只填直连，其他 ∞\n3. **第一轮交换**：每节点把自己的 DV（按行 min）发给所有邻居\n4. **接收方更新**：对每个邻居发来的 DV，用 BF 公式 D_x(y) = c(x, neighbor) + D_neighbor(y) 算新值，跟当前值取 min\n5. **判断稳定**：所有节点 DV 不再变\n\n### 这题（lec21 quiz）的具体例子\n节点 A、B、D + C 在三角中心。边权：A-B=4, A-D=9, B-D=?, B-C=?, ... （图里看）\n\n初始表（举 A 的）：\n```\n       via B   via D\n  B     4       ∞\n  C     ∞       ∞ (A 不直连 C)\n  D     ∞       9\n```\n\n第一轮 B 发 DV 给 A：『B 到 C=3, B 到 D=1』\nA 更新：经 B 到 C = 4+3 = 7；经 B 到 D = min(∞, 4+1) = 5\n\n继续直到稳定。\n\n### 收敛轮数快算（理想）\n找最短路径树里最大跳数 H，收敛 ≈ H − 1 轮。\n这题 3 节点最多 2 跳，所以 ≈ 1-2 轮就稳。",
  "gotcha": "**别漏列**。每节点 DV table 的列数 = 直连邻居数；行数 = 网络中所有节点。初始未直连邻居那一列里所有非直连邻居目的都是 ∞。"
},

"lec21:2": {
  "title": "DV Quiz — 第 1 轮表",
  "summary": "每个节点开始时只知道直连，第一轮交换后填进经邻居到非直连节点的代价。"
},
"lec21:3": {
  "title": "DV Quiz — 第 2 轮表",
  "summary": "继续推演；第二轮 DV 表更细。"
},

"lec21:4": {
  "title": "DV 收敛快算 ⭐",
  "summary": "找最短路径树里最大跳数，减 1 就是同步收敛轮数（理想条件）。",
  "key_points": [
    "前提：同步轮、静态拓扑、无 count-to-infinity",
    "找『从任一节点到最远节点』的跳数 H",
    "收敛 ≈ H − 1 轮"
  ],
  "explanation": "### 直觉\nDV 信息每轮传一跳。要让所有节点知道全网最短路径，必须等最远的那个节点的信息传遍。\n\n如果最长最短路径是 5 跳，需要 4 轮（第一轮邻居知道，第二轮邻居的邻居知道...）。\n\n### 例\nA - B - C - D - E\n最短路径树最大跳数 = 4（A 到 E）\n收敛轮数 = 4 − 1 = **3**\n\n### 不能用快算的情况\n- 异步更新（实际网络）\n- 链路变贵（count-to-infinity）\n- 拓扑动态变化\n\n这些情况只能模拟。"
},

"lec21:5": {
  "title": "Data Link Layer Services — 4 件事",
  "summary": "Framing + Error detection/correction + MAC + Reliable delivery（低 BER 链路常不用）。",
  "key_points": [
    "**Framing**: 加 header/trailer，把 packet 装进 frame",
    "**Error detection/correction**: 处理 bit error（信号衰减、噪声）",
    "**Medium access control (MAC)**: 谁能在什么时候发",
    "**Reliable delivery**: 本地重传（有线常省略，无线必备）"
  ],
  "explanation": "### 为什么 reliable delivery 在有线常省略\n有线 BER ≈ 10⁻¹²（极低），跑个文件几乎不会丢。让 TCP 端到端管就够。\n\n### 无线必须 reliable\n无线 BER 可能 10⁻³，每发 1000 个 bit 就可能错 1 个。如果都让 TCP 端到端重传，性能极差（每错一个就 RTT 级别的等待）。\n\n所以 802.11 在 MAC 层用 ACK + 重传做 link-level reliability。\n\n### 考法\n『Link layer 提供哪些服务？』必背 4 个。\n『为什么有线常省 reliable delivery？』→ BER 低。"
},

"lec21:6": {
  "title": "Two Types of Link Media",
  "summary": "Point-to-point（独占）vs Broadcast（共享）。Broadcast 才需要 MAC 协议。",
  "key_points": [
    "**Point-to-point**：长距光纤、Ethernet switch-host",
    "**Broadcast (shared)**：传统 Ethernet (hub)、802.11 WiFi",
    "Broadcast 上多节点共享 → 需要 MAC 协议协调"
  ]
},

"lec21:7": {
  "title": "Share a Medium — MAC 的本质",
  "summary": "避免多节点同时发；MAC 是分布式协调算法。",
  "explanation": "**MAC 协议的核心问题**：广播介质上，谁能在什么时候发？\n\n要求：\n- 公平（不让某节点饿死）\n- 高效（少浪费 + 少碰撞）\n- 分布式（不需要中央调度）\n\n下面几页讲三类解法。"
},

"lec21:8": {
  "title": "MAC #1: Channel Partitioning",
  "summary": "TDMA / FDMA / CDMA — 每节点固定时隙 / 频段 / 码字。",
  "key_points": [
    "**TDMA**: 时间切等分，每节点固定 slot",
    "**FDMA**: 频带切等分，每节点固定 sub-band",
    "**CDMA**: 用扩频码区分（手机系统）",
    "**优点**：无碰撞；**缺点**：静态分配 → 轻负载时浪费"
  ],
  "explanation": "### 直觉\n像排队上厕所：每人固定 5 分钟一次。如果当前没人想去（轻负载），那 5 分钟也没人能用 → 浪费。\n\n### 现代应用\n- 4G/5G LTE 用 TDMA + FDMA 混合（OFDMA）\n- GSM 早期用 TDMA\n- 蓝牙某种程度上用 TDMA\n\n### 不适合什么场景\n突发流量（bursty）。WiFi 流量极度突发（一会大文件下载，一会闲），TDMA 会大量浪费 → 所以 WiFi 用 random access (CSMA/CA)。"
},

"lec21:9": {
  "title": "MAC #2: Taking Turns",
  "summary": "Polling（master 轮询）/ Token（传 token）。",
  "key_points": [
    "**Polling**：master 节点轮询每个 worker：『轮到你了，发吗？』",
    "**Token passing**：一个 token 在环上转，拿到 token 的节点才能发",
    "**Cons**：overhead（轮询 / 传 token 本身耗时）、latency、单点故障"
  ],
  "explanation": "### Polling 例\n蓝牙 master-slave 模式：master 设备（手机）轮询 slave（耳机）：『有数据吗？』\n\n### Token Passing 例\nToken Ring（IBM 80s 推过，现已绝迹）：一个 token 在环上跑，拿到的才能发。\n\n### 单点故障\nMaster 挂了 / token 丢了 → 全网瘫痪。需要 leader election / token regeneration。\n\n现代有线网都换成 random access（Ethernet）+ switched 架构。"
},

"lec21:10": {
  "title": "How Do You Like These? — 引出 random access",
  "summary": "Controlled access 浪费信道（轻负载 + bursty 流量），让我们看看不避碰、只恢复的方案。"
},

"lec21:11": {
  "title": "MAC #3: Random Access",
  "summary": "想发就发（全速），碰了再恢复。无固定调度。",
  "key_points": [
    "无 master、无固定 slot",
    "节点想发就开始发",
    "**核心问题**：怎么检测 + 怎么恢复",
    "代表：ALOHA, CSMA, CSMA/CD, CSMA/CA"
  ]
},

"lec21:12": {
  "title": "Slotted ALOHA — 最简单的 random access",
  "summary": "1970 Hawaii 大学 Abramson 教授发明，原始无线包交换网。",
  "explanation": "**历史**：Norm Abramson 在夏威夷搞了 AlohaNet，把岛之间的计算机用无线连起来。ALOHA 意为『欢迎/再见』。是计算机网络史上第一个无线 packet radio。"
},

"lec21:13": {
  "title": "Slotted ALOHA — 假设和操作",
  "summary": "时间切等长 slot，每 slot 一个 frame；只在 slot 边界开始发；碰了下 slot 概率 p 重试。",
  "key_points": [
    "时间对齐到 slot",
    "节点同步",
    "可以立即检测碰撞",
    "有 data → 发；碰 → 概率 p 在下个 slot 重试"
  ]
},

"lec21:14": {
  "title": "Slotted ALOHA Timeline 例",
  "summary": "图示节点在不同 slot 发 frame，碰撞 → 重试。"
},

"lec21:15": {
  "title": "Slotted ALOHA 效率推导 ⭐⭐",
  "summary": "N 节点各以 p 发；最优 p* = 1/N → 效率 1/e ≈ 0.37。",
  "key_points": [
    "P(节点 i 成功) = p · (1−p)^(N−1)",
    "总吞吐 S = N · p · (1−p)^(N−1)",
    "对 p 求导：p* = 1/N",
    "代回：S* = (1 − 1/N)^(N−1) → 1/e 当 N → ∞"
  ],
  "formula": "$$S(p) = N p (1-p)^{N-1}, \\quad p^*=\\tfrac{1}{N}, \\quad S^* \\to \\tfrac{1}{e} \\approx 0.368$$",
  "explanation": "### 推导步骤（必会）\n\n**第一步**：P(节点 i 在某个 slot 成功)\n= P(i 发) × P(其他 N-1 个都不发)\n= p × (1-p)^(N-1)\n\n**第二步**：P(任何一个节点成功) = N × p × (1-p)^(N-1)\n（N 个节点独立，加起来）\n\n**第三步**：求 S 对 p 的最大值\ndS/dp = N · [(1-p)^(N-1) + p · (N-1)(1-p)^(N-2) · (-1)]\n     = N · (1-p)^(N-2) · [(1-p) - p(N-1)]\n     = N · (1-p)^(N-2) · [1 - Np]\n\n令 = 0 → p* = 1/N\n\n**第四步**：代回\nS* = N · (1/N) · (1 - 1/N)^(N-1) = (1 - 1/N)^(N-1)\n\n当 N → ∞：(1 - 1/N)^N → 1/e，所以 (1 - 1/N)^(N-1) ≈ 1/e\n\n→ **S_max ≈ 1/e ≈ 0.368** = 36.8%\n\n### Pure ALOHA（不对齐 slot）\n碰撞窗口翻倍（一个 packet 在『发完前』或『发完后 [-T, +T]』都可能碰），效率减半到 1/(2e) ≈ 0.184 = 18.4%。\n\n### 物理意义\nSlotted ALOHA 信道利用率最高 37% → 一大半时间在浪费（碰撞 + 空 slot）。所以后面要 CSMA（先听后说）。\n\n### 考法（高频）\n- 推导 1/e（必须手推 (1-1/N)^N → 1/e）\n- 选择题：max efficiency 多少？\n- Pure vs slotted 谁更优？为什么差 2 倍？",
  "gotcha": "(1 - 1/N)^N → 1/e 这个极限要会推。可用 Taylor 展开或直接记。"
},

"lec21:16": {
  "title": "Slotted ALOHA — 优缺点",
  "summary": "Pros: 简单、单活跃节点全速、分布；Cons: 碰撞 + 空 slot + 同步要求。",
  "key_points": [
    "Pros: 简单；单节点活跃时 100% 利用；高度分布",
    "Cons: 碰撞浪费（约 1/3）；idle slot 浪费；需要同步"
  ]
},

"lec21:17": {
  "title": "Slotted ALOHA 的问题 — 不听信道",
  "summary": "ALOHA 盲发是浪费 → 引出 CSMA。"
},

"lec21:18": {
  "title": "Listen Before Transmit — CSMA",
  "summary": "Carrier sense：传输前先听信道，闲就发，忙就等。仍可能碰（传播延迟）。",
  "key_points": [
    "Sender 监听信道",
    "Idle → 发；Busy → 等",
    "仍可能碰：propagation delay 期间多人都觉得 idle"
  ],
  "explanation": "### CSMA 改进 ALOHA 在哪\n至少避免明显的碰撞（看见别人在发就不抢）。\n\n### 但还会碰\n**传播延迟**：A 在 t=0 发，信号到 B 处需要 d/c 秒。这 d/c 秒内 B 监听信道仍 idle，于是 B 也开始发 → 在中间某处碰撞。\n\n所以 CSMA 减少但不能消除碰撞 → 需要 CSMA/CD 或 CSMA/CA 进一步处理。\n\n### 直觉数字\n10 Mbps 链路 100 m 长，传播延迟 ≈ 500 ns，但一个 frame 也就几 μs，所以 vulnerable window 占比不小。"
},

"lec21:19": {
  "title": "CSMA/CD — Collision Detection ⭐",
  "summary": "边发边听，发现碰撞就 abort + jam + 退避。有线易做 CD（比较 TX/RX 信号）；无线做不到。",
  "key_points": [
    "Carrier sense + Collision detection",
    "碰了立刻 abort（减少浪费）",
    "发 jam 信号（让所有人都知道碰了）",
    "Binary exponential backoff",
    "**无线做不到 CD**（自己发的时候耳朵被淹）"
  ],
  "explanation": "### CSMA/CD 的核心改进\nALOHA 等到 ACK 超时才知道碰了，浪费整个包时间。CSMA/CD 边发边检测，**碰了立刻停**，省下后面的传输时间。\n\n### 怎么检测碰撞（有线）\nNIC 同时听自己的发射信号 + 监听到的总信号。如果两者不一致（叠加了别人的信号）→ 碰撞。\n\n### Jam signal\nDetect 到碰撞后发 32-48 bit 的 jam（噪声）→ 确保所有人都察觉。然后大家 backoff。\n\n### Binary exponential backoff\n第 n 次碰撞，从 [0, 2^n − 1] 选随机 slot 数等待，再试。指数增加避免反复碰。\n\n### 为什么无线不能 CD\n自己天线发射的功率比接收到的别人信号大几亿倍 → 自己的耳朵被自己淹了。\n\n所以无线只能用 collision avoidance（提前避碰，而非 detect 后处理）= CSMA/CA。\n\n### 考法\n- 解释 CD 怎么实现\n- 为什么有线行无线不行\n- min frame size 推导（下页）"
},

"lec21:20": {
  "title": "CSMA/CD Collision Detection 例",
  "summary": "B 和 D 都能检测到碰撞但有距离限制（下页推导）。"
},

"lec21:21": {
  "title": "CSMA/CD Network Length Limit — 2d 推导 ⭐",
  "summary": "最长检测碰撞延迟 = 2 × max propagation delay。决定 min frame size + max cable length。",
  "key_points": [
    "A 发 → 信号到 B 要 d/c 秒",
    "B 在 d/c 之前以为 idle 也开始发",
    "两边信号在中间相撞",
    "碰撞信号传回 A 还需 d/c",
    "→ A 最坏 2d 才检测到碰撞"
  ],
  "explanation": "### 详细 timeline\n```\nt=0:   A 开始发\nt=d:   信号到 B；B 在 t=d-ε 那一刻也以为信道闲开始发\nt=d:   B 处碰撞发生\nt=2d:  碰撞 echo 回到 A\n→ A 在 t=2d 时刻才发现自己发的包碰了\n```\n\n### Min frame size 的含义\n如果 A 的 frame 只持续 1d 秒就发完了，那 A 在 t=1d 已经结束发送，根本来不及在 t=2d 那一刻还在『发同一个 frame』→ collision detection 失效。\n\n所以要求：**frame 持续时间 ≥ 2d → frame size / R ≥ 2d → frame size ≥ 2d·R**\n\n### 10Mbps Ethernet 的具体数\n- Max prop delay 2d = 51.2 μs（标准规定）\n- Min frame = 2d × R = 51.2 μs × 10 Mbps = **512 bit = 64 byte**\n- 由此推出 max cable ≈ 100 m（再长 2d 会超 51.2 μs）"
},

"lec21:22": {
  "title": "CSMA/CD — Min frame 推导 + 数值 ⭐",
  "summary": "10Mbps Ethernet min frame 512 bit；max cable 100 m。",
  "formula": "$$L_{\\min} \\geq 2 \\cdot d_{\\max} \\cdot R$$",
  "key_points": [
    "Min frame 等价说法：让 sender 在 frame 发完前能检测到碰撞",
    "10Mbps: min 512 bit, max cable 100 m",
    "100Mbps Fast Ethernet: 同样 min frame，max cable 缩到 10 m？现代 switched 后这个不重要",
    "1Gbps Ethernet: 用 carrier extension 维持 min frame"
  ],
  "explanation": "### 推导直接套公式\n10 Mbps × 51.2 μs = 512 bit\n\n### 这条规则在现代还有意义吗\n现代 Ethernet 全部 switched + 点对点 + 全双工 → 没有碰撞 → 无需 CSMA/CD。**Min frame 64 byte 仍保留** 是为了向后兼容老的协议。\n\n### 考法\n- 给 R 和 d，算 min frame\n- 给 frame 和 d，判断是否能检测碰撞"
},

"lec21:23": {
  "title": "Random Access 三件套",
  "summary": "Carrier sense + Collision detection + Randomness（避免再次碰）。"
},

"lec21:24": {
  "title": "Ethernet — 起源",
  "summary": "1973 年 Xerox 发明，共享 wired medium，CSMA/CD + binary backoff。"
},

"lec21:25": {
  "title": "Ethernet Evolution — 从 broadcast 到 switched ⭐",
  "summary": "起初是 broadcast；现代全部 switched，点对点全双工，没有 CSMA/CD。",
  "key_points": [
    "最初：所有 host 一根总线，CSMA/CD + binary backoff",
    "现代：switched，每 host dedicated link 到 switch",
    "点对点 + 全双工 = 无碰撞 + 不需要 CSMA/CD",
    "Min frame 64B 保留是为兼容"
  ],
  "explanation": "### Switched Ethernet 优势\n- 多对话并发\n- 每条链路独立 collision domain\n- 全双工：同时发收\n- 更高带宽（1G/10G/40G/100G）\n\n### CSMA/CD 现在还重要吗\n协议规范里还在，但实际数据中心 / 办公网都是 switched，完全不会触发 CSMA/CD。学这个主要是历史 + 理解 collision detection 原理。"
},

"lec21:26": {
  "title": "Ethernet Frame 格式 ⭐",
  "summary": "Preamble + Dst MAC + Src MAC + Type + Payload + CRC。",
  "key_points": [
    "**Preamble**: 7 byte 10101010 + SFD 1 byte 10101011（同步 receiver 时钟）",
    "**Dst MAC**: 6 byte（不匹配 receiver 自己的 MAC 就丢）",
    "**Src MAC**: 6 byte",
    "**Type**: 2 byte (0x0800=IP, 0x0806=ARP, 0x86DD=IPv6)",
    "**Payload**: 46 - 1500 byte",
    "**CRC**: 4 byte（错检）"
  ],
  "explanation": "### 字段顺序记忆\n『PADSTPC』= Preamble, (Add) Dst, (Add) Src, Type, Payload, CRC\n\n### Payload 46-1500\n- 上限 1500: MTU（IP datagram 一般不超 1500）\n- 下限 46: 加上 header (14B) + CRC (4B) = 64B（min frame size 来自 CSMA/CD 推导）\n- 如果 payload < 46，必须 pad 到 46\n\n### Type 字段重要性\nReceiver 收到 frame 后，根据 type 决定交给哪个上层协议处理：\n- 0x0800 → IPv4 → 交给 IP 处理\n- 0x0806 → ARP → 交给 ARP\n- 0x86DD → IPv6\n\n### MAC 地址过滤\nNIC 收到 frame，第一件事看 dst MAC：\n- 是自己的 → 解析\n- 是广播 FF:FF:FF:FF:FF:FF → 解析\n- 都不是 → 直接丢（除非 promiscuous mode）"
},

"lec21:27": {
  "title": "MAC Address — 详细",
  "summary": "6 byte，烧网卡里。前 3 byte = 厂商 OUI，后 3 byte = 厂商自分配。",
  "key_points": [
    "6 byte (48 bit)",
    "举例：00-15-C5-49-04-A9",
    "前 24 bit = OUI (厂商, IEEE 分配)",
    "后 24 bit = 厂商自分配",
    "Broadcast = FF:FF:FF:FF:FF:FF",
    "**MAC vs IP 区别**：MAC 烧硬件、扁平、L2、单 LAN；IP 软件配、层级、L3、全网"
  ],
  "explanation": "### MAC vs IP 区别（必考）\n\n| | MAC | IP |\n|---|---|---|\n| 层 | L2 | L3 |\n| 长度 | 6 B | 4 B (v4) |\n| 分配 | 厂商烧网卡 | 用户/DHCP 配置 |\n| 结构 | 扁平（不指示位置）| 层级（前缀指示子网）|\n| 范围 | 单 LAN | 全网 |\n| 改变 | 跟着网卡 | 跟着位置 |\n\n### 类比\n- MAC 像身份证号（一辈子不变，跟着你）\n- IP 像家庭住址（搬家就变）\n\n### MAC 怎么知道目的不在本子网？\n通过 netmask 判断目的 IP 是否在本子网（netmask 由 DHCP 给）。"
},

"lec21:28": {
  "title": "MAC 两种：Burned-in vs Effective",
  "summary": "Burned-in = 厂商烧的；Effective = OS 当前用的（可改）。",
  "key_points": [
    "**Burned-in**: 出厂烧硬件，全球唯一",
    "**Effective**: OS 配置，可覆盖（MAC spoofing）",
    "用于隐私随机化、虚拟化、安全测试",
    "**网络不靠 MAC 做安全**（容易伪造）"
  ],
  "explanation": "### 为什么要 effective MAC\n- **隐私**：iOS / Android 现在为每个 WiFi 网络生成随机 MAC，防止被广告商跟踪\n- **虚拟化**：VM 需要分配自己的 MAC\n- **MAC spoofing**：测试 / 攻击场景\n\n### 后果\n靠 MAC 做白名单的网络（咖啡馆 WiFi 之类）容易被伪造。所以真正的安全要靠 802.1X / WPA3 之类 L2+ 上层协议。"
},

"lec21:29": {
  "title": "Bootstrap Communication — DHCP + ARP",
  "summary": "Host 加入网络两件事：DHCP 拿 IP，ARP 找 MAC。"
},

"lec21:30": {
  "title": "Quiz — BDP 计算（接 lec22:1）",
  "summary": "声速 1.5km/s + 光速 3×10⁸m/s 算 BDP。"
},

}

def main():
    data = json.loads(DETAIL.read_text())
    data.update(NEW)
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"updated {len(NEW)} entries; total now {len(data)}")

if __name__ == "__main__":
    main()
