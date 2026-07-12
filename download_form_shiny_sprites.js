#!/usr/bin/env node
/**
 * download_form_shiny_sprites.js
 * - data/pokedex.json 의 각 엔트리 forms[] 마다 이로치(shiny) 아트워크를 채운다.
 * - 폼 종류 2가지:
 *   (A) za_*.png 폼 → 파일명을 PokeAPI 이름으로 변환(za_ 제거, .png 제거, '_'→'-')
 *       → PokeAPI /pokemon/{name} 조회 → official-artwork.front_shiny (폴백 home.front_shiny) 다운로드
 *   (B) master__...official-artwork__{id}.png 폼(type:base) → 같은 id 의 shiny 경로 사용
 *       (base 1025 다운로드에 이미 있음. 없으면 raw github 에서 받음)
 * - 각 form 에 shinySprite 필드 추가 후 pokedex.json 저장 (백업 .formbak)
 * - PokeAPI 에 없거나 shiny 아트워크 없는 폼은 누락 리스트로 출력(→ 위키 폴백 대상)
 *
 * 사용법: node download_form_shiny_sprites.js
 */

const fs    = require('fs');
const path  = require('path');
const https = require('https');

const CONCURRENCY  = 8;
const SPRITES_DIR  = path.join(__dirname, 'sprites', 'pokemon');
const POKEDEX_JSON = path.join(__dirname, 'data', 'pokedex.json');
const RAW_BASE = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other';

function urlToFilename(url) {
  const u = new URL(url);
  const after = u.pathname.replace(/^\/.*?\/sprites\//, '');
  return after.replace(/\//g, '__');
}

// 바이너리 다운로드 (리다이렉트 추적)
function download(url, dest) {
  return new Promise((resolve, reject) => {
    if (fs.existsSync(dest)) { resolve('cached'); return; }
    const tmp = dest + '.tmp';
    const file = fs.createWriteStream(tmp);
    const req = https.get(url, { timeout: 20000 }, res => {
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
      file.on('finish', () => file.close(() => fs.rename(tmp, dest, err => err ? reject(err) : resolve('ok'))));
    });
    req.on('error', err => { file.close(); fs.unlink(tmp, () => {}); reject(err); });
    req.on('timeout', () => { req.destroy(); file.close(); fs.unlink(tmp, () => {}); reject(new Error('timeout')); });
  });
}

// JSON GET
function httpJson(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { timeout: 20000, headers: { 'User-Agent': 'pokenova-shiny/1.0' } }, res => {
      if (res.statusCode !== 200) { res.resume(); reject(new Error(`HTTP ${res.statusCode}`)); return; }
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => { try { resolve(JSON.parse(body)); } catch (e) { reject(e); } });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
  });
}

// za_charizard_mega_x.png -> charizard-mega-x
function formToApiName(spriteFile) {
  return spriteFile.replace(/^za_/, '').replace(/\.png$/, '').replace(/_/g, '-');
}

// 한 폼 처리 → { ok, localPath, source, apiName, label }
async function fetchFormShiny(spriteFile, label) {
  // (B) base 타입: master__...official-artwork__{id}.png
  const mBase = spriteFile.match(/official-artwork__(\d+)\.png$/);
  if (mBase) {
    const id = mBase[1];
    const shinyName = `master__sprites__pokemon__other__official-artwork__shiny__${id}.png`;
    const dest = path.join(SPRITES_DIR, shinyName);
    if (fs.existsSync(dest)) return { ok: true, localPath: '/sprites/pokemon/' + shinyName, source: 'base-cached', label };
    try {
      await download(`${RAW_BASE}/official-artwork/shiny/${id}.png`, dest);
      return { ok: true, localPath: '/sprites/pokemon/' + shinyName, source: 'base-dl', label };
    } catch {
      return { ok: false, label, reason: `base id ${id} shiny 없음` };
    }
  }

  // (A) za_ 폼: PokeAPI 이름 변환 후 조회
  const apiName = formToApiName(spriteFile);
  let data;
  try {
    data = await httpJson(`https://pokeapi.co/api/v2/pokemon/${apiName}`);
  } catch (e) {
    return { ok: false, label, apiName, reason: `PokeAPI 미존재(${e.message})` };
  }
  const oa = data.sprites?.other?.['official-artwork']?.front_shiny;
  const home = data.sprites?.other?.home?.front_shiny;
  const shinyUrl = oa || home;
  if (!shinyUrl) return { ok: false, label, apiName, reason: 'shiny 아트워크 없음' };

  const dest = path.join(SPRITES_DIR, urlToFilename(shinyUrl));
  try {
    await download(shinyUrl, dest);
    return { ok: true, localPath: '/sprites/pokemon/' + path.basename(dest), source: oa ? 'official' : 'home', label };
  } catch (e) {
    return { ok: false, label, apiName, reason: `다운로드 실패(${e.message})` };
  }
}

async function main() {
  console.log('=== Pokénova FORM Shiny Downloader ===\n');
  if (!fs.existsSync(SPRITES_DIR)) fs.mkdirSync(SPRITES_DIR, { recursive: true });

  const pokedex = JSON.parse(fs.readFileSync(POKEDEX_JSON, 'utf8'));

  // (엔트리, 폼) 평탄화
  const jobs = [];
  for (const e of pokedex) {
    for (const f of (e.forms || [])) {
      const label = `${e.en}/${f.name_ko || f.name_en || f.type}`;
      jobs.push({ form: f, spriteFile: (f.sprite || '').split('/').pop(), label });
    }
  }
  const total = jobs.length;
  console.log(`  대상 폼: ${total}개  (동시 ${CONCURRENCY})\n`);

  let idx = 0, done = 0, official = 0, home = 0, base = 0, miss = 0;
  const misses = [];

  const workers = Array.from({ length: Math.min(CONCURRENCY, total) }, async () => {
    while (true) {
      const i = idx++;
      if (i >= total) break;
      const job = jobs[i];
      const r = await fetchFormShiny(job.spriteFile, job.label);
      if (r.ok) {
        job.form.shinySprite = r.localPath;
        if (r.source === 'official') official++;
        else if (r.source === 'home') home++;
        else base++;
      } else {
        miss++;
        misses.push(r);
      }
      done++;
      if (done % 10 === 0 || done === total) {
        const pct = Math.floor((done / total) * 100);
        process.stdout.write(`\r  진행 ${done}/${total} (${pct}%)  공식:${official} 홈:${home} base:${base} 누락:${miss}   `);
      }
    }
  });
  await Promise.all(workers);
  process.stdout.write('\n\n');

  fs.writeFileSync(POKEDEX_JSON + '.formbak', JSON.stringify(pokedex, null, 2), 'utf8');
  fs.writeFileSync(POKEDEX_JSON, JSON.stringify(pokedex, null, 2), 'utf8');

  console.log(`  결과: 공식 ${official} · 홈 ${home} · base ${base} · 누락 ${miss}`);
  if (misses.length) {
    console.log(`\n  === 누락(위키 폴백 대상) ${misses.length}개 ===`);
    for (const m of misses) console.log(`   - ${m.label}  [${m.apiName || 'base'}]  ${m.reason}`);
    fs.writeFileSync(path.join(__dirname, 'form_shiny_misses.json'), JSON.stringify(misses, null, 2), 'utf8');
    console.log(`\n  누락 목록 저장: form_shiny_misses.json`);
  }
  console.log(`\n  ✓ ${POKEDEX_JSON} forms 에 shinySprite 추가 (백업: pokedex.json.formbak)`);
  console.log('\n=== 완료 ===');
}

main().catch(err => { console.error('\n오류:', err); process.exit(1); });
