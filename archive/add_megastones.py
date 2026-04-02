import json

with open('data/quiz_items.json', encoding='utf-8') as f:
    current_items = json.load(f)

existing_en = {it['en'].lower() for it in current_items}
max_id = max(it['id'] for it in current_items)

new_stones = [
    # legends_za
    {"koName":"픽시나이트","enName":"Clefablite","desc":"픽시에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/b/b2/%EC%95%84%EC%9D%B4%EC%BD%98_%ED%94%BD%EC%8B%9C%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"우츠보트나이트","enName":"Victreebelite","desc":"우츠보트에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/f/f1/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%9A%B0%EC%B8%A0%EB%B3%B4%ED%8A%B8%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"아쿠스타나이트","enName":"Starminite","desc":"아쿠스타에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/8/88/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%95%84%EC%BF%A0%EC%8A%A4%ED%83%80%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"망나뇽나이트","enName":"Dragoninite","desc":"망나뇽에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/7/70/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%A7%9D%EB%82%98%EB%87%BD%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"메가니움나이트","enName":"Meganiumite","desc":"메가니움에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/c/c8/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%A9%94%EA%B0%80%EB%8B%88%EC%9B%80%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"장크로다일나이트","enName":"Feraligite","desc":"장크로다일에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/f/f2/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%9E%A5%ED%81%AC%EB%A1%9C%EB%8B%A4%EC%9D%BC%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"무장조나이트","enName":"Skarmorite","desc":"무장조에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/3/35/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%AC%B4%EC%9E%A5%EC%A1%B0%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"눈여아나이트","enName":"Froslassite","desc":"눈여아에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/2/29/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%88%88%EC%97%AC%EC%95%84%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"염무왕나이트","enName":"Emboarite","desc":"염무왕에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/7/75/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%97%BC%EB%AC%B4%EC%99%95%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"몰드류나이트","enName":"Excadrite","desc":"몰드류에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/2/21/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%AA%B0%EB%93%9C%EB%A5%98%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"펜드라나이트","enName":"Scolipite","desc":"펜드라에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/d/d1/%EC%95%84%EC%9D%B4%EC%BD%98_%ED%8E%9C%EB%93%9C%EB%9D%BC%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"곤율거니나이트","enName":"Scraftinite","desc":"곤율거니에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/c/c2/%EC%95%84%EC%9D%B4%EC%BD%98_%EA%B3%A4%EC%9C%A8%EA%B1%B0%EB%8B%88%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"저리더프나이트","enName":"Eelektrossite","desc":"저리더프에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/5/53/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%A0%80%EB%A6%AC%EB%8D%94%ED%94%84%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"샹델라나이트","enName":"Chandelurite","desc":"샹델라에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/6/62/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%83%B9%EB%8D%B8%EB%9D%BC%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"브리가론나이트","enName":"Chesnaughtite","desc":"브리가론에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/4/41/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%B8%8C%EB%A6%AC%EA%B0%80%EB%A1%A0%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"마폭시나이트","enName":"Delphoxite","desc":"마폭시에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/d/db/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%A7%88%ED%8F%AD%EC%8B%9C%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"개굴닌자나이트","enName":"Greninjite","desc":"개굴닌자에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/6/64/%EC%95%84%EC%9D%B4%EC%BD%98_%EA%B0%9C%EA%B5%B4%EB%8B%8C%EC%9E%90%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"화염레오나이트","enName":"Pyroarite","desc":"화염레오에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/b/b8/%EC%95%84%EC%9D%B4%EC%BD%98_%ED%99%94%EC%97%BC%EB%A0%88%EC%98%A4%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"플라엣테나이트","enName":"Floettite","desc":"특별한 플라엣테에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/2/2d/%EC%95%84%EC%9D%B4%EC%BD%98_%ED%94%8C%EB%9D%BC%EC%97%A3%ED%85%8C%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"칼라마네로나이트","enName":"Malamarite","desc":"칼라마네로에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/9/96/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%B9%BC%EB%9D%BC%EB%A7%88%EB%84%A4%EB%A1%9C%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"거북손데스나이트","enName":"Barbaracite","desc":"거북손데스에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/e/e0/%EC%95%84%EC%9D%B4%EC%BD%98_%EA%B1%B0%EB%B6%81%EC%86%90%EB%8D%B0%EC%8A%A4%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"드래캄나이트","enName":"Dragalgite","desc":"드래캄에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/4/4e/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%93%9C%EB%9E%98%EC%BA%84%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"루차불나이트","enName":"Hawluchanite","desc":"루차불에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/7/7b/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%A3%A8%EC%B0%A8%EB%B6%88%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"지가르데나이트","enName":"Zygardite","desc":"지가르데에게 지니게 하면 배틀할 때 퍼펙트폼 상태에서 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/3/3d/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%A7%80%EA%B0%80%EB%A5%B4%EB%8D%B0%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"할비롱나이트","enName":"Drampanite","desc":"할비롱에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/2/2a/%EC%95%84%EC%9D%B4%EC%BD%98_%ED%95%A0%EB%B9%84%EB%A1%B1%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"대여르나이트","enName":"Falinksite","desc":"대여르에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/f/f5/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%8C%80%EC%97%AC%EB%A5%B4%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    # mega_rush
    {"koName":"히드런나이트","enName":"Heatranite","desc":"히드런에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/7/7b/%EC%95%84%EC%9D%B4%EC%BD%98_%ED%9E%88%EB%93%9C%EB%9F%B0%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"다크라이나이트","enName":"Darkranite","desc":"다크라이에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/a/a2/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%8B%A4%ED%81%AC%EB%9D%BC%EC%9D%B4%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"제라오라나이트","enName":"Zeraorite","desc":"제라오라에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/e/e6/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%A0%9C%EB%9D%BC%EC%98%A4%EB%9D%BC%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"라이츄나이트X","enName":"Raichunite X","desc":"라이츄에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/6/64/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%9D%BC%EC%9D%B4%EC%B8%84%EB%82%98%EC%9D%B4%ED%8A%B8X_ZA.png"},
    {"koName":"라이츄나이트Y","enName":"Raichunite Y","desc":"라이츄에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/c/c3/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%9D%BC%EC%9D%B4%EC%B8%84%EB%82%98%EC%9D%B4%ED%8A%B8Y_ZA.png"},
    {"koName":"치렁나이트","enName":"Chimechite","desc":"치렁에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/0/07/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%B9%98%EB%A0%81%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"앱솔나이트Z","enName":"Absolite Z","desc":"앱솔에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/e/ea/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%95%B1%EC%86%94%EB%82%98%EC%9D%B4%ED%8A%B8Z_ZA.png"},
    {"koName":"찌르호크나이트","enName":"Staraptite","desc":"찌르호크에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/3/36/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%B0%8C%EB%A5%B4%ED%98%B8%ED%81%AC%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"한카리아스나이트Z","enName":"Garchompite Z","desc":"한카리아스에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/2/23/%EC%95%84%EC%9D%B4%EC%BD%98_%ED%95%9C%EC%B9%B4%EB%A6%AC%EC%95%84%EC%8A%A4%EB%82%98%EC%9D%B4%ED%8A%B8Z_ZA.png"},
    {"koName":"루카리오나이트Z","enName":"Lucarionite Z","desc":"루카리오에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/2/2a/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%A3%A8%EC%B9%B4%EB%A6%AC%EC%98%A4%EB%82%98%EC%9D%B4%ED%8A%B8Z_ZA.png"},
    {"koName":"골루그나이트","enName":"Golurkite","desc":"골루그에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/5/5d/%EC%95%84%EC%9D%B4%EC%BD%98_%EA%B3%A8%EB%A3%A8%EA%B7%B8%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"냐오닉스나이트","enName":"Meowsticite","desc":"냐오닉스에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/2/23/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%83%90%EC%98%A4%EB%8B%89%EC%8A%A4%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"모단단게나이트","enName":"Crabominite","desc":"모단단게에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/a/af/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%AA%A8%EB%8B%A8%EB%8B%A8%EA%B2%8C%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"갑주무사나이트","enName":"Golisopite","desc":"갑주무사에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/6/67/%EC%95%84%EC%9D%B4%EC%BD%98_%EA%B0%91%EC%A3%BC%EB%AC%B4%EC%82%AC%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"마기아나이트","enName":"Magearnite","desc":"마기아나에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/7/79/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%A7%88%EA%B8%B0%EC%95%84%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"스코빌런나이트","enName":"Scovillainite","desc":"스코빌런에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/f/f3/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%8A%A4%EC%BD%94%EB%B9%8C%EB%9F%B0%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"드닐레이브나이트","enName":"Baxcalibrite","desc":"드닐레이브에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/d/df/%EC%95%84%EC%9D%B4%EC%BD%98_%EB%93%9C%EB%8B%90%EB%A0%88%EC%9D%B4%EB%B8%8C%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"싸리용나이트","enName":"Tatsugirinite","desc":"싸리용에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/2/2c/%EC%95%84%EC%9D%B4%EC%BD%98_%EC%8B%B8%EB%A6%AC%EC%9A%A9%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
    {"koName":"킬라플로르나이트","enName":"Glimmoranite","desc":"킬라플로르에게 지니게 하면 배틀할 때 메가진화할 수 있는 신비한 메가스톤의 일종.","imgUrl":"https://static.wikia.nocookie.net/pokemon/images/7/73/%EC%95%84%EC%9D%B4%EC%BD%98_%ED%82%AC%EB%9D%BC%ED%94%8C%EB%A1%9C%EB%A5%B4%EB%82%98%EC%9D%B4%ED%8A%B8_ZA.png"},
]

added = []
skipped = []

for item in new_stones:
    en_lower = item['enName'].lower()
    if en_lower in existing_en:
        skipped.append(item['koName'])
        continue
    max_id += 1
    new_item = {
        "id": max_id,
        "ko": item['koName'],
        "en": en_lower,
        "desc": item['desc'],
        "desc_lang": "ko",
        "sprite": item['imgUrl'],
        "category": "mega-stones"
    }
    current_items.append(new_item)
    existing_en.add(en_lower)
    added.append(new_item)

with open('data/quiz_items.json', 'w', encoding='utf-8') as f:
    json.dump(current_items, f, ensure_ascii=False, indent=2)

print(f"✅ 추가: {len(added)}개")
for it in added:
    print(f"  {it['ko']} (id:{it['id']})")
if skipped:
    print(f"\n⏭ 스킵: {len(skipped)}개")
    for n in skipped:
        print(f"  {n}")
