#!/usr/bin/env python3
"""Deepen lec20 (SDN + OpenFlow + Link Layer Error Detection)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec20:1": {
  "title": "Quiz — TCP Throughput 公式 ⭐",
  "summary": "AIMD 下 cwnd 锯齿振荡在 W/2 ↔ W，平均 cwnd = 3W/4，throughput = 3W/(4·RTT)。",
  "formula": "$$\\bar{R}_{\\text{TCP}} = \\frac{3W}{4 \\cdot RTT}$$",
  "key_points": [
    "AIMD 下 cwnd 锯齿：从 W/2 线性加到 W，丢包切半，循环",
    "平均 cwnd = (W/2 + W) / 2 = 3W/4",
    "每 RTT 发 cwnd bytes",
    "平均 throughput = 平均 cwnd / RTT = 3W/(4·RTT)"
  ],
  "explanation": "### 推导（必会）\n\n忽略 slow start，只看 congestion avoidance 阶段：\n\ncwnd 在丢包后从 W（峰值）切半到 W/2，然后每 RTT +1 MSS 线性增长，直到再次丢包到 W → 又切半...\n\n**几何上**：cwnd 是一条锯齿，从 W/2 上升到 W，循环。\n\n**平均高度** = (最小 + 最大) / 2 = (W/2 + W) / 2 = **3W/4**\n\n**每 RTT 发送字节数** ≈ cwnd（满 window 推完一次）\n\n**平均吞吐量** = 3W/4 bytes/RTT = **3W / (4·RTT)**\n\n### 完整 throughput 公式（更准的）\n包括包大小 MSS 和 loss event rate p：\nB ≈ MSS / (RTT · √p)（Mathis formula）\n\n但 4119 范围只需 3W/(4·RTT) 这个版本。\n\n### 例\nW = 16 KB, RTT = 100 ms：\nthroughput = 3 × 16 KB / (4 × 100 ms) = 12 KB / 100 ms = **120 KB/s = 960 kbps**\n\n### 考法（高频）\n- 给 W 和 RTT，算 throughput\n- 反过来：给 throughput，估 W\n- 解释为什么是 3W/4 而不是 W/2 或 W",
  "gotcha": "不要写成 W/(2·RTT) 或 W/RTT —— 必须是 **3W/(4·RTT)**。"
},

"lec20:2": {
  "title": "Network Layer: SDN — 章节封面",
  "summary": "进入 SDN。前面学了 IP（数据面）和路由协议（控制面），现在学集中式控制面。"
},

"lec20:3": {
  "title": "Generalized Forwarding — Match + Action ⭐",
  "summary": "Router 不只看 dst IP，可以匹配 packet 任意 header 字段并执行多种动作。",
  "key_points": [
    "**Match**：link/network/transport 任意字段（含通配 *）",
    "**Action**：forward port / drop / modify / send to controller",
    "**Priority**：多条匹配时选最高",
    "**Counters**：字节 + 包数统计"
  ],
  "explanation": "### 传统 vs 通用 forwarding\n传统 router 只按 dst IP 做最长前缀匹配 → 单一行为模式。\n\nGeneralized forwarding 让一个表能表达：\n- Router：match dst IP\n- Firewall：match dst port\n- Switch：match dst MAC\n- NAT：match (src IP, src port)，action rewrite\n\n→ 所有 box 都能用同一抽象。这是 SDN 革命的基础。\n\n### 一个 Match 例\n```\nmatch: src IP = 10.3.*.*, dst IP = 10.2.*.*\naction: forward to port 3\npriority: 1000\n```\n\n### 多个 Action 可以组合\n- 同时 modify + forward（NAT 重写）\n- 同时 forward + count（监控）\n- 还可以 send-to-controller（让 controller 决策）\n\n### 考法\n- 解释 match+action 抽象\n- 给场景写 flow table entry"
},

"lec20:4": {
  "title": "Flow Table Abstraction ⭐",
  "summary": "Flow = 一组 header 字段值；flow table 包含 match + action + priority + counters。",
  "key_points": [
    "Flow 由 header 字段值定义",
    "Match: pattern（含 *）",
    "Action: drop / forward / modify / to-controller",
    "Priority: 解决重叠规则",
    "Counters: 统计 bytes 和 packets"
  ]
},

"lec20:5": {
  "title": "Flow Table 具体例",
  "summary": "三条规则：src=*.*.*.*, dst=3.4.*.* → forward(2)；src=1.2.*.* → drop；src=10.1.2.3 → to-controller。"
},

"lec20:6": {
  "title": "OpenFlow Flow Table Entry — 11 个 match 字段",
  "summary": "L2-L4 全字段都能匹配，action 灵活组合。",
  "key_points": [
    "Match 11 字段：ingress port, src/dst MAC, Ether type, VLAN ID/Pri, IP src/dst/proto/ToS, TCP/UDP src/dst port",
    "Action: forward port(s), drop, modify, encapsulate to controller"
  ]
},

"lec20:7": {
  "title": "OpenFlow 例 — Router / Firewall / Block sender",
  "summary": "Match dst IP 转发；match dst port=22 drop（block SSH）；match src=128.119.1.1 drop（block 某主机）。",
  "explanation": "### Router 行为\n```\nmatch: dst IP = 51.6.0.8\naction: forward port 6\n```\n\n### Firewall: 屏蔽 SSH\n```\nmatch: TCP dst port = 22\naction: drop\n```\n\n### Block 某 src IP\n```\nmatch: src IP = 128.119.1.1\naction: drop\n```\n\n→ 用 flow table 一个抽象统一所有功能。"
},

"lec20:8": {
  "title": "OpenFlow 例 — L2 destination forwarding（Switch 行为）",
  "summary": "Match dst MAC = 22:A7:23:11:E1:02 → forward port 3。Switch 也能用 flow table 实现。"
},

"lec20:9": {
  "title": "OpenFlow Abstraction — 统一各种盒子 ⭐⭐",
  "summary": "Router / Firewall / Switch / NAT 都能用 match+action 表达。",
  "key_points": [
    "**Router**: match longest dst IP → forward",
    "**Firewall**: match IP+port → permit/deny",
    "**Switch**: match dst MAC → forward",
    "**NAT**: match (IP, port) → rewrite"
  ],
  "explanation": "### 这页是 SDN 的核心思想\n\n以前每个网络盒子都是『专门设备』：\n- Router 公司卖路由器\n- Firewall 公司卖防火墙\n- NAT 单独硬件\n- ...\n\n各自封闭、专用 OS（Cisco IOS、Juniper Junos）、贵。\n\n**SDN/OpenFlow 说**：所有这些行为都能用 match+action 表达。那硬件可以统一成 generic switch，行为由 controller 下发的 flow table 决定。\n\n→ 硬件商品化，软件开源，价格暴跌。\n\n### 类比 mainframe → PC\n- 以前：每种应用一套封闭专用机\n- PC 革命：硬件标准化，OS 通用，应用层百花齐放\n\nSDN 把这套搬到网络。"
},

"lec20:10": {
  "title": "OpenFlow 跨多 switch — Network-wide 行为",
  "summary": "Controller 在多 switch 上下发协调的 flow rule，实现整体路径。"
},

"lec20:11": {
  "title": "OpenFlow 多 switch 实例",
  "summary": "h5/h6 → h3/h4 经 s1 → s2，各 switch 上各下发不同 flow entries。"
},

"lec20:12": {
  "title": "Generalized Forwarding 小结",
  "summary": "Match + Action 是网络可编程的基础，是 SDN / P4 / 现代网络架构的根。",
  "key_points": [
    "匹配多层字段",
    "本地多种动作",
    "『编程』整个网络行为",
    "历史根：active networking；现代演进：P4（更可编程）"
  ]
},

"lec20:13": {
  "title": "Network Layer: SDN — 子节封面",
  "summary": "下面深入 SDN control plane。"
},

"lec20:14": {
  "title": "SDN 动机 — 传统网络的问题",
  "summary": "传统 router 集成所有功能 + 厂商私有，难创新。",
  "key_points": [
    "Router = 硬件 + IOS + 私有路由协议实现，封闭",
    "Middlebox（firewall/LB/NAT/...）各自独立硬件",
    "管理困难：每台 router 单独配置",
    "2005 起业界重新思考"
  ]
},

"lec20:15": {
  "title": "Per-router Control Plane（传统）",
  "summary": "每个 router 独立跑路由算法 + 自己填 FT。"
},

"lec20:16": {
  "title": "SDN Control Plane ⭐",
  "summary": "Remote controller 算 FT，下发到所有 routers。",
  "key_points": [
    "Controller 全局视图",
    "Routers 退化为执行 FT 的 dumb pipe",
    "南向 API（controller → switch）",
    "北向 API（应用 → controller）"
  ]
},

"lec20:17": {
  "title": "SDN — 为什么集中？四大动机 ⭐",
  "summary": "易管理 + 可编程 + 避免分布式协议复杂度 + 开放避免锁厂商。",
  "key_points": [
    "**易管理**：全局视图，避免分布式协议带来的复杂配置/调试",
    "**可编程**：table-based forwarding → 计算 FT 是普通算法问题",
    "**集中算容易**：直接全局 Dijkstra；分布式算复杂（要同步 + 容错）",
    "**开放**：非私有，鼓励 100 朵花齐放"
  ],
  "explanation": "### 集中 vs 分布的 tradeoff\n**分布优点**：自然容错（一个节点挂另一个还能跑）。\n**分布缺点**：算法复杂（同步、收敛、消息开销）、配置碎片化、难全局优化。\n\nSDN 选集中是因为现代 controller 也可以做成分布式（多副本 + 一致性协议），单点故障可以通过工程手段缓解，换来管理简化和算法简化的收益。\n\n### Google B4 案例\nGoogle 用 SDN 控制 B4（连接所有 datacenter 的 WAN）。流量工程让链路利用率从 30-40% 提到 90%+。"
},

"lec20:18": {
  "title": "SDN 类比 — Mainframe → PC 革命",
  "summary": "Router = 老 mainframe（封闭）→ SDN = PC（硬件 + OS + 应用分离）。",
  "explanation": "### 类比表\n\n| | 老 router | SDN |\n|---|---|---|\n| 硬件 | 专用 | 通用 |\n| OS | Cisco IOS（封闭）| Linux/开源 |\n| 应用 | 内置路由协议 | 独立 controller apps |\n| 创新速度 | 慢 | 快 |\n| 厂商 | 几家寡头 | 百花齐放 |"
},

"lec20:19": {
  "title": "SDN — 三大设计原则 ⭐",
  "summary": "Generalized forwarding + Control/Data 分离 + Programmable。",
  "key_points": [
    "**1. Generalized flow-based forwarding (OpenFlow)**",
    "**2. Control plane / Data plane 分离**",
    "**3. Control plane 在 data plane 外部，可编程**",
    "**4. 应用层（外部）写 control logic**"
  ],
  "explanation": "### 4 个特征的来源\n\n1. Match+action 替代私有路由表\n2. Control plane（决策）跟 data plane（执行）解耦\n3. Controller 在远程，可统一升级\n4. App 写 control logic（routing, firewall, LB），不需要改 switch 软件\n\n### 考法\n『SDN 关键架构特征是什么？』必背 4 点。"
},

"lec20:20": {
  "title": "SDN — Data Plane Switches",
  "summary": "Commodity hardware，flow table 由 controller 算 + 下发。"
},

"lec20:21": {
  "title": "SDN Controller — Network OS",
  "summary": "维护网络状态 + 北向 API（给应用）+ 南向 API（控 switch）+ 分布式实现容错。"
},

"lec20:22": {
  "title": "SDN — Network Control Apps",
  "summary": "应用层 = 大脑：routing / firewall / load balance。可由第三方写，不绑厂商。"
},

"lec20:23": {
  "title": "SDN Controller 内部组成",
  "summary": "接口层 + 状态管理 + 通信层。",
  "key_points": [
    "**接口层**（北向）：抽象（network graph, RESTful API, intent）",
    "**状态管理**：分布式 DB，维护拓扑、host info、统计、flow tables",
    "**通信层**（南向）：OpenFlow / SNMP，控制 switches"
  ]
},

"lec20:24": {
  "title": "OpenFlow Protocol",
  "summary": "Controller ↔ switch 通过 TCP 上的 OpenFlow 协议交互。",
  "key_points": [
    "TCP 长连接（可选 TLS 加密）",
    "三类消息：controller→switch / switch→controller / symmetric"
  ]
},

"lec20:25": {
  "title": "OpenFlow — Controller → Switch Messages",
  "summary": "Features / Configure / Modify-state / Packet-out。",
  "key_points": [
    "**Features**: 查 switch 能力",
    "**Configure**: 改 switch 参数",
    "**Modify-state**: 增/删/改 flow entry（核心）",
    "**Packet-out**: controller 让 switch 从某 port 发包"
  ]
},

"lec20:26": {
  "title": "OpenFlow — Switch → Controller Messages",
  "summary": "Packet-in / Flow-removed / Port status。",
  "key_points": [
    "**Packet-in**: switch 不知道怎么处理 → 交 controller 决策",
    "**Flow-removed**: 表项被删（如超时）",
    "**Port status**: link up/down 通知"
  ]
},

"lec20:27": {
  "title": "SDN 控制 / 数据面交互例 (1)",
  "summary": "Link 失败 → port status → controller → Dijkstra 重算。"
},

"lec20:28": {
  "title": "SDN 交互例 (2)",
  "summary": "新路径算完 → controller 用 OpenFlow 下发新 FT 到相关 switches。"
},

"lec20:29": {
  "title": "Google ORION SDN",
  "summary": "Google 数据中心 + WAN 的 SDN 控制平面，NSDI 2021。"
},

"lec20:30": {
  "title": "OpenDaylight (ODL) Controller",
  "summary": "开源 SDN controller，Java 写，Linux Foundation 主持。"
},

"lec20:31": {
  "title": "ONOS Controller",
  "summary": "另一开源 controller，重视分布式可靠性 + intent framework。"
},

"lec20:32": {
  "title": "SDN 当前挑战",
  "summary": "Control plane 硬化 + 可靠 + 安全 + 扩展到跨 AS + 5G 应用。",
  "key_points": [
    "Control plane 可靠性、性能、安全",
    "跨 AS 扩展（目前 SDN 主要单 AS 内）",
    "5G/边缘计算应用"
  ]
},

"lec20:33": {
  "title": "Data Link Layer — 章节封面",
  "summary": "进入链路层。"
},

"lec20:34": {
  "title": "Link Layer 在协议栈中的位置",
  "summary": "L2 在 IP 下、物理层上。例：Ethernet, 802.11, PPP。"
},

"lec20:35": {
  "title": "From Network to Single Link",
  "summary": "每跳可能用不同链路技术（Ethernet, WiFi, fiber）。链路层隐藏这些差异给上层。"
},

"lec20:36": {
  "title": "Data Link Layer 实现位置",
  "summary": "L2 跑在 NIC（网卡 / adapter）里。Sender 封 datagram → frame；receiver 解 frame → datagram。"
},

"lec20:37": {
  "title": "Link Layer Services（复习）",
  "summary": "Framing + Error detection/correction + MAC + Reliable delivery。"
},

"lec20:38": {
  "title": "Error Detection — 概念",
  "summary": "信号衰减 + 噪声会引入 bit 错；用冗余信息检测。",
  "key_points": [
    "错的来源：电干扰、热噪声、信号衰减",
    "解药：传冗余信息检测",
    "Trade-off：开销 vs 检测能力",
    "三种技术：parity / checksum / CRC"
  ]
},

"lec20:39": {
  "title": "Parity Check — 1-bit",
  "summary": "加 1 个 bit 让总 1 数为奇/偶。",
  "key_points": [
    "**Odd parity**: 总 1 数为奇",
    "**Even parity**: 总 1 数为偶",
    "**只能检测奇数个 bit 错**（偶数翻转互相抵消）",
    "简单但弱"
  ],
  "explanation": "### 例\n数据 0101011（7 bit，4 个 1）\n- Odd parity：加 1 让总 1 = 5（奇）→ 01010111\n- Even parity：加 0 让总 1 = 4（偶）→ 01010110\n\n### 弱点\n如果传输时翻转 2 个 bit（偶数次），奇偶性不变，检测失败。\n\n→ Parity 只能可靠检测单 bit 错。下一页讲 2D parity 改进。"
},

"lec20:40": {
  "title": "Parity Check — 2D",
  "summary": "数据排成 i×j 矩阵，每行 + 每列各加 1 个 parity bit。能检测 + 纠正单 bit 错。",
  "key_points": [
    "i × j 数据矩阵 + 1 行 parity + 1 列 parity",
    "行 parity 错 + 列 parity 错 → 定位错的位",
    "翻转那一位 → 纠错完成"
  ],
  "explanation": "### 例（4x5 + parity，假设 even parity）\n```\n数据：     parity:\n1 0 1 0 1   1\n1 1 1 1 0   0\n0 1 1 1 0   1\n1 0 1 0 1   1\n--------    -\n1 0 0 0 0   0  ← column parity\n```\n\n如果传输后变成（第 2 行第 4 列翻转）：\n```\n1 0 1 0 1   1   ← row parity OK\n1 1 1 0 0   0   ← row parity wrong\n0 1 1 1 0   1   ← row parity OK\n1 0 1 0 1   1   ← row parity OK\n--------    -\n1 0 0 1 0   0   ← col parity wrong on col 4\n```\n\nRow 2 + Col 4 都报错 → 错在 (2, 4) → 翻转该位 → 纠错。\n\n### 局限\n仍只能纠单 bit 错。多 bit 错可能误诊。"
},

"lec20:41": {
  "title": "Error Detection — Checksum",
  "summary": "把数据当 16-bit 字累加（无进位），传 sum。TCP/UDP/IP 都用这个。",
  "explanation": "### 工作流程\nSender:\n1. 数据切成 16-bit word\n2. 全部相加，溢出位 wrap around 加到末尾\n3. 取反（one's complement）作为 checksum\n4. 发送 (data, checksum)\n\nReceiver:\n1. 把数据 + checksum 一起加\n2. 结果应全 1（如果取反过）→ 全对\n3. 任何位错都会让和不全 1\n\n### 比 CRC 弱\nChecksum 漏检率高（某些错会互相抵消）。但实现简单，TCP/UDP 用它够用（加上 IP 链路层有 CRC + ARQ 兜底）。"
},

"lec20:42": {
  "title": "CRC — 概念 ⭐",
  "summary": "用模 2 除法（XOR），D·2^r mod G = R。",
  "formula": "$$R = (D \\cdot 2^r) \\bmod G$$",
  "key_points": [
    "G = (r+1) bit 生成多项式（约定）",
    "D = 数据，r 个 CRC bit",
    "Sender 发 (D, R)",
    "Receiver 算 (D·2^r XOR R) mod G == 0 ？"
  ],
  "explanation": "### 直觉\n把数据看成大整数，找一个余数 R 让『D 左移 r 位 + R』正好被 G 整除。\n\nReceiver 收到后做同样的除法，余数应为 0。任何 bit 错会让余数 ≠ 0。\n\n### 模 2 运算\n不是真除法。**减法 = XOR**（无借位，无进位）。所以 CRC 用 XOR 实现，硬件极简。\n\n### 检错能力\nCRC 能检测 **所有 ≤ r 位的突发错**。例如 r=16 的 CRC-16 能检测所有 16 bit 以内的连续错。强于 parity 和 checksum。\n\n### 用途\n- Ethernet frame 末尾 4 byte CRC\n- 各种链路层协议\n- 文件存储 (CRC-32)"
},

"lec20:43": {
  "title": "CRC — 计算例 ⭐",
  "summary": "G=1001, D=101011, r=3。手算长除法（XOR）找 R。",
  "key_points": [
    "把 D 后面接 r 个 0：101011 → 101011000",
    "用 G 做 modulo-2 长除法（XOR 替代减法）",
    "余数 R（r 位）= CRC",
    "发 (D, R) = 101011 + R"
  ],
  "explanation": "### 详细手算\n```\nD = 101011, r = 3, G = 1001\nD · 2^3 = 101011000\n\n长除法（XOR 替代减法）：\n\n  101011000\n  1001       ← 第 1 位是 1，XOR G\n  ────\n   01101                              \n    1001     ← 第 2 位是 0 跳过；第 3 位是 1，XOR G（左对齐到这位）\n    ────\n    01001\n     1001    ← 第 4 位是 1，XOR\n     ────\n     00001000\n         1001 ← 第 7 位是 1，XOR\n         ────\n          110  ← 这就是余数 R（3 bit）\n```\n\n注意：实际算法中『当前最高位是 1 就 XOR G，0 就跳过，逐位右移』。\n\n### 验证\nReceiver 收到 (D=101011, R=110)：\n- 算 D·2^3 XOR R = 101011000 XOR 110 = 101011110\n- 用 G=1001 长除 101011110\n- 如果传输无错，余数应为 0\n\n### 考法\n- 给 G、D 让你算 R\n- 给 (D, R) 让你验证有没有错"
},

"lec20:44": {
  "title": "Quiz — DV 3 节点收敛（接 lec21）",
  "summary": "3 节点 DV，多少轮收敛。"
},

}

def main():
    data = json.loads(DETAIL.read_text())
    data.update(NEW)
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"updated {len(NEW)} entries; total now {len(data)}")

if __name__ == "__main__":
    main()
