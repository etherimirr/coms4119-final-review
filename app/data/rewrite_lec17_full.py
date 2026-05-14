#!/usr/bin/env python3
"""Full per-page rewrite for lec17 (IP / DHCP / NAT, 28 pages).

For each page:
  1. 复述 PPT 实际内容
  2. 关键点
  3. 详解 + 考点
  4. Quiz 答案（若 PPT 没给）
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec17:1": {
  "title": "Midterm Grades",
  "summary": "课程公布期中考成绩分布：median 50，mean 49.55，max 90，min 7。",
  "key_points": [
    "Median 50 / Mean 49.55 — 一半人不及格",
    "Max 90, Min 7 — 极差 83",
    "你的 52 略高于平均（前 50%）"
  ],
  "explanation": "**这一页本身没有技术内容**，就是宣布期中分数情况。给一个心理参考：跟平均比、跟最高比；卷面较难（平均刚过 50）。\n\n**对 final 的暗示**：老师认为期中难度合适，所以 final 类似难度可期。"
},

"lec17:2": {
  "title": "Network Layer Data Plane Roadmap",
  "summary": "本章节路线图：先 router 内部结构，再 IP 协议 + 寻址 + NAT + IPv6，最后 Generalized Forwarding/SDN + Middleboxes。",
  "key_points": [
    "Network layer 分 data plane 和 control plane",
    "本章先讲 data plane（这堂课覆盖 IP datagram → 寻址 → DHCP → NAT）",
    "Generalized forwarding 和 SDN 后面 lec20 才详讲"
  ],
  "explanation": "**整体框架**：data plane 在 router 内部 ns 级硬件转发；control plane 在 ms 级软件算路由表。本堂课聚焦『一个 router 收到 IP packet 后怎么处理』+ '一台 host 怎么拿到 IP'。\n\n**学习地图**：\n- Router 内：input port → fabric → output port\n- IP 协议：datagram 格式 + 32 位地址结构\n- 拿 IP：DHCP 自动 / 硬编码\n- NAT：私网公网映射\n- IPv6：128 位 + 简化 header（lec18 讲）"
},

"lec17:3": {
  "title": "Network Layer: Internet — 三大组件",
  "summary": "Host + router 都跑 IP 层。IP 层由三件事组成：IP 协议（datagram 格式 + 寻址 + 处理约定）、ICMP（错误报告 + router 信号）、Routing 算法（OSPF/BGP/SDN 等）。",
  "key_points": [
    "IP 协议本身：datagram 格式、addressing、packet handling 约定",
    "ICMP：error reporting、router signaling（ping、traceroute 的底层）",
    "Routing：OSPF/BGP/SDN 算法填 forwarding table",
    "三者协作形成完整 network layer"
  ],
  "explanation": "**这是 network layer 的全景图**，每台设备的 L3 都同时包含这三块：\n\n1. **IP 协议**：定义 packet 怎么写（datagram fields）+ 怎么寻址（32 位 IP）+ 怎么处理（TTL 减 1、checksum 校验、分片）。\n\n2. **ICMP**：当 packet 出问题（TTL 到 0、目的不可达、超大需分片但 DF=1）时，router 用 ICMP 发错误回 sender。`ping` 用 ICMP Echo Request/Reply；`traceroute` 故意设 TTL=1,2,3... 利用 ICMP TTL Exceeded 反馈。\n\n3. **Routing 算法**：构造 forwarding table 的智能层。OSPF 内部用、BGP 外部用。\n\n**考点**：这张图可能填空哪些字段属于 IP 协议层（vs transport / link）。"
},

"lec17:4": {
  "title": "IPv4 Datagram Format — 字段详解",
  "summary": "32 位行宽，base header 20 byte。重要字段：ver/hlen/ToS/total len、id/flags/frag offset（分片）、TTL、protocol（指 transport 层）、header checksum、src/dst IP（各 32 位）、options（可变）、payload。",
  "key_points": [
    "**Ver (4 b)**: 0100=IPv4, 0110=IPv6",
    "**Hlen (4 b)**: header 长度，以 4-byte 为单位；无 options 时 =5 → 20 byte",
    "**ToS (8 b)**: 高 6 位 diffserv（QoS），低 2 位 ECN",
    "**Total length (16 b)**: header + payload，单位 byte；最大 64 KB",
    "**Identifier + Flags + Frag offset**: 分片重组用",
    "**TTL (8 b)**: 每跳 −1，到 0 丢弃（防环 + 防包永远循环）",
    "**Upper layer protocol (8 b)**: 6=TCP, 17=UDP, 1=ICMP, 89=OSPF",
    "**Header checksum (16 b)**: 只算 header，每跳 TTL 变要重算",
    "**Src/Dst IP (32 b each)**: 端到端不变"
  ],
  "explanation": "**这一页极容易考填空**。重点：\n\n**TCP/IP 总开销**：TCP header 20 B + IP header 20 B = **40 B/packet**。所以小包（DNS 查询、ping）效率极低。\n\n**Total length 限制**：16-bit 字段最大 64 KB，但实际 MTU 通常 1500（Ethernet 默认），所以大包要分片。\n\n**TTL 用途**：\n- 防止 packet 永远在网络中循环（路由出 bug 时）\n- traceroute 利用：故意设 TTL=1,2,3... 每跳让 router 返回 ICMP TTL Exceeded，从而探测路径\n\n**Protocol 字段语义**：受信端 demux 上层的钥匙。Receiver 看到 protocol=6 就把 payload 交给 TCP 处理。\n\n**考点示例**：\n- 『TTL 字段作用？』→ 防环 + 限制最长跳数\n- 『TCP/IP 头总 overhead？』→ 40 B\n- 『IPv4 datagram 最大多长？』→ 64 KB",
  "gotcha": "**IPv4 checksum 只覆盖 header，不覆盖 payload**。Payload 的完整性靠 TCP/UDP checksum。IPv6 干脆去掉 IP checksum 字段（让 TCP/UDP 兜底）。"
},

"lec17:5": {
  "title": "IP Addressing — 32-bit ID 关联到 interface（不是 host）",
  "summary": "IP 地址是 32 位标识符，**关联到 host/router 的 interface**（每个接口一个）。Router 有多个接口故有多 IP；host 通常 1-2 个（有线 + 无线）。",
  "key_points": [
    "IP = 32 bit，点分十进制写法",
    "**关联到 interface，不是 host**",
    "Router 有多个接口 → 多 IP",
    "Host 通常 1-2 个接口（Ethernet + WiFi）",
    "223.1.1.1 = 11011111.00000001.00000001.00000001"
  ],
  "explanation": "**关键概念误区**：很多人以为 'IP 是机器的'，其实 IP 是**接口的**。\n\n一台 router 同时连 3 个子网就有 3 个 IP（每个接口配一个不同 subnet 的 IP）。一台笔记本同时连有线和 WiFi 就有 2 个 IP（属于不同子网）。\n\n**点分十进制就是把 32 位拆 4 段 × 8 bit**，每段 0-255。例如 223.1.1.1：\n- 223 = 11011111\n- 1 = 00000001\n- 1 = 00000001\n- 1 = 00000001\n\n**考点**：『一台 router 几个 IP？』要看它有几个接口（每接口一个）。"
},

"lec17:6": {
  "title": "IP Addressing — 同样的图，强调多设备视角",
  "summary": "复用前一页的图，强调网络里有多个 host 和 router 接口，每个接口都有自己的 IP。",
  "key_points": [
    "重复说明 interface ↔ IP 一对一关系",
    "Router 多接口，多 IP",
    "Host 通常 1-2 个"
  ],
  "explanation": "**纯重复，巩固概念**。看图：router 把 3 个子网（223.1.1.x、223.1.2.x、223.1.3.x）连起来，每个连接的接口都有自己的 IP。\n\n直觉：IP 像门牌号——挂在『门』上，不是挂在『屋主』上。"
},

"lec17:7": {
  "title": "IP Addressing — Interface 怎么物理连接？",
  "summary": "回答『接口物理上怎么连』：有线靠 Ethernet 交换机连，无线靠 WiFi 基站。L1/L2 细节后面 chapters 6, 7（即 lec22）讲。",
  "key_points": [
    "有线 interfaces：Ethernet switch 连",
    "无线 interfaces：WiFi base station / access point 连",
    "现在不用管细节，知道是黑盒就行"
  ],
  "explanation": "**先做抽象**：网络层只关心 'IP 怎么寻址'，不关心 'frame 物理上怎么传'。物理连接的事是 L1/L2 的问题，后续 lec22 详讲。\n\n**Q: 怎么知道两个接口是不是同子网？** 答：从 subnet 划分定义看（下一页讲）。"
},

"lec17:8": {
  "title": "Subnets — 定义",
  "summary": "Subnet = 一组能不经 router 直接互通的接口。IP 地址有结构：**subnet 部分**（高位，标识 LAN）+ **host 部分**（低位，区分 LAN 内主机）。",
  "key_points": [
    "Subnet = 设备接口之间不经 router 可达",
    "IP 高位 = subnet 部分（共同）",
    "IP 低位 = host 部分（不同）",
    "Subnet mask 决定『高位到哪位为止』"
  ],
  "explanation": "**核心概念**：同子网内可以 ARP 直接通信（L2），跨子网必须通过 router（L3）。\n\n**为什么这样切**：\n1. **路由表小**：路由器只需要记『某 subnet → 出哪个接口』，不需要记每个 host\n2. **广播限制**：ARP 等广播只在子网内，跨子网阻断\n\n**例**：223.1.1.1 和 223.1.1.4 共 24 位 → 同子网；223.1.1.1 和 223.1.2.1 前 16 位同后 8 位不同 → 不同子网。"
},

"lec17:9": {
  "title": "Subnets — 找子网的食谱",
  "summary": "断开每个 router 接口，剩下的孤岛就是 subnet。子网掩码 /24 表示『高 24 位 = subnet 部分』。",
  "key_points": [
    "**Recipe**: 把所有 router 接口拆掉，看剩多少个『孤岛』",
    "每个孤岛 = 一个 subnet",
    "图里 3 个孤岛 = 3 个 subnet (223.1.1.0/24, 223.1.2.0/24, 223.1.3.0/24)",
    "/24 = 高 24 位是 subnet 部分"
  ],
  "explanation": "**做题技巧**：\n1. 拿到拓扑图，把 router 标记出来\n2. 把每个 router 想象成『切断点』\n3. 数剩下几个互联的『孤岛』\n4. 每个孤岛是一个 subnet\n\n**图里**：图中每个虚线圈就是一个 subnet，223.1.1.0/24 包含 223.1.1.{1,2,3,4}，但 223.1.1.4 实际是 router 的接口。\n\n**考点**：给个拓扑图问『有几个 subnet』，按这套数法。"
},

"lec17:10": {
  "title": "Subnets — 更复杂的拓扑练习",
  "summary": "进阶练习：拓扑里有 6 个 subnet（223.1.1/24, 223.1.2/24, ..., 223.1.9/24），3 个 router 互连。",
  "key_points": [
    "复杂拓扑：3 个 router 互连 + 4 个末端 LAN",
    "总共 6 个 /24 subnet",
    "Router 接口分别属于不同 subnet"
  ],
  "explanation": "**应用上一页方法**：\n- 中间 3 个 router 把 IP 段分成 6 块\n- 每个末端 LAN 是一个 subnet\n- Router 之间的连线也是一个 subnet（即使只有 2 个接口）\n\n**考点**：『下图有几个 subnet？』数 router 接口分割出的孤岛。"
},

"lec17:11": {
  "title": "CIDR — Classless InterDomain Routing",
  "summary": "格式 **a.b.c.d/x**，x = subnet 部分位数（0-32）。打破老的 Class A/B/C 固定边界。Mask 长度可任意。",
  "key_points": [
    "格式: a.b.c.d/x",
    "x 任意 0-32",
    "Mask = x 个 1 + (32−x) 个 0",
    "200.23.16.0/23 → 高 23 位 = subnet, 低 9 位 = host"
  ],
  "explanation": "**老的 Class 系统的问题**：\n- Class A /8 = 1600 万地址\n- Class B /16 = 6.5 万\n- Class C /24 = 256\n\n要 500 个地址只能拿 Class B（浪费 99%）。\n\n**CIDR 让 mask 长度任意**：要 500 个地址 → /23（512 个）刚刚好。\n\n**路由聚合**也是 CIDR 的副产品（lec17:20 讲）。\n\n**期末 Q2 直接考这个**：128.16.51.2 /20 → prefix=128.16.48.0/20, host=0.0.3.2, 2¹²=4096 个地址。\n\n**做题套路**：\n1. mask 长度 = x（题目给）\n2. mask = x 个 1\n3. prefix = IP AND mask（用二进制 AND，别用十进制！）\n4. host part = IP XOR prefix 或 IP − prefix\n5. 容量 = 2^(32−x)",
  "gotcha": "**中间字节最坑**：第三段 51 ∧ 240 别用十进制算。51=00110011, 240=11110000, AND=00110000=48。心算容易错。"
},

"lec17:12": {
  "title": "IP 地址获取 — 两个问题",
  "summary": "拆成两问：(1) Host 怎么拿到 IP 的 host 部分？答：硬编码或 DHCP。(2) Subnet 怎么拿到 prefix 部分？答：ISP 分配（下面几页讲）。",
  "key_points": [
    "Q1: host 怎么拿 IP？→ 硬编码 / DHCP",
    "Q2: subnet 怎么拿 prefix？→ ISP / ICANN",
    "现代实践：DHCP plug-and-play"
  ],
  "explanation": "**两个层级的问题**：\n- **Host 部分**：插上 host 怎么自动配 IP？硬编码（如服务器、router）或 DHCP（动态）\n- **Subnet 部分**：组织怎么拿到自己的 IP 段？从 ISP 申请；ISP 从 ICANN/区域注册商（RR）申请\n\n下一页详讲 DHCP（host 拿 IP 的方式）。"
},

"lec17:13": {
  "title": "DHCP — Dynamic Host Configuration Protocol 介绍",
  "summary": "DHCP 让 host 加入网络时**动态拿 IP**。可续租、地址复用、plug-and-play。流程概览：discover → offer → request → ack（DORA）。前 2 步可省（如果 client 记得上次 IP）。",
  "key_points": [
    "Host 加入网络 → 广播 DHCP discover",
    "DHCP server 回 offer（包含候选 IP）",
    "Host 发 request 选这个 IP",
    "Server 发 ack 确认",
    "前 2 步可省（短路续租）",
    "支持 mobile users (join/leave)"
  ],
  "explanation": "**为什么不能硬编码**：\n- 移动设备到处跑（咖啡馆/家/学校）\n- 同子网内不能重复 IP\n- 离开后 IP 要还回去给别人用\n\n**DHCP 解决**：动态分配 + 租约管理 + 自动配置。手机 / 笔记本插 WiFi 几秒就能上网，靠的就是它。\n\n**广播性质**：client 还没 IP，无法 unicast，只能用 IP 全 1 (255.255.255.255) + MAC 全 F (FF×6) 广播。整个 LAN 都收到，但只有 DHCP server 会回。"
},

"lec17:14": {
  "title": "DHCP Client-Server 场景 — Server 部署位置",
  "summary": "DHCP server 通常装在 **router 上**（因为 router 跨多个 subnet），服务该 router 所有连接的 subnet。",
  "key_points": [
    "DHCP server 一般co-located 在 router 上",
    "一个 server 服务多个 subnet（router 连的每个）",
    "Arriving client 需要本 subnet 的 IP"
  ],
  "explanation": "**为什么放 router**：\n- Router 接所有 subnet，知道每个 subnet 的 IP 段\n- 集中分配避免冲突\n- 接好后立刻能为新设备服务\n\n家用路由器（如 TP-Link / Netgear）默认开 DHCP，连上 WiFi 几秒就拿到 192.168.x.x 的 IP。"
},

"lec17:15": {
  "title": "DHCP DORA — 全流程时序",
  "summary": "完整 4 步：(1) Discover (src 0.0.0.0:68, dst 255.255.255.255:67, broadcast), (2) Offer (server yiaddr + lease), (3) Request (client 接受), (4) ACK (server 确认绑定)。",
  "key_points": [
    "**Discover**: src 0.0.0.0:68 → dst 255.255.255.255:67, broadcast",
    "**Offer**: server → yiaddr 候选 IP + lease 时间",
    "**Request**: client 选择候选 IP",
    "**ACK**: server 确认",
    "yiaddr = 'your IP address' 字段",
    "transaction ID 让 client 匹配 reply"
  ],
  "explanation": "**为什么需要 4 步**：\n\n1. **Discover**: client 喊『有 DHCP server 吗？』\n2. **Offer**: server 答『有，给你这个 IP』（如有多 server，client 可能收多个 offer）\n3. **Request**: client 明确选择一个 offer（同时让其他 server 释放预留）\n4. **ACK**: 被选 server 确认绑定，给完整配置（DNS、gateway、netmask、lease）\n\n**端口约定**：server 67, client 68（固定，因为 client 还没 IP 不能动态分配）。\n\n**Short-circuit**: 若 client 想续用上次 IP，可直接发 Request 跳过 Discover/Offer。\n\n**考点**：『DHCP 4 步是什么？为什么用广播？』必背 DORA。"
},

"lec17:16": {
  "title": "DHCP — 还能给什么（不只 IP）",
  "summary": "DHCP server 不只给 IP，还给：(a) first-hop router (default gateway) 的 IP，(b) DNS server 的 IP，(c) subnet mask（用来判断目的是否本子网）。",
  "key_points": [
    "**IP address** 自己用",
    "**Default gateway**: first-hop router IP",
    "**DNS server IP**: 域名解析",
    "**Subnet mask**: 判断目的是否本子网（→ 决定 ARP 谁）",
    "+ lease 时长"
  ],
  "explanation": "**这 4 样缺一不可**：\n\n1. **IP**：没它发不出包\n2. **Gateway**：跨子网包要交给 router；不知道 router IP 就跨不出去\n3. **DNS server**：浏览器输 google.com 要解析\n4. **Netmask**：判断 dst IP 是不是同子网 → 决定 ARP 谁\n\n**没 mask 会怎样**：host 看到 dst 1.2.3.4，不知道是否同子网。试图直接 ARP 1.2.3.4 → 如果在别的子网，本地广播没人回 → 永远连不上。\n\n**考点（高频）**：『DHCP server 返回什么？』必背 4 样。"
},

"lec17:17": {
  "title": "DHCP 例 (1) — 协议栈封装",
  "summary": "DHCP 报文承载层级：DHCP message → UDP → IP → Ethernet。从 client 出去时全广播：Ethernet dst = FFFFFFFFFFFF, IP dst = 255.255.255.255, UDP dst port = 67。整个 LAN 都能收到，到 router 后逐层 demux 到 DHCP daemon。",
  "key_points": [
    "DHCP 在 UDP 上跑（轻量、不需要可靠）",
    "封装：DHCP → UDP → IP → Ethernet",
    "Ethernet 广播 (FFFFFFFFFFFF) 让整个 LAN 收到",
    "Router 上 Ethernet → IP → UDP → DHCP 逐层 demux"
  ],
  "explanation": "**为什么 DHCP 在 UDP 而不是 TCP**：\n- TCP 需要 3WHS 才能开始通信，但 client 还没 IP，无法建 TCP\n- DHCP 是少量交换，丢了就重发整段 DORA 即可\n- 不需要可靠交付的复杂性\n\n**完整封装链**（client→server）：\n```\n[Eth: dst=FFFFFFFFFFFF, src=client MAC]\n[IP:  dst=255.255.255.255, src=0.0.0.0]\n[UDP: dst=67, src=68]\n[DHCP Discover]\n```\n\nReceiver 看到 Eth 广播 → 接收 → IP 看 255.255.255.255 → 接受 → UDP 看 port 67 → 交给 DHCP daemon。"
},

"lec17:18": {
  "title": "DHCP 例 (2) — Server 应答路径",
  "summary": "Server 反向：DHCP ACK → UDP → IP → Ethernet 出去。Client 拿到后 demux 上来交给 DHCP client process，进而拿到完整配置。",
  "key_points": [
    "Server 同样要广播应答（因为 client 还没固定 IP）",
    "应答用 src=server IP, dst=255.255.255.255",
    "Client 上 Ethernet → IP → UDP → DHCP demux",
    "拿到 IP + gateway + DNS + mask"
  ],
  "explanation": "**关键设计**：server 应答也是广播（不能 unicast 给 client，因为 client 还在『协商中』IP）。Client 用 transaction ID 识别『这是我的 reply 不是别人的』。\n\n**整个过程时间**：典型 < 100ms（同 LAN）。所以你插 WiFi 几秒上线，DHCP 只占其中一小段。"
},

"lec17:19": {
  "title": "IP 地址获取 — Subnet 部分怎么来",
  "summary": "Q2 复习：subnet 部分（即 prefix）怎么来？答：从 ISP 拿。ISP 拿一段地址空间后切给客户。",
  "key_points": [
    "ISP 拿一大段地址（如 /20）",
    "ISP 切分给客户（每客户 /23 或更小）",
    "下一页讲层级聚合"
  ],
  "explanation": "**层级结构**：\n- ICANN/RR → 给 ISP 大段（如 200.23.16.0/20）\n- ISP → 给 8 个组织各 /23\n- 组织 → 给 host 分配（DHCP）\n\n这个层级支持 **路由聚合**（lec17:20）。"
},

"lec17:20": {
  "title": "Hierarchical Addressing — 路由聚合",
  "summary": "ISP 拿一段（如 200.23.16.0/20，4096 地址），切给 8 个组织各 /23（512 地址）。对外只 advertise /20 一条，路由表大幅缩小。",
  "key_points": [
    "ISP `Fly-By-Night` 拿 200.23.16.0/20",
    "切给 Org 0 (200.23.16.0/23), Org 1 (200.23.18.0/23), ..., Org 7 (200.23.30.0/23)",
    "对 Internet 只 advertise `200.23.16.0/20`（聚合）",
    "其他 ISP 只需要 1 条规则就能路由到这 8 个组织",
    "省路由表 + 省 BGP 更新流量"
  ],
  "explanation": "**没聚合 vs 有聚合**：\n- 没聚合：ISP 把 8 个 /23 都向外 advertise → Internet 路由表多 8 条\n- 聚合：ISP 只 advertise 1 个 /20 → 外面路由表只多 1 条\n\n**真实数字**：Internet BGP 全表约 100 万条。如果没聚合可能要 1 亿条 → 路由器内存撑不住。\n\n**额外好处**：如果一个 Org 内部细分网络变化（比如 Org 3 改了内部 subnet），不影响外部路由——内部细节对外界不可见。这就是 *hiding* 的好处。\n\n**考点**：『为什么 hierarchical addressing？』必答 → 路由聚合 + scalable + hiding internal changes."
},

"lec17:21": {
  "title": "IP Addressing — Last Words",
  "summary": "(a) ICANN 管全球 IP 分配（5 个区域注册商 RR）+ DNS 根。(b) IPv4 已分完（2011 年）。NAT 缓解 + IPv6 128 位是治本。Vint Cerf 自嘲『谁知道当年要这么多地址』。",
  "key_points": [
    "**ICANN**: Internet Corp. for Assigned Names and Numbers — 全球唯一权威",
    "5 个区域注册商 (RR)：ARIN(北美), RIPE(欧洲), APNIC(亚太), LACNIC(拉美), AFRINIC(非洲)",
    "**ICANN 还管**: DNS 根、TLD 分配 (.com, .edu)",
    "**IPv4 2011 已分完** → NAT 缓解 + IPv6 治本",
    "IPv6 128 bit = 2¹²⁸ ≈ 3.4×10³⁸ 个地址",
    "Vint Cerf 引言：『谁当年知道要多少地址』"
  ],
  "explanation": "**ICANN 是什么**：管整个 Internet 命名 / 编号的非营利机构（美国成立）。当 ICANN 给 .edu 注册某个名字时，全球所有 DNS server 都得听。\n\n**地理分配**：5 个 RR 各管一片，本地用户从本地 RR 申请。\n\n**IPv6 推进缓慢**：因为 NAT 已经『差不多够用』，加之改协议代价大。但 Google 2026 数据显示 ~49% 客户端走 IPv6 了。"
},

"lec17:22": {
  "title": "Data Plane Roadmap — 进入 NAT 章节",
  "summary": "目录回顾，接下来讲 NAT (Network Address Translation)。",
  "key_points": ["章节过渡，下一页进入 NAT 实质内容"]
},

"lec17:23": {
  "title": "NAT — Network Address Translation 介绍",
  "summary": "局域网内所有设备用私有 IP（10/8, 172.16/12, 192.168/16），共享 1 个公网 IP 对外通信。NAT router 负责改写 src 字段：出包改 src IP+port，入包反查表改 dst IP+port。",
  "key_points": [
    "LAN 内：用私有 IP（10.0.0.0/8, 172.16/12, 192.168/16）",
    "对外：所有设备共享 NAT router 的公网 IP",
    "出包 src 改写：(私 IP, 私 port) → (NAT IP, new port)",
    "记入 NAT 表",
    "入包 dst 反查表：(NAT IP, new port) → (私 IP, 私 port)"
  ],
  "explanation": "**为什么需要 NAT**：\n- IPv4 地址 2011 年已分完\n- 家用 / 小公司从 ISP 只能拿 1 个公网 IP\n- 但家里有手机、笔记本、电视、平板... 几十台设备\n- 解药：内部用私有 IP，对外共享 1 个公网 IP\n\n**私有 IP 段**（不可在 Internet 路由）：\n- **10.0.0.0/8**（1600 万地址，大型企业）\n- **172.16.0.0/12**（中型）\n- **192.168.0.0/16**（家用最常见）\n\n**对外只看到一个 IP**：从 google.com 角度，你家所有设备的流量都来自同一个 IP（你家 NAT router 的公网 IP）。\n\n**端口区分**：NAT 用不同的对外 port 区分内部哪台设备发的。"
},

"lec17:24": {
  "title": "NAT — 优点",
  "summary": "(1) 只需 1 个公网 IP 给整个 LAN；(2) LAN 内改 IP 对外透明；(3) 换 ISP 不需要改 host 配置；(4) 安全：外人看不到内网 host（除非 port forwarding）。",
  "key_points": [
    "省 IP：1 个公网 IP 给整个 LAN",
    "对外透明：LAN 内 host 改 IP 不影响外界",
    "换 ISP 不动 LAN 内 IP",
    "安全：外部主机无法主动连入（粗糙的防火墙）"
  ],
  "explanation": "**省 IP**：地址不够用的根本缓解。\n\n**透明性**：家里给手机换私有 IP（比如 192.168.1.5 → 192.168.1.10）不需要通知外部任何人。\n\n**安全副作用**：因为外部不能主动连进来（除非 port forwarding 配置），NAT 实际上充当了简单的防火墙。但也阻碍了 P2P / 自托管 server。\n\n**反面**：违反 end-to-end argument（下一页）；阻碍 P2P 需要 NAT traversal 技术（STUN/TURN/UPnP）。"
},

"lec17:25": {
  "title": "NAT — 实现细节",
  "summary": "NAT router 透明地：(a) 出包：将 (src IP, src port) 改为 (NAT IP, new port)，记入 NAT 表；(b) 入包：查 NAT 表把 (NAT IP, new port) 反查为 (src IP, src port)。",
  "key_points": [
    "出包：替换 src 字段，记录 (orig src IP, src port) ↔ (NAT IP, new port) 映射",
    "Remote server 用 (NAT IP, new port) 作为目的回包",
    "入包：替换 dst 字段，恢复原始 (src IP, src port)",
    "整个过程对 LAN 内 host 和 remote server 都透明"
  ],
  "explanation": "**NAT 表结构**：\n```\nWAN side (公网 IP, port)     LAN side (私 IP, port)\n138.76.29.7:5001          ↔  10.0.0.1:3345\n138.76.29.7:5002          ↔  10.0.0.2:4587\n138.76.29.7:5003          ↔  10.0.0.1:3346\n...\n```\n\n**Port 复用**：同一台公网 IP 可以同时支持多达 65535 - 1024 = 64511 个并发连接（动态 port 区间）。\n\n**Connection-level**：NAT 表项有 timeout（typically 几分钟到几十分钟），idle 连接自动清。"
},

"lec17:26": {
  "title": "NAT — 完整工作流程图解",
  "summary": "图示一个具体的 NAT 实例：host 10.0.0.1:3345 想访问 128.119.40.186:80。NAT 把 src 改成 138.76.29.7:5001，server 回包到 138.76.29.7:5001，NAT 反查表恢复成 10.0.0.1:3345。",
  "key_points": [
    "Step 1: host 10.0.0.1:3345 发包给 128.119.40.186:80",
    "Step 2: NAT router 改 src 为 138.76.29.7:5001，记表",
    "Step 3: server 回包 dst=138.76.29.7:5001",
    "Step 4: NAT 查表 5001 → 10.0.0.1:3345，改 dst",
    "Host 10.0.0.1 收到 reply"
  ],
  "explanation": "**4 步完整动作**（必会画图）：\n\n```\nLAN 内 host             NAT router               Internet server\n10.0.0.1:3345 ──S:10.0.0.1,3345──>\n                              \\          ┌─ NAT 表更新 ─┐\n                               └→ 改 src   │ 138.76.29.7:5001\n                                          │ ↔ 10.0.0.1:3345\n                                          └─────────────┘\n                              S:138.76.29.7,5001 D:128.119.40.186,80 ──>\n                                                                              server\n                              <── S:128.119.40.186,80 D:138.76.29.7,5001\n                              ┌─ NAT 查表 ─┐\n                              │ 5001 → 10.0.0.1:3345\n                              └────────────┘\n              <── S:128.119.40.186,80 D:10.0.0.1,3345 ──\n```\n\n**考点**：给一个 NAT 场景，问『出包/入包 src/dst 各是什么』。必须画出 NAT 表 + 4 行动作。"
},

"lec17:27": {
  "title": "NAT — 争议",
  "summary": "NAT 一直有争议：(a) Router 应该只看 L3，但 NAT 也动 L4 (port) → 违反 layering；(b) 阻碍 P2P / server（外部无法主动连入）→ 需要 NAT traversal（STUN/TURN/UPnP）；(c) IPv6 才是治本但部署慢；但 NAT 仍广泛使用（家用、4G/5G、企业）。",
  "key_points": [
    "Router 该只看 L3，NAT 改 L4 port → 违反 layering",
    "外部无法主动连入 → 阻碍 P2P (Skype, WebRTC, BitTorrent) 和自托管 server",
    "**NAT traversal**: STUN, TURN, UPnP, ICE",
    "IPv6 解决问题但部署慢（25 年了）",
    "实际：NAT 在家用 + 4G/5G + 企业都广泛使用"
  ],
  "explanation": "**层级违反争议**：\n- L3 (network) 协议应该只处理 IP\n- L4 (transport) 才处理 port\n- NAT 同时改两层 → 违反 end-to-end 和 layering 原则\n\n**P2P 难题**：\n- Skype 早期：用 'super-peer'（有公网 IP）做中继\n- WebRTC：用 STUN 服务器让 NAT 后的 host 发现自己对外的 (IP, port)\n- 复杂工程，但已经成熟（视频通话工作得很好）\n\n**为什么没换 IPv6**：\n- NAT 已经『够用』\n- 换协议要全网协调\n- IPv6 25 年了，2026 年 ~49% 客户端有 IPv6\n\n**真实工程**：NAT 已经成为 Internet 实际架构的一部分，不会消失。"
},

"lec17:28": {
  "title": "Quiz — 最长前缀匹配（LPM）",
  "summary": "给一个 router 的 forwarding table，有 3 条带通配符 (*) 的规则。问：包到达，dst IP 是 `1010.1000.0100.1000`，走哪个 port？",
  "key_points": [
    "Rule 1: 1010.xxxx.xxxx.xxxx (/4) → Port 2",
    "Rule 2: 10xx.xxxx.xxxx.xxxx (/2) → Port 1",
    "Rule 3: 1010.11xx.xxxx.xxxx (/6) → Port 3",
    "Packet: dst = 1010.1000.0100.1000"
  ],
  "explanation": "**做题步骤**：\n\n1. **比对每条规则**：\n   - Rule 1 (/4)：前 4 位 = `1010` → 与包前 4 位 `1010` **匹配** ✓\n   - Rule 2 (/2)：前 2 位 = `10` → 与包前 2 位 `10` **匹配** ✓\n   - Rule 3 (/6)：前 4 位 `1010` 匹配，但位 5-6 应为 `11`，包里是 `10` → **不匹配** ✗\n\n2. **匹配的规则**：Rule 1 (/4) 和 Rule 2 (/2)\n\n3. **选最长**：Rule 1 (/4) > Rule 2 (/2) → 走 **Port 2**\n\n**答案：Port 2**\n\n**核心原理**：当多条规则都匹配时，选『最具体』（前缀位数最多）的。这就是 'Longest Prefix Matching'。\n\n**易错点**：很多人看到 Rule 3 (/6) 比 (/4) 长就直接选，忘了先验证『匹配』。**必须先匹配，再比长度**。\n\n**考点**：这种题 final 和 midterm 都常出。做题时画位级对比图。"
},

}

def main():
    data = json.loads(DETAIL.read_text())
    overwritten = 0
    new = 0
    for key, val in NEW.items():
        if key in data:
            old = data[key]
            # preserve 'important' if existing
            if 'important' in old:
                val['important'] = old['important']
            data[key] = val
            overwritten += 1
        else:
            data[key] = val
            new += 1
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"lec17 rewrite: overwrote {overwritten}, added {new}")

if __name__ == "__main__":
    main()
