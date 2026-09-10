"""
일본어 이름 수집 — PokeAPI + 포켓몬위키 대조 (data/*.json 의 ja 필드)

  python3 scripts/fetch_japanese_names.py --check          # 저장 없이 무엇이 바뀔지만 본다
  python3 scripts/fetch_japanese_names.py                  # 전부 반영
  python3 scripts/fetch_japanese_names.py items abilities  # 일부만

⚠️ 예전 판이 도구 일본어 이름 121개를 망가뜨린 이유
  `/api/v2/item/{우리 id}` 로 물었다. 우리 내부 번호와 PokeAPI 번호가 같다고
  본 것인데 다르다. 583번 도구(요정의깃털)를 물으면 PokeAPI 583번(루가루암 Z)이
  돌아온다. 349번 이후가 통째로 밀려 있었다.
  → 지금은 **이름(슬러그)으로** 묻는다. 번호로 묻는 곳은 포켓몬뿐인데,
    포켓몬은 우리 id 가 곧 전국도감 번호이고 PokeAPI species 번호와 같다(확인함).

출처 두 곳을 대조한다
  PokeAPI    공식 게임 텍스트. 여기에 값이 있으면 이것을 쓴다
  포켓몬위키  PokeAPI 에 없는 것(챔피언스 신규 메가스톤 34종)을 채우고,
             값이 바뀌는 항목을 한 번 더 확인하는 용도
  둘이 다르면 **PokeAPI 를 쓰고 불일치를 화면에 남긴다.** 실측해 보니 어긋난
  세 건(달콤한꿀·꿀맛사과·녹슨방패)이 전부 위키 쪽 문제였다 — 문서 첫 줄 서식이
  달라 잘못 끊기거나(달콤한꿀·꿀맛사과), 아예 다른 도구 이름이 적혀 있었다(녹슨방패).
  PokeAPI 가 틀린 것이 확인되면 WIKI_OVERRIDE 에 그 항목만 적는다.

어느 쪽에도 없으면 **건드리지 않고 보고한다.** 이름을 지어내지 않는다.
거다이맥스 기술 33종이 그렇다 — PokeAPI 에 항목이 없고(맥스 기술만 있다)
포켓몬위키에도 기술별 문서가 없어서, 일본어 이름을 넣을 근거가 아직 없다.
"""
import json, os, re, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
CACHE = os.path.join(os.path.dirname(DATA), '.name_cache')

# PokeAPI 슬러그가 우리와 다른 것. 확인한 것만 적는다.
ITEM_SLUG = {'leek': 'stick'}                        # 대파는 PokeAPI 가 아직 구 이름
MOVE_SLUG = {'10,000,000_volt_thunderbolt': '10-000-000-volt-thunderbolt'}  # 쉼표는 하이픈
ABILITY_SLUG_BY_ID = {266: 'as-one-glastrier',       # 혼연일체는 우리 데이터가 두 항목
                      267: 'as-one-spectrier'}
ABILITY_SLUG = {'drill_pierce': 'piercing-drill', 'dragon_skin': 'dragonize',
                'mega_solar': 'mega-sol', 'habanero_burst': 'spicy-spray'}
# PokeAPI 가 틀렸다고 확인한 항목만 위키 값을 쓴다. 지금은 없다.
WIKI_OVERRIDE: set[str] = set()


def _cached(name, fetch):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, re.sub(r'[^\w.-]', '_', name) + '.json')
    if os.path.exists(path):
        return json.load(open(path, encoding='utf-8'))
    value = fetch()
    json.dump(value, open(path, 'w', encoding='utf-8'), ensure_ascii=False)
    time.sleep(0.05)
    return value


def to_slug(name):
    """우리 이름 -> PokeAPI 슬러그. 악센트를 뗀다(poké_ball -> poke-ball)."""
    plain = unicodedata.normalize('NFKD', name)
    plain = ''.join(c for c in plain if not unicodedata.combining(c))
    return plain.lower().replace('_', '-')


def pokeapi(kind, slug):
    """PokeAPI 조회. 없으면 None."""
    def fetch():
        url = f'https://pokeapi.co/api/v2/{kind}/{urllib.parse.quote(slug)}/'
        req = urllib.request.Request(url, headers={'User-Agent': 'pokenova/1.0'})
        try:
            return json.loads(urllib.request.urlopen(req, timeout=25).read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):   # 없는 이름이면 400 을 주기도 한다
                return None
            raise
    return _cached(f'api__{kind}__{slug}', fetch)


def pokeapi_ja(data):
    if not data:
        return None
    names = {n['language']['name']: n['name'] for n in data.get('names', [])}
    # ja 는 한자 포함 표기, ja-Hrkt 는 가나 표기. 게임 안 표기는 ja-Hrkt 쪽이다.
    text = names.get('ja-Hrkt') or names.get('ja-hrkt') or names.get('ja')
    return text.strip() if text else None


WIKI_PATTERNS = (
    re.compile(r'\|\s*일칭\s*=\s*([^|\n}]+)'),          # 특성·기술 정보상자
    re.compile(r'\(\s*일\s*:\s*(.+?)\s*(?:,|\)|영\s*:)'),  # 도구 문서 첫 줄
)


def wiki_ja(title):
    """포켓몬위키 문서에서 일본어 이름. 문서가 없거나 못 읽으면 None."""
    def fetch():
        params = urllib.parse.urlencode({
            'action': 'query', 'prop': 'revisions', 'rvprop': 'content',
            'rvslots': 'main', 'format': 'json', 'titles': title})
        req = urllib.request.Request(f'https://pokemon.fandom.com/ko/api.php?{params}',
                                     headers={'User-Agent': 'pokenova/1.0'})
        body = json.loads(urllib.request.urlopen(req, timeout=25).read().decode())
        for key, page in body['query']['pages'].items():
            if key == '-1':
                return None
            return page['revisions'][0]['slots']['main']['*']
        return None
    text = _cached(f'wiki__{title}', fetch)
    if not text:
        return None
    for pattern in WIKI_PATTERNS:
        m = pattern.search(text)
        if m and m.group(1).strip():
            return m.group(1).strip()
    return None


def resolve(row, api_data):
    """PokeAPI 와 위키를 대조해 최종 이름과 사유를 돌려준다."""
    api = pokeapi_ja(api_data)
    current = (row.get('ja') or '').strip()
    # 값이 그대로면 굳이 위키까지 묻지 않는다 (요청 수를 줄인다)
    if api and api == current:
        return current, None
    wiki = wiki_ja(row['ko'])
    if api and wiki and api != wiki:
        if row['en'] in WIKI_OVERRIDE:
            return wiki, f"{row['ko']} 불일치 — PokeAPI {api!r} / 위키 {wiki!r} → 위키 채택(확인함)"
        return api, f"{row['ko']} 불일치 — PokeAPI {api!r} / 위키 {wiki!r} → PokeAPI 채택"
    return (api or wiki), None


def run(kind, filename, slug_of):
    path = os.path.join(DATA, filename)
    rows = json.load(open(path, encoding='utf-8'))
    changed, missing, notes = [], [], []
    for row in rows:
        slug = slug_of(row)
        api_data = pokeapi(kind, slug) if slug else None
        name, note = resolve(row, api_data)
        if note:
            notes.append(note)
        if not name:
            missing.append(f"{row['ko']}({row['en']})")
            continue
        if (row.get('ja') or '') != name:
            changed.append((row['ko'], row.get('ja'), name))
            row['ja'] = name
    return rows, path, changed, missing, notes


TARGETS = {
    # 포켓몬만 번호로 묻는다. 우리 id = 전국도감 번호 = PokeAPI species 번호.
    'pokemon': ('pokemon-species', 'quiz_pokemon.json',
                lambda r: str(r['id']) if r['id'] <= 1025 else None),
    'moves': ('move', 'quiz_moves.json', lambda r: MOVE_SLUG.get(r['en'], to_slug(r['en']))),
    'items': ('item', 'quiz_items.json',
              lambda r: ITEM_SLUG.get(r['en'], to_slug(r['en']))),
    'abilities': ('ability', 'quiz_abilities.json',
                  lambda r: ABILITY_SLUG_BY_ID.get(r['id'])
                  or ABILITY_SLUG.get(r['en'], to_slug(r['en']))),
}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    check_only = '--check' in sys.argv
    for target in (args or TARGETS):
        kind, filename, slug_of = TARGETS[target]
        rows, path, changed, missing, notes = run(kind, filename, slug_of)
        print(f'\n[{target}] {len(rows)}개 — 바뀜 {len(changed)} · 못 찾음 {len(missing)}')
        for ko, before, after in changed:
            print(f'   {ko}: {before!r} -> {after!r}')
        for note in notes:
            print(f'   ※ {note}')
        if missing:
            print(f'   못 찾음: {", ".join(missing)}')
        if changed and not check_only:
            raw = open(path, encoding='utf-8').read()
            out = json.dumps(rows, ensure_ascii=False, indent=2)
            open(path, 'w', encoding='utf-8').write(out + '\n' if raw.endswith('\n') else out)
            print(f'   저장: {path}')
    if check_only:
        print('\n--check 라 저장하지 않았다')


if __name__ == '__main__':
    main()
