# -*- coding: utf-8 -*-
"""
Sobe campanha Clarilux/melasma na conta EUA 11 (act_2164352101016970).
1 campanha CBO + 1 conjunto + 10 ads single-image (as 10 imagens de melasma).
Cada ad: imagem + texto curto próprio + link pro advertorial do ângulo.
Tudo PAUSED. Pixel SANO-Clarilux 2873393396348834. Compliance BR.

Uso: META_TOKEN=... python subir-clarilux-melasma.py test|all
"""
import urllib.request, urllib.parse, json, os, sys, time
from pathlib import Path

TOKEN = os.environ["META_TOKEN"]
ACT = "act_2164352101016970"; PAGE = "759591800579421"; IG = "17841477315620430"
PIXEL = "2873393396348834"; BASE = "https://graph.facebook.com/v23.0/"
BENE = "880756411607509"
HERE = Path(__file__).parent
IMGDIR = HERE.parent / "clarilux" / "images" / "melasma-novas" / "jpg"
MANIFEST = json.load(open(HERE / "manifesto-clarilux-melasma.json", encoding="utf-8"))
OUT = HERE / "manifestos-prime" / "clarilux-melasma-resultado.jsonl"
OUT.parent.mkdir(exist_ok=True)

def post(path, data):
    d = dict(data); d["access_token"] = TOKEN
    req = urllib.request.Request(BASE + path, data=urllib.parse.urlencode(d).encode(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        return None, e.read().decode()[:400]

def upload_image(path):
    """Upload de imagem via multipart -> image_hash."""
    import mimetypes, uuid
    boundary = uuid.uuid4().hex
    fname = os.path.basename(path)
    with open(path, "rb") as f: content = f.read()
    body = []
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"access_token\"\r\n\r\n{TOKEN}\r\n".encode())
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"filename\"; filename=\"{fname}\"\r\nContent-Type: image/jpeg\r\n\r\n".encode())
    body.append(content)
    body.append(f"\r\n--{boundary}--\r\n".encode())
    data = b"".join(body)
    req = urllib.request.Request(BASE + f"{ACT}/adimages", data=data, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            j = json.load(r)
            # retorna {images: {fname: {hash: ...}}}
            imgs = j.get("images", {})
            for k, v in imgs.items():
                return v["hash"], None
            return None, "sem hash: " + json.dumps(j)[:200]
    except urllib.error.HTTPError as e:
        return None, e.read().decode()[:400]

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    log = open(OUT, "a", encoding="utf-8")
    def rec(**kw): log.write(json.dumps(kw, ensure_ascii=False) + "\n"); log.flush()

    # modo reuse: só sobe os ads restantes num adset já existente
    RC = os.environ.get("REUSE_CID"); RA = os.environ.get("REUSE_ASID")
    START = int(os.environ.get("START_AD", "1"))
    if RC and RA:
        cid, asid = RC, RA
        print(f"[reuse] campanha {cid}, adset {asid}, a partir do ad {START}")
        subir_ads(cid, asid, mode, rec, start=START); return

    # 1) Campanha CBO
    camp, err = post(f"{ACT}/campaigns", {
        "name": "CLARILUX | MELASMA | 10ADS",
        "objective": MANIFEST["campanha"]["objective"],
        "buying_type": "AUCTION",
        "special_ad_categories": json.dumps([]),
        "bid_strategy": MANIFEST["campanha"]["bid_strategy"],
        "daily_budget": str(MANIFEST["campanha"]["daily_budget"]),
        "status": "PAUSED",
    })
    if err: print("[ERRO campanha]", err); rec(step="campaign", ok=False, error=err); return
    cid = camp["id"]; print(f"[OK] campanha {cid}"); rec(step="campaign", ok=True, id=cid)

    # 2) AdSet (1 conjunto)
    aset, err = post(f"{ACT}/adsets", {
        "name": "CLARILUX | MELASMA | Conj1 (BR mulheres 30-65)",
        "campaign_id": cid, "status": "PAUSED",
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "OFFSITE_CONVERSIONS",
        "bid_amount": str(MANIFEST["campanha"]["bid_amount"]),
        "promoted_object": json.dumps({"pixel_id": PIXEL, "custom_event_type": "PURCHASE"}),
        "regional_regulated_categories": json.dumps(MANIFEST["compliance"]["regional_regulated_categories"]),
        "regional_regulation_identities": json.dumps(MANIFEST["compliance"]["regional_regulation_identities"]),
        "targeting": json.dumps({
            "geo_locations": {"countries": ["BR"]},
            "age_min": 30, "age_max": 65, "genders": [2],
            "targeting_automation": {"advantage_audience": 0}}),
    })
    if err: print("[ERRO adset]", err); rec(step="adset", ok=False, error=err); return
    asid = aset["id"]; print(f"[OK] adset {asid}"); rec(step="adset", ok=True, id=asid)
    subir_ads(cid, asid, mode, rec, start=1)

def subir_ads(cid, asid, mode, rec, start=1):
    # 3) ads
    ads = MANIFEST["ads"][:1] if mode == "test" else MANIFEST["ads"]
    img_cache = {}
    for i, ad in enumerate(ads, 1):
        if i < start: continue
        imgpath = IMGDIR / ad["img"].replace(".webp", ".jpg")
        if not imgpath.exists():
            print(f"[skip] {ad['img']} não existe"); continue
        h = img_cache.get(ad["img"])
        if not h:
            h, e = upload_image(str(imgpath))
            if e: print(f"[ERRO img {ad['img']}]", e); rec(step="img", img=ad["img"], ok=False, error=e); continue
            img_cache[ad["img"]] = h
        oss = {"page_id": PAGE, "instagram_user_id": IG,
               "link_data": {"link": ad["adv"], "message": ad["primary_text"], "image_hash": h,
                             "call_to_action": {"type": "LEARN_MORE", "value": {"link": ad["adv"]}}}}
        dof = {"creative_features_spec": {"site_extensions": {"enroll_status": "OPT_OUT"}}}
        cr, e = post(f"{ACT}/adcreatives", {
            "name": f"CR_melasma_{i:02d}_{ad['img'][:20]}",
            "object_story_spec": json.dumps(oss),
            "degrees_of_freedom_spec": json.dumps(dof)})
        if e: print(f"[ERRO creative {i}]", e); rec(step="creative", n=i, ok=False, error=e); continue
        adr, e2 = post(f"{ACT}/ads", {
            "name": f"MELASMA_{i:02d}_{ad['angulo'][:25]}",
            "adset_id": asid, "creative": json.dumps({"creative_id": cr["id"]}), "status": "PAUSED"})
        if e2: print(f"[ERRO ad {i}]", e2); rec(step="ad", n=i, ok=False, error=e2); continue
        print(f"[OK] ad {i:02d} -> {adr['id']} ({ad['img']})"); rec(step="ad", n=i, ok=True, id=adr["id"], img=ad["img"])
        time.sleep(1)
    print(f"\n=== FEITO. campanha {cid}, adset {asid} ===")

if __name__ == "__main__":
    main()
