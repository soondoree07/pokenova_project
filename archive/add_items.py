import json

with open('data/quiz_items.json', encoding='utf-8') as f:
    current_items = json.load(f)

existing_en = {it['en'].lower() for it in current_items}
max_id = max(it['id'] for it in current_items)

def sprite_url(en_name):
    slug = en_name.lower().replace(' ', '-').replace("'", '').replace('.', '')
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/{slug}.png"

new_data = [
    {"category":"for-sell","koName":"금구슬","enName":"Nugget","desc":"금색으로 반짝반짝 빛나는 순금으로 만들어진 구슬. 상점에서 비싸게 팔린다."},
    {"category":"for-sell","koName":"별의모래","enName":"Stardust","desc":"감촉이 보슬보슬한 빨갛고 예쁜 모래. 상점에서 비싸게 팔린다."},
    {"category":"for-sell","koName":"별의조각","enName":"Star Piece","desc":"반짝반짝 빨갛게 빛나는 예쁜 보석 조각. 상점에서 비싸게 팔린다."},
    {"category":"for-sell","koName":"작은버섯","enName":"Tiny Mushroom","desc":"작고 진귀한 버섯. 일부 마니아 사이에서는 매우 인기가 높다."},
    {"category":"for-sell","koName":"진주","enName":"Pearl","desc":"예쁜 은색으로 빛나는 자그마한 진주. 상점에서 싸게 팔린다."},
    {"category":"for-sell","koName":"큰버섯","enName":"Big Mushroom","desc":"크고 진귀한 버섯. 일부 마니아 사이에서는 매우 인기가 높다."},
    {"category":"for-sell","koName":"큰진주","enName":"Big Pearl","desc":"예쁜 은색으로 빛나는 상당히 큰 낱알의 진주. 상점에서 비싸게 팔린다."},
    {"category":"for-sell","koName":"귀중한뼈","enName":"Rare Bone","desc":"포켓몬 고고학 상에서 매우 귀중한 뼈. 상점에서 비싸게 팔린다."},
    {"category":"for-sell","koName":"달콤한꿀","enName":"Honey","desc":"풀숲에서 사용하면 야생 포켓몬과 조우할 수 있는 달콤한 꿀."},
    {"category":"for-sell","koName":"고운깃털","enName":"Pretty Feather","desc":"아름답기만 할 뿐 아무 효과도 없는 지극히 평범한 깃털."},
    {"category":"for-sell","koName":"향기버섯","enName":"Balm Mushroom","desc":"주변 일대에 좋은 향기가 퍼지는 희귀한 버섯. 상점에서 비싸게 팔린다."},
    {"category":"for-sell","koName":"혜성조각","enName":"Comet Shard","desc":"혜성이 가까워졌을 때 지표면에 떨어진 조각. 상점에서 비싸게 팔린다."},
    {"category":"for-sell","koName":"큰금구슬","enName":"Big Nugget","desc":"금색으로 반짝반짝 빛나는 순금으로 만들어진 큰 구슬. 상점에서 비싸게 팔린다."},
    {"category":"for-sell","koName":"경단진주","enName":"Pearl String","desc":"예쁜 은색으로 빛나는 매우 큰 낱알의 진주. 상점에서 비싸게 팔린다."},
    {"category":"for-sell","koName":"작은죽순","enName":"Tiny Bamboo Shoot","desc":"작고 진귀한 죽순. 일부 미식가 사이에서는 매우 인기가 높다."},
    {"category":"for-sell","koName":"큰죽순","enName":"Big Bamboo Shoot","desc":"크고 진귀한 죽순. 일부 미식가 사이에서는 매우 인기가 높다."},
    {"category":"evolution","koName":"가라두구팔찌","enName":"Galarica Cuff","desc":"가라두구가지를 엮어서 만든 팔찌. 가라르지방의 야돈에게 채워주면 기뻐한다."},
    {"category":"evolution","koName":"가라두구머리장식","enName":"Galarica Wreath","desc":"가라두구가지를 엮어서 만든 머리 장식. 가라르지방의 야돈에게 씌워주면 기뻐한다."},
    {"category":"evolution","koName":"연결의끈","enName":"Linking Cord","desc":"모종의 유대감이 느껴지는 신비한 에너지가 담긴 끈. 어떤 포켓몬들이 좋아하는 물건이다."},
    {"category":"evolution","koName":"검은휘석","enName":"Black Augurite","desc":"조각내면 예리하게 날이 서는 유리 같은 성질을 띠는 검은 돌. 어떤 포켓몬이 좋아하는 물건이다."},
    {"category":"evolution","koName":"피트블록","enName":"Peat Block","desc":"진흙 같은 석탄 덩어리. 말리면 연료로도 쓸 수 있다. 어떤 포켓몬이 좋아하는 물건이다."},
    {"category":"evolution","koName":"꽃사탕공예","enName":"Flower Sweet","desc":"꽃 모양의 사탕공예. 마빌크에게 지니게 하면 빙빙 돌며 기뻐한다."},
    {"category":"evolution","koName":"네잎사탕공예","enName":"Clover Sweet","desc":"네잎 모양의 사탕공예. 마빌크에게 지니게 하면 빙빙 돌며 기뻐한다."},
    {"category":"evolution","koName":"딸기사탕공예","enName":"Strawberry Sweet","desc":"딸기 모양의 사탕공예. 마빌크에게 지니게 하면 빙빙 돌며 기뻐한다."},
    {"category":"evolution","koName":"리본사탕공예","enName":"Ribbon Sweet","desc":"리본 모양의 사탕공예. 마빌크에게 지니게 하면 빙빙 돌며 기뻐한다."},
    {"category":"evolution","koName":"베리사탕공예","enName":"Berry Sweet","desc":"베리 모양의 사탕공예. 마빌크에게 지니게 하면 빙빙 돌며 기뻐한다."},
    {"category":"evolution","koName":"스타사탕공예","enName":"Star Sweet","desc":"스타 모양의 사탕공예. 마빌크에게 지니게 하면 빙빙 돌며 기뻐한다."},
    {"category":"evolution","koName":"하트사탕공예","enName":"Love Sweet","desc":"하트 모양의 사탕공예. 마빌크에게 지니게 하면 빙빙 돌며 기뻐한다."},
    {"category":"evolution","koName":"깨진포트","enName":"Cracked Pot","desc":"어느 특정 포켓몬을 진화시키는 이상한 포트. 깨졌지만 차는 맛있어진다."},
    {"category":"evolution","koName":"이빠진포트","enName":"Chipped Pot","desc":"어느 특정 포켓몬을 진화시키는 이상한 포트. 이가 빠졌지만 차는 맛있어진다."},
    {"category":"evolution","koName":"악의족자","enName":"Scroll of Darkness","desc":"어느 특정 포켓몬을 진화시키는 이상한 족자. 어두운 기운이 담겨 있다.","imgUrl":""},
    {"category":"evolution","koName":"물의족자","enName":"Scroll of Waters","desc":"어느 특정 포켓몬을 진화시키는 이상한 족자. 물의 기운이 담겨 있다.","imgUrl":""},
    {"category":"evolution","koName":"저주받은갑옷","enName":"Malicious Armor","desc":"어느 특정 포켓몬을 진화시키는 이상한 갑옷. 저주의 감정이 담겨 있다."},
    {"category":"evolution","koName":"축복받은갑옷","enName":"Auspicious Armor","desc":"어느 특정 포켓몬을 진화시키는 이상한 갑옷. 축복의 감정이 담겨 있다."},
    {"category":"evolution","koName":"꿀맛사과","enName":"Syrupy Apple","desc":"어느 특정 포켓몬을 진화시키는 이상한 사과. 엄청나게 꿀맛이다."},
    {"category":"evolution","koName":"범작찻잔","enName":"Unremarkable Teacup","desc":"어느 특정 포켓몬을 진화시키는 이상한 찻잔. 깨졌지만 차는 맛있어진다."},
    {"category":"evolution","koName":"걸작찻잔","enName":"Masterpiece Teacup","desc":"어느 특정 포켓몬을 진화시키는 이상한 찻잔. 이가 빠졌지만 차는 맛있어진다."},
    {"category":"evolution","koName":"복합금속","enName":"Metal Alloy","desc":"어느 특정 포켓몬을 진화시키는 이상한 금속. 여러 겹으로 겹쳐져 있다."},
    {"category":"species-specific","koName":"주춧돌의가면","enName":"Cornerstone Mask","desc":"결정이 장식되어 있는 목각 가면. 오거폰에게 지니게 하면 바위타입을 두르고 싸울 수 있다."},
    {"category":"species-specific","koName":"우물의가면","enName":"Wellspring Mask","desc":"결정이 장식되어 있는 목각 가면. 오거폰에게 지니게 하면 물타입을 두르고 싸울 수 있다."},
    {"category":"species-specific","koName":"화덕의가면","enName":"Hearthflame Mask","desc":"결정이 장식되어 있는 목각 가면. 오거폰에게 지니게 하면 불꽃타입을 두르고 싸울 수 있다."},
    {"category":"species-specific","koName":"큰금강옥","enName":"Adamant Crystal","desc":"눈부시게 빛나는 큰 구슬. 디아루가에게 사용하면 힘이 넘쳐서 모습이 바뀐다."},
    {"category":"species-specific","koName":"큰백옥","enName":"Lustrous Globe","desc":"눈부시게 빛나는 큰 구슬. 펄기아에게 사용하면 힘이 넘쳐서 모습이 바뀐다."},
    {"category":"species-specific","koName":"큰백금옥","enName":"Griseous Core","desc":"눈부시게 빛나는 큰 구슬. 기라티나에게 사용하면 힘이 넘쳐서 모습이 바뀐다."},
    {"category":"species-specific","koName":"녹슨검","enName":"Rusted Sword","desc":"먼 옛날의 영웅이 재앙을 막는 데 사용했다고 전해지는 검이지만 지금은 녹이 슬고 닳아버렸다."},
    {"category":"species-specific","koName":"녹슨방패","enName":"Rusted Shield","desc":"먼 옛날의 영웅이 재앙을 막는 데 사용했다고 전해지는 방패지만 지금은 녹이 슬고 닳아버렸다."},
    {"category":"species-specific","koName":"그라시데아꽃","enName":"Gracidea","desc":"생일이나 기념일 등에 감사의 마음을 전하기 위해 부케로 만들어 보내는 일이 있다."},
    {"category":"species-specific","koName":"비추는거울","enName":"Reveal Glass","desc":"진실을 비춰줌으로 포켓몬을 본래의 모습으로 바꿔버리는 이상한 거울."},
    {"category":"species-specific","koName":"유전자쐐기","enName":"DNA Splicers","desc":"원래는 하나였다고 전해지는 큐레무와 어떤 포켓몬을 합체시키는 한 쌍의 쐐기."},
    {"category":"species-specific","koName":"굴레의항아리","enName":"Prison Bottle","desc":"먼 옛날 어떤 포켓몬의 힘을 봉인했다고 여겨지는 항아리."},
    {"category":"species-specific","koName":"네크로플러스루나","enName":"N-Lunarizer","desc":"빛을 필요로 하는 네크로즈마와 루나아라를 합체시키기 위한 머신."},
    {"category":"species-specific","koName":"네크로플러스솔","enName":"N-Solarizer","desc":"빛을 필요로 하는 네크로즈마와 솔가레오를 합체시키기 위한 머신."},
    {"category":"type-enhancement","koName":"요정의깃털","enName":"Fairy Feather","desc":"빛에 비추면 희미하게 빛나는 깃털. 지니게 하면 페어리타입 기술의 위력이 올라간다."},
    {"category":"fossil","koName":"조개화석","enName":"Helix Fossil","desc":"화석을 복원시키면 암나이트가 나온다."},
    {"category":"fossil","koName":"껍질화석","enName":"Dome Fossil","desc":"화석을 복원시키면 투구가 나온다."},
    {"category":"fossil","koName":"비밀의호박","enName":"Old Amber","desc":"화석을 복원시키면 프테라가 나온다."},
    {"category":"fossil","koName":"뿌리화석","enName":"Root Fossil","desc":"화석을 복원시키면 릴링이 나온다."},
    {"category":"fossil","koName":"발톱화석","enName":"Claw Fossil","desc":"화석을 복원시키면 아노딥스가 나온다."},
    {"category":"fossil","koName":"두개의화석","enName":"Skull Fossil","desc":"화석을 복원시키면 두개도스가 나온다."},
    {"category":"fossil","koName":"방패의화석","enName":"Armor Fossil","desc":"화석을 복원시키면 방패톱스가 나온다."},
    {"category":"fossil","koName":"덮개화석","enName":"Cover Fossil","desc":"화석을 복원시키면 프로토가가 나온다."},
    {"category":"fossil","koName":"깃털화석","enName":"Plume Fossil","desc":"화석을 복원시키면 아켄이 나온다."},
    {"category":"fossil","koName":"턱화석","enName":"Jaw Fossil","desc":"화석을 복원시키면 티고라스가 나온다."},
    {"category":"fossil","koName":"지느러미화석","enName":"Sail Fossil","desc":"화석을 복원시키면 아마루스가 나온다."},
    {"category":"fossil","koName":"화석새","enName":"Fossilized Bird","desc":"오랜 옛날 하늘을 날던 고대 포켓몬 화석의 일부. 어떤 모습이었는지는 수수께끼다."},
    {"category":"fossil","koName":"화석물고기","enName":"Fossilized Fish","desc":"오랜 옛날 바다에 살았던 고대 포켓몬 화석의 일부. 어떤 모습이었는지는 수수께끼다."},
    {"category":"fossil","koName":"화석용","enName":"Fossilized Drake","desc":"오랜 옛날 육지에 살았던 고대 포켓몬 화석의 일부. 어떤 모습이었는지는 수수께끼다."},
    {"category":"fossil","koName":"화석긴목","enName":"Fossilized Dino","desc":"오랜 옛날 바다에 살았던 고대 포켓몬 화석의 일부. 어떤 모습이었는지는 수수께끼다."},
    {"category":"held-items","koName":"탈출팩","enName":"Eject Pack","desc":"지니게 한 포켓몬의 능력이 떨어지면 지닌 포켓몬과 교체한다."},
    {"category":"held-items","koName":"속임수주사위","enName":"Loaded Dice","desc":"좋은 눈만 나오는 주사위. 지니게 하고 연속 기술을 사용하면 많은 횟수로 기술을 사용할 수 있다."},
    {"category":"held-items","koName":"검은오물","enName":"Black Sludge","desc":"지니게 하면 독타입의 포켓몬은 조금씩 HP를 회복한다. 그 이외의 타입은 HP가 줄어 버린다."},
    {"category":"held-items","koName":"흉내허브","enName":"Mirror Herb","desc":"지니게 한 포켓몬은 한 번에 한해 상대의 능력이 올랐을 때 흉내 내어 똑같이 능력을 올린다."},
    {"category":"held-items","koName":"만능우산","enName":"Utility Umbrella","desc":"지니게 한 포켓몬은 비와 햇살이 강할 때의 영향을 받지 않게 된다."},
    {"category":"held-items","koName":"목스프레이","enName":"Throat Spray","desc":"소리 기술을 사용하면 특수공격이 올라간다."},
    {"category":"held-items","koName":"통굽부츠","enName":"Heavy-Duty Boots","desc":"발밑에 설치된 함정 등의 영향을 받지 않게 된다."},
    {"category":"held-items","koName":"허탕보험","enName":"Blunder Policy","desc":"명중률에 의해 기술이 빗나갔을 때 스피드가 크게 올라간다."},
    {"category":"held-items","koName":"룸서비스","enName":"Room Service","desc":"포켓몬에게 지니게 하면 트릭룸일 때 사용하여 스피드가 떨어진다."},
    {"category":"held-items","koName":"펀치글러브","enName":"Punching Glove","desc":"주먹을 보호하는 글러브. 지니게 하면 펀치 기술의 위력이 오르고 상대에게 접촉하지 않는 펀치가 된다."},
    {"category":"held-items","koName":"특성가드","enName":"Ability Shield","desc":"귀엽고 개성적인 방패. 지니게 하면 상대에 의해 특성이 바뀌지 않는다."},
    {"category":"held-items","koName":"클리어참","enName":"Clear Amulet","desc":"투명하고 빛나는 참. 지니게 하면 상대의 기술이나 특성으로 능력이 떨어지지 않는다."},
    {"category":"held-items","koName":"은밀망토","enName":"Covert Cloak","desc":"상대의 눈을 속이는 후드 달린 망토. 지니게 하면 몸을 숨겨서 기술의 추가 효과를 받지 않게 된다."},
    {"category":"held-items","koName":"부스트에너지","enName":"Booster Energy","desc":"에너지가 가득한 캡슐. 어떤 특성을 가진 포켓몬에게 지니게 하면 그 힘을 증폭시킨다."},
]

added = []
skipped = []

for item in new_data:
    en_lower = item['enName'].lower()
    if en_lower in existing_en:
        skipped.append(item['koName'])
        continue
    max_id += 1
    # 악의족자, 물의족자는 imgUrl 없음 → 빈 스프라이트
    no_sprite = item.get('imgUrl', None) == ''
    sp = '' if no_sprite else sprite_url(item['enName'])
    new_item = {
        "id": max_id,
        "ko": item['koName'],
        "en": en_lower,
        "desc": item['desc'],
        "desc_lang": "ko",
        "sprite": sp,
        "category": item['category']
    }
    current_items.append(new_item)
    existing_en.add(en_lower)
    added.append(new_item)

with open('data/quiz_items.json', 'w', encoding='utf-8') as f:
    json.dump(current_items, f, ensure_ascii=False, indent=2)

print(f"\n✅ 추가: {len(added)}개")
for it in added:
    print(f"  [{it['category']}] {it['ko']} / {it['en']} (id:{it['id']})")

print(f"\n⏭ 중복 스킵: {len(skipped)}개")
for name in skipped:
    print(f"  {name}")
