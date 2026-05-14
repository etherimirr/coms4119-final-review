#!/usr/bin/env python3
"""Mark important slides per Final Preview reference.

Adds an `important` string field to selected entries in explanations_detail.json.
The string is a 1-line reason "why this slide is exam-critical".
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

# Map "lecXX:page" -> reason.
# Cross-referenced with final-preview.pdf's 5 sample questions:
#   Q1 = TCP loss vs congestion (bit error, checksum)         → lec14 ECN, lec23 wireless
#   Q2 = DHCP / CIDR subnet calc (128.16.51.2 /20)            → lec17 CIDR, DHCP, lec16 LPM
#   Q3 = BGP policy (Columbia/CERN/NYU)                       → lec19 BGP policy
#   Q4 = Distance vector tables (4 nodes)                     → lec18 DV/BF, CTI
#   Q5 = Hidden / exposed terminal                            → lec23 wireless MAC
# Plus other guaranteed-frequent topics (TCP FSM, AIMD, Dijkstra,
# Ethernet/ARP/Switch, OpenFlow, CRC, ALOHA derivation).
IMPORTANT = {
    # ─────────── lec14 (TCP Congestion Control) ───────────
    "lec14:6":  "🔥 AIMD 几何收敛——TCP 公平性的唯一保证；考前必懂为什么 AIMD 唯一",
    "lec14:8":  "🔥 两种丢包反应不同——3 dup ACK = 切半续跑；timeout = 重启 slow start",
    "lec14:10": "🔥 ssthresh 切换点——丢包前 cwnd 的一半",
    "lec14:12": "🔥🔥 TCP CC FSM 必考——fast recovery + new ACK → CA，不是 slow start！",
    "lec14:20": "🔥 ECN——final Q1 的反向参考：没 ECN 时丢包 ≠ 拥塞",

    # ─────────── lec16 (Network DP basics) ───────────
    "lec16:3":  "TCP 公平性 + AIMD 前提条件",
    "lec16:11": "Forwarding vs Routing 核心对比",
    "lec16:24": "🔥 LPM——IP 层最常考的查表",
    "lec16:25": "LPM 例 1 - 位级匹配",
    "lec16:36": "HOL blocking 概念",
    "lec16:43": "WFQ 公式 + min-BW 保证",

    # ─────────── lec17 (IP / DHCP / NAT) ───────────
    "lec17:4":  "🔥 IPv4 datagram 字段——填空题/解释每字段含义",
    "lec17:8":  "Subnet 概念 + IP = 接口（不是 host）",
    "lec17:11": "🔥🔥 CIDR——final Q2 直接考；二进制 AND 必练",
    "lec17:15": "🔥 DHCP DORA——必背 4 步广播",
    "lec17:16": "🔥 DHCP 返回 4 样：IP + gateway + DNS + mask",
    "lec17:20": "🔥 路由聚合——为什么 hierarchical addressing 可扩展",
    "lec17:23": "🔥 NAT 实现 + 优缺点",
    "lec17:28": "🔥 LPM Quiz——必练这种题；位级对比规则",

    # ─────────── lec18 (IPv6 + Routing intro + Dijkstra + DV) ───────────
    "lec18:1":  "IPv6 动机——32 位不够 + 简化 header",
    "lec18:2":  "🔥 IPv6 datagram——128 b 地址、40 B 固定头、去 checksum/fragmentation",
    "lec18:7":  "Tunneling——逻辑 vs 物理视图，header 嵌套",
    "lec18:18": "🔥 Graph 抽象——cost 来源 + 非负权假设",
    "lec18:19": "🔥 LS 大嘴 vs DV 悄悄话——两种方法论",
    "lec18:26": "🔥🔥 Dijkstra 伪代码必背——6 节点演示必练手算",
    "lec18:38": "Dijkstra 最短路径树 + forwarding table 产出",
    "lec18:39": "Dijkstra 复杂度 O(n²) + 消息复杂度",
    "lec18:43": "🔥🔥 Bellman-Ford 方程——final Q4 核心",
    "lec18:44": "🔥 DV 距离表数据结构——每节点表 + 行 min",
    "lec18:48": "🔥 DV 邻居更新例——必会手推",
    "lec18:52": "🔥 Count-to-Infinity——坏消息慢传 + 互推现象",
    "lec18:53": "🔥 Poison Reverse——半解 CTI，只破 2 节点环",
    "lec18:54": "🔥🔥 LS vs DV 三大维度对比——必背全表",

    # ─────────── lec19 (BGP + OSPF) ───────────
    "lec19:3":  "🔥 AS 分区原因——scale + 管理自治",
    "lec19:7":  "🔥 OSPF——Open + LS + Dijkstra + area 层级",
    "lec19:11": "🔥🔥 BGP——'胶水协议'，path vector，跨 AS 必考",
    "lec19:12": "🔥 eBGP vs iBGP 分工",
    "lec19:15": "🔥🔥 BGP path attributes——AS-PATH + NEXT-HOP 必背",
    "lec19:20": "🔥 Hot Potato——intra-AS 最便宜出口",
    "lec19:21": "🔥🔥 BGP Policy——final Q3 完全一样的题",
    "lec19:23": "🔥 BGP 路由选择优先级——4 步必背",
    "lec19:24": "🔥 Why intra ≠ inter——三大原因（policy/scale/perf）",

    # ─────────── lec20 (SDN + Link error detection) ───────────
    "lec20:1":  "🔥🔥 TCP throughput = 3W/(4·RTT)——公式 + 推导",
    "lec20:3":  "🔥 Generalized forwarding——match + action 抽象",
    "lec20:9":  "🔥 OpenFlow 抽象——router/firewall/switch/NAT 统一",
    "lec20:17": "SDN 集中控制动机——4 大动机",
    "lec20:19": "🔥 SDN 三大设计原则",
    "lec20:39": "Parity 1D + 2D——基础错检",
    "lec20:42": "🔥 CRC 概念——D·2^r mod G = R",
    "lec20:43": "🔥🔥 CRC 计算例——手算长除法必会",

    # ─────────── lec21 (Data Link MAC) ───────────
    "lec21:5":  "🔥 Link layer 4 件事——必背",
    "lec21:8":  "Channel partition——TDMA/FDMA/CDMA",
    "lec21:14": "Slotted ALOHA 假设和操作",
    "lec21:15": "🔥🔥 ALOHA 效率 1/e 推导——必会数学",
    "lec21:18": "🔥 CSMA 为什么仍碰撞——propagation delay",
    "lec21:19": "🔥 CSMA/CD——有线 detect + abort + binary backoff",
    "lec21:21": "🔥 CSMA/CD 2d 推导——min frame size 来源",
    "lec21:22": "🔥 Min frame 64 B 数字 + max cable 100 m",
    "lec21:26": "🔥 Ethernet frame 格式——必背字段",
    "lec21:27": "🔥 MAC address vs IP——必备对比",

    # ─────────── lec22 (Switch + Wireless intro) ───────────
    "lec22:1":  "🔥 BDP 计算——期中考过",
    "lec22:3":  "🔥 DHCP 返回 4 样",
    "lec22:7":  "🔥🔥 ARP 跨子网——必考的陷阱：找的是网关 MAC",
    "lec22:13": "🔥 Switch 自学习——流程必会，给 frame 序列画 table",
    "lec22:17": "VLAN——traffic isolation + 跨 VLAN 需 router",
    "lec22:18": "🔥🔥 Router vs Switch 对比表——必背全行",
    "lec22:28": "🔥 Pathloss 公式——频率与衰减关系",
    "lec22:30": "Real pathloss with α——环境系数",

    # ─────────── lec23 (Wireless MAC) ───────────
    "lec23:5":  "🔥 Multipath fading——ISI + coherence time",
    "lec23:7":  "🔥 SNR/SINR——dB 计算 + rate adaptation",
    "lec23:10": "🔥 Wireless ≠ Wired——两条根源驱动整章设计",
    "lec23:15": "🔥 三种 range——transmission/interference/sensing 的层次",
    "lec23:18": "🔥🔥 Sender-driven vs receiver-side——隐藏终端根源",
    "lec23:19": "🔥🔥🔥 Hidden Terminal——final Q5 直接考",
    "lec23:20": "🔥🔥🔥 Exposed Terminal——final Q5 直接考；与隐藏相反方向",
    "lec23:23": "🔥 MACA RTS/CTS——解 hidden 不解 exposed",
    "lec23:27": "🔥 CSMA/CA 三大机制——物理 CS + 虚拟 CS + collision avoidance",
    "lec23:29": "🔥 CSMA/CA 完整流程——DIFS vs SIFS 优先级",
    "lec23:32": "🔥 Binary exponential backoff——CW × 2 / 复位",
    "lec23:39": "🔥 802.11 channels 1/6/11 不重叠",
}


def main():
    data = json.loads(DETAIL.read_text())
    added = 0
    for key, reason in IMPORTANT.items():
        if key in data:
            data[key]["important"] = reason
            added += 1
        else:
            print(f"[skip] {key} not in detail file")
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"added 'important' on {added} entries")


if __name__ == "__main__":
    main()
