#!/usr/bin/env node
/**
 * 번역 적용 스크립트
 *
 * 사용법:
 *   1. node collect-data.js 실행 → data/needs_translation.json 생성
 *   2. needs_translation.json 열어서 ko / desc 필드를 한국어로 수정
 *   3. node apply-translations.js 실행 → 각 quiz_*.json 에 반영
 */

const fs   = require('fs');
const path = require('path');

const OUT_DIR    = path.join(__dirname, 'data');
const TRANS_FILE = path.join(OUT_DIR, 'needs_translation.json');

const FILES = {
  pokemon:   'quiz_pokemon.json',
  moves:     'quiz_moves.json',
  abilities: 'quiz_abilities.json',
  items:     'quiz_items.json',
};

function applyCategory(category, translations) {
  const filePath = path.join(OUT_DIR, FILES[category]);
  if (!fs.existsSync(filePath)) {
    console.warn(`  ⚠ ${FILES[category]} 없음, 건너뜀`);
    return 0;
  }

  const data  = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  const byId  = Object.fromEntries(translations.map(t => [t.id, t]));
  let updated = 0;

  for (const item of data) {
    const t = byId[item.id];
    if (!t) continue;

    // ko 필드가 번역됐으면 적용
    if (t.ko && t.ko !== item.en) {
      item.ko = t.ko;
    }

    // desc 필드가 번역됐으면 적용
    if (t.desc && t.desc !== item.desc) {
      item.desc      = t.desc;
      item.desc_lang = 'ko';
    }

    // 번역 완료되면 needs_ko 제거
    const koApplied   = item.ko   && item.ko   !== item.en;
    const descApplied = !item.desc || item.desc_lang === 'ko';
    if (koApplied && descApplied) {
      delete item.needs_ko;
      updated++;
    }
  }

  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
  return updated;
}

function main() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(' 번역 적용 스크립트');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  if (!fs.existsSync(TRANS_FILE)) {
    console.error('data/needs_translation.json 파일이 없습니다.');
    console.error('먼저 node collect-data.js 를 실행하세요.');
    process.exit(1);
  }

  const translations = JSON.parse(fs.readFileSync(TRANS_FILE, 'utf8'));
  let totalUpdated = 0;

  for (const [category, items] of Object.entries(translations)) {
    if (!items.length) {
      console.log(`  ${category}: 번역 항목 없음`);
      continue;
    }
    const updated = applyCategory(category, items);
    console.log(`  ${category}: ${updated}/${items.length}개 적용 완료`);
    totalUpdated += updated;
  }

  // 적용된 항목은 needs_translation.json에서 제거
  const remaining = {};
  for (const [category, items] of Object.entries(translations)) {
    const filePath = path.join(OUT_DIR, FILES[category]);
    if (!fs.existsSync(filePath)) continue;
    const data  = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const doneIds = new Set(data.filter(i => !i.needs_ko).map(i => i.id));
    remaining[category] = items.filter(i => !doneIds.has(i.id));
  }

  fs.writeFileSync(TRANS_FILE, JSON.stringify(remaining, null, 2));
  const remainCount = Object.values(remaining).reduce((s, a) => s + a.length, 0);

  console.log(`\n총 ${totalUpdated}개 적용 완료`);
  if (remainCount > 0) {
    console.log(`미번역 ${remainCount}개 → needs_translation.json 에 남겨둠`);
  } else {
    console.log('모든 번역 완료!');
  }
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
}

main();
