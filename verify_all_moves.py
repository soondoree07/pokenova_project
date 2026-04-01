#!/usr/bin/env python3
"""
quiz_moves.json 전체 기술 데이터 PokeAPI 검증 스크립트
실행: python3 verify_all_moves.py
"""

import json
import urllib.request
import time
import os

TYPE_KO = {
    'normal':'노말', 'fire':'불꽃', 'water':'물', 'electric':'전기', 'grass':'풀',
    'ice':'얼음', 'fighting':'격투', 'poison':'독', 'ground':'땅', 'flying':'비행',
    'psychic':'에스퍼', 'bug':'벌레', 'rock':'바위', 'ghost':'고스트', 'dragon':'드래곤',
    'dark':'악', 'steel':'강철', 'fairy':'페어리'
}
CLASS_KO = { 'physical':'물리', 'special':'특수', 'status':'변화' }
GEN_KO = {
    'generation-i':'1세대', 'generation-ii':'2세대', 'generation-iii':'3세대',
    'generation-iv':'4세대', 'generation-v':'5세대', 'generation-vi':'6세대',
    'generation-vii':'7세대', 'generation-viii':'8세대', 'generation-ix':'9세대'
}

os.chdir('/home/soondoree07/pokenova_project')

def fetch(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'pokenova/1.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(1)
        except Exception:
            time.sleep(1.2)
    return None

with open('data/quiz_moves.json', 'r', encoding='utf-8') as f:
    moves = json.load(f)

# hidden 플래그 있는 기술 제외 여부 확인
hidden_count = sum(1 for m in moves if m.get('hidden'))
print(f"전체 기술: {len(moves)}개 (hidden: {hidden_count}개)")

errors = {}   # id -> {move, issues, api_data}
api_missing = []  # 404 기술
skipped = []  # 고의로 skip (Z기술, 다이맥스 등)

# 검증 제외: Z기술(622-702), 다이맥스 Max Move(743-774) → power/accuracy가 원래 없음
SKIP_RANGES = set(range(622, 703)) | set(range(743, 775))

total = len(moves)
for i, move in enumerate(sorted(moves, key=lambda x: x.get('id', 0))):
    mid = move.get('id', 0)
    pct = (i+1)/total*100
    print(f"\r  [{i+1}/{total}] {pct:.0f}% ID {mid} {move.get('ko','')[:8]:<8}", end='', flush=True)

    if move.get('hidden'):
        continue
    if mid in SKIP_RANGES:
        skipped.append(move)
        continue

    data = fetch(f'https://pokeapi.co/api/v2/move/{mid}/')
    if data is None:
        api_missing.append(move)
        time.sleep(0.2)
        continue

    api_gen   = GEN_KO.get(data['generation']['name'], data['generation']['name'])
    api_type  = TYPE_KO.get(data['type']['name'], data['type']['name'])
    api_class = CLASS_KO.get(data['damage_class']['name'], data['damage_class']['name'])
    api_power = data.get('power')
    if api_power == 0:
        api_power = None
    api_acc   = data.get('accuracy')
    api_en    = data.get('name', '')   # lowercase-hyphen

    # 우리 데이터 en을 같은 형식으로 정규화
    our_en = move.get('en', '').lower().replace(' ', '-')

    issues = {}
    if api_gen != move.get('gen'):
        issues['gen'] = (move.get('gen'), api_gen)
    if api_type != move.get('type'):
        issues['type'] = (move.get('type'), api_type)
    if api_class != move.get('class'):
        issues['class'] = (move.get('class'), api_class)
    if api_power != move.get('power'):
        issues['power'] = (move.get('power'), api_power)
    if api_acc != move.get('accuracy'):
        issues['accuracy'] = (move.get('accuracy'), api_acc)
    if api_en != our_en and our_en:
        issues['en'] = (move.get('en'), api_en)

    if issues:
        errors[mid] = {'move': move, 'issues': issues, 'api': data}

    time.sleep(0.25)

print()  # newline

# 결과 저장
result = {
    'errors': {
        str(mid): {
            'ko': v['move'].get('ko'),
            'en': v['move'].get('en'),
            'issues': {k: {'current': cur, 'api': api} for k, (cur, api) in v['issues'].items()}
        }
        for mid, v in sorted(errors.items())
    },
    'api_missing': [{'id': m.get('id'), 'ko': m.get('ko'), 'en': m.get('en')} for m in api_missing],
    'skipped': len(skipped)
}

with open('data/verify_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# 요약 출력
print(f"\n=== 검증 완료 ===")
print(f"오류 기술: {len(errors)}개")
print(f"API 없음(404): {len(api_missing)}개")
print(f"검증 제외(Z기술/다이맥스): {len(skipped)}개")
print()

# 오류 상세
if errors:
    print("=== 오류 목록 ===")
    by_issue = {}
    for mid, v in sorted(errors.items()):
        for k in v['issues']:
            by_issue.setdefault(k, []).append((mid, v))

    for issue_type in ['gen', 'type', 'class', 'power', 'accuracy', 'en']:
        items = by_issue.get(issue_type, [])
        if items:
            print(f"\n[{issue_type} 오류 {len(items)}개]")
            for mid, v in items:
                cur, api = v['issues'][issue_type]
                print(f"  [{mid}] {v['move'].get('ko')} ({v['move'].get('en')}): {cur} → {api}")

if api_missing:
    print(f"\n=== API 없음 (404) ===")
    for m in api_missing:
        print(f"  [{m['id']}] {m['ko']} ({m['en']})")
