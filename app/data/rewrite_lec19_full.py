#!/usr/bin/env python3
"""Full per-page rewrite for lec19 (BGP + OSPF, 25 pages)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec19:1": {
  "title": "Control Plane Roadmap",
  "summary": "目录回顾：本课接着 lec18 讲 routing 协议，重点 intra-AS (OSPF) 和 inter-AS (BGP)，最后 SDN、ICMP、网络管理。",
  "key_points": [
    "Intra-ISP routing: OSPF（lec19 前半）",
    "Inter-ISP routing: BGP（lec19 后半）",
    "SDN control plane（lec20）",
    "ICMP + network management（后面）"
  ]
},

"lec19:2": {
  "title": "Making Routing Scalable — 现实问题",
  "summary": "理想化路由（所有 router 相同 + 网络『平坦』）在 Internet 不可行。两大挑战：(a) **Scale** — 数十亿目的地，存不下路由表，交换会塞满链路；(b) **Administrative autonomy** — Internet 是 'network of networks'，每个网络 admin 想自己控制路由。",
  "key_points": [
    "Scale: 数十亿目的地存不下路由表",
    "路由表交换 swamp 链路",
    "Admin autonomy: 每 AS 想自己说了算"
  ],
  "explanation": "**为什么不可扩展**：\n1. **表太大**：Internet 现在 ~100 万 BGP 前缀。每 router 都存全表要大量内存。\n2. **更新太多**：链路变化频繁，全网广播会饱和链路。\n3. **政治**：Comcast 不让 AT&T 决定 Comcast 内部怎么走。\n\n→ 必须分区域，每区自治。**这就是 AS 的来由**。"
},

"lec19:3": {
  "title": "AS — Autonomous Systems",
  "summary": "解药：把 routers 聚合到『autonomous systems (AS)』。同 AS 内 routers 必须跑同一个 intra-AS 协议；不同 AS 可以跑不同的；AS 之间统一跑 BGP。Gateway router = AS 边界，跑双协议。",
  "key_points": [
    "AS = 一个管理实体（ISP, 大学, 公司）",
    "Intra-AS: AS 内部 routing（各 AS 自选协议）",
    "Inter-AS: AS 间 routing（统一 BGP）",
    "**Gateway router**: AS 边界，跑双协议"
  ],
  "explanation": "**真实例子**（AS Number, ASN）：\n- AS 7922 = Comcast\n- AS 14618 = Amazon AWS\n- AS 15169 = Google\n- AS 8075 = Microsoft\n- AS 36 = Columbia University\n\n互联网约 **10 万** 活跃 AS。\n\n**Intra-AS 各 AS 自选**：\n- Columbia 可能 OSPF\n- Google 用 SDN\n- 小公司可能 RIP\n\n**Inter-AS 必统一**：所有 AS 之间必须能 advertise 可达性 → 都跑 BGP（『胶水协议』）。\n\n**考点**：『为什么 router 分 AS？』必答 3 点：scale + autonomy + policy。"
},

"lec19:4": {
  "title": "Interconnected ASes — Forwarding Table 来源",
  "summary": "Router 的 forwarding table 由 intra-AS 和 inter-AS 算法**共同**决定。Intra-AS 算法填本 AS 内目的的条目；inter-AS + intra-AS 共同填外部目的的条目。",
  "key_points": [
    "FT 由 intra-AS + inter-AS 共同决定",
    "Intra-AS algo → 本 AS 内目的的条目",
    "Inter-AS + intra-AS → 外部目的的条目"
  ],
  "explanation": "**例**：AS1 里的 router 1d 收到目的 = AS3 某子网的包：\n1. Inter-AS（BGP）告诉它『去 AS3 经 gateway 1c』\n2. Intra-AS（OSPF）告诉它『去 1c 经接口 X』\n3. FT 里就有『dst AS3 → 接口 X』\n\n**两者协作必不可少**。"
},

"lec19:5": {
  "title": "Inter-AS 的作用 — 影响 intra-domain forwarding",
  "summary": "假设 AS1 一个 router 收到目的在 AS1 外的包，要转给某个 gateway router，但 *哪个* gateway？AS1 的 inter-domain routing 必须：(1) 学到哪些目的经 AS2 / AS3 可达；(2) 把这个可达性传播给 AS1 内所有 router。",
  "key_points": [
    "Router 收到外部目的包 → 转给某 gateway，但哪个？",
    "AS1 inter-domain routing 任务：",
    "  ① 学到哪些目的经 AS2/AS3 可达",
    "  ② 把信息传给 AS1 内所有 router"
  ],
  "explanation": "**例子场景**（图）：\n- AS1 内 router 1d 想发包到 AS3 某子网\n- AS1 有 gateway 1b（连 AS2）和 1c（连 AS3）\n- 1d 该转给 1b 还是 1c？\n\n**答**：取决于 inter-domain routing 学到的『AS3 可达性』。BGP 学到『AS3 经 1c 直达』。然后通过 iBGP 告诉 1d。1d 用 intra-AS (OSPF) 决定 *怎么到 1c*。\n\n**这是 BGP 和 OSPF 协作的核心场景**。"
},

"lec19:6": {
  "title": "Intra-AS Routing 协议家族",
  "summary": "**RIP (已淘汰)**: 经典 DV，30 秒发一次。**EIGRP**: Cisco 原私有，DV 基础。**OSPF**: link-state，最常用。**IS-IS**: ISO 标准（不是 RFC），跟 OSPF 几乎一样，Tier-1 ISP 核心常用。",
  "key_points": [
    "**RIP** (RFC 1723): classic DV，30s 一次，hop 16=∞，已淘汰",
    "**EIGRP**: DV，原 Cisco 私有，2013 开放 (RFC 7868)",
    "**OSPF** (RFC 2328): link-state，最广泛",
    "**IS-IS**: ISO 标准，跟 OSPF 类似，Tier-1 ISP 核心"
  ],
  "explanation": "**为什么 RIP 淘汰**：\n- Hop limit 16 太低（大网会被截断）\n- 30s 周期更新太慢（变化响应不及时）\n- Count-to-infinity 问题\n\n**OSPF vs IS-IS**：技术上几乎等价。OSPF IETF 标准更普及，IS-IS 在大型 ISP 核心更常见（历史原因）。\n\n**Q: 你的家庭路由器跑什么 intra-AS？** A: 通常什么都不跑（家用 LAN 平坦，没多 router）。"
},

"lec19:7": {
  "title": "OSPF — Open Shortest Path First",
  "summary": "Open（公开标准）+ link-state（每 router flood LSA）+ 跑 Dijkstra。LSA **直接走 IP**（不用 TCP/UDP，自己保证 reliable）。支持多种 metric（带宽、延迟）。所有消息认证（防恶意）。",
  "key_points": [
    "Open = 公开（vs Cisco 私有协议）",
    "Link-state 算法",
    "Flood LSA **直接 over IP**（protocol number 89），不用 TCP/UDP",
    "支持多种 link cost metric（BW, delay）",
    "所有消息认证（HMAC）防伪造"
  ],
  "explanation": "**为什么直接 over IP 而非 TCP/UDP**：\n- 路由协议本身要决定『怎么走』，依赖 TCP 会有 'chicken and egg' 问题（没有路由怎么 TCP 通信）\n- OSPF 自己做可靠交付（ACK、超时重传）\n- 直接 IP 减少封装开销\n\n**Authentication 重要**：\n- 防止恶意 router 注入虚假 LSA 把流量引到自己（DoS / 窃听）\n- 早期 plaintext password，现代 HMAC-MD5/SHA"
},

"lec19:8": {
  "title": "Hierarchical OSPF",
  "summary": "大 AS 用两级层级：(a) **local area** — LSA 只在 area 内 flood，每 node 详细知 area 拓扑；(b) **backbone (area 0)** — 连各 area。**ABR (Area Border Router)** 在 area 边界，汇总 area 内距离向 backbone advertise。**Boundary router** 连其他 AS（跑 BGP）。",
  "key_points": [
    "**Area**: AS 内子区域",
    "**Backbone (area 0)**: 连各 area",
    "**ABR**: area 边界，汇总 advertise",
    "**Backbone router**: 跑 OSPF 限于 backbone",
    "**Boundary router**: 连其他 AS（跑 BGP）",
    "**Internal router**: 只在某 area 内 flood"
  ],
  "explanation": "**为什么分层**：大 AS 时 LSA flood 全网开销太大。分 area 后：\n- LSA 只在自己 area 内 flood\n- ABR 把 area 内可达性汇总成几条 advertise 到 backbone\n- 其他 area 经 backbone 学到\n\n→ Local LSA 流量 ↓↓，全网消息复杂度 ↓\n\n**类比**：公司组织。每个部门内频繁沟通，部门间靠经理汇总传达。"
},

"lec19:9": {
  "title": "Control Plane Roadmap（重复）",
  "summary": "目录过渡：进入 inter-AS routing (BGP) 部分。",
  "key_points": ["章节过渡"]
},

"lec19:10": {
  "title": "Interconnected ASes（复习）",
  "summary": "复习 intra-AS vs inter-AS 概念，准备 BGP 详讲。",
  "key_points": ["复习概念"]
},

"lec19:11": {
  "title": "Internet inter-AS routing: BGP",
  "summary": "BGP (Border Gateway Protocol) = de facto inter-domain routing 协议，'glue that holds the Internet together'。让 subnet 向全 Internet advertise 自己的存在和可达性。BGP 提供：(a) 学到邻居 AS 可达性 (eBGP)；(b) 根据可达性 + policy 决定路由；(c) 通过 iBGP 传播到 AS 内所有 router；(d) 向邻居 AS advertise 可达性。",
  "key_points": [
    "**BGP = Internet 'glue'**, 互联网间路由标准",
    "Subnet advertise: '我在这，我能到 X，怎么到'",
    "AS 用 BGP 做 4 件事:",
    "  ① 学邻居 AS 可达性 (eBGP)",
    "  ② 根据 reachability + policy 决定路由",
    "  ③ iBGP 传给 AS 内所有 router",
    "  ④ advertise 给邻居 AS"
  ],
  "explanation": "**BGP ≠ DV ≠ LS**：它是 **path vector**：\n- 不像 DV 只传距离，BGP 传完整 AS-PATH（防环 + policy 决策）\n- 不像 LS 共享全网拓扑，只共享 AS 间路径（不暴露内部）\n- 跑在 **TCP** 上（不像 OSPF 自己处理 reliable）\n\n**为什么 path vector 而不是 distance vector**：\n- DV 只有距离信息 → 不能做 policy\n- Path vector 给完整路径 → AS 能根据『谁在路径里』做策略决定（接不接受、advertise 不 advertise）\n\n**Advertise 的承诺**：AS3 告诉 AS2『去 X 经 AS3 可达』→ AS3 **承诺** 收到目的 = X 的包会 forward。不只是信息共享，是合同。"
},

"lec19:12": {
  "title": "eBGP / iBGP — 连接图",
  "summary": "**eBGP**: 跨 AS gateway routers 之间。**iBGP**: 同 AS 内 routers 之间。Gateway router 同时跑两种。例图：AS1 内 1a, 1b, 1c, 1d 跑 iBGP 互通；1c 跨 AS2 用 eBGP；类似 AS3。",
  "key_points": [
    "**eBGP**: 跨 AS（gateway 间）",
    "**iBGP**: 同 AS 内（传播 eBGP 学到的路径）",
    "Gateway router 同时跑两种协议",
    "iBGP 让 AS 内所有 router 知道外部可达性"
  ],
  "explanation": "**为什么要 iBGP**：\n- 假设 AS1 的 gateway 1c 通过 eBGP 学到『去 X 经 AS3』\n- AS1 内部其他 router（1a, 1b, 1d）不知道这条\n- 它们必须知道才能正确转发外部目的的包\n- → 1c 通过 iBGP 告诉所有 AS1 router：『去 X 经我（1c）出去』\n\n**iBGP vs Intra-AS routing**：\n- IBGP 只传**目的可达性**（『X 经 1c 可达』），不算最短路径\n- 最短路径由 intra-AS（OSPF）算（『到 1c 走 interface 2』）\n- 两者协作得 FT"
},

"lec19:13": {
  "title": "BGP Basics — Session",
  "summary": "BGP peers (两个 BGP routers) 通过 semi-permanent TCP 连接交换 BGP 消息。Advertise 路径到不同 dst network prefix。BGP 是 path-vector 协议。",
  "key_points": [
    "Session = 半永久 TCP 连接（port 179）",
    "Advertise: prefix + AS-PATH",
    "Path-vector 协议",
    "TCP 提供 reliable delivery + 顺序 + 流控"
  ],
  "explanation": "**为什么用 TCP**（vs OSPF 直接 over IP）：\n- BGP 消息很多（inter-AS 全表 ~100 万前缀），需要可靠 + 流控\n- TCP 提供天然支持\n- 半永久连接：保持直到链路断或重配；周期 KEEPALIVE 防 idle 超时\n\n**Session 一开就稳定**：典型 BGP session 持续数月。"
},

"lec19:14": {
  "title": "BGP Protocol Messages",
  "summary": "4 种消息：**OPEN** 建 TCP + 认证；**UPDATE** 主力 — 宣告新路径或撤回旧的；**KEEPALIVE** 维持连接；**NOTIFICATION** 错误报告 + 关闭。",
  "key_points": [
    "**OPEN**: 建 TCP, 认证 peer",
    "**UPDATE**: 宣告新路径 OR 撤回旧路径（主力消息）",
    "**KEEPALIVE**: 维持连接，ACK OPEN",
    "**NOTIFICATION**: 错误报告 + 关闭"
  ],
  "explanation": "**UPDATE 的两种语义**：\n- **Announce**: 新路径可用 → 告诉 peer『去 X 经我的 AS-PATH=[...]』\n- **Withdraw**: 路径不再可用 → 告诉 peer『撤回之前那条』\n\n**KEEPALIVE 频率**：典型 30-60 秒一次。如果 3-4 次没收到 → 认为 peer 死了 → withdraw 所有从 peer 学到的路径。"
},

"lec19:15": {
  "title": "Path Attributes — AS-PATH + NEXT-HOP",
  "summary": "BGP advertised route = **prefix + attributes**。Prefix = 被 advertise 的目的子网。两个重要 attributes：**AS-PATH** (沿途经过的 AS 列表) + **NEXT-HOP** (到下一 AS 的具体内部 router IP)。**Policy-based routing**: gateway 用 import policy 决定接不接路径；AS policy 决定是否 advertise 给邻居。",
  "key_points": [
    "**Prefix**: 被 advertise 的目的子网（如 200.23.16.0/20）",
    "**AS-PATH**: 沿途经过的 AS 列表（防环 + 路径长度比较）",
    "**NEXT-HOP**: 到下一 AS 的具体 router IP",
    "**Policy**: import (accept/reject) + export (advertise/not)"
  ],
  "explanation": "**AS-PATH 的两个作用**：\n1. **防环**：如果自己 AS 在 AS-PATH 里，reject（说明这条路径已经回到了自己）\n2. **路径长度比较**：用 AS 个数做 tie-break（短的优先）\n\n**NEXT-HOP 的细节**：\n- 不是『下一个 AS 的边界 router』那么简单\n- 是『去那个目的，AS 内应该走的下一跳 IP』\n- iBGP 把 NEXT-HOP 传到 AS 内所有 router 后，每 router 用 OSPF 算到 NEXT-HOP 怎么走\n\n**Policy 配置示例**：\n```\nimport policy: \n  accept from neighbor X if AS-PATH doesn't contain Y\n  reject from Z all\nexport policy:\n  advertise to customer all\n  advertise to peer only own prefixes\n  advertise to provider only own prefixes\n```\n\n**考点**：『BGP advertisement 包含什么？』必背 prefix + AS-PATH + NEXT-HOP。"
},

"lec19:16": {
  "title": "BGP Path Advertisement — 单条路径",
  "summary": "AS3 → AS2 → AS1 路径宣告链。AS3 边界 3a 通过 eBGP advertise『去 X 经 AS3』给 AS2 边界 2c。AS2 用 policy 接受，2c 通过 iBGP 传给所有 AS2 router。AS2 边界 2a 通过 eBGP advertise『去 X 经 AS2-AS3』给 AS1 边界 1c。",
  "key_points": [
    "AS3.3a → eBGP → AS2.2c: 'X via AS3'",
    "AS2.2c → iBGP → all AS2 routers",
    "AS2.2a → eBGP → AS1.1c: 'X via AS2-AS3'"
  ],
  "explanation": "**关键观察**：AS-PATH 在每个 AS 边界都被 prepend：\n- 在 AS3 内：『AS3, X』\n- 出 AS3 进 AS2：『AS3, X』（AS3 advertise 时已有 AS3）\n- 在 AS2 内：『AS3, X』（不变）\n- 出 AS2 进 AS1：『AS2, AS3, X』（AS2 advertise 时 prepend AS2）\n\n这样每个 AS 收到的 AS-PATH 是完整的、自含的，能做 policy 决策。"
},

"lec19:17": {
  "title": "BGP Path Advertisement — 多路径",
  "summary": "Gateway 可能学到多条到同一 dst 的路径。例：AS1 gateway 1c 从 2a 学到 AS2-AS3-X，又从 3a 直连学到 AS3-X。1c 根据 policy 选一条，传给 AS1 内部。",
  "key_points": [
    "Gateway 学到多条到 X 的路径",
    "例: AS1.1c 学到 AS2-AS3-X (经 AS2) 和 AS3-X (直连 AS3)",
    "按 policy 选最优一条",
    "通过 iBGP 传给 AS1 内所有 router"
  ],
  "explanation": "**为什么会有多条**：\n- 大型 AS 可能跟多个 AS peering\n- 同一个 dst 可能多条 inter-AS 路径\n\n**选择依据**（下页讲）：\n1. Local pref（policy）\n2. AS-PATH 短\n3. Hot potato\n4. 其他"
},

"lec19:18": {
  "title": "BGP — 填 Forwarding Table (1)",
  "summary": "AS1 内 1d 通过 iBGP 学到『X 经 1c』。1d 用 OSPF (intra-AS) 算到 1c 走 interface 1。结合得到 FT：dst=X → interface 1。",
  "key_points": [
    "1d 收 iBGP: 'X via 1c'",
    "1d 跑 OSPF: 'to 1c → interface 1'",
    "FT: dst=X → interface 1"
  ],
  "explanation": "**完整流程示范**：\n1. eBGP 让 1c 学到『X 经 1c 出去就行』\n2. iBGP 让 1d 知道『X 经 1c』\n3. OSPF 让 1d 知道『到 1c 走 interface 1』\n4. 综合：1d 的 FT 写『dst=X → interface 1』\n\nBGP + OSPF 配合得完整的 FT。"
},

"lec19:19": {
  "title": "BGP — 填 Forwarding Table (2)",
  "summary": "另一个 router 1a 的视角：通过 iBGP 也学到『X 经 1c』。1a 用 OSPF 算到 1c 走 interface 2（不同于 1d）。FT: dst=X → interface 2。",
  "key_points": [
    "1a 收 iBGP: 'X via 1c'（同 1d）",
    "1a 跑 OSPF: 'to 1c → interface 2'（拓扑相关）",
    "FT: dst=X → interface 2"
  ],
  "explanation": "**关键**：iBGP 给 1a 和 1d 的信息是一样的（都是『X 经 1c』），但 1a 和 1d 在 AS1 内的位置不同，到 1c 的内部最短路径不同（interface 1 vs interface 2）。所以 FT 不同。\n\n**这就是 iBGP + intra-AS 的协作**：iBGP 决定 'which gateway'，intra-AS 决定 'how to reach gateway'。"
},

"lec19:20": {
  "title": "Hot Potato Routing",
  "summary": "Gateway 学到多条到同一 dst 的路径（经不同本 AS gateway 出去），选 intra-AS 代价最小的那个 gateway 扔出去。即使经那个 gateway 后 AS-PATH 更长，也不管。",
  "key_points": [
    "Router 学到多条到同 dst 的路径",
    "都通过本 AS 不同 gateway 出去",
    "选 **intra-AS 代价最小** 的 gateway",
    "不管出 AS 后 path 长短"
  ],
  "explanation": "**字面意思**：『烫手山芋赶紧扔』。\n\n**例**：AS1 内 router 2d 学到去 X 可以经 2a 或 2c（不同 gateway）。\n- 经 2a：AS-PATH 长，但 intra-AS 到 2a 近\n- 经 2c：AS-PATH 短，但 intra-AS 到 2c 远\n\n2d 选 2a（intra-AS 近），即使 AS-PATH 长一些。\n\n**经济动机**：carry traffic on own network 耗资源（电费、带宽、设备）。能让别的 AS 早扛就让它扛。\n\n**反义词 Cold potato**: 有些 ISP 反过来 — 流量在自己网内多 carry 一段，让客户体验最优。代价是自己多扛流量。\n\n**考点**：『hot potato 是什么？为什么？』必答：选 intra-AS 最便宜出口 + 经济动机。"
},

"lec19:21": {
  "title": "BGP Policy via Advertisements (1)",
  "summary": "ISP 通常只 carry 自己 customer 的流量，不愿当 transit。机制：通过『不 advertise』实现。例：B 学到 A→w，但 B 不 advertise『B 经 A 到 w』给 C，所以 C 不知道这条路径，不会经 B 到 w。",
  "key_points": [
    "ISP 不愿 carry transit traffic（替别人扛流量）",
    "实现：**不 advertise** 路径给特定邻居",
    "B 学到 A→w，但不 advertise 给 C",
    "C 不知道 → 不会经 B 到 w → B 不当中转"
  ],
  "explanation": "**Final Q3 完全是这个**：\n- Columbia 跟 CERN 直连（为 LHC 合作）\n- Columbia 跟 NYU peering（互相）\n- Q: NYU 学生能否经 Columbia 走到 CERN？\n- A: 不能。Columbia 通过 BGP 配置 **export policy**，**不向 NYU advertise** 自己到 CERN 的路径。NYU 学不到 → 不会路由过来。\n\n**经济动机**：B 替 C 中转到 A 的 customer w，B 拿不到钱（C 不是 B 的 customer），白白扛流量 → 拒绝。\n\n**这就是 '不 advertise = 不当 transit' 的标准模式**。"
},

"lec19:22": {
  "title": "BGP Policy via Advertisements (2) — Customer 视角",
  "summary": "Customer X dual-homed（接 B 和 C 两个 provider）。X 不想替 B 和 C 之间当过境。策略：X 不向 B advertise 自己到 C 的路径。",
  "key_points": [
    "X 是 dual-homed customer（连两 ISP B 和 C）",
    "X 不想 B 到 C 经 X（避免过境流量）",
    "X 配置 export policy: 不向 B advertise C 的路径"
  ],
  "explanation": "**典型场景**：大公司 dual-homed 给两个 ISP 做冗余。如果不配 policy，BGP 默认 might let X 当 B-C 间的中转，X 流量爆炸。\n\n**X 的配置**：\n```\nto B: don't advertise C's prefixes\nto C: don't advertise B's prefixes\n```\n\n这样 B 看不到经 X 到 C 的路 → B 不会用 X 中转。\n\n**这就是 'customer 不当 transit' 的标准做法**。"
},

"lec19:23": {
  "title": "BGP Route Selection — 优先级 4 步",
  "summary": "Router 学到多条到同 dst 的路径时按优先级选：(1) **Local preference**（admin 配置的偏好，policy）；(2) **Shortest AS-PATH**；(3) **Closest NEXT-HOP**（hot potato）；(4) 其他 tie-breakers（如 router ID 最小）。",
  "key_points": [
    "**1. Local pref**: admin policy 决定",
    "**2. Shortest AS-PATH**: 经 AS 数最少",
    "**3. Closest NEXT-HOP**: hot potato",
    "**4. Tie-breakers**: e.g. router ID 最小"
  ],
  "explanation": "**优先级顺序决定一切**：当 BGP 学到多条路径，按这个顺序逐级 tie-break。\n\n**Local pref 永远最高**：因为它代表 policy（policy > performance）。\n\n**例**：两条路径\n- 路径 A：AS-PATH=[AS2, AS3]，local pref=100\n- 路径 B：AS-PATH=[AS3]，local pref=200\n\nStep 1（local pref）：200 > 100 → 选 B。Step 2（AS-PATH）也是 B 短。最终 B。\n\n**改一下**：\n- 路径 A：AS-PATH=[AS3]，local pref=100\n- 路径 B：AS-PATH=[AS2, AS3]，local pref=200\n\nStep 1：B 的 local pref 高 → 选 B（即使 AS-PATH 长！）。\n\n这就是 **policy 高于 performance** 的体现。\n\n**考点**：『BGP 多条路径怎么选？』必答 4 步顺序。"
},

"lec19:24": {
  "title": "Why Intra ≠ Inter AS Routing? — 三大原因",
  "summary": "三大原因：(1) **Policy** — inter 需要 policy 支持，intra 单一 admin 不需要；(2) **Scale** — 分层路由表大幅缩小 + 更新流量减少；(3) **Performance** — intra 可以为性能优化，inter 政策第一。",
  "key_points": [
    "**Policy**: inter 跨 AS 必须支持 policy; intra 单 admin",
    "**Scale**: hierarchy → 路由表大幅缩小",
    "**Performance**: intra 为 perf 优化; inter policy 第一"
  ],
  "explanation": "**三个原因的具体含义**：\n\n1. **Policy**: \n   - Inter: ISP 不愿替别人 carry 过境流量 → BGP 必须能配 policy\n   - Intra: 同 AS 内一家管，policy 不重要\n\n2. **Scale**:\n   - 不分层：整网 1 亿条 host 路由\n   - 分层：每 AS 自己几千-几万条，AS 间 ~100 万 BGP 前缀\n   - 路由表小 N 个数量级\n\n3. **Performance**:\n   - Intra-AS 节点都信任，可以为最短路径全力优化\n   - Inter-AS 不可能让 ISP A 替 ISP B 优化性能（B 自己决定）\n\n**考点（高频简答）**：『为什么不用一个统一的协议处理 intra 和 inter？』必答 3 点。"
},

"lec19:25": {
  "title": "Quiz: TCP Throughput (preview for lec20)",
  "summary": "Quiz：『TCP 用 AIMD 管 sliding window。Window 在 W/2 ↔ W 之间锯齿。忽略 slow start。What is average throughput as function of W and RTT?』",
  "key_points": [
    "AIMD 下 cwnd 在 W/2 ↔ W 锯齿振荡",
    "平均 cwnd = (W/2 + W) / 2 = 3W/4",
    "每 RTT 发 cwnd bytes",
    "**Average throughput = 3W / (4·RTT)**"
  ],
  "explanation": "**完整推导**：\n\n忽略 slow start，只看 congestion avoidance 阶段：\n\ncwnd 在丢包后从 W（峰值）切半到 W/2，然后每 RTT +1 MSS 线性增长，直到再次丢包到 W → 又切半...\n\n**几何上**：cwnd 是一条锯齿，从 W/2 上升到 W，循环。\n\n**平均高度** = (最小 + 最大) / 2 = (W/2 + W) / 2 = **3W/4**\n\n**每 RTT 发送字节数** ≈ cwnd（满 window 推完一次）\n\n**平均吞吐量** = 3W/4 bytes/RTT = **3W / (4·RTT)**\n\n**例**：W = 16 KB, RTT = 100 ms：\nthroughput = 3 × 16 KB / (4 × 100 ms) = 12 KB / 100 ms = **120 KB/s = 960 kbps**\n\n**考点**：『TCP throughput as function of W and RTT?』必答 3W/(4·RTT)。"
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
    print(f"lec19 rewrite: overwrote {overwritten}, added {new}")

if __name__ == "__main__":
    main()
