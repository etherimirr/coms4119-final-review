#!/usr/bin/env python3
"""Full per-page rewrite for lec21 (DV quiz + Data Link + ALOHA + CSMA/CD + Ethernet, 30 pages)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec21:1": {
  "title": "Quiz — DV 收敛轮数（3 节点）",
  "summary": "题目：3 节点（实际图是 4 节点 A, B, C, D；边权 A-B=4, B-C=3, C-D=1, A-D=9）所有节点跑 distance vector。**Q: 几轮收敛？**\n\n**做法**：画 distance vector 表，模拟邻居交换。",
  "key_points": [
    "4 节点：A B C D",
    "Edges: A-B=4, B-C=3, C-D=1, A-D=9",
    "求 DV 算法收敛轮数"
  ],
  "explanation": "**完整解题流程**：\n\n**Round 0 (Init)** — 每节点只填直连：\n```\n     A           B           C           D\n  via B  D    via A  C    via B  D    via A  C\nA  -  -      4   ∞       ∞    ∞       9    ∞    (only direct edges, others ∞)\nB  4   ∞     -  -        3    ∞       ∞    1\nC  ∞   ∞     3   ∞       -  -         ∞    1\nD  9   ∞     ∞   1       ∞   1        -  -\n```\n(简化：每节点的 distance table)\n\n**Round 1**: 邻居互换 DV，每节点用 BF 重算。\n\n**Round 2-3**: 继续直到 DV 稳定。\n\n**直觉**：最短路径树的最大跳数 = 3 (A→B→C→D)。收敛轮数 ≈ 3-1 = 2 轮（理论同步前提）。\n\n实际答案需画完整 DV 表（下面几页详解）。"
},

"lec21:2": {
  "title": "Quiz Round 1 — A 的视角",
  "summary": "Round 1 后 A 的 distance table 更新。A 收到 B 发来的 DV (B: A=4, C=3, D=∞ 等)，用 BF 重算：\n- A→C 经 B = 4+3 = 7 → A 的 DV 加上 C=7 via B\n- A→D 经 B = 4+∞ = ∞ → 不变\n- A→D 经 D = 9 (直连) → 不变",
  "key_points": [
    "A 收到 B 和 D 的 DV",
    "A→C 经 B = 4+3 = 7 (新)",
    "A→D 经 D = 9 (直连，保持)",
    "A→D 经 B = 4+∞ = ∞ (不变)"
  ]
},

"lec21:3": {
  "title": "Quiz Round 1 — B 的视角",
  "summary": "Round 1 后 B 的 distance table。B 收到 A (A: B=4, D=9) 和 C (C: B=3, D=1) 的 DV：\n- B→D 经 A = 4+9 = 13\n- B→D 经 C = 3+1 = 4 → 更新 DV: B→D=4 via C",
  "key_points": [
    "B 收到 A, C 的 DV",
    "B→D 经 A = 4+9 = 13",
    "B→D 经 C = 3+1 = **4** → 新",
    "B 的 DV: A=4, C=3, D=4"
  ]
},

"lec21:4": {
  "title": "Quiz — 快速找收敛轮数",
  "summary": "**Trick**: 不用完整模拟，用『最长最短路径』法。\n\n方法：\n1. 找出图里每对节点的 shortest path\n2. 在所有 shortest path 中，找跳数最大的\n3. **最大跳数 − 1 = 收敛轮数**（同步前提）\n\n**Assumptions**: synchronous rounds, no count-to-infinity, static topology, no triggered updates.",
  "key_points": [
    "找所有节点对的 shortest path",
    "Identify the one with max hops",
    "**Max hops − 1 = convergence rounds**",
    "Assumes: sync rounds, no CTI, static topology"
  ],
  "explanation": "**为什么**：DV 信息每轮传一跳。要让最远的节点知道，需 max-hops−1 轮（第一轮邻居知道、第二轮邻居的邻居知道、...）。\n\n**本题**: A↔D 经 B-C-D 是 3 跳路径 → 收敛 2 轮。\n\n**例外**：如果有 link cost 变化、CTI、异步、触发更新，实际收敛比这个慢。"
},

"lec21:5": {
  "title": "Data Link Layer Services（复习）",
  "summary": "4 大服务：(1) Framing；(2) Error detection/correction；(3) Medium access control (MAC)；(4) Reliable delivery（有线常省，无线必备）。",
  "key_points": [
    "Framing: 加 header/trailer 包 packet",
    "Error detection/correction: 处理 bit error",
    "MAC: 谁能在什么时候发",
    "Reliable delivery: 本地重传"
  ]
},

"lec21:6": {
  "title": "Two Types of Link Media",
  "summary": "**Point-to-point**: 长距 fiber、Ethernet switch ↔ host。**Broadcast (shared)**: 传统 Ethernet (hub)、802.11 WiFi。Broadcast 介质才需要 MAC 协议协调。",
  "key_points": [
    "**Point-to-point**: 长距 fiber, switch-host",
    "**Broadcast**: 传统 Ethernet, 802.11 WiFi",
    "Broadcast → 需要 MAC 协议"
  ],
  "explanation": "**Point-to-point 不需要 MAC**：只有两端，没人和谁抢，直接发就行。\n\n**Broadcast 必须 MAC**：多人共享一根线/一片空气，必须协调谁说话。\n\n**现代 Ethernet 实际是 switched (point-to-point)** → 不需要 CSMA/CD。但 WiFi 仍然 broadcast → 仍需 CSMA/CA。"
},

"lec21:7": {
  "title": "Share a Medium — MAC 协议本质",
  "summary": "**问题**: 避免多节点同时说话（碰撞）。**MAC 协议** = 分布式算法分享介质。决定每个节点能否传输。**Q**: 怎么分享？(下页讲)",
  "key_points": [
    "Goal: 避免多节点同时说话",
    "MAC = 分布式算法",
    "每节点决定能否传输",
    "Three categories (下页)"
  ]
},

"lec21:8": {
  "title": "#1: Channel Partitioning",
  "summary": "**TDMA (Time Division Multiple Access)**: 每节点拿固定时隙。**FDMA (Frequency Division)**: 每节点拿固定频段。每轮固定分配，无碰撞，但**轻负载浪费**。",
  "key_points": [
    "**TDMA**: 每节点固定时隙",
    "**FDMA**: 每节点固定频段",
    "**CDMA** (额外): 码分多址（手机系统）",
    "Pro: 无碰撞",
    "Con: 静态分配 → 轻负载浪费"
  ],
  "explanation": "**TDMA 图**：时间切成 round，每 round 有 N 个 slot，每个 slot 给一个节点。\n\n**FDMA 图**：频段切成 N 个子频段，每个节点占一个。\n\n**适用**：负载均匀、稳态可预测时优。\n\n**不适合**：突发 (bursty) 流量。WiFi 流量极突发（一会大下载一会闲），TDMA 会大量浪费 → 所以 WiFi 用 CSMA/CA。\n\n**现代应用**：4G LTE 用 TDMA + FDMA 混合（OFDMA）；GSM 早期用 TDMA。"
},

"lec21:9": {
  "title": "#2: Taking Turns",
  "summary": "**Polling**: Master 轮询每个 worker：『轮到你了，发吗？』。Master 节点是中央协调者。**Token Passing**: 一个 token 在环上传，拿到 token 的节点才能发。\n\n**Cons (共同)**: polling/token overhead、latency、单点故障（master 挂 或 token 丢 → 全瘫）。",
  "key_points": [
    "**Polling**: master 轮询",
    "**Token Passing**: token 环上传",
    "Cons: overhead, latency, single point of failure"
  ],
  "explanation": "**Polling 例**：蓝牙 master-slave。Master（手机）轮询 slave（耳机）。\n\n**Token Ring 例**：1980s IBM 推过的 Token Ring。一个 token 在环上跑，拿到的能发，发完释放。现已绝迹。\n\n**单点故障**：\n- Master 挂 / token 丢 → 全网瘫\n- 需要 leader election 或 token regeneration → 复杂\n\n现代有线网都换成 random access（Ethernet）+ switched 架构，简单 + 高效。"
},

"lec21:10": {
  "title": "How Do You Like These So Far?",
  "summary": "(过渡页) Controlled access 浪费信道（轻负载或 bursty 流量）。**Better idea**: 不避免碰撞，从碰撞中恢复。",
  "key_points": [
    "Controlled access 在 bursty 流量下浪费",
    "Idea: 不避碰，只恢复",
    "下页讲 random access"
  ]
},

"lec21:11": {
  "title": "#3: Random Access Protocol",
  "summary": "**无固定调度，无中央协调**。节点有 data 就以满信道速率发。两个或更多同时发 → **collision**。\n\n**Key components**: (a) 如何检测碰撞？(b) 如何从碰撞恢复？",
  "key_points": [
    "无固定 schedule, 无中央协调",
    "想发就发（at full channel rate）",
    "同时发 → collision",
    "**关键**: (a) 检测碰撞 (b) 恢复"
  ],
  "explanation": "**思想**：『不预约，赶上就用』，效率高于固定分配（轻负载时）。代价是要处理碰撞。\n\n**例**：人多嘴杂的会议室，没有主持人，谁有话说谁说；两人同时说会卡 → 都停下来等几秒再试。"
},

"lec21:12": {
  "title": "Start with the Simplest — ALOHA",
  "summary": "**ALOHA**: Norm Abramson 教授 1970 年发明，夏威夷岛之间的无线 packet 通信网（AlohaNet）。ALOHA 在夏威夷语 = 爱、慰问、再见、你好...",
  "key_points": [
    "Norm Abramson, 1970",
    "First wireless packet radio network",
    "夏威夷岛之间通信",
    "AlohaNet"
  ],
  "explanation": "**历史意义**：第一个分布式 random access 协议。后来的 Ethernet (CSMA/CD)、WiFi (CSMA/CA) 都从 ALOHA 演进。\n\n图片：Abramson 在夏威夷大学（1970s）。"
},

"lec21:13": {
  "title": "Slotted ALOHA — 假设和操作",
  "summary": "**假设**: (1) 时间切等长 slot，每 slot 一 frame；(2) 节点对齐 slot 边界（同步）；(3) 立即能检测碰撞。\n\n**Operations**: (a) 有 data 就发；(b) 无碰撞 → 下个 slot 发新 frame；(c) 碰撞 → 下个 slot 以概率 p 重试。",
  "key_points": [
    "时间切等长 slot",
    "节点同步在 slot 边界发",
    "立即检测碰撞",
    "无碰: 下 slot 发新",
    "碰: 下 slot 以概率 p 重试"
  ]
},

"lec21:14": {
  "title": "Slotted ALOHA — Timeline 例",
  "summary": "图示 3 节点 timeline。每个 slot 中可能：成功（一个发）、空闲（无人发）、碰撞（多人同时发）。碰撞后概率 p 重试。",
  "key_points": [
    "Slot 中三种状态: 成功 / 空闲 / 碰撞",
    "碰撞后概率 p 重发"
  ]
},

"lec21:15": {
  "title": "Slotted ALOHA — 效率推导",
  "summary": "假设 N 节点要发，每个 slot 以概率 p 发。\n\n**单节点 i 成功概率**: S_i = p · (1−p)^(N−1)\n（i 发 + 其他 N-1 个不发）\n\n**任一节点成功**: S = N · p · (1−p)^(N−1)\n\n**最优 p**: 对 S 求导 → p* = 1/N。\n\n**代回**: S_max = (1−1/N)^(N−1) → **1/e ≈ 0.368** as N → ∞。\n\n→ **最大效率仅 ~37%**。",
  "key_points": [
    "P(单 i 成功) = p(1−p)^(N−1)",
    "总吞吐 S = Np(1−p)^(N−1)",
    "对 p 求导: p* = 1/N",
    "S_max → 1/e ≈ 0.368 as N → ∞",
    "**Max efficiency only ~37%**"
  ],
  "explanation": "**完整推导**：\n\n**第一步**: P(节点 i 在某 slot 成功)\n= P(i 发) × P(其他 N-1 不发)\n= p × (1-p)^(N-1)\n\n**第二步**: P(任一节点成功) = N × p × (1-p)^(N-1)\n(N 节点独立加和)\n\n**第三步**: 求 S 对 p 的最大\ndS/dp = N · [(1-p)^(N-1) + p · (N-1)(1-p)^(N-2) · (-1)]\n     = N · (1-p)^(N-2) · [(1-p) − p(N-1)]\n     = N · (1-p)^(N-2) · [1 − Np]\n\n令 = 0 → **p* = 1/N**\n\n**第四步**: 代回\nS* = N · (1/N) · (1−1/N)^(N−1) = (1−1/N)^(N−1)\n\nN → ∞: (1−1/N)^N → 1/e，所以 (1−1/N)^(N−1) ≈ 1/e\n\n→ **S_max ≈ 1/e ≈ 0.368 = 36.8%**\n\n**Pure ALOHA**（不对齐 slot）：碰撞窗口翻倍，max ~18.4% = 1/(2e)。\n\n**考点（高频）**：手推 1/e。考试可能要你推 (1-1/N)^N → 1/e 的极限。",
  "gotcha": "推 (1−1/N)^N → 1/e 用 Taylor 展开或直接记。"
},

"lec21:16": {
  "title": "Slotted ALOHA — Good and Bad",
  "summary": "**Pros**: 简单、单节点独占时全速、高度分布式。**Cons**: 碰撞浪费、空 slot 浪费、需要同步。",
  "key_points": [
    "**Pros**: 简单, 单节点全速, distributed",
    "**Cons**: 碰撞, 空 slot 浪费, 同步需求"
  ]
},

"lec21:17": {
  "title": "Why Slotted ALOHA is Not Enough?",
  "summary": "(过渡页) ALOHA 不听信道，盲发是浪费。**Idea**: 听一下再发？→ 下页 CSMA。",
  "key_points": [
    "ALOHA 盲发",
    "Idea: listen before send",
    "→ CSMA"
  ]
},

"lec21:18": {
  "title": "Listen Before Transmit — CSMA",
  "summary": "**Carrier Sense Multiple Access**: 传输前先**载波感知**。信道闲 → 发；忙 → 推迟。\n\n**Q: 解决问题了吗？**\n**A: No, 还有碰撞**：原因 (a) propagation delay（节点听不到彼此立即）；(b) 也可能 transmitter 听不到自己。",
  "key_points": [
    "Sense before send",
    "Idle → send",
    "Busy → defer",
    "仍可能碰撞 (propagation delay)"
  ],
  "explanation": "**为什么 CSMA 仍碰撞**：\n- A 在 t=0 开始发\n- 信号到 B 处需要 d/c 秒\n- 这 d/c 秒内 B 监听信道是 idle，于是 B 也开始发\n- 两边信号在中间某处碰撞\n\n**propagation delay 的影响**：链路越长，CSMA 越容易碰撞。WiFi 因为还有 hidden terminal 问题，CSMA 远不够，必须 CSMA/CA。"
},

"lec21:19": {
  "title": "CSMA/CD — Collision Detection",
  "summary": "**Carrier sense + collision detection**：边发边监听。一旦检测到碰撞，立即停止 → 减少浪费的传输时间。\n\n**Collision detection easy in 有线 LAN**: 比较 transmitted 和 received signal。**Difficult in wireless**: 发自己信号时 receiver 被自己淹了听不到别人。",
  "key_points": [
    "CSMA + CD: 边发边检测",
    "碰撞 → 立即停 (减少浪费)",
    "有线 CD 容易: 比较 TX/RX 信号",
    "无线 CD 难: TX deafens RX"
  ],
  "explanation": "**有线 CD 怎么实现**：NIC 同时听自己发的 + 监听总信号。如果两者不一致（叠加了别人的）→ collision detected。\n\n**无线为什么 CD 不行**：天线发射功率比接收强 10⁹ 倍，自己耳朵被自己淹了，听不见别人。所以无线只能 collision avoidance（提前避碰，CSMA/CA）。"
},

"lec21:20": {
  "title": "Collision Detection Example",
  "summary": "图示 A 和 D 同时发，B 和 C 处碰撞。B 和 D 都能检测到。**Q: 总能检测吗？** **A: No, 有距离限制**（下页）。",
  "key_points": [
    "Multiple nodes can detect collision",
    "Limits: distance, frame size",
    "下页推导限制"
  ]
},

"lec21:21": {
  "title": "Limits on CSMA/CD Network Length",
  "summary": "**Latency d**: A 发 → 信号到 B 要 d 秒。**B 在 d-ε 时刻**以为 idle 也开始发。**B 立即看到 A 信号但已开始发** → 碰撞。**Distorted waveform 传回 A 还要 d 秒** → **A 最坏 2d 才检测到碰撞**。",
  "key_points": [
    "A→B 信号 latency = d",
    "B 在 d-ε 也开始发（以为 idle）",
    "Signals overlap → collision",
    "Echo back to A 还要 d",
    "**A detects collision in worst case 2d**"
  ],
  "explanation": "**Timeline 详**：\n```\nt=0:   A 开始发\nt=d:   信号到 B；B 在 t=d-ε 那一刻也以为 idle 开始发\nt=d:   B 处碰撞\nt=2d:  碰撞 echo 回到 A\n```\n\n→ A 在 t=2d 时刻才发现自己包碰了。"
},

"lec21:22": {
  "title": "Limits — Min Frame Size + Max Cable Length",
  "summary": "**Min frame size 公式**: A 需等 2d 才能检测碰撞 → frame 持续时间 ≥ 2d → **frame size / R ≥ 2d → frame size ≥ 2dR**。\n\n**IEEE 802.3 Ethernet**: max 2d = 51.2 μs (定值)。\n\n**10 Mbps Ethernet**: min frame = 51.2 μs × 10 Mbps = **512 bit = 64 byte**。Max cable length = 100 m（再长 2d 超 51.2 μs）。",
  "key_points": [
    "Min frame size: frame_time ≥ 2d → L_min ≥ 2d · R",
    "10 Mbps Ethernet: max 2d = 51.2 μs",
    "Min frame = 51.2 μs × 10 Mbps = **512 bit = 64 byte**",
    "Max cable = **100 m**",
    "Min frame 不能更小，max cable 不能更长"
  ],
  "explanation": "**为什么 min frame**：如果 frame 太短，发完才察觉碰撞 → 来不及 abort + 接收端搞不清是数据还是噪声。\n\n**10 Mbps 推导**：\n- max 2d = 51.2 μs（标准规定）\n- min frame = 2d × R = 51.2 μs × 10 Mbps = 512 bit = 64 byte\n- max cable = 100 m\n\n**100 Mbps Fast Ethernet**：同样 51.2 μs → min frame 仍 64 byte → max cable 缩到 10 m（因为信号传得远但 frame 时间短）。现代 switched 后这个不重要了。\n\n**1 Gbps Ethernet**：用 'carrier extension'（填充 0 让 frame 凑 512 byte）维持 min frame 概念。\n\n**考点**：『为什么 Ethernet min frame 64 byte？max cable 100 m？』必答 2d 推导。"
},

"lec21:23": {
  "title": "Key Ideas of Random Access",
  "summary": "**三件套**：(1) **Carrier sense** — 听后说，不打断；(2) **Collision detection** — 检测到碰撞（边发边听信号 garbled）；(3) **Randomness (collision recovery)** — 不立即重试，等随机时间。",
  "key_points": [
    "① **Carrier sense**: 听后说",
    "② **Collision detection**: 检测碰撞",
    "③ **Randomness**: 等随机时间再试"
  ]
},

"lec21:24": {
  "title": "Ethernet — 起源",
  "summary": "Ethernet 起源：1970s Xerox PARC 发明。共享 wired medium。所有 host 一根总线，所有人都能听到所有 frame，地址过滤决定接收。",
  "key_points": [
    "1970s Xerox PARC 发明",
    "Shared wired medium",
    "所有 host 一根总线",
    "广播 + 地址过滤"
  ]
},

"lec21:25": {
  "title": "Ethernet Evolution — Broadcast → Switched",
  "summary": "**Ethernet 进化**：\n- **最初 (broadcast)**: shared bus, CSMA/CD + binary backoff\n- **现代 (switched)**: 每对 host-switch 是 point-to-point full-duplex link\n- **没碰撞**: 每条链路独占，无 CSMA/CD",
  "key_points": [
    "Originally: broadcast, CSMA/CD + binary backoff",
    "Now: **switched**, point-to-point full-duplex",
    "每条 link 独立 collision domain",
    "现代 Ethernet **不用 CSMA/CD**"
  ],
  "explanation": "**Switched Ethernet 优势**：\n- 多对话并发\n- 每条链路独立 collision domain\n- 全双工（同时发收）\n- 高带宽（10 Gbps / 40 Gbps / 100 Gbps）\n\n**CSMA/CD 现在还重要吗**：协议规范里保留，但实际数据中心 / 办公网都是 switched，完全不会触发 CSMA/CD。学这个主要历史 + 理解 collision detection 原理。"
},

"lec21:26": {
  "title": "Ethernet Frame Structure",
  "summary": "**Ethernet frame 字段**:\n- **Preamble** (7 byte): 10101010 × 7，同步 receiver 时钟\n- **SFD** (1 byte): 10101011，frame 开始\n- **Dst MAC** (6 byte): 不匹配就丢\n- **Src MAC** (6 byte)\n- **Type** (2 byte): 上层协议（0x0800=IP, 0x0806=ARP）\n- **Payload** (46-1500 byte)\n- **CRC** (4 byte): 错检",
  "key_points": [
    "**Preamble (7B)** + SFD (1B): 时钟同步",
    "**Dst MAC** (6B): 不匹配丢",
    "**Src MAC** (6B)",
    "**Type** (2B): 0x0800=IP, 0x0806=ARP, 0x86DD=IPv6",
    "**Payload** (46-1500B)",
    "**CRC** (4B): 错检"
  ],
  "explanation": "**Type 字段重要**：让 receiver 知道交给哪个上层协议处理。\n- 0x0800 → IPv4 → 交给 IP\n- 0x0806 → ARP → 交给 ARP\n- 0x86DD → IPv6\n\n**Payload 46-1500**：\n- 上限 1500: MTU\n- 下限 46: 加 header (14B) + CRC (4B) = 64B min frame size（CSMA/CD 推导）\n- payload < 46 时 pad 到 46\n\n**MAC 地址过滤**：NIC 收到 frame，看 dst MAC：\n- 是自己的 → 解析\n- 是 broadcast (FF:FF:FF:FF:FF:FF) → 解析\n- 都不是 → 丢（除非 promiscuous 模式）\n\n**考点**：『Ethernet frame 字段？』必背 7 字段顺序 + 大小。"
},

"lec21:27": {
  "title": "MAC Address",
  "summary": "**6 byte (48 bit)**, 例: 00-15-C5-49-04-A9 (hex)。烧在 adapter 出厂时，唯一。\n\n**Hierarchical allocation**: (a) **Blocks** 由 IEEE 分给 vendors (前 24 bit = OUI)；(b) **Adapter** 由 vendor 自分配 (后 24 bit)。\n\n**Broadcast**: FF-FF-FF-FF-FF-FF。\n\n**Q: MAC vs IP 区别？** (下页详解)",
  "key_points": [
    "6 byte = 48 bit",
    "Format: 00-15-C5-49-04-A9 (hex)",
    "Hierarchical: OUI 24b + adapter 24b",
    "Broadcast: FF×6",
    "Q: MAC vs IP?"
  ],
  "explanation": "**MAC vs IP 对比**（必背）：\n\n| | MAC | IP |\n|---|---|---|\n| 层 | L2 | L3 |\n| 长度 | 6 B | 4 B (v4) |\n| 分配 | 厂商烧网卡 | 用户/DHCP 配 |\n| 结构 | 扁平（不指示位置）| 层级（前缀指示子网）|\n| 范围 | 单 LAN | 全网 |\n| 改变 | 跟着网卡 | 跟着位置 |\n\n**类比**：\n- MAC 像身份证号（一辈子不变，跟着你）\n- IP 像家庭住址（搬家就变）\n\n**考点**：『MAC vs IP？』必备对比。"
},

"lec21:28": {
  "title": "Two Types of MAC Address",
  "summary": "**Burned-in**: 出厂烧硬件，原则上全球唯一。**Effective**: OS 当前用的，可以被 OS 覆盖（**MAC spoofing**）。用于隐私随机化、虚拟化等。\n\n**Network 不依赖 MAC 做 security**（容易被改）。",
  "key_points": [
    "Burned-in: 厂商烧硬件",
    "Effective: OS 用的（可改）",
    "MAC spoofing: 改 MAC 伪装",
    "Used for: 隐私随机化, 虚拟化",
    "网络不靠 MAC 做安全（易伪造）"
  ],
  "explanation": "**为什么 effective MAC 可改**：\n- **隐私**: iOS / Android 现为每个 WiFi 生成随机 MAC，防广告追踪\n- **虚拟化**: VM 需要分配自己的 MAC\n- **MAC spoofing**: 测试 / 攻击场景\n\n**后果**：靠 MAC 做白名单的网络（咖啡馆 WiFi 之类）容易被伪造。真正安全要靠 802.1X / WPA3 之类 L2+ 协议。"
},

"lec21:29": {
  "title": "Bootstrap Communication",
  "summary": "Host 上网两件大事：(a) **DHCP** 拿 IP；(b) **ARP** 找目的 MAC。下面 lec22 详讲这两个。",
  "key_points": [
    "Host 上网 = DHCP + ARP",
    "DHCP: 拿 IP",
    "ARP: IP → MAC"
  ]
},

"lec21:30": {
  "title": "Quiz — BDP 计算（衔接 lec22）",
  "summary": "下次小测：**bandwidth-latency product (BDP)** = bandwidth × RTT。给两段链路：30 Kbps 60m + 4 Mbps 3km。声速 1.5 km/s，光速 3×10⁸ m/s。\n\n**Solve**:\n- 段 1 prop = 60 / 1500 = 40 ms (声速)\n- 段 2 prop = 3000 / 3×10⁸ = 0.01 ms\n- 单程 = 40 + 0.01 ≈ 40 ms\n- **RTT = 80 ms**\n- Bottleneck BW = min(30 Kbps, 4 Mbps) = 30 Kbps\n- **BDP = 30 Kbps × 80 ms = 2400 bits**",
  "key_points": [
    "BDP = bandwidth × RTT",
    "段 1 prop = 60m / 1.5km/s = 40 ms",
    "段 2 prop = 3km / 3×10⁸ m/s = 0.01 ms",
    "RTT = 2 × 40 ≈ 80 ms",
    "Bottleneck BW = min(30K, 4M) = 30 Kbps",
    "**BDP = 30K × 80ms = 2400 bits**"
  ],
  "explanation": "**完整解题步骤**：\n\n1. **每段 propagation delay**:\n   - 段 1: 60 m / 1.5 km/s = 60 / 1500 = 0.04 s = **40 ms**\n   - 段 2: 3 km / 3×10⁸ m/s = 3000 / 3×10⁸ = 10⁻⁵ s = **0.01 ms**\n\n2. **总 propagation (单程)**: 40 + 0.01 ≈ 40 ms\n\n3. **RTT** = 2 × 单程 = **80 ms**\n\n4. **瓶颈带宽**: min(30 Kbps, 4 Mbps) = **30 Kbps**\n\n5. **BDP** = bandwidth × RTT = 30 × 10³ bps × 80 × 10⁻³ s = **2400 bits**\n\n**意义**：管道里能塞 2400 bit。滑动窗口至少要 2400 bit / 8 = 300 byte 才能填满管道。",
  "gotcha": "**别忘 RTT 是 2 倍单程**。题目给的 distance 是单程。"
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
    print(f"lec21 rewrite: overwrote {overwritten}, added {new}")

if __name__ == "__main__":
    main()
