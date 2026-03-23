#!/usr/bin/env node
/**
 * PokeAPI 데이터 수집 스크립트
 * 실행: node collect-data.js
 * 필요: Node.js 18+ (built-in fetch)
 *
 * 생성 파일:
 *   data/quiz_pokemon.json   - 포켓몬 이름 + 타입 + 특성 + 폼(메가/거다이맥스/리전폼)
 *   data/quiz_moves.json     - 기술 정보
 *   data/quiz_abilities.json - 특성 정보 + 보유 포켓몬 목록
 *   data/quiz_items.json     - 도구 정보 + 스프라이트
 */

const fs   = require('fs');
const path = require('path');

const CONCURRENCY = 20;
const OUT_DIR = path.join(__dirname, 'data');

/* ── 매핑 테이블 ── */
const VERS_ORDER = [
  'red-blue','yellow','gold-silver','crystal','ruby-sapphire',
  'firered-leafgreen','emerald','diamond-pearl','platinum',
  'heartgold-soulsilver','black-white','black-2-white-2',
  'x-y','omega-ruby-alpha-sapphire','sun-moon','ultra-sun-ultra-moon',
  'lets-go-pikachu-lets-go-eevee','sword-shield',
  'brilliant-diamond-and-shining-pearl','legends-arceus','scarlet-violet'
];

const TYPE_KO = {
  normal:'노말', fire:'불꽃', water:'물', electric:'전기', grass:'풀',
  ice:'얼음', fighting:'격투', poison:'독', ground:'땅', flying:'비행',
  psychic:'에스퍼', bug:'벌레', rock:'바위', ghost:'고스트', dragon:'드래곤',
  dark:'악', steel:'강철', fairy:'페어리'
};

const CLASS_KO = { physical:'물리', special:'특수', status:'변화' };

const GEN_KO = {
  'generation-i':'1세대', 'generation-ii':'2세대', 'generation-iii':'3세대',
  'generation-iv':'4세대', 'generation-v':'5세대', 'generation-vi':'6세대',
  'generation-vii':'7세대', 'generation-viii':'8세대', 'generation-ix':'9세대'
};

// 폼 타입 감지 키워드
const FORM_DETECT = [
  { key: 'mega',   label: '메가진화' },
  { key: 'gmax',   label: '거다이맥스' },
  { key: 'alola',  label: '알로라' },
  { key: 'galar',  label: '가라르' },
  { key: 'hisui',  label: '히스이' },
  { key: 'paldea', label: '팔데아' },
];

function detectFormType(variantName) {
  for (const { key, label } of FORM_DETECT) {
    if (variantName.includes(key)) return { key, label };
  }
  return null;
}

/* ── 유틸 ── */
const sleep = ms => new Promise(r => setTimeout(r, ms));

function getFlavorText(entries, lang) {
  const f = (entries || []).filter(e => e.language.name === lang);
  if (!f.length) return null;
  f.sort((a, b) => {
    const ai = VERS_ORDER.indexOf(a.version_group?.name || '');
    const bi = VERS_ORDER.indexOf(b.version_group?.name || '');
    if (ai === -1 && bi === -1) return 0;
    if (ai === -1) return -1;
    if (bi === -1) return 1;
    return ai - bi;
  });
  if (!f[0].flavor_text) return null;
  return f[0].flavor_text.replace(/[\f\n\r]/g, ' ').replace(/\s+/g, ' ').trim();
}

async function fetchJSON(url) {
  for (let i = 0; i < 3; i++) {
    try {
      const res = await fetch(url);
      if (res.status === 404) return null;
      if (!res.ok) { await sleep(600); continue; }
      return await res.json();
    } catch {
      await sleep(1200);
    }
  }
  return null;
}

function showProgress(label, cur, total) {
  const pct  = Math.round(cur / total * 100);
  const fill = Math.floor(pct / 5);
  const bar  = '█'.repeat(fill) + '░'.repeat(20 - fill);
  process.stdout.write(`\r  ${label} [${bar}] ${cur}/${total} (${pct}%)`);
  if (cur >= total) process.stdout.write('\n');
}

async function batchProcess(ids, fn, label) {
  const results = [];
  for (let i = 0; i < ids.length; i += CONCURRENCY) {
    const batch = ids.slice(i, i + CONCURRENCY);
    const res   = await Promise.all(batch.map(id => fn(id)));
    results.push(...res);
    showProgress(label, Math.min(i + CONCURRENCY, ids.length), ids.length);
    await sleep(80);
  }
  return results;
}

/* ══════════════════════════════════════════════
   1단계: 종족 맵 (이름 + legendary/mythical + varieties)
══════════════════════════════════════════════ */
async function buildSpeciesMap() {
  console.log('\n[1/6] 포켓몬 종족 정보 수집...');
  const ids = Array.from({ length: 1025 }, (_, i) => i + 1);
  const map = {};

  await batchProcess(ids, async id => {
    const data = await fetchJSON(`https://pokeapi.co/api/v2/pokemon-species/${id}`);
    if (!data) return null;
    const ko = data.names.find(n => n.language.name === 'ko')?.name;
    const en = data.names.find(n => n.language.name === 'en')?.name || data.name;
    map[id] = {
      ko: ko || en,
      en,
      is_legendary: !!data.is_legendary,
      is_mythical:  !!data.is_mythical,
      // 기본형 제외한 비기본 변형 이름 목록
      varieties: data.varieties
        .filter(v => !v.is_default)
        .map(v => v.pokemon.name)
    };
    return map[id];
  }, '종족');

  console.log(`  → ${Object.keys(map).length}마리 수집 완료`);
  return map;
}

/* ══════════════════════════════════════════════
   2단계: 특성 이름 맵 (en → {ko, en})
   - collectPokemon에서 포켓몬별 특성 이름에 사용
══════════════════════════════════════════════ */
async function buildAbilityNameMap() {
  console.log('\n[2/6] 특성 이름 맵 수집...');
  const ids = Array.from({ length: 307 }, (_, i) => i + 1);
  const map = {};

  await batchProcess(ids, async id => {
    const data = await fetchJSON(`https://pokeapi.co/api/v2/ability/${id}`);
    if (!data) return null;
    const ko = data.names.find(n => n.language.name === 'ko')?.name;
    const en = data.names.find(n => n.language.name === 'en')?.name || data.name;
    map[data.name] = { ko: ko || en, en: en.toLowerCase() };
    return map[data.name];
  }, '특성명');

  console.log(`  → ${Object.keys(map).length}개 특성명 수집 완료`);
  return map;
}

/* ══════════════════════════════════════════════
   3단계: 포켓몬 (타입 + 특성 + 폼 포함)
══════════════════════════════════════════════ */
async function collectPokemon(speciesMap, abilityMap) {
  console.log('\n[3/6] 포켓몬 데이터 수집...');
  const ids     = Array.from({ length: 1025 }, (_, i) => i + 1);
  const pokemon = [];

  await batchProcess(ids, async id => {
    const data   = await fetchJSON(`https://pokeapi.co/api/v2/pokemon/${id}`);
    if (!data) return null;
    const sprite = data.sprites.other?.['official-artwork']?.front_default
                || data.sprites.front_default;
    if (!sprite) return null;

    const species = speciesMap[id] || {};
    const hasKo   = species.ko && species.ko !== species.en;

    // 타입
    const types = data.types
      .sort((a, b) => a.slot - b.slot)
      .map(t => TYPE_KO[t.type.name] || t.type.name);

    // 특성 (일반 + 숨겨진 특성)
    const abilities = data.abilities
      .sort((a, b) => a.slot - b.slot)
      .map(a => {
        const info = abilityMap[a.ability.name] || {};
        return {
          ko:     info.ko || a.ability.name,
          en:     info.en || a.ability.name,
          hidden: a.is_hidden
        };
      });

    // 특수 폼 (메가/거다이맥스/리전폼)
    const forms = [];
    for (const variantName of (species.varieties || [])) {
      const formType = detectFormType(variantName);
      if (!formType) continue;

      const fd = await fetchJSON(`https://pokeapi.co/api/v2/pokemon/${variantName}`);
      if (!fd) continue;

      const formSprite = fd.sprites.other?.['official-artwork']?.front_default
                      || fd.sprites.front_default;
      const formTypes = fd.types
        .sort((a, b) => a.slot - b.slot)
        .map(t => TYPE_KO[t.type.name] || t.type.name);
      const formAbilities = fd.abilities
        .sort((a, b) => a.slot - b.slot)
        .map(a => {
          const info = abilityMap[a.ability.name] || {};
          return { ko: info.ko || a.ability.name, en: info.en || a.ability.name, hidden: a.is_hidden };
        });

      // 폼 한국어 이름 구성
      const baseKo = species.ko || species.en || data.name;
      let nameKo;
      if (formType.key === 'mega') {
        const suffix = variantName.split('-mega-')[1]?.toUpperCase();
        nameKo = suffix ? `메가${baseKo} ${suffix}` : `메가${baseKo}`;
      } else if (formType.key === 'gmax') {
        nameKo = `거다이맥스 ${baseKo}`;
      } else {
        nameKo = `${formType.label} ${baseKo}`;
      }

      forms.push({
        type:    formType.key,
        name_ko: nameKo,
        name_en: variantName,
        sprite:  formSprite || null,
        types:   formTypes,
        abilities: formAbilities
      });
    }

    const entry = {
      id,
      ko:     species.ko  || species.en || data.name,
      en:     species.en  || data.name,
      sprite,
      types,
      abilities,
      ...(forms.length          ? { forms }           : {}),
      ...(species.is_legendary  ? { is_legendary: true } : {}),
      ...(species.is_mythical   ? { is_mythical:  true } : {}),
      ...(!hasKo                ? { needs_ko: true }     : {})
    };
    pokemon.push(entry);
    return entry;
  }, '포켓몬');

  pokemon.sort((a, b) => a.id - b.id);
  fs.writeFileSync(
    path.join(OUT_DIR, 'quiz_pokemon.json'),
    JSON.stringify(pokemon, null, 2)
  );
  const needsKo   = pokemon.filter(p => p.needs_ko).length;
  const withForms = pokemon.filter(p => p.forms?.length).length;
  console.log(`  → ${pokemon.length}마리 저장 완료 (폼 보유: ${withForms}마리 / 번역 필요: ${needsKo}마리)`);
  return pokemon;
}

/* ══════════════════════════════════════════════
   4단계: 기술 (Z기술 제외)
══════════════════════════════════════════════ */
async function collectMoves() {
  console.log('\n[4/6] 기술 데이터 수집...');
  const ids   = Array.from({ length: 850 }, (_, i) => i + 1);
  const moves = [];

  await batchProcess(ids, async id => {
    const data = await fetchJSON(`https://pokeapi.co/api/v2/move/${id}`);
    if (!data) return null;
    if (data.meta?.category?.name === 'z-move') return null;
    const koN    = data.names.find(n => n.language.name === 'ko');
    const enN    = data.names.find(n => n.language.name === 'en');
    const koDesc = getFlavorText(data.flavor_text_entries, 'ko');
    const enDesc = getFlavorText(data.flavor_text_entries, 'en') || '';
    const hasKoName = !!koN;
    const hasKoDesc = !!koDesc;
    const entry = {
      id,
      ko:       koN?.name || enN?.name || data.name,
      en:       (enN?.name || data.name).toLowerCase(),
      type:     TYPE_KO[data.type?.name]         || data.type?.name         || '',
      type_en:  data.type?.name                  || '',
      class:    CLASS_KO[data.damage_class?.name] || data.damage_class?.name || '',
      pp:       data.pp       ?? null,
      power:    data.power    ?? null,
      accuracy: data.accuracy ?? null,
      gen:      GEN_KO[data.generation?.name]    || data.generation?.name   || '',
      desc:     koDesc || enDesc,
      desc_lang: hasKoDesc ? 'ko' : 'en',
      ...(!hasKoName || !hasKoDesc ? { needs_ko: true } : {})
    };
    moves.push(entry);
    return entry;
  }, '기술');

  moves.sort((a, b) => a.id - b.id);
  fs.writeFileSync(
    path.join(OUT_DIR, 'quiz_moves.json'),
    JSON.stringify(moves, null, 2)
  );
  const needsKo = moves.filter(m => m.needs_ko).length;
  console.log(`  → ${moves.length}개 저장 완료 (번역 필요: ${needsKo}개)`);
  return moves;
}

/* ══════════════════════════════════════════════
   5단계: 특성
══════════════════════════════════════════════ */
async function collectAbilities(speciesMap) {
  console.log('\n[5/6] 특성 데이터 수집...');
  const ids       = Array.from({ length: 307 }, (_, i) => i + 1);
  const abilities = [];

  await batchProcess(ids, async id => {
    const data = await fetchJSON(`https://pokeapi.co/api/v2/ability/${id}`);
    if (!data) return null;
    const koN    = data.names.find(n => n.language.name === 'ko');
    const enN    = data.names.find(n => n.language.name === 'en');
    const koDesc = getFlavorText(data.flavor_text_entries, 'ko');
    const enDesc = getFlavorText(data.flavor_text_entries, 'en');
    const desc   = koDesc || enDesc;
    if (!desc) return null;
    const hasKoName = !!koN;
    const hasKoDesc = !!koDesc;

    const pokemonNames = data.pokemon
      .filter(p => !p.is_hidden)
      .map(p => {
        const pid = parseInt(p.pokemon.url.split('/').filter(Boolean).pop());
        return speciesMap[pid]?.ko || p.pokemon.name;
      })
      .slice(0, 6);

    const entry = {
      id,
      ko:      koN?.name || enN?.name || data.name,
      en:      (enN?.name || data.name).toLowerCase(),
      desc,
      desc_lang: hasKoDesc ? 'ko' : 'en',
      pokemon: pokemonNames,
      ...(!hasKoName || !hasKoDesc ? { needs_ko: true } : {})
    };
    abilities.push(entry);
    return entry;
  }, '특성');

  abilities.sort((a, b) => a.id - b.id);
  fs.writeFileSync(
    path.join(OUT_DIR, 'quiz_abilities.json'),
    JSON.stringify(abilities, null, 2)
  );
  const needsKo = abilities.filter(a => a.needs_ko).length;
  console.log(`  → ${abilities.length}개 저장 완료 (번역 필요: ${needsKo}개)`);
  return abilities;
}

/* ══════════════════════════════════════════════
   6단계: 도구
══════════════════════════════════════════════ */
async function collectItems() {
  console.log('\n[6/6] 도구 데이터 수집...');
  const ids   = Array.from({ length: 1700 }, (_, i) => i + 1);
  const items = [];

  await batchProcess(ids, async id => {
    const data = await fetchJSON(`https://pokeapi.co/api/v2/item/${id}`);
    if (!data) return null;
    const koN  = data.names.find(n => n.language.name === 'ko');
    const enN  = data.names.find(n => n.language.name === 'en');

    const koDesc = (data.effect_entries || []).find(e => e.language.name === 'ko')?.short_effect
                || getFlavorText(data.flavor_text_entries || [], 'ko');
    const enDesc = (data.effect_entries || []).find(e => e.language.name === 'en')?.short_effect
                || getFlavorText(data.flavor_text_entries || [], 'en');
    const desc = koDesc || enDesc;
    if (!desc) return null;
    const hasKoName = !!koN;
    const hasKoDesc = !!koDesc;

    const entry = {
      id,
      ko:        koN?.name || enN?.name || data.name,
      en:        (enN?.name || data.name).toLowerCase(),
      desc:      desc.replace(/\s+/g, ' ').trim(),
      desc_lang: hasKoDesc ? 'ko' : 'en',
      sprite:    data.sprites?.default || null,
      category:  data.category?.name   || '',
      ...(!hasKoName || !hasKoDesc ? { needs_ko: true } : {})
    };
    items.push(entry);
    return entry;
  }, '도구');

  items.sort((a, b) => a.id - b.id);
  fs.writeFileSync(
    path.join(OUT_DIR, 'quiz_items.json'),
    JSON.stringify(items, null, 2)
  );
  const needsKo = items.filter(i => i.needs_ko).length;
  console.log(`  → ${items.length}개 저장 완료 (번역 필요: ${needsKo}개)`);
  return items;
}

/* ══════════════════════════════════════════════
   메인
══════════════════════════════════════════════ */
async function main() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(' PokeAPI 데이터 수집 스크립트');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(' 예상 시간: 5~10분 (네트워크 상태에 따라 다름)');

  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  const start = Date.now();

  const speciesMap  = await buildSpeciesMap();
  const abilityMap  = await buildAbilityNameMap();
  const pokemon     = await collectPokemon(speciesMap, abilityMap);
  const moves       = await collectMoves();
  const abilities   = await collectAbilities(speciesMap);
  const items       = await collectItems();

  // needs_translation.json 추출
  console.log('\n[+] 번역 필요 항목 추출...');
  const needsTranslation = {
    pokemon:   pokemon  .filter(p => p.needs_ko).map(({ needs_ko, ...rest }) => rest),
    moves:     moves    .filter(m => m.needs_ko).map(({ needs_ko, ...rest }) => rest),
    abilities: abilities.filter(a => a.needs_ko).map(({ needs_ko, ...rest }) => rest),
    items:     items    .filter(i => i.needs_ko).map(({ needs_ko, ...rest }) => rest),
  };
  const totalNeeds = Object.values(needsTranslation).reduce((s, arr) => s + arr.length, 0);
  fs.writeFileSync(
    path.join(OUT_DIR, 'needs_translation.json'),
    JSON.stringify(needsTranslation, null, 2)
  );
  console.log(`  → 총 ${totalNeeds}개 항목 → data/needs_translation.json`);
  console.log(`     포켓몬: ${needsTranslation.pokemon.length} / 기술: ${needsTranslation.moves.length} / 특성: ${needsTranslation.abilities.length} / 도구: ${needsTranslation.items.length}`);

  const elapsed = Math.round((Date.now() - start) / 1000);
  const min     = Math.floor(elapsed / 60);
  const sec     = elapsed % 60;

  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(` 완료! 소요 시간: ${min}분 ${sec}초`);
  console.log(` 저장 위치: ${OUT_DIR}`);
  console.log(' 번역 후 apply-translations.js 실행');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
}

main().catch(err => {
  console.error('\n오류 발생:', err.message);
  process.exit(1);
});
