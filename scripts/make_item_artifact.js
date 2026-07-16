#!/usr/bin/env node
/**
 * make_item_artifact.js
 * 아이템 아이콘 전후 비교 자기완결 HTML(이미지 base64 임베드) 생성 → 아티팩트용.
 * 출력: 인자로 받은 경로(기본 scratchpad).
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const OUT = process.argv[2] || path.join(ROOT, 'item_icons_qa.html');

const items = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'quiz_items.json'), 'utf8'));

const CAT_KO = { 'held-items': '지닌도구', 'type-enhancement': '타입강화', 'type-protection': '타입보호',
  jewels: '주얼', choice: '구애', 'bad-held-items': '역효과도구', 'in-a-pinch': '위기도구',
  plates: '플레이트', memories: '메모리', 'species-specific': '전용도구', 'z-crystals': 'Z크리스탈',
  evolution: '진화도구', healing: '회복', 'status-cures': '상태회복', vitamins: '영양제', scarves: '목걸이',
  fossil: '화석', 'for-sell': '판매용', other: '기타', revival: '부활', 'pp-recovery': 'PP회복',
  'stat-boosts': '능력상승', 'effort-training': '노력치', 'effort-drop': '노력치감소', training: '트레이닝',
  flutes: '비드로', spelunking: '동굴탐험', medicine: '약', 'picky-healing': '까다로운회복',
  'type-enhancement': '타입강화', 'status-cures': '상태회복' };

function b64(rel) {
  const p = path.join(ROOT, rel);
  if (!fs.existsSync(p)) return null;
  return 'data:image/png;base64,' + fs.readFileSync(p).toString('base64');
}

const cards = [];
let hi = 0;
for (const it of items) {
  const newRel = `sprites/items/bulba__${it.en}.png`;
  if (!fs.existsSync(path.join(ROOT, newRel))) continue;
  const oldData = b64(it.sprite);
  const newData = b64(newRel);
  if (!newData) continue;
  hi++;
  const cat = CAT_KO[it.category] || it.category;
  cards.push(`<figure class="card" data-cat="${it.category}">
  <div class="pair">
    <div class="cell old"><img src="${oldData || ''}" alt="" loading="lazy"><span>기존</span></div>
    <div class="arrow">→</div>
    <div class="cell new"><img src="${newData}" alt="" loading="lazy"><span>HD</span></div>
  </div>
  <figcaption>${it.ko}</figcaption>
  <div class="chip">${cat}</div>
</figure>`);
}

// 카테고리 필터 목록
const cats = [...new Set(items
  .filter(it => fs.existsSync(path.join(ROOT, `sprites/items/bulba__${it.en}.png`)))
  .map(it => it.category))];
const catBtns = ['<button class="f-btn active" data-f="all">전체 ' + hi + '</button>']
  .concat(cats.sort().map(c => `<button class="f-btn" data-f="${c}">${CAT_KO[c] || c}</button>`))
  .join('');

const html = `<title>포케노바 · 아이템 아이콘 화질 비교</title>
<style>
  :root{
    --bg:#0f1113; --panel:#17191c; --panel-2:#1e2126; --line:#2a2e34;
    --ink:#eceef0; --muted:#8b9198; --faint:#5b616a;
    --ball:#e63946; --new:#4caf6a; --new-dim:#2c6b42;
  }
  *{box-sizing:border-box}
  body{margin:0;background:
      radial-gradient(1200px 600px at 50% -10%, #1a1d21 0%, var(--bg) 60%);
    color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
    -webkit-font-smoothing:antialiased;padding-bottom:60px}
  header{position:sticky;top:0;z-index:5;padding:18px 20px 14px;
    background:rgba(15,17,19,.82);backdrop-filter:blur(10px);
    border-bottom:1px solid var(--line)}
  .title{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
  h1{font-size:1.05rem;font-weight:700;margin:0;letter-spacing:-.01em}
  .lead{color:var(--muted);font-size:.82rem}
  .lead b{color:var(--new);font-variant-numeric:tabular-nums}
  .filters{display:flex;gap:6px;flex-wrap:wrap;margin-top:12px}
  .f-btn{font:inherit;font-size:.74rem;color:var(--muted);background:var(--panel-2);
    border:1px solid var(--line);border-radius:999px;padding:5px 11px;cursor:pointer;
    transition:.12s}
  .f-btn:hover{color:var(--ink);border-color:#3a3f47}
  .f-btn.active{color:#fff;background:var(--ball);border-color:var(--ball)}
  .f-btn:focus-visible{outline:2px solid var(--new);outline-offset:2px}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(158px,1fr));
    gap:12px;padding:18px 20px;max-width:1400px;margin:0 auto}
  .card{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:12px;
    padding:12px 10px 10px;text-align:center;display:flex;flex-direction:column;gap:8px}
  .pair{display:flex;align-items:center;justify-content:center;gap:6px}
  .cell{display:flex;flex-direction:column;align-items:center;gap:3px;flex:1}
  .cell img{width:60px;height:60px;object-fit:contain;
    background:#0a0b0c;border-radius:8px;padding:4px}
  .cell.old img{image-rendering:auto;opacity:.92}
  .cell.new img{outline:1.5px solid var(--new-dim)}
  .cell span{font-size:.6rem;letter-spacing:.06em;text-transform:uppercase;color:var(--faint)}
  .cell.new span{color:var(--new)}
  .arrow{color:var(--faint);font-size:.9rem}
  figcaption{font-size:.86rem;font-weight:600;line-height:1.2}
  .chip{font-size:.66rem;color:var(--muted);background:var(--panel-2);
    border-radius:6px;padding:2px 7px;align-self:center}
  footer{color:var(--faint);font-size:.72rem;text-align:center;padding:0 20px;margin-top:6px}
</style>
<header>
  <div class="title">
    <h1>🔴 포케노바 · 아이템 아이콘 화질 비교</h1>
    <span class="lead">기존 30px → 신규 Bulbapedia HD 160px · <b>${hi}개</b> 교체 예정</span>
  </div>
  <div class="filters">${catBtns}</div>
</header>
<main class="grid" id="grid">
${cards.join('\n')}
</main>
<footer>왼쪽=현재 스프라이트 · 오른쪽=적용 예정 HD(초록 테두리) · 여기 없는 아이템(구세대·화석·Z크리스탈 등)은 HD 소스가 없어 그대로 유지돼요.</footer>
<script>
  const grid=document.getElementById('grid');
  document.querySelectorAll('.f-btn').forEach(b=>b.addEventListener('click',()=>{
    document.querySelectorAll('.f-btn').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    const f=b.dataset.f;
    grid.querySelectorAll('.card').forEach(c=>{
      c.style.display = (f==='all'||c.dataset.cat===f)?'':'none';
    });
  }));
</script>`;

fs.writeFileSync(OUT, html);
const kb = Math.round(fs.statSync(OUT).size / 1024);
console.log(`✓ ${OUT} 생성 (${hi}개 카드, ${kb}KB)`);
