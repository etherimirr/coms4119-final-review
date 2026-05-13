// ============ Data registry ============
const FILES = [
  { id: 'lec14', label: 'lec14 · TCP 拥塞控制',  pages: 20 },
  { id: 'lec16', label: 'lec16 · Network 数据面', pages: 45 },
  { id: 'lec17', label: 'lec17 · 期中后续/IP',    pages: 28 },
  { id: 'lec18', label: 'lec18 · IPv6 · 路由协议',pages: 54 },
  { id: 'lec19', label: 'lec19 · BGP · OSPF',     pages: 25 },
  { id: 'lec20', label: 'lec20 · SDN · OpenFlow', pages: 44 },
  { id: 'lec21', label: 'lec21 · Data Link/MAC',  pages: 30 },
  { id: 'lec22', label: 'lec22 · 交换机 · 无线',  pages: 31 },
  { id: 'lec23', label: 'lec23 · 无线 MAC',       pages: 39 },
  { id: 'final-preview', label: 'final-preview · 样题',  pages: 14 },
];

const SPECIAL = [
  { id: 'overview',   label: '📚 总览',         pages: 0 },
  { id: 'stars',      label: '⭐ 收藏的重点',   pages: 0 },
  { id: 'final',      label: '🎯 Final Preview', pages: 14 },
  { id: 'midterm',    label: '📝 期中复盘',     pages: 4 },
  { id: 'concepts',   label: '🧠 概念知识库',   pages: 0 },
  { id: 'cheat',      label: '🖨️ Cheat Sheet',  pages: 0 },
];

// ============ Q&A (OpenAI proxy) ============
const KEY_OPENAI = '4119:openai_key';
const KEY_QA = '4119:qa';  // map "{fileId}:{page}" -> [{q, a, ts}]

function getApiKey() { return localStorage.getItem(KEY_OPENAI) || ''; }
function setApiKey(k) { localStorage.setItem(KEY_OPENAI, k); }

function loadQAMap() {
  try { return JSON.parse(localStorage.getItem(KEY_QA) || '{}'); }
  catch { return {}; }
}
function getQA(fileId, page) {
  const m = loadQAMap();
  return m[`${fileId}:${page}`] || [];
}
function saveQA(fileId, page, list) {
  const m = loadQAMap();
  m[`${fileId}:${page}`] = list;
  localStorage.setItem(KEY_QA, JSON.stringify(m));
}

function openSettings() {
  const cur = getApiKey();
  const masked = cur ? cur.slice(0,7) + '...' + cur.slice(-4) : '';
  const k = prompt(`粘贴 OpenAI API Key (留空保留当前)\n\n当前: ${masked || '(未设置)'}\n获取: https://platform.openai.com/api-keys`, '');
  if (k === null) return;
  if (k.trim()) { setApiKey(k.trim()); alert('已保存。问问题试试！'); }
  // re-render so settings hint refreshes
  if (FILES.find(f=>f.id===currentTab)) showPage();
}

async function askQuestion(fileId, page) {
  const ta = document.getElementById('qaInput');
  const btn = document.getElementById('qaAskBtn');
  const status = document.getElementById('qaStatus');
  const q = (ta.value || '').trim();
  if (!q) { ta.focus(); return; }
  const key = getApiKey();
  if (!key) {
    if (confirm('还没设置 OpenAI API Key，现在设置？')) openSettings();
    return;
  }

  // gather context from current page's expl entry
  const arr = EXPL[fileId] || [];
  const e = arr[page-1] || {};
  const ctxParts = [
    `文件: ${fileId}, 第 ${page} 页`,
    e.title ? `标题: ${e.title}` : '',
    e.summary ? `摘要: ${e.summary}` : '',
    Array.isArray(e.key_points) ? `关键点:\n- ${e.key_points.join('\n- ')}` : '',
    e.explanation ? `详解:\n${e.explanation}` : '',
    e.gotcha ? `易错点: ${e.gotcha}` : '',
  ].filter(Boolean);
  const context = ctxParts.join('\n\n');
  const history = getQA(fileId, page);

  btn.disabled = true;
  status.textContent = '🤔 AI 思考中...';
  status.className = 'qa-status thinking';
  try {
    const resp = await fetch('/api/ask', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ question: q, context, history, apiKey: key }),
    });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || 'unknown error');
    const list = getQA(fileId, page);
    list.push({ q, a: data.answer, ts: Date.now() });
    saveQA(fileId, page, list);
    ta.value = '';
    status.textContent = '';
    renderQAList(fileId, page);
  } catch (err) {
    status.textContent = '❌ ' + err.message;
    status.className = 'qa-status error';
  } finally {
    btn.disabled = false;
  }
}

function deleteQA(fileId, page, idx) {
  const list = getQA(fileId, page);
  list.splice(idx, 1);
  saveQA(fileId, page, list);
  renderQAList(fileId, page);
}

function renderQAList(fileId, page) {
  const container = document.getElementById('qaList');
  if (!container) return;
  const list = getQA(fileId, page);
  if (list.length === 0) { container.innerHTML = ''; return; }
  container.innerHTML = list.map((qa, i) => `
    <div class="qa-item">
      <div class="qa-q"><b>Q:</b> ${escapeHtml(qa.q)}
        <button class="qa-del" onclick="deleteQA('${fileId}', ${page}, ${i})" title="删除">✕</button>
      </div>
      <div class="qa-a"><b>A:</b> ${marked.parse(qa.a)}</div>
    </div>
  `).join('');
  if (window.renderMathInElement) {
    renderMathInElement(container, { delimiters: [
      {left:'$$',right:'$$',display:true},
      {left:'$', right:'$', display:false}
    ]});
  }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  })[c]);
}

// ============ Persisted state (last tab + per-file page) ============
const TAB_KEY = '4119:tab';
const PAGE_KEY = '4119:page'; // map fileId -> last page

function loadLastTab() { return localStorage.getItem(TAB_KEY) || 'overview'; }
function saveLastTab(t) { localStorage.setItem(TAB_KEY, t); }

function loadPageMap() {
  try { return JSON.parse(localStorage.getItem(PAGE_KEY) || '{}'); }
  catch { return {}; }
}
function getLastPage(fileId) {
  const m = loadPageMap();
  const p = parseInt(m[fileId]);
  return (Number.isFinite(p) && p >= 1) ? p : 1;
}
function setLastPage(fileId, page) {
  const m = loadPageMap();
  m[fileId] = page;
  localStorage.setItem(PAGE_KEY, JSON.stringify(m));
}

// ============ Stars (localStorage-backed) ============
const STAR_KEY = '4119:stars';
function loadStars() {
  try { return JSON.parse(localStorage.getItem(STAR_KEY) || '[]'); }
  catch { return []; }
}
function saveStars(arr) {
  localStorage.setItem(STAR_KEY, JSON.stringify(arr));
}
function starKey(fileId, page) { return `${fileId}:${page}`; }
function isStarred(fileId, page) {
  return loadStars().includes(starKey(fileId, page));
}
function toggleStar(fileId, page) {
  const k = starKey(fileId, page);
  const stars = loadStars();
  const i = stars.indexOf(k);
  if (i >= 0) stars.splice(i, 1);
  else stars.push(k);
  saveStars(stars);
  return i < 0; // true if newly starred
}

let EXPL = {};   // id -> [{title, summary, key_points, explanation}]
let FINAL = []; // problem walkthroughs
let MIDTERM = [];
let CONCEPTS = null;

let currentTab = loadLastTab();
let currentPage = 1; // will be restored per-file in selectTab

// ============ Boot ============
async function boot() {
  const [a,b,c,d] = await Promise.all([
    fetch('data/explanations.json').then(r=>r.json()).catch(()=>({})),
    fetch('data/finalpreview.json').then(r=>r.json()).catch(()=>([])),
    fetch('data/midterm.json').then(r=>r.json()).catch(()=>([])),
    fetch('data/concepts.json').then(r=>r.json()).catch(()=>null),
  ]);
  EXPL = a; FINAL = b; MIDTERM = c; CONCEPTS = d;
  renderTabs();
  selectTab(currentTab);
  document.addEventListener('keydown', e=>{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.target.isContentEditable) return;
    if (e.key === 'ArrowRight') step(1);
    if (e.key === 'ArrowLeft') step(-1);
    if ((e.key === 's' || e.key === 'S') && FILES.find(f=>f.id===currentTab)) onToggleStar();
    if ((e.key === 'y' || e.key === 'Y') && FILES.find(f=>f.id===currentTab)) hlSelected(currentTab, currentPage);
  });
}

function renderTabs() {
  const nav = document.getElementById('tabs');
  nav.innerHTML = '';
  const mkTab = (item) => {
    const el = document.createElement('div');
    el.className = 'tab';
    el.dataset.id = item.id;
    el.innerHTML = `<span>${item.label}</span>${item.pages?`<span class="count">${item.pages}</span>`:''}`;
    el.onclick = ()=>selectTab(item.id);
    return el;
  };
  // overview first
  nav.appendChild(mkTab(SPECIAL[0]));
  // section header
  const sec1 = document.createElement('div');
  sec1.className = 'tab section'; sec1.textContent = '讲义 (期中后)';
  nav.appendChild(sec1);
  FILES.forEach(f=>nav.appendChild(mkTab(f)));
  const sec2 = document.createElement('div');
  sec2.className = 'tab section'; sec2.textContent = '重点复习';
  nav.appendChild(sec2);
  SPECIAL.slice(1).forEach(s=>nav.appendChild(mkTab(s)));
}

function selectTab(id) {
  currentTab = id;
  saveLastTab(id);
  // For paged lecture tabs, restore last viewed page; for special tabs use page 1
  const isLecture = !!FILES.find(f=>f.id===id);
  currentPage = isLecture ? getLastPage(id) : 1;
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active', t.dataset.id===id));
  if (id==='overview') return renderOverview();
  if (id==='final') return renderFinal();
  if (id==='midterm') return renderMidterm();
  if (id==='concepts') return renderConcepts();
  if (id==='cheat') return renderCheatSheet();
  if (id==='stars') return renderStars();
  // lecture
  renderLecture(id);
}

// ============ Overview ============
function renderOverview() {
  const content = document.getElementById('content');
  let cards = FILES.map(f=>{
    const topics = (EXPL[f.id]?.[0]?.topics) || '';
    return `<div class="card" data-id="${f.id}">
      <h3>${f.label}</h3>
      <div class="meta">${f.pages} 页</div>
    </div>`;
  }).join('');
  let specials = SPECIAL.slice(1).map(s=>`<div class="card" data-id="${s.id}">
    <h3>${s.label}</h3>
    <div class="meta">${s.pages? s.pages+' 页': '专题视图'}</div>
  </div>`).join('');

  content.innerHTML = `<div class="overview">
    <h2>4119 期末复习 Notebook</h2>
    <p class="subtle">明天考试。左侧任意打开一个讲义，左边是 PPT 原图，右边是 AI 讲解。重点请直接看 <b>⭐ Final Preview</b> 和 <b>🧠 概念知识库</b>。期中卷在 <b>📝 期中复盘</b> 里。</p>

    <h3 style="color:var(--accent-2);margin-top:24px">考纲（按 Final Preview 整理）</h3>
    <ul>
      <li><b>Application Layer</b>：HTTP（持久/非持久、Web cache）、DNS、视频流、P2P（BitTorrent、文件分发时间、DHT）、socket</li>
      <li><b>Transport Layer</b>：UDP/TCP、可靠传输（GBN vs SR）、拥塞控制（slow start、AIMD、CUBIC、BBR、ECN）</li>
      <li><b>Network Data Plane</b>：最长前缀匹配、IP 地址 / 子网 / DHCP、NAT、IPv4 vs IPv6</li>
      <li><b>Network Control Plane</b>：Link-state（Dijkstra）vs Distance vector（Bellman-Ford）、BGP、SDN/OpenFlow</li>
      <li><b>Data Link Layer (Wired)</b>：差错检测（parity / checksum / CRC）、MAC（ALOHA、CSMA/CD、Ethernet）、ARP</li>
      <li><b>Wireless</b>：自由空间路径损耗、SNR/SINR、隐藏/暴露终端、RTS/CTS、CSMA/CA</li>
    </ul>

    <h3 style="color:var(--accent-2)">讲义</h3>
    <div class="cards">${cards}</div>

    <h3 style="color:var(--accent-2)">重点复习</h3>
    <div class="cards">${specials}</div>
  </div>`;
  content.querySelectorAll('.card').forEach(c=>c.onclick = ()=>selectTab(c.dataset.id));
}

// ============ Lecture view ============
function renderLecture(id) {
  const file = FILES.find(f=>f.id===id);
  const total = file.pages;
  const content = document.getElementById('content');
  content.innerHTML = `
    <div class="toolbar">
      <div class="title"><b>${file.label}</b> <span class="subtle">— 第 <span id="curp">1</span> / ${total} 页</span></div>
      <div class="pager">
        <button id="starBtn" onclick="onToggleStar()" title="收藏/取消收藏 (S)">☆ 收藏</button>
        <button onclick="step(-1)">← 上一页</button>
        <input type="number" id="goto" min="1" max="${total}" value="1">
        <button onclick="gotoInput()">跳转</button>
        <button onclick="step(1)">下一页 →</button>
      </div>
    </div>
    <div class="split">
      <div class="slide-pane"><img id="slide" alt=""></div>
      <div class="explain-pane" id="explain"></div>
    </div>
  `;
  showPage();
}

function refreshStarBtn() {
  const btn = document.getElementById('starBtn');
  if (!btn) return;
  const on = isStarred(currentTab, currentPage);
  btn.innerHTML = on ? '★ 已收藏' : '☆ 收藏';
  btn.classList.toggle('starred', on);
}

function onToggleStar() {
  const newly = toggleStar(currentTab, currentPage);
  refreshStarBtn();
  // brief feedback in title bar
  const t = document.querySelector('.toolbar .title');
  if (t) {
    const old = t.innerHTML;
    t.innerHTML += `  <span class="subtle" style="color:var(--warn)">${newly?'⭐ 已加入收藏':'已移除'}</span>`;
    setTimeout(()=>{ t.innerHTML = old; }, 1200);
  }
}

function showPage() {
  const file = FILES.find(f=>f.id===currentTab);
  if (!file) return;
  const total = file.pages;
  if (currentPage < 1) currentPage = 1;
  if (currentPage > total) currentPage = total;
  setLastPage(currentTab, currentPage);
  document.getElementById('curp').textContent = currentPage;
  document.getElementById('goto').value = currentPage;
  const pad = String(currentPage).padStart(2,'0');
  document.getElementById('slide').src = `pages/${currentTab}/p-${pad}.jpg`;
  // explanation
  const arr = EXPL[currentTab] || [];
  const e = arr[currentPage-1];
  renderExplain(e, currentTab, currentPage);
  refreshStarBtn();
}

function renderExplain(e, fileId, pageNum) {
  const target = document.getElementById('explain');
  let aiHtml = '';
  if (!e) {
    aiHtml = `<h2>AI 讲解</h2>
      <p class="skeleton">骨架未生成 — 这一页 AI 讲解还在生成中。</p>
      <p class="subtle">提示：键盘 ← / → 翻页 · S 收藏。</p>`;
  } else {
    aiHtml = `<h2>${e.title || ''}</h2>`;
    if (e.topics) aiHtml += `<div>${e.topics.map(t=>`<span class="tag">${t}</span>`).join('')}</div>`;
    if (e.summary) aiHtml += `<p><b>这一页讲了什么 —</b> ${e.summary}</p>`;
    if (e.key_points && e.key_points.length) {
      aiHtml += `<h3>关键点</h3><ul>${e.key_points.map(k=>`<li>${k}</li>`).join('')}</ul>`;
    }
    if (e.explanation) {
      aiHtml += `<h3>详解</h3>${marked.parse(e.explanation)}`;
    } else if (!e.summary) {
      aiHtml += `<p class="skeleton">详解尚未生成 — 这页主要是图示/标题页，留意上面的关键词即可。</p>`;
    }
    if (e.gotcha) {
      aiHtml += `<blockquote><b>易错点 / Final 考点：</b><br>${e.gotcha}</blockquote>`;
    }
  }
  // Restore saved highlights for this page if present
  const savedHl = getHighlightHtml(fileId, pageNum);
  if (savedHl) aiHtml = savedHl;

  let html = `<div class="hl-toolbar">
    <button onclick="hlSelected('${fileId}', ${pageNum})" title="选中文字后点这里高亮 (Y 键也行)">🖍️ 高亮选中</button>
    <button onclick="hlClearPage('${fileId}', ${pageNum})" class="ghost" title="清除本页所有高亮">🧹 清除</button>
    <span class="subtle hl-hint">提示：双击黄色文本可取消单条高亮</span>
  </div>
  <div id="aiExplain">${aiHtml}</div>`;
  // Q&A section (only for paged lecture views)
  const isLecture = !!FILES.find(f=>f.id===fileId);
  if (isLecture) {
    html += `<div class="qa-box">
      <div class="qa-header">
        <h3>问 AI 助教 <span class="subtle">· 这一页的笔记会保存</span></h3>
        <button class="qa-settings-btn" onclick="openSettings()" title="设置 OpenAI API Key">⚙️</button>
      </div>
      <div class="qa-list" id="qaList"></div>
      <div class="qa-input">
        <textarea id="qaInput" placeholder="对这页有不懂的，问我（按 Cmd/Ctrl + Enter 提交）"></textarea>
        <button id="qaAskBtn" onclick="askQuestion('${fileId}', ${pageNum})">问</button>
      </div>
      <div id="qaStatus" class="qa-status"></div>
    </div>`;
  }
  target.innerHTML = html;
  if (window.renderMathInElement) {
    renderMathInElement(target, {
      delimiters: [
        {left:'$$',right:'$$',display:true},
        {left:'$', right:'$', display:false},
        {left:'\\[',right:'\\]',display:true},
        {left:'\\(',right:'\\)',display:false}
      ]
    });
  }
  if (isLecture) {
    renderQAList(fileId, pageNum);
    const ta = document.getElementById('qaInput');
    if (ta) ta.addEventListener('keydown', ev => {
      if ((ev.metaKey || ev.ctrlKey) && ev.key === 'Enter') {
        askQuestion(fileId, pageNum);
      }
    });
    // double-click on a <mark> removes that highlight
    const aiExplain = document.getElementById('aiExplain');
    if (aiExplain) aiExplain.addEventListener('dblclick', _onMarkDblClick);
  }
}

function step(d) {
  if (currentTab === 'final' || currentTab === 'midterm' || currentTab === 'overview' || currentTab === 'concepts') return;
  currentPage += d;
  showPage();
}
function gotoInput() {
  const v = parseInt(document.getElementById('goto').value);
  if (!isNaN(v)) { currentPage = v; showPage(); }
}

// ============ Final Preview (problem walkthrough view) ============
function renderFinal() {
  const content = document.getElementById('content');
  let html = `<div class="toolbar">
      <div class="title"><b>⭐ Final Preview · 详细讲解</b> <span class="subtle">老师给出的样题 + 每题手把手</span></div>
    </div>
    <div class="problem-list">`;
  html += `<p class="subtle">这是 final-preview.pdf 里的每道题的逐题精讲。点开看就行，每题都包含：题目 → 标准答案 → 思路 → 易错点。</p>`;
  FINAL.forEach((p, i)=>{
    html += `<div class="problem-card">
      <header><h3>题 ${i+1}: ${p.title}</h3><span class="tag">${p.topic}</span></header>
      <div class="body">
        <div class="question"><b>题目：</b><br>${p.question}</div>
        <div class="answer"><b>标准答案：</b><br>${p.answer}</div>
        <div class="walkthrough"><h4 style="color:var(--accent-2)">💡 思路 + 详解</h4>${marked.parse(p.walkthrough || '')}
        ${p.gotcha?`<blockquote><b>易错点：</b> ${p.gotcha}</blockquote>`:''}
        ${p.related?`<p class="subtle">相关概念：${p.related.map(r=>`<span class="tag">${r}</span>`).join('')}</p>`:''}
        </div>
      </div>
    </div>`;
  });
  html += `</div>`;
  content.innerHTML = html;
  if (window.renderMathInElement) {
    renderMathInElement(content, {
      delimiters: [
        {left:'$$',right:'$$',display:true},
        {left:'$', right:'$', display:false}
      ]
    });
  }
}

// ============ Midterm Review (split view: original PDF + standard answers) ============
let midtermPage = 1;
function renderMidterm() {
  const content = document.getElementById('content');
  content.innerHTML = `<div class="toolbar">
      <div class="title"><b>📝 期中复盘</b> <span class="subtle">左：原题 PDF (4 页) · 右：标准答案 / 错点分析</span></div>
      <div class="pager">
        <button onclick="midtermStep(-1)">← 上一页</button>
        <span id="midpg">1 / 4</span>
        <button onclick="midtermStep(1)">下一页 →</button>
      </div>
    </div>
    <div class="split">
      <div class="slide-pane"><img id="midimg" alt=""></div>
      <div class="explain-pane" id="midbody"></div>
    </div>`;
  showMidterm();
}
function midtermStep(d) {
  midtermPage = Math.max(1, Math.min(4, midtermPage + d));
  showMidterm();
}
function showMidterm() {
  document.getElementById('midpg').textContent = `${midtermPage} / 4`;
  document.getElementById('midimg').src = `pages/midoriginoutput/p-0${midtermPage}.jpg`;
  // Map page → which questions appear on this page
  const pageMap = {
    1: [0, 1],       // Q1 + Q2 begin
    2: [1, 2, 3],    // Q2 rest + Q3 + Q4 begin
    3: [3, 4, 5],    // Q4 rest + Q5 + Q6 begin (Q5 has Q6 split)
    4: [5, 6]        // Q6 cont + final extras
  };
  const qs = pageMap[midtermPage] || [];
  let html = `<h2>这页对应的题（你总分 <span class="score-mid">52 / 100</span>）</h2>`;
  qs.forEach(i => {
    const q = MIDTERM[i];
    if (!q) return;
    const scoreClass = q.got/q.full>=0.8?'score-good': q.got/q.full>=0.5?'score-mid':'score-bad';
    html += `<div class="midterm-q">
      <h3>Q${i+1}. ${q.title} <span class="${scoreClass}">(${q.got} / ${q.full})</span></h3>
      <details open><summary class="subtle">题目原文</summary><div>${marked.parse(q.question || '')}</div></details>
      <div class="gold"><b>✅ 标准答案：</b><br>${marked.parse(q.gold || '')}</div>
      ${q.your_mistake?`<div class="gotcha"><b>❌ 你失分的点：</b><br>${marked.parse(q.your_mistake)}</div>`:''}
      ${q.takeaway?`<blockquote><b>带走：</b> ${q.takeaway}</blockquote>`:''}
    </div>`;
  });
  document.getElementById('midbody').innerHTML = html;
  if (window.renderMathInElement) {
    renderMathInElement(document.getElementById('midbody'), {
      delimiters: [{left:'$$',right:'$$',display:true},{left:'$', right:'$', display:false}]
    });
  }
}

// ============ Concept Graph ============
function renderConcepts() {
  const content = document.getElementById('content');
  content.innerHTML = `<div class="toolbar">
      <div class="title"><b>🧠 概念知识库</b> <span class="subtle">点击节点查看说明 · 拖动可重新布局</span></div>
    </div>
    <div class="graph-help">提示：节点颜色 = 所属层；边表示「依赖 / 出自」。点击一个节点，右下角会弹出它的定义和它出现在哪几页。</div>
    <div id="graph"><div class="graph-loading">加载中...</div></div>
    <div id="conceptDetail" style="position:absolute;right:20px;bottom:20px;width:380px;max-height:60vh;overflow-y:auto;background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:14px 18px;display:none;box-shadow:0 8px 30px rgba(0,0,0,0.5);"></div>`;
  const container = document.getElementById('graph');
  if (typeof vis === 'undefined' || !vis.Network) {
    container.innerHTML = `<div class="graph-loading" style="color:var(--bad)">❌ vis-network 库没加载成功，刷新一次试试 (Cmd+Shift+R 强刷)</div>`;
    console.error('vis is undefined');
    return;
  }
  if (!CONCEPTS) {
    container.innerHTML = `<div class="graph-loading" style="color:var(--bad)">❌ concepts.json 没加载成功</div>`;
    console.error('CONCEPTS is null');
    return;
  }
  // clear loading placeholder
  container.innerHTML = '';
  const nodes = new vis.DataSet(CONCEPTS.nodes);
  const edges = new vis.DataSet(CONCEPTS.edges);
  const data = { nodes, edges };
  const options = {
    nodes: {
      shape: 'dot',
      size: 18,
      font: { color: '#e6e8ec', size: 14, face: 'system-ui' },
      borderWidth: 1.5,
    },
    edges: {
      color: { color: '#3c4258', highlight: '#7aa2ff' },
      smooth: { type: 'continuous' },
      arrows: { to: { enabled: true, scaleFactor: 0.5 } },
    },
    groups: {
      app:       { color: { background: '#5bd6a3', border: '#3aa37c' } },
      transport: { color: { background: '#7aa2ff', border: '#4d76d6' } },
      network:   { color: { background: '#a78bfa', border: '#7a5cd1' } },
      link:      { color: { background: '#f5c46e', border: '#c69642' } },
      wireless:  { color: { background: '#ff7a8a', border: '#cc4d5e' } },
      general:   { color: { background: '#8a90a3', border: '#5d6376' } },
    },
    physics: { stabilization: { iterations: 200 }, barnesHut: { springLength: 130 } },
    interaction: { hover: true, tooltipDelay: 80 },
  };
  const network = new vis.Network(container, data, options);
  const detail = document.getElementById('conceptDetail');
  network.on('selectNode', (params)=>{
    const id = params.nodes[0];
    const n = CONCEPTS.nodes.find(x=>x.id===id);
    if (!n) return;
    let html = `<h3 style="margin:0 0 8px;color:var(--accent)">${n.label}</h3>
      <div class="subtle" style="margin-bottom:8px">分类：${n.group}</div>
      ${n.desc?`<div>${marked.parse(n.desc)}</div>`:''}`;
    if (n.refs && n.refs.length) html += `<h4 style="color:var(--accent-2);margin-bottom:4px">出现在</h4><ul style="margin:0;padding-left:18px">${n.refs.map(r=>`<li>${r.file} 第 ${r.page} 页</li>`).join('')}</ul>`;
    if (n.formula) html += `<h4 style="color:var(--accent-2);margin-bottom:4px">公式</h4><div>${n.formula}</div>`;
    html += `<div style="margin-top:10px;text-align:right"><button onclick="document.getElementById('conceptDetail').style.display='none'" style="background:var(--panel-2);border:1px solid var(--border);color:var(--text);padding:4px 10px;border-radius:4px;cursor:pointer">关闭</button></div>`;
    detail.innerHTML = html;
    detail.style.display = 'block';
    if (window.renderMathInElement) renderMathInElement(detail, {delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]});
  });
  network.on('deselectNode', ()=>{ detail.style.display='none'; });
}

// ============ Stars view ============
function renderStars() {
  const content = document.getElementById('content');
  const stars = loadStars();
  // group by file
  const byFile = {};
  stars.forEach(k => {
    const [f, p] = k.split(':');
    (byFile[f] = byFile[f] || []).push(parseInt(p));
  });
  Object.values(byFile).forEach(a => a.sort((x,y)=>x-y));

  // file ordering: follow FILES list
  const fileOrder = FILES.map(f=>f.id);

  let html = `<div class="toolbar">
      <div class="title"><b>⭐ 收藏的重点 PPT</b> <span class="subtle">共 ${stars.length} 张 · 点缩略图跳转 · 点 ✕ 取消收藏 · 在讲义页按 S 快速收藏</span></div>
      <div class="pager">${stars.length?`<button onclick="clearAllStars()">清空全部</button>`:''}</div>
    </div>
    <div class="stars-host">`;

  if (stars.length === 0) {
    html += `<div class="stars-empty">
      <h2>还没收藏任何 PPT</h2>
      <p>打开任何一份讲义，看到关键页就点工具栏右上角的 <span class="kbd">☆ 收藏</span> 按钮（或按键盘 <span class="kbd">S</span>）。</p>
      <p class="subtle">收藏会保存在浏览器 localStorage 里，刷新/换 tab 都不会丢。</p>
    </div>`;
  } else {
    fileOrder.forEach(fid => {
      const pages = byFile[fid];
      if (!pages || pages.length===0) return;
      const fileMeta = FILES.find(f=>f.id===fid) || { label: fid };
      html += `<section class="stars-group">
        <h3>${fileMeta.label} <span class="subtle">· ${pages.length} 张</span></h3>
        <div class="stars-grid">`;
      pages.forEach(p => {
        const pad = String(p).padStart(2,'0');
        const expl = (EXPL[fid] || [])[p-1] || {};
        const title = expl.title || `第 ${p} 页`;
        html += `<div class="star-card" data-file="${fid}" data-page="${p}">
          <div class="star-thumb"><img loading="lazy" src="pages/${fid}/p-${pad}.jpg" alt=""></div>
          <div class="star-meta">
            <div class="star-title">${title}</div>
            <div class="subtle">${fid} · p${p}</div>
          </div>
          <button class="star-remove" title="移除收藏" onclick="event.stopPropagation(); removeStar('${fid}', ${p})">✕</button>
        </div>`;
      });
      html += `</div></section>`;
    });
  }
  html += `</div>`;
  content.innerHTML = html;
  content.querySelectorAll('.star-card').forEach(card => {
    card.onclick = () => {
      currentTab = card.dataset.file;
      currentPage = parseInt(card.dataset.page);
      saveLastTab(currentTab);
      setLastPage(currentTab, currentPage);
      document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active', t.dataset.id===currentTab));
      renderLecture(currentTab);
    };
  });
}

function removeStar(fid, p) {
  const stars = loadStars();
  const i = stars.indexOf(starKey(fid, p));
  if (i >= 0) { stars.splice(i,1); saveStars(stars); renderStars(); }
}
function clearAllStars() {
  if (!confirm('确定清空全部收藏？')) return;
  saveStars([]);
  renderStars();
}

// ============ Cheat Sheet (interactive editor) ============
const KEY_CHEAT = '4119:cheatsheet:html';

async function renderCheatSheet() {
  const content = document.getElementById('content');
  const saved = localStorage.getItem(KEY_CHEAT);
  let bodyHtml;
  if (saved) {
    bodyHtml = saved;
  } else {
    bodyHtml = await fetch('cheatsheet.html').then(r=>r.text()).catch(()=>'<p>cheatsheet.html not found</p>');
  }
  content.innerHTML = `<div class="toolbar">
      <div class="title"><b>🖨️ Cheat Sheet</b> <span class="subtle">直接点击编辑 · ✕ 删 section · 📷 加图 · 自动存</span></div>
      <div class="pager">
        <button onclick="cheatInsertAuto()" title="把你的收藏/笔记/期中要点拉过来">📥 拉取重点</button>
        <button onclick="cheatAddSection()">➕ Section</button>
        <button onclick="cheatReset()" title="丢弃所有编辑">↻ Reset</button>
        <button onclick="window.print()">🖨️ Print</button>
      </div>
    </div>
    <div class="cheat-host" id="cheatHost">${bodyHtml}</div>`;
  attachCheatHandlers();
  if (window.renderMathInElement) {
    renderMathInElement(content, { delimiters: [
      {left:'$$',right:'$$',display:true},
      {left:'$', right:'$', display:false}
    ]});
  }
}

function attachCheatHandlers() {
  const host = document.getElementById('cheatHost');
  if (!host) return;
  host.querySelectorAll('section').forEach(section => {
    if (section.dataset.wired) return;
    section.dataset.wired = '1';
    section.contentEditable = 'true';
    section.spellcheck = false;
    // overlay buttons (non-editable)
    const overlay = document.createElement('div');
    overlay.className = 'section-overlay';
    overlay.contentEditable = 'false';
    overlay.innerHTML = `
      <button title="加图" onclick="cheatAddImage(this); event.stopPropagation();">📷</button>
      <button title="删除" onclick="cheatDeleteSection(this); event.stopPropagation();">✕</button>`;
    section.appendChild(overlay);
  });
  // single input listener, debounced
  if (!host.dataset.listenerWired) {
    host.dataset.listenerWired = '1';
    host.addEventListener('input', debouncedSaveCheat);
  }
}

let _cheatSaveTimer;
function debouncedSaveCheat() {
  clearTimeout(_cheatSaveTimer);
  _cheatSaveTimer = setTimeout(saveCheatSheet, 400);
}

function saveCheatSheet() {
  const host = document.getElementById('cheatHost');
  if (!host) return;
  // clone, strip overlays + ephemeral attrs
  const clone = host.cloneNode(true);
  clone.querySelectorAll('.section-overlay').forEach(o => o.remove());
  clone.querySelectorAll('[contenteditable]').forEach(e => e.removeAttribute('contenteditable'));
  clone.querySelectorAll('[data-wired]').forEach(e => e.removeAttribute('data-wired'));
  clone.querySelectorAll('[spellcheck]').forEach(e => e.removeAttribute('spellcheck'));
  localStorage.setItem(KEY_CHEAT, clone.innerHTML);
}

function cheatDeleteSection(btn) {
  const section = btn.closest('section');
  const title = section.querySelector('h2')?.textContent || '(no title)';
  if (!confirm(`删除这个 section?\n\n标题: ${title}`)) return;
  section.remove();
  saveCheatSheet();
}

function cheatAddImage(btn) {
  const section = btn.closest('section');
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.onchange = async (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    if (file.size > 8 * 1024 * 1024) { alert('图太大 (>8MB)'); return; }
    const reader = new FileReader();
    reader.onload = async () => {
      const dataUrl = reader.result;
      try {
        const resp = await fetch('/api/upload', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ dataUrl, filename: file.name }),
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.error || 'upload failed');
        const fig = document.createElement('figure');
        fig.contentEditable = 'false';
        fig.innerHTML = `<img src="${data.path}" alt=""><figcaption contenteditable="true">caption</figcaption>`;
        const overlay = section.querySelector('.section-overlay');
        section.insertBefore(fig, overlay);
        saveCheatSheet();
      } catch (err) {
        alert('上传失败: ' + err.message);
      }
    };
    reader.readAsDataURL(file);
  };
  input.click();
}

function cheatAddSection() {
  const host = document.getElementById('cheatHost');
  const sheets = host.querySelectorAll('.sheet');
  const lastSheet = sheets[sheets.length - 1];
  const cols = lastSheet?.querySelector('.cols') || lastSheet;
  if (!cols) { alert('没找到 sheet 容器'); return; }
  const sec = document.createElement('section');
  sec.innerHTML = '<h2>New section</h2><p>Edit me…</p>';
  cols.appendChild(sec);
  attachCheatHandlers();
  saveCheatSheet();
  sec.scrollIntoView({behavior:'smooth', block:'center'});
}

function cheatReset() {
  if (!confirm('丢弃所有编辑，恢复默认 cheatsheet?')) return;
  localStorage.removeItem(KEY_CHEAT);
  renderCheatSheet();
}

// Pull from your collected content: midterm takeaways, starred slides, Q&A, highlights
function cheatInsertAuto() {
  const host = document.getElementById('cheatHost');
  if (!host) return;
  // Build a new sheet that aggregates user-collected importance
  const sheet = document.createElement('div');
  sheet.className = 'sheet';
  sheet.innerHTML = `<h1>YOUR COLLECTED IMPORTANT POINTS</h1><div class="cols"></div>`;
  const cols = sheet.querySelector('.cols');
  let count = 0;

  // 1) Midterm takeaways
  (MIDTERM || []).forEach((q, i) => {
    if (q.takeaway) {
      const sec = document.createElement('section');
      sec.innerHTML = `<h2>📝 Mid Q${i+1}: ${escapeHtml(q.title || '').slice(0,40)}</h2>
        <p>${escapeHtml(q.takeaway)}</p>`;
      cols.appendChild(sec);
      count++;
    }
  });

  // 2) Starred slides
  const stars = loadStars();
  if (stars.length > 0) {
    const sec = document.createElement('section');
    const items = stars.map(k => {
      const [f, p] = k.split(':');
      const e = (EXPL[f] || [])[parseInt(p) - 1] || {};
      return `<li><b>${f} p${p}</b>: ${escapeHtml(e.title || '')}</li>`;
    }).join('');
    sec.innerHTML = `<h2>⭐ Starred slides (${stars.length})</h2><ul>${items}</ul>`;
    cols.appendChild(sec);
    count++;
  }

  // 3) Q&A entries
  const qa = loadQAMap();
  let qaCount = 0;
  Object.entries(qa).forEach(([k, list]) => {
    if (!list || !list.length) return;
    const [f, p] = k.split(':');
    list.forEach(item => {
      const sec = document.createElement('section');
      const aHtml = marked.parse(item.a || '').replace(/<\/?p[^>]*>/g, '');
      sec.innerHTML = `<h2>💬 Q&A · ${f} p${p}</h2>
        <p><b>Q:</b> ${escapeHtml(item.q || '')}</p>
        <p>${aHtml}</p>`;
      cols.appendChild(sec);
      count++;
      qaCount++;
    });
  });

  // 4) Highlighted text from AI explanations
  const hl = loadHighlights();
  const hlEntries = Object.entries(hl);
  if (hlEntries.length > 0) {
    const sec = document.createElement('section');
    const items = hlEntries.map(([k, marks]) => {
      const [f, p] = k.split(':');
      const e = (EXPL[f] || [])[parseInt(p) - 1] || {};
      const lines = marks.map(t => `<li>${escapeHtml(t)}</li>`).join('');
      return `<div><b>${f} p${p}</b> — ${escapeHtml(e.title || '')}<ul>${lines}</ul></div>`;
    }).join('');
    sec.innerHTML = `<h2>🖍️ Highlights</h2>${items}`;
    cols.appendChild(sec);
    count++;
  }

  if (count === 0) {
    alert('还没有可拉取的内容。先去:\n• 讲义页按 S 收藏重点\n• 在 AI 解释里划词点高亮\n• 在 Q&A 框里问问题\n• 看期中复盘');
    return;
  }
  host.appendChild(sheet);
  attachCheatHandlers();
  saveCheatSheet();
  sheet.scrollIntoView({behavior:'smooth', block:'start'});
}

// ============ Highlights for AI explanations ============
const KEY_HL = '4119:highlights';  // map "{fileId}:{page}" -> [text strings]

function loadHighlights() {
  try { return JSON.parse(localStorage.getItem(KEY_HL) || '{}'); }
  catch { return {}; }
}
function getHighlightHtml(fileId, page) {
  const m = loadHighlights();
  return m[`${fileId}:${page}__html`] || '';
}
function setHighlightHtml(fileId, page, html, marksList) {
  const m = loadHighlights();
  m[`${fileId}:${page}__html`] = html;
  m[`${fileId}:${page}`] = marksList || [];
  localStorage.setItem(KEY_HL, JSON.stringify(m));
}
function clearHighlights(fileId, page) {
  const m = loadHighlights();
  delete m[`${fileId}:${page}__html`];
  delete m[`${fileId}:${page}`];
  localStorage.setItem(KEY_HL, JSON.stringify(m));
}

function hlSelected(fileId, pageNum) {
  const sel = window.getSelection();
  if (!sel || sel.isCollapsed) { alert('先用鼠标选中要高亮的文字'); return; }
  const range = sel.getRangeAt(0);
  const aiExplain = document.getElementById('aiExplain');
  if (!aiExplain || !aiExplain.contains(range.commonAncestorContainer)) {
    alert('请在 AI 讲解区域内选择');
    return;
  }
  const mark = document.createElement('mark');
  try {
    range.surroundContents(mark);
  } catch (e) {
    // selection crosses element boundaries
    mark.appendChild(range.extractContents());
    range.insertNode(mark);
  }
  sel.removeAllRanges();
  persistHighlights(fileId, pageNum);
}

function hlClearPage(fileId, pageNum) {
  if (!confirm('清除这一页所有高亮？')) return;
  clearHighlights(fileId, pageNum);
  showPage(); // re-render
}

function persistHighlights(fileId, pageNum) {
  const aiExplain = document.getElementById('aiExplain');
  if (!aiExplain) return;
  const marks = Array.from(aiExplain.querySelectorAll('mark')).map(m => m.textContent.trim()).filter(Boolean);
  setHighlightHtml(fileId, pageNum, aiExplain.innerHTML, marks);
}

// Allow double-click on a mark to remove it
function _onMarkDblClick(ev) {
  if (ev.target.tagName !== 'MARK') return;
  const mark = ev.target;
  const parent = mark.parentNode;
  while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
  mark.remove();
  parent.normalize();
  persistHighlights(currentTab, currentPage);
}

boot();
