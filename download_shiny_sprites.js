#!/usr/bin/env node
/**
 * download_shiny_sprites.js
 * - data/pokedex.json 의 도감번호(id)마다 이로치(shiny) 공식 아트워크를 다운로드
 * - 1순위: PokeAPI official-artwork/shiny/{id}.png
 *   폴백: PokeAPI home/shiny/{id}.png (공식 아트워크 없는 경우)
 * - 파일명 규칙은 기존 download_sprites.js 와 동일하게 URL 경로의 '/' → '__'
 * - 각 항목에 shinySprite 필드를 추가해 pokedex.json 저장 (기존 sprite 는 그대로 둠)
 *
 * 사용법: node download_shiny_sprites.js
 */

const fs    = require('fs');
const path  = require('path');
const https = require('https');

const CONCURRENCY   = 20;
const SPRITES_DIR   = path.join(__dirname, 'sprites', 'pokemon');
const POKEDEX_JSON  = path.join(__dirname, 'data', 'pokedex.json');

const BASE = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other';

// URL 경로에서 'sprites/' 이후를 '__' flat 파일명으로 (기존 download_sprites.js 와 동일 규칙)
function urlToFilename(url) {
  const u = new URL(url);
  const after = u.pathname.replace(/^\/.*?\/sprites\//, '');
  return after.replace(/\//g, '__');
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    if (fs.existsSync(dest)) { resolve('cached'); return; }
    const tmp = dest + '.tmp';
    const file = fs.createWriteStream(tmp);
    const req = https.get(url, { timeout: 15000 }, res => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        file.close(); fs.unlink(tmp, () => {});
        download(res.headers.location, dest).then(resolve).catch(reject);
        return;
      }
      if (res.statusCode !== 200) {
        file.close(); fs.unlink(tmp, () => {});
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }
      res.pipe(file);
      file.on('finish', () => file.close(() => {
        fs.rename(tmp, dest, err => err ? reject(err) : resolve('ok'));
      }));
    });
    req.on('error', err => { file.close(); fs.unlink(tmp, () => {}); reject(err); });
    req.on('timeout', () => { req.destroy(); file.close(); fs.unlink(tmp, () => {}); reject(new Error('timeout')); });
  });
}

// 이로치 1건: official-artwork/shiny 시도 → 실패 시 home/shiny 폴백
// 성공 시 { id, localPath } / 완전 실패 시 { id, localPath: null }
async function fetchShiny(id) {
  const candidates = [
    `${BASE}/official-artwork/shiny/${id}.png`,
    `${BASE}/home/shiny/${id}.png`,
  ];
  for (const url of candidates) {
    const dest = path.join(SPRITES_DIR, urlToFilename(url));
    try {
      await download(url, dest);
      return { id, localPath: '/sprites/pokemon/' + path.basename(dest), source: url.includes('official-artwork') ? 'official' : 'home' };
    } catch { /* 다음 후보 시도 */ }
  }
  return { id, localPath: null, source: null };
}

async function main() {
  console.log('=== Pokénova Shiny Sprite Downloader ===\n');
  if (!fs.existsSync(SPRITES_DIR)) fs.mkdirSync(SPRITES_DIR, { recursive: true });

  const pokedex = JSON.parse(fs.readFileSync(POKEDEX_JSON, 'utf8'));
  const ids = pokedex.map(p => p.id);
  const total = ids.length;

  console.log(`  대상 도감: ${total}종\n  다운로드 시작 (동시 ${CONCURRENCY}개)...\n`);

  const results = new Map(); // id → { localPath, source }
  let done = 0, official = 0, home = 0, missing = 0;
  const missingIds = [];

  let idx = 0;
  const workers = Array.from({ length: Math.min(CONCURRENCY, total) }, async () => {
    while (true) {
      const i = idx++;
      if (i >= total) break;
      const r = await fetchShiny(ids[i]);
      results.set(r.id, r);
      if (r.source === 'official') official++;
      else if (r.source === 'home') home++;
      else { missing++; missingIds.push(r.id); }
      done++;
      if (done % 25 === 0 || done === total) {
        const pct = Math.floor((done / total) * 100);
        process.stdout.write(`\r  진행 ${done}/${total} (${pct}%)  공식:${official} 홈:${home} 누락:${missing}   `);
      }
    }
  });
  await Promise.all(workers);
  process.stdout.write('\n\n');

  // pokedex.json 백업 후 shinySprite 필드 추가
  fs.writeFileSync(POKEDEX_JSON + '.bak', JSON.stringify(pokedex, null, 2), 'utf8');
  for (const p of pokedex) {
    const r = results.get(p.id);
    if (r && r.localPath) p.shinySprite = r.localPath;
  }
  fs.writeFileSync(POKEDEX_JSON, JSON.stringify(pokedex, null, 2), 'utf8');

  console.log(`  결과: 공식 아트워크 ${official} · HOME 폴백 ${home} · 누락 ${missing}`);
  if (missingIds.length) console.log(`  누락 도감번호: ${missingIds.join(', ')}`);
  console.log(`\n  ✓ ${POKEDEX_JSON} 에 shinySprite 필드 추가 (백업: pokedex.json.bak)`);
  console.log('\n=== 완료 ===');
}

main().catch(err => { console.error('\n오류:', err); process.exit(1); });
