#!/usr/bin/env python3
"""Full per-page rewrite for lec23 (Wireless MAC + propagation modes + CSMA/CA + 802.11, 39 pages)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec23:1": {
  "title": "Reflection — 三种传播现象之一",
  "summary": "**Reflection (反射)**: 电磁波撞到比波长大很多的表面（地面、墙、车体）会反射。波长 λ = c/f。\n\nWiFi 2.4 GHz: λ ≈ 12 cm; 5 GHz: λ ≈ 6 cm。墙、地面、家具都算『大』。\n\n**例子**: '用啤酒罐增强 WiFi 信号' — 金属罐反射 + 几何聚焦像抛物面天线。",
  "key_points": [
    "Reflection: 波撞大表面 (比 λ 大)",
    "λ = c/f；WiFi 2.4G λ≈12cm, 5G λ≈6cm",
    "墙、地面、家具都 reflect",
    "反射能量基本保留，方向改变",
    "→ 引出 multipath（多径）"
  ],
  "explanation": "**判定『大』的尺度** = 波长 λ：\n- 频率 f 越高，λ 越小：c = λf，c = 3×10⁸ m/s\n- 2.4 GHz: λ = 3×10⁸ / 2.4×10⁹ ≈ **0.125 m = 12.5 cm**\n- 5 GHz: λ ≈ **6 cm**\n- 900 MHz: λ ≈ **33 cm**\n\n**反射后果**：直达路径 + 反射路径同时到达接收端 → **multipath**（多径），后面 fading、ISI、coherence time 的根源。\n\n**易记的反例**：lec23 用 'beer can boost WiFi' 的梗 — 金属罐切开放在路由器后面，反射 + 几何聚焦增强信号。"
},

"lec23:2": {
  "title": "Diffraction (衍射 / 阴影绕射)",
  "summary": "**Diffraction**: 波遇到**锐利不规则边缘**会『绕过去』，使阴影区也能收到信号（虽然弱）。例：墙后能收到 WiFi 就是衍射。",
  "key_points": [
    "Object 有锐利边 → 衍射",
    "即使没 LOS（line of sight）也能通信",
    "阴影区信号比直达弱，但不为零",
    "WiFi 拐角能传靠的就是这个"
  ],
  "explanation": "**物理**（不用深究）：惠更斯-菲涅耳原理 — 波前每点可看作新波源。碰到锐利边时，这些『次波源』发射进几何阴影区，相当于波被『重新发射』绕过障碍。\n\n**vs 反射**：\n| | 反射 | 衍射 |\n|---|---|---|\n| 触发 | 大面镜面 | 锐利边 |\n| 方向 | 镜像 | 弯曲进阴影 |\n| 强度 | 近原信号 | 弱 |\n\n**后果**：WiFi 在墙角后面能收到；蜂窝基站不需每户都看见。\n\n**考点**：看到关键词『**no LOS**』『绕过障碍』『锐利边』→ 选衍射。"
},

"lec23:3": {
  "title": "Diffraction 图示",
  "summary": "另一角度图示衍射。信号源 → 障碍物 → 障碍物后阴影区也能收到（弱）。",
  "key_points": ["重复 image", "阴影区收到信号"]
},

"lec23:4": {
  "title": "Scattering (散射)",
  "summary": "**Scattering**: 波碰到比波长小的物体（树叶、灯柱、路标）被散成多个方向。**最难建模**（方向是统计性的）。",
  "key_points": [
    "Object < λ → scattering",
    "波被散成各方向",
    "数学上最难精确预测",
    "野外测量比纯计算可靠"
  ],
  "explanation": "**类比**：反射像镜子（大平面），衍射像门缝（边缘），**散射像把球扔进一堆小石子**（小物体）— 球弹出去方向乱。\n\n**例子**：\n- WiFi 信号穿过盆栽 → 树叶尺寸跟 λ 接近 → 散射\n- 路过的小路标、灯柱 → 散射\n- 雨滴对高频毫米波（5G）→ 散射（毫米波雨天衰减大）\n\n**三个一起记忆**（必考）：\n```\n物体尺寸\n   ≫ λ   →  Reflection（反射）\n   锐边  →  Diffraction（衍射）\n   < λ   →  Scattering（散射）\n```\n\n**考点**：选择 / 判断三种传播现象。**先看物体尺寸跟 λ 比**。"
},

"lec23:5": {
  "title": "Multipath Fading + Impact of Mobility",
  "summary": "**Multipath**: 信号从多条路径到达 (LOS + 反射 + ...)，路径长度不同 → 相位不同 → 叠加可能相消或相长。**Mobility creates signal fluctuations**。\n\n**Large-scale fading**: 信号随距离平均衰减（pathloss + 阴影）。\n**Small-scale fading**: 小范围（一两个 λ）剧烈跳动。",
  "key_points": [
    "Multipath: LOS + 反射 + 衍射 + 散射",
    "路径差 → 相位差 → 干涉",
    "Mobility 让相位关系实时变",
    "**Large-scale**: 随距离平均衰减 (pathloss + shadow)",
    "**Small-scale**: 小范围剧烈跳动 (multipath interference)"
  ],
  "explanation": "**为什么会这样**：想象两个人同时朝水池扔石头：波峰对波峰 → 加强，波峰对波谷 → 抵消。电磁波一样。\n\n两条路径差 Δd → 时间差 Δt = Δd/c → 相位差 Δφ。如果 Δφ = π（半波长差），两路径信号正好相消 → 接收端几乎收不到（深 fade）。\n\n**大尺度 vs 小尺度**：\n- **Large-scale**: 距离 1m→10m，信号衰 20 dB（『慢』变化）\n- **Small-scale**: 一两个波长（10-20 cm）范围内可跳 30 dB → **接收端动几 cm，信号瞬间从 -40 dBm 变 -70 dBm**\n\n**Mobility 角色**：\n- 你走路时，每条反射路径长度变 → 相位关系实时改变 → 干涉模式动态变 → 信号波动\n- **开车信号忽满格忽 1 格的原因**\n\n**静止也会 fade**：你不动，但屋里人走过、空调风扇转 → 反射体动 → multipath 关系变 → 信号仍波动。"
},

"lec23:6": {
  "title": "Multipath — Coherence Time",
  "summary": "**Coherence time (Tc)**: 信道脉冲响应保持不变的最大时间。\n\n**ISI (Inter-Symbol Interference)**: 一个 symbol 通过多径到达接收端有多个延迟拷贝（拖尾）。如果下个 symbol 来得太早，上个 symbol 拖尾还没散完 → ISI。\n\n→ **Symbol period 必须 ≤ Tc** 才能正确解码。",
  "key_points": [
    "**Tc** = coherence time",
    "Symbol period > Tc → ISI → 解码失败",
    "Mobility 大 → Tc 小（信道变化快）",
    "限制最大 symbol rate"
  ],
  "explanation": "**关键直觉**：想象你跟人说话，每句之间 1 秒间隔。如果你说完一句后房间立刻变成另一个空间（回声完全变），第二句和第一句余音搅在一起 → 听不清。\n\n无线信道也这样。一个 symbol 经多径到接收端有多个延迟拷贝（拖尾）。如果下个 symbol 来得早，上个的拖尾还没散完 → **ISI**。\n\n**数值感觉**：\n- 室内 WiFi 静止：Tc ≈ 几十 ms\n- 开车（30 m/s）：Tc 显著下降到 ms 级\n- 高铁/飞机：Tc 更短\n\n**考点**：『为什么 multipath 限制最大 symbol rate？』→ Coherence time 限制 symbol 间隔。"
},

"lec23:7": {
  "title": "Noise and Interference — SNR / SINR",
  "summary": "两个无线链路质量指标：\n\n**SNR (Signal-to-Noise Ratio)** dB = 10·log₁₀(S/N) — 只考虑热噪声。\n\n**SINR (Signal-to-Interference-plus-Noise Ratio)** dB = 10·log₁₀(S/(N+I)) — 还加干扰。\n\n**SNR/SINR vs BER**: 高 SNR → 低 BER → 可用高 modulation/code rate。",
  "formula": "$$\\mathrm{SNR}_{dB} = 10 \\log_{10}\\frac{S}{N}, \\quad \\mathrm{SINR}_{dB} = 10 \\log_{10}\\frac{S}{N+I}$$",
  "key_points": [
    "**SNR** dB = 10·log(S/N), 纯热噪声背景",
    "**SINR** = 10·log(S/(N+I)), 加干扰",
    "高 SNR → 低 BER → 高 bit rate",
    "Rate adaptation 依据"
  ],
  "explanation": "**dB 是什么**：对数刻度，让大跨度好读。\n- 比值 ×10 = +10 dB\n- 比值 ×2 ≈ +3 dB\n- 比值 ÷10 = -10 dB\n\n→ SNR=20 dB 意味信号比噪声大 100 倍。\n\n**SNR 怎么影响 bit rate**：\n香农极限：C = B · log₂(1+SNR)。**SNR 高 → 同 BW 能传更多 bit**。\n\n实际中 WiFi/蜂窝用 **rate adaptation**：\n- SNR 高 → 64-QAM, 5/6 码率 → 高数据率\n- SNR 中 → QPSK, 1/2 码率\n- SNR 低 → BPSK, 1/3 码率（保守，求别出错）\n\n**SNR vs SINR**：\n- 单一发射 → SNR\n- 密集部署（office, 会议中心多 AP）→ 必须 SINR\n\n**例题**：信号 S = -50 dBm, 噪声 N = -90 dBm。\nSNR_dB = (-50) − (-90) = **40 dB**（dB 减法 = 比值）。",
  "gotcha": "dB 不能直接『加』信号强度，要转线性单位再加。但 SNR_dB = S_dB − N_dB（对数比）。"
},

"lec23:8": {
  "title": "Received Signal Over Time",
  "summary": "图示实际接收信号在时间维度剧烈波动（multipath + mobility 综合）。即使静止节点，环境物体动 → 信号也波动。**Wireless 信道是 statistical**，不是 deterministic。",
  "key_points": [
    "实际信号 dB 跳几十 dB",
    "静止也会变（环境物体动）",
    "Wireless 信道是 statistical",
    "建模通常给均值 + 方差"
  ],
  "explanation": "**核心结论**：**无线信道是 time-varying + unpredictable**，不像有线一根管子畅通。\n\n**对网络设计意义**：\n- TCP 在无线下会被 fade 误判为拥塞 → 错误减半 cwnd\n- 视频码率自适应必须容忍突发 fade\n- 蜂窝基站调度依赖 channel state info (CSI) feedback"
},

"lec23:9": {
  "title": "Simulating Wireless Environment — 实际公式",
  "summary": "实际 path loss 用：**PL(d) = PL(d₀) + 10α·log(d/d₀) + X**\n\n- PL(d₀): 参考距离 (通常 1m) 的 path loss\n- α: pathloss exponent (环境决定)\n- X: log-normal 随机 shadowing 项\n\nTestbed 和实测远比理论可靠。",
  "formula": "$$PL(d) = PL(d_0) + 10 \\alpha \\log\\left(\\frac{d}{d_0}\\right) + X$$",
  "key_points": [
    "PL(d) = PL(d₀) + 10α·log(d/d₀) + X",
    "α: pathloss exponent",
    "X: log-normal random shadowing",
    "α 典型: 2 free, 2.7-3.5 urban, 4-6 indoor",
    "实测 > 理论"
  ],
  "explanation": "**X 是什么**：随机变量（typically log-normal），代表『同距离不同位置的随机变化』。两人都在 AP 10m 远，一个在走廊一个在房间深处，信号能差 10 dB → 这就是 X。\n\n**例**：d₀=1m，PL(d₀)=40dB，α=3，d=10m：\nPL(10) = 40 + 10×3×log(10/1) = 40 + 30 = **70 dB + 随机阴影**。\n\n**考点**：\n- 给参数算 PL\n- 解释为什么室内信号衰得比理论快 → α 高\n- 选择题：城市蜂窝 α 多少？→ 2.7-3.5"
},

"lec23:10": {
  "title": "Difference Between Wireless and Wired — 两大根本差异",
  "summary": "**两大根本差异**:\n\n(1) **Time-varying, often unpredictable channel quality**: 无线信道因为 mobility + 动态环境不断变化。\n\n(2) **Interference**: 广播性质 → 多发射机互相干扰。\n\n→ 这两点是后续所有 wireless MAC 设计的根源。",
  "key_points": [
    "(1) **Time-varying, unpredictable**: mobility + 环境动",
    "(2) **Interference**: 广播 → 邻居干扰",
    "这两条决定了 wireless 比 wired 难做"
  ],
  "explanation": "**为什么这页这么重要**：如果你能记住这两条，你能推出整个 wireless MAC 章节的设计动机：\n\n1. **Time-varying channel** → 需要 **rate adaptation**\n   - 信号强度不停变 → modulation/code rate 也得跟着变\n\n2. **Broadcast 介质 → interference**\n   - 一个频段同一时刻只能一个发\n   - 必须 MAC 协议决定谁发\n   - 干扰由 sender 看不见的人造成 (hidden terminal) → MAC 设计难\n\n**跟有线对比**：\n| | 有线 | 无线 |\n|---|---|---|\n| 信道 | 稳定 | 时变 |\n| 介质 | 独占 | 广播 |\n| BER | 极低 (~10⁻¹²) | 可能 10⁻³ |\n| 半 / 全双工 | 全双工 | 通常半双工 |\n| Collision detect | 容易 | **不可能**（耳朵被淹）|\n\n**考点（极高频）**：『为什么 wireless 比 wired 难？』必答这两条。"
},

"lec23:11": {
  "title": "Wireless MAC Protocols — 章节封面",
  "summary": "从物理层进入 MAC 层。接下来讲 ALOHA、CSMA、CSMA/CA、RTS/CTS。核心问题：广播媒介下怎么分配信道。",
  "key_points": [
    "进入 MAC 层",
    "广播介质下分配信道",
    "覆盖 ALOHA, CSMA, CSMA/CA, RTS/CTS"
  ]
},

"lec23:12": {
  "title": "The More, The Messier",
  "summary": "多无线节点同发会互相碰撞，需要 MAC 协调。节点越多 → 碰撞越多 → MAC 越关键。",
  "key_points": [
    "多节点 → 碰撞概率 ↑",
    "MAC 必须协调"
  ]
},

"lec23:13": {
  "title": "Role of MAC — 三大职责",
  "summary": "MAC 要做的三件事：\n\n(1) **Rate adaptation** — 根据信道质量选 modulation。\n\n(2) **Avoid interference** — 碰撞避免。\n\n(3) **Provide fairness** — 让多节点公平共享。",
  "key_points": [
    "① Rate adaptation",
    "② Avoid interference",
    "③ Fairness"
  ],
  "explanation": "**为什么 wireless MAC 比 wired MAC 多了一件事**：\n- 有线 MAC（如 Ethernet CSMA/CD）只管『谁能发』\n- 无线 MAC 还要管 **rate adaptation**：因为信道时变\n\n**三个目标冲突**：\n- 极致 fairness → 信道好的节点也不能多用\n- 极致 throughput → 弱节点 starve\n- 802.11 DCF 折中：节点机会均等（fair）+ 允许 rate adaptation\n\n**考点**：『wireless MAC 目标？』必答 3 点。"
},

"lec23:14": {
  "title": "MAC Categories — 三大类",
  "summary": "三类（重复 lec21）：\n\n(1) **Centralized base station** — 基站调度 (TDMA/FDMA/CDMA), 蜂窝网。\n\n(2) **Controlled access** — channel reservation (token)。\n\n(3) **Random access** — ALOHA, 802.11 CSMA/CA, TDMA, FDMA。",
  "key_points": [
    "① Centralized BS: 蜂窝, TDMA/FDMA/CDMA",
    "② Controlled access: token",
    "③ Random access: ALOHA, 802.11 CSMA/CA",
    "现代 wireless 主要用 random (CSMA/CA)"
  ],
  "explanation": "**WiFi 用 random access (CSMA/CA)**，蜂窝用 channel partition (BS 集中调度)。"
},

"lec23:15": {
  "title": "All These Ranges — Transmission / Interference / Carrier Sensing",
  "summary": "每个无线节点有 **3 个圆**：\n\n(a) **Transmission range** — 能正确解码\n\n(b) **Interference range** — 能干扰但解不了\n\n(c) **Carrier sensing range** — 能检测能量\n\n**关系**: Transmission < Interference < Carrier sensing。",
  "key_points": [
    "**Transmission range**: 能解码",
    "**Interference range**: 能干扰但解不了",
    "**Carrier sensing range**: 检测能量",
    "**Layer**: Transmission < Interference < Sensing"
  ],
  "explanation": "**为什么有 3 个范围**：信号强度随距离衰减。从近到远：\n1. **近** (高 SNR) → 能解码 = transmission range\n2. **中** (SNR 低，解不了但能量明显) → 干扰别人接收 = interference range\n3. **远** (SNR 更低，但能量还能测到) → carrier sense 检测但解不了 = sensing range\n\n**数值感觉**（典型 WiFi）：\n- Transmission: 30 m\n- Interference: 70 m\n- Carrier sensing: 100 m\n\n**为什么这页重要**：后面 **hidden / exposed terminal** 判定靠这三个范围。"
},

"lec23:16": {
  "title": "Carrier Sense Medium Access (CSMA)",
  "summary": "**CSMA**: 传输前先 carrier sense。**Idle** → 发；**Busy** → 推迟。**CSMA is sender-driven**。",
  "key_points": [
    "Sense before send",
    "Idle → send",
    "Busy → defer",
    "**Sender-driven** (决策只看自己听到什么)"
  ],
  "explanation": "**CSMA vs ALOHA**：CSMA 至少看见别人在说话就闭嘴。\n\n**但还会碰**：propagation delay。A 在 t=0 发，信号到 B 要 d/c 秒。这段时间 B 监听仍 idle，于是 B 也发 → 在中间某处碰。\n\n**Sender-driven 是关键问题**（下页讲）。"
},

"lec23:17": {
  "title": "Discussion Time — CSMA 够吗？",
  "summary": "讨论题：『CSMA 在无线下够用吗？』",
  "key_points": ["课堂讨论题，引出下页"]
},

"lec23:18": {
  "title": "CSMA 不够 — Sender vs Receiver 错配",
  "summary": "**Insight (核心)**: CSMA **sender-driven**，但 **interference 是 receiver-driven**。Sender 听到自己附近的载波，但**干扰发生在 receiver 端**。**Sender 看到 idle 不等于 receiver 那边也 idle**。",
  "key_points": [
    "CSMA = sender-driven",
    "Interference = receiver-driven",
    "**Sender 看 ≠ Receiver 看**",
    "这就是 hidden terminal 的根源"
  ],
  "explanation": "**这一页是 wireless MAC 的核心 insight**：\n\n**有线下**：A、B 通过电缆物理连接，A 处载波 = B 处载波（信号沿电缆走）。所以 sender 听到 idle = 整条线 idle，能安全发。\n\n**无线下**：A 和 B 通过空气（不同物理介质区域）。A 监听 A 周围，B 接收看 B 周围。**两者范围可以完全不重叠**。\n\n```\n[A]---listens around A---     ---around B---[B]\n                            ^\n                这里有个 C 在发，A 听不到，但会干扰 B\n```\n\n**解药**：让 receiver 也参与协调（CTS）。\n\n**考点**：『CSMA 在无线下为什么不够？』必答 sender vs receiver 不对称。"
},

"lec23:19": {
  "title": "Hidden Terminal Problem — final Q5",
  "summary": "**Hidden Terminal**: \n- X 在 sender A 的 sensing range **外**（听不到 A）\n- X 在 receiver B 的干扰 range **内**（能干扰 B）\n- X 觉得信道闲 → 也发 → 在 B 处碰撞 → B 收不到 A\n\n**A 自己觉得发得好好的**，但 B 收不到。",
  "key_points": [
    "判定: X 在 sender 范围**外** + 在 receiver 干扰范围**内**",
    "X 听不到 A → 觉得 idle → 也发",
    "B 处碰撞",
    "A 不知道（自己听到 idle）",
    "**Final Q5 直接考**"
  ],
  "explanation": "**详细场景**：\n```\n           A 的范围\n         ┌─────────┐\n         │   A───▶ B │\n         └─────────┘ \n                     C\n             ↑\n          C 在 A 范围外，听不到 A\n          但 C 能干扰 B\n```\n\n**步骤还原**：\n1. A 想发数据给 B\n2. A 监听信道：idle (C 当前没发，没干扰 A)\n3. A 开始发\n4. **同时** C 监听：也是 idle（C 在 A 范围外）\n5. C 觉得能发，开始发\n6. A 和 C 的信号在 B 处碰撞 → B 收不到\n7. A 不知道，以为发成功\n8. ACK 没回，A 才知道丢了\n\n**判定方法**（必背）：节点 X 是 A→B 通信的 hidden ⟺\n- X 在 **A 的 sensing range 外**（X 听不到 A）\n- X 在 **B 的 interference range 内**（X 能干扰 B）\n\n**解药 RTS/CTS**：B 发 CTS 后周围都静默，即使 C 听不到 A，听得到 B 的 CTS。\n\n**期末样题 Q5**：4 节点 A、B、C、E，A→B 通信。判定 C、E 是 hidden（在 A 范围外 + 在 B 范围内）。\n\n**考点**：判定 hidden 必背：sender 外 + receiver 内。",
  "gotcha": "判定方向：sender 外 + receiver 内。**别记反**。"
},

"lec23:20": {
  "title": "Exposed Terminal Problem — final Q5",
  "summary": "**Exposed Terminal**:\n- C 在 sender A 的范围 **内**（听到 A）\n- C 的目标 receiver D 在 A 范围 **外**（不会被 A 干扰）\n- C 因 CSMA 见信道忙就退让 → **本可并发但被抑制 → 浪费**\n\n**No clean fix in CSMA/CA**。",
  "key_points": [
    "判定: C 在 sender 范围**内** + C 的目标在 sender 范围**外**",
    "症状: 本可并发但 CSMA 抑制 C",
    "**Final Q5 直接考**",
    "RTS/CTS 不能解 exposed"
  ],
  "explanation": "**详细场景**：\n```\n         A 的范围\n       ┌────────────┐\n       │   C─▶D     │\n       │   ▲        │\n  E───▶│   │        │\n       │   A────▶B  │\n       └────────────┘\n                D 在 A 范围外\n```\n\n**步骤还原**：\n1. A 正在发数据给 B\n2. C 监听信道：busy (C 在 A 范围内，听到 A)\n3. CSMA 让 C 退让\n4. **但是！** C 想发给 D，D 在 A 范围外，A 的发射到不了 D → C 和 A 同时发不会在任何 receiver 处碰\n5. C 退让 = 浪费并发机会\n\n**判定方法**（必背）：节点 X 是 exposed ⟺\n- X 在 **sender 范围内**（听到 sender）\n- X 的 **receiver 在 sender 范围外**（不会被 sender 干扰）\n\n**为什么 RTS/CTS 不能解**：C 听到 A 的 RTS 仍要静默（协议机械执行）。即使 C 知道自己发给 D（A 干扰不到的人），协议规定就这样。\n\n**对比记忆 hidden vs exposed**：\n| | Hidden | Exposed |\n|---|---|---|\n| X 跟 sender A | 在 A 范围**外** | 在 A 范围**内** |\n| X 跟 receiver B | 在 B 干扰范围**内** | X 自己 receiver 在 A 范围**外** |\n| 症状 | 该停没停 → 碰撞 | 该发没发 → 浪费 |\n| 802.11 解法 | RTS/CTS 解 | **没解** |\n\n**期末样题 Q5**：A→B 通信，C、E 节点。判定 C 和 E 都听不到 A（在 A 范围外）→ 都是 **hidden**。没节点同时满足『在 A 范围内 + 自己目标在外』→ **无 exposed**。\n\n**考点**：判定方向反就全错。**记忆抓手**：『隐藏 = 隐身没看见，该停没停 → 撞』；『暴露 = 暴露在视野里，该发不敢发 → 亏』。",
  "gotcha": "Hidden 和 exposed 的判定方向**正好相反**。考前默写一遍判定条件。"
},

"lec23:21": {
  "title": "How to Deal with Hidden Terminal Problem",
  "summary": "两条思路：(1) **Avoid it** — 用 busy tone 或 RTS/CTS 提前避碰；(2) **Deal with it** — ZigZag 让碰撞包能解码。",
  "key_points": [
    "Solution #1: Avoid (busy tone, RTS/CTS)",
    "Solution #2: Deal with collisions (ZigZag)"
  ]
},

"lec23:22": {
  "title": "Solution #1: Avoid it — Busy Tone",
  "summary": "**Busy tone**: receiver 在收数据时**广播 busy tone**。Nodes hearing busy tone keep silent。\n\n**思想**: 让 receiver 主动喊『我在收，安静』。",
  "key_points": [
    "Receiver 收数据时发 busy tone",
    "Nodes hearing 静默",
    "需要双信道（数据 + tone）",
    "硬件复杂，早期 802.11 不采用"
  ],
  "explanation": "**为什么没普及**：\n- 需要专用 busy tone 信道（频段）\n- 硬件实现复杂\n- 实际部署不实用 → 让位给 RTS/CTS"
},

"lec23:23": {
  "title": "Solution #1: Avoid it — MACA (RTS/CTS)",
  "summary": "**MACA (Karn'90) 协议**:\n\n1. **Transmitter** → **RTS (Request-to-Send)** → Receiver\n2. **Receiver** → **CTS (Clear-to-Send)** → Transmitter\n3. Nodes hearing RTS keep silent 短时（让 sender 能收 CTS）\n4. Nodes hearing CTS keep silent for **transmission duration**",
  "key_points": [
    "Sender 发 RTS",
    "Receiver 回 CTS",
    "听到 RTS 静默 t_CTS（让 sender 能收 CTS）",
    "听到 CTS 静默 t_data（保护数据）",
    "**MACA = Multiple Access with Collision Avoidance**",
    "Cite: Karn (1990)"
  ],
  "explanation": "**为什么 RTS 之后还要 CTS**：\n- 仅 RTS 不够：只有听到 A 的人会静默，但 hidden 听不到 A（这就是 hidden 的定义）\n- 所以靠 CTS：CTS 由 B 发，B 周围所有节点（包括 hidden）都听得到\n\n**为什么用『短包』RTS/CTS 而不是直接发数据**：\n- 如果 RTS 跟别人碰撞，损失的只是 RTS 这点字节；数据本身没浪费\n- 先用短包试水\n\n**缺点**：\n- RTS/CTS 本身有开销\n- **不能解 exposed terminal**\n- 短帧场景（如 ACK）反而 RTS/CTS 开销大于收益 → 可选\n\n**考点**：\n- 解释 RTS/CTS 流程\n- 为什么 CTS 由 receiver 发（不是 sender）\n- 为什么 RTS/CTS 解 hidden 不解 exposed"
},

"lec23:24": {
  "title": "Example of RTS and CTS",
  "summary": "图示 A→B 通信，C 听到 RTS 静默，D 听到 CTS 静默。两人都安静到 ACK 完成。",
  "key_points": [
    "A 发 RTS 给 B",
    "C 听到 RTS（C 在 A 范围内）",
    "D 听到 CTS（D 在 B 范围内）",
    "两人都静默到 ACK 完成"
  ]
},

"lec23:25": {
  "title": "802.11 MAC = CSMA/CA",
  "summary": "**802.11 MAC = CSMA/CA**:\n\n- **Carrier Sense** (听后说)\n- **Collision Avoidance** (不能 CD，靠 random backoff + 可选 RTS/CTS)\n- 用 ACK 确认成功（无线丢包概率高）\n- **NAV** (Network Allocation Vector): 虚拟载波检测\n- Random backoff: 倒计时 [0, CW]，闲减、忙冻结",
  "key_points": [
    "Carrier sense (物理 + 虚拟 NAV)",
    "Collision avoidance (不 CD)",
    "RTS/CTS 可选",
    "ACK 确认（无线丢包多）",
    "Random backoff + binary exponential"
  ],
  "explanation": "**CSMA/CA vs CSMA/CD**：\n| | CSMA/CD (Ethernet) | CSMA/CA (WiFi) |\n|---|---|---|\n| Detect collision | 边发边听 | **做不到** (TX 淹自己 RX) |\n| Avoid collision | 一旦碰立即 abort | 提前 random backoff + 可选 RTS/CTS |\n| Recovery | abort + 重发 | 必须 ACK 确认；超时重发 |\n\n**为什么无线不能 CD**：发射机和接收机在同一根天线上。**发自己信号时，自己能量比接收的别人信号大 10⁹ 倍**，根本听不到别人。"
},

"lec23:26": {
  "title": "CSMA/CA — 时序例",
  "summary": "完整时序图示：A→B 通信，C/D 通过听 RTS/CTS 静默。\n\nNAV (Network Allocation Vector) = 8，意思是『接下来 8 单位时间静默』。\n\n1. A 发 RTS\n2. B 回 CTS (with NAV=8)\n3. A 发 DATA\n4. B 回 ACK",
  "key_points": [
    "1. A → RTS → B",
    "2. B → CTS (NAV=8) → A",
    "3. A → DATA → B",
    "4. B → ACK → A",
    "C, D 维护 NAV 静默"
  ]
},

"lec23:27": {
  "title": "CSMA/CA — 三大机制拆解",
  "summary": "CSMA/CA 三大机制：\n\n(1) **Physical carrier sense** (energy detection) — 测信道能量。\n\n(2) **Virtual carrier sense** (packet sniffing) — RTS/CTS 内的 **NAV** 字段。\n\n(3) **Collision avoidance** (random backoff)。",
  "key_points": [
    "① **Physical CS** = energy detection",
    "② **Virtual CS** = NAV 维护",
    "③ **Collision avoidance** = random backoff"
  ],
  "explanation": "**虚拟载波检测 NAV**：\n- RTS 和 CTS header 里有 Duration 字段，说『接下来要占用多久』\n- 其他节点解析这字段，**自己维护倒数计时器 NAV (Network Allocation Vector)**\n- NAV > 0 时即使能量检测显示 idle，也认为忙\n\n**完整判断**：\n```\n物理 CS busy 或 NAV > 0 → 忙\n物理 CS idle 且 NAV = 0 → 闲\n```\n\n**考点**：『CSMA/CA 几种载波检测？』→ 物理 + 虚拟两种。『NAV 怎么维护？』→ 听到 RTS/CTS 后读 Duration 字段，倒数到 0。"
},

"lec23:28": {
  "title": "Random Backoff",
  "summary": "**Random Backoff**:\n\n1. 选 backoff interval ∈ [0, CW] (CW = Contention Window)\n2. **Count down** when medium idle\n3. **Freeze** if medium busy\n4. **Suspend** if medium becomes busy\n5. Backoff → 0 → 发 RTS\n\n**例**: B1=25, B2=20。B2 倒到 0 先发，B1 冻结在 5。",
  "key_points": [
    "CW = Contention Window 大小",
    "随机数 ∈ [0, CW] 倒数",
    "Medium idle → 减 1",
    "Medium busy → 冻结",
    "Backoff = 0 → 发 RTS",
    "**冻结不重置**"
  ],
  "explanation": "**为什么随机退避**：如果两节点都见信道闲就发就一定碰。各自挑随机数 → 不同节点不同时刻发 → 减少碰撞。\n\n**Medium 忙就冻结**：保证退避时间真实反映等待，不因信道一直忙而无效消耗。\n\n**Timeline 例**：CW=31\n- 节点 1: 随机选 25\n- 节点 2: 随机选 20\n\n两人开始倒数，medium idle 时每 slot 减 1。\n- 时刻 0: 节点 1=25, 节点 2=20\n- 时刻 20: 节点 2 到 0，开始发\n- 节点 1 看到 medium 忙，**冻结在 5**\n- 节点 2 发完，medium 闲\n- 节点 1 从 5 继续倒数（不重置！）\n\n**冻结 → 恢复** 机制保证『等久了的节点优先』，避免反复碰。\n\n**考点**：给 timeline 题画对冻结行为。常见错：以为 medium 闲下来重选随机数。",
  "gotcha": "冻结时 backoff counter **保留**，不重新随机选。"
},

"lec23:29": {
  "title": "Put All Together — CSMA/CA 完整流程",
  "summary": "**完整发送决策流程**:\n\n1. Carrier sense\n2. If idle → wait **DIFS** → still idle → send\n3. Replies (CTS, ACK): wait **SIFS** (shorter, priority)\n4. If busy → wait until idle\n5. Realize idle after DIFS\n6. Start random backoff\n7. Send when backoff = 0\n8. No ACK → increase backoff (CW × 2)",
  "key_points": [
    "Sense → idle → DIFS → still idle → send",
    "Replies (CTS/ACK) → SIFS (短，优先)",
    "Busy → wait → DIFS → random backoff",
    "No ACK → CW × 2",
    "Success → reset CW = CWmin"
  ],
  "explanation": "**DIFS vs SIFS**（必背）：\n- **SIFS** (Short Inter-Frame Space) ≈ 10 μs: 给立即回复 (CTS/ACK) 用，让回复抢先于新一轮竞争\n- **DIFS** (DCF Inter-Frame Space) ≈ 50 μs: 给新一轮竞争用\n\nSIFS < DIFS 保证『同一对话』的 ACK/CTS 优先于『新对话』开始。\n\n**完整 timeline**:\n```\nA: --DIFS--RTS-----------DATA------\nB:        --SIFS--CTS--SIFS--ACK\nC:        ────── 静默 (NAV) ──────\n```\n\n**考点**：\n- 看到题目里『DIFS vs SIFS 区别』→ 先看是不是回复包（CTS/ACK）\n- 时间间隔分析: 能不能从 timeline 看出哪个是 SIFS、哪个是 DIFS"
},

"lec23:30": {
  "title": "How to Choose the Backoff Interval?",
  "summary": "**Trade-off**: CW 太大 → 等久浪费；CW 太小 → 容易碰。Tricky 选『正确』CW。**Idea**: 动态调整。",
  "key_points": [
    "CW 大 → MAC overhead 大",
    "CW 小 → 碰撞多",
    "**直觉**: 动态调",
    "下页讲 DCF"
  ]
},

"lec23:31": {
  "title": "802.11 DCF — Distributed Coordination Function",
  "summary": "**802.11 DCF**: **CW depends on # of contending nodes**, 随时间变。\n\n→ **Adapt CW based on collision occurrence**。\n\n→ Binary Exponential Backoff (下页)。",
  "key_points": [
    "DCF: 802.11 默认 MAC",
    "CW 随竞争节点数动态变",
    "Failure (collision) → 调整 CW",
    "下页详讲 binary exp backoff"
  ]
},

"lec23:32": {
  "title": "Binary Exponential Backoff",
  "summary": "**Binary Exponential Backoff**:\n\n- Failure (no CTS for RTS) → **CW = CW × 2**\n- Success → **CW = CWmin**\n- CWmin = 31 (802.11b) / 15 (802.11g)\n- 最大 CWmax\n\n**Problems**: (a) Fast oscillation in CW; (b) Unfairness when one node backs off more than others.\n\n**Key reason**: CW 重置太快！",
  "key_points": [
    "Failure → CW × 2",
    "Success → CW = CWmin",
    "CWmin = 31 (b) / 15 (g)",
    "**问题**: 振荡 + 不公平",
    "Root cause: CW 重置太快"
  ],
  "explanation": "**为什么 binary exp**：\n- 失败多 = 拥挤 → CW 应大让大家分散\n- Doubling 增长合适\n\n**数字例**：\n- 失败 1 次 CW=63\n- 失败 2 次 CW=127\n- 失败 5 次 CW=1023\n\n**为什么不公平**：\n- 节点 A 经历多次失败 CW=1023，刚成功一次回到 31\n- 节点 B 一直成功，CW 始终 31\n- 平均看 A 等的时间是 B 的 16 倍 → 不公平\n\n**考点**：\n- 给失败次数算当前 CW\n- 解释为什么不公平"
},

"lec23:33": {
  "title": "MACAW Solution — 指数增 + 线性减",
  "summary": "**MACAW (SIGCOMM '94) 改进**:\n\n- 成功 → **CW -= 1** (linear decrease)\n- 失败 → CW × 2 (exponential)\n- **类比 TCP AIMD**\n- Append CW to packet → 邻居也调",
  "key_points": [
    "Success → CW − 1 (linear)",
    "Failure → CW × 2 (exponential)",
    "类 TCP AIMD",
    "Append CW to packet 让邻居同步"
  ],
  "explanation": "**思路**：TCP AIMD = 加法增、乘法减。MACAW 反过来：**指数增（碰撞），线性减（成功）**。\n\n两者本质都是『失败时大幅退让，成功时谨慎进取』。\n\n**跟 TCP CC 的关系**：\n- TCP: cwnd 想 **变大** (吞吐)，AI 增 + MD 减\n- MAC backoff: CW 想 **变小** (少等)，ED 增 + LD 减\n\n概念一致，方向相反。"
},

"lec23:34": {
  "title": "Solution #2: Deal With It — ZigZag Decoding",
  "summary": "**ZigZag decoding (SIGCOMM '08)** by 学术界：不躲碰撞，直接从两次碰撞包里逐 chunk 解出原数据。利用 802.11 重传 + jitter。",
  "key_points": [
    "Receiver designed to cancel/utilize interference",
    "Decode collisions instead of avoiding",
    "学术亮点 (SIGCOMM '08)"
  ]
},

"lec23:35": {
  "title": "ZigZag Decoding — 流程",
  "summary": "Step 1: 利用第 1 次碰撞中的『干净 chunk』解 chunk 1。\nStep 2: 从第 2 次碰撞减去 chunk 1 解 chunk 2。\nStep 3: 反过来减 chunk 2 解 chunk 3。...\n\n要求：两次重传 jitter 不同，让 chunks 错位。",
  "key_points": [
    "Two collision rounds (sender retransmits with jitter)",
    "Step 1: decode chunk 1 from first round's clean part",
    "Step 2: subtract chunk 1 from second round → decode chunk 2",
    "Step 3: subtract chunk 2 → decode chunk 3 ..."
  ],
  "explanation": "**思路新颖**：把『碰撞 = 损失』变成『碰撞 = 多次机会』。利用 sender 自然 retransmit 行为，无需额外信道。\n\n**实际未普及**，但作为思路理解就好。"
},

"lec23:36": {
  "title": "IEEE 802.11 Wireless Protocols — b/a/g/n/ac",
  "summary": "速度演进:\n\n- **b (1999)**: 2.4 GHz, DSSS/FHSS, ≤11 Mbps\n- **a (1999)**: 5 GHz, OFDM, ≤54 Mbps\n- **g (2003)**: 2.4 GHz, OFDM, ≤54 Mbps\n- **n (2009)**: 2.4/5 GHz, **MIMO-OFDM** (max 4 MIMO streams), 300-500 Mbps\n- **ac / WiFi 5 (2013)**: 5 GHz, MIMO-OFDM (max 8 MIMO), >1 Gbps",
  "key_points": [
    "**b**: 2.4G, 11M",
    "**a/g**: 5/2.4G, 54M",
    "**n**: MIMO ~600M (key inflection)",
    "**ac (WiFi5)**: 5G, >1Gbps",
    "Key change: 802.11n 引入 MIMO"
  ],
  "explanation": "**关键拐点**：\n- **n** 引入 MIMO（多天线同时发不同流），throughput 跃升\n- **ac** 用更大 channel BW + 更高阶 MIMO\n\n**考点**：考试一般问 **频段** 或 **大致速率**。记：\n- 2.4 GHz: b/g/n（慢但穿墙好）\n- 5 GHz: a/n/ac/ax（快但短距）"
},

"lec23:37": {
  "title": "IEEE 802.11 Wireless Protocols — af/ah/ax",
  "summary": "**新一代标准**:\n\n- **af / White-Fi (2014)**: 未用 TV bands (54-590 MHz), 35-560 Mbps, **1-km range**\n- **ah / Wi-Fi HaLow (2017)**: 900 MHz, 347 Mbps, 1-km range, **低功耗，支持 IoT**\n- **ax / Wi-Fi 6 (2020)**: 2.4/5 GHz, max 14 Gbps, 密集场景优化\n\n**都用 CSMA/CA 做 MAC**。",
  "key_points": [
    "**af**: TV whitespace, 1km range",
    "**ah**: 900MHz, IoT, low power",
    "**ax (WiFi 6)**: 14 Gbps, 密集场景",
    "All CSMA/CA"
  ]
},

"lec23:38": {
  "title": "802.11 LAN Architecture",
  "summary": "**Wireless host** 跟 base station (AP) 通信。\n\n**Modes**:\n(a) **Infrastructure mode**: 通过 AP 互通\n(b) **Ad-hoc mode**: 节点直接互通，无 AP\n\n**Basic Service Set (BSS)** 在 infrastructure mode 包括: wireless hosts + AP。Ad-hoc mode 只有 hosts。",
  "key_points": [
    "Wireless host ↔ AP (base station)",
    "**Infrastructure mode**: 通过 AP",
    "**Ad-hoc mode**: 直连，无 AP",
    "**BSS** = AP + hosts (infrastructure)",
    "ad-hoc: hosts only"
  ],
  "explanation": "**家用 WiFi = Infrastructure**：手机 / 笔记本通过 AP 上网。AP 同时连有线（到 router）→ 桥接 wireless 到 wired internet。\n\n**Ad-hoc 场景**：两台设备直接对连（如 AirDrop 早期 / WiFi Direct）。没有 AP，节点间直接 CSMA/CA。\n\n**进入 BSS 流程**：\n1. **Scan**: 扫描看周围 AP（被动监听 beacon 或主动发 probe request）\n2. **Auth**: 跟 AP 认证（早期 open / WEP，现代 WPA2/3）\n3. **Associate**: 跟 AP 关联（AP 把你加入它的客户表）\n4. **Data**: 开始通信"
},

"lec23:39": {
  "title": "802.11 Channels",
  "summary": "**802.11b**: 11 channels in US, each 22 MHz wide (实际 20+2)。**Three orthogonal channels: 1, 6, 11**。每个 channel 中心频率相差 5 MHz，但 22 MHz 宽 → 大部分重叠。\n\n2400 MHz — Channel 1 (2412) — Channel 6 (2437) — Channel 11 (2462) — 2483.5 MHz。",
  "key_points": [
    "美国 802.11b: 11 channels (2412-2462 MHz)",
    "每 channel 22 MHz",
    "**Non-overlapping: 1, 6, 11**",
    "AP 部署常用 1/6/11 交错"
  ],
  "explanation": "**为什么只有 3 个不重叠**：\n- Channel 编号 1, 2, ..., 11 中心频率相差 5 MHz\n- 但每 channel 22 MHz 宽\n- Ch 1 占 2401-2423 MHz\n- Ch 2 占 2406-2428 MHz → 跟 1 大量重叠\n- Ch 6 占 2426-2448 MHz → 跟 1 不重叠（差 25 MHz）\n- Ch 11 占 2451-2473 MHz → 跟 6 不重叠\n\n所以只有 **1, 6, 11** 三个不会互相干扰。\n\n**5 GHz 优势**：5 GHz 有 20+ 个不重叠 channel，所以高密度场景（写字楼、机场）优先用 5 GHz。\n\n**考点**：『为什么 WiFi AP 部署常配 1/6/11？』→ 只有这 3 个不重叠。",
  "gotcha": "其他国家 channel 数不同（欧洲 13, 日本 14），但都遵循『3 个不重叠』工程实践。"
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
    print(f"lec23 rewrite: overwrote {overwritten}, added {new}")

if __name__ == "__main__":
    main()
