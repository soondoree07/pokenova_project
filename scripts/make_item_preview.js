#!/usr/bin/env node
/**
 * make_item_preview.js
 * 아이템 아이콘 전후(기존 30px vs 새 Bulbapedia 160px) 비교 미리보기 HTML 생성.
 * 새 이미지 존재 여부 = sprites/items/bulba__<en>.png 파일 유무로 판단.
 * 출력: preview_items.html (프로젝트 루트, 커밋 안 함)
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const items = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'quiz_items.json'), 'utf8'));

const CAT_KO = { 'held-items': '지닌도구', 'type-enhancement': '타입강화', 'type-protection': '타입보호',
  jewels: '주얼', choice: '구애', 'bad-held-items': '나쁜지닌도구', 'in-a-pinch': '위기지닌도구',
  plates: '플레이트', memories: '메모리', 'species-specific': '전용도구', 'z-crystals': 'Z크리스탈',
  evolution: '진화', healing: '회복', 'status-cures': '상태회복', vitamins: '영양제', scarves: '목걸이',
  fossil: '화석', 'for-sell': '판매용', other: '기타' };

const rows = [];
let hiCount = 0;
for (const it of items) {
  const newFile = `sprites/items/bulba__${it.en}.png`;
  const has = fs.existsSync(path.join(ROOT, newFile));
  if (has) hiCount++;
  rows.push({ ...it, newFile: has ? newFile : null });
}
// HI 있는 것만, 카테고리별 정렬
const shown = rows.filter(r => r.newFile).sort((a, b) => (a.category + a.ko).localeCompare(b.category + b.ko));

const cards = shown.map(r => `
  <div class="card">
    <div class="pair">
      <figure><img src="${r.sprite}" loading="lazy"><figcaption>기존</figcaption></figure>
      <figure><img src="${r.newFile}" loading="lazy" class="new"><figcaption>신규 HD</figcaption></figure>
    </div>
    <div class="name">${r.ko}</div>
    <div class="cat">${CAT_KO[r.category] || r.category}</div>
  </div>`).join('');

const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>아이템 아이콘 전후 비교 (${hiCount}개)</title>
<style>
  body{background:#111;color:#eee;font-family:system-ui,sans-serif;margin:0;padding:20px}
  h1{font-size:1.1rem}
  .sub{color:#888;font-size:.85rem;margin-bottom:16px}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px}
  .card{background:#1b1b1b;border:1px solid #2a2a2a;border-radius:10px;padding:10px;text-align:center}
  .pair{display:flex;justify-content:center;gap:10px;align-items:flex-end}
  figure{margin:0}
  figure img{width:56px;height:56px;object-fit:contain;image-rendering:auto;background:#000;border-radius:6px}
  figure img.new{outline:2px solid #2e7d32}
  figcaption{font-size:.65rem;color:#777;margin-top:3px}
  .name{margin-top:8px;font-size:.85rem;font-weight:600}
  .cat{font-size:.7rem;color:#888}
</style></head><body>
<h1>아이템 아이콘 전후 비교</h1>
<div class="sub">고화질 교체 대상 ${hiCount}개 · 왼쪽=기존(30px) / 오른쪽=신규 Bulbapedia HD(160px, 초록테두리)</div>
<div class="grid">${cards}</div>
</body></html>`;

fs.writeFileSync(path.join(ROOT, 'preview_items.html'), html);
console.log(`✓ preview_items.html 생성 (HD ${hiCount}개 표시)`);
console.log(`  브라우저에서 열기: file://${path.join(ROOT, 'preview_items.html')}`);
