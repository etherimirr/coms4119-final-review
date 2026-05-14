#!/usr/bin/env python3
"""Full per-page rewrite for lec20 (Generalized Forwarding + SDN + Link Layer + Error Detection, 44 pages)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec20:1": {
  "title": "Quiz: TCP Throughput",
  "summary": "(承接 lec19) AIMD 下 sliding window 在 W/2 ↔ W 锯齿振荡。忽略 slow start。求平均 throughput 关于 W 和 RTT。\n\n**答**: 平均 sliding window = (W/2+W)/2 = 3W/4，平均每 RTT 发 3W/4 bytes，throughput = **3W/(4·RTT)**。",
  "key_points": [
    "AIMD 锯齿：cwnd 从 W/2 升到 W 后切半",
    "平均 cwnd = 3W/4",
    "每 RTT 发 cwnd bytes",
    "Throughput = 3W/(4·RTT)"
  ],
  "explanation": "**这是必背公式**。详见 lec19:25 推导。"
},

"lec20:2": {
  "title": "Network Layer: SDN — 章节封面",
  "summary": "进入 SDN 部分。子目录：(1) SDN data plane = generalized forwarding（match+action, OpenFlow）；(2) SDN control plane。",
  "key_points": ["SDN 章节开始", "包括 data plane (match+action) 和 control plane"]
},

"lec20:3": {
  "title": "Generalized Forwarding — Match Plus Action",
  "summary": "复习：每 router 有 forwarding table (aka flow table)。**Match + action** 抽象：匹配 packet header 的 bit，执行动作。传统 = destination-based forwarding。**Generalized forwarding**：能匹配任意 header 字段；能执行多种 action（drop / copy / modify / log）。",
  "key_points": [
    "Match + Action 抽象",
    "Destination-based forwarding 是特例（只 match dst IP）",
    "Generalized: 任意 header 字段都能 match",
    "Action 不只 forward: drop / copy / modify / log"
  ],
  "explanation": "**传统 vs 通用 forwarding**：\n- **传统**: router 只 match dst IP，action 是 forward 到某 port\n- **通用 (Generalized)**: match 任意字段（src IP, port, MAC, VLAN, ...），action 灵活（drop/forward/modify/...）\n\n**为什么需要**：现代网络要做 firewall、NAT、load balancer、监控... 这些 box 行为各异，但都可以归纳为 match+action。\n\n**这就是 OpenFlow 的核心思想**：把所有 box 统一为 match+action 模型。"
},

"lec20:4": {
  "title": "Flow Table Abstraction",
  "summary": "**Flow** = 由 header field 值定义的一组 packets（如『src IP = 1.2.3.4 的所有包』）。Flow table 是 router 的 match+action 规则集。每条规则：(a) **match**: header pattern (可含 *); (b) **action**: drop / forward / modify / to-controller; (c) **priority**: 重叠规则用；(d) **counters**: 字节 + 包数。",
  "key_points": [
    "**Flow** = header field 值的组合定义",
    "Flow table entry: match + action + priority + counters",
    "Action: drop / forward / modify / to-controller",
    "Priority 解决重叠规则",
    "Counters 监控用"
  ]
},

"lec20:5": {
  "title": "Flow Table — 具体例",
  "summary": "示例 3 条规则：(1) src=*.*.*.*, dst=3.4.*.* → forward port 2；(2) src=1.2.*.*, dst=*.*.*.* → drop；(3) src=10.1.2.3 → send to controller。",
  "key_points": [
    "Rule 1: dst 是 3.4.*.* → forward 2",
    "Rule 2: src 是 1.2.*.* → drop",
    "Rule 3: src=10.1.2.3 → to controller"
  ],
  "explanation": "**这就像一个统一的 ACL + router + monitoring 规则**。每个 packet 经过 flow table：\n- 找匹配的规则（priority 最高）\n- 执行对应 action\n\n这种统一让网络设备硬件可以非常通用化（不再需要专门的 firewall / router / NAT 硬件）。"
},

"lec20:6": {
  "title": "OpenFlow — Flow Table Entry 11 个字段",
  "summary": "OpenFlow 标准支持 11 个 match 字段（L2/L3/L4 全覆盖）。每条 entry: match + action + stats。\n\nMatch 字段：Ingress port, Src/Dst MAC, Eth Type, VLAN ID/Pri, IP Src/Dst/Proto/ToS, TCP/UDP src/dst port。Action: forward to port(s) / drop / modify header / encapsulate + to controller。",
  "key_points": [
    "**11 个 match 字段**:",
    "  - L1: Ingress port",
    "  - L2: Src MAC, Dst MAC, Eth Type, VLAN ID, VLAN Pri",
    "  - L3: IP Src, IP Dst, IP Proto, IP ToS",
    "  - L4: TCP/UDP src port, dst port",
    "**4 类 Action**:",
    "  ① Forward to port(s)",
    "  ② Drop",
    "  ③ Modify fields in headers",
    "  ④ Encapsulate + forward to controller",
    "**Stats**: packet + byte counters"
  ],
  "explanation": "**完整 11 字段表**让 OpenFlow 能精确表达：\n- 防火墙规则（dst port = 22 → drop）\n- 负载均衡（dst IP = X → forward to one of {A, B, C}）\n- NAT（src IP, port → modify）\n- 监控（match → counter）\n- ACL（src MAC → drop）\n\n**任何 packet handling 都能用 11 字段 + action 表达**。"
},

"lec20:7": {
  "title": "OpenFlow 例 — Router / Firewall",
  "summary": "示范用 flow table 写 router 和 firewall 行为：\n\n(1) **Destination-based forwarding (router)**: match `dst IP = 51.6.0.8` → forward port 6.\n\n(2) **Firewall block port 22 (SSH)**: match `dst TCP port = 22` → drop.\n\n(3) **Block specific src**: match `src IP = 128.119.1.1` → drop.",
  "key_points": [
    "Router 行为：match dst IP → forward port",
    "Firewall 行为：match port 22 → drop（block SSH）",
    "Source filter: match src IP → drop"
  ],
  "explanation": "**关键观察**：传统上你需要 *router* + *firewall* 两台设备。OpenFlow 用一张 flow table 在一台设备上就能做。\n\n**真实场景**：data center 里所有 hypervisor 都跑 Open vSwitch（OVS），用 OpenFlow flow table 同时做 forwarding + ACL + VLAN + tunneling 多种事。"
},

"lec20:8": {
  "title": "OpenFlow 例 — L2 Destination-based Forwarding (Switch)",
  "summary": "Switch 行为也能用 flow table 写：match `dst MAC = 22:A7:23:11:E1:02` → forward port 3。",
  "key_points": [
    "Switch 用 dst MAC 转发",
    "Flow table entry: match dst MAC → forward port"
  ],
  "explanation": "**所以 switch 也是 match+action 的特例**：只 match dst MAC，action 是 forward。\n\n→ 硬件可以统一为『flow table executor』，所有不同 box 的差异只在『写什么规则进去』。"
},

"lec20:9": {
  "title": "OpenFlow 抽象 — 统一各种盒子",
  "summary": "Match + Action 抽象统一不同设备：\n\n- **Router**: match longest dst IP prefix → forward port\n- **Firewall**: match IP+port → permit/deny\n- **Switch**: match dst MAC → forward port\n- **NAT**: match IP+port → rewrite IP+port",
  "key_points": [
    "Router: match dst IP → forward",
    "Firewall: match IP+port → drop/permit",
    "Switch: match dst MAC → forward",
    "NAT: match (IP, port) → rewrite"
  ],
  "explanation": "**SDN 革命的核心**：以前每种 box 是『专门设备 + 专门 OS + 专门协议』。OpenFlow 说『所有 box 行为都能用 match+action 表达』→ 硬件可以商品化，软件可以开源。\n\n**类比**：mainframe → PC 革命，硬件标准化 + OS 通用 + 应用百花齐放。"
},

"lec20:10": {
  "title": "OpenFlow 例 — 跨多 Switch Orchestration",
  "summary": "Controller 同时管理多个 switch 的 flow tables，实现 network-wide 行为。例：让 h5 和 h6 的流量经 s1 → s2，到达 h3 或 h4。",
  "key_points": [
    "Controller 同时控制多 switch",
    "Network-wide policy 由 controller 编排",
    "示例: 控制流量 h5/h6 → s1 → s2 → h3/h4"
  ],
  "explanation": "**这是 SDN 真正的力量**：单点 controller 看到全局，可以协调所有 switch 实现复杂行为（如 load balancing, traffic engineering, security policies），用同一个 flow table 抽象。"
},

"lec20:11": {
  "title": "OpenFlow 多 Switch 实例 — 详细规则",
  "summary": "为前一页例子写出具体 flow table 规则。\n\n- 中间 switch s1: match IP src=10.3.*.*, dst=10.2.*.* → forward 3\n- 边缘 switch（h5 一侧）：match ingress=1, IP src=10.3.*.* → forward 4\n- 边缘 switch（h3 一侧）：match ingress=2 → forward 3 或 4",
  "key_points": [
    "每 switch 不同规则",
    "Controller 统一协调",
    "示例展示如何用 match+action 实现路径选择"
  ]
},

"lec20:12": {
  "title": "Generalized Forwarding 总结",
  "summary": "Match + Action 抽象 = 现代网络可编程基础。匹配任意层字段（L2/L3/L4），本地多种 action，能编程整个网络行为。是简单形式的『network programmability』。历史根：active networking；现代演进：P4（更可编程）。",
  "key_points": [
    "Match + Action 统一所有设备",
    "Programmable per-packet processing",
    "历史: active networking",
    "现代: P4 (更可编程)"
  ],
  "explanation": "**P4 是什么**：比 OpenFlow 更通用的 'programmable data plane' 语言。OpenFlow 限定 11 个 match 字段，P4 让你自定义任意 header 格式 + parsing + match。\n\n参考：[p4.org](http://p4.org)\n\n**学术界 → 工业界**：Google、Microsoft、Intel 都在用 P4 部署可编程交换机。"
},

"lec20:13": {
  "title": "Network Layer: SDN — 子节封面",
  "summary": "进入 SDN control plane 详讲。前面讲了 SDN data plane (match+action)；现在讲 control plane (controller 架构 + OpenFlow 协议)。",
  "key_points": ["子节过渡，进入 control plane"]
},

"lec20:14": {
  "title": "SDN — 动机",
  "summary": "Internet network layer 历史上 = distributed per-router control。Monolithic router：硬件 + 厂商私有 OS（Cisco IOS）+ 私有协议实现（IP/RIP/IS-IS/OSPF/BGP）。各种 middleboxes 各自独立。**~2005 起业界重新思考**：能否把 CP 抽出来？",
  "key_points": [
    "传统 router = monolithic（硬件 + IOS + 协议）",
    "Middleboxes 各自独立（firewall, LB, NAT, ...）",
    "封闭、私有、慢创新",
    "~2005 开始 rethink"
  ],
  "explanation": "**问题诊断**：\n- 路由器是『一体机』：硬件 + OS + 协议都 vendor 锁\n- Cisco IOS、Juniper Junos 是封闭的\n- 部署一个新功能（比如 traffic engineering）非常困难\n- Middleboxes（防火墙、LB、NAT）各自专门硬件、互不兼容\n\n**SDN 解决**：把硬件和软件分离（类似 PC 革命）。"
},

"lec20:15": {
  "title": "Per-router Control Plane（复习 — 传统模式）",
  "summary": "传统：每 router 独立跑路由算法 + 填 forwarding table。Router = 路由算法 + 本地 FT。Routing 在 control plane，forwarding 在 data plane。",
  "key_points": [
    "每 router 跑自己的路由算法",
    "Algorithm 间互相通信",
    "本地填 FT"
  ]
},

"lec20:16": {
  "title": "SDN Control Plane（新架构）",
  "summary": "**Remote controller** 集中计算所有 router 的 FT，通过 SDN protocol（如 OpenFlow）下发给 routers/switches。Switches 退化为执行 FT 的 'dumb pipe'。",
  "key_points": [
    "Remote controller 全局视图",
    "Controller 算 FT，下发到所有 router",
    "Routers/switches 退化为 dumb pipe",
    "OpenFlow 是常用的 controller↔switch 协议"
  ]
},

"lec20:17": {
  "title": "SDN — 为什么集中？4 大动机",
  "summary": "(1) **更易管理**: 全局视图，避免 router misconfig，更灵活控流；(2) **Table-based forwarding (OpenFlow) 允许编程 router**；(3) **集中编程比分布式编程容易**: 算法跑在 controller，结果下发；分布式 controller 算法（如 OSPF）复杂；(4) **Open (非私有) 实现**: 鼓励创新。",
  "key_points": [
    "① 更易管理（全局视图 + 灵活控流）",
    "② Table-based forwarding 允许 programming",
    "③ 集中算法 < 分布式算法 复杂度",
    "④ Open 鼓励创新（'让千朵花齐放'）"
  ],
  "explanation": "**集中 vs 分布式 trade-off**：\n- 分布式优点：天然容错（一节点挂别人还能跑）\n- 分布式缺点：算法复杂（同步、收敛、消息开销）、配置碎片、难全局优化\n\n**SDN 选集中**：因为 controller 可以做成分布式（多副本 + 一致性协议），单点故障可通过工程手段缓解，换来管理简化和算法简化的收益。\n\n**Google B4**：Google 用 SDN 控制 B4（连接 datacenter 的 WAN）。流量工程让链路利用率从 30-40% 提到 90%+。"
},

"lec20:18": {
  "title": "SDN — 类比 Mainframe → PC 革命",
  "summary": "类比 1980s mainframe 到 PC 转型：specialized applications 加 specialized OS 加 specialized hardware → 转变为 open interfaces + 通用硬件 + 多 OS 选择（Windows/Linux/Mac）+ 微处理器。垂直集成 → 水平分层，慢创新 → 快创新，小行业 → 大行业。",
  "key_points": [
    "前：垂直集成（封闭、私有）",
    "后：水平分层（开放接口）",
    "前：慢创新 + 小行业",
    "后：快创新 + 大行业",
    "Slide credit: N. McKeown (SDN pioneer)"
  ],
  "explanation": "**Mainframe 时代**：每家公司（IBM, DEC, Burroughs）卖完整套件（硬件 + OS + 应用），互不兼容，贵。\n\n**PC 时代**：硬件（Intel/AMD）+ OS（Microsoft/Linux）+ 应用（独立软件商）分离，标准接口（x86 ISA），价格大降，创新爆炸。\n\n**网络对应**：\n- 旧 router = mainframe\n- SDN switch + controller + apps = PC + OS + apps\n\n**N. McKeown** 是斯坦福教授，OpenFlow 主推动者之一。"
},

"lec20:19": {
  "title": "SDN — 关键 4 特征",
  "summary": "**4 大设计原则**：(1) Generalized 'flow-based' forwarding（如 OpenFlow）；(2) Control + data plane 分离；(3) Control plane functions external to data-plane switches；(4) Programmable control applications。",
  "key_points": [
    "① **Generalized flow-based forwarding** (OpenFlow)",
    "② **Control/Data plane 分离**",
    "③ **Control 在 data plane 外部**（remote controller）",
    "④ **Programmable** control applications（外部 app 写逻辑）"
  ],
  "explanation": "**这 4 条是 SDN 的『宪法』**：\n\n1. Match+action 替代私有路由表\n2. CP（决策）跟 DP（执行）解耦\n3. Controller 在远程，可统一升级\n4. App 写 control logic（routing, firewall, LB），不需要改 switch 软件\n\n**考点**：『SDN 关键架构特征是什么？』必背 4 点。"
},

"lec20:20": {
  "title": "SDN — Data Plane Switches",
  "summary": "Data plane switches: **快、简单、commodity hardware**，硬件实现 generalized data-plane forwarding。Flow table 由 controller 计算 + 安装。API 用于 table-based control（如 OpenFlow）—— 定义『可控的 vs 不可控的』。Protocol 让 controller 跟 switch 通信。",
  "key_points": [
    "Switches = commodity hardware, fast + simple",
    "FT 由 controller 计算 + 下发",
    "API 定义可控范围（OpenFlow）",
    "Switch-controller protocol"
  ]
},

"lec20:21": {
  "title": "SDN Controller (Network Operating System)",
  "summary": "SDN controller = 'network OS'：维护网络状态 + 上面跟 apps（北向 API）+ 下面跟 switches（南向 API）通信 + 分布式实现以保证性能、可扩展、容错。",
  "key_points": [
    "维护网络状态信息",
    "北向 API (northbound): app → controller",
    "南向 API (southbound): controller → switch (OpenFlow)",
    "分布式实现 → 容错 + 扩展"
  ],
  "explanation": "**类比 PC OS**：Linux/Windows 维护设备状态 + 上面跟 app 通信（system call）+ 下面跟硬件通信（driver）。SDN controller 同理。\n\n**容错**：单 controller 失败 = 全网瘫痪。所以实际部署分布式 controller（如 ONOS, Google ORION），多副本一致性协议（Paxos/Raft）。"
},

"lec20:22": {
  "title": "SDN — Network Control Applications",
  "summary": "App = control plane 的『大脑』。实现 control 功能用 controller 提供的低层 service/API。Apps 是 **unbundled** —— 可由第三方提供，独立于路由 vendor 或 controller。",
  "key_points": [
    "Apps 是 'brains of control'",
    "用 controller 暴露的低层 API",
    "Unbundled: 第三方可写",
    "独立于 router/switch/controller vendor"
  ],
  "explanation": "**例**：你不需要等 Cisco 给你写 traffic engineering 算法。你可以自己写一个 Python 程序，通过 controller 的北向 API 控制网络。\n\n这就是『network as code』的雏形。"
},

"lec20:23": {
  "title": "SDN Controller — 内部组件",
  "summary": "**Controller 内部 3 层**：\n\n(1) **Interface layer**: 对 control apps 暴露的抽象（network graph, RESTful API, intent）。\n\n(2) **Network-wide state management**: 状态分布式 DB，保存 links 信息、host 信息、switches 信息。\n\n(3) **Communication layer**: 跟 controlled devices 通信（OpenFlow, SNMP, OVSDB）。",
  "key_points": [
    "① Interface layer (北向): graph, RESTful API, intent",
    "② State management: 分布式 DB",
    "③ Communication layer (南向): OpenFlow, SNMP, OVSDB",
    "Goal: 高可用、容错、可扩展"
  ]
},

"lec20:24": {
  "title": "OpenFlow Protocol",
  "summary": "OpenFlow 在 controller 和 switch 之间运行。**TCP 上**传消息（可选加密）。3 类消息：(a) **Controller-to-switch**, (b) **Asynchronous (switch-to-controller)**, (c) **Symmetric (misc.)**。OpenFlow API（定义动作）跟 OpenFlow protocol（定义消息）是两件事。",
  "key_points": [
    "TCP 上跑（可选 TLS）",
    "3 类消息：C→S / S→C / symmetric",
    "API 和 protocol 是两件事"
  ]
},

"lec20:25": {
  "title": "OpenFlow — Controller → Switch Messages",
  "summary": "Key C→S messages: (a) **features** — controller 查询 switch 能力；(b) **configure** — query/set switch 参数；(c) **modify-state** — 增/删/改 flow table entries；(d) **packet-out** — controller 让 switch 从某 port 发出特定包。",
  "key_points": [
    "**features**: 查 switch 能力",
    "**configure**: 设置参数",
    "**modify-state**: 增/删/改 flow entries（核心）",
    "**packet-out**: controller 主动发包"
  ]
},

"lec20:26": {
  "title": "OpenFlow — Switch → Controller Messages",
  "summary": "Key S→C messages: (a) **packet-in** — 把包（及其上下文）转给 controller，对应 controller 的 packet-out；(b) **flow-removed** — flow table entry 被删（超时/被替换）；(c) **port status** — 端口状态变（up/down）。",
  "key_points": [
    "**packet-in**: switch 不会处理 → 交 controller",
    "**flow-removed**: entry 被删（超时等）",
    "**port status**: link up/down"
  ],
  "explanation": "**实际开发**：用 higher-level abstraction（如 Floodlight, Ryu, ONOS 等 controller frameworks），不直接构造 OpenFlow message。"
},

"lec20:27": {
  "title": "SDN 控制 / 数据面 交互例 (1)",
  "summary": "完整工作流示意：(1) S1 检测到 link 失败，用 OpenFlow port status message 通知 controller；(2) Controller 收到 OpenFlow 消息，更新 link 状态信息；(3) Dijkstra routing 算法（之前注册了『link status change 时调用我』）被触发；(4) Dijkstra 算新路径，访问 controller 内的 network graph + link state info。",
  "key_points": [
    "① Switch port status 通知 controller",
    "② Controller 更新 link state",
    "③ 触发 Dijkstra app（之前注册回调）",
    "④ Dijkstra 算新路径"
  ]
},

"lec20:28": {
  "title": "SDN 交互例 (2) — 路径计算 + 下发",
  "summary": "续：(5) Dijkstra app 跟 controller 的 flow-table-computation 模块交互，算新 flow tables；(6) Controller 用 OpenFlow 安装新 flow tables 到需要更新的 switches。",
  "key_points": [
    "⑤ Routing app 跟 flow-table-computation 协作",
    "⑥ Controller 用 OpenFlow 下发新 FT"
  ],
  "explanation": "**完整闭环**：拓扑变化 → switch 通知 controller → controller 触发 app → app 计算 → controller 下发 → switch 执行。整个过程毫秒级。\n\n**对比传统**：分布式协议（OSPF）需要 LSA 广播 + 每 router 自跑 Dijkstra，几秒级。"
},

"lec20:29": {
  "title": "Google ORION SDN Control Plane",
  "summary": "Real-world 案例：Google ORION（NSDI'21）—— Google datacenter (Jupiter) 和 WAN (B4) 的 SDN control plane。提供 routing (intradomain, iBGP)、traffic engineering、edge-edge flow controls（CoFlow scheduling），保证 SLA。管理用 pub-sub 微服务，OpenFlow 做 switch 信号 / 监控。",
  "key_points": [
    "Google 内部 SDN controller",
    "管理 Jupiter (datacenter) + B4 (WAN)",
    "Routing + Traffic Engineering + CoFlow",
    "Microservices 架构",
    "Note: intradomain 内"
  ],
  "explanation": "**B4 是经典 SDN 案例**：Google 把所有 datacenter 间的流量用 SDN 控制。Traffic engineering 让链路利用率从典型的 30-40% 提到 90%+（接近极限）。\n\nORION 是其新一代 control plane（2021 NSDI 论文）。"
},

"lec20:30": {
  "title": "OpenDaylight (ODL) Controller",
  "summary": "OpenDaylight：开源 Java SDN controller，Linux Foundation 主持。架构：traffic engineering / firewalling / load balancing 等 apps → Northbound API → enhanced services + basic network functions → Service Abstraction Layer (SAL) → Southbound API (OpenFlow, NETCONF, SNMP, OVSDB) → 设备。",
  "key_points": [
    "开源 SDN controller，Linux Foundation",
    "Java",
    "SAL 抽象设备差异",
    "支持多 southbound 协议"
  ]
},

"lec20:31": {
  "title": "ONOS Controller",
  "summary": "ONOS = Open Network Operating System。另一个开源 SDN controller，重视分布式可靠性。架构：apps → northbound API → ONOS distributed core → southbound API → 设备。提供 'intent framework'：高层声明『我要什么』而非『怎么做』。",
  "key_points": [
    "ONOS 开源 controller，Java",
    "Distributed core: 多副本一致性",
    "Intent framework: declarative",
    "强调可靠性 + 性能 + 扩展"
  ]
},

"lec20:32": {
  "title": "SDN — 当前挑战",
  "summary": "(a) Hardening control plane: 可靠、性能、可扩展、安全的分布式系统；(b) 满足任务特定需求（实时、超可靠、超安全）的网络/协议；(c) Internet-scaling: 跨多 AS；(d) SDN 在 5G cellular 网络的关键作用。",
  "key_points": [
    "Control plane 硬化（容错、扩展、安全）",
    "任务特定网络（real-time, ultra-reliable, ultra-secure）",
    "跨 AS 扩展（目前 SDN 主要单 AS 内）",
    "5G cellular 应用"
  ]
},

"lec20:33": {
  "title": "CSEE4119 — Data Link Layer 章节封面",
  "summary": "进入新章节：Data Link Layer。Xia Zhou 教，2026 年 4 月 2 日。",
  "key_points": ["新章节，4/2 开课"]
},

"lec20:34": {
  "title": "Data Link Layer — 在协议栈位置",
  "summary": "5 层栈：L7 App (HTTP, FTP, DASH, DNS) → L4 Transport (TCP, UDP) → L3 Network (IP) → L2 Data Link (Ethernet, 802.11, PPP) → L1 Physical (optical, copper, radio, PSTN)。本章讲 L2。",
  "key_points": [
    "L2 = 数据链路层",
    "例: Ethernet, 802.11 (WiFi), PPP",
    "L1 例: optical, copper, radio, PSTN"
  ]
},

"lec20:35": {
  "title": "From a Network to a Single Link",
  "summary": "Network = 多跳。每跳可能用不同 link 技术（Ethernet、802.11 wireless LAN、...）。Link layer 协议 = 每跳一个。**隐藏 link 技术细节给上层**（统一接口）。",
  "key_points": [
    "网络 = 多跳, 每跳可能不同 link 技术",
    "Link layer 协议 per-hop",
    "隐藏细节给 upper layer"
  ],
  "explanation": "**好处**：IP 不需要知道下面是 Ethernet 还是 WiFi，统一接口。\n\n**坏处**：不同 link 技术性能、可靠性差异大（有线 vs 无线），上层无法针对性优化。"
},

"lec20:36": {
  "title": "Data Link Layer — 实现在 NIC (Network Interface Card)",
  "summary": "Link layer 跑在 **network adapter (NIC)** 里。Ethernet card、802.11 card、PC card。**Sender** 把 datagram 包成 frame、加错检 bit、流控。**Receiver** 检错、流控、解包成 datagram 交给上层。",
  "key_points": [
    "Link layer 在 NIC 里实现",
    "Sender 端: 包 datagram 成 frame, 加错检, 流控",
    "Receiver 端: 检错, 流控, 解 frame 成 datagram"
  ]
},

"lec20:37": {
  "title": "Data Link Layer Services",
  "summary": "4 大服务：(1) **Framing** — 加 header/trailer 包 packet 成 frame；(2) **Error detection/correction** — 处理信号衰减、噪声；(3) **Medium access control (MAC)** — 谁能在什么时候上信道；(4) **Reliable delivery** — 本地重传应对 frame loss（低 BER 链路常省）。",
  "key_points": [
    "① **Framing**: 包 packet 成 frame",
    "② **Error detect/correct**: 处理 bit error",
    "③ **MAC**: 谁能在什么时候发",
    "④ **Reliable delivery**: 本地重传（有线常省）"
  ],
  "explanation": "**Reliable delivery 在有线 vs 无线**：\n- 有线 BER ≈ 10⁻¹²（极低），TCP 端到端管够\n- 无线 BER ≈ 10⁻³（高），如果只 TCP 端到端重传性能极差\n\n所以 802.11 在 MAC 层做 ACK + 重传（link-level reliability）。"
},

"lec20:38": {
  "title": "Error Detection — 概念",
  "summary": "错误不可避免（电干扰、热噪声...）。解药：**传冗余信息**用于检错。Trade-off：开销 vs 检测能力。**三种检测技术**：Parity check, Checksum, Cyclic Redundancy Check (CRC)。",
  "key_points": [
    "Error 来源: 电干扰, 热噪声, 信号衰减",
    "Solution: 传冗余 bits",
    "Trade-off: overhead vs accuracy",
    "**3 种技术**: parity, checksum, CRC"
  ]
},

"lec20:39": {
  "title": "Error Detection — Parity Check (1-bit)",
  "summary": "加 1 个 bit 到 7-bit 数据末尾。**Odd parity**: 让总 1 数为奇。**Even parity**: 让总 1 数为偶。例: 0101011 → 01010111 (奇 parity 加 1)。**Fail to deal with multiple bit errors**: 偶数个 bit 翻转，奇偶性不变。",
  "key_points": [
    "Add 1 bit to 7-bit code",
    "Odd parity: 总 1 数为奇",
    "Even parity: 总 1 数为偶",
    "**只能可靠检测奇数个 bit 错误**",
    "偶数错误奇偶性不变 → 漏检"
  ],
  "explanation": "**例**（even parity）：\n- 数据 0101011（3 个 1）\n- 加 parity 1 让总 1 数变 4（偶）→ 01010111\n\n传输后某 bit 翻：\n- 1 个 bit 翻 → 总 1 数变奇 → 检测出错\n- 2 个 bit 翻 → 总 1 数仍偶 → 漏检 ❌\n\n**结论**：parity 弱，只检单 bit。下一页 2D parity 改进。"
},

"lec20:40": {
  "title": "Error Detection — 2D Parity",
  "summary": "数据排成 i×j 矩阵。每行 + 每列各加 1 parity bit。**Detect AND correct single bit errors**。例: 5×4 矩阵 + 1 行 parity + 1 列 parity。如果 row 2 列 4 翻转，row 2 parity 出错 + col 4 parity 出错 → 定位 (2,4) → 翻转校正。",
  "key_points": [
    "数据 i×j 矩阵",
    "+ 行 parity + 列 parity",
    "Single bit error: row + col parity 同时出错 → 定位 → 翻转校正",
    "Detect + correct"
  ],
  "explanation": "**例**（even parity, 4×5）：\n```\n数据:        parity:\n1 0 1 0 1   1\n1 1 1 1 0   0\n0 1 1 1 0   1\n1 0 1 0 1   1\n----------  -\ncol parity:\n1 0 0 0 0   0\n```\n\n如果 (2, 4) 翻转：\n```\n1 0 1 0 1   1   ← row OK\n1 1 1 0 0   0   ← row WRONG\n0 1 1 1 0   1   ← row OK\n1 0 1 0 1   1   ← row OK\n----------\n1 0 0 1 0   0   ← col 4 WRONG\n```\n\nRow 2 错 + col 4 错 → (2, 4) → 翻回。"
},

"lec20:41": {
  "title": "Error Detection — Checksum",
  "summary": "把数据当 16-bit word 累加（无 carry），传 sum。TCP/UDP/IP 都用 checksum。同 TCP/UDP checksum。",
  "key_points": [
    "数据当 16-bit word 序列",
    "全部相加（无 carry, 即 one's complement sum）",
    "Wraparound: overflow 加到末尾",
    "TCP/UDP/IP 都用 checksum"
  ],
  "explanation": "**例**: 加两个 16-bit:\n```\n  1110011001100110\n+ 1101010101010101\n-------------------\n  10111101110111011  ← overflow\n→ wraparound:\n  1011110111011011\n+ 1\n-------------------\n  1011110111011100\n→ 取反 (one's complement):\n  0100001000100011  ← 这是 checksum\n```\n\n**比 CRC 弱**：可能漏检某些错误模式。但简单，TCP/UDP 用够。"
},

"lec20:42": {
  "title": "Error Detection — CRC 概念",
  "summary": "**Cyclic Redundancy Check**: key idea — 把信息当数除以一个 number，余数为 check value。例: 1000/6 = 166 余 4；如果错变成 996/6 余 0，detected。\n\n**真 CRC**: Generator G (r+1)-bit pattern, sender 和 receiver 都知道；选 r 额外 bits 接 data D，让结果能被 G 整除（modulo-2 = XOR）；这 r bits 就是 CRC。",
  "key_points": [
    "Idea: divide D by G, remainder = check",
    "G = (r+1)-bit generator polynomial",
    "Choose r extra bits R s.t. (D·2^r) mod G = 0 - R',即 R = (D·2^r) mod G",
    "Send (D, R)",
    "Modulo-2 arithmetic = XOR (no borrow)"
  ],
  "explanation": "**公式**: R = (D · 2^r) mod G\n\n直觉：把 D 左移 r 位（在末尾加 r 个 0），用 G 做 mod-2 除法，余数 R 就是 CRC。最后传 D 拼 R（共 d+r bits）。\n\n**Receiver 验证**：把收到的 (D, R) 当一整个数，再用 G 做 mod-2 除法。如果余 0 → 数据正确；否则 → 检测到错。\n\n**为什么强**：CRC 能检测所有 ≤ r 位的 burst error。常用 CRC-32（r=32）几乎万无一失。"
},

"lec20:43": {
  "title": "Error Detection — CRC 手算例",
  "summary": "G=1001 (4-bit, r=3), D=101011. Compute R.\n\n**Step**: D·2^r = 101011 000 (左移 3 位).\n\n**Mod-2 long division by 1001**:\n```\n  1001 | 101011000\n         1001\n         ----\n          0010 10\n          0000  (next bit 0, skip)\n           0101\n           0000\n            1010\n            1001\n            ----\n            0011 0\n            0000\n            ----\n             0110\n             0000\n             ----\n              110  ← remainder R\n```\n\n**R = 110**. Transmit `101011 110`.",
  "key_points": [
    "G=1001, D=101011, r=3",
    "D·2^r = 101011000",
    "Mod-2 division (XOR)",
    "Remainder R = 110",
    "Send: 101011 110 (9 bits total)"
  ],
  "explanation": "**手算技巧**：\n1. 从最高位开始，看当前位是 1 → XOR G（对齐到当前位）\n2. 当前位是 0 → 跳过\n3. 一位一位向右推\n4. 最后剩 r bits 是 R\n\n**Receiver 验证**：把『101011 110』当作 9-bit 数除以 1001，余数应为 0。\n\n**期末/期中题型**：给你 G 和 D，手算 R。一定要会做。"
},

"lec20:44": {
  "title": "Quiz — DV 收敛轮数 (3 节点)",
  "summary": "课后小测：3 节点拓扑，所有节点跑 distance vector 算最短路径。**Q: 几轮收敛？**\n\n**图**: A-D=9, A-B=4, B-C=3, C-D=1。\n\n**答**: 假设同步轮、无 CTI、静态拓扑、无触发更新。\n\n**最短路径**: A→D=9 直连 vs A→B→C→D = 4+3+1=8。所以 A→D 实际 8 (经 B-C-D)，最大跳数 3。\n\n**收敛轮数 = max-hops − 1 = 3 − 1 = 2 轮**？实际看图：4 节点（不是 3），最长跳数 3 (A→B→C→D 或反过来)。理论 2 轮收敛。",
  "key_points": [
    "DV 收敛轮数 ≈ max hops in shortest-path tree − 1",
    "前提: 同步轮 + 无 CTI + 静态 + 无触发更新",
    "本图最长跳数 3 → 2 轮收敛"
  ],
  "explanation": "**手推 DV 表 (4 节点 A B C D, 边 A-B=4, B-C=3, C-D=1, A-D=9)**：\n\n**Round 0 (init)**:\n- A: B=4 via B, C=∞, D=9 via D\n- B: A=4 via A, C=3 via C, D=∞\n- C: A=∞, B=3 via B, D=1 via D\n- D: A=9 via A, B=∞, C=1 via C\n\n**Round 1** (邻居换 DV)：\n- A 收到 B 的 DV(A=4, C=3, D=∞)，C 不在邻居，跳过；D 的 DV(A=9, B=∞, C=1)：\n  - A 经 B 到 C = 4+3=7 → 新 A→C=7 via B\n  - A 经 D 到 C = 9+1=10 → 不如经 B\n  - A 经 B 到 D = 4+∞=∞ → 跳过\n  - A 经 D 到 B = 9+∞=∞ → 跳过（D 不直邻 B）\n  - 注意 D 给 A 的 'B=∞' 意味 D 不直邻 B\n- B 收到 A, C 的 DV：\n  - B 经 A 到 D = 4+9=13\n  - B 经 C 到 D = 3+1=4 → 新 B→D=4 via C\n- C 收到 B, D 的 DV：\n  - C 经 B 到 A = 3+4=7 → 新 C→A=7 via B\n  - C 经 D 到 A = 1+9=10\n- D 收到 A, C 的 DV：\n  - D 经 A 到 B = 9+4=13\n  - D 经 C 到 B = 1+3=4 → 新 D→B=4 via C\n\n**Round 2** (再换)：\n- A 收到 B(C=3, D=4), D(C=1)：\n  - A 经 B 到 D = 4+4=8 → 新 A→D=8 via B (比原 9 短！)\n  - A 经 D 到 C 仍 10，不变\n- 类似 D→A 经 C-B 变 8\n\n**Round 3** (再换)：\n- DV 不再变 → 收敛\n\n所以约 2-3 轮收敛。**最短路径树最大跳数 = 3 (A→B→C→D)**，**收敛轮 = 3-1 = 2 轮**（理论值，实际可能稍多）。"
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
    print(f"lec20 rewrite: overwrote {overwritten}, added {new}")

if __name__ == "__main__":
    main()
