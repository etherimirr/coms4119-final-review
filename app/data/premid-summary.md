# COMS 4119 Pre-Midterm Summary (lec1–13)

Concise per-lecture digest of what was actually taught (not the broader Internet).
Mirror of `postmid-summary.md`.

---

## 📘 lec1 · Intro

Scale of the Internet, scope of the course. **No exam content.**

---

## 📘 lec2 · Network Basics 1

### 1. What is the Internet
- Network of networks (~100K AS)
- Edge: hosts / access network / physical media
- Core: routers + links

### 2. What is a protocol
Set of rules: message format + order + actions on send/receive.

### 3. Packet vs Circuit switching
- **Circuit**: establish → reserve resources → send (no dst addr) → tear down. Multiplex via TDM or FDM.
- **Packet**: split into packets w/ header → independent forward → store-and-forward → dst reassembles. Best-effort.
- **Circuit ✅**: guaranteed BW, simple, low overhead.
- **Circuit ❌**: wastes BW on bursty traffic, blocked connections, setup delay, per-connection state.
- Internet picks packet: good for bursty, simple, robust.

### 4. TDM vs FDM
- TDM = time slots per circuit
- FDM = frequency bands per circuit

---

## 📘 lec3 · Performance

### 1. 4 sources of delay
1. **Transmission** = L/R (size / bandwidth)
2. **Propagation** = d/v (light ≈ 3·10⁸ m/s vacuum, 2·10⁸ in copper; sound 1.5 km/s in water)
3. **Queuing** = depends on load
4. **Processing** = at each router (small)

### 2. Throughput
- Bottleneck rule: `throughput = min(per-link rate) = max(L/R)`
- Not propagation!

### 3. Store-and-forward
- Pipelined N packets: `1st full path + (N−1) · bottleneck L/R`
- Propagation paid only once (1st packet)

---

## 📘 lec4 · Layering, Encapsulation, BDP

### 1. 5 layers (PDU per layer)
- **Application** — Message
- **Transport** — Segment (TCP & UDP both)
- **Network** — (IP) Datagram
- **Data Link** — Frame
- **Physical** — Bits

### 2. Encapsulation
Each layer wraps upper-layer PDU with its own header.
Demux upward: Ethertype → IP protocol → port → app.

### 3. End-to-End Principle
Complex functions at endpoints, not in network core (e.g., reliability via TCP at hosts).

### 4. RTT + BDP
- **BDP = R · RTT** (bits in pipe)
- Window must ≥ BDP to keep pipe full

### 5. Stop-and-Wait Utilization
`U = T_trans / (T_trans + 2·T_prop)`  · Small L or large RTT → U collapses → need sliding window

### 6. Sliding Window
Sender keeps window `[base, base+N)`; ACK slides base. Stop-and-wait = window of 1.

---

## 📘 lec5 · Web / HTTP

### 1. HTTP non-persistent vs persistent
- **Non-persistent (HTTP/1.0)**: new TCP per object. Each object: 2 RTT (TCP setup + GET)
- **Persistent (HTTP/1.1)**: reuse TCP. Pipelining: send next req before prev response

### 2. HTTP RTT Counting
- Draw dependency tree: base → inline siblings → CSS-referenced → JS-triggered
- Non-persistent: each obj = 2 RTT
- Persistent + pipelined: base 2 RTT; same-layer inline +1 RTT; each nesting +1 RTT
- Persistent no pipeline: each obj 1 RTT sequentially

### 3. HTTP Cookies
- HTTP is stateless. Cookies add per-user server-side state.
- 4 parts: Set-Cookie response header → cookie file on client → Cookie request header → server DB

### 4. Web Cache (proxy)
- Caches responses; cuts RTT + outbound BW
- **Conditional GET**: `If-Modified-Since` → server returns 304 (no body) if unchanged

### 5. HTTP/2 + HTTP/3
- HTTP/1.1 HOL: small obj blocked behind large
- HTTP/2: split into frames over single TCP; client priority; push
- HTTP/3: over UDP (QUIC); per-object recovery; TLS default

---

## 📘 lec6 · Video / DASH

### 1. Video basics
- CBR (constant bit rate) vs VBR
- Encoding: spatial + temporal redundancy

### 2. DASH (Dynamic Adaptive Streaming over HTTP)
- Server holds multiple bitrates of each chunk
- Client measures BW + picks next chunk bitrate
- HTTP-based → any CDN works

### 3. CDN
- Push content close to users
- HTTP requests redirected to nearest cache

---

## 📘 lec7 · Sockets

### 1. UDP socket
- **1 socket** at server, no connection
- Server distinguishes clients by `(src IP, src port)` in incoming datagram

### 2. TCP socket
- **1 welcome socket** at server
- Each `accept()` returns a **new socket** for that client
- N clients → 1 + N sockets at server

---

## 📘 lec8 · DNS

### 1. Hierarchy
local resolver → root → TLD (.com, .edu) → authoritative

### 2. Recursive vs iterative
- **Recursive**: "resolve for me", server chases the chain (used between client ↔ local resolver)
- **Iterative**: "tell me next hop", caller chases (used between resolvers ↔ root/TLD)

### 3. Resource Records (RR)
- **A** — IPv4
- **AAAA** — IPv6
- **NS** — name server for domain
- **MX** — mail server
- **CNAME** — alias

### 4. Transport
UDP port 53 (short queries); falls back to TCP for large responses.

---

## 📘 lec9 · P2P / BitTorrent

### 1. P2P architecture
- No always-on server; peers serve each other
- Self-scaling: N peers join → upload capacity also grows N×

### 2. P2P file distribution time
`T_P2P = max(F/U_s, F/d_min, NF/(U_s + ΣU_i))`
vs CS: `T_CS = max(NF/U_s, F/d_min)`
- CS time grows linearly with N (server bottleneck)
- P2P time grows slowly with N (collective upload also grows)

### 3. BitTorrent mechanisms
- **Rarest first**: prioritize chunks scarce in the swarm
- **Tit-for-tat**: upload to those who upload to you
- **Optimistic unchoke**: every ~30 s gift bandwidth to a new peer

### 4. DHT (Distributed Hash Table)
Replaces central tracker; consistent hashing maps key → responsible node.

---

## 📘 lec10 · Transport intro

### 1. Mux / Demux
- Transport layer adds (src port, dst port)
- Demux: incoming segment → socket via (src IP, src port, dst IP, dst port) for TCP; via (dst IP, dst port) for UDP

### 2. UDP
- Header: 8 B (src port, dst port, length, checksum)
- Connectionless, no reliability, no order, no flow/cong control

### 3. TCP segment format
- src/dst port (16 b each)
- Seq # = first byte of data (32 b)
- ACK # = next expected byte (32 b)
- HLEN, flags: SYN / FIN / ACK / RST / PSH / URG / CWR / ECE
- rwnd (16 b) — flow control
- Checksum (16 b), urgent pointer

### 4. TCP 3-way handshake
1. Client → server: SYN, seq=x
2. Server → client: SYN-ACK, seq=y, ack=x+1
3. Client → server: ACK, seq=x+1, ack=y+1

### 5. TCP 4-way close
FIN / ACK each direction. TIME_WAIT 2·MSL avoids stray packets affecting next connection.

---

## 📘 lec11 · Reliability (RDT)

### 1. 5 problems RDT must handle
1. Bit errors → checksum
2. Duplicate packets → seq #
3. Packet losses → timer + retransmit
4. Packet delay → in-order delivery
5. Out-of-order arrival → seq # reorder

### 2. RDT 1.0 → 3.0
- 1.0: perfect channel (useless)
- 2.0: + ACK/NAK + checksum (bit errors)
- 2.1: + seq # (ACK corruption)
- 2.2: NAK-free (use ACK + last good seq)
- 3.0: + timer (packet loss) → stop-and-wait

### 3. Pipelined RDT: GBN vs SR
| | GBN | SR |
|---|---|---|
| ACK | cumulative | per-packet |
| Loss | resend window | resend just lost |
| Data loss heavy | bad | **good** |
| ACK loss heavy | **good** | bad (timeout) |
| Buffer at rcvr | none | required |

Rule: data-loss heavy → SR; ACK-loss heavy → GBN. Always write the reason.
SR window must be ≤ N/2 (seq space).

---

## 📘 lec12 · TCP

### 1. TCP Reliable Mechanisms
- **Timeout retransmit**: `TimeoutInterval = EstRTT + 4·DevRTT`
- `EstRTT = (1−α)·EstRTT + α·SampleRTT`, α = 0.125
- `DevRTT = (1−β)·DevRTT + β·|SampleRTT − EstRTT|`, β = 0.25
- **Fast retransmit**: 3 dup ACKs → immediate resend
- Exponential backoff after timeout (RTO doubles)

### 2. TCP Flow Control
- Receiver advertises `rwnd` in every ACK
- Sender inflight ≤ min(cwnd, rwnd)
- SR receive buffer holds out-of-order packets; if buffer can't release → upstream packets dropped

### 3. TCP cwnd basics
- `LastByteSent − LastByteAcked < cwnd`
- `rate ≈ cwnd / RTT`

---

## 📘 lec13 · Congestion Control Intro

### 1. End-end vs Network-assisted
- **End-end**: infer congestion from observed loss / delay (TCP default)
- **Network-assisted**: router signals host (TCP ECN, ATM, DECbit)

### 2. AIMD
Additive Increase, Multiplicative Decrease (TCP's strategy):
- +a moves both up 45° (efficiency line)
- ×b scales toward origin (preserves ratio)
- Spiral converges to `x1 = x2 ∩ x1 + x2 = 1`
- **Only AIMD** achieves both fairness and efficiency

### 3. AIAD / MIAD / MIMD
- AIAD: doesn't converge to fairness (gap stays)
- MIMD: doesn't converge (ratio stays)
- MIAD: unstable
- AIMD wins

### 4. Slow Start → CA transition
- Start: cwnd = 1, exponential growth (×2 per RTT)
- `cwnd ≥ ssthresh` → Congestion Avoidance, linear growth (+1 MSS / RTT)

---

## 🎯 Key formulas (memorize)

| Formula | Where |
|---|---|
| End-to-end (1 pkt) = Σ(L/R + d/v) + queue | lec3 |
| Pipelined N pkts = 1st full path + (N−1)·bottleneck L/R | lec3 |
| BDP = R · RTT | lec4 |
| U_stop-and-wait = T_trans / (T_trans + 2·T_prop) | lec4 |
| HTTP non-persistent: 2 RTT/obj | lec5 |
| CS time = max(NF/U_s, F/d_min) | lec9 |
| P2P time = max(F/U_s, F/d_min, NF/(U_s + ΣU_i)) | lec9 |
| EstRTT = (1−α)·EstRTT + α·SampleRTT, α = 0.125 | lec12 |
| TimeoutInterval = EstRTT + 4·DevRTT | lec12 |
| TCP CC: timeout → cwnd=1+SS; 3 dup ACK → cwnd/=2+CA | lec13 |
