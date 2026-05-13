# COMS 4119 — Final Review Notebook

一个为 Columbia COMS / CSEE 4119 Computer Networks 期末复习造的本地 Web app。

## 功能

- **逐页讲义浏览**：lec14–lec23 + final-preview，左边 PPT 原图，右边 AI 写的应试角度讲解（关键点 / 公式 / 易错点）
- **⭐ 收藏**：按 `S` 或工具栏按钮收藏重点页，集中列表里再回访
- **🧠 概念知识库**：102 节点力导向思维导图（vis-network），按层分色
- **📝 期中复盘**：左边原题 PDF，右边标准答案 + 失分点对照
- **🖨️ Cheat Sheet**：A4 双面、超紧凑、可直接打印
- **问 AI 助教**：每页右侧 Q&A 框，调 OpenAI Chat Completions，**问答保存到 localStorage**
- **状态记忆**：最后一个 tab + 每个 PPT 的最后一页全部记住

## 运行

```bash
cd app
python3 server.py 8788
# 浏览器打开 http://localhost:8788
```

`server.py` 同时：
1. 用 `ThreadingHTTPServer` 提供静态文件
2. 把 `POST /api/ask` 转发给 OpenAI（API key 通过请求体传，前端存在 localStorage，不落盘）

## 文件结构

```
4119/
├── lec14.pdf .. lec23.pdf       # 期中后讲义
├── final-preview.pdf            # 老师给的样题
├── midoriginoutput.pdf          # 期中原题
├── submission_396807124.pdf     # Gradescope 评分
└── app/
    ├── index.html / app.js / style.css
    ├── cheatsheet.html          # A4 双面 cheat sheet
    ├── server.py                # 静态 + OpenAI proxy
    ├── data/
    │   ├── explanations.json    # 330 页 AI 讲解（auto-built）
    │   ├── explanations_detail.json  # 详细 override
    │   ├── finalpreview.json    # 5 道样题逐题精讲
    │   ├── midterm.json         # 7 道期中题标答
    │   ├── concepts.json        # 概念思维导图数据
    │   └── build_explanations.py     # 重建脚本
    ├── pages/                   # 各 PDF 转的 JPG（每页一张）
    └── cheatsheet-assets/       # cheat sheet 用的图
```

## 重新生成 AI 讲解 JSON

改完 `explanations_detail.json` 后：

```bash
python3 app/data/build_explanations.py
```

## 期末日期

2026-05-14 (考前一晚 ✊)
