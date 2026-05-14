// ============ Data registry ============
const FILES = [
  // 期中前
  { id: 'lec1-intro',       label: 'lec1 · Intro',           pages: 29, premid: true },
  { id: 'lec2-basics1',     label: 'lec2 · Basics 1',        pages: 36, premid: true },
  { id: 'lec3-basics2',     label: 'lec3 · Basics 2',        pages: 26, premid: true },
  { id: 'lec4-basics3',     label: 'lec4 · Basics 3',        pages: 34, premid: true },
  { id: 'lec5-web',         label: 'lec5 · Web / HTTP',      pages: 32, premid: true },
  { id: 'lec6-video',       label: 'lec6 · Video / DASH',    pages: 24, premid: true },
  { id: 'lec7',             label: 'lec7 · Socket',          pages: 15, premid: true },
  { id: 'lec8-dns',         label: 'lec8 · DNS',             pages: 28, premid: true },
  { id: 'lec9-p2p',         label: 'lec9 · P2P / BitTorrent',pages: 21, premid: true },
  { id: 'lec10-transport',  label: 'lec10 · Transport intro',pages: 36, premid: true },
  { id: 'lec11-reliability',label: 'lec11 · RDT / GBN / SR', pages: 49, premid: true },
  { id: 'lec12-tcp',        label: 'lec12 · TCP',            pages: 27, premid: true },
  { id: 'lec13-congestion', label: 'lec13 · 拥塞控制 intro', pages: 38, premid: true },
  { id: 'midterm-preview',  label: 'midterm-preview · 样题', pages: 9,  premid: true },
  // 期中后
  { id: 'lec14',            label: 'lec14 · TCP 拥塞控制',   pages: 20 },
  { id: 'lec16',            label: 'lec16 · Network 数据面', pages: 45 },
  { id: 'lec17',            label: 'lec17 · IP / DHCP / NAT',pages: 28 },
  { id: 'lec18',            label: 'lec18 · IPv6 · 路由',    pages: 54 },
  { id: 'lec19',            label: 'lec19 · BGP · OSPF',     pages: 25 },
  { id: 'lec20',            label: 'lec20 · SDN · OpenFlow', pages: 44 },
  { id: 'lec21',            label: 'lec21 · Data Link / MAC',pages: 30 },
  { id: 'lec22',            label: 'lec22 · 交换机 · 无线',  pages: 31 },
  { id: 'lec23',            label: 'lec23 · 无线 MAC',       pages: 39 },
  { id: 'final-preview',    label: 'final-preview · 样题',   pages: 14 },
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

function openSettings() {
  const cur = getApiKey();
  const masked = cur ? cur.slice(0,7) + '...' + cur.slice(-4) : '';
  const k = prompt(`粘贴 OpenAI API Key (留空保留当前)\n\n当前: ${masked || '(未设置)'}\n获取: https://platform.openai.com/api-keys`, '');
  if (k === null) return;
  if (k.trim()) { setApiKey(k.trim()); alert('已保存。问问题试试！'); }
  // re-render so settings hint refreshes
  if (FILES.find(f=>f.id===currentTab)) showPage();
}

// Generic Q&A: contextKey is an arbitrary string like
//   "lec23:5"     (lecture page)
//   "midterm:2"   (midterm question index)
//   "final:1"     (final-preview question index)
//   "concepts"    (the concept graph)
function safeId(s) { return String(s).replace(/[^a-zA-Z0-9]/g, '_'); }

function getQA(qaKey) {
  const m = loadQAMap();
  return m[qaKey] || [];
}
function saveQA(qaKey, list) {
  const m = loadQAMap();
  m[qaKey] = list;
  localStorage.setItem(KEY_QA, JSON.stringify(m));
}

function qaWidgetHtml(qaKey, title) {
  const safe = safeId(qaKey);
  const t = title || '问 AI 助教';
  return `<div class="qa-box" data-qa-key="${qaKey}">
    <div class="qa-header">
      <h3>${t} <span class="subtle">· 笔记会保存到本地</span></h3>
      <button class="qa-settings-btn" onclick="openSettings()" title="设置 OpenAI API Key">⚙️</button>
    </div>
    <div class="qa-list" id="qaList-${safe}"></div>
    <div class="qa-input">
      <textarea id="qaInput-${safe}" placeholder="对这里有不懂的，问我（Cmd/Ctrl + Enter 提交）"></textarea>
      <button id="qaAskBtn-${safe}" onclick="askQuestion('${qaKey.replace(/'/g, "\\'")}')">问</button>
    </div>
    <div id="qaStatus-${safe}" class="qa-status"></div>
  </div>`;
}

function buildContextForKey(qaKey) {
  if (qaKey.startsWith('midterm:')) {
    const idx = parseInt(qaKey.split(':')[1]);
    const q = (MIDTERM || [])[idx];
    if (!q) return qaKey;
    return [
      `[场景] 期中复盘 — Q${idx+1}: ${q.title}`,
      `得分: ${q.got} / ${q.full}`,
      `题目原文:\n${q.question || ''}`,
      `标准答案:\n${q.gold || ''}`,
      q.your_mistake ? `学生失分点:\n${q.your_mistake}` : '',
      q.takeaway ? `带走口诀:\n${q.takeaway}` : '',
    ].filter(Boolean).join('\n\n');
  }
  if (qaKey.startsWith('final:')) {
    const idx = parseInt(qaKey.split(':')[1]);
    const p = (FINAL || [])[idx];
    if (!p) return qaKey;
    return [
      `[场景] Final Preview 样题 — Q${idx+1}: ${p.title}`,
      `主题: ${p.topic}`,
      `题目:\n${p.question || ''}`,
      `标准答案:\n${p.answer || ''}`,
      `老师讲解:\n${p.walkthrough || ''}`,
      p.gotcha ? `易错点: ${p.gotcha}` : '',
    ].filter(Boolean).join('\n\n');
  }
  if (qaKey === 'concepts' || qaKey === 'overview' || qaKey === 'cheat' || qaKey === 'stars') {
    return `[场景] ${qaKey} 视图`;
  }
  // lecture page: "fileId:page"
  const parts = qaKey.split(':');
  const fileId = parts[0], page = parts[1];
  const arr = EXPL[fileId] || [];
  const e = arr[parseInt(page) - 1];
  if (!e) return qaKey;
  return [
    `[场景] 文件 ${fileId}, 第 ${page} 页`,
    e.title ? `标题: ${e.title}` : '',
    e.summary ? `摘要: ${e.summary}` : '',
    Array.isArray(e.key_points) ? `关键点:\n- ${e.key_points.join('\n- ')}` : '',
    e.explanation ? `详解:\n${e.explanation}` : '',
    e.gotcha ? `易错点: ${e.gotcha}` : '',
  ].filter(Boolean).join('\n\n');
}

async function askQuestion(qaKey) {
  const safe = safeId(qaKey);
  const ta = document.getElementById('qaInput-' + safe);
  const btn = document.getElementById('qaAskBtn-' + safe);
  const status = document.getElementById('qaStatus-' + safe);
  if (!ta) return;
  const q = (ta.value || '').trim();
  if (!q) { ta.focus(); return; }
  const key = getApiKey();
  if (!key) {
    if (confirm('还没设置 OpenAI API Key，现在设置？')) openSettings();
    return;
  }
  const context = buildContextForKey(qaKey);
  const history = getQA(qaKey);
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
    const list = getQA(qaKey);
    list.push({ q, a: data.answer, ts: Date.now() });
    saveQA(qaKey, list);
    ta.value = '';
    status.textContent = '';
    renderQAList(qaKey);
  } catch (err) {
    status.textContent = '❌ ' + err.message;
    status.className = 'qa-status error';
  } finally {
    btn.disabled = false;
  }
}

function deleteQA(qaKey, idx) {
  const list = getQA(qaKey);
  list.splice(idx, 1);
  saveQA(qaKey, list);
  renderQAList(qaKey);
}

function renderQAList(qaKey) {
  const safe = safeId(qaKey);
  const container = document.getElementById('qaList-' + safe);
  if (!container) return;
  const list = getQA(qaKey);
  if (list.length === 0) { container.innerHTML = ''; return; }
  container.innerHTML = list.map((qa, i) => `
    <div class="qa-item">
      <div class="qa-q"><b>Q:</b> ${escapeHtml(qa.q)}
        <button class="qa-del" onclick="deleteQA('${qaKey.replace(/'/g, "\\'")}', ${i})" title="删除">✕</button>
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

// Wire all Q&A textareas: Cmd/Ctrl + Enter submits
function wireQAShortcuts(rootEl) {
  rootEl.querySelectorAll('[data-qa-key] textarea').forEach(ta => {
    if (ta.dataset.wired) return;
    ta.dataset.wired = '1';
    ta.addEventListener('keydown', ev => {
      if ((ev.metaKey || ev.ctrlKey) && ev.key === 'Enter') {
        const box = ta.closest('[data-qa-key]');
        const key = box?.dataset.qaKey;
        if (key) askQuestion(key);
      }
    });
  });
}

// Render all Q&A lists found in a container (for each data-qa-key element)
function renderAllQAIn(rootEl) {
  rootEl.querySelectorAll('[data-qa-key]').forEach(box => {
    const k = box.dataset.qaKey;
    if (k) renderQAList(k);
  });
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
  // 期中前
  const secA = document.createElement('div');
  secA.className = 'tab section'; secA.textContent = '讲义 · 期中前';
  nav.appendChild(secA);
  FILES.filter(f=>f.premid).forEach(f=>nav.appendChild(mkTab(f)));
  // 期中后
  const secB = document.createElement('div');
  secB.className = 'tab section'; secB.textContent = '讲义 · 期中后';
  nav.appendChild(secB);
  FILES.filter(f=>!f.premid).forEach(f=>nav.appendChild(mkTab(f)));
  // 重点复习
  const secC = document.createElement('div');
  secC.className = 'tab section'; secC.textContent = '重点复习';
  nav.appendChild(secC);
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

    <h3 style="color:var(--accent-2);margin-top:32px">问 AI 助教</h3>
    <p class="subtle">这里是『总课程层面』的 Q&A — 跨章节、考前疑问、对比题。每个 PPT / 题目页本身也有自己的 Q&A 框。</p>
    ${qaWidgetHtml('overview', '问 AI（整门课）')}
  </div>`;
  content.querySelectorAll('.card').forEach(c=>c.onclick = ()=>selectTab(c.dataset.id));
  const overview = content.querySelector('.overview');
  if (overview) {
    renderAllQAIn(overview);
    wireQAShortcuts(overview);
  }
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
      <div class="slide-pane">
        <div class="slide-wrap" id="slideWrap">
          <img id="slide" alt="">
          <div id="slideOverlay" class="slide-overlay"></div>
        </div>
        <div class="slide-tools">
          <button id="hlImgToggle" onclick="toggleImgHL()" title="按下后在 PPT 上拖出黄色高亮框">🖍️ 划框</button>
          <button onclick="clearImgHL()" title="清除本页所有图片高亮">🧹 清空框</button>
          <span class="subtle hl-hint">拖鼠标画框 · 点框删除</span>
        </div>
      </div>
      <div class="explain-pane" id="explain"></div>
    </div>
  `;
  showPage();
  setupImgHL();
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
  const img = document.getElementById('slide');
  img.src = `pages/${currentTab}/p-${pad}.jpg`;
  // explanation
  const arr = EXPL[currentTab] || [];
  const e = arr[currentPage-1];
  renderExplain(e, currentTab, currentPage);
  refreshStarBtn();
  // re-render image highlights for this page (image load event also covers this)
  if (typeof renderImgHL === 'function') renderImgHL();
}

function renderExplain(e, fileId, pageNum) {
  const target = document.getElementById('explain');
  let aiHtml = '';
  // 🔥 important banner at very top
  if (e && e.important) {
    aiHtml += `<div class="important-banner">🔥 <b>重点：</b> ${e.important}</div>`;
  }
  if (!e) {
    aiHtml += `<h2>AI 讲解</h2>
      <p class="skeleton">骨架未生成 — 这一页 AI 讲解还在生成中。</p>
      <p class="subtle">提示：键盘 ← / → 翻页 · S 收藏。</p>`;
  } else {
    aiHtml += `<h2>${e.title || ''}</h2>`;
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
    html += qaWidgetHtml(`${fileId}:${pageNum}`, '问 AI 助教');
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
    renderAllQAIn(target);
    wireQAShortcuts(target);
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
        ${qaWidgetHtml(`final:${i}`, '问 AI（这题）')}
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
  renderAllQAIn(content);
  wireQAShortcuts(content);
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
      ${qaWidgetHtml(`midterm:${i}`, '问 AI（这题）')}
    </div>`;
  });
  const body = document.getElementById('midbody');
  body.innerHTML = html;
  if (window.renderMathInElement) {
    renderMathInElement(body, {
      delimiters: [{left:'$$',right:'$$',display:true},{left:'$', right:'$', display:false}]
    });
  }
  renderAllQAIn(body);
  wireQAShortcuts(body);
}

// ============ Concept Graph ============
function renderConcepts() {
  const content = document.getElementById('content');
  content.innerHTML = `<div class="toolbar">
      <div class="title"><b>🧠 概念知识库</b> <span class="subtle">点击节点查看说明 · 拖动可重新布局 · 右下角 💬 问 AI</span></div>
    </div>
    <div class="graph-help">
      <div>提示：节点颜色 = 所属层；边表示「依赖 / 出自」。点击一个节点，右下角会弹出它的定义和它出现在哪几页。</div>
      <div class="graph-legend">
        <span class="dot" style="background:#3a7c83"></span>期中前
        <span class="dot" style="background:#7aa2ff"></span>Transport (CC)
        <span class="dot" style="background:#a78bfa"></span>Network
        <span class="dot" style="background:#f5c46e"></span>Link
        <span class="dot" style="background:#ff7a8a"></span>Wireless
        <span class="dot" style="background:#8a90a3"></span>其他
      </div>
    </div>
    <div id="graph"><div class="graph-loading">加载中...</div></div>
    <div id="conceptDetail" style="position:absolute;right:20px;bottom:20px;width:380px;max-height:60vh;overflow-y:auto;background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:14px 18px;display:none;box-shadow:0 8px 30px rgba(0,0,0,0.5);"></div>
    <button id="conceptQAToggle" onclick="toggleConceptQA()" title="问 AI 助教" style="position:absolute;right:20px;top:90px;background:var(--accent);color:#0a0c12;border:none;border-radius:50%;width:44px;height:44px;font-size:20px;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,0.4);z-index:5;">💬</button>
    <div id="conceptQAPanel" style="position:absolute;right:20px;top:140px;width:380px;max-height:70vh;overflow-y:auto;background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:14px 18px;display:none;box-shadow:0 8px 30px rgba(0,0,0,0.5);z-index:5;">
      ${qaWidgetHtml('concepts', '问 AI（概念图）')}
    </div>`;
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
      pre_mid:   { color: { background: '#3a7c83', border: '#235257' }, font: { color: '#e6e8ec' } },  // 期中前：深青绿
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
  // wire concept Q&A widget
  const qaPanel = document.getElementById('conceptQAPanel');
  if (qaPanel) {
    renderAllQAIn(qaPanel);
    wireQAShortcuts(qaPanel);
  }
}

function toggleConceptQA() {
  const panel = document.getElementById('conceptQAPanel');
  if (!panel) return;
  panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
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
        <button onclick="cheatInsertAuto()" title="拉取你的收藏 / 笔记 / Q&A / 高亮">📥 拉取笔记</button>
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
      <button title="让 AI 往这个 section 补内容" onclick="cheatLLMAddTo(this); event.stopPropagation();">🤖</button>
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

// LLM-fill a section: prompt user, ask AI to produce dense cheat-sheet HTML, append
async function cheatLLMAddTo(btn) {
  const section = btn.closest('section');
  const apiKey = getApiKey();
  if (!apiKey) {
    if (confirm('还没设置 OpenAI API Key，现在设置？')) openSettings();
    return;
  }
  const userAsk = prompt('要 AI 在这个 section 里加点什么？\n(比如：加个例题 / 加 BGP policy 详解 / 加 5GHz vs 2.4GHz 对比表)');
  if (!userAsk || !userAsk.trim()) return;

  // Get current section text content (strip overlay)
  const clone = section.cloneNode(true);
  clone.querySelectorAll('.section-overlay').forEach(o => o.remove());
  const currentText = clone.innerText.trim().slice(0, 800);

  const status = section.querySelector('.llm-status') || (() => {
    const s = document.createElement('div');
    s.className = 'llm-status subtle';
    s.contentEditable = 'false';
    s.style.cssText = 'font-size:7pt;color:#666;margin-top:1mm;font-style:italic;';
    section.insertBefore(s, section.querySelector('.section-overlay'));
    return s;
  })();
  status.textContent = '🤖 思考中…';

  const context = `这是 COMS 4119 cheat sheet 的一个 section。

当前 section 内容：
${currentText}

学生要求：${userAsk}

请直接返回要追加到这个 section 的 HTML 片段（不要 <section> 包裹，可以用 <p> <ul> <li> <table> <b> <code>）。
要求：极度紧凑、cheat-sheet 风格、英文为主（除非用户特别要中文）、用 KaTeX 数学公式（$...$ 形式）、表格用最少列。最多 150 字。`;

  try {
    const resp = await fetch('/api/ask', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        question: userAsk,
        context,
        history: [],
        apiKey,
      }),
    });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || 'unknown error');

    // Insert AI response before overlay
    const wrap = document.createElement('div');
    wrap.className = 'ai-addition';
    wrap.contentEditable = 'true';
    // Try to detect if response is HTML; else treat as markdown
    let html = data.answer || '';
    if (!/<\w+/.test(html)) {
      // markdown → HTML
      html = marked.parse(html);
    }
    wrap.innerHTML = html;
    const overlay = section.querySelector('.section-overlay');
    section.insertBefore(wrap, overlay);

    if (window.renderMathInElement) {
      renderMathInElement(wrap, { delimiters: [
        {left:'$$', right:'$$', display: true},
        {left:'$', right:'$', display: false}
      ]});
    }
    status.remove();
    saveCheatSheet();
  } catch (err) {
    status.textContent = '❌ ' + err.message;
    status.style.color = 'red';
    setTimeout(() => status.remove(), 5000);
  }
}

// Insert a Pre-Midterm sheet packed with pre-mid content (app/transport up to flow control)
function cheatInsertPreMid() {
  const host = document.getElementById('cheatHost');
  if (!host) return;
  const sheet = document.createElement('div');
  sheet.className = 'sheet pre-mid-sheet';
  sheet.innerHTML = `<h1>COMS 4119 — PRE-MIDTERM REVIEW</h1><div class="cols">
<section><h2>HTTP Sockets <span class="tag">mid Q1</span></h2>
<ul>
<li>UDP server: <b>1 socket</b> (connectionless)</li>
<li>TCP server: <b>N+1</b> sockets (welcome + per-client)</li>
<li>UDP distinguishes clients via (src IP, port)</li>
</ul></section>

<section><h2>HTTP RTT Counting <span class="tag">mid Q1</span></h2>
<ul>
<li>Non-persistent: <b>2 RTT/obj</b> (TCP setup + GET)</li>
<li>Persistent + pipelined: 2 RTT for base, +1 per nesting layer</li>
<li>Example: HTML + 4 jpg + 1 css(2 jpg) = <b>4 RTT</b></li>
</ul></section>

<section><h2>HTTP Persistence</h2>
<ul>
<li>Non-persistent (HTTP/1.0): new TCP per object</li>
<li>Persistent (HTTP/1.1): reuse TCP for all objects</li>
<li>Pipelining: send next request before previous response</li>
<li>Cookie: stateless HTTP + server-side state</li>
</ul></section>

<section><h2>Web Cache (Proxy)</h2>
<ul>
<li>Proxy caches HTTP responses; cuts RTT + bandwidth</li>
<li>Consistency: <b>Conditional GET</b> with If-Modified-Since</li>
<li>Server responds 304 Not Modified (no body) if unchanged</li>
</ul></section>

<section><h2>DNS Hierarchy</h2>
<ul>
<li>local resolver → root → TLD(.com, .edu) → authoritative</li>
<li>Recursive (resolve for me) vs iterative (tell me next hop)</li>
<li>RR types: A (IPv4), AAAA (IPv6), NS, MX, CNAME</li>
<li>UDP 53; falls back to TCP for large responses</li>
</ul></section>

<section><h2>P2P File Distribution <span class="tag">mid Q6</span></h2>
<div class="formula">CS:  T = max(NF/U_s, F/d_min)</div>
<div class="formula">P2P: T = max(F/U_s, F/d_min, NF/(U_s + ΣU_i))</div>
<ul>
<li>Server upload is multiplied by N in CS, NOT in P2P</li>
<li>P2P scales: more peers = more total upload BW</li>
<li>For 1GB / 100 users, 40Mbps server: CS = 20000s, P2P ≈ 1000s</li>
</ul></section>

<section><h2>BitTorrent Mechanics</h2>
<ul>
<li><b>Rarest first</b>: prioritize chunks scarce in the swarm</li>
<li><b>Tit-for-tat</b>: upload to those who upload to you</li>
<li><b>Optimistic unchoke</b>: every ~30s give bw to a new peer (explore)</li>
<li><b>DHT</b>: distributed hash table replaces central tracker</li>
</ul></section>

<section><h2>Performance Metrics <span class="tag">mid Q2 Q4</span></h2>
<ul>
<li><b>Trans</b> delay = L/R; <b>Prop</b> delay = d/v</li>
<li>Light c = 3·10⁸ m/s; sound = 1.5 km/s</li>
<li>End-to-end = Σ per link (L/R + d/v) + queuing</li>
<li>Pipelined N pkts: 1st pkt full path + (N−1)·<span class="red">bottleneck</span> tx</li>
<li>Throughput = min(per-link R) = bottleneck</li>
</ul></section>

<section><h2>BDP — Bandwidth-Delay Product</h2>
<div class="formula">BDP = R · RTT  (bits in pipe)</div>
<ul>
<li>Window size must ≥ BDP to keep pipe full</li>
<li>Example: 30 Kbps × 80 ms = 2400 bits</li>
</ul></section>

<section><h2>Stop-and-Wait U <span class="tag">mid Q5</span></h2>
<div class="formula">U = T_trans / (T_trans + 2·T_prop)</div>
<ul>
<li>Bad when L small or RTT large (T_trans ≪ T_prop)</li>
<li>Example: 2 Kb @ 40 Kbps over 30m acoustic + 3km air → U ≈ 0.54; @ 200b → 0.11</li>
<li><b>Fix</b>: sliding window with size ≥ BDP</li>
</ul></section>

<section><h2>Sliding Window</h2>
<ul>
<li>Sender maintains window [base, base+N)</li>
<li>Can send any unACKed packet in window without waiting</li>
<li>ACK arrives → base slides forward</li>
<li>Stop-and-wait = window of 1 (special case)</li>
</ul></section>

<section><h2>UDP vs TCP</h2>
<table>
<tr><th></th><th>UDP</th><th>TCP</th></tr>
<tr><td>conn</td><td>none</td><td>3WHS</td></tr>
<tr><td>reliable</td><td>no</td><td>yes</td></tr>
<tr><td>order</td><td>no</td><td>yes</td></tr>
<tr><td>flow ctrl</td><td>no</td><td>rwnd</td></tr>
<tr><td>hdr</td><td>8 B</td><td>20 B</td></tr>
<tr><td>uses</td><td>DNS, RTP, DHCP</td><td>HTTP, SSH</td></tr>
</table></section>

<section><h2>TCP Segment</h2>
<ul>
<li>Src/dst port (16b each)</li>
<li>Seq #: first byte of data (32b)</li>
<li>ACK #: next expected byte (32b)</li>
<li>HLEN, flags: SYN/FIN/ACK/RST/PSH/URG/CWR/ECE</li>
<li><b>Receive window</b> (16b): rwnd, for flow control</li>
<li>Checksum (16b)</li>
</ul></section>

<section><h2>TCP 3WHS &amp; 4-Way Close</h2>
<ol>
<li><b>SYN</b> seq=x</li>
<li><b>SYN-ACK</b> seq=y ack=x+1</li>
<li><b>ACK</b> seq=x+1 ack=y+1</li>
</ol>
<p>Close = 4-way (FIN/ACK each direction). TIME_WAIT 2·MSL.</p></section>

<section><h2>RDT: GBN vs SR <span class="tag">mid Q3</span></h2>
<table>
<tr><th></th><th>GBN</th><th>SR</th></tr>
<tr><td>ACK</td><td>cumulative</td><td>per-packet</td></tr>
<tr><td>Loss</td><td>resend window</td><td>resend just lost</td></tr>
<tr><td>Data-loss heavy</td><td>bad</td><td><span class="green">good</span></td></tr>
<tr><td>ACK-loss heavy</td><td><span class="green">good</span></td><td>bad</td></tr>
<tr><td>Rcvr buffer</td><td>none</td><td>required</td></tr>
</table>
<p class="mini">SR window ≤ N/2 (seq space)</p></section>

<section><h2>TCP Reliable Mechanisms</h2>
<ul>
<li><b>Timeout retransmit</b>: TimeoutInterval = EstRTT + 4·DevRTT</li>
<li>EstRTT = (1−α)·EstRTT + α·SampleRTT, α=0.125</li>
<li>DevRTT = (1−β)·DevRTT + β·|SampleRTT−EstRTT|, β=0.25</li>
<li><b>Fast retransmit</b>: 3 dup ACKs trigger immediate resend</li>
<li>Exponential backoff after timeout</li>
</ul></section>

<section><h2>TCP Flow Control <span class="tag">mid Q5</span></h2>
<ul>
<li>Receiver advertises <b>rwnd</b> in every ACK</li>
<li>Sender's inflight ≤ min(cwnd, rwnd)</li>
<li>SR receive buffer holds out-of-order pkts; if packet 1 lost + 2,3,4 occupy buffer → 5+ get dropped</li>
<li><b>Advertise rwnd = buffer size</b>, not larger</li>
</ul></section>

<section><h2>RDT Evolution (1.0 → 3.0)</h2>
<ul>
<li><b>1.0</b>: perfect channel (useless)</li>
<li><b>2.0</b>: + ACK/NAK + checksum (handles bit errors)</li>
<li><b>2.1</b>: + seq # (handles ACK corruption)</li>
<li><b>2.2</b>: NAK-free (use ACK + last good seq)</li>
<li><b>3.0</b>: + timer (handles packet loss) — stop-and-wait</li>
<li>Pipelined: GBN / SR</li>
</ul></section>

<section><h2>Pre-Mid Exam Pitfalls</h2>
<ul>
<li>UDP server: <b>1</b> socket (not N+1)</li>
<li>TCP server: <b>N+1</b> (welcome + per-client)</li>
<li>Non-persistent HTTP: <b>×2 RTT</b> per object (setup + GET)</li>
<li>Pipelining N pkts: bottleneck × (N−1)</li>
<li>RTT not just propagation — include trans delay if asked</li>
<li>Stop-and-wait U denominator: <b>T_trans + 2·T_prop</b></li>
<li>SR receive buffer: out-of-order stuck → drops later pkts</li>
<li>BT vs CS: server upload multiplied by N only in CS</li>
</ul></section>

</div>`;
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

// ============ Image Highlights (draw rects on PPT image) ============
const KEY_IMGHL = '4119:imghl'; // map "fileId:page" -> [{x,y,w,h}] normalized 0-1

function loadImgHLMap() {
  try { return JSON.parse(localStorage.getItem(KEY_IMGHL) || '{}'); }
  catch { return {}; }
}
function getImgHL(fileId, page) {
  return loadImgHLMap()[`${fileId}:${page}`] || [];
}
function saveImgHL(fileId, page, list) {
  const m = loadImgHLMap();
  m[`${fileId}:${page}`] = list;
  localStorage.setItem(KEY_IMGHL, JSON.stringify(m));
}
function clearImgHL() {
  if (!confirm('清空这一页所有图片高亮框?')) return;
  saveImgHL(currentTab, currentPage, []);
  renderImgHL();
}

let _hlActive = false;
function toggleImgHL() {
  _hlActive = !_hlActive;
  const btn = document.getElementById('hlImgToggle');
  if (btn) {
    btn.classList.toggle('active', _hlActive);
    btn.innerHTML = _hlActive ? '✖ 退出划框' : '🖍️ 划框';
  }
  const wrap = document.getElementById('slideWrap');
  if (wrap) wrap.classList.toggle('hl-drawing', _hlActive);
}

function renderImgHL() {
  const overlay = document.getElementById('slideOverlay');
  if (!overlay) return;
  overlay.innerHTML = '';
  const list = getImgHL(currentTab, currentPage);
  list.forEach((r, idx) => {
    const box = document.createElement('div');
    box.className = 'imghl-box';
    box.style.left = (r.x * 100) + '%';
    box.style.top = (r.y * 100) + '%';
    box.style.width = (r.w * 100) + '%';
    box.style.height = (r.h * 100) + '%';
    box.title = '点击删除';
    box.onclick = (ev) => {
      ev.stopPropagation();
      const cur = getImgHL(currentTab, currentPage);
      cur.splice(idx, 1);
      saveImgHL(currentTab, currentPage, cur);
      renderImgHL();
    };
    overlay.appendChild(box);
  });
}

function setupImgHL() {
  const overlay = document.getElementById('slideOverlay');
  const img = document.getElementById('slide');
  if (!overlay || !img) return;
  // re-render highlights when image loads / changes
  img.addEventListener('load', renderImgHL);
  if (img.complete) renderImgHL();

  let drawing = null;
  overlay.addEventListener('mousedown', ev => {
    if (!_hlActive) return;
    ev.preventDefault();
    const rect = overlay.getBoundingClientRect();
    const x = (ev.clientX - rect.left) / rect.width;
    const y = (ev.clientY - rect.top) / rect.height;
    drawing = { startX: x, startY: y };
    const ghost = document.createElement('div');
    ghost.className = 'imghl-box ghost';
    ghost.id = '__hlghost';
    overlay.appendChild(ghost);
  });
  overlay.addEventListener('mousemove', ev => {
    if (!drawing) return;
    const rect = overlay.getBoundingClientRect();
    const x = (ev.clientX - rect.left) / rect.width;
    const y = (ev.clientY - rect.top) / rect.height;
    const ghost = document.getElementById('__hlghost');
    if (!ghost) return;
    const left = Math.min(drawing.startX, x);
    const top = Math.min(drawing.startY, y);
    const w = Math.abs(x - drawing.startX);
    const h = Math.abs(y - drawing.startY);
    ghost.style.left = (left * 100) + '%';
    ghost.style.top = (top * 100) + '%';
    ghost.style.width = (w * 100) + '%';
    ghost.style.height = (h * 100) + '%';
  });
  overlay.addEventListener('mouseup', ev => {
    if (!drawing) return;
    const rect = overlay.getBoundingClientRect();
    const x = (ev.clientX - rect.left) / rect.width;
    const y = (ev.clientY - rect.top) / rect.height;
    const left = Math.min(drawing.startX, x);
    const top = Math.min(drawing.startY, y);
    const w = Math.abs(x - drawing.startX);
    const h = Math.abs(y - drawing.startY);
    drawing = null;
    document.getElementById('__hlghost')?.remove();
    if (w > 0.01 && h > 0.01) {
      const list = getImgHL(currentTab, currentPage);
      list.push({ x: left, y: top, w, h });
      saveImgHL(currentTab, currentPage, list);
      renderImgHL();
    }
  });
  overlay.addEventListener('mouseleave', () => {
    drawing = null;
    document.getElementById('__hlghost')?.remove();
  });
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
