"""
포켓몬별 기술 학습 데이터 수집 (PokeAPI → data/learnsets.json)
- quiz_pokemon.json의 모든 포켓몬(원종 + 폼) 대상
- quiz_moves.json에 있는 기술만 수록 (나머지는 무시)
- 재실행 시 기존 캐시 이어서 진행
"""
import json, time, os, sys
import urllib.request, urllib.error

VERSION_PRIORITY = [
    'scarlet-violet', 'the-teal-mask', 'the-indigo-disk',
    'sword-shield', 'the-isle-of-armor', 'the-crown-tundra',
    'brilliant-diamond-and-shining-pearl', 'legends-arceus',
    'ultra-sun-ultra-moon', 'sun-moon',
    'omega-ruby-alpha-sapphire', 'x-y',
    'black-2-white-2', 'black-white',
    'heartgold-soulsilver', 'platinum', 'diamond-pearl',
    'firered-leafgreen', 'emerald', 'ruby-sapphire',
    'crystal', 'gold-silver', 'yellow', 'red-blue'
]

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'pokenova-builder/1.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())

def get_learnset(poke_en, known_moves):
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_en}/"
    try:
        data = fetch_json(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # 존재하지 않는 폼
        print(f"  HTTP {e.code}: {poke_en}")
        return []
    except Exception as e:
        print(f"  Error {poke_en}: {e}")
        return []

    raw_moves = data.get('moves', [])

    # 사용 가능한 버전 그룹 탐색
    vg_set = set()
    for m in raw_moves:
        for vgd in m.get('version_group_details', []):
            vg_set.add(vgd['version_group']['name'])

    latest_vg = next((vg for vg in VERSION_PRIORITY if vg in vg_set), None)

    result = []
    seen = set()
    for m in raw_moves:
        move_en = m['move']['name']
        if move_en not in known_moves:
            continue  # quiz_moves.json에 없는 기술 제외
        if move_en in seen:
            continue

        if latest_vg:
            vgd = next((v for v in m['version_group_details']
                        if v['version_group']['name'] == latest_vg), None)
            if not vgd:
                continue
            method = vgd['move_learn_method']['name']
            level  = vgd['level_learned_at']
        else:
            # 버전 그룹 없으면 최신 순으로 아무 버전
            vgd = m['version_group_details'][-1] if m['version_group_details'] else None
            if not vgd:
                continue
            method = vgd['move_learn_method']['name']
            level  = vgd['level_learned_at']

        seen.add(move_en)
        result.append({'en': move_en, 'method': method, 'level': level})

    return result


# ─── 로드 ───
with open('data/quiz_pokemon.json', encoding='utf-8') as f:
    pokemon = json.load(f)
with open('data/quiz_moves.json', encoding='utf-8') as f:
    moves = json.load(f)

# PokeAPI uses hyphens ("dragon-ascent") but quiz_moves.json uses spaces ("dragon ascent")
# Build a hyphen-normalized set so multi-word moves aren't silently dropped
known_moves = set(m['en'].replace(' ', '-') for m in moves)

# 수집 대상 목록 (원종 + 폼)
to_fetch = []
seen_names = set()
for p in pokemon:
    name = p['en'].lower().replace(' ', '-')
    if name not in seen_names:
        seen_names.add(name)
        to_fetch.append(name)
    if 'forms' in p:
        for f in p['forms']:
            fname = (f.get('name_en') or '').lower().replace(' ', '-')
            if fname and fname not in seen_names:
                seen_names.add(fname)
                to_fetch.append(fname)

# 기존 캐시 불러오기 (재실행 시 이어서 진행)
cache_file = 'data/learnsets.json'
if os.path.exists(cache_file):
    with open(cache_file, encoding='utf-8') as f:
        learnsets = json.load(f)
    print(f"캐시 불러오기: {len(learnsets)}개")
else:
    learnsets = {}

# 수집
total = len(to_fetch)
done = 0
skipped = 0

for i, poke_en in enumerate(to_fetch):
    if poke_en in learnsets:
        skipped += 1
        continue

    result = get_learnset(poke_en, known_moves)
    if result is None:
        # 404 — 폼이 PokeAPI에 없음, 기록만 남기고 skip
        learnsets[poke_en] = []
    else:
        learnsets[poke_en] = result
    done += 1

    prog = i + 1
    print(f"[{prog}/{total}] {poke_en}: {len(learnsets[poke_en])}개 기술")

    # 50개마다 중간 저장
    if done % 50 == 0:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(learnsets, f, ensure_ascii=False)

    time.sleep(0.08)

# 최종 저장
with open(cache_file, 'w', encoding='utf-8') as f:
    json.dump(learnsets, f, ensure_ascii=False)

total_moves = sum(len(v) for v in learnsets.values() if v)
print(f"\n✅ 완료: {len(learnsets)}개 포켓몬, 총 {total_moves}개 기술 레코드")
print(f"   캐시 스킵: {skipped}개")
