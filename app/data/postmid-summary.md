# 4119 期中后总结 — 所有重要概念

> 涵盖 lec14, 16-23 + final-preview。lec22 和 23（无线）部分写得最详。

---

## 📘 lec14 · TCP 拥塞控制（CC）

### 1. AIMD — 唯一收敛公平的策略

**为什么 TCP 用 AIMD**：4 种组合（AIAD/AIMD/MIAD/MIMD）只有 AIMD 既收敛到效率最优又收敛到公平。
- **AI** (additive increase): 每 RTT cwnd += 1 MSS（沿 45° 走向效率线）
- **MD** (multiplicative decrease): 丢包时 cwnd /= 2（沿原点缩，比例不变但差距缩 0.5）
- 反复 AI + MD → 螺旋收敛到 fair line × efficiency line 交点

### 2. TCP 拥塞控制 FSM ⭐⭐⭐

**3 个状态**：Slow Start → CA (Congestion Avoidance) → Fast Recovery

| 状态 | cwnd 变化 |
|---|---|
| Slow Start | 每收 1 个 ACK，cwnd += 1 MSS（每 RTT 翻倍）|
| CA | 每 RTT，cwnd += 1 MSS（线性）|
| Fast Recovery | 每个 dup ACK，cwnd += MSS（维持 pipeline）|

**4 种转移**：
- Slow start → CA: `cwnd > ssthresh`
- CA → Fast Recovery: 收到 **3 个 dup ACK**（`ssthresh = cwnd/2`, `cwnd = ssthresh + 3`）
- Fast Recovery → CA: 收到 **new ACK**（`cwnd = ssthresh`）⚠️ **不是回 slow start！**
- 任何状态 → Slow Start: **timeout**（`ssthresh = cwnd/2`, `cwnd = 1`）

### 3. 两种丢包的不同反应
- **3 dup ACK**：网络还能传（n+1, n+2, n+3 到了，只丢了 n）→ 轻度，多用 fast retransmit + cwnd/2
- **Timeout**：可能整窗都丢 → 重度，cwnd 退回 1，重启 slow start

### 4. 必背公式：TCP 平均吞吐量
$$\text{Throughput} = \frac{3W}{4 \cdot RTT}$$
（W = 丢包前 cwnd 峰值。CA 下 cwnd 锯齿振荡在 W/2 ↔ W，平均 3W/4。）

### 5. 现代 CC 变种
- **CUBIC**（Linux 默认）：W(t) = C(t−K)³ + Wmax。激进追回 + 临近 Wmax 减速。
- **Delay-based** (Vegas)：用 RTT 上升而非丢包判拥塞。问题：跟 loss-based 共存会 starve。
- **BBR** (Google)：估计 BtlBw + RTprop，控制 inflight = BDP。不靠丢包。
- **ECN**：路由器在 IP ToS 用 2 bit 标记，receiver 经 ACK 回传，sender 减半但不丢包。**network-assisted CC** 的代表。

### 6. 易错点
- Fast Recovery 收到 new ACK 是回 **CA**，**不是 slow start**
- Timeout 才回 slow start
- ssthresh 总是设为丢包前 cwnd 的一半

---

## 📘 lec16 · Network 数据面 + Router 内部

### 1. 两个核心功能：Forwarding vs Routing

| | Forwarding（数据面）| Routing（控制面）|
|---|---|---|
| 时间尺度 | ns（硬件）| ms（软件）|
| 范围 | 单 router | 全网 |
| 干啥 | 用 FT 转发 | 算 FT |

类比：forwarding = 过交叉路口；routing = 行前规划。

### 2. Data Plane vs Control Plane（用户老问的）⭐
- **Data plane**：local，per-router，基于 header 字段决定 input→output port
- **Control plane**：network-wide logic，决定 datagram 怎么在 routers 间路由
- **2 种 CP 模式**：(1) 传统每 router 自跑路由算法 (2) SDN remote controller 集中算

### 3. Router 架构
- **Routing processor**（软件 ms）：control plane
- **Switching fabric**（硬件 ns）：data plane 核心
- **Input + Output ports**：数据进出

### 4. Longest Prefix Matching (LPM) ⭐⭐
查转发表时**选匹配前缀位数最多**的那条。
- 用 **TCAM**（ternary content-addressable memory）支持 0/1/* 三值匹配
- 一拍出结果，O(1) lookup with wildcards
- Cisco Catalyst ~1M entries

**做题套路**：列出每条 rule 的有效前缀位数，逐位对比 packet dst IP，选位数最多且匹配的。

### 5. HOL Blocking 和 VOQ
- **HOL (Head-of-Line) blocking**：队头 datagram 被堵 → 后面 datagram 即使去其他 output 也卡住
- **解药 VOQ** (Virtual Output Queue)：input port 为每个 output port 分开维护队列

### 6. 调度策略
- **FCFS / FIFO**：按到达顺序发
- **Priority**：按 header 字段分类，高优先级先发
- **Round Robin (RR)**：循环每 class 发一个
- **WFQ (Weighted Fair Queueing)**：class i 份额 = w_i / Σw_j，最小带宽保证

### 7. Network Neutrality（FCC 2015 三大原则）
- No blocking — 不能屏蔽合法内容
- No throttling — 不能限速合法流量
- No paid prioritization — 不能付费插队

---

## 📘 lec17 · IP / DHCP / NAT

### 1. IPv4 Datagram 字段（必填空）
- `ver(4) | hlen(4) | ToS(8) | total length(16)`
- `identifier(16) | flags(3) | frag offset(13)` — 分片
- `TTL(8) | upper protocol(8) | header checksum(16)`
- `src IP (32) | dst IP (32)`
- options + payload

**关键字段**：
- TTL：每跳 −1，到 0 丢包（防环）
- Protocol：6=TCP, 17=UDP, 1=ICMP
- Header checksum 只算 header

### 2. IP = interface 的（不是 host 的）
Router 有几个接口就有几个 IP。Host 有 WiFi + 有线就有 2 个 IP。

### 3. Subnet 概念
- **Subnet** = 一组不经 router 互通的接口
- IP = subnet 部分（高位）+ host 部分（低位）
- **识别 recipe**：断开每个 router 接口 → 剩下的孤岛 = 一个 subnet

### 4. CIDR — `a.b.c.d/x` ⭐⭐⭐ (final Q2)

**做题套路**：
1. `mask = x 个 1 + (32-x) 个 0`
2. `prefix = IP AND mask`（**二进制做 AND，别用十进制减**）
3. `host part = IP XOR prefix` 或 IP - prefix
4. `容量 = 2^(32-x)`

**Final Q2 例**：128.16.51.2 / 255.255.240.0
- mask /20（240 = 11110000）
- 第三段 51 (00110011) AND 240 (11110000) = 00110000 = 48
- → **prefix = 128.16.48.0/20，host = 0.0.3.2，容量 = 2¹² = 4096**

### 5. DHCP DORA（4 步全广播）
1. **Discover** (src 0.0.0.0:68 → dst 255.255.255.255:67)
2. **Offer**（server 提供候选 IP）
3. **Request**（client 选择）
4. **ACK**（server 确认）

DHCP **还返回 4 样**：IP + default gateway + DNS server + subnet mask + lease。

### 6. NAT
- LAN 内私有 IP（10/8, 172.16/12, 192.168/16），对外共享 1 个公网 IP
- 出包：(src IP, port) → (NAT IP, new port)，记 NAT 表
- 入包：查表反查 → (priv IP, port)
- 违反 end-to-end，阻碍 P2P / self-host server（需 STUN/TURN）

### 7. 路由聚合
ISP 拿 /20，切给 8 个组织各 /23。对外只 advertise /20 → 路由表大幅缩小。

---

## 📘 lec18 · IPv6 + 路由协议（Dijkstra + DV）

### 1. IPv6
- **128 位地址**（解决 IPv4 不够用）
- **40 byte 固定 header**（IPv4 是 20+ 变长）
- 去掉 checksum + fragmentation + options（用 next-header 链替代）
- 加 flow label
- 体现 **end-to-end principle**（复杂功能交给端）

### 2. IPv4 → IPv6 过渡：Tunneling
IPv6 packet 当 payload 塞进 IPv4 packet，穿过 v4-only 路由段。

### 3. 路由两种方法论（核心）⭐⭐⭐

| | Link State（LS）"大嘴" | Distance Vector（DV）"悄悄话" |
|---|---|---|
| 视角 | 全局 | 局部 |
| 告诉谁 | flood 全网 | 只跟邻居 |
| 算法 | Dijkstra | Bellman-Ford |
| 消息 | O(n²) | 邻居间 |
| 收敛 | 快（可能震荡）| 慢（可能 CTI）|
| 错误传染 | 本地化 | **全网传染（黑洞）** |
| 例 | OSPF, IS-IS | RIP（废）|

### 4. Dijkstra 算法（LS 用）⭐⭐
```
Init: N' = {u}; D(v) = c(u,v) or ∞
Loop:
  w = argmin_{v ∉ N'} D(v)
  add w to N'
  for v ∉ N' adjacent to w:
    D(v) = min(D(v), D(w) + c(w,v))
Until all in N'
```
**复杂度**: O(n²)，heap 实现 O(n log n)

### 5. Bellman-Ford 方程（DV 用）⭐⭐⭐ (final Q4)
$$D_x(y) = \min_{v \in N(x)} \{ c(x,v) + D_v(y) \}$$

直觉：『我到 y 最短』= '我先到某邻居 v 的代价' + 'v 估计到 y 的距离'，对所有邻居 v 取 min。

**做题套路**：
1. 写每节点的初始 DV（只填直连邻居，其他 ∞）
2. 邻居交换 DV → 用 BF 公式更新
3. 反复直到稳定
4. 收敛轮数 ≈ 最短路径树最大跳数 − 1

### 6. Count-to-Infinity（DV 的硬伤）
链路变贵时 stale DV 导致循环。**Poison reverse** 半解决：『我经 Y 到 X』就告诉 Y 自己到 X 是 ∞。**只破 2 节点环，不破 3+ 节点环**。

---

## 📘 lec19 · BGP + OSPF

### 1. 为什么要 AS
- Scale：十亿目的地存不下
- Admin autonomy：每个 ISP 想自己说了算
- → 把 routers 聚合到 AS（autonomous systems）

### 2. OSPF（intra-AS）
- **Open** + **link-state** + **Dijkstra**
- 每 router flood LSA（**直接走 IP，不用 TCP/UDP**，自己保证可靠）
- 支持多 metric（带宽、延迟）
- 消息认证
- **分层**：area + backbone (area 0)，ABR 在边界汇总

### 3. BGP（inter-AS）⭐⭐⭐
- **Path vector** 协议（不是 DV 也不是 LS）
- 跑在 **TCP** 上
- **eBGP**：跨 AS gateway 之间
- **iBGP**：同 AS 内传播 eBGP 学到的路径
- 4 类消息：OPEN / UPDATE / KEEPALIVE / NOTIFICATION

### 4. BGP advertisement 三要素
- **Prefix**：被 advertise 的目的子网
- **AS-PATH**：沿途经过的 AS 列表（**防环**：见到自己 AS 在路径里就 reject）
- **NEXT-HOP**：到下一 AS 的具体 router IP

### 5. BGP Policy（final Q3）⭐⭐⭐
- **Export policy**：决定 advertise 给谁
- **Import policy**：决定接不接路径
- 通过『不 advertise』实现不当 transit

**Final Q3 完全这个**：Columbia 跟 CERN 直连，跟 NYU peering。NYU 能否经 Columbia 到 CERN？答：不能。Columbia 配置 export policy **不向 NYU advertise** 到 CERN 的路径，NYU 学不到 → 不会借道。

### 6. Hot Potato Routing
对多条出口选 intra-AS 最便宜的 gateway 扔出去。经济动机：carry traffic 越久越费钱。

### 7. BGP 路由选择 4 步优先级
1. **Local pref**（policy）
2. **Shortest AS-PATH**
3. **Closest NEXT-HOP**（hot potato）
4. 其他 tie-breakers

### 8. Why Intra ≠ Inter（3 大原因）
- **Policy**：inter 需 admin policy；intra 单 admin
- **Scale**：分层路由表大幅缩小
- **Performance**：intra 注重性能；inter policy 第一

---

## 📘 lec20 · SDN + 错检（CRC）

### 1. Generalized Forwarding：Match + Action ⭐
- Router 不只看 dst IP，可以匹配 packet 任意 header 字段
- Action：drop / forward / modify / send to controller
- Priority 解决重叠规则
- Counters 监控

### 2. OpenFlow 11 个 match 字段
L2/L3/L4 全字段：ingress port, src/dst MAC, Ether Type, VLAN ID/Pri, IP src/dst/proto/ToS, TCP/UDP src/dst port。

### 3. OpenFlow 统一各种设备 ⭐
- **Router**: match longest dst IP → forward
- **Firewall**: match IP+port → permit/deny
- **Switch**: match dst MAC → forward
- **NAT**: match (IP, port) → rewrite

### 4. SDN 4 大设计原则
1. Generalized flow-based forwarding（OpenFlow）
2. Control / Data plane 分离
3. Control plane functions external to data-plane switches
4. Programmable control applications

### 5. CRC（错检最强）⭐⭐

**公式**：R = (D · 2^r) mod G

**Sender**：算 R，发 (D, R)。
**Receiver**：算 (D·2^r XOR R) mod G == 0？

**模 2 算术 = XOR**（无借位）。能检测所有 ≤ r 位的 burst error。

**手算例**：G=1001, D=101011, r=3
1. D·2³ = 101011000
2. 用 G 做 mod-2 长除法
3. 余数 R = 110
4. 发 `101011 110`

### 6. Parity vs Checksum vs CRC
- **Parity 1-bit**：只检奇数错。**2D parity** 能检+纠单 bit 错。
- **Checksum**：16-bit 字累加（无 carry）。TCP/UDP/IP 用。**比 CRC 弱**。
- **CRC**：检错最强。Ethernet frame 末尾 4 byte CRC。

---

## 📘 lec21 · Data Link / ALOHA / CSMA/CD / Ethernet

### 1. Data Link Layer 4 大服务
- Framing
- Error detection/correction
- MAC (Medium Access Control)
- Reliable delivery（有线常省，无线必备）

### 2. MAC 三大类
| 类 | 例 | 优 | 缺 |
|---|---|---|---|
| **Channel partition** | TDMA/FDMA/CDMA | 无碰撞 | 静态分配浪费 |
| **Taking turns** | polling, token | 无碰撞 | overhead + 单点故障 |
| **Random access** | ALOHA, CSMA/CD, CSMA/CA | 突发流量高效 | 可能碰撞 |

### 3. Slotted ALOHA 1/e 推导 ⭐⭐
- N 节点各以概率 p 发
- 单节点成功概率 P_i = p · (1-p)^(N-1)
- 总成功概率 S = N · p · (1-p)^(N-1)
- 对 p 求导：**p\* = 1/N**
- 代回：**S\_max → 1/e ≈ 0.368**（N → ∞ 时）

**Pure ALOHA**（不对齐 slot）：碰撞窗口翻倍 → 1/(2e) ≈ 0.184。

### 4. CSMA — "Listen before transmit"
**仍可能碰撞**：propagation delay 期间多节点都觉得 idle。

### 5. CSMA/CD（有线）— Min Frame Size 推导 ⭐
- A 发包，信号到 B 要 d/c 秒
- B 在 d-ε 时也以为 idle 开始发 → 碰撞
- 碰撞 echo 回到 A 需要 d/c
- → **A 检测碰撞最坏 2d**
- → frame 持续时间 ≥ 2d → **min frame size ≥ 2d·R**

**10 Mbps Ethernet 数字**：
- max 2d = 51.2 μs（标准规定）
- min frame = 51.2 × 10 = **512 bit = 64 byte**
- max cable = **100 m**

### 6. Ethernet Frame 格式
| 字段 | 长度 |
|---|---|
| Preamble + SFD | 8 byte |
| Dst MAC | 6 byte |
| Src MAC | 6 byte |
| Type | 2 byte (0x0800=IP, 0x0806=ARP) |
| Payload | 46-1500 byte |
| CRC | 4 byte |

**Min frame 64 byte，max 1518 byte**。

### 7. MAC Address vs IP Address
| | MAC | IP |
|---|---|---|
| 层 | L2 | L3 |
| 长度 | 6 B | 4 B (v4) |
| 分配 | 厂商烧网卡 | DHCP / 配置 |
| 结构 | 扁平 | 层级 |
| 范围 | 单 LAN | 全网 |
| 改变 | 跟着网卡走 | 跟着位置变 |

类比：MAC = 身份证号；IP = 家庭住址。

### 8. 现代 Ethernet 是 switched
- 早期：shared bus + CSMA/CD + binary backoff
- 现代：每对 host-switch 是 dedicated 全双工链路
- **没有碰撞**，**没有 CSMA/CD**
- 速度 10M/100M/1G/10G/40G/100G

---

## 📘 lec22 · ARP + Switch + VLAN + 无线物理入门

### 1. ARP — 把 IP 翻译成 MAC ⭐⭐

**为什么需要**：网卡只懂 MAC（L2），发包必须先知道目的 MAC。但应用层只有 IP。

**流程**：
1. Host A 想发包给 IP 1.2.3.6
2. 查 ARP 表，没命中
3. **广播** ARP request：『Who has 1.2.3.6?』（dst MAC = FF:FF:FF:FF:FF:FF）
4. 只有 IP=1.2.3.6 的 host B **unicast 回应**：『My MAC is 0C-C4-...』
5. A 缓存 (IP, MAC, TTL)，发包

**ARP table**：(IP, MAC, TTL) 三元组。Soft state，TTL 到期自动清。

### 2. ARP 跨子网 ⭐⭐⭐（必考陷阱）

**关键陷阱**：当目的 IP **不在本子网** 时，host 用 ARP 解析的是 **first-hop router（default gateway）的 MAC**，**不是终点 IP 的 MAC**。

**为什么**：ARP 是 L2 广播，只在同一 LAN 内有效。跨网必须经 router。

**Frame 沿路 MAC 变化（IP 不变）**：
```
A → R → R' → B
段 A→R: src MAC=A, dst MAC=R-LAN, src IP=A, dst IP=B
段 R→R': src MAC=R-WAN, dst MAC=R'-LAN, src IP=A, dst IP=B（不变）
段 R'→B: src MAC=R'-LAN, dst MAC=B, src IP=A, dst IP=B
```

**IP 端到端不变，MAC 每跳变**。

**怎么判断目的是否本子网**：用 netmask（DHCP 给的）做 AND 比较。

### 3. Switch（L2 设备）

**自学习**（plug-and-play）：
- 看 incoming frame 的 src MAC + 来自哪个 port → 记 (src MAC, port, TTL)
- 发包时：
  - dst MAC 在表 → **单口发**
  - dst MAC 不在表 → **flood**（除入口外所有 port）

**多对话并发**：
- 每条 host-switch link 独立 collision domain
- 全双工
- 多对 host 同时通信不冲突
- 只有同目的 host 会在 switch 内 buffer 排队

### 4. VLAN
- 一台物理 switch 切成多个虚拟 LAN
- 按 port 划分（最常用）或 MAC 划分
- **隔离广播域 + 安全 + 灵活**
- 跨 VLAN **必须经 router**（不是 switch）

### 5. Router vs Switch ⭐
| | Router | Switch |
|---|---|---|
| 层 | L3 | L2 |
| 看什么 | dst IP | dst MAC |
| 表来源 | 路由算法 | 自学习 |
| 范围 | 跨网 | 单 LAN |
| TTL | 减 1 | 不动 |

**一句话**：跨子网用 router，同 LAN 用 switch。

### 6. 无线网络 3 层范围
- **WPAN**（Personal Area）：Bluetooth, Zigbee, RFID — 米级
- **WLAN**（Local Area）：WiFi 802.11 — 数十米
- **WWAN**（Wide Area）：Cellular, WiMAX — 公里

### 7. 自由空间路径损耗（pathloss）⭐⭐

$$L = \left(\frac{4\pi d}{\lambda}\right)^2 = \left(\frac{4\pi d f}{c}\right)^2$$

- **d** = 距离, **λ** = 波长, **f** = 频率, **c** = 光速
- **频率越高（波长越短）loss 越大**
- 所以 5GHz 比 2.4GHz 衰得快、穿墙差

**实际环境**：PL(d) = PL(d₀) + 10α · log(d/d₀) + X
- α = pathloss exponent
- 自由空间 α=2，城市 α=2.7-3.5，室内阻挡 α=4-6

---

## 📘 lec23 · 无线 MAC（重点章节）

### 1. 三种传播现象（必背）⭐

| 现象 | 物体尺寸条件 | 例 |
|---|---|---|
| **Reflection 反射** | 物体 ≫ λ | 墙、地面、建筑 |
| **Diffraction 衍射** | 锐利边缘 | 墙角、书架边（绕进阴影区）|
| **Scattering 散射** | 物体 < λ | 树叶、灯柱、路标 |

记忆抓手：判断物体尺寸跟波长 λ 比。

**WiFi 波长**：
- 2.4 GHz → λ ≈ 12.5 cm
- 5 GHz → λ ≈ 6 cm

### 2. 多径衰落（Multipath Fading）

**为什么会有**：直达路径 + 多条反射路径同时到达 receiver。路径长度不同 → 时间差 → 相位差 → 干涉。

**两种 fading**：
- **Large-scale fading**：随距离平均衰减（pathloss + shadowing）
- **Small-scale fading**：小范围内（一两个 λ = 10-20 cm）剧烈跳动（multipath 干涉）

**Mobility 主要导致 small-scale**（接收端移动几 cm 就可能从满格变 1 格）。

### 3. Coherence Time + ISI

**Coherence time (Tc)**：信道脉冲响应保持不变的最大时间。

**ISI (Inter-Symbol Interference)**：一个 symbol 经多径到达 receiver 时有多个延迟拷贝（拖尾）。如果下一个 symbol 来得太早，上个的拖尾还没散 → ISI。

**Symbol period 必须 ≤ Tc** 才能正确解码。

### 4. SNR / SINR ⭐⭐

$$\text{SNR}_{\text{dB}} = 10 \log_{10}(S/N)$$
$$\text{SINR}_{\text{dB}} = 10 \log_{10}(S/(N+I))$$

- **SNR**：纯热噪声背景
- **SINR**：加上其他发射机干扰
- **高 SNR → 低 BER → 可用高 modulation/code rate**

**dB 计算 trick**：dB 减法 = 比值。信号 -50 dBm，噪声 -90 dBm → SNR = (-50)-(-90) = **40 dB**（信号比噪声大 100 倍）。

### 5. Wireless ≠ Wired — 两大根本差异 ⭐⭐

1. **Time-varying, unpredictable channel**：mobility + 环境物体动 + multipath
2. **Broadcast → interference**：邻居发射互相干扰

**这两条驱动整个 wireless MAC 设计**。

跟有线对比：
| | 有线 | 无线 |
|---|---|---|
| 信道 | 稳定 | 时变 |
| 介质 | 独占 | 广播 |
| BER | 10⁻¹² | 10⁻³ |
| Collision detect | 容易（边发边听）| **不可能**（耳朵被淹）|

### 6. 三种 Range（设置 Hidden/Exposed 概念）

每个无线节点有 3 个圆：
- **Transmission range**（能解码）
- **Interference range**（能干扰但解不了）
- **Carrier sensing range**（能检测到能量）

**Layer**：Transmission < Interference < Carrier sensing。

### 7. CSMA — sender-driven 的根本问题

**CSMA**：传输前先 carrier sense。信道闲 → 发；忙 → 等。

**Insight（核心）**：
- CSMA 是 **sender-driven**（sender 听自己周围）
- **但干扰发生在 receiver 端**
- Sender 听到 idle 不等于 receiver 那边 idle

→ **这就是 hidden terminal 的根源**

### 8. Hidden Terminal（必考）⭐⭐⭐ (final Q5)

**判定**：节点 X 是 A → B 通信的 hidden terminal ⟺
- X 在 sender A 的 sensing range **外**（X 听不到 A）
- X 在 receiver B 的干扰范围 **内**（X 能干扰 B）

**症状**：
- A 自己以为发得好好的
- X 也觉得信道 idle 也发
- A 和 X 的信号在 B 处碰撞
- B 收不到 A
- A 等不到 ACK 才知道丢

**解药**：RTS/CTS。Receiver B 发 CTS → B 周围（包括 X）听到 CTS → 在 NAV 时长内静默。

### 9. Exposed Terminal（必考）⭐⭐⭐ (final Q5)

**判定**：节点 X 是 exposed terminal ⟺
- X 在 sender A 的范围 **内**（听到 A）
- X 自己的目标 receiver 在 A 的范围 **外**（不会被 A 干扰）

**症状**：
- X 想发给 D，D 在 A 范围外，A 干扰不到 D
- 但 X 听到 A 在发，CSMA 让 X 退让
- → X **本可并发但被抑制，浪费**

**解药**：CSMA/CA 没完美解。RTS/CTS 也只解 hidden。

### 10. 对比记忆 Hidden vs Exposed

|  | Hidden | Exposed |
|---|---|---|
| X 跟 sender A | 在范围**外** | 在范围**内** |
| X 跟 receiver | 在 B 干扰范围**内** | X 自己的目标在 A 范围**外** |
| 症状 | 该停没停 → 碰撞 | 该发没发 → 浪费 |
| 解药 | RTS/CTS | 无 |

**记忆抓手**：
- **隐藏 = 隐身看不见，该停没停 → 撞**
- **暴露 = 暴露在视野，该发不敢发 → 亏**

### 11. RTS / CTS / NAV

**MACA (Karn'90) 协议**：
1. Sender → **RTS (Request-to-Send)** → Receiver
2. Receiver → **CTS (Clear-to-Send)** → Sender（含 NAV 时长）
3. 听到 RTS 的人静默 t_CTS（让 sender 能收 CTS）
4. 听到 CTS 的人静默 NAV 时长（保护数据传输）

**NAV (Network Allocation Vector)**：RTS/CTS 包内 Duration 字段告诉别人『接下来要占多久』。其他节点维护本地 NAV 倒数。NAV > 0 时即使物理检测 idle 也算忙 → **虚拟载波检测**。

### 12. CSMA/CA 完整流程 ⭐⭐

1. **载波感知**（物理 + 虚拟 NAV）
2. 信道闲 → 等 **DIFS**（~50 μs）→ 仍闲 → 发
3. 回复（CTS, ACK）等 **SIFS**（~10 μs，更短，优先）
4. 信道忙 → 等 idle 后 DIFS → 启动 **random backoff**
5. Backoff 在 [0, CW] 内随机选；信道闲就减 1，忙就 freeze
6. Backoff = 0 → 发 RTS
7. 发完没 CTS → **CW × 2**（binary exp backoff）
8. 成功一次完整 transmission → CW reset 为 CWmin

**为什么 SIFS < DIFS**：让回复包优先于新一轮竞争，保证一次对话不被打断。

**为什么无线不能 CD**：发射时自己天线发的功率比接收强 10⁹ 倍，听不到别人。

### 13. Binary Exponential Backoff
- 失败 → CW = min(2·CW, CWmax)
- 成功 → CW = CWmin
- CWmin = 31 (802.11b) / 15 (802.11g)

**问题**：CW 重置太激进 → 振荡 + 不公平。

**MACAW 改进**：成功 → CW −1（线性减），类比 TCP AIMD。

### 14. 802.11 标准家族
| 标准 | 频段 | 速率 | 关键 |
|---|---|---|---|
| b (1999) | 2.4G | 11 Mbps | DSSS |
| a (1999) | 5G | 54 Mbps | OFDM |
| g (2003) | 2.4G | 54 Mbps | OFDM |
| n (2009) | 2.4/5G | 600 Mbps | **MIMO** 多天线 |
| ac WiFi 5 (2013) | 5G | >1 Gbps | MIMO + 大 BW |
| ax WiFi 6 (2020) | 2.4/5G | 14 Gbps | 密集场景优化 |

**全部用 CSMA/CA**。

### 15. WiFi Channels — 1/6/11 不重叠
- 802.11b 美国 11 个 channels
- 每个 channel 22 MHz 宽
- **只有 channel 1, 6, 11 三个不重叠**（间隔 25 MHz）
- AP 部署常用 1/6/11 交错避免互相干扰

### 16. 802.11 LAN 架构
- **BSS** (Basic Service Set) = AP + 关联的 hosts（infrastructure mode）
- **Ad-hoc mode**：hosts 直连，无 AP
- 进入 BSS 流程：Scan → Auth → Associate → Data

---

## 🎯 Final Preview 5 道例题 — 综合解题思路

### Q1: TCP 丢包 ≠ 拥塞？
- 涉及：lec14 TCP CC + lec12 TCP checksum + lec23 无线 BER
- 答：bit error → checksum 失败 → receiver 不发 ACK → sender 误判拥塞
- 解药：ECN

### Q2: CIDR / DHCP 计算
- 涉及：lec17 CIDR + DHCP
- 128.16.51.2 / 255.255.240.0
- 答：prefix = 128.16.48.0/20, host = 0.0.3.2, 容量 = 2¹² = 4096

### Q3: BGP Policy
- 涉及：lec19 BGP export policy
- 答：Columbia 通过 BGP export policy 不向 NYU advertise 到 CERN 的路径

### Q4: Distance Vector 表
- 涉及：lec18 DV + Bellman-Ford
- 写每节点初始 DV → 交换 → BF 公式更新 → 收敛

### Q5: Hidden / Exposed Terminal
- 涉及：lec23 wireless MAC
- 判定：sender 范围外 + receiver 范围内 = hidden
- 判定：sender 范围内 + 自己目标范围外 = exposed

---

## 🔥 考前必背清单（10 件）

1. **TCP CC FSM 转移**：fast recovery + new ACK → CA（不是 slow start！）
2. **AIMD 公平性几何论证**：AI 走 45° + MD 沿原点缩
3. **LPM**：选最长前缀，必练这种题
4. **CIDR 计算**：二进制 AND，别用十进制
5. **Dijkstra 伪代码**：N' = {u}, 找 min D，relax 邻居
6. **Bellman-Ford 方程**：D_x(y) = min_v {c(x,v) + D_v(y)}
7. **BGP 路由选择 4 步**：local pref → AS-PATH → hot potato → others
8. **CRC 手算**：D·2^r mod G = R（模 2 = XOR）
9. **ALOHA 1/e 推导**：S = Np(1-p)^(N-1)，p* = 1/N
10. **Hidden/Exposed 判定**：sender 外+receiver 内 = hidden；sender 内+目标外 = exposed

---

## 🔧 必背公式列表

| 公式 | 出处 |
|---|---|
| End-to-end = Σ(L/R + d/v) + queue | lec3 |
| BDP = R · RTT | lec3 |
| U_stop-wait = T_trans / (T_trans + 2·T_prop) | lec11 |
| TCP throughput = 3W/(4·RTT) | lec14 |
| CS time = max(NF/U_s, F/d_min) | lec9 |
| P2P time = max(F/U_s, F/d_min, NF/(U_s+ΣU_i)) | lec9 |
| Slotted ALOHA S_max → 1/e at p=1/N | lec21 |
| CSMA/CD min frame: L ≥ 2d·R | lec21 |
| Pathloss L = (4πdf/c)² | lec22 |
| SNR_dB = 10·log(S/N) | lec23 |
| D_x(y) = min_v {c(x,v) + D_v(y)} | lec18 |
| CRC: R = D·2^r mod G | lec20 |
| WFQ class i 份额 = w_i / Σw_j | lec16 |

加油，明天考好 💪
