#!/usr/bin/env python3
"""Patch explanations.json with detailed Chinese explanations for NYU Quiz 3 + Final."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPL = ROOT / "explanations.json"

# detailed entries keyed by "fileId:pageNum"
PATCH = {
    "nyu-Quiz_3_Solutions:1": {
        "title": "Q1 损坏/丢包检测 · Q2 Fast-retransmit 触发条件 ⭐",
        "summary": "Q1a checksum 检测损坏；Q1b timeout→cwnd=1+SS / 3-dup-ACK→cwnd/=2+CA。Q2 cwnd=3 第1包丢 → 凑不齐 3 个 dup-ACK，不能 FR；cwnd=4 第2包丢 → 能 FR。",
        "key_points": [
            "**Q1a 损坏检测**: TCP header 里的 16-bit `checksum`，header+data 加 + 取反；接收方再加应当 = 全 1",
            "**Q1b 丢包检测两条路**: `timeout`（RTO 到期） + `3 dup-ACK`",
            "Timeout → `cwnd = 1`，进入 **slow start**（保守，假设网络很差）",
            "3 dup-ACK → `cwnd /= 2`，进入 **congestion avoidance**（fast recovery，因为后续包还在到达）",
            "**Fast-retransmit 触发**: 必须凑齐 3 个 dup-ACK；每个 dup-ACK 由一个乱序包到达产生"
        ],
        "explanation": "### Q1a — TCP 怎么发现包被改了？\nTCP segment header 里有 16-bit **checksum** 字段。发送方把 header+data 当成 16-bit 字流相加（带进位回卷），取反填入。接收方再次相加，结果应当全 1。不等就丢这个 segment。\n\n### Q1b — 两种丢包检测 + 立刻怎么改 cwnd\n| 检测方式 | cwnd 立即变 | 之后进入 |\n|---|---|---|\n| **Timeout** | `cwnd ← 1 MSS` | Slow start（每 ACK +1） |\n| **3 dup-ACK** | `cwnd ← cwnd/2 + 3` | Fast recovery → CA（每 RTT +1） |\n\n**直觉**：timeout 说明网络很差（连 dup-ACK 都收不到）→ 保守降到 1。3-dup-ACK 说明后续包还到达 → 只半减。\n\n### Q2 — Fast-retransmit 啥时候触发不了？\nFR 需要 **3 个 dup-ACK**。dup-ACK 由乱序包到达产生（接收方说『我等的还是 N，但又收到一个』）。\n\n**Case 1**: cwnd=3，**第 1** 个 segment 丢。\n- 发送方发 seg1, seg2, seg3（窗口塞满）\n- seg1 丢；seg2 到 → dup-ACK#1；seg3 到 → dup-ACK#2\n- cwnd 用完了，没新 ACK 推进 → 不能再发 seg4\n- 只 2 个 dup-ACK，不够 3 个 → ❌ **不能 FR**，只能等 timeout\n\n**Case 2**: cwnd=4，**第 2** 个 segment 丢。\n- 发送方发 seg1, seg2, seg3, seg4\n- seg1 到 → ACK 2（正常）；ACK 推动窗口 → 可以再发 seg5\n- seg2 丢；seg3 到 → dup-ACK#1；seg4 到 → dup-ACK#2；seg5 到 → dup-ACK#3\n- ✅ **触发 FR**，重发 seg2\n\n### 这题核心\n要 FR：**丢包要靠前 + 窗口要够大**，让接收方至少能收到 3 个『丢包之后』的乱序包。否则只能 timeout。"
    },

    # ===== NYU Final 2024 Spring =====
    "nyu-final_24s_solutions1:1": {
        "title": "Final Q1 Dijkstra · Q2 DV · Q3 BGP ⭐",
        "summary": "Q1 Dijkstra 跑 A 到全网最短路。Q2 DV: min(2+10, 4+12, 3+8)=11；DV 单调不增；B 下一轮 ≤12。Q3 BGP policy-based 不取最短；hot-potato 把包甩给最近边界。",
        "key_points": [
            "**Q1**: Dijkstra 每轮挑 D 最小的点固定，松弛邻边。最后整理 routing table（目的→第一跳）",
            "**Q2a**: Bellman-Ford 方程 `D_s(d) = min_n [w(s,n) + D_n(d)]`。2+10=12 / 4+12=16 / `3+8=11` → **11**",
            "**Q2b 单调性**: DV 距离估计随迭代『不增』→ `D^{k-1}_A(x) ≥ D^k_A(x) = 10`，范围 **[10, ∞)**",
            "**Q2b 续**: B 下轮经 A 的代价 = 10+2 = 12 → `D^{k+1}_B(x) ≤ 12`",
            "**Q3a**: BGP 是 **policy-based**，不必走 AS 跳数最少的路（neighbor 可能拒绝转发）",
            "**Q3b**: Hot-potato = 跨 AS 包尽快交给 intra-AS 代价最小的边界 router；动机是每 AS 只关心自己 cost"
        ],
        "explanation": "### Q1 — Dijkstra (Link-State)\n```\nS = {A}; D[A]=0; D[v]=∞ for v≠A\nfor 邻居 n: D[n] = w(A,n)\n重复 N-1 次：\n    挑 u ∈ V\\S with min D[u]\n    S ← S ∪ {u}\n    for u 的邻居 v: D[v] = min(D[v], D[u]+w(u,v))\n```\n图里 A 直连 B(3), D(2)。第一轮选 D（最小 2），松弛 D 的邻居…依此类推。\n\n**Routing table 写法**：每个目的 v，沿最短路回溯，找到从 A 出发的第一跳邻居。\n\n### Q2a — DV 一步更新（Bellman-Ford）\n`D_s(d) = min_{n ∈ neighbors(s)} [w(s,n) + D_n(d)]`\n- 经 x：2 + 10 = 12\n- 经 y：4 + 12 = 16\n- 经 z：3 + 8 = **11** ← min\n\n**Answer: 11**，下一跳 z。\n\n### Q2b — DV 单调性约束\n稳定网络下 DV 距离估计 **只会变小或不变**（每轮看到的邻居估计本身也单调，所以汇总后也单调）。\n- `D^{k-1}_A(x) ≥ D^k_A(x) = 10` → 范围 **[10, ∞)**\n- 下一轮 B 通过 A 估算到 x 的代价 = `D^k_A(x) + w(A,B) = 10 + 2 = 12`\n- B 取 min → `D^{k+1}_B(x) ≤ 12`，范围 **(−∞, 12]**（实际 ≥ 0）\n\n### Q3a — BGP 不取最短\nBGP 是 **policy-based**（Gao-Rexford 规则）。AS 不一定 announce 学到的路由。\n例：A→B→C→D 4 跳；A→E→D 3 跳。但 E 把 D 当成竞争 AS → 不 announce D 给 A → A 只能走长路。**所以 BGP ≠ 最短 AS-path**。\n\n### Q3b — Hot Potato\n跨 AS 包，router 选 **intra-AS cost 最小** 的边界 router 交出去（『烫手山芋』丢出去）。\n动机：每 AS 只关心自己的 cost，不在乎包出去后走多远。\n→ 全局未必最优，但每 AS 自己便宜。"
    },

    "nyu-final_24s_solutions1:2": {
        "title": "Final Q4 — CRC 计算 + 错误检测 ⭐",
        "summary": "G=1011（4 bit），D=1101011。除尾追 000 后做模-2 除法得余数 R=110。发送 1101011 110。首尾翻转后做 CRC 检验，余数≠0 即能检测。",
        "key_points": [
            "**G 长度 r+1，余数 R 长度 r**：这里 G=1011 (4 bit) → R 3 bit",
            "**步骤**：D · 2^r ⊕ ... = (D 追 r 个 0) 模-2 除以 G，得余数 R",
            "**模-2 除法**: 没有进位的二进制除法，每步看最高位是 1 就用 G 异或",
            "**接收方**：把收到的 message 模-2 除 G，余数 = 0 → 正确；≠ 0 → 有错",
            "**CRC 能否检 burst error**: ≤ r 位连续翻转**一定**检得到；其它情况几乎都行（漏检概率 2^{-r}）"
        ],
        "explanation": "### Q4a — 求 CRC bits\n**Given**: D = `1101011`, G = `1011` (r = 3)\n\n**Step 1**: D 后追 3 个 0 → `1101011 000`\n\n**Step 2**: 用 G=1011 做模-2 除法（XOR 替代减）：\n```\n  1101011000  ÷ 1011\n\n  1101011000\n  1011\n  ----\n  0110011000\n   1011\n   ----\n   1010 1000     (移位继续)\n   1011\n   ----\n   0001 1000\n      1011\n      ----\n      0011 00\n         1011  ←  不够，先移位\n  ...\n```\n直接给最终余数 → **R = 110**。\n\n**Transmitted message** = D + R = `1101011 110` (10 bits)。\n\n### Q4b — 收方能否检测到首尾翻转？\n首位 1→0、末位 0→1：收到 `0101011 111`。\n收方做：`0101011111 ÷ 1011`，若余数 ≠ 0 → 检出错误。\n做模-2 除法：余数算出来非零（具体值不重要，关键是 ≠ 0）→ **能检测到**。\n\n### 为什么 CRC 这么强？\n- 任意单 bit 错都能检（因为 G 不能整除 2^i）\n- 任意 2 bit 错都能检（如果 G 有 3 个及以上 1）\n- 任意奇数 bit 错都能检（如果 G 含 `(x+1)` 因子，即 G 偶数个 1）\n- 长度 ≤ r 的 burst 错 **一定**检得到\n- 长度 > r 的 burst 漏检率 ≈ `2^{-r}` (这里 r=3 → 12.5%)\n\nCRC-32 (Ethernet) 用 r=32，漏检率 ≈ 2.3×10⁻¹⁰。"
    },

    "nyu-final_24s_solutions1:3": {
        "title": "Final Q5 交换机 self-learning · Q6 MAC + 隐藏终端 ⭐",
        "summary": "Q5: switch 收到帧 → 学习 src MAC ↔ port + TTL；查 dst 表，找不到则 flood。Q6a: 3 站撞，下次成功 = 一个选 0 两个选 1 = 3/8。Q6b: 隐藏终端 → CSMA/CA + RTS/CTS。",
        "key_points": [
            "**Switch 自学习**: 每收一帧 → 在表里登记 `(src MAC, 进来的 port, TTL=60s)`；TTL 过期自动删",
            "**转发决策**: 查表找 dst MAC → 命中就单播，未命中就 flood 到所有除入口外的 port",
            "**Q6a 撞车后**: 每站独立 1-persistent backoff，3 站各选 (0 或 1)。下一帧成功 = 恰一站选 0 两站选 1 = `C(3,1)·(1/2)^3 = 3/8`",
            "**隐藏终端**: A 和 B 都对 C 发，C 在中间，A↔B 听不到 → 在 C 处碰撞；CSMA 无效",
            "**解法**: 1) CSMA/CA（接收方显式 ACK）；2) **RTS/CTS** — 谁先发 RTS，C 选一个 grant CTS，CTS **广播** 给所有人，其它人静音"
        ],
        "explanation": "### Q5 — Switch self-learning 走一遍\nSwitch table 初始为空。\n\n**Frame 1: A → B'**（设 A 在 port-1, B' 在 port-3）\n- Learn: 记入 `(A, port-1, 60s)`\n- Lookup dst B'：表里没有 → **flood** 给除 port-1 外所有 port → B' 收到\n\n**Frame 2: C → A**（设 C 在 port-2）\n- Learn: 记入 `(C, port-2, 60s)`\n- Lookup dst A：命中 port-1 → **单播** A，不打扰其它 port\n\n**Frame 3: B → B'**（设 B 在 port-3）\n- Learn: 记入 `(B, port-3, 60s)`\n- Lookup dst B'：表里还是没有 → flood\n\n表最后：A↔port-1, C↔port-2, B↔port-3。\n\n### Q6a — 撞车后下一发成功概率\n碰撞后 Ethernet binary exponential backoff。题目里第 1 次碰撞 → 每站独立从 `{0, 1}` 等概率挑一个时隙等。\n\n下一发**成功** = **恰好 1 个站选 0**（其它两站选 1，等更久所以听到这站发就让）。\n概率 = `C(3,1) · (1/2)^1 · (1/2)^2 = 3 · 1/8 = 3/8`。\n\n### Q6b — 隐藏终端 + 解法\n**问题**: A、C、B 一线，C 在中间。A 对 C 发，B 也对 C 发。A↔B 距离 > 信号衰减半径 → 互相听不到。A 和 B 都以为信道空 → 同时发 → 在 C 处冲突。**纯 CSMA 失效**（CSMA 假设能听到所有发送者）。\n\n**解法 1: CSMA/CA + 显式 ACK**\nWiFi 接收方对每帧回 ACK；发送方没收到 ACK = 推断碰撞 → 退避重发。\n\n**解法 2: RTS / CTS**\n1. A 发 **RTS** → C\n2. B 也发 RTS → C\n3. C 选一个（比如 A），回 **CTS** → CTS **广播**（A 和 B 都听到）\n4. CTS 里写明信道占用时长 → B 设 NAV 计时器 → 静音\n5. A 发 data；C 回 ACK；ACK 后 B 醒来\n\nRTS/CTS 是『预约』模式，避免 hidden terminal 在长 data 帧上撞车。短包不用 RTS（开销不划算）。"
    },

    "nyu-final_24s_solutions1:4": {
        "title": "Final Q7 PKI · Q8 数字签名漏洞 · Q9 移动 IP · Q10 综合 ⭐",
        "summary": "Q7 公钥加密/签名/对称密钥分发三种方案。Q8 hash 可逆 → 攻击者找碰撞替换消息。Q9 direct routing 用 Y/indirect 用 X；各有 trade-off。Q10 入网→DHCP/UDP/broadcast→ARP first-hop→HTTPS→实际包 src/dst 地址。",
        "key_points": [
            "**Q7a 加密**: Alice 用 **Bob 公钥 K_B+** 加密；Bob 用自己私钥 K_B- 解",
            "**Q7b 签名**: Alice hash(M) 后用自己私钥 K_A- 加密 → 签名；附 M 一起发；只有 Alice 能产生此签名",
            "**Q7c 长消息加密**: PKI 慢 → 协商对称密钥 S（K_B+ 加密 S 给 Bob），后续用 S 对称加密",
            "**Q8 漏洞**: hash 可逆 → 攻击者找 M' 使 H(M')=H(M) → 替换 M 不改签名 → Bob 无感",
            "**Q9 direct**: C→Y（不绕路）；**indirect**: C→X（home agent 转）",
            "**Q10 接入流程**: DHCP(UDP)→广播 FF:FF...→DHCP reply 给 IP + first-hop router IP→ARP 拿 router MAC→HTTPS=HTTP/TLS/TCP→包里 src=自己 IP+MAC，dst=server IP + **router 的 MAC**（因为要跨子网）"
        ],
        "explanation": "### Q7a — 加密通信\nAlice 想给 Bob 发机密消息 m。\n- Alice: c = `Encrypt(K_B+, m)` （用 Bob 公钥）\n- Bob:   m = `Decrypt(K_B-, c)`  （只有 Bob 私钥能解）\n\n### Q7b — 长消息认证（签名）\nPKI 慢，整个 m 加密代价大。改用 **签名**：\n- Alice: 算 `h = H(m)`，签 `σ = Encrypt(K_A-, h)`，发 `(m, σ)`\n- Bob:   解 `H(m)' = Decrypt(K_A+, σ)`，自己再算 `H(m)`，对比是否相等\n\n**保证认证**: 只有 Alice 有 K_A-，所以只有 Alice 能产生有效 σ。\n**保证完整性**: m 被改，H(m) 变，对不上 σ。\n但 **不保证机密性**（m 是明文传的）。\n\n### Q7c — 长消息机密性\n用 PKI 协商 **对称密钥**：\n1. Alice 随机生成 S（AES 之类）\n2. Alice: `c0 = Encrypt(K_B+, S)`，发给 Bob\n3. Bob: `S = Decrypt(K_B-, c0)`\n4. 之后所有消息用 **AES(S)** 加密对称传\n\nTLS 1.2 之前的 RSA key exchange 就是这种。\n\n### Q8 — Hash 可逆 → 签名漏洞\n攻击者知道 Alice 公钥 K_A+ 和 (M, σ)。攻击者可以：\n1. 解出 `h = H(M) = Decrypt(K_A+, σ)`\n2. 用 hash 逆函数找一个 **M'** 使 `H(M') = H(M)`\n3. 把消息换成 `(M', σ)` 发给 Bob\n4. Bob 验签：`Decrypt(K_A+, σ) = H(M) = H(M')` ✅ → 通过！\n\nBob 完全察觉不到。所以 hash 必须 **抗 preimage**（已知 h 难找 m）。\n\n### Q9 — Mobile IP\nM 永久地址 X（home network），漫游地址 Y（visited）。C 想给 M 发包。\n\n| 路由方式 | C 该用哪个地址 | 优 | 劣 |\n|---|---|---|---|\n| **Direct** | Y | 直达，不绕路 | C 要追踪 M 当前位置，M 换网时连接断 |\n| **Indirect** | X | C 永远用 X，连接不断 | 三角路由（先到 home agent 再转），慢 |\n\n### Q10 — 上网全流程（综合题）\na) 拿 IP → **DHCP**，UDP 承载，目的 MAC = `FF:FF:FF:FF:FF:FF` (广播)\nb) 知道 first-hop router IP（DHCP reply 给的）→ **ARP** 广播请求，拿 router MAC\nc) 安全上网银 → **HTTP/TLS/TCP**（或 HTTP/3 = HTTP/QUIC/UDP）\nd) 发包给 server：\n   - **IP 层**: src = Alice IP, dst = server IP\n   - **以太网层**: src MAC = Alice 网卡, dst MAC = **first-hop router 的 MAC**\n   - 注意：MAC 是逐跳改的，IP 是端到端的。Server 不在同子网 → MAC 写下一跳的"
    },

    "nyu-final_24s_solutions1:5": {
        "title": "End of Exam — 祝暑假快乐",
        "summary": "考试结束页，无内容。",
        "explanation": "NYU 2024 Spring Final 试卷结尾页。"
    },

    "nyu-final_24s_solutions1:6": {
        "title": "草稿页（如果题目空间不够用）",
        "summary": "考卷的额外作答空间页。",
        "explanation": "试卷预留的额外作答空间页，没有题目内容。"
    },

    "nyu-final_24s_solutions1:7": {
        "title": "草稿页（如果题目空间不够用）",
        "summary": "考卷的额外作答空间页。",
        "explanation": "试卷预留的额外作答空间页，没有题目内容。"
    },
}

def main():
    data = json.loads(EXPL.read_text())
    for key, entry in PATCH.items():
        file_id, page_s = key.split(":")
        page = int(page_s) - 1
        arr = data.get(file_id, [])
        if page >= len(arr):
            print(f"WARN {key}: page out of range ({len(arr)} pages)", file=sys.stderr)
            continue
        # preserve topics tag if any, merge title/summary/key_points/explanation
        arr[page].update(entry)
    EXPL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Patched {len(PATCH)} entries into {EXPL}")

if __name__ == "__main__":
    main()
