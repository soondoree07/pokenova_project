"""
SV(9세대) 기술 데이터 수집
1. 모든 포켓몬의 SV 기술 리스트 → data/learnsets.json 재구축
2. quiz_moves.json에 없는 기술 감지 → 자동 추가
3. 한국어 설명 없는 기술 → data/missing_ko_moves.json 에 리스트화

실행: python3 build_sv_learnsets.py
재실행 시 캐시 이어서 진행
"""
import json, time, os
import urllib.request, urllib.error

SV_GROUPS = {'scarlet-violet', 'the-teal-mask', 'the-indigo-disk'}

TYPE_KO = {
    'normal': '노말', 'fire': '불꽃', 'water': '물', 'electric': '전기',
    'grass': '풀', 'ice': '얼음', 'fighting': '격투', 'poison': '독',
    'ground': '땅', 'flying': '비행', 'psychic': '에스퍼', 'bug': '벌레',
    'rock': '바위', 'ghost': '고스트', 'dragon': '드래곤', 'dark': '악',
    'steel': '강철', 'fairy': '페어리', 'stellar': '스텔라',
}

GEN_MAP = {
    1: '1세대', 2: '2세대', 3: '3세대', 4: '4세대', 5: '5세대',
    6: '6세대', 7: '7세대', 8: '8세대', 9: '9세대',
}

CLASS_KO = {'physical': '물리', 'special': '특수', 'status': '변화'}

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'pokenova-builder/1.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())

def get_sv_learnset(poke_en):
    """포켓몬의 SV 기술 리스트 반환. 404면 None, SV 없으면 []"""
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

    result = []
    seen = set()
    for m in data.get('moves', []):
        move_en = m['move']['name']
        if move_en in seen:
            continue

        # SV 버전 그룹에서 배우는지 확인
        sv_vgd = None
        for vgd in m['version_group_details']:
            if vgd['version_group']['name'] in SV_GROUPS:
                sv_vgd = vgd
                break

        if not sv_vgd:
            continue

        seen.add(move_en)
        result.append({
            'en': move_en,
            'method': sv_vgd['move_learn_method']['name'],
            'level': sv_vgd['level_learned_at'],
        })

    return result


def fetch_move_data(move_en):
    """PokeAPI에서 기술 상세 정보 가져오기"""
    url = f"https://pokeapi.co/api/v2/move/{move_en}/"
    try:
        data = fetch_json(url)
    except Exception as e:
        print(f"  Move fetch error {move_en}: {e}")
        return None

    move_id = data['id']

    # 한국어 이름
    ko_name = next((n['name'] for n in data.get('names', [])
                    if n['language']['name'] == 'ko'), None)

    # 영문 이름 (표시용, 공백 포맷)
    en_name = next((n['name'] for n in data.get('names', [])
                    if n['language']['name'] == 'en'), move_en.replace('-', ' '))

    # 한국어 설명 (flavor text — 최신 SV 우선)
    ko_desc = None
    en_desc = None
    sv_versions = {'scarlet', 'violet'}
    for ft in reversed(data.get('flavor_text_entries', [])):
        lang = ft['language']['name']
        ver = ft.get('version', {}).get('name', '')
        if lang == 'ko' and ko_desc is None:
            ko_desc = ft['flavor_text'].replace('\n', ' ').replace('\f', ' ')
        if lang == 'en' and en_desc is None:
            en_desc = ft['flavor_text'].replace('\n', ' ').replace('\f', ' ')

    # 타입
    type_en = data.get('type', {}).get('name', '')
    type_ko = TYPE_KO.get(type_en, type_en)

    # 분류
    class_en = data.get('damage_class', {}).get('name', '')
    class_ko = CLASS_KO.get(class_en, class_en)

    # 세대
    gen_url = data.get('generation', {}).get('url', '')
    gen_num = int(gen_url.rstrip('/').split('/')[-1]) if gen_url else 0
    gen_ko = GEN_MAP.get(gen_num, f'{gen_num}세대')

    pp     = data.get('pp')
    power  = data.get('power')
    acc    = data.get('accuracy')

    entry = {
        'id': move_id,
        'ko': ko_name or en_name,
        'en': en_name,
        'type': type_ko,
        'type_en': type_en,
        'class': class_ko,
        'pp': pp,
        'power': power,
        'accuracy': acc,
        'gen': gen_ko,
    }

    if ko_desc:
        entry['desc'] = ko_desc
        entry['desc_lang'] = 'ko'
    elif en_desc:
        entry['desc'] = en_desc
        entry['desc_lang'] = 'en'
    else:
        entry['desc'] = ''
        entry['desc_lang'] = 'none'

    if not ko_name:
        entry['needs_ko'] = True

    return entry


# ─── 로드 ───
with open('data/quiz_pokemon.json', encoding='utf-8') as f:
    pokemon = json.load(f)
with open('data/quiz_moves.json', encoding='utf-8') as f:
    moves_list = json.load(f)

# quiz_moves 룩업: hyphen 형식으로 정규화
existing_move_by_hyphen = {m['en'].replace(' ', '-'): m for m in moves_list}
existing_move_by_space  = {m['en']: m for m in moves_list}

# 수집 대상 포켓몬 목록
to_fetch = []
seen_names = set()
for p in pokemon:
    name = p['en'].lower().replace(' ', '-')
    if name not in seen_names:
        seen_names.add(name); to_fetch.append(name)
    for form in p.get('forms', []):
        fname = (form.get('name_en') or '').lower().replace(' ', '-')
        if fname and fname not in seen_names:
            seen_names.add(fname); to_fetch.append(fname)

# SV 전용 캐시 파일 (기존 learnsets.json과 분리)
# 수집 완료 후 learnsets.json으로 교체
LEARNSET_FILE = 'data/learnsets.json'
CACHE_FILE    = 'data/learnsets_sv_cache.json'

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, encoding='utf-8') as f:
        learnsets = json.load(f)
    print(f"SV 캐시 불러오기: {len(learnsets)}개")
else:
    learnsets = {}

# ─── STEP 1: 포켓몬별 SV 기술 수집 ───
print(f"\n[STEP 1] SV 기술 수집 ({len(to_fetch)}마리)")
done = skipped = 0
total = len(to_fetch)

for i, poke_en in enumerate(to_fetch):
    if poke_en in learnsets:
        skipped += 1
        continue

    result = get_sv_learnset(poke_en)
    learnsets[poke_en] = [] if result is None else result
    done += 1

    sv_count = len(learnsets[poke_en])
    print(f"  [{i+1}/{total}] {poke_en}: SV {sv_count}개기술")

    if done % 50 == 0:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(learnsets, f, ensure_ascii=False)

    time.sleep(0.08)

# 캐시 저장
with open(CACHE_FILE, 'w', encoding='utf-8') as f:
    json.dump(learnsets, f, ensure_ascii=False)
print(f"  → SV 캐시 저장 완료 (스킵: {skipped}개)")

# ─── STEP 2: quiz_moves에 없는 기술 감지 ───
print("\n[STEP 2] 미수록 기술 감지")
all_sv_moves = set()
for ls in learnsets.values():
    for m in ls:
        all_sv_moves.add(m['en'])  # hyphen 형식

missing_move_ens = sorted(
    m for m in all_sv_moves
    if m not in existing_move_by_hyphen
)
print(f"  quiz_moves에 없는 SV 기술: {len(missing_move_ens)}개")
for m in missing_move_ens:
    print(f"    - {m}")

if not missing_move_ens:
    print("  (없음 — quiz_moves.json 완전함)")
else:
    # ─── STEP 3: 미수록 기술 데이터 수집 후 quiz_moves에 추가 ───
    print(f"\n[STEP 3] 미수록 기술 {len(missing_move_ens)}개 데이터 수집")
    new_entries = []
    missing_ko  = []

    for move_en in missing_move_ens:
        print(f"  fetching: {move_en}")
        entry = fetch_move_data(move_en)
        if not entry:
            continue

        new_entries.append(entry)
        if entry.get('needs_ko') or entry.get('desc_lang') != 'ko':
            missing_ko.append(entry)

        time.sleep(0.1)

    # quiz_moves.json에 추가 후 id순 정렬
    moves_list.extend(new_entries)
    moves_list.sort(key=lambda m: m['id'])

    with open('data/quiz_moves.json', 'w', encoding='utf-8') as f:
        json.dump(moves_list, f, ensure_ascii=False, indent=2)
    print(f"  → quiz_moves.json 업데이트: +{len(new_entries)}개 (총 {len(moves_list)}개)")

    # 한국어 미번역 리스트 저장
    if missing_ko:
        with open('data/missing_ko_moves.json', 'w', encoding='utf-8') as f:
            json.dump(missing_ko, f, ensure_ascii=False, indent=2)
        print(f"\n⚠️  한국어 이름/설명 없는 기술: {len(missing_ko)}개")
        print(f"   → data/missing_ko_moves.json 에 저장")
        for m in missing_ko:
            flag = '(이름없음)' if m.get('needs_ko') else '(설명없음)'
            print(f"    - [{m['id']}] {m['en']} {flag}")

# learnsets.json 최종 교체 (quiz_moves와 동기화된 후)
with open(LEARNSET_FILE, 'w', encoding='utf-8') as f:
    json.dump(learnsets, f, ensure_ascii=False)
print(f"  → learnsets.json 교체 완료")

total_sv = sum(len(v) for v in learnsets.values())
print(f"\n✅ 완료: {len(learnsets)}마리, SV 기술 레코드 총 {total_sv}개")
