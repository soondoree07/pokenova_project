"""
포켓몬별 기술 학습 데이터 수집 (PokeAPI → data/learnsets.json)
- SV 등장 포켓몬: SV(scarlet-violet/teal-mask/indigo-disk) 기준
- SV 미등장 포켓몬: 가장 최신 버전 기준
- 메가진화/거다이맥스: 원종의 기술 그대로 복사
- 재실행 시 캐시 이어서 진행
"""
import json, time, os
import urllib.request, urllib.error

def normalize(name):
    """quiz_moves.json 과 PokeAPI 이름을 동일 형식으로 정규화 (소문자+하이픈, 따옴표 제거)"""
    return name.lower().replace(' ', '-').replace("'", '')

SV_GROUPS = {'scarlet-violet', 'the-teal-mask', 'the-indigo-disk'}

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

def get_learnset(poke_en):
    """SV 우선, 없으면 최신 버전으로 fallback. 404면 None."""
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_en}/"
    try:
        data = fetch_json(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        print(f"  HTTP {e.code}: {poke_en}")
        return []
    except Exception as e:
        print(f"  Error {poke_en}: {e}")
        return []

    raw_moves = data.get('moves', [])

    # 사용 가능한 버전 그룹 수집
    vg_set = set()
    for m in raw_moves:
        for vgd in m.get('version_group_details', []):
            vg_set.add(vgd['version_group']['name'])

    # 최신 버전 그룹 선택 (SV 우선 → VERSION_PRIORITY 순)
    best_vg = next((vg for vg in VERSION_PRIORITY if vg in vg_set), None)
    if not best_vg:
        return []

    result = []
    seen = set()
    for m in raw_moves:
        move_en = m['move']['name']
        if move_en in seen:
            continue

        vgd = next((v for v in m['version_group_details']
                    if v['version_group']['name'] == best_vg), None)
        if not vgd:
            continue

        seen.add(move_en)
        result.append({
            'en': move_en,
            'method': vgd['move_learn_method']['name'],
            'level': vgd['level_learned_at'],
        })

    return result


# ─── 로드 ───
with open('data/quiz_pokemon.json', encoding='utf-8') as f:
    pokemon = json.load(f)

# 메가/거다이맥스 폼 → 원종 이름 매핑
INHERIT_TYPES = {'mega', 'gmax'}
form_base_map = {}   # fname -> base_name (원종 EN)
for p in pokemon:
    base_name = p['en'].lower().replace(' ', '-')
    for form in p.get('forms', []):
        fname = (form.get('name_en') or '').lower()
        ftype = form.get('type', 'alt')
        if ftype in INHERIT_TYPES and fname:
            form_base_map[fname] = base_name

print(f"메가/거다이맥스 상속 매핑: {len(form_base_map)}개")

# 수집 대상 목록 (원종 먼저, 폼 나중)
base_names = []
form_names = []
seen_names = set()

for p in pokemon:
    base_name = p['en'].lower().replace(' ', '-')
    if base_name not in seen_names:
        seen_names.add(base_name)
        base_names.append(base_name)
    for form in p.get('forms', []):
        fname = (form.get('name_en') or '').lower()
        if fname and fname not in seen_names:
            seen_names.add(fname)
            form_names.append(fname)

to_fetch_api   = [n for n in base_names + form_names if n not in form_base_map]
to_inherit     = [n for n in form_names if n in form_base_map]

print(f"API 수집 대상: {len(to_fetch_api)}개 / 원종 상속: {len(to_inherit)}개")

# 기존 캐시 불러오기
CACHE_FILE    = 'data/learnsets_cache.json'
LEARNSET_FILE = 'data/learnsets.json'

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, encoding='utf-8') as f:
        learnsets = json.load(f)
    print(f"캐시 불러오기: {len(learnsets)}개")
else:
    learnsets = {}

# ─── STEP 1: API 수집 ───
print(f"\n[STEP 1] API 수집 ({len(to_fetch_api)}마리)")
total = len(to_fetch_api)
done = skipped = 0

for i, poke_en in enumerate(to_fetch_api):
    if poke_en in learnsets:
        skipped += 1
        continue

    result = get_learnset(poke_en)
    learnsets[poke_en] = [] if result is None else result
    done += 1

    print(f"  [{i+1}/{total}] {poke_en}: {len(learnsets[poke_en])}개")

    if done % 50 == 0:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(learnsets, f, ensure_ascii=False)

    time.sleep(0.08)

with open(CACHE_FILE, 'w', encoding='utf-8') as f:
    json.dump(learnsets, f, ensure_ascii=False)
print(f"  → 캐시 저장 (스킵: {skipped}개)")

# ─── STEP 2: 메가/거다이맥스 원종 기술 상속 ───
print(f"\n[STEP 2] 메가/거다이맥스 원종 기술 상속 ({len(to_inherit)}개)")
for fname in to_inherit:
    base = form_base_map[fname]
    learnsets[fname] = learnsets.get(base, [])
    print(f"  {fname} ← {base} ({len(learnsets[fname])}개)")

# quiz_moves.json 기준 허용 기술 목록 (정규화된 이름 → 원본 en)
with open('data/quiz_moves.json', encoding='utf-8') as f:
    quiz_moves = json.load(f)

known_moves = {normalize(m['en']): m['en'] for m in quiz_moves}
print(f"\n[STEP 3] quiz_moves.json 기준 필터링 (허용 기술: {len(known_moves)}개)")

filtered_out = {}
for poke, moves in learnsets.items():
    before = len(moves)
    filtered = [m for m in moves if normalize(m['en']) in known_moves]
    removed = before - len(filtered)
    if removed:
        filtered_out[poke] = [m['en'] for m in moves if normalize(m['en']) not in known_moves]
    learnsets[poke] = filtered

if filtered_out:
    print(f"  제거된 기술 있는 포켓몬: {len(filtered_out)}개")
    for poke, removed in list(filtered_out.items())[:10]:
        print(f"    {poke}: {removed}")
    if len(filtered_out) > 10:
        print(f"    ... 외 {len(filtered_out)-10}개")
else:
    print("  제거된 기술 없음 (전부 매칭)")

# 최종 저장 (포켓몬 알파벳순, 기술은 method→level 순 정렬, 가독성 포맷)
def sort_key(move):
    order = {'level-up': 0, 'machine': 1, 'egg': 2, 'tutor': 3}
    return (order.get(move.get('method', ''), 9), move.get('level', 0))

def dedup(moves):
    # 정렬 후 같은 기술명은 첫 번째(우선순위 높은 것)만 유지
    seen = set()
    result = []
    for m in sorted(moves, key=sort_key):
        if m['en'] not in seen:
            seen.add(m['en'])
            result.append(m)
    return result

sorted_learnsets = {
    k: dedup(v)
    for k, v in sorted(learnsets.items())
}

with open(LEARNSET_FILE, 'w', encoding='utf-8') as f:
    json.dump(sorted_learnsets, f, ensure_ascii=False, indent=2)

total_moves = sum(len(v) for v in learnsets.values())
print(f"\n✅ 완료: {len(learnsets)}마리, 총 {total_moves}개 기술 레코드")
print(f"   캐시 스킵: {skipped}개")
