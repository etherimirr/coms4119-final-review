#!/usr/bin/env python3
"""Reset and re-apply STRICT important markers.

Strict criteria:
- 🔥🔥🔥: directly tested in midterm Q1–Q7 OR final-preview Q1–Q5
- 🔥🔥: core formula / algorithm necessary to solve those questions
- 🔥: a single conceptual page that the exam questions hinge on
- No marker: everything else (titles, intros, recap, repeats, side topics)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

# Strict-criteria important markers only
STRICT = {
    # ───── lec5-web (mid Q1: HTTP RTT) ─────
    "lec5-web:8":  "🔥 HTTP 持久 vs 非持久 — mid Q1 选项依据",
    "lec5-web:11": "🔥🔥🔥 Non-persistent response time = 2 RTT/obj — mid Q1 公式来源",
    "lec5-web:12": "🔥 Persistent + pipelining — mid Q1 4 RTT 答案的前提",

    # ───── lec7 (mid Q1: socket count) ─────
    "lec7:7":  "🔥🔥 UDP server = 1 socket — mid Q1 答案",
    "lec7:12": "🔥🔥 TCP server = N+1 sockets — mid Q1 答案",

    # ───── lec8-dns (mid Q1: DNS over UDP) ─────
    "lec8-dns:14": "🔥 DNS 4 层 — root/TLD/auth 必背",

    # ───── lec9-p2p (mid Q7: CS vs P2P) ─────
    "lec9-p2p:19": "🔥🔥🔥 CS time = max(NF/U_s, F/d_min) — mid Q7 公式",
    "lec9-p2p:20": "🔥🔥🔥 P2P time = max(F/U_s, F/d_min, NF/(U_s+ΣU_i)) — mid Q7 公式",

    # ───── lec3-basics2 (mid Q2/Q4: store-and-forward, delays) ─────
    "lec3-basics2:12": "🔥🔥 Store-and-forward — mid Q2 直接",
    "lec3-basics2:16": "🔥 4 种延迟 — mid Q4 端到端公式",

    # ───── lec11-reliability (mid Q3/Q5: GBN, stop-and-wait) ─────
    "lec11-reliability:42": "🔥🔥🔥 Stop-and-Wait U 公式 — mid Q5",
    "lec11-reliability:43": "🔥🔥 Stop-and-Wait U 推导 — mid Q5",
    "lec11-reliability:47": "🔥🔥🔥 GBN sender — mid Q3",
    "lec11-reliability:48": "🔥🔥🔥 GBN receiver(累积 ACK) — mid Q3",

    # ───── lec12-tcp (mid Q3/Q6: SR + flow control) ─────
    "lec12-tcp:1":  "🔥🔥🔥 Selective Repeat — mid Q3",
    "lec12-tcp:2":  "🔥🔥 SR 窗口大小 — mid Q3",
    "lec12-tcp:21": "🔥🔥🔥 TCP flow control rwnd — mid Q6 直接",

    # ───── lec13-congestion (slow start / AIMD) ─────
    "lec13-congestion:6":  "🔥 TCP 3-way handshake — 必背",
    "lec13-congestion:32": "🔥 Slow Start 概念 — 必背",
    "lec13-congestion:36": "🔥🔥 TCP AIMD — 必背核心",

    # ───── lec14 (TCP CC: FSM, AIMD, ECN) ─────
    "lec14:6":  "🔥 AIMD 几何收敛 — 必背公平性证明",
    "lec14:12": "🔥🔥🔥 TCP CC FSM — 必考；fast recovery + new ACK → CA 不是 slow start",
    "lec14:20": "🔥 ECN — final Q1 反向参考（没 ECN 时丢包≠拥塞）",

    # ───── lec16 (Network DP) ─────
    "lec16:12": "🔥 Data Plane vs Control Plane — 概念核心",

    # ───── lec17 (IP/DHCP/NAT) ─────
    "lec17:4":  "🔥 IPv4 datagram 字段 — 填空必考",
    "lec17:11": "🔥🔥🔥 CIDR — final Q2 直接",
    "lec17:15": "🔥 DHCP DORA — 4 步流程必背",
    "lec17:23": "🔥 NAT 实现机制 — 必考",
    "lec17:28": "🔥🔥 LPM Quiz — 期末类似题",

    # ───── lec18 (Dijkstra, DV/BF) ─────
    "lec18:26": "🔥🔥 Dijkstra 伪代码 — 必背",
    "lec18:43": "🔥🔥🔥 Bellman-Ford 方程 — final Q4 核心",
    "lec18:52": "🔥 Count-to-Infinity — 经典现象",
    "lec18:53": "🔥 Poison Reverse — 只破 2-node 环",
    "lec18:54": "🔥🔥 LS vs DV 对比表 — 必背",

    # ───── lec19 (BGP) ─────
    "lec19:7":  "🔥 OSPF — intra-AS, LS, area 层级",
    "lec19:11": "🔥🔥 BGP 基础 — path vector + TCP",
    "lec19:15": "🔥🔥 BGP path attributes (AS-PATH + NEXT-HOP) — 必背",
    "lec19:21": "🔥🔥🔥 BGP Policy — final Q3 完全一样的题",
    "lec19:23": "🔥 BGP 路由选择 4 步优先级",

    # ───── lec20 (SDN + CRC) ─────
    "lec20:1":  "🔥🔥 TCP throughput = 3W/(4·RTT) — 必背公式",
    "lec20:3":  "🔥 Match + Action — OpenFlow 抽象",
    "lec20:43": "🔥🔥 CRC 手算例 — 必会",

    # ───── lec21 (Data Link) ─────
    "lec21:15": "🔥🔥 Slotted ALOHA 1/e 推导 — 必会数学",
    "lec21:22": "🔥 CSMA/CD min frame — 2d 推导",
    "lec21:26": "🔥 Ethernet frame 格式 — 必背字段",

    # ───── lec22 (ARP, Switch) ─────
    "lec22:7":  "🔥🔥 ARP 跨子网找 first-hop router — 经典陷阱",
    "lec22:13": "🔥 Switch 自学习 — 流程必会",
    "lec22:18": "🔥 Router vs Switch — 必背对比",

    # ───── lec23 (Wireless MAC) ─────
    "lec23:19": "🔥🔥🔥 Hidden Terminal — final Q5 直接",
    "lec23:20": "🔥🔥🔥 Exposed Terminal — final Q5 直接",
    "lec23:23": "🔥 RTS/CTS — 解 hidden 不解 exposed",
    "lec23:29": "🔥 CSMA/CA 完整流程 — DIFS vs SIFS",

    # ───── final-preview (the 5 exam questions themselves) ─────
    "final-preview:10": "🔥🔥🔥 Final Q1 — Loss ≠ Congestion",
    "final-preview:11": "🔥🔥🔥 Final Q2 — CIDR/Subnet calc",
    "final-preview:12": "🔥🔥🔥 Final Q3 — BGP policy",
    "final-preview:13": "🔥🔥🔥 Final Q4 — DV table",
    "final-preview:14": "🔥🔥🔥 Final Q5 — Hidden/Exposed",
}


def main():
    data = json.loads(DETAIL.read_text())

    # Step 1: remove all existing `important` markers
    removed = 0
    for key in list(data.keys()):
        if "important" in data[key]:
            del data[key]["important"]
            removed += 1
        # Drop entries that became empty (were stub-only)
        if not data[key]:
            del data[key]

    # Step 2: apply strict set
    added = 0
    for key, reason in STRICT.items():
        if key not in data:
            data[key] = {}
        data[key]["important"] = reason
        added += 1

    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"removed {removed} old markers; added {added} strict markers")


if __name__ == "__main__":
    main()
