"""
learnsets.json 의 빈 항목 채우기 (PokeAPI)

왜 비어 있었나
  build_learnsets.py 는 포켓몬 키를 그대로 PokeAPI 슬러그로 썼다. 그런데 PokeAPI 는
  "대표 폼"에 접미사를 붙여 부른다 — 시비꼬는 `squawkabilly` 가 아니라
  `squawkabilly-green-plumage`, 불비달마는 `darmanitan-standard` 다. 404 가 나면
  옛 스크립트는 조용히 빈 배열을 넣고 넘어갔다. 그래서 배틀팀 빌더·기술 도감에서
  그 포켓몬만 기술이 하나도 안 뜬다.

두 갈래로 채운다
  1) SLUG_FIX     — PokeAPI 이름이 다른 것. 다시 받아온다 (시비꼬·불비달마·펌킨인 등)
  2) INHERIT_BASE — 계절 폼처럼 겉모습만 다르거나, 메가·거다이맥스라 기술을 원종과
                    공유하는 것. learnsets.json 안의 원종을 그대로 물려받는다.
                    API 를 다시 부르지 않는 이유는 파일과 어긋나지 않기 위해서다 —
                    버미루를 다시 받으면 7개가 1개로 줄어든다(버전 선택이 달라진다).

실행: python3 scripts/fill_missing_learnsets.py [--check]
      --check 를 주면 저장하지 않고 무엇이 채워질지만 보여준다
"""
import json, sys, time, urllib.request, urllib.error, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEARNSETS = ROOT / "data" / "learnsets.json"
QUIZ_MOVES = ROOT / "data" / "quiz_moves.json"

# 1) PokeAPI 슬러그가 다른 것
SLUG_FIX = {
    "darmanitan": "darmanitan-standard",
    "dudunsparce": "dudunsparce-two-segment",
    "eiscue": "eiscue-ice",
    "farfetchd": "farfetchd",
    "flabébé": "flabebe",
    "meowstic_mega": "meowstic-male-mega",
    "minior": "minior-red-meteor",
    "mr_mime": "mr-mime",
    "necrozma_dawn_wings": "necrozma-dawn",
    "necrozma_dusk_mane": "necrozma-dusk",
    "pumpkaboo": "pumpkaboo-average",
    "pyroar_mega": "pyroar-mega",
    "squawkabilly": "squawkabilly-green-plumage",
}

# 2) 원종에서 그대로 물려받는 것 (겉모습 폼 + 기술이 0개로 오는 메가·거다이맥스)
INHERIT_BASE = {
    "burmy_sandy": "burmy",
    "burmy_trash": "burmy",
    "deerling_autumn": "deerling",
    "deerling_summer": "deerling",
    "deerling_winter": "deerling",
    "sawsbuck_autumn": "sawsbuck",
    "sawsbuck_summer": "sawsbuck",
    "sawsbuck_winter": "sawsbuck",
    "tatsugiri_stretchy_mega": "tatsugiri_stretchy",
    "toxtricity_amped_gmax": "toxtricity",
    "urshifu_rapid_strike_gmax": "urshifu_rapid_strike",
    "urshifu_single_strike_gmax": "urshifu",
    "zygarde_mega": "zygarde",
}

# SV 를 최우선으로, 없으면 최신 버전 순 (build_learnsets.py 와 같은 순서)
VERSION_PRIORITY = [
    "scarlet-violet", "the-teal-mask", "the-indigo-disk",
    "sword-shield", "the-isle-of-armor", "the-crown-tundra",
    "brilliant-diamond-shining-pearl", "legends-arceus",
    "ultra-sun-ultra-moon", "sun-moon",
    "omega-ruby-alpha-sapphire", "x-y",
    "black-2-white-2", "black-white",
    "heartgold-soulsilver", "platinum", "diamond-pearl",
    "firered-leafgreen", "emerald", "ruby-sapphire",
    "crystal", "gold-silver", "yellow", "red-blue",
    # 포켓몬 챔피언스. 본가 데이터가 있으면 그쪽을 쓰고, 챔피언스에만 있는
    # 메가폼(냐오닉스·화염레오)일 때만 여기까지 내려온다.
    "champions",
]

METHOD_ORDER = {"level-up": 0, "machine": 1, "egg": 2, "tutor": 3}


def fetch(slug):
    url = f"https://pokeapi.co/api/v2/pokemon/{urllib.parse.quote(slug)}/"
    req = urllib.request.Request(url, headers={"User-Agent": "pokenova-builder/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def learnset_from_api(slug):
    """PokeAPI 응답에서 가장 최신 버전 기준 기술 목록을 뽑는다."""
    data = fetch(slug)
    raw = data.get("moves", [])
    groups = {vgd["version_group"]["name"] for m in raw for vgd in m["version_group_details"]}
    best = next((vg for vg in VERSION_PRIORITY if vg in groups), None)
    if not best:
        return []
    out, seen = [], set()
    for m in raw:
        name = m["move"]["name"].replace("-", "_")
        if name in seen:
            continue
        vgd = next((v for v in m["version_group_details"]
                    if v["version_group"]["name"] == best), None)
        if not vgd:
            continue
        seen.add(name)
        out.append({
            "en": name,
            "method": vgd["move_learn_method"]["name"],
            "level": vgd["level_learned_at"],
        })
    return out


def tidy(moves, known):
    """quiz_moves.json 에 있는 기술만 남기고, 습득 방법·레벨 순으로 정렬한다."""
    kept = [m for m in moves if m["en"] in known]
    kept.sort(key=lambda m: (METHOD_ORDER.get(m["method"], 9), m["level"]))
    seen, out = set(), []
    for m in kept:
        if m["en"] not in seen:
            seen.add(m["en"])
            out.append(m)
    return out


def main():
    check_only = "--check" in sys.argv
    learnsets = json.loads(LEARNSETS.read_text(encoding="utf-8"))
    known = {m["en"] for m in json.loads(QUIZ_MOVES.read_text(encoding="utf-8"))}

    empty = [k for k, v in learnsets.items() if not v]
    print(f"빈 항목 {len(empty)}개: {', '.join(empty)}\n")

    filled, unhandled = {}, []
    cache = {}

    for key in empty:
        slug = SLUG_FIX.get(key)
        if slug:
            if slug not in cache:
                try:
                    cache[slug] = learnset_from_api(slug)
                except urllib.error.HTTPError as e:
                    print(f"  {key:28s} <- {slug:28s} HTTP {e.code}")
                    unhandled.append(key)
                    continue
                time.sleep(0.08)
            moves = tidy(cache[slug], known)
        elif key in INHERIT_BASE:
            base = INHERIT_BASE[key]
            slug = f"(원종 {base})"
            moves = list(learnsets.get(base, []))
        else:
            unhandled.append(key)
            continue

        if not moves:
            print(f"  {key:28s} <- {slug:28s} 0개 — 건너뜀")
            unhandled.append(key)
            continue
        filled[key] = moves
        print(f"  {key:28s} <- {slug:28s} {len(moves)}개")

    print(f"\n채운 항목 {len(filled)}개 / 남은 빈 항목 {len(unhandled)}개")
    if unhandled:
        print(f"  남음: {', '.join(unhandled)}")

    if check_only:
        print("\n--check 라 저장하지 않았다")
        return

    # 키 순서는 건드리지 않는다. 원본은 알파벳순이 아니라서 다시 정렬하면
    # 내용이 그대로인데도 파일 전체가 바뀐 것처럼 보인다.
    learnsets.update(filled)
    LEARNSETS.write_text(
        json.dumps(learnsets, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n저장 완료: {LEARNSETS}")


if __name__ == "__main__":
    main()
