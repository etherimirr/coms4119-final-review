#!/usr/bin/env python3
"""Re-tag pre-midterm concepts with a new color group + add a few missing nodes.

Pre-midterm = up to and including flow control / sliding window (lec1-13).
Post-midterm = lec14+ (congestion control, network, link, wireless).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONCEPTS = ROOT / "concepts.json"

# Pre-midterm node IDs (everything we've been calling general/app and the basic transport pieces)
PRE_MID_IDS = {
    # general (all of these were pre-mid)
    "basics", "delays", "bdp", "throughput", "stop_wait_u",
    # app (all pre-mid)
    "app", "socket", "http", "rtt_count", "dns", "p2p", "file_dist_time", "video",
    # transport pre-mid pieces (intro + UDP/TCP basics + RDT + flow control)
    "transport", "udp", "tcp", "3whs", "rdt", "gbn", "sr", "flow_control",
}

# New pre-mid nodes to add
NEW_NODES = [
    {
        "id": "sliding_window",
        "label": "Sliding Window",
        "group": "pre_mid",
        "desc": "Sender 维护一个窗口 [base, base+N)，窗口内的包可以连发不等 ACK；ACK 回来 base 滑动。\n窗口大小要 ≥ BDP 才能填满管道。\n**Stop-and-Wait** 是窗口 = 1 的特例。",
        "refs": [{"file":"midterm","page":"Q6"}]
    },
    {
        "id": "rtt_estimation",
        "label": "RTT Estimation",
        "group": "pre_mid",
        "desc": "TCP 用 EWMA（指数加权移动平均）估 RTT：\nEstimatedRTT = (1−α)·EstimatedRTT + α·SampleRTT  (α ≈ 0.125)\nDevRTT = (1−β)·DevRTT + β·|SampleRTT − EstimatedRTT|  (β ≈ 0.25)\nTimeoutInterval = EstimatedRTT + 4·DevRTT",
        "formula": "$$\\text{EstRTT} \\leftarrow (1-\\alpha)\\cdot\\text{EstRTT} + \\alpha\\cdot\\text{SampleRTT}$$"
    },
    {
        "id": "web_cache",
        "label": "Web Cache (Proxy)",
        "group": "pre_mid",
        "desc": "Proxy server 缓存 HTTP 响应。Client 先问 proxy；命中直接返；未命中代为请求 origin 再缓存。\n**好处**: 减小 RTT / 节约外网带宽。\n**问题**: 一致性（用 Last-Modified / ETag + Conditional GET 解决）。"
    },
    {
        "id": "cond_get",
        "label": "Conditional GET",
        "group": "pre_mid",
        "desc": "客户端 / proxy 发 GET 带 `If-Modified-Since: <date>`。Server 若资源没变 → 返 `304 Not Modified`（无 body）；变了 → 返 200 + 新 body。\n这是 web cache 保持一致性的关键。"
    },
    {
        "id": "dht",
        "label": "DHT — 分布式哈希表",
        "group": "pre_mid",
        "desc": "每个 key 哈希到一个节点 ID。查找 key 时走 O(log N) 步到达 owner 节点。\nBitTorrent 用 DHT 替代中央 tracker，去中心化找 peer。"
    },
    {
        "id": "bt_mechanisms",
        "label": "BitTorrent Mechanisms",
        "group": "pre_mid",
        "desc": "**Rarest first**: 优先抢 swarm 里副本少的 chunk\n**Tit-for-tat**: 你给我多少我给你多少 → 激励上传\n**Optimistic unchoke**: 每 30s 随机选一个新邻居『无条件给』，探索更好的 peer"
    },
    {
        "id": "tcp_close",
        "label": "TCP 4-way Close",
        "group": "pre_mid",
        "desc": "关连接是双向半关 → 4 步：\n1. A → FIN\n2. B → ACK\n3. (B 把剩余数据发完)\n4. B → FIN\n5. A → ACK\n→ TIME_WAIT 状态保留 2·MSL 防止旧包扰新连接。"
    },
    {
        "id": "tcp_retx",
        "label": "TCP 重传机制",
        "group": "pre_mid",
        "desc": "**超时重传**: 没收到 ACK 超过 TimeoutInterval → 重发最早未确认包\n**Fast retransmit**: 收到 3 个 dup ACK 立刻重传那个包，不等 timeout\n超时之后 timer 翻倍（exp backoff），但收到正确 ACK 后用 RTT 估算重置"
    },
    {
        "id": "rdt_evolution",
        "label": "RDT 演化",
        "group": "pre_mid",
        "desc": "**rdt 1.0**: 完全可靠信道（无意义）\n**rdt 2.0**: 加 ACK + checksum（处理 bit error）\n**rdt 2.1**: 加 seq# 处理 ACK 损坏\n**rdt 2.2**: NAK-free（用 ACK + last seq）\n**rdt 3.0**: 加 timer 处理丢失（stop-and-wait）\n**Pipelined**: GBN / SR",
    },
    {
        "id": "tcp_segment",
        "label": "TCP Segment 格式",
        "group": "pre_mid",
        "desc": "**Header 20 B（无 options）**:\n- Source port (16 b) | Dest port (16 b)\n- Sequence # (32 b) — first byte of data\n- ACK # (32 b) — next expected byte\n- HLEN (4 b) | Flags: URG/ACK/PSH/RST/SYN/FIN/CWR/ECE\n- **Receive window** (16 b) — for flow control\n- Checksum (16 b) | Urgent ptr (16 b)\n- Options (variable)"
    },
    {
        "id": "ip_in_app",
        "label": "Socket Programming",
        "group": "pre_mid",
        "desc": "**TCP**: server `bind()` + `listen()` + `accept()`; client `connect()`\n每个 `accept()` 返回一个新 socket，原 listening socket 继续监听。\n**UDP**: 单个 socket `sendto(addr)` / `recvfrom()`。\n→ 这就是为什么 N 客户端时 TCP server 有 N+1 sockets，UDP 只有 1。"
    },
]

# New edges connecting the new nodes to existing graph
NEW_EDGES = [
    {"from": "sliding_window", "to": "tcp"},
    {"from": "sliding_window", "to": "stop_wait_u"},
    {"from": "rtt_estimation", "to": "tcp"},
    {"from": "tcp_retx", "to": "tcp"},
    {"from": "tcp_close", "to": "tcp"},
    {"from": "tcp_segment", "to": "tcp"},
    {"from": "rdt_evolution", "to": "rdt"},
    {"from": "web_cache", "to": "http"},
    {"from": "cond_get", "to": "web_cache"},
    {"from": "dht", "to": "p2p"},
    {"from": "bt_mechanisms", "to": "p2p"},
    {"from": "ip_in_app", "to": "socket"},
]


def main():
    d = json.loads(CONCEPTS.read_text())
    # Re-tag existing pre-mid nodes
    retagged = 0
    for n in d["nodes"]:
        if n["id"] in PRE_MID_IDS:
            n["group"] = "pre_mid"
            retagged += 1
    # Add new nodes (avoid dup)
    existing_ids = {n["id"] for n in d["nodes"]}
    for new in NEW_NODES:
        if new["id"] not in existing_ids:
            d["nodes"].append(new)
    # Add new edges (avoid dup)
    existing_edges = {(e["from"], e["to"]) for e in d["edges"]}
    for e in NEW_EDGES:
        if (e["from"], e["to"]) not in existing_edges:
            d["edges"].append(e)
    CONCEPTS.write_text(json.dumps(d, ensure_ascii=False, indent=2))
    print(f"retagged {retagged} nodes to pre_mid")
    print(f"total nodes now: {len(d['nodes'])}")
    print(f"total edges now: {len(d['edges'])}")


if __name__ == "__main__":
    main()
