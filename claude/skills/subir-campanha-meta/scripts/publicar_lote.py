#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publisher generico Meta Ads (Graph API v23.0) — estrutura 1-1-1.

    python3 publicar_lote.py <manifesto.json>          sobe o lote
    python3 publicar_lote.py <manifesto.json> --dry     valida e mostra o plano

Toda a config (conta, pixel, page, advertiser, copy, link, midia) vem do
manifesto, entao o mesmo script serve pra qualquer produto e qualquer conta.

Idempotente por NOME DE CAMPANHA: lista o que ja existe antes de comecar e pula.
Rodar de novo depois de uma falha continua de onde parou.

Token: variavel de ambiente META_ACCESS_TOKEN, ou um token.txt ao lado deste
arquivo. Nunca hardcodar, nunca commitar.

Trilha de video (upload -> ready -> thumb -> video_data) roda em producao desde
2026-09. Trilha de imagem (adimages -> link_data) segue o formato validado em
2026-05; se for o primeiro lote de imagem numa conta, rode 1 anuncio antes do
lote inteiro.
"""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
API = "https://graph.facebook.com/v23.0"


def carregar_token():
    tok = os.environ.get("META_ACCESS_TOKEN", "").strip()
    if tok:
        return tok
    caminho = os.path.join(AQUI, "token.txt")
    if os.path.isfile(caminho):
        tok = open(caminho).read().strip()
        if tok:
            return tok
    sys.exit(
        "ERRO: token ausente.\n"
        "  export META_ACCESS_TOKEN='...'   ou   crie token.txt ao lado do script.\n"
        "  Gere no Graph API Explorer com permissao ads_management."
    )


TOKEN = carregar_token()


# --------------------------------------------------------------- HTTP
def call(path, params=None, method="GET"):
    """GET/POST com retry exponencial em rate limit (code 17 / subcode 2446079)."""
    params = dict(params or {})
    params["access_token"] = TOKEN
    for tentativa in range(4):
        try:
            if method == "GET":
                req = urllib.request.Request(f"{API}/{path}?" + urllib.parse.urlencode(params))
            else:
                req = urllib.request.Request(
                    f"{API}/{path}", data=urllib.parse.urlencode(params).encode("utf-8")
                )
            return json.load(urllib.request.urlopen(req, timeout=180))
        except urllib.error.HTTPError as e:
            corpo = e.read().decode("utf-8", "replace")
            try:
                err = json.loads(corpo)["error"]
            except Exception:
                raise RuntimeError(f"{path}: {corpo[:500]}")
            if err.get("code") == 17 or err.get("error_subcode") == 2446079:
                espera = 60 * (tentativa + 1)
                print(f"   rate limit — aguardando {espera}s")
                time.sleep(espera)
                continue
            raise RuntimeError(f"{path}: {json.dumps(err, ensure_ascii=False)[:600]}")
    raise RuntimeError(f"{path}: rate limit persistente")


# --------------------------------------------------------------- midia
def upload_video(act, caminho):
    """Upload simples. Acima de ~90MB o Meta devolve HTTP 413 em 0,2s (nao e timeout)."""
    mb = os.path.getsize(caminho) / 1e6
    if mb > 90:
        raise RuntimeError(f"{os.path.basename(caminho)} tem {mb:.0f}MB — precisa de upload em partes")
    saida = subprocess.run(
        ["curl", "-s", "-X", "POST", f"{API}/{act}/advideos",
         "-F", f"source=@{caminho}", "-F", f"access_token={TOKEN}",
         "-w", "\nHTTP_CODE=%{http_code}"],
        capture_output=True, text=True, timeout=1200).stdout
    payload, _, code = saida.rpartition("\nHTTP_CODE=")
    if code.strip() != "200":
        raise RuntimeError(f"upload {os.path.basename(caminho)} HTTP {code.strip()}: {payload[:400]}")
    d = json.loads(payload)
    if "error" in d:
        raise RuntimeError(f"upload {os.path.basename(caminho)}: {d['error']}")
    return d["id"]


def esperar_ready(video_id, timeout=1800):
    """Video de 34MB ja levou >15min. Timeout padrao de 30min, nao 15."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        st = call(video_id, {"fields": "status"}).get("status", {})
        if st.get("video_status") == "ready":
            return
        if st.get("video_status") == "error":
            raise RuntimeError(f"video {video_id} falhou: {st}")
        time.sleep(10)
    raise RuntimeError(f"video {video_id} nao ficou ready em {timeout}s")


def pegar_thumb(video_id):
    """Miniatura e obrigatoria no video_data — sem ela, subcode 1443226."""
    thumbs = call(f"{video_id}/thumbnails", {"fields": "uri,is_preferred"}).get("data", [])
    if not thumbs:
        raise RuntimeError(f"video {video_id} sem thumbnails")
    return next((t["uri"] for t in thumbs if t.get("is_preferred")), thumbs[0]["uri"])


def upload_imagem(act, caminho):
    """O nome do campo multipart tem que ser o NOME DO ARQUIVO.
    Usar 'bytes=@...' devolve Invalid parameter com file_size: 8."""
    nome = os.path.basename(caminho)
    saida = subprocess.run(
        ["curl", "-s", "-X", "POST", f"{API}/{act}/adimages",
         "-F", f"{nome}=@{caminho}", "-F", f"access_token={TOKEN}",
         "-w", "\nHTTP_CODE=%{http_code}"],
        capture_output=True, text=True, timeout=600).stdout
    payload, _, code = saida.rpartition("\nHTTP_CODE=")
    if code.strip() != "200":
        raise RuntimeError(f"upload {nome} HTTP {code.strip()}: {payload[:400]}")
    d = json.loads(payload)
    if "error" in d:
        raise RuntimeError(f"upload {nome}: {d['error']}")
    return next(iter(d["images"].values()))["hash"]


# --------------------------------------------------------------- conta
def campanhas_existentes(act):
    nomes = {}
    url = f"{API}/{act}/campaigns?" + urllib.parse.urlencode(
        {"fields": "id,name", "limit": "200", "access_token": TOKEN})
    while url:
        d = json.load(urllib.request.urlopen(url))
        for c in d.get("data", []):
            nomes[c["name"]] = c["id"]
        url = d.get("paging", {}).get("next")
    return nomes


# --------------------------------------------------------------- validacao
def validar(m):
    """Pega no seco os erros que so apareceriam no meio do run."""
    problemas = []

    for campo in ("account_id", "campanha", "adset", "creative", "ads"):
        if campo not in m:
            problemas.append(f"falta a chave '{campo}' no manifesto")
    if problemas:
        return problemas

    if not str(m["account_id"]).startswith("act_"):
        problemas.append("account_id precisa do prefixo 'act_'")

    a, c = m["adset"], m["creative"]
    for campo in ("pixel_id", "advertiser_id", "targeting"):
        if not a.get(campo):
            problemas.append(f"adset.{campo} vazio")
    for campo in ("page_id", "link", "message"):
        if not c.get(campo):
            problemas.append(f"creative.{campo} vazio")

    dof = c.get("degrees_of_freedom_spec") or {}
    feats = dof.get("creative_features_spec") or {}
    if not feats:
        problemas.append(
            "creative.degrees_of_freedom_spec ausente — sem ele a Meta liga os "
            "aprimoramentos automaticos, inclusive o 'Ligar agora' que vaza clique")
    else:
        if "standard_enhancements" in feats:
            problemas.append(
                "creative_features_spec tem 'standard_enhancements' — DESCONTINUADO, "
                "quebra o POST com subcode 3858504. Remover so esse campo.")
        se = feats.get("site_extensions", {}).get("enroll_status")
        if se != "OPT_OUT":
            problemas.append(f"site_extensions esta '{se}', tem que ser OPT_OUT")

    alvo = a.get("targeting") or {}
    aa = (alvo.get("targeting_automation") or {}).get("advantage_audience")
    if aa is None:
        problemas.append(
            "targeting.targeting_automation.advantage_audience nao declarado — subcode 1870227")
    if aa == 1 and alvo.get("age_min", 0) > 25:
        problemas.append(
            f"advantage_audience=1 com age_min={alvo.get('age_min')} — o maximo e 25 (subcode 1870188)")

    vistos = set()
    for i, item in enumerate(m["ads"]):
        if not item.get("campaign_name"):
            problemas.append(f"ads[{i}] sem campaign_name")
            continue
        nome = item["campaign_name"]
        if nome in vistos:
            problemas.append(f"campaign_name duplicado no manifesto: '{nome}'")
        vistos.add(nome)
        caminho = item.get("video_path") or item.get("image_path")
        if not caminho and not item.get("video_id") and not item.get("image_hash"):
            problemas.append(f"'{nome}' sem video_path, image_path, video_id ou image_hash")
        elif caminho and not os.path.isfile(caminho):
            problemas.append(f"'{nome}': arquivo nao existe — {caminho}")

    return problemas


# --------------------------------------------------------------- main
def main():
    if len(sys.argv) < 2:
        sys.exit("uso: publicar_lote.py <manifesto.json> [--dry]")
    manifesto_path = sys.argv[1]
    dry = "--dry" in sys.argv

    m = json.load(open(manifesto_path, encoding="utf-8"))
    problemas = validar(m)
    if problemas:
        print("MANIFESTO INVALIDO:")
        for p in problemas:
            print(f"  - {p}")
        sys.exit(1)

    act = m["account_id"]
    camp_cfg, adset_cfg, cre = m["campanha"], m["adset"], m["creative"]
    result_path = os.path.join(
        os.path.dirname(os.path.abspath(manifesto_path)),
        os.path.basename(manifesto_path).replace(".json", "") + ".resultado.json")

    conta = call(act, {"fields": "name,account_status,currency"})
    print(f"conta {conta.get('name')} ({act}) · status {conta.get('account_status')} "
          f"· {conta.get('currency')}")
    if conta.get("account_status") != 1:
        print("  AVISO: account_status != 1, a conta pode estar restrita")

    ja = campanhas_existentes(act)
    novos = [i for i in m["ads"] if i["campaign_name"] not in ja]
    print(f"manifesto com {len(m['ads'])} anuncios · {len(m['ads']) - len(novos)} ja no ar "
          f"· {len(novos)} a criar")

    if dry:
        print("\n[dry] manifesto valido. Seria criado:")
        for i in novos:
            midia = i.get("video_path") or i.get("image_path") or i.get("video_id") or i.get("image_hash")
            print(f"  {i['campaign_name']}  <- {os.path.basename(str(midia))}")
        print(f"\n[dry] campanha {camp_cfg['status']} · "
              f"{camp_cfg['daily_budget_cents']} centavos/dia · {camp_cfg['bid_strategy']}")
        print("[dry] rode sem --dry pra aplicar.")
        return

    resultados = []
    for item in m["ads"]:
        nome = item["campaign_name"]
        print(f"\n=== {nome} ===")
        if nome in ja:
            print(f"   JA EXISTE ({ja[nome]}) — pulando")
            resultados.append({**item, "skipped": True, "campaign_id": ja[nome]})
            continue

        # ---------- midia
        video_id = item.get("video_id")
        image_hash = item.get("image_hash")
        thumb = None
        eh_video = bool(video_id or item.get("video_path"))

        if eh_video:
            if video_id:
                print(f"   1/6 reusando video ja no Meta: {video_id}")
            else:
                print("   1/6 upload do video...")
                video_id = upload_video(act, item["video_path"])
                print(f"       video_id={video_id}")
            print("   2/6 aguardando processamento...")
            esperar_ready(video_id)
            thumb = pegar_thumb(video_id)
        else:
            if image_hash:
                print(f"   1/6 reusando imagem ja no Meta: {image_hash}")
            else:
                print("   1/6 upload da imagem...")
                image_hash = upload_imagem(act, item["image_path"])
                print(f"       image_hash={image_hash}")
            print("   2/6 imagem nao precisa de processamento")

        # ---------- campanha
        print("   3/6 campanha...")
        params_camp = {
            "name": nome,
            "objective": camp_cfg["objective"],
            "buying_type": camp_cfg["buying_type"],
            "bid_strategy": camp_cfg["bid_strategy"],
            "daily_budget": str(camp_cfg["daily_budget_cents"]),
            "special_ad_categories": json.dumps([]),
            "is_adset_budget_sharing_enabled": "false",
            "status": camp_cfg["status"],
        }
        camp = call(f"{act}/campaigns", params_camp, "POST")

        # ---------- conjunto
        print("   4/6 conjunto...")
        params_adset = {
            "name": nome,
            "campaign_id": camp["id"],
            "optimization_goal": adset_cfg["optimization_goal"],
            "billing_event": adset_cfg["billing_event"],
            "destination_type": "UNDEFINED",
            "promoted_object": json.dumps({
                "pixel_id": adset_cfg["pixel_id"],
                "custom_event_type": adset_cfg["custom_event_type"]}),
            "targeting": json.dumps(adset_cfg["targeting"]),
            "attribution_spec": json.dumps(adset_cfg["attribution_spec"]),
            # sem estes 2 campos nenhum conjunto BR e criado (subcode 3858634)
            "regional_regulated_categories": json.dumps(
                ["BRAZIL_REGULATION", "VOLUNTARY_VERIFICATION"]),
            "regional_regulation_identities": json.dumps({
                "universal_beneficiary": adset_cfg["advertiser_id"],
                "universal_payer": adset_cfg["advertiser_id"]}),
            "status": adset_cfg["status"],
        }
        if adset_cfg.get("bid_amount"):  # so em campanha com bid cap
            params_adset["bid_amount"] = str(adset_cfg["bid_amount"])
        adset = call(f"{act}/adsets", params_adset, "POST")

        # ---------- criativo
        print("   5/6 criativo...")
        oss = {"page_id": cre["page_id"]}
        if cre.get("instagram_user_id"):
            oss["instagram_user_id"] = cre["instagram_user_id"]
        if eh_video:
            oss["video_data"] = {
                "video_id": video_id,
                "title": cre["title"],
                "message": cre["message"],
                "image_url": thumb,
                "call_to_action": {"type": cre["cta_type"], "value": {"link": cre["link"]}},
            }
        else:
            oss["link_data"] = {
                "link": cre["link"],
                "message": cre["message"],
                "name": cre["title"],
                "image_hash": image_hash,
                "call_to_action": {"type": cre["cta_type"], "value": {"link": cre["link"]}},
            }
            if cre.get("description"):
                oss["link_data"]["description"] = cre["description"]

        creative = call(f"{act}/adcreatives", {
            "name": nome,
            "object_story_spec": json.dumps(oss, ensure_ascii=False),
            "url_tags": cre["url_tags"],
            "degrees_of_freedom_spec": json.dumps(cre["degrees_of_freedom_spec"]),
        }, "POST")

        # ---------- anuncio
        print("   6/6 anuncio...")
        ad = call(f"{act}/ads", {
            "name": nome,
            "adset_id": adset["id"],
            "creative": json.dumps({"creative_id": creative["id"]}),
            "status": m.get("ad_status", "ACTIVE"),
        }, "POST")

        resultados.append({**item, "video_id": video_id, "image_hash": image_hash,
                           "thumb_url": thumb, "campaign_id": camp["id"],
                           "adset_id": adset["id"], "creative_id": creative["id"],
                           "ad_id": ad["id"], "skipped": False})
        print(f"   OK — camp {camp['id']} / adset {adset['id']} / ad {ad['id']}")
        # grava a cada item: se o run morrer, o video_id nao se perde
        json.dump(resultados, open(result_path, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)

    m["resultado"] = resultados
    json.dump(m, open(manifesto_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    criadas = sum(1 for r in resultados if not r.get("skipped"))
    print(f"\nFIM — {criadas} campanhas novas")
    print(f"resultado: {result_path}")
    if criadas:
        print("Campanhas nascem PAUSED. Conferir no gerenciador antes de ligar.")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        msg = str(e)
        print(f"\nFALHOU: {msg}")
        if '"code": 190' in msg or "code': 190" in msg:
            print("  Token expirado ou invalido. Gere outro no Graph API Explorer")
            print("  com permissao ads_management e reexporte META_ACCESS_TOKEN.")
        elif "3858634" in msg:
            print("  Anunciante ausente. Confira adset.advertiser_id — tem que vir de um")
            print("  conjunto que ja esta no ar NESTA conta. Secao 3 da referencia.")
        elif "3858504" in msg:
            print("  Tire 'standard_enhancements' do degrees_of_freedom_spec. Secao 4.")
        elif "1870188" in msg:
            print("  Com advantage_audience=1 o age_min nao pode passar de 25.")
        else:
            print("  Procure o codigo/subcode na secao 5 de REFERENCIA-API-META.md")
        print("  O que ja subiu esta no .resultado.json — rodar de novo continua de la.")
        sys.exit(1)
