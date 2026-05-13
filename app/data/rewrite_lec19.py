#!/usr/bin/env python3
"""Deepen lec19 (OSPF + BGP)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec19:1": {
  "title": "Control Plane Roadmap",
  "summary": "本课目标：intra-AS (OSPF) + inter-AS (BGP) + SDN + ICMP + 网络管理。"
},

"lec19:2": {
  "title": "Making Routing Scalable — 现实问题",
  "summary": "理想路由（全网平铺）不可行，必须分区。",
  "key_points": [
    "十亿个目的地 → 路由表太大",
    "全网频繁交换路由会塞满链路",
    "管理自治：每个公司想自己说了算自己的网络"
  ],
  "explanation": "### 不可扩展的几个原因\n1. **表太大**：全 Internet 大约有 100 万 BGP 前缀。每个 router 都存全表需要大量内存。\n2. **更新太多**：链路状态变化频繁，全网广播会饱和链路。\n3. **政治**：Comcast 不会让 AT&T 决定怎么路由 Comcast 自己网络内的流量。\n\n→ 必须分区域，每区自己管。"
},

"lec19:3": {
  "title": "AS（Autonomous Systems）⭐",
  "summary": "把 router 分到 AS（自治系统）。AS 内部用 intra-AS 协议；AS 之间用 inter-AS（BGP）。",
  "key_points": [
    "AS = 一个管理实体（ISP, 大学, 公司）",
    "Intra-AS：AS 内路由（每个 AS 选自己的协议）",
    "Inter-AS：AS 之间（统一 BGP）",
    "Gateway router：AS 边界，跑两种协议"
  ],
  "explanation": "### 真实例子\n- AS 7922 = Comcast\n- AS 14618 = Amazon\n- AS 15169 = Google\n- AS 8075 = Microsoft\n- AS 36 = Columbia University\n\n互联网有 ~10 万个活跃 AS。\n\n### Intra-AS 各家自选\n- Columbia 可能用 OSPF\n- Google 内部用 SDN\n- 小公司用 RIP\n- 各 AS 内随便\n\n### Inter-AS 必须统一\n所有 AS 之间必须能互相 advertise 可达性 → 大家都跑 BGP。这是 Internet 互通的『黏合剂』。\n\n### 考法\n『为什么把 router 分到 AS？』答 3 点：scale + 管理自治 + policy。"
},

"lec19:4": {
  "title": "Interconnected ASes — 转发表的来源",
  "summary": "Forwarding table 由 intra-AS（本 AS 内目的）+ inter-AS（外部目的）共同决定。"
},

"lec19:5": {
  "title": "Inter-AS 在 intra forwarding 中的作用",
  "summary": "Inter-AS 学到的『外部可达性』要传到 AS 内所有 router 才能形成完整 FT。",
  "key_points": [
    "Gateway router 通过 eBGP 学到外部 AS 的路径",
    "通过 iBGP 在 AS 内部分发『去外部经哪个 gateway』",
    "Intra-AS（OSPF）告诉每个 router 怎么到 gateway",
    "组合 → 完整 FT"
  ]
},

"lec19:6": {
  "title": "Intra-AS Routing 协议家族",
  "summary": "RIP（DV，已废）/ EIGRP（DV，原 Cisco）/ OSPF（LS，最常用）/ IS-IS（LS，与 OSPF 类似）。",
  "key_points": [
    "**RIP**: classic DV，30s 一次 update（已淘汰）",
    "**EIGRP**: DV 基础，原 Cisco 私有 → 2013 开放",
    "**OSPF**: link-state，最常用",
    "**IS-IS**: ISO 标准，跟 OSPF 几乎一样，常用于 Tier-1 ISP 核心"
  ]
},

"lec19:7": {
  "title": "OSPF — Open Shortest Path First ⭐",
  "summary": "Open + link-state + Dijkstra。每 router flood LSA，全 AS 同步拓扑，跑 Dijkstra。",
  "key_points": [
    "**Open**：公开标准（vs Cisco IOS 的私有 protocols）",
    "**Link-state**：广播链路状态",
    "**Flood LSA 直接走 IP**（不用 TCP/UDP，自己 reliable）",
    "支持多 metric（BW、delay、cost）",
    "消息认证（防伪造）",
    "**层级**：area + backbone"
  ],
  "explanation": "### 工作流程\n1. 每个 router 监听自己的接口状态\n2. 状态变（link up/down/cost 变）→ 生成 LSA (Link State Advertisement)\n3. Flood LSA 给整个 area 内所有 router\n4. 每个 router 维护完整 LS DB\n5. 跑 Dijkstra 算最短路径，填 FT\n\n### LSA 直接走 IP 是什么意思\n大多数协议跑在 TCP（如 BGP）或 UDP 上，但 OSPF 直接用 IP 协议号 89，**自己处理 reliable delivery**。原因：路由协议本身要决定『怎么走』，依赖 TCP 会有鸡生蛋问题。\n\n### Authentication\n防止恶意 router 伪造 LSA 把流量引到自己。早期 plaintext password，现在 HMAC。"
},

"lec19:8": {
  "title": "Hierarchical OSPF — 分层 ⭐",
  "summary": "大 AS 分多个 area + 一个 backbone。LSA 只在 area 内 flood，节省广播。",
  "key_points": [
    "**Area**: AS 内的一块子区域",
    "**Backbone**: area 0，连接所有 area",
    "**ABR (Area Border Router)**: 连 area 跟 backbone；汇总 area 内距离 advertise 进 backbone",
    "**Backbone router**: 跑 OSPF 限于 backbone",
    "**Boundary router**: 连其他 AS（跑 BGP）",
    "**Internal router**: 只在某 area 内"
  ],
  "explanation": "### 为什么分层\nAS 大时，LSA flood 全网开销太大。分 area 后：\n- LSA 只在自己 area 内 flood\n- ABR 把 area 内可达性『汇总』成几条 advertise 到 backbone\n- 其他 area 通过 backbone 学到\n\n→ Local LSA 量 ↓↓，全网消息复杂度 ↓\n\n### 类比\n像公司组织：每个部门内部沟通频繁，部门之间靠经理总结后传达。"
},

"lec19:9": { "title": "Control Plane Roadmap（重复）", "summary": "进入 BGP。" },

"lec19:10": {
  "title": "Interconnected ASes（复习）",
  "summary": "Intra-AS vs Inter-AS。"
},

"lec19:11": {
  "title": "BGP — 互联网间路由 ⭐⭐",
  "summary": "BGP (Border Gateway Protocol) = inter-AS 路由协议，『把互联网粘起来的胶水』。",
  "key_points": [
    "Subnet 通过 BGP advertise 自己的存在和可达性",
    "**AS 学外部可达性**：通过 eBGP",
    "**AS 内传播**：通过 iBGP",
    "**承诺**：advertise = 我会 forward",
    "决策基于 reachability info + policy"
  ],
  "explanation": "### BGP ≠ DV / LS\nBGP 不是简单的 DV 或 LS：\n- 它传 **完整 AS 路径**（path vector，防环）\n- 它考虑 **policy**（不一定走最短路径）\n- 它跑在 **TCP** 上（不像 OSPF 自己处理 reliable）\n\n### Advertise 的语义\nAS3 advertise『我能到前缀 X，路径 AS3-X』给 AS2 → AS3 **承诺** 收到去 X 的包它会 forward。这是合同关系，不只是信息共享。"
},

"lec19:12": {
  "title": "eBGP / iBGP ⭐",
  "summary": "eBGP = AS 间 (跨 AS 的 gateway 之间)；iBGP = AS 内 (传 eBGP 学到的信息)。",
  "key_points": [
    "**eBGP**: 跨 AS gateway router 之间",
    "**iBGP**: 同 AS 内 router 之间（传播 eBGP 学到的外部路径）",
    "Gateway 同时跑两种"
  ],
  "explanation": "### 为什么需要 iBGP\nGateway 1c 从 eBGP 学到『去 X 经 AS3』。但 AS1 内部其他 router (1a, 1b, 1d) 不知道这条。它们必须知道才能正确转发外部目的的包。\n\n→ 1c 通过 iBGP 告诉所有 AS1 内 router：『去 X 经我（1c）出去』。\n\n### iBGP vs intra-AS routing\nIBGP 只传 **目的可达性**（『X 经 1c 可达』），不算最短路径。最短路径由 intra-AS（如 OSPF）算（『到 1c 走 interface 2』）。\n\n两个一起组成完整的 forwarding decision。"
},

"lec19:13": {
  "title": "BGP Session — TCP 长连接",
  "summary": "BGP peers 通过半永久 TCP 连接交换路径。",
  "key_points": [
    "TCP 长连接（一直保持）",
    "Path-vector：传 prefix + AS-PATH",
    "Advertise = 承诺 forward",
    "区别于 DV（只传距离）和 LS（传链路状态）"
  ],
  "explanation": "### 为什么用 TCP\n- 可靠交付（不会丢 update）\n- 顺序保证\n- 流控（避免压垮 peer）\n\n### 为什么是『半永久』\nSession 一开就保持直到链路断或重配置。periodic KEEPALIVE 防止 idle 超时。"
},

"lec19:14": {
  "title": "BGP 协议消息",
  "summary": "OPEN / UPDATE / KEEPALIVE / NOTIFICATION。",
  "key_points": [
    "**OPEN**: 建 TCP 后认证，开 BGP session",
    "**UPDATE**: 主力 — 宣告新路径或撤回旧路径",
    "**KEEPALIVE**: 维持连接（idle 时也发）",
    "**NOTIFICATION**: 错误报告 + 关闭"
  ]
},

"lec19:15": {
  "title": "BGP Path Attributes ⭐⭐",
  "summary": "Advertise route = (prefix, AS-PATH, NEXT-HOP)。Policy 决定 import/export。",
  "key_points": [
    "**Prefix**: 被 advertise 的目的子网（如 200.23.16.0/20）",
    "**AS-PATH**: 沿途经过的 AS 列表（如 [AS2, AS3]）",
    "**NEXT-HOP**: 到下一 AS 的具体 IP（哪个 router 接口）",
    "**Policy**: import 决定接不接；export 决定 advertise 给谁"
  ],
  "explanation": "### AS-PATH 的两个作用\n1. **防环**：如果自己 AS 在 AS-PATH 里，reject（说明这条路径已经回到了自己）\n2. **路径长度比较**：用 AS-PATH 长度（hop count）做 tie-break\n\n### NEXT-HOP 的细微\n不是『下一个 AS 的边界 router』那么简单。是『去那个目的，AS 内应该走的下一跳 IP』。iBGP 把 NEXT-HOP 传到 AS 内所有 router 后，每个 router 通过 OSPF 算到 NEXT-HOP 怎么走。\n\n### Policy 的实际配置\n```\nimport policy: \n  accept from neighbor X if AS-PATH 不含 Y\n  reject from Z all\nexport policy:\n  advertise to customer all\n  advertise to peer only own prefixes\n  advertise to provider only own prefixes\n```\n\n### 考法\n『BGP advertisement 包含什么？』→ AS-PATH + NEXT-HOP + prefix。"
},

"lec19:16": {
  "title": "BGP Path Advertisement — 单条路径",
  "summary": "AS3 → AS2 → AS1 的 path advertisement 传播链。",
  "explanation": "### 例\n1. AS3 边界 router 3a 通过 eBGP advertise『去 X 经 AS3』给 AS2 边界 2c\n2. AS2 根据 policy 接受，2c 通过 iBGP 传给 AS2 所有 router\n3. AS2 边界 2a 根据 policy 决定 advertise『去 X 经 AS2-AS3』给 AS1 边界 1c\n4. ..."
},

"lec19:17": {
  "title": "BGP Path Advertisement — 多路径",
  "summary": "Gateway 可能学到多条路径，按 policy 选一条。",
  "explanation": "### 例\nAS1 的 1c 同时学到：\n- 经 AS3 直接：AS-PATH = [AS3]\n- 经 AS2 转：AS-PATH = [AS2, AS3]\n\n1c 按 policy 选 [AS3]（更短），advertise 到 AS1 内部。"
},

"lec19:18": {
  "title": "BGP 填 FT (1) — iBGP + OSPF 配合",
  "summary": "1c 通过 iBGP 告诉所有 router 『X 经 1c』；OSPF 告诉每个 router 怎么到 1c。",
  "explanation": "### 完整例\n1d 收到 iBGP 信息：『X 经 1c』\n1d 跑 OSPF：到 1c 走 interface 1（intra-AS 最短路径）\n→ 1d 的 FT：去 X 的包从 interface 1 出"
},

"lec19:19": {
  "title": "BGP 填 FT (2) — 另一个 router 的视角",
  "summary": "1a 同样：iBGP 给『X 经 1c』；OSPF 算到 1c 走 interface 2 → FT: X → interface 2。"
},

"lec19:20": {
  "title": "Hot Potato Routing ⭐",
  "summary": "对多条出口路径，选 intra-AS 最便宜的，扔出 AS 给别人 carry。",
  "key_points": [
    "Router 学到多条到目的的路径",
    "如果都通过本 AS 不同 gateway 出去",
    "选 **intra-AS 代价最小的 gateway**（最快扔出去）",
    "不管出 AS 后路径长短"
  ],
  "explanation": "### 直觉\n烫手山芋赶紧扔。这个例子里 2d 学到去 X 可以经 2a 或 2c，即使经 2a 后整体 AS-PATH 更长，2d 仍选 2a（因为 2d 到 2a 的 OSPF cost 比 2d 到 2c 小）。\n\n### 经济动机\nCarry traffic on your own network costs money（电费、带宽、SLA）。能让别人扛就让别人扛。\n\n### 反之 — Cold potato\n有些 ISP 反过来：流量在自己网内多 carry 一段，目标是把流量送到最优的对外出口（性能最好）。代价是自己网多扛流量，但客户体验好。\n\n### 考法\n『hot potato 是什么？为什么这么做？』必答 2 点：选 intra-AS 最便宜出口 + 经济动机。"
},

"lec19:21": {
  "title": "BGP Policy via Advertisements (1) ⭐",
  "summary": "ISP 不替别人 carry transit traffic：通过『不 advertise』实现。",
  "key_points": [
    "B 学到 A → w 路径（A 是 B 的 customer）",
    "C 想问 B：『有去 w 的路吗？』",
    "B 选择 **不 advertise『C 经 B 经 A 到 w』**",
    "C 学不到这条路径，不会经 B 到 w"
  ],
  "explanation": "### Policy 通过 advertise/不-advertise 实现\n你 advertise 什么，邻居才知道什么；你不 advertise，对方根本不知道这条路存在。\n\n### 经济原因\nB 跟 C 是 peering（互发对方 customer 流量免费）。如果 B 让 C 经过 B 到 A（另一个 ISP）的客户 w，B 替别人扛流量却拿不到钱 → 拒绝。\n\n### Final Q3 — Columbia/CERN/NYU\n完全同样的模式：\n- Columbia 有 customer『Columbia 自己人』\n- Columbia 有 peer『NYU』\n- Columbia 到 CERN 的链路是为自己 customer 用的\n- Columbia **不向 NYU advertise** 这条路径\n- NYU 看不到 → 不会用 Columbia 转去 CERN\n\n→ 政策完全通过 BGP advertisement 控制实现，不需要 firewall 或显式 deny。"
},

"lec19:22": {
  "title": "BGP Policy (2) — Customer 视角",
  "summary": "X 是 dual-homed customer（接两个 ISP），通过『不 advertise』实现『不当 transit』。",
  "explanation": "### 场景\nX 同时接 ISP B 和 ISP C（图中 x 连 B 和 C）。X 不想替 B 和 C 之间当过境（成本 + 法律）。\n\nX 的策略：**不向 B advertise 去 C 的路径**。\n\n这样 B 看不到经 X 到 C 的路 → B 永远不会通过 X 路由到 C → X 不会被夹在中间当 transit。\n\n这就是 'customer 不当 transit' 的标准做法。"
},

"lec19:23": {
  "title": "BGP Route Selection — 优先级 ⭐",
  "summary": "1) Local preference 2) Shortest AS-PATH 3) Closest NEXT-HOP (hot potato) 4) Others。",
  "key_points": [
    "**1. Local pref**: 管理员配置的偏好（policy 决策）",
    "**2. Shortest AS-PATH**: 经过 AS 数最少",
    "**3. Closest NEXT-HOP**: hot potato（intra-AS 最便宜出口）",
    "**4. Tie-breakers**: e.g. router ID 最小"
  ],
  "explanation": "### 这个顺序决定一切\n当 BGP 学到多条到同一前缀的路径，按这个顺序逐级 tie-break。**Local pref 永远第一**，因为它代表 policy（policy 高于路径短）。\n\n### 例\n两条路径：\n- 路径 A：AS-PATH=[AS2, AS3]，local pref=100\n- 路径 B：AS-PATH=[AS3]，local pref=200\n\n按 step 1：local pref 200 > 100 → 选 B？等等，路径 A 写错了，应该是 local pref 配置的优先级。**Local pref 大的赢**。\n\n### 考法\n『BGP 多条路径怎么选？』按 4 步顺序答。"
},

"lec19:24": {
  "title": "Why Different Intra vs Inter? ⭐",
  "summary": "Policy + Scale + Performance —— 三个原因。",
  "key_points": [
    "**Policy**: inter-AS 跨多个管理实体，必须支持 policy；intra-AS 单管理无需 policy",
    "**Scale**: 分层路由表显著缩小 + 更新流量减少",
    "**Performance**: intra-AS 可以为性能优化；inter-AS 政策第一"
  ],
  "explanation": "### 三个原因的具体含义\n\n**Policy**：\n- inter: ISP 不愿 carry transit、不愿走某 AS、收不同价钱 → BGP 必须能配 policy\n- intra: Columbia 内部就一家管，policy 不重要\n\n**Scale**：\n- 不分层：整网 1 亿条 host 路由\n- 分层：每个 AS 自己几千-几万条，AS 之间几十万 BGP 前缀\n- 路由表小好几个数量级\n\n**Performance**：\n- intra-AS 节点都信任，可以为最短路径全力优化\n- inter-AS 不可能让 ISP A 替 ISP B 优化性能（B 自己掂量）\n\n### 考法（高频简答）\n『为什么不用一个统一的协议处理 intra 和 inter？』必答 3 点。"
},

"lec19:25": {
  "title": "Quiz — TCP Throughput（接 lec20）",
  "summary": "AIMD throughput = 3W/(4·RTT)。"
},

}

def main():
    data = json.loads(DETAIL.read_text())
    data.update(NEW)
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"updated {len(NEW)} entries; total now {len(data)}")

if __name__ == "__main__":
    main()
