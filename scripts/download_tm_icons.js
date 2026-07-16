#!/usr/bin/env node
/**
 * download_tm_icons.js
 * 기술머신(all-machines) 108개를 SV 타입별 디스크 아이콘(160px HD)으로 교체.
 * - desc "…에게 <기술명>을/를 가르친다" 에서 기술명 추출
 * - quiz_moves.json 에서 기술 → type_en 조회
 * - Bulbapedia Bag_TM_<Type>_SV_Sprite.png (타입당 1개) 다운로드 → bulba__tm_<type>.png
 * - quiz_items.json 각 기술머신 sprite 를 해당 타입 파일로 지정
 */
const fs = require('fs');
const path = require('path');
const https = require('https');

const ROOT = path.join(__dirname, '..');
const ITEMS = path.join(ROOT, 'data', 'quiz_items.json');
const MOVES = path.join(ROOT, 'data', 'quiz_moves.json');
const OUT_DIR = path.join(ROOT, 'sprites', 'items');
const UA = 'Mozilla/5.0 (pokenova-tm-icons)';
const dry = process.argv.includes('--dry');

function fetchBuf(url, r = 0) {
  return new Promise((res, rej) => {
    if (r > 5) return rej(new Error('redirects'));
    https.get(url, { headers: { 'User-Agent': UA }, timeout: 20000 }, rs => {
      if ([301, 302, 303, 307, 308].includes(rs.statusCode)) {
        rs.resume(); const loc = rs.headers.location;
        return fetchBuf(loc.startsWith('http') ? loc : new URL(loc, url).href, r + 1).then(res, rej);
      }
      if (rs.statusCode !== 200) { rs.resume(); return rej(new Error('HTTP ' + rs.statusCode)); }
      const c = []; rs.on('data', x => c.push(x)); rs.on('end', () => res(Buffer.concat(c)));
    }).on('error', rej).on('timeout', function () { this.destroy(new Error('timeout')); });
  });
}
const isPng = b => b.length > 24 && b.slice(1, 4).toString() === 'PNG';
const cap = s => s.charAt(0).toUpperCase() + s.slice(1);

// 기술머신 desc의 기술명이 quiz_moves 표기와 다른 경우 별칭
const MOVE_ALIAS = { '드래곤크루': '드래곤클로', '섀도크루': '섀도클로', '깨트리다': '깨트리기' };

function moveNameFromDesc(desc) {
  const m = (desc || '').match(/에게\s*(.+?)[을를]\s*가르친다/);
  if (!m) return null;
  const name = m[1].trim();
  return MOVE_ALIAS[name] || name;
}

async function main() {
  const items = JSON.parse(fs.readFileSync(ITEMS, 'utf8'));
  const moves = JSON.parse(fs.readFileSync(MOVES, 'utf8'));
  const moveByKo = new Map(moves.map(m => [m.ko, m]));

  const tms = items.filter(it => it.category === 'all-machines');
  console.log(`기술머신 ${tms.length}개 처리\n`);

  // 1) 각 TM → type_en 매핑
  const need = new Set();       // 필요한 type_en 집합
  const tmType = new Map();     // it.en → type_en
  const misses = [];
  for (const it of tms) {
    const mv = moveNameFromDesc(it.desc);
    const move = mv ? moveByKo.get(mv) : null;
    if (!move || !move.type_en) { misses.push(`${it.en} (${it.ko}) desc="${mv}"`); continue; }
    tmType.set(it.en, move.type_en);
    need.add(move.type_en);
  }
  console.log(`타입 매핑 성공 ${tmType.size} / 실패 ${misses.length}`);
  console.log(`필요 타입 ${need.size}종: ${[...need].join(', ')}\n`);
  if (misses.length) { console.log('[매핑 실패]'); misses.forEach(m => console.log('  ' + m)); console.log(); }

  // 2) 타입별 디스크 다운로드 (타입당 1개)
  const typeFile = new Map(); // type_en → 로컬 상대경로
  for (const t of need) {
    const fn = `bulba__tm_${t}.png`;
    const dest = path.join(OUT_DIR, fn);
    if (!dry) {
      try {
        const buf = await fetchBuf(`https://archives.bulbagarden.net/w/index.php?title=Special:Redirect/file/Bag_TM_${cap(t)}_SV_Sprite.png`);
        if (!isPng(buf)) { console.log(`  ✗ ${t}: PNG 아님`); continue; }
        fs.writeFileSync(dest, buf);
      } catch (e) { console.log(`  ✗ ${t}: ${e.message}`); continue; }
    }
    typeFile.set(t, `sprites/items/${fn}`);
  }
  console.log(`타입 디스크 확보 ${typeFile.size}/${need.size}종`);

  // 3) quiz_items.json 갱신
  let applied = 0;
  for (const it of tms) {
    const t = tmType.get(it.en);
    const rel = t && typeFile.get(t);
    if (rel) { it.sprite = rel; applied++; }
  }
  if (!dry) {
    fs.writeFileSync(ITEMS, JSON.stringify(items, null, 2));
    console.log(`\n✓ quiz_items.json 갱신 — 기술머신 ${applied}/${tms.length}개 HD 적용`);
  } else {
    console.log(`\n(dry) 적용 예정 ${applied}/${tms.length}개`);
  }
}
main().catch(e => { console.error('오류:', e); process.exit(1); });
