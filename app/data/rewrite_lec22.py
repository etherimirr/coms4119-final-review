#!/usr/bin/env python3
"""Deepen lec22 explanations (switches + intro to wireless)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec22:1": {
  "title": "Quiz — Bandwidth-Delay Product 计算",
  "summary": "BDP = 瓶颈带宽 × RTT。给两段链路（无线 30 Kbps 60m + 有线 4 Mbps 3km），算 BDP。",
  "formula": "$$BDP = R_{\\min} \\times RTT \\approx 2400 \\text{ bits}$$",
  "key_points": [
    "瓶颈带宽 = min(30 Kbps, 4 Mbps) = **30 Kbps**",
    "段 1 prop delay = 60 m / 1.5 km/s = 40 ms（声速）",
    "段 2 prop delay = 3 km / 3·10⁸ m/s = 0.01 ms（光速）",
    "单程 ≈ 40 ms，RTT ≈ 80 ms",
    "BDP = 30 Kbps × 80 ms = 2400 bits"
  ],
  "explanation": "### BDP 是什么\n**Bandwidth-Delay Product** = 带宽 × RTT = 『管道里能塞多少 bit』。这个数告诉你：sender 一次性能发多少 bit 才能把管道填满（不浪费、不溢出）。\n\n### 直觉\n想象一根又细又长的管子。\n- 流量是 30 Kbps（细）\n- RTT 是 80 ms（长）\n- 你能在管子里同时塞 2400 bit\n\n滑动窗口大小要 ≥ BDP 才能填满管道（否则带宽利用不足）。\n\n### 计算步骤（必练）\n1. **瓶颈带宽**：min(各段带宽)\n2. **传播延迟**：每段算 d/v，速度看介质（光速 / 声速）\n3. **RTT** = 2 × 单程（来回各一次）\n4. **BDP** = 瓶颈带宽 × RTT\n\n### 这题的具体数\n- 30 Kbps + 40 ms（段1）+ 4 Mbps + 0.01 ms（段2）\n- 单程 = 40 + 0.01 ≈ 40 ms（段2 propagation 几乎可忽略）\n- RTT = 80 ms\n- BDP = 30,000 × 0.08 = 2400 bits\n\n### 期中已经考过\n期中 Q4 (4) 让你算 cellular link utilization，本质就是 BDP 思维：sender 推得多快、receiver 看到多快、利用率多少。",
  "gotcha": "**RTT 是 2 倍单程延迟**，不要忘了乘 2。题目给的『distance』通常是单程。"
},

"lec22:2": {
  "title": "Who Am I — DHCP 拿 IP 地址",
  "summary": "Host 加入网络第一件事：DHCP 广播『我要 IP』→ server 给一个。",
  "explanation": "### 为什么不能硬编码\n- 移动设备到处跑，每个网络的 IP 段不同\n- 同一个 IP 段下要避免重复\n- 离开后 IP 要还回去重用\n\n手动配置不可扩展，所以有 DHCP。\n\n### 这一页只是引子，详细在下一页\n后面会拆 DHCP 4 步握手（DORA）。"
},

"lec22:3": {
  "title": "DHCP — 还能拿什么",
  "summary": "DHCP 不只给 IP，还给 DNS / 网关 / netmask / 租期。",
  "key_points": [
    "Temporary IP address",
    "Local DNS name server IP",
    "Default gateway (first-hop router) IP",
    "Subnet mask（用来判断目的是不是本子网）",
    "Lease 时长（到期前续约或释放）"
  ],
  "explanation": "### 这几个为什么必须\n- **IP** 不用说\n- **DNS server**：你打开浏览器输 google.com，必须问 DNS server 解析\n- **Gateway**：跨网包要交给 router\n- **Netmask**：判断目的 IP 是否在本子网 → 决定 ARP 谁\n\n→ 没这几个，host 根本上不了网。\n\n### 考法\n『DHCP server 还返回什么除了 IP？』必背 4 样。"
},

"lec22:4": {
  "title": "Need of Address Resolution — 为什么要 ARP",
  "summary": "网卡只懂 MAC，IP 包发出必须先把目的 IP 翻成 MAC。",
  "explanation": "### 链路层 vs 网络层\n- **L3 (IP)**：逻辑地址，跨网\n- **L2 (MAC)**：物理地址，写在网卡上，只在 LAN 内有效\n\nFrame 发送时必须用 MAC（电缆上传的是 frame，frame header 装 dst MAC）。但应用层只知道 IP（浏览器输 URL → DNS → IP）。\n\n→ 必须有个机制把 IP 翻成 MAC。\n\n### 这个机制 = ARP（下一页）"
},

"lec22:5": {
  "title": "ARP — Address Resolution Protocol",
  "summary": "已知 IP，广播『谁的 MAC 是这个 IP？』，目标 unicast 回应。",
  "explanation": "### 流程\n1. Host A 想发包给 IP 1.2.3.6（同子网）\n2. A 查自己的 ARP 表，没找到\n3. A 广播 ARP request：『谁的 MAC 是 1.2.3.6？』，dst = FF:FF:FF:FF:FF:FF（广播 MAC）\n4. LAN 上所有节点收到\n5. 只有 IP=1.2.3.6 的节点 B 回应：『我是，MAC 是 0C-C4-11-6F-E3-98』，**unicast 给 A**\n6. A 把 (1.2.3.6, 0C-C4-...) 存进 ARP 表，TTL 几分钟\n\n### 为什么 reply 是 unicast 不是 broadcast\n省广播流量。A 已经在 request 里给出自己 MAC，B 就 unicast 回去。\n\n### 例题（理解辅助）\n- A 的 IP: 71-65-F7-2B-08-53 → 1.2.3.4\n- DHCP server: 1A-2F-BB-76-09-AD → 1.2.3.x\n- 目标 IP: 1.2.3.6 → 解析 MAC = 0C-C4-11-6F-E3-98"
},

"lec22:6": {
  "title": "ARP 表 + 缓存机制",
  "summary": "每节点维护 ARP 表 (IP, MAC, TTL)，缓存命中直接用，没命中才广播。",
  "key_points": [
    "缓存键 = IP",
    "值 = MAC + TTL（typically 几分钟 - 几十分钟）",
    "TTL 到期清除，下次再查",
    "**Soft state**：靠定期刷新维持"
  ],
  "explanation": "### 为什么要 cache\n如果每次发包都广播 ARP，**链路上一半都是 ARP 流量**。Cache 让常用 IP 的 MAC 直接命中。\n\n### Soft state 的含义\n不需要显式『注销』。Entry 过期自动清，错误（比如对方换了网卡）会因为 TTL 过期自动修复。\n\n### 典型 TTL\nLinux 默认 60 秒（gc_stale_time）。Mac 通常 20 分钟。这些细节不用记。\n\n### 考法\n- 流程：未命中怎么办？\n- 为什么 reply 是 unicast 不是 broadcast？\n- ARP 跟 DHCP 关系？（DHCP 给 IP，ARP 把 IP → MAC）"
},

"lec22:7": {
  "title": "ARP 跨子网 — 解析的是 first-hop router 的 MAC ⭐⭐",
  "summary": "目的 IP 不在本子网时，host ARP 解析的是 default gateway（first-hop router）的 MAC，不是终点 IP。",
  "key_points": [
    "先用 netmask 判断目的是否本子网",
    "本子网 → ARP 目的 IP",
    "跨子网 → ARP 自己 default gateway 的 IP",
    "Router IP 通过 DHCP 拿到（lec22:3）"
  ],
  "explanation": "### 为什么不能直接 ARP 终点 IP\nARP 是 L2 协议，广播只在 **本 LAN** 内有效。终点 IP 在别的子网（甚至别的国家），广播过不去。\n\n所以 host 把包『交给 router』，router 再做下一跳决策。要把包交给 router，必须知道 router 的 MAC → ARP router 的 IP。\n\n### Frame 沿路 MAC 变化\n```\nHost A (1.2.3.48) → Router → ... → Host B (5.6.7.8)\n```\n\n| 段 | Src MAC | Dst MAC | Src IP | Dst IP |\n|---|---|---|---|---|\n| A → R | A 的 MAC | R 的 MAC | A 的 IP | B 的 IP |\n| R → B | R 的下游 MAC | B 的 MAC | A 的 IP | B 的 IP |\n\n**注意**：IP 始终不变（端到端语义），但 MAC 每一跳都变（链路层 hop-by-hop）。\n\n### Host 怎么知道目的不在本子网\n用 netmask：`(dst_IP AND netmask) == (my_IP AND netmask)`？\n- 是 → 同子网，ARP 终点 IP\n- 否 → 跨子网，ARP 自己 default gateway\n\n### 考法（高频）\n『1.2.3.48 要发包给 5.6.7.8，它 ARP 谁？』\n答：先用 netmask 算出 5.6.7.8 不在本子网，所以 ARP **自己 default gateway**（比如 1.2.3.19）的 MAC，不是 5.6.7.8 的 MAC。",
  "gotcha": "**典型错误**：以为 ARP 直接找终点 IP 的 MAC。永远记得 ARP 是 L2，跨 L2 必须经 router。"
},

"lec22:8": {
  "title": "ARP & DHCP 三大设计思想",
  "summary": "Broadcasting + Caching + Soft state — 网络协议的通用范式。",
  "key_points": [
    "**Broadcasting**：用广播做首次发现（限制：广播域要有限大小）",
    "**Caching**：学到的存起来减少重复 overhead",
    "**Soft state**：带 TTL，到期就忘 → 容错"
  ],
  "explanation": "### 这三条是网络系统设计的『万金油』\n- DHCP 广播 Discover；ARP 广播 query → **broadcasting**\n- ARP 缓存 IP→MAC；DNS 缓存域名解析 → **caching**\n- 都带 TTL，到期重学 → **soft state**\n\n### Soft state vs Hard state\n- **Hard state**：必须显式注册 / 注销（比如 telnet 会话）\n- **Soft state**：到期自动清，更容错，是 Internet 的设计哲学之一\n\n### 考法\n选择题：『ARP / DHCP 用了什么设计原则？』→ 三个都中。"
},

"lec22:9": {
  "title": "802.3 Ethernet 标准 — 速度家族",
  "summary": "共同的 MAC 协议 + frame 格式，不同速度 + 不同物理层（光纤、铜线）。",
  "key_points": [
    "速度从 2 Mbps 到 80 Gbps",
    "命名：100BASE-TX = 双绞铜线 100 Mbps；100BASE-FX = 光纤 100 Mbps",
    "MAC 和 frame 格式完全相同（兼容）",
    "物理层不同"
  ]
},

"lec22:10": {
  "title": "Switches — 链路层设备",
  "summary": "Switch 转发 Ethernet frame，按 dst MAC 选 port。Plug-and-play 自学习。",
  "key_points": [
    "Store-and-forward",
    "看 incoming frame 的 dst MAC 决定出 port",
    "Plug-and-play：不需要配置",
    "自学习填表（下页详解）"
  ],
  "explanation": "### Switch vs Hub\n- **Hub**（老旧）：所有 port 同一个 collision domain，物理层广播\n- **Switch**：每 port 独立 collision domain，按 MAC 智能转发\n\n现在『Hub』基本绝迹，所有都是 Switch。\n\n### Switch vs Router（详见 p18）\n两者都 store-and-forward，但层不同：\n- Switch: L2, 看 MAC\n- Router: L3, 看 IP\n\n### 自学习是 switch 的核心特性\n下一页详细讲。"
},

"lec22:11": {
  "title": "Switch — 多路并发能力",
  "summary": "Host 到 switch 是点对点链路 → 全双工 → 多条对话同时进行不碰撞。",
  "key_points": [
    "每条接入链路独立 collision domain",
    "全双工（同时发收）",
    "Switch 内部 buffer 包",
    "**唯一限制**：同一目标的多个 sender 会在 buffer 排队"
  ],
  "explanation": "### Switch 怎么解决 CSMA/CD 的瓶颈\n传统 broadcast Ethernet 所有 host 一根线 → 同时只能一个发，效率低。\n\nSwitch 让每个 host 都用 dedicated link 连进来 → 多条对话并发：\n- A→A'\n- B→B'\n- C→C' 同时进行，不打架\n\n**唯一不行的**：A→A' 和 C→A' 不能同时（同一个 receiver A'）→ switch 会在 buffer 里排队。\n\n### 这一页要传达的\nSwitched Ethernet 是『现代有线网』的核心实现，几乎没有 CSMA/CD 了。"
},

"lec22:12": {
  "title": "Switch Forwarding Table — 数据结构",
  "summary": "每个 entry = (host MAC, 哪个 port 能到, timestamp)。",
  "explanation": "**像路由表但更简单**：路由表查 IP，转发表查 MAC。两者都 destination-based forwarding。\n\nTimestamp 用于 entry 老化（『多久没看到这个 MAC』）。\n\n### 例\n收到一帧 (src=A, dst=A')。Switch 查表：\n- 找到 A' → 直发那个 port\n- 没找到 → flood 所有 port（除入口）"
},

"lec22:13": {
  "title": "Switch Self-Learning ⭐",
  "summary": "Switch 不需要配置，靠 frame 流量自动学：见 frame → 记 (src MAC, in-port, TTL)。",
  "key_points": [
    "收到 frame → 记 (src MAC, in-port, TTL)",
    "Dst MAC 在表 → 单口发",
    "Dst MAC 不在表 → flood 除入口外所有 port",
    "TTL 到期自动清",
    "Plug-and-play"
  ],
  "explanation": "### 完整时序例（必须能复述）\n\n初始 switch table 空。Host A 第一次发给 A'（端口约定：A 在 port 1, A' 在 port 4）：\n\n```\n时刻 1: A 发 frame (src=A, dst=A')\n  Switch 看到 frame 从 port 1 进来 → 记 (A, 1, TTL=60)\n  查 dst=A'，没找到 → flood 到 port 2, 3, 4, 5, 6\n\n时刻 2: A' 收到，回 frame (src=A', dst=A)\n  Switch 看到 frame 从 port 4 进来 → 记 (A', 4, TTL=60)\n  查 dst=A，找到在 port 1 → 单口发到 port 1\n\n时刻 3+: A → A' 的 frame 都能直接 port 4，不再 flood\n```\n\n### 为什么能 self-learn\n关键观察：**frame 的 src MAC 是免费信息**。Switch 看到 frame 从 port 1 进来，就知道 src 那个 host 通过 port 1 可达。\n\n### TTL\nMAC table entry 自然老化，比如几分钟没看到流量就清除。这样换接口 / 新设备进来都能自动更新。\n\n### 考法\n给 timeline 帧序列，问每一步 switch table 长什么样。一定要会画。",
  "gotcha": "**flooding 不发到入口 port**（否则就回环了）。Switch 永远不会把 frame 从它进来的那个 port 再发出去。"
},

"lec22:14": {
  "title": "VLAN — Virtual LAN 动机",
  "summary": "大 LAN 广播流量太多 + 用户搬位置后想保留逻辑归属 → 把物理 switch 切成多个虚拟 LAN。",
  "explanation": "### 大 LAN 的问题\n所有 ARP、DHCP discovery、unknown MAC flood 在整个 LAN 上广播。LAN 越大，广播流量越呛：\n- 1000 个 host 各每分钟 1 个 ARP → 每秒 ~17 个广播\n- 还有 DHCP / IPv6 NDP / mDNS / ...\n\n### 行政诉求\nCS 部门员工临时调到 EE 工作，物理插到 EE 的 switch，但想保留 CS 网络访问权限（CS 内部服务器、文件夹）。\n\n### 解药：VLAN\n用 VLAN 配置把 switch 切成多个虚拟 LAN，**每个 VLAN 是独立的广播域**。"
},

"lec22:15": {
  "title": "VLAN — 行政场景再举例",
  "summary": "CS 用户搬到 EE，想保留 CS LAN 访问 → VLAN 实现物理 ≠ 逻辑分离。"
},

"lec22:16": {
  "title": "Port-based VLAN — 配置方式",
  "summary": "把 switch ports 分到多个 VLAN，每个 VLAN 等效为一台独立 switch。",
  "key_points": [
    "Port 划分（最简单）：port 1-8 = VLAN A, port 9-16 = VLAN B",
    "或 MAC 划分：按 MAC 决定 VLAN",
    "Frame 默认不跨 VLAN（除非走 router）"
  ]
},

"lec22:17": {
  "title": "Port-based VLAN — 隔离 + 灵活分配 ⭐",
  "summary": "VLAN 提供 traffic isolation + 动态成员变更。跨 VLAN 必须 router。",
  "key_points": [
    "**Traffic isolation**：VLAN A 的 frame 进不了 VLAN B（包括 broadcast）",
    "**Dynamic membership**：port 随时可以重分配 VLAN",
    "**跨 VLAN** → 必须走 router（不只 switch）"
  ],
  "explanation": "### 为什么跨 VLAN 必须 router\nVLAN 划分在 L2，router 在 L3。Switch 看到 frame 的 VLAN tag 后只在同 tag 内转发；跨 VLAN 等于 frame 进到一个新的 L2 域，需要 L3 设备（router）解包 → 重新 frame → 发到新 VLAN。\n\n### VLAN trunk\n两台 switch 之间的链路要承载多个 VLAN 的流量时，frame 加 VLAN tag（802.1Q），叫 trunk 链路。\n\n### 考法\n『为什么 VLAN？』→ 隔离 + 安全 + 灵活。\n『跨 VLAN 怎么通？』→ router。"
},

"lec22:18": {
  "title": "Router vs Switch — 对比表 ⭐⭐",
  "summary": "都是 store-and-forward；router 看 IP（L3），switch 看 MAC（L2）。",
  "key_points": [
    "Router: L3, 看 IP, 跑路由算法 (OSPF/BGP)",
    "Switch: L2, 看 MAC, 自学习",
    "Router 跨网络，switch 单 LAN",
    "Router 减 TTL，switch 不动"
  ],
  "explanation": "### 完整对比表（必须能默写）\n\n| | Router | Switch |\n|---|---|---|\n| **层** | L3 (网络层) | L2 (数据链路层) |\n| **看什么** | dst IP | dst MAC |\n| **表来源** | 路由协议（OSPF/BGP）或 SDN | **自学习**（src MAC → in-port）|\n| **范围** | 跨网（router connects networks） | 单 LAN（switch within one network）|\n| **TTL** | 每跳 −1，0 就丢 | 不碰 IP 字段 |\n| **packet 视角** | 拆 frame → 解 IP → 重新封 frame | 转发整个 frame |\n| **目的找不到** | drop（带 ICMP） | flood |\n| **失败重传** | ICMP destination unreachable | 不负责 |\n\n### 一句话区分\n『看到 IP 段不同（跨子网）→ router；同一 LAN 内点对点 → switch。』\n\n### 考法（高频）\n给一个网络拓扑，问『这一跳该用 router 还是 switch？』看是否跨子网。"
},

"lec22:19": {
  "title": "Wireless Physical Layer & MAC（章节封面）",
  "summary": "进入无线章节。"
},

"lec22:20": {
  "title": "My Goals — 这章学什么",
  "summary": "无线物理基础 + 无线 MAC 协议 + 暴露你看一些前沿研究。"
},

"lec22:21": {
  "title": "Wireless Networks — 三层范围",
  "summary": "WPAN / WLAN / WWAN — 按地理范围划分。",
  "key_points": [
    "**WPAN**（Personal Area）：Bluetooth, Zigbee, RFID — 厘米到米",
    "**WLAN**（Local Area）：WiFi (802.11), mesh — 数十米",
    "**WWAN**（Wide Area）：Cellular, WiMAX — 公里"
  ]
},

"lec22:22": {
  "title": "Radio Propagation 101 — 子节开始",
  "summary": "下面几页探讨无线信号怎么传播 → 为后面 MAC 设计铺垫。"
},

"lec22:23": {
  "title": "If We Could See WiFi Signals (1) — 可视化",
  "summary": "讲师用艺术家可视化 WiFi 信号的图片激励大家。"
},
"lec22:24": { "title": "WiFi 可视化 (2)", "summary": "继续 WiFi 信号可视化。" },
"lec22:25": { "title": "WiFi 可视化 (3)", "summary": "继续。" },
"lec22:26": { "title": "WiFi 可视化 (4)", "summary": "继续。" },

"lec22:27": {
  "title": "What Happens After We Cut the Wire?",
  "summary": "断掉电缆后信号在空气里到处飞 → 引出 path loss + 多径 + 干扰等问题。"
},

"lec22:28": {
  "title": "Free-Space Pathloss 公式 ⭐",
  "summary": "信号功率随距离 d² 衰减；频率越高 loss 越大。",
  "formula": "$$L = \\left(\\frac{4\\pi d}{\\lambda}\\right)^2 = \\left(\\frac{4\\pi d f}{c}\\right)^2$$",
  "key_points": [
    "d = 距离（米）",
    "λ = 波长（米）",
    "f = 频率（Hz）",
    "c = 光速 3×10⁸ m/s",
    "f 大 → λ 小 → loss 大"
  ],
  "explanation": "### 直觉\n点光源把光均匀辐射到一个球面上。球面积 = 4πd²，所以单位面积接收到的功率 ∝ 1/d² → 距离加倍，功率 ÷4 = **−6 dB / 加倍距离**。\n\n### 为什么频率高 loss 大\n看公式，f 在分子。物理上：高频 → 短波长 → 天线有效面积 ∝ λ² → 接收同样能量需要更大天线（或牺牲距离）。\n\n### 频段对比\n| 频段 | λ | 特点 |\n|---|---|---|\n| 900 MHz | 33 cm | 远距 + 穿墙好 + 带宽窄 |\n| 2.4 GHz | 12 cm | 中距 + 中等穿墙 + 带宽 83.5 MHz |\n| 5 GHz | 6 cm | 近距 + 穿墙差 + 带宽 200 MHz |\n\n这是为什么 5 GHz WiFi 速度快但需要靠近路由器，2.4 GHz 在屋外也能用但慢。\n\n### 考法\n- 给 d、f 算 loss（dB 单位下：10·log(loss)）\n- 解释 5GHz vs 2.4GHz 哪个穿墙好",
  "gotcha": "实际环境 loss 比公式快得多（α=2 只在外太空准确），实际用 PL(d) = PL(d₀) + 10α·log(d/d₀)。下页讲。"
},

"lec22:29": {
  "title": "Pathloss — 频段表",
  "summary": "不同 WiFi 频段的范围、波长、带宽对比。",
  "key_points": [
    "900 MHz: λ=0.33 m, 26 MHz 带宽",
    "2.4 GHz: λ=0.125 m, 83.5 MHz 带宽",
    "5 GHz: λ=0.06 m, 200 MHz 带宽"
  ]
},

"lec22:30": {
  "title": "Pathloss with exponent α ⭐",
  "summary": "实际环境 loss ∝ d^α，α 通常 2-6（不是自由空间的 2）。",
  "formula": "$$\\text{loss} \\propto \\left(\\frac{4\\pi d f}{c}\\right)^\\alpha$$",
  "key_points": [
    "Free space α = 2",
    "城市 α = 2.7 - 3.5",
    "城市阴影 α = 3 - 5",
    "室内阻挡 α = 4 - 6",
    "工厂 α = 2 - 3"
  ],
  "explanation": "### α 的物理意义\n衡量信号衰减速度。α=2 表示『每加倍距离 −6 dB』。α=4 表示『每加倍 −12 dB』，衰得快。\n\n### 实际 vs 理论\n自由空间公式假设无障碍。现实有墙、地面、家具，每经过一次反射 / 衍射都吃掉一些能量 → α 比 2 大很多。\n\n### 怎么用 α 算实际 loss\nPL(d) = PL(d₀) + 10α · log(d/d₀) + X\n- PL(d₀): 参考距离的 loss（如 1 m 处）\n- α: 环境决定\n- X: 阴影随机项（log-normal）\n\n### 例\n参考 1 m 处 loss = 40 dB，α=3，d=10 m：\nPL = 40 + 10×3×log(10/1) = 40 + 30 = **70 dB**（再加随机阴影项）。\n\n### 考法\n给 α、d 算 loss；判断环境对应哪个 α。"
},

"lec22:31": {
  "title": "Physics of Radio Propagation — 进入反射 / 衍射 / 散射",
  "summary": "下一章 lec23 开头介绍三种传播现象。"
},

}

def main():
    data = json.loads(DETAIL.read_text())
    data.update(NEW)
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"updated {len(NEW)} entries; total now {len(data)}")

if __name__ == "__main__":
    main()
