import json, re

with open('data/quiz_items.json') as f:
    items = json.load(f)
with open('data/quiz_pokemon.json') as f:
    pokemon = json.load(f)

# Build: base_ko -> { variant -> form }
mega_forms = {}
for p in pokemon:
    if 'forms' in p:
        for f in p['forms']:
            if f.get('type') == 'mega':
                key = p['ko']
                if key not in mega_forms:
                    mega_forms[key] = {}
                mk = f['name_ko']
                var_match = re.search(r' ([XYZ])$', mk)
                var = var_match.group(1) if var_match else ''
                mega_forms[key][var] = {
                    'mega_ko': mk,
                    'mega_en': f['name_en'],
                    'base_id': p['id'],
                }

name_fix = {
    '후디': '후딘',
    '마기아': '마기아나',
}

updated = 0
for item in items:
    if item.get('category') != 'mega-stones':
        continue
    sname = item['ko']
    suffix = re.match(r'^(.+?)나이트([XYZ]?)$', sname)
    if not suffix:
        continue
    base = name_fix.get(suffix.group(1), suffix.group(1))
    var = suffix.group(2)
    if base not in mega_forms:
        continue
    forms = mega_forms[base]
    form = forms.get(var) or forms.get('')
    if form:
        item['mega_ko'] = form['mega_ko']
        item['mega_en'] = form['mega_en']
        item['base_id'] = form['base_id']
        updated += 1

with open('data/quiz_items.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f'✅ {updated}개 메가스톤에 매칭 정보 추가 완료')
