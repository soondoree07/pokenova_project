#!/usr/bin/env python3
"""
Gen 9 기술 데이터 수정 스크립트 (ID 850-884)
PokeAPI에서 올바른 타입/위력/명중/세대/영어명을 가져와서 quiz_moves.json 수정
한국어 이름(ko)과 설명(desc)은 보존
"""

import json
import urllib.request
import time

TYPE_KO = {
    'normal':'노말', 'fire':'불꽃', 'water':'물', 'electric':'전기', 'grass':'풀',
    'ice':'얼음', 'fighting':'격투', 'poison':'독', 'ground':'땅', 'flying':'비행',
    'psychic':'에스퍼', 'bug':'벌레', 'rock':'바위', 'ghost':'고스트', 'dragon':'드래곤',
    'dark':'악', 'steel':'강철', 'fairy':'페어리'
}

CLASS_KO = { 'physical':'물리', 'special':'특수', 'status':'변화' }

def fetch_json(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'pokenova/1.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            if i < retries - 1:
                time.sleep(1)
            else:
                print(f"  ERROR: {url} -> {e}")
                return None

def fix_moves():
    with open('data/quiz_moves.json', 'r', encoding='utf-8') as f:
        moves = json.load(f)

    # ID 850-884 기술만 선별
    target_ids = set(range(850, 885))
    fixed = []

    for move in moves:
        mid = move.get('id', 0)
        if mid not in target_ids:
            fixed.append(move)
            continue

        print(f"  [{mid}] {move.get('ko','?')} 수정 중...")

        data = fetch_json(f"https://pokeapi.co/api/v2/move/{mid}/")
        if not data:
            print(f"    -> PokeAPI 실패, 기존 데이터 유지 + gen만 9세대로 수정")
            move['gen'] = '9세대'
            fixed.append(move)
            continue

        # 영어 이름 (하이픈 제거, 첫글자만 대문자)
        en_name = data.get('name', move.get('en', ''))

        # 타입
        type_en = data.get('type', {}).get('name', '')
        type_ko = TYPE_KO.get(type_en, type_en)

        # 분류
        dc = data.get('damage_class', {}).get('name', '')
        class_ko = CLASS_KO.get(dc, dc)

        # PP
        pp = data.get('pp')

        # 위력 (0이면 null로)
        power = data.get('power')
        if power == 0:
            power = None

        # 명중률 (0이면 null로 - 반드시 명중)
        accuracy = data.get('accuracy')
        if accuracy == 0:
            accuracy = None

        new_move = {
            'id': mid,
            'ko': move['ko'],       # 보존
            'en': en_name,
            'type': type_ko,
            'type_en': type_en,
            'class': class_ko,
            'pp': pp,
            'power': power,
            'accuracy': accuracy,
            'gen': '9세대',
            'desc': move.get('desc', ''),
            'desc_lang': move.get('desc_lang', 'ko')
        }

        # 변경사항 출력
        changes = []
        if move.get('en') != en_name:
            changes.append(f"en: {move.get('en')} -> {en_name}")
        if move.get('type') != type_ko:
            changes.append(f"type: {move.get('type')} -> {type_ko}")
        if move.get('class') != class_ko:
            changes.append(f"class: {move.get('class')} -> {class_ko}")
        if move.get('power') != power:
            changes.append(f"power: {move.get('power')} -> {power}")
        if move.get('accuracy') != accuracy:
            changes.append(f"accuracy: {move.get('accuracy')} -> {accuracy}")
        if move.get('gen') != '9세대':
            changes.append(f"gen: {move.get('gen')} -> 9세대")
        if changes:
            print(f"    변경: {', '.join(changes)}")
        else:
            print(f"    변경 없음")

        fixed.append(new_move)
        time.sleep(0.3)  # API 부하 방지

    with open('data/quiz_moves.json', 'w', encoding='utf-8') as f:
        json.dump(fixed, f, ensure_ascii=False, indent=2)

    print(f"\n완료: 총 {len([m for m in fixed if 850 <= m.get('id',0) <= 884])}개 기술 수정됨")

if __name__ == '__main__':
    import os
    os.chdir('/home/soondoree07/pokenova_project')
    fix_moves()
