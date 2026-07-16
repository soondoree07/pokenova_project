#!/usr/bin/env node
/**
 * download_hires_items.js
 * 저해상도(30x30 등) 아이템 아이콘을 Bulbapedia 고화질(주로 160x160) 스프라이트로 교체한다.
 *
 * 소스: Bulbapedia 파일 Bag_<이름>_<세대>_Sprite.png
 *   - Special:Redirect/file/<파일명> 로 해시경로 몰라도 받을 수 있다.
 * 매칭: 아이템 en(snake_case) → 여러 파일명 후보를 순서대로 시도, 첫 유효 PNG 채택.
 *   - 유효 = PNG 매직바이트 + 가로>=MIN_W. 작은 것만 있으면 그거라도 채택(fallback).
 *
 * 사용:
 *   node scripts/download_hires_items.js --sample 20     # 샘플만 (다운로드 저장O, JSON수정X)
 *   node scripts/download_hires_items.js                 # 전체 (다운로드 + JSON 갱신)
 *   node scripts/download_hires_items.js --dry           # 전체 시도하되 JSON 저장 안 함
 * 옵션:
 *   --sample N   앞에서 N개만 (JSON 미수정, 적중률 측정용)
 *   --dry        JSON 저장 안 함
 *   --report FILE  결과 JSON 리포트 저장 경로
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const ROOT = path.join(__dirname, '..');
const ITEMS_JSON = path.join(ROOT, 'data', 'quiz_items.json');
const OUT_DIR = path.join(ROOT, 'sprites', 'items');
const MIN_W = 120;              // 이보다 크면 '고화질'로 인정
const CONCURRENCY = 4;          // Bulbapedia 예의상 낮게
const UA = 'Mozilla/5.0 (pokenova-sprite-updater)';

// 제외 카테고리: 이미 고화질(볼) / 사용자 만족(메가스톤) / 별도매핑 필요(기술머신 타입디스크)
const SKIP_CATEGORIES = new Set([
  'standard-balls', 'special-balls', 'apricorn-balls', 'mega-stones', 'all-machines',
]);

// 약어는 전부 대문자로 (hp → HP)
const ACRONYMS = new Set(['hp', 'pp', 'tm', 'tr', 'ev', 'iv']);

// Bulbapedia 파일명이 규칙과 다른 아이템: en → 베이스 이름(밑줄)들. 여러 후보 허용.
const ALIAS_BASE = {
  hp_up: ['HP_Up'],
  guard_spec: ['Guard_Spec.', 'Guard_Spec'],
  exp_share: ['Exp._Share', 'Exp.Share', 'Exp_Share'],
  pp_up: ['PP_Up'],
  pp_max: ['PP_Max'],
  x_attack: ['X_Attack'], x_defense: ['X_Defense'], x_sp_atk: ['X_Sp._Atk'],
  x_sp_def: ['X_Sp._Def'], x_speed: ['X_Speed'], x_accuracy: ['X_Accuracy'],
  never_melt_ice: ['Never-Melt_Ice', 'NeverMeltIce'],
  bright_powder: ['BrightPowder', 'Bright_Powder'],
};

// ── args
const args = process.argv.slice(2);
const sampleN = args.includes('--sample') ? parseInt(args[args.indexOf('--sample') + 1], 10) : null;
const dry = args.includes('--dry') || sampleN != null;        // 다운로드 X, JSON X
const imagesOnly = args.includes('--images-only');            // 다운로드 O, JSON X (확인용)
const reportPath = args.includes('--report') ? args[args.indexOf('--report') + 1] : null;

// ── 이름 후보 생성
function titleWords(en) {           // bright_powder → ['Bright','Powder'], hp_up → ['HP','Up']
  return en.split(/[_\s-]+/).filter(Boolean)
    .map(w => ACRONYMS.has(w) ? w.toUpperCase() : w.charAt(0).toUpperCase() + w.slice(1));
}
function candidateFilenames(en) {
  const w = titleWords(en);
  const spaced = w.join('_');       // Bright_Powder
  const joined = w.join('');        // BrightPowder
  const bases = [];
  if (ALIAS_BASE[en]) bases.push(...ALIAS_BASE[en]);   // 별칭 우선
  bases.push(spaced);
  if (joined !== spaced) bases.push(joined);
  // 세대 접미사: 최신순 SV → HOME → SwSh → LA → 무접미(구버전). 고화질은 SV/HOME에 몰려있다.
  const gens = ['SV', 'HOME', 'SwSh', 'LA', ''];
  const names = [];
  for (const g of gens) {
    for (const base of bases) {
      names.push(g ? `Bag_${base}_${g}_Sprite.png` : `Bag_${base}_Sprite.png`);
    }
  }
  return [...new Set(names)];
}

function bulbaUrl(file) {
  return `https://archives.bulbagarden.net/w/index.php?title=Special:Redirect/file/${encodeURIComponent(file)}`;
}

// ── 다운로드 (버퍼로 받아 PNG 검증)
function fetchBuf(url, redirects = 0) {
  return new Promise((resolve, reject) => {
    if (redirects > 5) return reject(new Error('too many redirects'));
    https.get(url, { headers: { 'User-Agent': UA }, timeout: 20000 }, res => {
      if ([301, 302, 303, 307, 308].includes(res.statusCode)) {
        res.resume();
        const loc = res.headers.location;
        const next = loc.startsWith('http') ? loc : new URL(loc, url).href;
        return fetchBuf(next, redirects + 1).then(resolve, reject);
      }
      if (res.statusCode !== 200) { res.resume(); return reject(new Error('HTTP ' + res.statusCode)); }
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => resolve(Buffer.concat(chunks)));
    }).on('error', reject).on('timeout', function () { this.destroy(new Error('timeout')); });
  });
}

function pngSize(buf) {
  if (buf.length < 24 || buf.slice(1, 4).toString() !== 'PNG') return null;
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}

// 아이템 하나에 대해 최선의 스프라이트를 찾는다.
async function resolveItem(it) {
  const cands = candidateFilenames(it.en);
  let best = null; // {buf,file,w,h}
  for (const file of cands) {
    let buf;
    try { buf = await fetchBuf(bulbaUrl(file)); }
    catch { continue; }
    const s = pngSize(buf);
    if (!s) continue;
    if (!best || s.w > best.w) best = { buf, file, w: s.w, h: s.h };
    if (s.w >= MIN_W) break;         // 고화질 찾으면 즉시 종료
  }
  return best;
}

async function main() {
  const items = JSON.parse(fs.readFileSync(ITEMS_JSON, 'utf8'));
  let targets = items.filter(it => it.en && !SKIP_CATEGORIES.has(it.category));
  if (sampleN != null) {
    // 카테고리 다양성 있게 앞에서 고르게 샘플
    const byCat = {};
    for (const it of targets) (byCat[it.category] ||= []).push(it);
    const picked = [];
    const cats = Object.keys(byCat);
    let i = 0;
    while (picked.length < sampleN && cats.some(c => byCat[c].length)) {
      const c = cats[i % cats.length]; i++;
      if (byCat[c].length) picked.push(byCat[c].shift());
    }
    targets = picked;
  }

  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  console.log(`대상 아이템: ${targets.length}개  (dry=${dry})\n`);
  const results = [];
  let idx = 0, hi = 0, lo = 0, miss = 0;

  async function worker() {
    while (true) {
      const i = idx++;
      if (i >= targets.length) break;
      const it = targets[i];
      const best = await resolveItem(it);
      let status;
      if (!best) { status = 'MISS'; miss++; }
      else if (best.w >= MIN_W) { status = 'HI'; hi++; }
      else { status = 'LO'; lo++; }
      // 고화질(HI)만 교체한다. 저화질(LO)/미스는 기존 스프라이트 유지.
      if (best && best.w >= MIN_W && !dry) {
        const fn = `bulba__${it.en}.png`;
        fs.writeFileSync(path.join(OUT_DIR, fn), best.buf);
        // --images-only: 이미지만 저장하고 JSON(it.sprite)은 건드리지 않는다(확인용)
        if (!imagesOnly) it.sprite = `sprites/items/${fn}`;
      }
      results.push({ en: it.en, ko: it.ko, category: it.category, status,
        file: best?.file || null, size: best ? `${best.w}x${best.h}` : null });
      process.stdout.write(`\r  진행 ${results.length}/${targets.length}  HI:${hi} LO:${lo} MISS:${miss}   `);
    }
  }
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  process.stdout.write('\n\n');

  // 카테고리별 요약
  const byCat = {};
  for (const r of results) {
    const b = (byCat[r.category] ||= { HI: 0, LO: 0, MISS: 0 });
    b[r.status]++;
  }
  console.log('카테고리별 (HI=고화질160급 / LO=저화질만있음 / MISS=못찾음):');
  Object.keys(byCat).sort().forEach(c => {
    const b = byCat[c];
    console.log('  ' + c.padEnd(20) + `HI:${b.HI}  LO:${b.LO}  MISS:${b.MISS}`);
  });
  console.log(`\n총계  HI:${hi}  LO:${lo}  MISS:${miss}  / ${results.length}`);

  if (miss || lo) {
    console.log('\n[LO/MISS 목록]');
    results.filter(r => r.status !== 'HI').forEach(r =>
      console.log(`  ${r.status}  ${r.category.padEnd(18)} ${r.en.padEnd(24)} ${r.ko}`));
  }

  if (reportPath) fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));

  if (!dry && !imagesOnly) {
    fs.writeFileSync(ITEMS_JSON, JSON.stringify(items, null, 2), 'utf8');
    console.log(`\n✓ ${ITEMS_JSON} 갱신 완료 (고화질 ${hi}개 sprite 교체, LO/MISS는 원본 유지)`);
  } else if (imagesOnly) {
    console.log(`\n✓ 고화질 ${hi}개 이미지 다운로드 완료 (sprites/items/bulba__*.png). JSON 미수정 — 확인용.`);
  } else {
    console.log('\n(dry: JSON 미수정)');
  }
}

main().catch(e => { console.error('\n오류:', e); process.exit(1); });
