#!/usr/bin/env python3
"""Mark important pre-midterm slides per midterm Q1-Q7 + foundation topics."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

IMPORTANT = {
    # ─────────── lec2-basics1 ───────────
    "lec2-basics1:7":  "🔥 什么是协议——格式 + 顺序 + 动作（基础概念）",
    "lec2-basics1:26": "Circuit Switching 基础",
    "lec2-basics1:31": "🔥 Packet Switching——Internet 选这个的根本原因",
    "lec2-basics1:33": "Network core 两功能：forwarding + routing",
    "lec2-basics1:36": "🔥 Packet vs Circuit 对比表——必考题型",

    # ─────────── lec3-basics2 ───────────
    "lec3-basics2:12": "🔥🔥 Store-and-forward——mid Q2 直接考",
    "lec3-basics2:14": "队列延迟——网络拥塞的根",
    "lec3-basics2:16": "🔥🔥 Packet delay 4 类来源——transmission/propagation/queuing/processing 必背",
    "lec3-basics2:17": "Packet delay 4 类来源（续）",
    "lec3-basics2:18": "Caravan analogy——理解 store-and-forward 的直觉",
    "lec3-basics2:23": "Packet loss——队列溢出导致",
    "lec3-basics2:24": "🔥🔥 Throughput——min(per-link R) 必考",
    "lec3-basics2:25": "Throughput 续",
    "lec3-basics2:26": "🔥 Throughput 多场景——end-to-end vs per-link",

    # ─────────── lec4-basics3 ───────────
    "lec4-basics3:3":  "Layering 模块化思想",
    "lec4-basics3:7":  "🔥 5 层协议栈——必背 L1-L7 + 各层例",
    "lec4-basics3:9":  "🔥 Services / Layering / Encapsulation",
    "lec4-basics3:12": "🔥 Encapsulation 流程——每层加自己 header",
    "lec4-basics3:18": "🔥 End-to-end principle——把复杂放在端",
    "lec4-basics3:23": "Client-server 模型",
    "lec4-basics3:25": "🔥 Processes communicating 概念",
    "lec4-basics3:26": "🔥 Sockets 抽象",
    "lec4-basics3:29": "Transport service 需求——可靠/带宽/timing",
    "lec4-basics3:31": "🔥 Internet transport：TCP vs UDP 对比",

    # ─────────── lec5-web (HTTP, mid Q1) ───────────
    "lec5-web:6":  "🔥 HTTP overview——request/response model",
    "lec5-web:8":  "🔥🔥 HTTP 两种连接类型——非持久 vs 持久",
    "lec5-web:9":  "🔥🔥 Non-persistent HTTP 例——RTT 计数基础（mid Q1）",
    "lec5-web:10": "🔥🔥 Non-persistent 续——多对象时 RTT × 2",
    "lec5-web:11": "🔥🔥🔥 Non-persistent response time = 2 RTT/obj——mid Q1 公式来源",
    "lec5-web:12": "🔥🔥 Persistent HTTP 1.1——pipelining 思想",
    "lec5-web:13": "HTTP request message 格式",
    "lec5-web:16": "HTTP response message 格式",
    "lec5-web:17": "🔥 HTTP 状态码——200/301/404/505",
    "lec5-web:19": "🔥 Cookies——HTTP 无状态 + 服务端状态",
    "lec5-web:28": "HTTP/2 改进",
    "lec5-web:30": "🔥 HTTP/2 HOL blocking 缓解",

    # ─────────── lec6-video ───────────
    "lec6-video:1":  "Video streaming 占带宽 80%",
    "lec6-video:10": "🔥 DASH——可变 bitrate adapter",
    "lec6-video:11": "🔥 CDN——把内容放近用户",

    # ─────────── lec7 (Socket, mid Q1) ───────────
    "lec7:5":  "🔥 Socket programming 概念",
    "lec7:7":  "🔥🔥 UDP socket——server 端 1 个 socket（mid Q1）",
    "lec7:8":  "🔥🔥 UDP client/server 交互——sendto/recvfrom",
    "lec7:12": "🔥🔥 TCP socket——server N+1 sockets（mid Q1）",
    "lec7:13": "🔥🔥 TCP socket 交互——bind/listen/accept",

    # ─────────── lec8-dns ───────────
    "lec8-dns:7":  "🔥 DNS 是什么——name ↔ address 映射",
    "lec8-dns:12": "🔥 DNS 是分布式 + 层级 + 缓存",
    "lec8-dns:14": "🔥🔥 DNS 4 层层级——root → TLD → authoritative",
    "lec8-dns:18": "🔥 Local DNS name server——客户端入口",
    "lec8-dns:19": "🔥🔥 Iterative query——本地 server 一跳一跳问",
    "lec8-dns:20": "🔥🔥 Recursive query——server 帮你递归到底",
    "lec8-dns:21": "🔥 DNS Caching——TTL 软状态",
    "lec8-dns:22": "🔥 DNS records 类型——A, NS, CNAME, MX",
    "lec8-dns:28": "DNS Quiz",

    # ─────────── lec9-p2p (BitTorrent, mid Q7) ───────────
    "lec9-p2p:9":  "🔥 BitTorrent 基本架构",
    "lec9-p2p:10": "🔥 Simultaneous downloading——P2P 核心优势",
    "lec9-p2p:17": "🔥 Anti free-riding——tit-for-tat",
    "lec9-p2p:18": "🔥🔥🔥 File distribution: CS vs P2P——mid Q7 直接",
    "lec9-p2p:19": "🔥🔥🔥 CS time = max(NF/U_s, F/d_min)——必背",
    "lec9-p2p:20": "🔥🔥🔥 P2P time = max(F/U_s, F/d_min, NF/(U_s + ΣU_i))——必背",
    "lec9-p2p:21": "🔥 Numerical example——CS 大 N 输给 P2P",

    # ─────────── lec10-transport ───────────
    "lec10-transport:2":  "DHT 概念",
    "lec10-transport:12": "🔥 Transport services 概览",
    "lec10-transport:13": "🔥 Transport vs Network layer——端到端 vs 跳到跳",
    "lec10-transport:17": "🔥🔥 TCP/UDP 双协议",
    "lec10-transport:19": "🔥🔥 Multiplexing/Demultiplexing——核心概念",
    "lec10-transport:30": "🔥 Demux 流程——按 (src/dst IP, port) 分发",
    "lec10-transport:31": "🔥🔥 Connectionless (UDP) demux——dst port 即可",
    "lec10-transport:33": "🔥🔥 Connection-oriented (TCP) demux——按 4-tuple",
    "lec10-transport:35": "🔥 Mux/Demux 总结",

    # ─────────── lec11-reliability (RDT, GBN/SR, mid Q3 Q5 Q6) ───────────
    "lec11-reliability:3":  "UDP 协议结构",
    "lec11-reliability:6":  "🔥 UDP transport actions——封装/解封",
    "lec11-reliability:9":  "🔥 UDP segment header——8 字节",
    "lec11-reliability:10": "🔥 UDP checksum——错检",
    "lec11-reliability:11": "🔥 Internet checksum——16 bit 字累加",
    "lec11-reliability:12": "🔥 Checksum 例——具体计算",
    "lec11-reliability:16": "🔥🔥 RDT 原理——5 个机制",
    "lec11-reliability:17": "RDT 原理续",
    "lec11-reliability:22": "🔥 数据传输可能出错的 5 种情况",
    "lec11-reliability:23": "🔥 rdt 1.0——完美信道",
    "lec11-reliability:24": "🔥 rdt 2.0——加 ACK + checksum 处理 bit error",
    "lec11-reliability:26": "🔥 rdt 2.0 FSM——sender + receiver",
    "lec11-reliability:30": "🔥 rdt 2.0 fatal flaw——ACK 损坏怎么办？",
    "lec11-reliability:31": "🔥 rdt 2.1——加 seq #",
    "lec11-reliability:34": "🔥 rdt 2.2——NAK-free 协议",
    "lec11-reliability:36": "🔥 rdt 3.0——加 timer 处理丢失",
    "lec11-reliability:40": "🔥 rdt 3.0 in action——timeline",
    "lec11-reliability:42": "🔥🔥🔥 Performance of stop-and-wait——mid Q5 公式来源",
    "lec11-reliability:43": "🔥🔥 Stop-and-wait operation——U 公式推导",
    "lec11-reliability:45": "🔥 Pipelined protocols——overcome stop-and-wait limit",
    "lec11-reliability:46": "🔥🔥 Pipelining 提升 U——填满管道",
    "lec11-reliability:47": "🔥🔥🔥 GBN sender——mid Q3 直接",
    "lec11-reliability:48": "🔥🔥🔥 GBN receiver——累积 ACK",
    "lec11-reliability:49": "🔥🔥 GBN in action——timeline",

    # ─────────── lec12-tcp (mid Q6) ───────────
    "lec12-tcp:1":  "🔥🔥🔥 Selective Repeat 思想——mid Q3 直接",
    "lec12-tcp:2":  "🔥🔥 SR sender/receiver windows——窗口大小约束",
    "lec12-tcp:3":  "🔥🔥 SR sender + receiver 详细",
    "lec12-tcp:4":  "🔥 SR in action——timeline",
    "lec12-tcp:5":  "🔥 SR 序号歧义——窗口 ≤ N/2",
    "lec12-tcp:8":  "🔥 TCP overview——面向连接 + 可靠 + 流控 + 拥控",
    "lec12-tcp:9":  "🔥🔥 TCP segment structure——必背字段",
    "lec12-tcp:10": "🔥🔥 TCP seq# 和 ACK#——首字节序号语义",
    "lec12-tcp:11": "TCP seq# 例",
    "lec12-tcp:12": "🔥 TCP RTT estimation——EWMA α=0.125",
    "lec12-tcp:13": "🔥 TCP timeout 计算——EstRTT + 4·DevRTT",
    "lec12-tcp:15": "🔥 TCP Sender 行为简化版",
    "lec12-tcp:16": "🔥 TCP Receiver ACK 生成规则",
    "lec12-tcp:17": "🔥 TCP retransmission 场景",
    "lec12-tcp:19": "🔥🔥 TCP fast retransmit——3 dup ACK",
    "lec12-tcp:21": "🔥🔥🔥 TCP flow control——mid Q6 直接（rwnd）",
    "lec12-tcp:22": "🔥🔥 Flow control 细节",
    "lec12-tcp:23": "🔥🔥 Flow control 续",
    "lec12-tcp:24": "🔥🔥 Flow control 总结",

    # ─────────── lec13-congestion (3WHS, AIMD intro) ───────────
    "lec13-congestion:2":  "🔥 TCP connection management",
    "lec13-congestion:4":  "🔥 2-way handshake 为什么不够",
    "lec13-congestion:6":  "🔥🔥 TCP 3-way handshake——必背",
    "lec13-congestion:7":  "3WHS Step 1: SYN",
    "lec13-congestion:8":  "3WHS Step 2: SYN-ACK",
    "lec13-congestion:9":  "3WHS Step 3: ACK",
    "lec13-congestion:11": "🔥 TCP 4-way close + TIME_WAIT",
    "lec13-congestion:15": "🔥 Principles of congestion control",
    "lec13-congestion:17": "🔥 Congestion scenario 1——无 loss",
    "lec13-congestion:21": "🔥 Congestion scenario 2——有 loss",
    "lec13-congestion:23": "🔥 Congestion scenario 3——多跳",
    "lec13-congestion:25": "🔥🔥 Congestion insights——3 个结论",
    "lec13-congestion:26": "🔥 End-host vs Network-assisted CC",
    "lec13-congestion:32": "🔥🔥 Slow Start——指数增到 ssthresh",
    "lec13-congestion:33": "🔥🔥 Slow Start example——timeline",
    "lec13-congestion:35": "🔥🔥 How to adapt cwnd——四种增减策略",
    "lec13-congestion:36": "🔥🔥🔥 TCP AIMD——必考核心",
    "lec13-congestion:37": "🔥 TCP AIMD more details",

    # ─────────── midterm-preview ───────────
    "midterm-preview:1": "Midterm review 封面",
    "midterm-preview:2": "🔥 Recap content — performance metrics",
    "midterm-preview:3": "🔥 Recap content — application",
    "midterm-preview:4": "🔥 Recap content — transport",
}


def main():
    data = json.loads(DETAIL.read_text())
    added = 0
    skipped = 0
    for key, reason in IMPORTANT.items():
        if key in data:
            data[key]["important"] = reason
            added += 1
        else:
            data[key] = {"important": reason}
            skipped += 1
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"added 'important' on {added} existing entries, created {skipped} new stub entries")


if __name__ == "__main__":
    main()
