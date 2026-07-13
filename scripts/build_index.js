// index.html 생성 — 루트(/)를 이로치 도감으로 서빙하기 위한 pokedex.html 사본.
//
// 왜 사본인가: Cloudflare 정적 자산은 /pokedex.html 을 clean-URL(/pokedex)로 307 리다이렉트한다.
// 그래서 _redirects 의 '/ → /pokedex.html 200' rewrite 가 리다이렉트로 튕겨 루트가 404가 됐다.
// 루트에 실제 파일을 두는 방식이 가장 확실하다.
//
// pokedex.html 을 고쳤으면 반드시 이 스크립트를 다시 돌릴 것:  node scripts/build_index.js
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const SRC = path.join(ROOT, 'pokedex.html');
const OUT = path.join(ROOT, 'index.html');

const BANNER = `<!--
  ⚠️ 자동 생성 파일 — 직접 고치지 마세요.
  이 파일은 pokedex.html 의 사본입니다. 루트(/)를 이로치 도감으로 쓰기 위한 것이고,
  pokedex.html 의 IS_ROOT 판정이 경로가 '/' 일 때 이로치 모드를 켭니다.
  수정은 pokedex.html 에서 하고, 아래 명령으로 다시 생성하세요.
      node scripts/build_index.js
-->
`;

const src = fs.readFileSync(SRC, 'utf8');
if (!src.includes('IS_ROOT')) {
  console.error('❌ pokedex.html 에 IS_ROOT 판정이 없습니다. 루트에서 이로치 모드가 안 켜집니다.');
  process.exit(1);
}
fs.writeFileSync(OUT, BANNER + src);
console.log(`✅ index.html 생성 (pokedex.html 사본, ${(src.length / 1024).toFixed(0)} KB)`);
