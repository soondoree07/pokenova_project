#!/usr/bin/env node
/**
 * download_sprites.js
 * - data/quiz_pokemon.json, data/quiz_items.json 의 sprite URL 전부 추출
 * - sprites/ 폴더에 병렬 20개씩 다운로드
 * - 두 JSON 파일의 sprite 값을 로컬 상대경로로 교체 후 저장
 */

const fs   = require('fs');
const path = require('path');
const https = require('https');
const http  = require('http');

const CONCURRENCY  = 20;
const SPRITES_DIR  = path.join(__dirname, 'sprites');
const POKEMON_JSON = path.join(__dirname, 'data', 'quiz_pokemon.json');
const ITEMS_JSON   = path.join(__dirname, 'data', 'quiz_items.json');

// ── 유틸 ─────────────────────────────────────────────────────────────────────

function urlToFilename(url) {
  // URL 경로의 마지막 부분을 파일명으로 사용, 서브디렉터리 구조 유지
  // e.g. .../sprites/pokemon/other/official-artwork/1.png
  //   → pokemon__official-artwork__1.png  (슬래시 → __)
  try {
    const u = new URL(url);
    // PokeAPI CDN 경로에서 "sprites/" 이후 부분만 가져옴
    const after = u.pathname.replace(/^\/.*?\/sprites\//, '');
    // 디렉터리 구분자를 '__' 로 치환해 flat 파일명으로
    return after.replace(/\//g, '__');
  } catch {
    // URL 파싱 실패 시 hash 대체
    return url.replace(/[^a-zA-Z0-9._-]/g, '_');
  }
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    if (fs.existsSync(dest)) { resolve('cached'); return; }

    const tmp = dest + '.tmp';
    const file = fs.createWriteStream(tmp);
    const client = url.startsWith('https') ? https : http;

    const req = client.get(url, { timeout: 15000 }, res => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        file.close();
        fs.unlink(tmp, () => {});
        download(res.headers.location, dest).then(resolve).catch(reject);
        return;
      }
      if (res.statusCode !== 200) {
        file.close();
        fs.unlink(tmp, () => {});
        reject(new Error(`HTTP ${res.statusCode} for ${url}`));
        return;
      }
      res.pipe(file);
      file.on('finish', () => {
        file.close(() => {
          fs.rename(tmp, dest, err => err ? reject(err) : resolve('ok'));
        });
      });
    });

    req.on('error', err => {
      file.close();
      fs.unlink(tmp, () => {});
      reject(err);
    });
    req.on('timeout', () => {
      req.destroy();
      file.close();
      fs.unlink(tmp, () => {});
      reject(new Error(`Timeout: ${url}`));
    });
  });
}

// ── URL 수집 ──────────────────────────────────────────────────────────────────

function collectPokemonSprites(pokemon) {
  // { url → localPath } Map 반환
  // pokemon 배열 항목 참조도 함께 수집해 나중에 교체
  const entries = []; // { obj, key, url }

  for (const p of pokemon) {
    if (p.sprite) entries.push({ obj: p, key: 'sprite', url: p.sprite });
    if (p.forms) {
      for (const f of p.forms) {
        if (f.sprite) entries.push({ obj: f, key: 'sprite', url: f.sprite });
      }
    }
  }
  return entries;
}

function collectItemSprites(items) {
  const entries = [];
  for (const it of items) {
    if (it.sprite) entries.push({ obj: it, key: 'sprite', url: it.sprite });
  }
  return entries;
}

// ── 병렬 다운로드 (concurrency 제한) ─────────────────────────────────────────

async function downloadAll(tasks) {
  let done = 0;
  let failed = 0;
  const total = tasks.length;

  function progressBar() {
    const pct = Math.floor((done / total) * 40);
    const bar = '█'.repeat(pct) + '░'.repeat(40 - pct);
    const pctNum = Math.floor((done / total) * 100);
    process.stdout.write(`\r  [${bar}] ${pctNum}%  ${done}/${total}  실패:${failed}  `);
  }

  progressBar();

  let idx = 0;
  const workers = Array.from({ length: Math.min(CONCURRENCY, total) }, async () => {
    while (true) {
      const i = idx++;
      if (i >= total) break;
      const { url, dest } = tasks[i];
      try {
        await download(url, dest);
      } catch (e) {
        failed++;
        if (process.env.DEBUG) console.error(`\n  ✗ ${url}\n    ${e.message}`);
      }
      done++;
      progressBar();
    }
  });

  await Promise.all(workers);
  process.stdout.write('\n');
  return { done, failed };
}

// ── 메인 ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log('=== Pokénova Sprite Downloader ===\n');

  // sprites 폴더 생성
  if (!fs.existsSync(SPRITES_DIR)) {
    fs.mkdirSync(SPRITES_DIR, { recursive: true });
    console.log(`  📁 sprites/ 폴더 생성\n`);
  }

  // JSON 읽기
  const pokemon = JSON.parse(fs.readFileSync(POKEMON_JSON, 'utf8'));
  const items   = JSON.parse(fs.readFileSync(ITEMS_JSON,   'utf8'));

  // sprite 참조 수집
  const pokemonEntries = collectPokemonSprites(pokemon);
  const itemEntries    = collectItemSprites(items);
  const allEntries     = [...pokemonEntries, ...itemEntries];

  // URL → 로컬경로 Map (중복 URL 방지)
  const urlToLocal = new Map();
  for (const { url } of allEntries) {
    if (!urlToLocal.has(url)) {
      const filename = urlToFilename(url);
      urlToLocal.set(url, path.join(SPRITES_DIR, filename));
    }
  }

  // 다운로드 태스크 목록 (중복 제거)
  const tasks = [...urlToLocal.entries()].map(([url, dest]) => ({ url, dest }));

  console.log(`  포켓몬 sprite: ${pokemonEntries.length}개`);
  console.log(`  아이템 sprite: ${itemEntries.length}개`);
  console.log(`  고유 URL 총계: ${tasks.length}개\n`);
  console.log(`  다운로드 시작 (동시 ${CONCURRENCY}개)...\n`);

  const { done, failed } = await downloadAll(tasks);

  console.log(`\n  완료: ${done - failed}개 성공, ${failed}개 실패\n`);

  // JSON 파일의 sprite 값을 로컬 상대경로로 교체
  console.log('  JSON 파일 sprite 경로 업데이트 중...');

  for (const { obj, key, url } of allEntries) {
    const localAbs = urlToLocal.get(url);
    if (localAbs && fs.existsSync(localAbs)) {
      // HTML에서 사용할 상대경로 (프로젝트 루트 기준)
      obj[key] = 'sprites/' + path.basename(localAbs);
    }
    // 다운로드 실패한 경우 원본 URL 유지
  }

  fs.writeFileSync(POKEMON_JSON, JSON.stringify(pokemon, null, 2), 'utf8');
  fs.writeFileSync(ITEMS_JSON,   JSON.stringify(items,   null, 2), 'utf8');

  console.log(`  ✓ ${POKEMON_JSON} 저장 완료`);
  console.log(`  ✓ ${ITEMS_JSON} 저장 완료`);
  console.log('\n=== 완료 ===');
}

main().catch(err => {
  console.error('\n오류:', err);
  process.exit(1);
});
