#!/usr/bin/env python3
"""Deepen lec23 explanations: teach-a-beginner style.

Each entry gets a much richer `explanation` field (markdown) covering:
1. 直觉/动机 — why we care
2. 机制 — what's actually happening
3. 例子 — concrete numbers
4. 易错点 / 陷阱
5. 考法 — how it'll be tested

Run:
    python3 rewrite_lec23.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DETAIL = ROOT / "explanations_detail.json"

NEW = {

"lec23:1": {
  "title": "Reflection（反射）— 三种传播现象之一",
  "summary": "电磁波撞到比波长大很多的表面（地面、墙、车体）会反射出去，方向改变但能量基本保留。",
  "key_points": [
    "判定条件：物体尺寸 ≫ 波长 λ",
    "WiFi 2.4 GHz: λ≈12 cm；5 GHz: λ≈6 cm。墙、地面、家具都算『大』",
    "反射不消耗信号 → 接收端会同时收到直达 + 多条反射 → 引出 multipath",
    "可以利用：金属罐做反射器聚焦 WiFi"
  ],
  "explanation": "### 为什么要学三种传播现象？\n无线信号不像有线一样『沿电缆走』，它在空气里到处弹。理解信号怎么从 sender 到 receiver，是后面 multipath、fading、隐藏/暴露终端、CSMA/CA 设计的基础。\n\n### 反射的物理直觉\n你拿手电筒照镜子，光会被反射回来。无线电波本质就是高频电磁波，碰到导体或大平面（相对自己的波长而言）就反弹。\n\n**判定『大』的尺度**：波长 λ。\n- 频率 f 越高，λ 越小：c = λf，c = 3×10⁸ m/s\n  - 2.4 GHz: λ = 3×10⁸ / 2.4×10⁹ ≈ **0.125 m = 12.5 cm**\n  - 5 GHz: λ ≈ **6 cm**\n  - 900 MHz: λ ≈ **33 cm**\n- 一面墙（几 m 宽）≫ 12 cm → 反射；一片树叶（10 cm）跟 λ 差不多 → 散射（后面讲）\n\n### 反射的后果\n直达路径 + 反射路径同时到达接收端 → **multipath**。这是后面 fading、ISI、coherence time 的根源。\n\n### 易记的反例\n讲义里有个梗：把啤酒罐剪开放路由器后面增强 WiFi —— 金属罐反射 + 几何聚焦，像抛物面天线。\n\n### 考法\n选择题 / 简答：『哪种传播现象主要由墙、地面引起？』→ 反射。或者反过来：『为什么 WiFi 在屋里到处都能收到？』→ 反射 + 衍射的组合。",
  "gotcha": "**别和『散射』混淆**：反射是大面镜面反射方向集中；散射是小物体把信号散成各方向。判定靠 **物体尺寸 vs 波长** 的比较，不是『硬不硬』。"
},

"lec23:2": {
  "title": "Diffraction（衍射 / 阴影绕射）",
  "summary": "波遇到锐利不规则边缘时会『绕过去』，使阴影区也能收到信号（虽然弱）。",
  "key_points": [
    "判定条件：物体有锐利边",
    "结果：即使没有直视路径（LOS）也能通信",
    "信号强度比 LOS 弱，但不为零",
    "WiFi 能穿墙拐角靠的就是这个"
  ],
  "explanation": "### 直觉\n站在大楼背面接电话，你和基站之间根本没有直线视野，为什么还能通话？因为电磁波在楼角边缘『绕了一下』就进了你这边的阴影区。这就是衍射。\n\n### 物理（不用深究）\n惠更斯-菲涅耳原理：波前上每一点都可以看作新的波源。碰到锐利边时，这些『次波源』会发射进几何阴影区，相当于波被『重新发射』并绕过障碍。\n\n### 跟反射的区别\n| | 反射 | 衍射 |\n|---|---|---|\n| 触发 | 大面镜面 | 锐利边缘 |\n| 方向 | 镜像反射方向 | 弯曲进阴影 |\n| 强度 | 接近原信号 | 比 LOS 弱很多 |\n\n### 后果\n你能用 WiFi 在墙角后面收到信号；蜂窝基站不需要每户都看见就能服务整个街区。\n\n### 考法\n看到关键词『**no LOS**』『绕过障碍』『锐利边』→ 选衍射。",
  "gotcha": "衍射不等于反射。题目说『信号绕过书架边缘到达接收端』→ **衍射**。说『信号撞到地板后到达』→ **反射**。"
},

"lec23:3": {
  "title": "Diffraction 图示",
  "summary": "形象展示波在锐利边缘的『绕射』。",
  "key_points": ["阴影区也能收到信号", "通常比 LOS 弱", "WiFi 室内典型"],
  "explanation": "这页只是图示，关键已经在前一页讲清。看图记住：信号源 → 障碍物 → 障碍物后面阴影区也能收到（比 LOS 路径弱但可解码）。"
},

"lec23:4": {
  "title": "Scattering（散射）",
  "summary": "波碰到小于波长的物体（树叶、灯柱、路标）时被散成多个方向，最难建模。",
  "key_points": [
    "判定：物体尺寸 < λ",
    "波被分散到很多方向",
    "数学上最难精确预测",
    "野外测量比纯计算可靠"
  ],
  "explanation": "### 直觉\n反射像镜子（大平面），衍射像门缝（边缘），**散射像把球扔进一堆小石子**（小物体）—— 球弹出去后方向乱七八糟。\n\n### 例子（题目可能问的）\n- WiFi 信号穿过盆栽 → 树叶尺寸跟 λ 接近 → 散射\n- 路过的小路标、灯柱 → 散射\n- 雨滴对高频毫米波（5G）→ 散射（这就是为什么毫米波雨天衰减大）\n\n### 三个一起记忆（必考）\n```\n     物体尺寸\n        ≫ λ   →  Reflection（反射）\n        锐边  →  Diffraction（衍射）\n        < λ   →  Scattering（散射）\n```\n\n### 为什么难建模\n散射方向是统计性的，跟物体形状、材质、几何分布都有关，没法用单一公式表达 → 实际部署 WiFi/蜂窝靠测量，不靠纯计算。",
  "gotcha": "考题给场景判断三种现象时，**先看物体尺寸跟 λ 比**。墙、地面是大物体 → 反射；树叶、路标是小物体 → 散射；锐利边角 → 衍射。"
},

"lec23:5": {
  "title": "Multipath Fading（多径衰落）⭐",
  "summary": "信号从多条路径到达接收端，路径长度不同 → 相位不同 → 叠加可能相消或相长，导致信号忽强忽弱。",
  "key_points": [
    "多条路径：LOS + 反射 + 衍射",
    "路径差 → 时间延迟差 → 相位差",
    "Mobility 让相位关系实时变化 → 信号波动",
    "Large-scale fading: 随距离平均衰减",
    "Small-scale fading: 小范围内剧烈跳动（multipath 干涉）"
  ],
  "explanation": "### 为什么会这样？\n想象两个人同时朝水池里扔石头：水波相遇时，**波峰对波峰 → 加强**，**波峰对波谷 → 抵消**。电磁波一样。\n\n两条路径长度差 Δd → 信号到达接收端的时间差 Δt = Δd/c → 相位差 Δφ。如果 Δφ = π（半个波长差），两条路径的信号正好相消 → 接收端几乎收不到信号（深 fade）。\n\n### 大尺度 vs 小尺度\n**Large-scale fading**：随距离平均衰减（path loss 公式那一套）。距离从 1m 走到 10m，信号能衰 20 dB，这是『慢』变化。\n\n**Small-scale fading**：在一两个波长（10-20 cm）的范围内信号能跳动 30 dB。**接收端动 几 cm，信号强度可能瞬间从 -40 dBm 变 -70 dBm**。\n\n### Mobility 的角色\n你走路时，每个反射路径的长度都在变 → 相位关系实时改变 → 干涉模式动态变 → 信号波动。**这就是为什么开车时手机信号忽满格忽 1 格**。\n\n### 即使静止也会 fade\n你不动，但屋里有人走过、空调风扇转 → 反射体在动 → multipath 关系变 → 信号仍波动。\n\n### 考法\n『为什么静止节点接收信号还会随时间变化？』→ 环境物体动 → multipath 改变。\n\n『large vs small scale fade 的区别？』→ 时间/空间尺度 + 成因（pathloss 平均衰减 vs multipath 干涉）。",
  "gotcha": "**Mobility 主要导致小尺度 fading**（不是大尺度，大尺度是距离决定的）。"
},

"lec23:6": {
  "title": "Multipath — Coherence Time（相干时间）",
  "summary": "信道脉冲响应保持不变的最大时间。Symbol period 必须 ≤ coherence time 才能正确解码。",
  "key_points": [
    "**Tc** = coherence time = 信道『稳定』的窗口",
    "Symbol period > Tc → ISI（符号间干扰）→ 解码失败",
    "Mobility 越大 → Tc 越小（信道变化越快）",
    "限制最大 symbol rate"
  ],
  "explanation": "### 关键直觉\n想象你跟人说话，每句话之间有 1 秒间隔。如果你说完一句后房间立刻变成另一个空间（回声完全变了），第二句就跟第一句的余音搅在一起 → 听不清。\n\n无线信道也这样。一个 symbol（比如一个 bit）从 sender 经过多径到 receiver，会有多个延迟拷贝（直达 + 反射 + ...）。这些拷贝在时间上拖了个『尾巴』。如果你下一个 symbol 来得太早，**上一个 symbol 的尾巴还没散完，两个 symbol 就重叠** → ISI（Inter-Symbol Interference）。\n\n### Coherence time 的具体含义\nTc = 信道脉冲响应（impulse response）从一个状态变到显著不同的另一个状态所需时间。\n\n**Symbol period T_s 的约束**：T_s 不能比信道变化时间还慢，否则发送的同时信道已经变了样。\n\n更直接地说：**T_s ≤ Tc** 才能保证一个 symbol 期间信道稳定，能解码。\n\n### 数值感觉\n- 室内 WiFi 静止：Tc ≈ 几十 ms\n- 开车（30 m/s）：Tc 显著下降到 ms 级\n- 高铁 / 飞机：Tc 更短\n\n所以高速移动场景需要更短的 symbol period（更高 symbol rate？不是，**反过来**——更短的 symbol 让你能跟得上信道变化）。\n\n### 考法\n『为什么 multipath 限制最大 symbol rate？』\n答：multipath 使一个 symbol 在接收端被拖成多个延迟副本，下一个 symbol 必须等前一个的余音散完，否则 ISI；这个『散完时间』就是 coherence time，决定 symbol period 下限。",
  "gotcha": "Coherence time 不是『一个 symbol 持续多久』，是『信道脉冲响应保持不变的时间』。两者关系是 symbol period **≤** coherence time。"
},

"lec23:7": {
  "title": "SNR / SINR — 衡量信号质量",
  "summary": "SNR = 信号/噪声；SINR 还要扣除其他发射机的干扰。dB 形式 = 10·log₁₀。",
  "key_points": [
    "**SNR (Signal-to-Noise Ratio)**：只考虑热噪声",
    "**SINR (Signal-to-Interference-plus-Noise Ratio)**：还加邻居发射的干扰",
    "都是 **dB**: 10·log₁₀(比值)",
    "SNR 高 → BER（bit error rate）低 → 可用更高 modulation/code rate",
    "这是 rate adaptation 的依据"
  ],
  "formula": "$$\\mathrm{SNR}_{dB} = 10 \\log_{10}\\frac{S}{N}, \\quad \\mathrm{SINR}_{dB} = 10 \\log_{10}\\frac{S}{N+I}$$",
  "explanation": "### dB 是什么？为什么用它？\n信号强度跨度非常大（发射 1 W = 30 dBm，接收 1 nW = -60 dBm，比值 10⁹），用线性单位读不下来。dB 是对数刻度：\n- 比值 ×10 = +10 dB\n- 比值 ×2 ≈ +3 dB\n- 比值 ÷10 = −10 dB\n\n所以 SNR=20 dB 意味着信号比噪声大 100 倍。\n\n### SNR 怎么影响 bit rate\n香农极限：C = B·log₂(1+SNR)。**SNR 高 → 同样带宽下能传更多 bit**。\n\n实际中 WiFi/蜂窝用 **rate adaptation**：\n- SNR 高 → 用 64-QAM、5/6 码率 → 高数据率\n- SNR 中 → 用 QPSK、1/2 码率\n- SNR 低 → 用 BPSK、1/3 码率（保守，求别出错）\n\n### SNR vs SINR\nSNR 只考虑热噪声（背景），SINR 还加上 **邻居发射机的干扰**。\n- 单一发射场景 → SNR 够用\n- 密集部署（office、会议中心多 AP）→ 必须考虑 SINR\n\n### 例题\n信号 S = -50 dBm, 噪声 N = -90 dBm。\nSNR_dB = (-50) - (-90) = **40 dB**（dB 减法就是 dB 比值）。\n\n### 考法\n- 给数值算 SNR/SINR\n- 解释为什么 5GHz 比 2.4GHz 在远处 SNR 低（pathloss 更高）\n- 说明 SNR 跟 BER 的关系",
  "gotcha": "dB 单位下不能直接『加』信号强度，要先转线性单位。但 **SNR_dB = S_dB − N_dB**（因为 dB 是对数，比值变减法）。"
},

"lec23:8": {
  "title": "Received Signal Over Time — 实际接收的信号到底什么样",
  "summary": "图示展示实际信号在时间维度的剧烈波动（multipath + mobility 综合效果）。",
  "key_points": [
    "信号 dB 跳几十 dB",
    "即使静止也会变（环境物体动）",
    "无线信道是『统计的』，不是确定的",
    "建模通常给均值 + 方差"
  ],
  "explanation": "### 这页要传达的核心\n**无线信道不像有线信道是『一根管子一直畅通』**。它是个会自己抖动、变形、消失再回来的连续随机过程。\n\n下次实验 / 项目中遇到 WiFi 不稳定，不是 bug，是物理。\n\n### 为什么对网络设计重要\n- TCP 在无线下会被 fade 误判为拥塞 → 错误减半 cwnd\n- 视频码率自适应必须容忍突发 fade\n- 蜂窝基站调度算法依赖 channel state info (CSI) feedback"
},

"lec23:9": {
  "title": "Simulating Wireless Environment — 实际工程怎么建模",
  "summary": "用 PL(d) = PL(d₀) + 10α·log(d/d₀) + X，α 是环境相关的『pathloss exponent』。",
  "formula": "$$PL(d) = PL(d_0) + 10\\alpha\\log\\left(\\frac{d}{d_0}\\right) + X$$",
  "key_points": [
    "α = pathloss exponent，决定衰减速度",
    "X = log-normal 随机阴影项（shadowing）",
    "d₀ = 参考距离（通常 1 m）"
  ],
  "explanation": "### 为什么要这个公式？\n自由空间公式 `L = (4πdf/c)²` 假设没有障碍物，**只在外太空准确**。地面上有墙、家具、树木、人，实际衰减比公式快得多。\n\n### α 的物理意义\nα 描述『多快地衰减』：\n- α = 2 → 自由空间（每加倍距离，功率减 6 dB）\n- α = 3 → 城市（每加倍，−9 dB）\n- α = 5 → 室内多墙（每加倍，−15 dB）\n\n### α 典型值表（记一下）\n| 环境 | α |\n|---|---|\n| 自由空间 | 2 |\n| 城市蜂窝 | 2.7 – 3.5 |\n| 城市阴影 | 3 – 5 |\n| 室内阻挡 | 4 – 6 |\n| 工厂阻挡 | 2 – 3 |\n\n### X 是什么\nX 是随机变量（典型 log-normal 分布），代表『同一距离上不同位置的随机变化』。两个人都在 AP 10 m 远，一个站走廊里、一个在房间深处，信号能差 10 dB → 这就是 X 起作用。\n\n### 例题\nd₀=1m，PL(d₀)=40dB，α=3，d=10m：\nPL(10) = 40 + 10×3×log(10/1) + X = 40 + 30·1 = **70 dB + 随机阴影**。\n\n### 考法\n- 给参数算 PL\n- 解释为什么室内信号衰得比公式快 → α 高\n- 选择题：城市蜂窝 α 多少？→ 2.7-3.5"
},

"lec23:10": {
  "title": "Wireless vs Wired — 两大根本差异 ⭐⭐",
  "summary": "无线相对有线有两个本质区别：信道时变 + 广播干扰。这是后面所有 wireless MAC 设计的根源。",
  "key_points": [
    "**Time-varying, unpredictable**：mobility + 环境物体动 + multipath",
    "**Interference（广播本质）**：邻居发射会互相干扰",
    "这两条决定了：需要 rate adaptation、需要 MAC 协议、需要错误恢复"
  ],
  "explanation": "### 为什么这页这么重要\n如果你能记住这两条，你能推出整个 wireless MAC 章节的设计动机：\n\n**1. Time-varying channel** → 需要 rate adaptation\n- 信号强度不停变 → modulation/code rate 也得跟着变\n- 接收端做 channel estimation 反馈给发送端\n\n**2. Broadcast 介质 → interference**\n- 一个频段同一时刻只能有一个发送（否则碰撞）\n- 必须有协议决定『谁发』→ MAC 协议\n- 而且接收端干扰由 sender 看不见的人造成（hidden terminal）→ MAC 设计很难\n\n### 跟有线对比\n| | 有线 | 无线 |\n|---|---|---|\n| 信道 | 稳定 | 时变 |\n| 介质 | 独占 | 广播 |\n| Bit error rate | 极低（~10⁻¹²） | 可能 10⁻³ |\n| 半 / 全双工 | 全双工 | 通常半双工 |\n| 碰撞检测 | 容易 | **不可能**（耳朵被自己淹）|\n\n### 这一页几乎一定考\n『为什么 wireless MAC 比 wired MAC 难设计？』→ 必答这两条：信道时变 + 广播干扰。\n\n『为什么无线下 TCP 表现差？』→ time-varying + bit error 高 → 丢包不一定意味着拥塞。",
  "gotcha": "考试时『为什么 wireless 难』不要只答一条。**两条都要答到** + 各举一个具体后果。"
},

"lec23:11": {
  "title": "Wireless MAC Protocols — 章节封面",
  "summary": "从物理层进入 MAC 层。"
},

"lec23:12": {
  "title": "The More, The Messier — 多节点意味着冲突",
  "summary": "多节点同发会碰撞，需要 MAC 协议协调。",
  "explanation": "**核心问题**：广播媒介下，多个节点同时发送 → 接收端看到的信号是叠加的乱码 → 谁的包都解不出来 → 都得重传。\n\nMAC 协议就是『谁能在什么时候发』的分布式仲裁机制。"
},

"lec23:13": {
  "title": "Role of MAC — 三大职责",
  "summary": "无线 MAC 要做三件事：rate adaptation、避免干扰、保证公平。",
  "key_points": [
    "**Rate adaptation**：根据信道质量选 modulation",
    "**Avoid interference**：碰撞避免",
    "**Fairness**：让多节点公平共享"
  ],
  "explanation": "### 为什么 wireless MAC 比 wired 多了一件事\n有线 MAC（比如 Ethernet CSMA/CD）只管『谁能发』。\n\n无线 MAC 还要管 **rate adaptation**：因为信道时变，sender 要根据当前 SNR 选合适的 bit rate。\n\n### 三个目标的潜在冲突\n- 极致 fairness（所有人等量带宽）→ 信道好的节点也不能多用\n- 极致 throughput（最优节点先发）→ 弱节点 starve\n- 802.11 折中：DCF 让节点机会均等（fair），但允许 rate adaptation\n\n### 考法\n『wireless MAC 的目标？』必答三点。"
},

"lec23:14": {
  "title": "MAC Categories — 三大类 ⭐",
  "summary": "Centralized BS / Controlled access / Random access — 现代无线主要用 random access (CSMA/CA)。",
  "key_points": [
    "**Centralized (BS)**：基站调度（TDMA/FDMA/CDMA，蜂窝）",
    "**Controlled access**：token、polling",
    "**Random access**：ALOHA、CSMA/CD（有线）、CSMA/CA（无线）"
  ],
  "explanation": "### 三类对比\n\n| | Channel partition | Taking turns | Random access |\n|---|---|---|---|\n| 例子 | TDMA, FDMA, CDMA | polling, token | ALOHA, CSMA |\n| 谁说了算 | 中央分配 | 顺序传 | 自己抢 |\n| 碰撞 | 无 | 无 | 可能 |\n| 轻负载 | 浪费时隙 | overhead | 高效 |\n| 重负载 | 满载高效 | 满载高效 | 碰撞多 |\n| 单点故障 | BS 挂全瘫 | master 挂瘫 | 没有 |\n\n### 应用场景\n- 蜂窝 4G/5G：channel partition（基站集中调度，TDD/FDD + OFDMA）\n- WiFi：random access (CSMA/CA)\n- Bluetooth：polling-based\n- 早期 Ethernet：random access (CSMA/CD)\n\n### 考法\n『把下列协议归类』『轻负载下哪类最优？』→ random（partition 还在等自己时隙浪费）。",
  "gotcha": "蜂窝是 **centralized** （基站说了算），WiFi 是 **random access** （没有 AP 控制谁先发，每个节点自己竞争）。"
},

"lec23:15": {
  "title": "Three Wireless Ranges — Transmission / Interference / Carrier sensing",
  "summary": "每个无线节点有三个圆圈：能解码的范围 < 能干扰的范围 < 能感知的范围。",
  "key_points": [
    "**Transmission range**：能正确解码的距离",
    "**Interference range**：能造成显著干扰但解不了的距离",
    "**Carrier sensing range**：能检测到能量但不一定解码的距离",
    "三者关系：Transmission < Interference < Carrier sensing"
  ],
  "explanation": "### 为什么会有三个范围\n信号强度随距离衰减。在 sender 周围，距离从近到远：\n\n1. **近**（高 SNR）→ 能解码所有内容 = transmission range\n2. **中**（SNR 较低，解不出但能量明显）→ 干扰别人接收 = interference range\n3. **远**（SNR 更低，但能量还检测得到）→ carrier sense 能检测，但解不出 = carrier sensing range\n\n### 数值感觉\n典型 WiFi：\n- Transmission: 30 m\n- Interference: 70 m\n- Carrier sensing: 100 m\n\n### 为什么这页重要\n后面 **hidden / exposed terminal** 的判定就靠这三个范围：\n- **隐藏**：X 在 A 的 sensing range **外**，但在 B 的 interference range **内**\n- **暴露**：X 在 A 的 sensing range **内**，但自己目标在 A 的 interference range **外**\n\n### 考法\n给一张图（圆圈表示 sensing range），让你判断 X 是不是 hidden 或 exposed。",
  "gotcha": "三个范围的层次：**carrier sensing 最大 > interference > transmission 最小**。别记反。"
},

"lec23:16": {
  "title": "CSMA — Carrier Sense Multiple Access ⭐",
  "summary": "发送前先 carrier sense（监听信道）。信道闲就发，忙就等。仍可能碰撞（传播延迟）。",
  "key_points": [
    "Sender 监听信道",
    "Idle → 发",
    "Busy → 退让到 idle",
    "仍可能碰：propagation delay 期间多人都觉得 idle",
    "**Sender-driven**: 决策只看自己听到什么"
  ],
  "explanation": "### CSMA vs ALOHA\n- ALOHA：盲发（不听），碰了重试\n- CSMA：**先听后说**（至少减少不必要的碰撞）\n\n### 工作流程\n```\n想发？\n  ↓\n监听信道\n  ↓        ↓\nIdle      Busy\n  ↓        ↓\n发送    等到 idle\n```\n\n### 为什么 CSMA 还会碰撞？\n**传播延迟**。A 在 t=0 开始发，信号要 d/c 秒才能传到 B。在这 d/c 秒内 B 监听信道仍是 idle，于是 B 也开始发 → 在中间某处碰撞。\n\n所以 CSMA 减少碰撞但不能完全消除。**有线**：A 边发边听，能立刻发现碰撞（CSMA/CD）；**无线**：自己发的时候耳朵被淹听不到别人，必须用别的办法（CSMA/CA）。\n\n### Sender-driven 的关键问题（下一页讲）\nCSMA 是 sender 决定『信道闲不闲』，但实际碰撞发生在 receiver 那边。Sender 看到的『闲』不代表 receiver 那边也闲。\n\n### 考法\n『为什么 CSMA 仍会有碰撞？』→ propagation delay 期间多人都觉得信道闲。\n\n『CSMA 在无线下不够用，为什么？』→ 隐藏终端，sender-driven vs receiver-driven 错配。"
},

"lec23:17": {
  "title": "Discussion Time — CSMA 够了吗？",
  "summary": "课堂问题，引出下一页的核心 insight。"
},

"lec23:18": {
  "title": "CSMA 不够的根本原因 — Sender vs Receiver 错配 ⭐⭐",
  "summary": "CSMA 是 sender 听自己附近的载波，但**干扰发生在 receiver 端**。Sender 听到 idle 不等于 receiver 那边没人在发。",
  "key_points": [
    "Sender 监听是『自己周围』",
    "干扰发生在 **receiver** 处",
    "Sender 看不到 receiver 周围谁在发 → 漏洞",
    "这就是 hidden terminal 的本质"
  ],
  "explanation": "### 这一页是 wireless MAC 的核心 insight\n\n**有线下**：A、B 通过电缆物理连接，A 处的载波检测 = B 处的载波检测（信号沿着电缆走）。所以 sender 听到 idle = 整条线 idle，能安全发。\n\n**无线下**：A 和 B 通过空气（不同的物理介质区域）。A 监听『A 周围』，B 接收时看『B 周围』。**两者范围可以完全不重叠**。\n\n```\n[A]---listens around A---     ---around B---[B]\n                            ^\n                这里有个 C 在发，A 听不到，但会干扰 B\n```\n\n### 解药：让 receiver 也参与协调\nCTS（Clear-to-Send）由 receiver 发出，**告诉自己周围的人『我接下来要收数据，请安静』**。这样即使 sender 听不到 C，C 听到 CTS 后也会安静。\n\n这就是 RTS/CTS 解隐藏终端的核心。\n\n### 考法\n『CSMA 在无线下为什么不够？』必须答到 sender vs receiver 的不对称。\n\n『RTS/CTS 怎么解决这个问题？』→ 让 receiver 主动广播自己附近的『安静』信号。",
  "gotcha": "**别只说『因为隐藏终端』** — 老师要的是 deeper reason: sender-driven detection 跟 receiver-side interference 不匹配。"
},

"lec23:19": {
  "title": "Hidden Terminal Problem（隐藏终端）⭐⭐⭐",
  "summary": "C 在 sender A 范围外（听不到 A），但在 receiver B 干扰范围内 → C 觉得信道闲就发 → B 处碰撞。",
  "key_points": [
    "**判定**：X 在 A 的 sensing range **外**（X 听不到 A），且 X 在 B 的干扰范围 **内**",
    "症状：A 自己觉得发得好好的，但 B 收不到（碰撞在 B 处发生）",
    "**解药**：CTS（B 发 CTS 给自己附近所有节点说『安静』）"
  ],
  "explanation": "### 场景\n```\n           A 的范围\n         ┌─────────┐\n         │   A───▶ B │\n         └─────────┘ \n                     C\n             ↑\n          C 在 A 范围外，听不到 A\n          但 C 能干扰 B\n```\n\n### 步骤还原\n1. A 想发数据给 B\n2. A 监听信道：idle（C 当前没发，没干扰 A）\n3. A 开始发\n4. **同时** C 监听信道：也是 idle（A 不在 C 范围内，C 听不到 A）\n5. C 觉得能发，开始发\n6. A 和 C 的信号在 B 处碰撞 → B 收不到\n7. A 不知道（自己听到的是 idle），以为发成功\n8. ACK 没回来，A 才知道丢了\n\n### 判定方法（必背）\n- X 在 sender A 的 sensing range **外**？✓ → 第一个条件\n- X 能干扰 receiver B（在 B 的 interference range 内）？✓ → 第二个条件\n- 两个都满足 → X 是 hidden\n\n### 解药 RTS/CTS\n- A 先发 RTS（Request-to-Send）给 B\n- B 回 CTS（Clear-to-Send），CTS 携带 NAV（接下来要占用多久）\n- **B 周围所有节点（包括 C）听到 CTS** → 在 NAV 时间内静默\n- 即使 C 听不到 A，也听得到 B 的 CTS，所以不会干扰\n\n### 期末样题 Q5 / final-preview\n4 节点 A、B、C、E，A→B 通信。C 和 E 都听不到 A 但能干扰 B → C 和 E 都是 hidden terminal。\n\n### 考法\n- 给一张图（圆圈表示范围），让你识别 hidden\n- 解释机制\n- 解释 RTS/CTS 怎么解",
  "gotcha": "**判定方向**：sender 外 + receiver 内。**别记反**。考前默写一遍判定条件。"
},

"lec23:20": {
  "title": "Exposed Terminal Problem（暴露终端）⭐⭐⭐",
  "summary": "C 听到 sender A 发包就抑制自己，但 C 的目标在 A 范围外（不会被 A 干扰）→ 浪费了并发机会。",
  "key_points": [
    "**判定**：X 在 sender A 的范围 **内**（听得到 A）",
    "且 X 的目标 receiver 在 A 的范围 **外**（不会被 A 干扰）",
    "症状：本可并发但被 CSMA 抑制",
    "**RTS/CTS 不能解暴露终端**"
  ],
  "explanation": "### 场景\n```\n         A 的范围\n       ┌────────────┐\n       │   C─▶D     │\n       │   ▲        │\n  E───▶│   │        │\n       │   A────▶B  │\n       └────────────┘\n                D 在 A 范围外\n```\n\n### 步骤还原\n1. A 正在发数据给 B\n2. C 监听信道：busy（C 在 A 范围内，听到 A）\n3. CSMA 让 C 退让\n4. **但是！** C 想发给 D，D 在 A 范围外，A 的发射根本到不了 D → C 和 A 同时发不会在任何 receiver 处碰撞\n5. C 退让等同于浪费并发机会\n\n### 判定方法（必背）\n- X 在 sender A 的 sensing range **内**？✓\n- X 的 receiver 在 A 的 sensing range **外**？✓\n- 两个都满足 → X 是 exposed\n\n### 为什么 RTS/CTS 不能解\nC 听到 A 的 RTS 仍然要静默（按协议）。即使 C 知道自己想发给 D（A 干扰不到的人），协议机械执行『听到 RTS 就静默 t_CTS』。\n\n### 对比记忆 hidden vs exposed\n| | Hidden | Exposed |\n|---|---|---|\n| X 跟 sender A 的关系 | 在 A 范围**外** | 在 A 范围**内** |\n| X 跟 receiver B 的关系 | 在 B 干扰范围**内** | X 自己的 receiver 在 A 范围**外** |\n| 症状 | 该停没停 → 碰撞 | 该发没发 → 浪费 |\n| 802.11 解法 | CTS 解 | 没解 |\n\n### 期末样题 Q5\nA→B 通信，C、E 节点。判定 C、E 都听不到 A（在 A 范围外）→ 都是 hidden。没节点同时满足『在 A 范围内 + 自己目标在外』→ **无暴露终端**。\n\n### 考法\n- 判断哪些节点是 hidden / exposed\n- 解释为什么 RTS/CTS 解 hidden 不解 exposed\n- 描述各自的『后果』（碰撞 vs 浪费）",
  "gotcha": "**Hidden 和 exposed 的判定方向正好相反**。记忆抓手：『隐藏 = 隐身没看见，该停没停 → 撞』；『暴露 = 暴露在视野里，该发不敢发 → 亏』。"
},

"lec23:21": {
  "title": "如何应对 hidden terminal — 两条思路",
  "summary": "Solution #1：避碰（busy tone / RTS-CTS）。Solution #2：处理碰撞（ZigZag decoding）。"
},

"lec23:22": {
  "title": "Solution #1: Busy Tone（避碰）",
  "summary": "Receiver 在收数据时广播 busy tone，听到的所有节点静默。",
  "key_points": [
    "Receiver 主动告诉周围『我在收数据』",
    "需要双信道（数据 + tone）",
    "硬件复杂，早期 802.11 不采用",
    "后来被 RTS/CTS 取代"
  ],
  "explanation": "### 思想\n隐藏终端的本质是 sender 无法替 receiver 喊话。busy tone 让 **receiver 自己喊话**：『我正在收数据，安静！』。\n\n### 为什么没普及\n- 需要专用 busy tone 信道（频段）\n- 硬件实现复杂\n- 实际部署不实用 → 让位给 RTS/CTS"
},

"lec23:23": {
  "title": "Solution #1: MACA — RTS/CTS ⭐",
  "summary": "Sender 发 RTS，receiver 回 CTS。听到 RTS 的人静默 t_CTS（等 sender 收 CTS）；听到 CTS 的人静默 t_data（解 hidden）。",
  "key_points": [
    "MACA = Multiple Access with Collision Avoidance",
    "RTS (Request-to-Send) 先广播一个短包",
    "Receiver 回 CTS (Clear-to-Send) 也短",
    "听到 RTS 的人静默短时间（让 CTS 能传过去）",
    "听到 CTS 的人静默 NAV 时长（保护数据）"
  ],
  "explanation": "### 完整序列\n```\n A → RTS → B          ← 听到 RTS 的人静默到 CTS 之后\n B ← CTS ← A          ← 听到 CTS 的人静默整个 data 时间（NAV）\n A → DATA → B\n B ← ACK ← A\n```\n\n### 为什么 RTS 之后还要 CTS\n仅 RTS 不够：只有听到 A 的人会静默，但 hidden terminal 听不到 A（这正是 hidden 的定义）。\n\n所以靠 CTS：CTS 由 B 发，B 周围所有节点（包括 hidden）都听得到。\n\n### 为什么用『短包』RTS/CTS 而不是直接发数据\n如果 RTS 跟别人碰撞，损失的只是 RTS 这点字节；数据本身没浪费。先用短包试水。\n\n### 缺点\n- RTS/CTS 本身有开销（短包，但每次都得发）\n- **不能解 exposed terminal**\n- 短帧场景（如 ACK）反而 RTS/CTS 开销大于收益，所以可选\n\n### 802.11 默认\nRTS/CTS 是 **optional**。一些实现只在帧 > 阈值时启用。\n\n### 考法\n- 解释 RTS/CTS 流程\n- 为什么 CTS 由 receiver 发（不是 sender 直接广播）\n- 为什么 RTS/CTS 解 hidden 不解 exposed",
  "gotcha": "CTS 必须由 receiver 发，不能由 sender 发。如果 sender 自己『预告』，隐藏终端听不到照样无效。"
},

"lec23:24": {
  "title": "RTS / CTS 实例",
  "summary": "图示 A→B 通信，C 和 D 通过听到 RTS/CTS 而静默。",
  "explanation": "图里 A 发 RTS 到 B，C 听到 RTS（C 在 A 范围内），D 听到 CTS（D 在 B 范围内）。两人都静默到 ACK 完成。"
},

"lec23:25": {
  "title": "802.11 MAC = CSMA/CA",
  "summary": "Carrier Sense + Collision Avoidance（不是 Detection）。无线版的 MAC。",
  "key_points": [
    "Carrier sense（物理 + 虚拟 NAV）",
    "Collision avoidance（不 CD，靠 random backoff + RTS/CTS）",
    "RTS/CTS 可选",
    "用 ACK 确认成功（无线丢包概率高）"
  ],
  "explanation": "### CSMA/CA vs CSMA/CD\n| | CSMA/CD（Ethernet） | CSMA/CA（WiFi） |\n|---|---|---|\n| Detect collision | 边发边听 | **做不到**（半双工，自己淹自己）|\n| Avoid collision | 一旦碰立刻 abort | 提前用 random backoff + 可选 RTS/CTS |\n| Recovery | abort + 重发 | 必须 ACK 确认；超时重发 |\n\n### 为什么无线不能 CD\n发射机和接收机在同一根天线上。**发自己的信号时，自己的能量比接收到的别人信号大 10⁹ 倍**，根本听不到别人。\n\n### CSMA/CA 核心三大件\n1. Physical CS（载波感知）\n2. Virtual CS（NAV，通过 RTS/CTS 包内字段）\n3. Random backoff（避碰）"
},

"lec23:26": {
  "title": "CSMA/CA 时序例子",
  "summary": "完整 4 步：RTS, CTS, DATA, ACK。中间夹 SIFS 间隔；周围节点根据 NAV 静默。"
},

"lec23:27": {
  "title": "CSMA/CA 三大机制拆解 ⭐",
  "summary": "Physical CS + Virtual CS + Collision Avoidance（random backoff）。",
  "key_points": [
    "**Physical CS**：测能量（energy detection）",
    "**Virtual CS**：解析 RTS/CTS 包内的 NAV 字段",
    "**Collision Avoidance**：random backoff"
  ],
  "explanation": "### 物理载波检测\n直接测信道能量，超过阈值就认为忙。\n\n### 虚拟载波检测 NAV\n RTS 和 CTS 的 header 里有 Duration 字段，说『接下来要占用多久』。其他节点解析这个字段，**自己维护一个倒数计时器 NAV (Network Allocation Vector)**。NAV > 0 时即使能量检测显示 idle，也认为忙。\n\n### 完整判断\n```\n物理 CS busy 或 NAV > 0 → 忙\n物理 CS idle 且 NAV = 0 → 闲\n```\n\n### 考法\n『CSMA/CA 有几种载波检测？』→ 物理 + 虚拟两种。\n『NAV 是什么？怎么维护？』→ 听到 RTS/CTS 后从 Duration 字段读，倒数到 0。"
},

"lec23:28": {
  "title": "Random Backoff（随机退避）⭐",
  "summary": "选 [0, CW] 内随机整数，每个 idle slot 减 1；信道忙就冻结。倒数到 0 才能发 RTS。",
  "key_points": [
    "CW = Contention Window 大小",
    "随机数 ∈ [0, CW]",
    "Medium idle → 倒数 −1",
    "Medium busy → 冻结",
    "倒数 = 0 → 发 RTS"
  ],
  "explanation": "### 为什么要随机退避\n如果两个节点都见信道忙，等到 idle 同时发 → 一定碰撞。\n\n各自随机选个等待时间 → 不同节点不同时刻发 → 概率上避碰。\n\n### Timeline 例子\nCW=31\n- 节点 1：随机选 25\n- 节点 2：随机选 20\n\n两人一起开始倒数，medium idle 时每个 slot 减 1。\n- 时刻 0: 节点 1=25, 节点 2=20\n- 时刻 20: 节点 2 到 0，开始发\n- 节点 1 看到 medium 忙，**冻结** 在 5\n- 节点 2 发完后，medium 闲下来\n- 节点 1 从 5 继续倒数（不重置！）\n\n这个『冻结 → 恢复』机制保证『等久了的节点优先』，避免同一波节点反复碰。\n\n### 考法\n给 timeline 题，要画对『冻结 → 恢复』的行为。常见错误：误以为每次 medium 闲下来就重选随机数。",
  "gotcha": "冻结时 backoff counter **保留**，不重新随机选。"
},

"lec23:29": {
  "title": "CSMA/CA 完整发送决策流程 ⭐",
  "summary": "Sense → DIFS → 闲 → 发；忙 → 等 idle + DIFS → backoff → 0 才发。回复用 SIFS（更短，优先）。",
  "key_points": [
    "**DIFS**（DCF Inter-Frame Space）≈ 50 μs：给新一轮竞争用",
    "**SIFS**（Short Inter-Frame Space）≈ 10 μs：给回复（CTS, ACK）用",
    "SIFS < DIFS 保证『回复』优先于『新对话』",
    "失败（无 CTS）→ CW × 2"
  ],
  "explanation": "### 详细步骤\n```\n1. 信道闲？\n     是 → 等 DIFS\n     否 → 等 idle\n\n2. 等 DIFS 后还闲？\n     是 → 发\n     否 → 启 random backoff\n\n3. 回复（CTS, ACK）：\n     等 SIFS（更短）直接发，不参与 contention\n```\n\n### 为什么 SIFS 短\n如果回复也等 DIFS，那别人在等的同时已经超过 DIFS 也开始竞争 → 回复跟新流量混在一起。**SIFS 故意比 DIFS 短**，保证一次对话内的所有回复优先级最高。\n\n### Timeline\n```\nA: --DIFS--RTS-----------DATA------\nB:        --SIFS--CTS--SIFS--ACK\nC:        ────── 静默 (NAV) ──────\n```\n\n### 考法\n看到题目里『DIFS vs SIFS 区别』→ 先问是不是回复包（CTS/ACK）。\n时间间隔分析题：能不能从 timeline 上看出哪个是 SIFS、哪个是 DIFS。"
},

"lec23:30": {
  "title": "怎么选 backoff CW 大小 — trade-off",
  "summary": "CW 太大 → 等太久浪费；CW 太小 → 容易碰。动态调整最好。"
},

"lec23:31": {
  "title": "802.11 DCF — Distributed Coordination Function",
  "summary": "DCF 通过碰撞情况动态调 CW：失败 → ×2，成功 → 重置。",
  "key_points": [
    "DCF = 默认 802.11 MAC 机制",
    "通过 binary exponential backoff 自适应"
  ]
},

"lec23:32": {
  "title": "Binary Exponential Backoff ⭐",
  "summary": "失败 → CW × 2（上限 CWmax）；成功 → CW = CWmin。",
  "key_points": [
    "CWmin = 31 (802.11b) / 15 (802.11g)",
    "CWmax 通常 1023",
    "n 次连续失败 → CW = min(CWmin · 2ⁿ, CWmax)"
  ],
  "explanation": "### 为什么 binary 指数增\n失败多 = 拥挤 → CW 应该大，让大家分散。Doubling 增长速度合适：\n- 失败 1 次 CW=63\n- 失败 2 次 CW=127\n- 失败 5 次 CW=1023\n\n### 问题：太激进重置\n一旦成功就立刻回 CWmin → 振荡 + 不公平：\n- 节点 A 经历多次失败 CW=1023，刚成功一次回到 31\n- 节点 B 一直成功，CW 始终 31\n- 平均看 A 等的时间是 B 的 16 倍 → 不公平\n\n### MACAW 改进\nMACAW: A Media Access Protocol for Wireless LAN's (SIGCOMM '94)\n- 成功 → CW −1（线性减）\n- 跟 binary exponential 类比 TCP AIMD\n\n### 考法\n- 给失败次数算当前 CW\n- 解释为什么 binary backoff 不公平\n- MACAW 怎么改进",
  "gotcha": "**别把 backoff 跟 cwnd 搞混**。Backoff 是 MAC 层的退避计数（slot 数），cwnd 是 TCP 层的滑动窗口（字节）。两个是不同层的概念，虽然都用 AIMD 思想。"
},

"lec23:33": {
  "title": "MACAW Solution — 指数增 + 线性减",
  "summary": "成功后 CW −1（线性减），跟 TCP CC AIMD 同思想。",
  "explanation": "### 思路\nTCP 的 AIMD：加法增、乘法减。MACAW 反过来：**指数增（碰撞）、线性减（成功）**。\n\n两者本质都是『失败时大幅退让，成功时谨慎进取』。\n\n### 跟 TCP CC 的关系\n方向：\n- TCP：cwnd 想 **变大**（吞吐），AI 增 + MD 减\n- MAC backoff：CW 想 **变小**（少等），ED 增 + LD 减\n\n概念一致，方向相反。"
},

"lec23:34": {
  "title": "Solution #2: Deal with Collisions — ZigZag",
  "summary": "不躲碰撞，直接从两次碰撞包里逐 chunk 解出原数据。",
  "explanation": "ZigZag (SIGCOMM 2008) 是一个学术上的方案：\n- 利用 802.11 的 retransmission + jitter（每次发的 timing 略不同）\n- 接收两次碰撞，每次 jitter 让 chunks 错位\n- 第一次干净的 chunk 1 + 第二次减去 chunk 1 解出 chunk 2 + ...\n\n实用层面没普及，但作为思路理解就好。"
},

"lec23:35": {
  "title": "ZigZag Decoding 详细",
  "summary": "Step 1 解第一次碰撞中干净的 chunk 1 → Step 2 从第二次碰撞减去 chunk 1 解 chunk 2 → ..."
},

"lec23:36": {
  "title": "802.11 标准家族 (b/a/g/n/ac)",
  "summary": "速度演进表 —— 重要的是 802.11n 引入 MIMO。",
  "key_points": [
    "**802.11b** (1999): 2.4 GHz, 11 Mbps, DSSS",
    "**802.11a** (1999): 5 GHz, 54 Mbps, OFDM",
    "**802.11g** (2003): 2.4 GHz, 54 Mbps, OFDM",
    "**802.11n** (2009): 2.4/5, ~600 Mbps, **MIMO** 多天线",
    "**802.11ac / WiFi 5** (2013): 5 GHz, >1 Gbps"
  ],
  "explanation": "### 关键拐点\n- **n** 引入 **MIMO**（多输入多输出）—— 用多根天线同时发不同流，throughput 跃升\n- **ac** 用更大的 channel 带宽 + 更高阶 MIMO\n\n### 数值不用死记\n考试一般问 **频段** 或 **大致速率**。记住：\n- 2.4 GHz: b/g/n (慢但穿墙好)\n- 5 GHz: a/n/ac/ax (快但短距)"
},

"lec23:37": {
  "title": "802.11 新一代标准 (af/ah/ax)",
  "summary": "白频段、低功耗 IoT、WiFi 6。",
  "key_points": [
    "**802.11af / White-Fi** (2014): TV 白频段 54-590 MHz, 1 km",
    "**802.11ah / Wi-Fi HaLow** (2017): 900 MHz, IoT, 低功耗",
    "**802.11ax / Wi-Fi 6** (2020): 14 Gbps, 密集场景优化",
    "都用 CSMA/CA"
  ]
},

"lec23:38": {
  "title": "802.11 LAN 架构 — Infrastructure vs Ad-hoc",
  "summary": "Infrastructure：通过 AP；Ad-hoc：host 直连，无 AP。",
  "key_points": [
    "**AP (Access Point)** = 基站",
    "**BSS (Basic Service Set)** = AP + 关联的 hosts",
    "Infrastructure mode = 通过 AP 互通",
    "Ad-hoc mode = 节点直接互通，没 AP",
    "**关联** 需要先 probe + authenticate"
  ],
  "explanation": "### 家用 WiFi = Infrastructure\n手机 / 笔记本通过 AP 上网。AP 同时连有线 (到 router) → 桥接 wireless 到 wired internet。\n\n### Ad-hoc 场景\n两台设备直接对连（如 AirDrop 早期 / WiFi Direct）。没有 AP，节点间直接 CSMA/CA。\n\n### 进入 BSS 的流程\n1. **Scan**：扫描看周围 AP（被动监听 beacon 或主动发 probe request）\n2. **Auth**：跟 AP 认证（早期 open / WEP，现代 WPA2/3）\n3. **Associate**：跟 AP 关联（AP 把你加入它的客户表）\n4. **Data**：开始通信"
},

"lec23:39": {
  "title": "802.11 信道分布 — 1, 6, 11 ⭐",
  "summary": "2.4 GHz 11 个信道，每个 22 MHz，只有 **1、6、11** 不重叠。",
  "key_points": [
    "美国 802.11b 11 个信道 (2412 - 2462 MHz)",
    "每信道 22 MHz 宽",
    "不重叠的三个：**1, 6, 11**",
    "AP 部署常用三色规划 (1/6/11 交错)"
  ],
  "explanation": "### 为什么只有 3 个不重叠\n信道编号 1, 2, 3, ... 11 每个中心频率相差 5 MHz，但每个信道 22 MHz 宽。所以：\n- Ch 1 占 2401-2423 MHz\n- Ch 2 占 2406-2428 MHz → 跟 1 大量重叠\n- Ch 6 占 2426-2448 MHz → 跟 1 不重叠（差 25 MHz）\n- Ch 11 占 2451-2473 MHz → 跟 6 不重叠\n\n所以只有 1、6、11 三个不会互相干扰。\n\n### 5 GHz 优势\n5 GHz 有 20+ 个不重叠信道，所以高密度场景（写字楼、机场）优先用 5 GHz。\n\n### 考法\n『为什么 WiFi AP 部署常用 1/6/11？』→ 因为只有这 3 个不重叠。",
  "gotcha": "其他国家信道数量不同（欧洲 13 个，日本 14 个），但都遵循『3 个不重叠』的工程实践。"
},

}

def main():
    data = json.loads(DETAIL.read_text())
    data.update(NEW)
    DETAIL.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"updated {len(NEW)} entries; total now {len(data)}")

if __name__ == "__main__":
    main()
