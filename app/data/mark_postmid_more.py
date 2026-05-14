#!/usr/bin/env python3
"""Expand 🔥 markers across all post-mid lectures, covering every key concept page.
Especially the conceptual pages (Data Plane vs Control Plane, etc.) the user
specifically called out.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW_MARKS = {
    # ─────────── lec14 (TCP Congestion Control) ───────────
    "lec14:2":  "🔥 四种增减策略——AIAD/AIMD/MIAD/MIMD 对比",
    "lec14:3":  "🔥 拥塞控制几何模型——(x1, x2) 坐标系",
    "lec14:7":  "🔥 cwnd 工作机制——LastByteSent - Acked < cwnd",
    "lec14:11": "Slow start restart 行为",
    "lec14:13": "🔥 CUBIC 直觉——切半后激进追回 Wmax",
    "lec14:14": "🔥 CUBIC 公式——W(t)=C(t-K)³+Wmax",
    "lec14:15": "🔥 Bottleneck link 概念",
    "lec14:16": "🔥 增 cwnd → RTT 升 ≠ 提吞吐量（BBR 的种子）",
    "lec14:17": "🔥 Delay-based CC 公式",
    "lec14:18": "🔥 Delay-based 缺点——跟 loss-based 共存 starve",
    "lec14:19": "🔥 BBR——估 BtlBw + RTprop，inflight=BDP",

    # ─────────── lec16 (Network DP basics) ───────────
    "lec16:4":  "🔥 公平性现实——UDP 和并行 TCP 破坏 AIMD 公平",
    "lec16:10": "🔥 Network layer services——封装 segment → datagram",
    "lec16:12": "🔥🔥 Data Plane vs Control Plane——核心分层概念",
    "lec16:13": "Per-router control plane（传统）",
    "lec16:14": "SDN control plane（现代）",
    "lec16:15": "🔥 Network service model——Internet best-effort vs ATM CBR/ABR vs IntServ/DiffServ",
    "lec16:16": "Service model 全表",
    "lec16:17": "🔥 Best-effort 反思——简单 = 普及 = 成功",
    "lec16:19": "🔥 Router 架构概览——CP 软件 ms / DP 硬件 ns",
    "lec16:21": "🔥 Input port 功能——match + action",
    "lec16:22": "🔥 Generalized forwarding——多字段匹配",
    "lec16:23": "Destination-based forwarding",
    "lec16:30": "🔥 Switching fabrics——memory/bus/interconnection",
    "lec16:31": "Switching fabrics 三类",
    "lec16:34": "🔥 Crossbar 互联——现代高端路由 100s Tbps",
    "lec16:37": "🔥 Output port queuing——丢包来源",
    "lec16:39": "🔥 Buffer management——drop policy + marking",
    "lec16:40": "FCFS scheduling",
    "lec16:41": "🔥 Priority scheduling",
    "lec16:42": "Round Robin",
    "lec16:44": "Network Neutrality——技术 + 社会 + 法律",
    "lec16:45": "🔥 Net Neutrality 三原则——no block / no throttle / no paid prio",

    # ─────────── lec17 (IP/DHCP/NAT) ───────────
    "lec17:3":  "🔥 Network Layer 三大组件——IP + ICMP + Routing",
    "lec17:5":  "🔥 IP 关联到 interface（不是 host！）",
    "lec17:9":  "🔥 Subnet 食谱——断开 router 看孤岛",
    "lec17:17": "🔥 DHCP 协议栈——DHCP/UDP/IP/Ethernet 封装",
    "lec17:18": "DHCP 应答路径",
    "lec17:21": "ICANN 分配 + IPv4 已分完",
    "lec17:25": "🔥 NAT 表实现——出包改 src 入包改 dst",
    "lec17:26": "🔥 NAT 实例图——10.0.0.1 ↔ 138.76.29.7",
    "lec17:27": "🔥 NAT 争议——违反端到端 + 阻碍 P2P + STUN/TURN",

    # ─────────── lec18 (IPv6 + Routing intro + DV) ───────────
    "lec18:3":  "🔥 IPv6 design philosophy——end-to-end principle",
    "lec18:4":  "🔥 IPv4 → IPv6 过渡——tunneling",
    "lec18:5":  "Tunneling 详图 1",
    "lec18:6":  "Tunneling 详图 2",
    "lec18:8":  "IPv6 采用率 ~49%",
    "lec18:12": "🔥 Network layer 两功能（复习）",
    "lec18:16": "🔥 What is routing? — Jon Postel 引言",
    "lec18:17": "🔥 Routing protocol 目标——找『好』路径",
    "lec18:20": "🔥 路由算法分类——global/decentralized × static/dynamic",
    "lec18:22": "LS step 1——本地 link state",
    "lec18:23": "🔥 LS step 2——flooding 全网",
    "lec18:24": "🔥 LS step 3-4——全网拓扑 → Dijkstra",
    "lec18:25": "🔥 Dijkstra 符号定义",
    "lec18:40": "Dijkstra 震荡问题——cost 跟流量相关时",
    "lec18:42": "Time for a Game——DV 直觉演示",
    "lec18:45": "🔥 DV 初始化——只填直连邻居",
    "lec18:46": "DV init 例（4 节点）",
    "lec18:47": "DV 发送 DV 给邻居",
    "lec18:49": "🔥 DV 核心 loop——周期 + 触发更新",
    "lec18:50": "🔥 DV 异步、自停",
    "lec18:51": "DV link cost ↓——好消息传得快",

    # ─────────── lec19 (BGP + OSPF) ───────────
    "lec19:2":  "🔥 Making routing scalable——分区原因",
    "lec19:4":  "🔥 Interconnected ASes——FT 来源（intra + inter）",
    "lec19:5":  "🔥 Inter-AS 在 intra forwarding 中的作用",
    "lec19:6":  "🔥 Intra-AS 协议家族——RIP/EIGRP/OSPF/IS-IS",
    "lec19:8":  "🔥 Hierarchical OSPF——area + backbone + ABR",
    "lec19:13": "BGP Session——TCP 长连接",
    "lec19:14": "🔥 BGP 4 类消息——OPEN/UPDATE/KEEPALIVE/NOTIFICATION",
    "lec19:16": "🔥 BGP path advertisement——单条路径传播链",
    "lec19:17": "🔥 BGP 多路径选择——policy 决定",
    "lec19:18": "🔥 BGP 填 FT——iBGP + OSPF 配合",
    "lec19:19": "🔥 BGP 填 FT (2)——另一 router 视角",
    "lec19:22": "🔥 BGP Policy (2)——customer 视角，dual-homed 不当 transit",

    # ─────────── lec20 (SDN + Link Error Detection) ───────────
    "lec20:5":  "🔥 Flow table 具体例",
    "lec20:6":  "🔥 OpenFlow flow entry——11 个 match 字段",
    "lec20:7":  "🔥 OpenFlow 例——router/firewall/block-sender",
    "lec20:8":  "OpenFlow 例——L2 dst MAC forwarding",
    "lec20:10": "🔥 OpenFlow 跨多 switch——network-wide 行为",
    "lec20:11": "OpenFlow 多 switch 实例",
    "lec20:12": "🔥 Generalized forwarding 小结",
    "lec20:14": "🔥 SDN 动机——传统 router 封闭",
    "lec20:15": "Per-router control plane（传统）",
    "lec20:16": "🔥 SDN control plane——远程 controller",
    "lec20:18": "🔥 SDN 类比——mainframe → PC 革命",
    "lec20:20": "Data plane switches——commodity",
    "lec20:21": "🔥 SDN Controller——network OS",
    "lec20:22": "Network control apps——routing/FW/LB",
    "lec20:23": "🔥 SDN Controller 内部——接口 + 状态管理 + 通信层",
    "lec20:24": "🔥 OpenFlow Protocol——TCP 长连接",
    "lec20:25": "🔥 OpenFlow controller→switch 消息",
    "lec20:26": "🔥 OpenFlow switch→controller 消息",
    "lec20:27": "🔥 SDN 交互例 (1)——link 失败响应",
    "lec20:28": "SDN 交互例 (2)——新路径下发",
    "lec20:34": "Link Layer 协议栈位置",
    "lec20:35": "From network to single link",
    "lec20:36": "🔥 Data Link Layer——跑在 NIC 里",
    "lec20:37": "Link Layer services（复习）",
    "lec20:38": "🔥 Error Detection 概念——冗余检测 bit 错",
    "lec20:40": "🔥 Parity 2D——检测 + 纠正单 bit 错",
    "lec20:41": "🔥 Checksum——TCP/UDP/IP 用",

    # ─────────── lec21 (Data Link MAC) ───────────
    "lec21:1":  "🔥 DV 收敛轮数 quiz",
    "lec21:6":  "🔥 两类链路媒介——P2P vs broadcast",
    "lec21:7":  "🔥 Share a medium——MAC 的本质",
    "lec21:9":  "🔥 MAC #2 Taking turns——polling vs token",
    "lec21:10": "How do you like these so far",
    "lec21:11": "🔥 MAC #3 Random access——核心 paradigm",
    "lec21:12": "Slotted ALOHA——Norm Abramson 1970",
    "lec21:13": "🔥 Slotted ALOHA 假设和操作",
    "lec21:16": "Slotted ALOHA 优缺点",
    "lec21:17": "Slotted ALOHA 不听信道问题",
    "lec21:20": "CSMA/CD 碰撞检测例",
    "lec21:23": "🔥 Random Access 三件套——CS + CD + Random",
    "lec21:24": "Ethernet 起源",
    "lec21:25": "🔥 Ethernet 演进——broadcast → switched",
    "lec21:28": "🔥 MAC 两种——burned-in vs effective (spoofing)",
    "lec21:29": "Bootstrap——DHCP + ARP",

    # ─────────── lec22 (Switch + Wireless intro) ───────────
    "lec22:2":  "DHCP 拿 IP",
    "lec22:4":  "🔥 Address Resolution 需求",
    "lec22:5":  "🔥 ARP 协议——广播 query + unicast reply",
    "lec22:6":  "🔥 ARP 表 + cache 机制——soft state",
    "lec22:8":  "🔥 ARP & DHCP 三大设计思想——broadcast + cache + soft state",
    "lec22:9":  "802.3 Ethernet 标准家族",
    "lec22:10": "🔥 Switches——L2 store-and-forward",
    "lec22:11": "🔥 Switch 多路并发——dedicated link + 全双工",
    "lec22:12": "Switch forwarding table——(MAC, port, ts)",
    "lec22:14": "VLAN 动机——大 LAN 广播流量 + 行政",
    "lec22:15": "VLAN 行政场景",
    "lec22:16": "🔥 Port-based VLAN 配置",
    "lec22:21": "🔥 Wireless 三层范围——WPAN/WLAN/WWAN",
    "lec22:27": "What happens after we cut the wire",
    "lec22:29": "Pathloss 频段对比表",

    # ─────────── lec23 (Wireless MAC) ───────────
    "lec23:1":  "🔥 Reflection——物体 ≫ λ",
    "lec23:2":  "🔥 Diffraction——锐利边绕射",
    "lec23:3":  "Diffraction 图示",
    "lec23:4":  "🔥 Scattering——物体 < λ，最难建模",
    "lec23:6":  "🔥 Multipath Coherence Time——限制 symbol rate",
    "lec23:8":  "Received Signal Over Time——实测剧烈波动",
    "lec23:9":  "🔥 Real environment α——实测建模",
    "lec23:11": "Wireless MAC 章节封面",
    "lec23:12": "The More, The Messier",
    "lec23:13": "🔥 Role of MAC——3 大职责",
    "lec23:14": "🔥 MAC Categories 三类",
    "lec23:16": "🔥 CSMA——listen before transmit",
    "lec23:17": "Discussion CSMA 够吗",
    "lec23:21": "Hidden terminal 应对——两条思路",
    "lec23:22": "Solution #1 Busy Tone",
    "lec23:24": "RTS/CTS 实例",
    "lec23:25": "🔥 802.11 = CSMA/CA",
    "lec23:26": "CSMA/CA 时序例",
    "lec23:28": "🔥 Random Backoff 详细——CW + freeze",
    "lec23:30": "如何选 CW",
    "lec23:31": "🔥 802.11 DCF——自适应 CW",
    "lec23:33": "🔥 MACAW——指数增 + 线性减",
    "lec23:34": "Solution #2 ZigZag——处理碰撞",
    "lec23:35": "ZigZag 详细",
    "lec23:36": "🔥 802.11 b/a/g/n/ac 标准家族",
    "lec23:37": "802.11 af/ah/ax 新一代",
    "lec23:38": "🔥 802.11 架构——Infrastructure vs Ad-hoc",

    # ─────────── final-preview ───────────
    "final-preview:2":  "🔥 Recap Basics——performance metrics",
    "final-preview:3":  "🔥 Recap Application Layer",
    "final-preview:4":  "🔥 Recap Transport (UDP/TCP)",
    "final-preview:5":  "🔥 Recap Transport (CC)",
    "final-preview:6":  "🔥 Recap Network DP",
    "final-preview:7":  "🔥 Recap Network CP",
    "final-preview:8":  "🔥 Recap Data Link (wired)",
    "final-preview:9":  "🔥 Recap Wireless",
    "final-preview:10": "🔥🔥 Example Q1——TCP loss ≠ congestion (bit error)",
    "final-preview:11": "🔥🔥🔥 Example Q2——CIDR DHCP 必练",
    "final-preview:12": "🔥🔥🔥 Example Q3——BGP policy",
    "final-preview:13": "🔥🔥🔥 Example Q4——DV table 必练",
    "final-preview:14": "🔥🔥🔥 Example Q5——Hidden/Exposed terminal",
}


def main():
    data = json.loads(DETAIL.read_text())
    added = 0
    new_stubs = 0
    for key, reason in NEW_MARKS.items():
        if key in data:
            # Only add if not already marked
            if "important" not in data[key]:
                data[key]["important"] = reason
                added += 1
        else:
            data[key] = {"important": reason}
            new_stubs += 1
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"added 'important' to {added} existing entries, created {new_stubs} stub entries")


if __name__ == "__main__":
    main()
