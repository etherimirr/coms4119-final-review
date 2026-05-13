#!/usr/bin/env python3
"""Deepen lec17, lec16, lec14 explanations."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

# ============= lec17 =============
"lec17:1": {
  "title": "Midterm Grades — 这次成绩分布",
  "summary": "Median 50, Mean 49.55, Max 90, Min 7。你 52 略高于均值。"
},
"lec17:2": { "title": "Network Layer Roadmap (data plane)", "summary": "Router 内部 → IP → 通用 forwarding → middleboxes。" },
"lec17:3": {
  "title": "Network Layer Internet 三大组件",
  "summary": "IP + ICMP + Routing 算法。",
  "key_points": [
    "**IP protocol**: datagram 格式、寻址、packet handling",
    "**ICMP**: 错误报告、router 信号 (ping, traceroute)",
    "**Routing algorithms**: OSPF、BGP、SDN"
  ]
},
"lec17:4": {
  "title": "IPv4 Datagram 格式 ⭐⭐",
  "summary": "32 bit wide，20 B 基础 header；各字段含义。",
  "key_points": [
    "**ver(4)** | **hlen(4)** | **ToS(8)** | **total length(16)**",
    "**identifier(16)** | **flags(3)** | **frag offset(13)** — 分片",
    "**TTL(8)** | **upper-layer protocol(8)** | **header checksum(16)**",
    "**32-bit src IP**",
    "**32-bit dst IP**",
    "**options**（可变）",
    "**payload**（典型 TCP/UDP segment）"
  ],
  "explanation": "### 重点字段逐个看\n\n**Version (4 bit)**：0100 = IPv4，0110 = IPv6。Router 看这个决定怎么解。\n\n**HLEN (4 bit)**：以 4 字节为单位。没 options 时 hlen=5 → header 20 B。最大 hlen=15 → 60 B。\n\n**ToS (8 bit)**：分两部分：高 6 位 diffserv（QoS 标记）；低 2 位 ECN（拥塞通知）。\n\n**Total length (16 bit)**：包括 header + payload，单位字节。最大 64 KB。实际通常 ≤ MTU (1500)。\n\n**Identifier + Flags + Frag Offset**：分片用。MTU 大的 IP 包要切成几小段，每段同 identifier，flags 标 'more fragments'，offset 说位置。\n\n**TTL (8 bit)**：每跳 -1，到 0 路由器 drop。防环 + 防包永远循环。初始通常 64 或 128。\n\n**Protocol (8 bit)**：6 = TCP, 17 = UDP, 1 = ICMP, 89 = OSPF。Receiver 用这个 demux 到上层协议。\n\n**Header Checksum (16 bit)**：只对 header（不含 payload）。每跳 TTL 变 → checksum 也得重算。IPv6 去掉了这个字段省 CPU。\n\n**Src/Dst IP (32 bit each)**：端到端不变。\n\n### TCP/IP overhead\nTCP header 20 B + IP header 20 B = 40 B overhead/packet（不含 application 数据）。所以小包（如 DNS 查询）效率低。\n\n### 考法\n- 选择题问字段含义\n- TTL 计算（traceroute 原理）\n- 算 overhead"
},
"lec17:5": {
  "title": "IP Addressing 介绍",
  "summary": "32 bit ID 关联到 interface（不是 host！）。Router 多接口，host 通常 1-2 个。",
  "key_points": [
    "IP 关联到 **interface**（不是 host）",
    "Router 有多个接口（每个不同子网）",
    "Host 通常 1-2 个（有线 + 无线）",
    "点分十进制：223.1.1.1 = 11011111 00000001 00000001 00000001"
  ],
  "explanation": "### 重要：IP 是接口的，不是主机的\n一台 router 同时连 3 个子网 → 它有 3 个 IP（每个接口一个）。一台笔记本同时连有线 + WiFi → 它有 2 个 IP。\n\n这个细节在画拓扑时容易搞错。"
},
"lec17:6": { "title": "IP Addressing 介绍（续）", "summary": "Interface 物理上由 Ethernet switch / WiFi base station 连接。" },
"lec17:7": { "title": "IP Addressing — 同子网定义", "summary": "同子网 = 不经 router 互通的接口集合。" },

"lec17:8": {
  "title": "Subnet 定义 ⭐",
  "summary": "Subnet = 一组能直接互通（不经 router）的接口。IP 分子网部分（高位）和主机部分（低位）。",
  "key_points": [
    "同子网 = 不经 router",
    "Subnet 部分 = 共同高位",
    "Host 部分 = 不同低位",
    "Subnet mask 决定『高位多长』"
  ],
  "explanation": "### 直觉\n类比地址：『纽约 - 哥大 - 408 号房』，前两个相同是同一栋楼（同子网），房间号区分。\n\n### 为什么需要子网概念\n- 同子网内可以直接 L2 通信（ARP + Ethernet）\n- 跨子网必须 L3 经 router\n- Routing 表大幅缩小（不需要每台主机一条规则，只需要每个子网一条）"
},

"lec17:9": { "title": "Subnets — 分子网食谱", "summary": "断开每个 router 接口 → 形成的孤岛 = 一个 subnet。" },
"lec17:10": { "title": "Subnets — 找子网练习", "summary": "给一个拓扑识别其中的子网。" },

"lec17:11": {
  "title": "CIDR — Classless InterDomain Routing ⭐",
  "summary": "a.b.c.d/x 表示前 x 位是 subnet 部分。打破老的 class A/B/C 固定边界。",
  "key_points": [
    "格式：a.b.c.d/x，x = 0-32",
    "/24 = 256 个地址（前 24 位 subnet）",
    "/16 = 65536 个地址",
    "Mask = x 个 1 + (32-x) 个 0",
    "Prefix = IP AND mask"
  ],
  "explanation": "### 老的 class 系统\n- Class A: /8 (16M 个地址)\n- Class B: /16 (65K)\n- Class C: /24 (256)\n\n固定边界导致浪费：要 500 个地址只能拿一个 Class B（65K，浪费 99%）。\n\n### CIDR 让 mask 长度任意\n要 500 个地址 → /23 (512 个) 刚刚好。\n\n### 路由聚合\nISP 拿 /20（4096 个），切给 8 个组织 /23（512 个）。对外只 advertise /20，路由表大幅缩小。"
},

"lec17:12": { "title": "IP 地址获取 — 两个问题", "summary": "Host 怎么拿 IP？Subnet 怎么拿地址？" },
"lec17:13": { "title": "DHCP 介绍", "summary": "Host 加入网络动态拿 IP。可续租、地址复用、plug-and-play。" },
"lec17:14": { "title": "DHCP 场景 1", "summary": "Host 加入子网拿 IP，DHCP server 通常在 router 上。" },

"lec17:15": {
  "title": "DHCP 场景 2 — DORA 全流程 ⭐⭐",
  "summary": "Discover → Offer → Request → Ack，全部广播。",
  "key_points": [
    "**Discover** (src 0.0.0.0:68 → dst 255.255.255.255:67, broadcast)",
    "**Offer** (server: yiaddr 候选 IP + lease)",
    "**Request** (client 选择候选 IP)",
    "**Ack** (server 确认绑定)"
  ],
  "explanation": "### 为什么全部广播\nClient 还没有 IP，无法 unicast。只能广播让任何在 LAN 上的 DHCP server 听到。\n\n### 为什么需要 4 步而不是 2 步\n- 多 server 场景：一个 LAN 可能有多个 DHCP server（冗余）。Client 可能收到多个 offer，必须用 Request 明确选一个 → 其他 server 释放保留的 IP。\n- 一个 server 场景下也保留 4 步流程（统一）。\n\n### 短路：续租\nRFC 2131 允许 client 跳过 Discover/Offer，直接 Request 上次用过的 IP。Server ACK 就续上。\n\n### 字段\nyiaddr (your IP address) = server 给 client 的 IP。\ntransaction ID 让 client 匹配 reply。\n\n### 考法\n『DHCP 4 步是什么？』必背 DORA 顺序。\n『为什么 Discover 用广播？』→ client 没 IP，无法 unicast。"
},

"lec17:16": {
  "title": "DHCP 还给什么 ⭐",
  "summary": "除 IP 还给：first-hop router (default gateway), DNS server, netmask, lease 时长。",
  "key_points": [
    "**IP address**",
    "**Default gateway** (first-hop router IP)",
    "**DNS server IP**",
    "**Subnet mask** (用来判断目的是否本子网)",
    "**Lease time**"
  ],
  "explanation": "### 为什么这几个必须\n这四样一起决定 host 能不能正常上网：\n\n1. **IP**：自己的身份，没它发不出包\n2. **Gateway**：跨网包要交给 router；如果不知道 router IP，跨子网完全废\n3. **DNS server**：打开浏览器输 google.com 要解析\n4. **Netmask**：判断目的是不是同子网 → 决定 ARP 谁\n\n### 没 mask 会怎样\nHost 看到目的 IP 1.2.3.4，不知道是不是本子网。试图 ARP 1.2.3.4 → 如果不在本子网 LAN 上广播没人回 → 永远连不上。\n\n### 考法\n『DHCP server 还能返回什么？』必背 4 个加 lease。"
},

"lec17:17": { "title": "DHCP 例 (1) — 协议栈封装", "summary": "DHCP / UDP / IP / Ethernet 封装；Ethernet 广播。" },
"lec17:18": { "title": "DHCP 例 (2) — 应答路径", "summary": "DHCP server 通过 router 返回 ACK，反向解 demux 到 client。" },
"lec17:19": { "title": "IP 地址获取 — Subnet 部分", "summary": "Subnet 从 ISP 拿一段；ISP 从 ICANN/RR 拿。" },

"lec17:20": {
  "title": "Hierarchical Addressing — 路由聚合 ⭐",
  "summary": "ISP 拿一大块 (/20)，切给 8 个组织各 /23。对外只 advertise /20 → 路由表大幅缩小。",
  "key_points": [
    "ISP 拿 200.23.16.0/20 (4096 地址)",
    "切给 Org 0-7，各 /23 (512 地址)",
    "对 Internet 只 advertise /20（一条规则）",
    "**省路由表 + 省 BGP 更新流量**"
  ],
  "explanation": "### 没聚合 vs 有聚合\n没聚合：ISP 把 8 个 /23 都向外 advertise → Internet 路由表多 8 条。\n聚合：ISP 只 advertise 1 个 /20 → 外面路由表只多 1 条。\n\n外网路由器知道『去 200.23.16.0/20 走 ISP A』就够了，不需要管内部细分。包到 ISP A 后再用更具体的 /23 决定到哪个 Org。\n\n### 路由表条目数\nInternet 现在 BGP 全表 ~100 万条。如果没聚合可能要 1 亿条 → 路由器内存撑不住。\n\n### 考法\n『为什么 hierarchical addressing？』必答路由聚合 + scalable。"
},

"lec17:21": { "title": "IP Addressing — Last Words", "summary": "ICANN 分配；IPv4 2011 用完；IPv6 128 bit 足够长。" },
"lec17:22": { "title": "Data Plane Roadmap — NAT", "summary": "进入 NAT。" },

"lec17:23": {
  "title": "NAT — Network Address Translation ⭐⭐",
  "summary": "局域网共用一个公网 IP；NAT router 改写 (src IP, src port)。",
  "key_points": [
    "局域网用私有 IP（10/8, 172.16/12, 192.168/16）",
    "对外只看到 NAT router 的公网 IP",
    "NAT router 改 src 字段 + 记 NAT 表",
    "回程改回 dst 字段"
  ],
  "explanation": "### 历史背景\n2000 年代 IPv4 地址不够用，但每户家庭/小公司都要联网 → NAT 让一个公网 IP 服务整个家。\n\n### 私有 IP 段\n- 10.0.0.0/8（大型企业）\n- 172.16.0.0/12（中型）\n- 192.168.0.0/16（家用最常见）\n\n这些 IP 在公网上是不可路由的（路由器看到这些 src/dst 会直接 drop）。\n\n### 工作流程\n```\n[10.0.0.1:3345] → [NAT 138.76.29.7:5001] → [128.119.40.186:80]\n                       ↑\n                NAT 改 src，记表\n```\n\n回程：\n```\n[128.119.40.186:80] → [138.76.29.7:5001] → 查 NAT 表 → [10.0.0.1:3345]\n```"
},

"lec17:24": {
  "title": "NAT — 优点",
  "summary": "省 IP、对外透明、换 ISP 不变 host 配置、安全（外人看不到内网 host）。",
  "key_points": [
    "只需 1 个公网 IP 给整个 LAN",
    "LAN 内 host 改 IP 对外透明",
    "换 ISP 只换 NAT 公网 IP，LAN 不变",
    "外部 host 无法主动连到 LAN 内（除非 port forwarding）→ 一种粗糙的防火墙"
  ]
},

"lec17:25": {
  "title": "NAT 实现 — 流程",
  "summary": "出包改 src 记表；入包查表改 dst。",
  "explanation": "### NAT 表结构\n```\nLAN side          WAN side\n(10.0.0.1, 3345) ↔ (138.76.29.7, 5001)\n(10.0.0.2, 4587) ↔ (138.76.29.7, 5002)\n...\n```\n\n### 出包改 src\nClient 发 (src=10.0.0.1:3345, dst=128.119.40.186:80)\nNAT 改成 (src=138.76.29.7:5001, dst=128.119.40.186:80)，记表。\n\n### 入包改 dst\nServer 回 (src=128.119.40.186:80, dst=138.76.29.7:5001)\nNAT 查表找到 5001 → 10.0.0.1:3345\n改成 (src=128.119.40.186:80, dst=10.0.0.1:3345)，发给 client。\n\n### Port 怎么选\nNAT 通常用一个递增的 port pool（从 5000 起跳）。每条连接分配不同 port。"
},

"lec17:26": { "title": "NAT 实例图 ⭐", "summary": "完整路径图：10.0.0.1:3345 ↔ NAT ↔ 128.119.40.186:80。" },

"lec17:27": {
  "title": "NAT — 争议",
  "summary": "违反端到端原则；阻碍 P2P / server；IPv6 才是治本但部署慢。",
  "key_points": [
    "Router 应该只看 L3，但 NAT 也改 L4 (port) → **违反 layering**",
    "外部无法主动连入 → 阻碍 P2P (Skype, BitTorrent) 和 self-hosted server",
    "**NAT traversal**: STUN, TURN, UPnP（复杂的 workaround）",
    "IPv6 解决问题但部署慢"
  ],
  "explanation": "### NAT traversal 简介\n- **STUN**: 让 NAT 后的 host 知道自己对外的 (IP, port)\n- **TURN**: 用中继 server 转包（NAT-NAT 通信）\n- **ICE**: 协调 STUN + TURN\n- **UPnP**: 让 NAT 自动配 port forwarding（家庭 router 用）\n\n这些方案让 Skype / WebRTC 等能在 NAT 后工作，但增加复杂度。\n\n### 考法\n『NAT 优缺点？』必背 + 知道 NAT traversal 概念。"
},

"lec17:28": {
  "title": "Quiz — 最长前缀匹配 ⭐",
  "summary": "3 条规则带 *，packet dst=1010.1000.0100.1000 → 走哪个 port？",
  "key_points": [
    "规则 1: 1010.xxxx.xxxx.xxxx (/4) → Port 2",
    "规则 2: 10xx.xxxx.xxxx.xxxx (/2) → Port 1",
    "规则 3: 1010.11xx.xxxx.xxxx (/6) → Port 3"
  ],
  "explanation": "### 解题步骤\n\n包 dst = `1010.1000.0100.1000`（用 . 分组方便看）\n\n**对比规则 1** (1010.xxxx, /4)：前 4 位 1010 == 1010 ✓ → 匹配\n\n**对比规则 2** (10xx.xxxx, /2)：前 2 位 10 == 10 ✓ → 匹配\n\n**对比规则 3** (1010.11xx, /6)：前 4 位 1010 == 1010 ✓；位 5-6 应该是 11，但包是 1000.xxxx 的前 2 位 = **10**，不是 11 ✗ → 不匹配\n\n**匹配的规则**：1 (/4) 和 2 (/2)。\n\n**最长**：/4 > /2 → 选规则 1 → **Port 2**\n\n### 必练这种题\n期末样题里就有 LPM 题。做题套路：\n1. 数清每条规则的前缀位数\n2. 逐位比对，看哪些匹配\n3. 选最长的（即前缀位数最多的）",
  "gotcha": "**1010.11 ≠ 1010.10**：注意位的具体值。位 5、6 必须是 11 才匹配规则 3。"
},


# ============= lec16 =============
"lec16:1": { "title": "ECN（lec14 末尾复习）", "summary": "路由器在 IP 头打 2 bit ECN 标记；receiver 经 ACK 回传 ECE=1；sender 不丢包就减半。" },

"lec16:2": {
  "title": "TCP Fairness — 目标",
  "summary": "K 个 TCP 共享带宽 R，理想每个 R/K。",
  "explanation": "### 公平的含义\n如果有 K 个长期跑 CA 的 TCP session 共享同一个 bottleneck，每个『应该』拿到 R/K。\n\n实际中：\n- 不同 RTT 的 session 会不公平（短 RTT 抢得多）\n- UDP 不做 CC 占用更多\n- 并行 TCP 一个用户开多条赢更多\n- 这些都在『理论公平』之外"
},

"lec16:3": {
  "title": "TCP 公平不公平？⭐",
  "summary": "AIMD + 相同 RTT + 长期 CA → 理论上收敛到公平。",
  "explanation": "### 完整论证\nAIMD 的几何收敛：加法走 45°（向效率线），乘法沿原点缩（保比例 + 向公平线靠）。两步交替 → 螺旋收敛到 fair line × efficiency line 交点。\n\n### 前提（必须强调）\n1. 相同 RTT（不然短 RTT 的赢）\n2. 都长期在 CA（不是反复 slow start）\n3. Session 数固定（动态加入 / 退出会扰动）\n4. AIMD（不是 AIAD / MIMD）"
},

"lec16:4": {
  "title": "公平性 — UDP / 并行 TCP 破坏 ⭐",
  "summary": "UDP 不做 CC 任意抢；浏览器并行 TCP 拿多份。",
  "key_points": [
    "**UDP 多媒体**：不愿被 CC 减速，所以用 UDP",
    "**并行 TCP**：浏览器开 K 条 TCP → 自己拿 K/(K+others) 份",
    "**没 Internet 警察**"
  ]
},

"lec16:5": { "title": "TCP — 研究热点", "summary": "TCP 改进至今仍是活跃研究。" },
"lec16:6": { "title": "TCP — 论文列表（续）" },

"lec16:7": { "title": "Network Layer — 章节封面", "summary": "进入 Network Data Plane。" },
"lec16:8": { "title": "协议栈位置", "summary": "L3 IP 在 L4 TCP/UDP 下、L2 Ethernet/802.11 上。" },
"lec16:9": { "title": "Network Layer Data Plane Roadmap", "summary": "Router 内部 + IP + Generalized forwarding + Middleboxes。" },

"lec16:10": {
  "title": "Network Layer 服务",
  "summary": "把 transport segment 从 sender 送到 receiver 主机。",
  "key_points": [
    "Sender 封装 segment 进 datagram，传给链路层",
    "Receiver 解出 segment 给 transport 层",
    "**每个 Internet 设备都跑 IP**（host + router）"
  ]
},

"lec16:11": {
  "title": "Forwarding vs Routing — 核心区别 ⭐⭐",
  "summary": "Forwarding 是单 router 内的逐包动作（ns 级硬件）；Routing 决定整体路径（ms 级算法）。",
  "key_points": [
    "**Forwarding**: input port → output port，本地",
    "**Routing**: 跨整网决定路径",
    "类比 开车：forwarding = 过路口；routing = 行前规划"
  ]
},

"lec16:12": {
  "title": "Data Plane vs Control Plane ⭐⭐",
  "summary": "Data plane：单 router、ns 级、硬件 forwarding。Control plane：跨网、ms 级、软件 routing。",
  "explanation": "### 时间尺度差异\n- **Data plane**：每个 packet 通过 router 几百 ns。要快 → 硬件实现（ASIC、TCAM）。\n- **Control plane**：路由收敛通常 ms 到 s 级。可以软件实现，灵活。\n\n这就是为什么 SDN 容易：把慢的 control plane 拉到 controller 即可，data plane 依然在 switch 硬件。"
},

"lec16:13": { "title": "Per-router Control Plane", "summary": "传统：每 router 跑路由算法填自己 FT。" },
"lec16:14": { "title": "SDN Control Plane", "summary": "现代：remote controller 算 + 下发 FT。" },

"lec16:15": { "title": "Network Service Model — 表", "summary": "Internet best-effort vs ATM CBR/ABR vs IntServ/DiffServ。" },
"lec16:16": { "title": "Service Model — 补全表", "summary": "同上。" },

"lec16:17": {
  "title": "Best-Effort 反思 ⭐",
  "summary": "简单 = 易部署 = 成功。Internet 的成功来自最小化 network layer 复杂度。",
  "key_points": [
    "简单机制 → 广泛部署",
    "**Packet switching** 优势：bursty 流量不浪费 + 多路复用",
    "**Best-effort** 优势：简单 + 容错（不需要状态）",
    "『难以反驳 best-effort 模型的成功』"
  ]
},

"lec16:18": { "title": "Data Plane Roadmap — Router 内部", "summary": "进入 router 架构。" },

"lec16:19": {
  "title": "Router 架构概览 ⭐",
  "summary": "Routing processor + Switching fabric + Input/Output ports。",
  "key_points": [
    "**Routing processor**: control plane (软件, ms)",
    "**Switching fabric + Ports**: data plane (硬件, ns)",
    "两个时间尺度不同"
  ]
},

"lec16:20": {
  "title": "Router 类比 — 火车站",
  "summary": "Station manager = control plane；进出站台 = data plane。"
},

"lec16:21": {
  "title": "Input Port 功能 ⭐",
  "summary": "Physical → Link → Lookup → Forward → Queue → Fabric。",
  "key_points": [
    "**Physical**: bit-level 接收",
    "**Link layer**: 解 Ethernet frame",
    "**Lookup + Forward**: 查 FT 决定 output port (match+action)",
    "**Queue**: fabric 满了暂存"
  ]
},

"lec16:22": {
  "title": "Input Port — Generalized Forwarding",
  "summary": "Destination-based（看 IP）vs Generalized（看任意字段）。"
},

"lec16:23": { "title": "Destination-based Forwarding", "summary": "按 dst IP 段分配 output port。" },

"lec16:24": {
  "title": "Longest Prefix Matching — 概念 ⭐",
  "summary": "查 FT 时选『匹配前缀最长』的条目。",
  "explanation": "### 为什么 LPM 不是 first-match\n层级 IP 寻址下，一个目的 IP 可能匹配多条规则（一条粗的 /20，一条细的 /23）。粗的覆盖大段，细的覆盖小段。**包应该走更具体（细）的那条**。\n\n→ 最长前缀匹配。"
},

"lec16:25": { "title": "LPM 例 1", "summary": "11001000 00010111 00010110 10100001 匹配 00010***。" },
"lec16:26": { "title": "LPM 例 1 — 匹配标注", "summary": "前 24 位匹配，位 25-27 = 010 → 匹配规则 0。" },
"lec16:27": { "title": "LPM 例 2", "summary": "11001000 00010111 00011000 10101010 匹配 00011000 (/24)。" },
"lec16:28": { "title": "LPM 例 2 — 匹配标注", "summary": "完全匹配 /24 那条。" },

"lec16:29": {
  "title": "LPM + TCAM ⭐",
  "summary": "TCAM 一拍出结果，支持通配。Cisco Catalyst ~1M 条目。",
  "key_points": [
    "TCAM = Ternary Content Addressable Memory",
    "**支持 0, 1, * 三值**（不像普通 RAM 只 0/1）",
    "一拍并行匹配所有条目，O(1) 查询",
    "硬件贵 + 耗电 + 容量有限"
  ],
  "explanation": "### 为什么需要 TCAM\nLPM 要求查表时同时考虑多条带 * 的规则。普通 RAM 串行查 N 条 → O(N)，慢。\n\nTCAM 把所有条目并行比较，一个时钟周期出答案。\n\n### 容量\nCisco 高端路由器 TCAM 容纳 ~1M 条目，刚好覆盖 BGP 全表（~100 万）。如果 BGP 表继续涨，需要更大 TCAM。\n\n### 考法\n『为什么 LPM 用 TCAM？』→ 并行匹配带 * 的规则。"
},

"lec16:30": { "title": "Switching Fabrics — 概念", "summary": "Fabric 把 input 转到 output。Rate ≥ N·R 才不堵。" },
"lec16:31": { "title": "Switching Fabrics — 三类", "summary": "Memory / Bus / Interconnection (crossbar)。" },
"lec16:32": { "title": "Switching via Memory", "summary": "1st gen routers: CPU 控制，包过 memory 两次。慢。" },
"lec16:33": { "title": "Switching via Bus", "summary": "共享 bus；带宽限制（32 Gbps Cisco 5600）。" },

"lec16:34": {
  "title": "Switching via Interconnection (Crossbar) ⭐",
  "summary": "多级开关网络 (Crossbar, Clos)；现代高端 100s Tbps。",
  "key_points": [
    "Crossbar / Clos / 多 stage",
    "Datagram 分片成 cell 进 fabric，出口重组",
    "并行多个 fabric planes",
    "Cisco CRS: 8 planes × 3-stage 互联 → 100s Tbps"
  ]
},

"lec16:35": { "title": "Switching via Interconnection — 多平面", "summary": "8 个 fabric planes 并行扩展。" },

"lec16:36": {
  "title": "Input Port Queuing — HOL Blocking ⭐",
  "summary": "Fabric 慢于 input → 排队；队头被堵后面动不了。",
  "key_points": [
    "Fabric 不够快 → input 排队",
    "**HOL blocking**: 队头 packet 出口冲突，后面包都等",
    "解药: VOQ (virtual output queue) — 每个 output 一个 input 队列"
  ],
  "explanation": "### 例\nInput port 1 队列：[红→outputA, 绿→outputB, 蓝→outputC]\nInput port 2 同时想发到 outputA。\n\n如果只一个 fabric 通道，只能选一个发，比如红色去 outputA。\n\n**问题**：input 1 的绿色和蓝色其实可以同时发到 B 和 C（不冲突），但它们卡在队头红色后面动不了 → **HOL blocking**。\n\n### VOQ 解法\nInput port 维护多个队列，每个对应一个 output port。这样不同 output 不互相阻塞。"
},

"lec16:37": { "title": "Output Port Queuing", "summary": "Fabric 快于 output → output 排队。Drop policy + scheduling。" },
"lec16:38": { "title": "Output Port Queuing — 续图", "summary": "Buffer 溢出 → 丢包 = 拥塞核心来源。" },
"lec16:39": { "title": "Buffer Management ⭐", "summary": "Drop（tail/priority）+ Marking（ECN/RED）。" },

"lec16:40": { "title": "FCFS Scheduling", "summary": "First Come First Served = FIFO。最简单。" },

"lec16:41": {
  "title": "Priority Scheduling",
  "summary": "按 header 字段分类，高优先级队列先发；同类内 FCFS。",
  "explanation": "### 例\nVoIP 流量优先级高 → 总是优先于 web 流量。\n\n### 风险\n高优先级 starve 低优先级。需要 admission control。"
},

"lec16:42": { "title": "Round Robin", "summary": "循环服务每个 class 队列。" },

"lec16:43": {
  "title": "Weighted Fair Queueing (WFQ) ⭐",
  "summary": "Class i 得 w_i / Σw_j 份额服务时间。保证每个 class 最小带宽。",
  "formula": "$$\\text{class } i \\text{ share} = \\frac{w_i}{\\sum_j w_j}$$",
  "explanation": "### 直觉\nWFQ 是 RR 的泛化：每轮服务每个 class 但量不一样大。\n\n例：3 个 class，w = [1, 2, 3]。每个循环 class 1 发 1 个 packet，class 2 发 2 个，class 3 发 3 个。\n\n→ 长期看 class i 占 w_i / 6 的带宽。\n\n### Min BW 保证\n只要 class i 有流量，它至少拿到 w_i/Σw_j 的带宽。\n\n### 考法\n给 weights 算 share。"
},

"lec16:44": { "title": "Sidebar: Network Neutrality (1)", "summary": "技术 vs 社会 vs 法律层面的 net neutrality。" },

"lec16:45": {
  "title": "ISP: 电信 vs 信息服务？",
  "summary": "2015 FCC 三大原则。Title II（电信）vs Title I（信息）影响监管。",
  "key_points": [
    "**No blocking**: 不能阻断合法内容",
    "**No throttling**: 不能限速合法流量",
    "**No paid prioritization**: 不能付费插队"
  ]
},


# ============= lec14 =============
"lec14:1": {
  "title": "QUIZ — 文件分发时间 (Client-Server vs P2P) ⭐",
  "summary": "100 client 下载 50MB；server 并发限 10，client 上传 0.5Mbps。CS 4000s vs P2P 800s。",
  "explanation": "### Client-Server 算法\nServer 上传带宽是 1Mbps，但限 10 并发。每轮 10 个 client 各拿 50MB:\n- 时间 / client = 50MB × 8 / 1Mbps = 400s\n- 需要 100/10 = 10 轮 → 4000s\n\n### P2P 算法\n下限 = 总数据 / 总上传带宽 = (100 × 50MB × 8) / (100 × 0.5Mbps)\n= 40,000 Mb / 50 Mbps\n= **800s**\n\n忽略 server 上传。所有 peer 互相帮上传。\n\n### P2P 远好于 CS\n5 倍快。N 越大 P2P 优势越大（CS 时间随 N 线性增长，P2P 时间增长慢得多）。"
},

"lec14:2": {
  "title": "四种增/减策略 — AIAD/AIMD/MIAD/MIMD",
  "summary": "Additive 加 / Multiplicative 乘 × 增 / 减 → 4 种组合。",
  "key_points": [
    "**AIAD**: 温和增 + 温和减",
    "**AIMD**: 温和增 + 剧烈减 ← TCP 用",
    "**MIAD**: 剧烈增 + 温和减",
    "**MIMD**: 剧烈增 + 剧烈减"
  ],
  "explanation": "### 拥塞控制的本质权衡\n『发得多 vs 让带宽』。\n\n**Additive**: cwnd += b（每 RTT 加固定数）\n**Multiplicative**: cwnd ← a · cwnd（按比例放缩）\n\n### 4 种组合可视化\n几何上：\n- AIAD：加法平移，平移不改差距 → 不收敛公平\n- MIMD：乘法缩放，比例不变 → 不收敛公平\n- MIAD：增长过快，容易溢出 + 不公平\n- **AIMD**：唯一同时收敛公平和效率\n\n→ TCP 选 AIMD 不是偶然，是几何上的唯一解。"
},

"lec14:3": { "title": "Simple Congestion Control 模型", "summary": "两用户 (x1, x2)，效率线 x1+x2=1，公平线 x1=x2。" },
"lec14:4": { "title": "AIAD — 不收敛", "summary": "加法平移不改差距，差始终不变。" },
"lec14:5": { "title": "MIMD — 不收敛", "summary": "乘法缩放比例不变。" },

"lec14:6": {
  "title": "AIMD — 唯一收敛公平 ✨ ⭐⭐",
  "summary": "加法走 45°（向效率线），乘法沿原点缩（保比例 → 向公平线）。两步反复 → 螺旋收敛。",
  "key_points": [
    "Additive +a 走 45°",
    "Multiplicative ×b 沿原点缩",
    "螺旋收敛到 x1=x2 ∩ x1+x2=1，即 (0.5, 0.5)"
  ],
  "explanation": "### 直觉\n两用户从某起点出发：\n1. AI 阶段：(x1, x2) → (x1+a, x2+a)。沿 45° 走，碰效率线 x1+x2=1\n2. MD 阶段：(x1, x2) → (b·x1, b·x2)。沿原点缩，比例 x1/x2 不变。\n\n关键：MD 沿原点缩 + AI 走 45° → 两步交替的轨迹是『斜螺旋』，越来越靠近公平线。\n\n### 几何证明（简）\n令 D = x1 - x2 是差距。\nAI: D 不变（同时加 a）。\nMD: D' = b·x1 - b·x2 = b·D。\n\n所以每次 MD 后 D 缩小 b 倍（b<1）→ D 收敛到 0 → 公平。\n\n### 考法\n『为什么 AIMD 收敛公平？』必须画图 + 说出『加法走 45° + 乘法保比例 + 螺旋』。"
},

"lec14:7": {
  "title": "TCP cwnd 工作机制",
  "summary": "Sender 在 cwnd 字节范围内可发，发完等 ACK 推进。Rate ≈ cwnd/RTT。",
  "key_points": [
    "约束 LastByteSent − LastByteAcked < cwnd",
    "意思：未确认的 bytes 不能超过 cwnd",
    "Rate ≈ cwnd bytes / RTT"
  ],
  "explanation": "### 这个不等式什么意思？\n想象 sender 维护一个字节序号轴：\n\n```\n0 ────────── LastByteAcked ─── LastByteSent ─── 未发\n              |←─ 已确认 ─→|←── inflight ──→|\n```\n\n**inflight = LastByteSent − LastByteAcked** = 已发但还没收 ACK 的字节数。\n\nTCP 规定 inflight 不能超过 cwnd，即 sender 在 ACK 回来之前最多只能 cwnd 字节『在路上』。\n\n### 为什么这个约束\n- 防止 sender 把网络打爆\n- ACK 来一波，cwnd 滑动 → 再发一波\n\n### 跟 rwnd 的关系\nSender 实际受 min(cwnd, rwnd) 限制：\n- cwnd 是网络给的限制（拥塞控制）\n- rwnd 是 receiver 给的限制（flow control）\n\n### Throughput 公式\n每 RTT 能发 cwnd bytes → throughput ≈ cwnd/RTT。\n\n### 考法\n『LastByteSent − LastByteAcked < cwnd 意思？』→ inflight ≤ cwnd。\n『为什么这样限？』→ 不让 sender 超过拥塞控制估计的可用带宽。"
},

"lec14:8": {
  "title": "TCP 两种丢包 — 3 dup ACK vs Timeout ⭐",
  "summary": "丢一个 + 后续到 → 3 dup ACK（轻度）；丢一片 → timeout（重度）。反应力度不同。",
  "explanation": "### 3 Dup ACK 的故事\n- Sender 发 1,2,3,4,5\n- 包 1 丢了，2,3,4,5 都到了\n- Receiver 收到 2 时：ACK 1（『我还在等 1』）\n- 收到 3 时：ACK 1（dup ACK #1）\n- 收到 4 时：ACK 1（dup ACK #2）\n- 收到 5 时：ACK 1（dup ACK #3）\n- Sender 收到 3 个 dup ACK → 确认 1 真的丢了 + 但 2-5 到了 → 网络还能传\n\n→ **轻度拥塞**：multiplicative decrease (cwnd/2)，但不重启 slow start。\n\n### Timeout 的故事\n- Sender 发完 cwnd bytes\n- 一个 ACK 都没回\n- 等到超时\n- 可能整窗都丢了 → 网络严重拥塞\n\n→ **重度拥塞**：cwnd 退回 1 MSS，重启 slow start。\n\n### 为什么两种处理\n直觉：网络还在传东西（有 dup ACK 回来）说明只是边缘拥塞，可以乐观；什么都收不到说明严重，必须保守。"
},

"lec14:9": { "title": "Timeout 处理", "summary": "cwnd ← 1 MSS, ssthresh ← cwnd/2, 回 slow start。" },

"lec14:10": {
  "title": "Slow Start → CA 切换 ⭐",
  "summary": "cwnd 指数增长 (每 RTT ×2) 到 ssthresh 切线性 (+1 MSS/RTT)。",
  "explanation": "### Slow Start 实际是指数增\n名字误导。起点 cwnd=1 小，但增长速度 → 每收一个 ACK cwnd += MSS → 每 RTT cwnd 翻倍 → **指数**。\n\nRTT 0: cwnd = 1\nRTT 1: cwnd = 2\nRTT 2: cwnd = 4\nRTT 3: cwnd = 8 → 这是指数\n\n### 切换点\n- 起始 ssthresh = 64 KB（默认）\n- cwnd 增到 ssthresh 时切 CA（每 RTT +1 MSS，线性）\n- 丢包时 ssthresh = cwnd / 2（记忆『上次大约多少打爆了网络』）"
},

"lec14:11": { "title": "Timeout 后重启 slow start", "summary": "cwnd=1 重新指数增，到 ssthresh = old cwnd/2 切线性。" },

"lec14:12": {
  "title": "TCP CC FSM 总图 ⭐⭐⭐",
  "summary": "三状态：slow start / CA / fast recovery；四种转移。",
  "key_points": [
    "**Timeout** 任何状态 → slow start (cwnd=1, ssthresh=cwnd/2)",
    "**Slow start**: cwnd > ssthresh → CA",
    "**CA**: 3 dup ACK → fast recovery (cwnd=ssthresh+3, ssthresh=cwnd/2)",
    "**Fast recovery**: new ACK → CA (cwnd=ssthresh) ← 关键易错！"
  ],
  "explanation": "### 完整 FSM\n```\n          slow_start\n          ↓ (cwnd>ssthresh)\n              CA ←─────────┐\n              ↓ 3 dup ACK   │ new ACK\n        fast_recovery ─────┘\n\n  任何状态 + timeout → slow_start (cwnd=1)\n```\n\n### 每个状态 cwnd 更新\n- slow start: new ACK → cwnd += MSS\n- CA: new ACK → cwnd += MSS × (MSS/cwnd)（平均每 RTT +1 MSS）\n- fast recovery: dup ACK → cwnd += MSS（人为膨胀维持 pipeline）；new ACK → CA, cwnd=ssthresh\n\n### 易错点\n**Fast recovery 收 new ACK 回 CA（不是 slow start）**。考试常考这个细节。\n\n### 考法\n给 timeline 画 cwnd 变化；判断当前在哪个状态。"
},

"lec14:13": { "title": "TCP CUBIC — 直觉", "summary": "丢包切半后激进追回 Wmax，临近时减速。" },

"lec14:14": {
  "title": "TCP CUBIC 公式",
  "summary": "W(t) = C(t−K)³ + Wmax。Linux 默认。",
  "formula": "$$W(t) = C(t - K)^3 + W_{\\max}$$",
  "explanation": "### 为什么用 cubic\nAIMD 的线性增长在高 BDP 链路（千兆 + 太平洋 RTT）太慢：每 RTT +1 MSS，几十秒才追回切半的 cwnd。\n\nCUBIC 的洞察：丢包后切半，但 bottleneck link 容量 probably 没变多少，所以可以激进追回 Wmax，然后小心试探。\n\n### 三次曲线的优点\nt 远小于 K（远离 Wmax）→ |t-K| 大 → cubic 项很大 → 增长快\nt 接近 K → cubic 项小 → 平稳\nt 略超过 K → 缓慢试探新容量\n\n### 默认参数\nLinux 默认 CUBIC，几乎所有 web server 都跑它。Mac/Windows 也是。"
},

"lec14:15": { "title": "TCP & Bottleneck Link", "summary": "TCP 加 cwnd 直到某段链路丢包。" },
"lec14:16": { "title": "Bottleneck 洞察", "summary": "增 cwnd 让 RTT 升、但 throughput 不变。引出 BBR 思想。" },

"lec14:17": {
  "title": "Delay-based CC 推导",
  "summary": "用 RTT 上升判拥塞而非丢包。",
  "explanation": "### 思想\nTCP loss-based 必须等到 queue 满 + 丢包才反应。Delay-based 在 queue 刚开始堆积（RTT 上升）就反应 → 低延迟、少丢包。\n\n### 估算\n- RTTmin = 历史最小 RTT（无拥塞）\n- 无拥塞 throughput = cwnd / RTTmin\n- 实测 throughput ≈ uncongested → 无拥塞 → 增 cwnd\n- 实测 << uncongested → 拥塞（queue 堆积）→ 减 cwnd"
},

"lec14:18": {
  "title": "Delay-based 优缺点 ⭐",
  "summary": "低延迟 + 少丢包；但跟 loss-based 共存会 starve。",
  "key_points": [
    "✅ 稳定 + 低延迟 + 小队列",
    "❌ 跟 loss-based 共存 → loss-based 一直加 cwnd 直到丢包，delay-based 早退让 → **starvation**"
  ]
},

"lec14:19": {
  "title": "Model-based (BBR) ⭐",
  "summary": "Google 提出。估 BtlBw + RTprop，控制 inflight = BDP。不靠丢包不靠纯延迟。",
  "key_points": [
    "**BtlBw**: 估算最近 bottleneck 带宽（最近最大 delivered rate）",
    "**RTprop**: 估算 propagation RTT（最近最小 RTT）",
    "**目标**: inflight ≈ BtlBw × RTprop（刚好填满管道）",
    "**避免**: queue 堆积（多了），underutilization（少了）"
  ],
  "explanation": "### 为什么 BBR 牛\n传统 loss-based CC 反应慢（要等 buffer 满 + 丢包）。Delay-based 反应更早但跟 loss-based 共存会 starve。BBR 主动测量网络真实状态：\n\n- 测最大 delivered rate → 知道 bottleneck 是多少\n- 测最小 RTT → 知道无队列时多少\n- 控制 inflight = bandwidth × RTprop → 刚好填管\n\n### Google 部署\nB4 backbone 网络全跑 BBR。YouTube 视频流量大量靠 BBR 提升体验。\n\n### 考法\n『BBR 跟 loss-based 区别？』必答：基于网络模型测量，不靠丢包。"
},

"lec14:20": {
  "title": "ECN ⭐",
  "summary": "Router 在 IP ToS 字段打 2 bit 标记；Receiver 经 ACK ECE bit 回传；Sender 减半 cwnd 但不丢包。IP + TCP 协作。",
  "key_points": [
    "Router 在 IP header ToS (LSB 2 bit) 打 ECN=11 标记",
    "Receiver 收到 ECN=11 → 在 ACK 的 TCP header ECE bit = 1",
    "Sender 见 ECE=1 → cwnd /= 2（跟 dup ACK 反应一样），**但没真丢包**"
  ],
  "explanation": "### 为什么需要 ECN\nLoss-based CC 必须等到 buffer 满 → 丢包 → 重传。这浪费：\n1. Queue 满了延迟已经很大\n2. 重传消耗带宽\n3. 反应时机晚\n\nECN 让 router 在 queue 长度超阈值时（还没满）就标记包。Receiver 通过 ACK 把信号传回 sender。Sender 提前减速 → 队列降回稳态。\n\n### IP + TCP 协作\n- IP 层：ECN 字段（2 bit on ToS）\n- TCP 层：ECE bit on ACK + CWR bit on next packet（确认收到 ECE）\n\n### 谈判\nECN 必须双方支持。建连时通过 SYN 协商：SYN 的 ECE+CWR 都设 1 表示 'I support ECN'。\n\n### 部署\nLinux 默认开 ECN（被动响应，主动协商在某些发行版关闭）。"
},

}

def main():
    data = json.loads(DETAIL.read_text())
    data.update(NEW)
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"updated {len(NEW)} entries; total now {len(data)}")

if __name__ == "__main__":
    main()
