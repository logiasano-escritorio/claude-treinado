#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copia campanha(s) inteira(s) entre contas do Meta (Graph API v23.0): campanha
(orcamento + bid_strategy), todos os conjuntos (targeting, promoted_object,
optimization_goal, billing_event, attribution_spec, bid_amount, status) e os
anuncios por POST EXISTENTE (object_story_id + url_tags), com o mesmo status.

Baseado na logica validada em producao em copiar_campanha_completa.py e
mover_1642_para_2164.py (~/Sano/scripts/meta). Generalizado aqui: CLI em vez
de env var fixa, --pagador-regulacao em vez de advertiser_id hardcoded.

    python3 copiar_campanhas.py --origem <campaign_id> [<campaign_id> ...] \
        --destino act_X --estado estado.json [--pausar-original] \
        [--pagador-regulacao <advertiser_id>] [--dry]

    python3 copiar_campanhas.py --origem-arquivo ids.json --destino act_X \
        --estado estado.json

`ids.json` aceita lista de strings ou lista de dicts com a chave "id" (formato
dos rankings de criativo, ex. top-N por ROAS).

Retomada pelo arquivo de estado: cada campanha/conjunto/anuncio criado e
gravado na hora, re-rodar nao duplica.

Token: variavel de ambiente META_ACCESS_TOKEN. Nunca hardcodar, nunca commitar.
"""
import argparse
import collections
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v23.0"

# codigos transientes que valem retry com backoff (rate limit, erro interno,
# timeout de banco, etc. — validado em produção)
CODIGOS_TRANSIENTES = {1, 2, 4, 17, 32, 613, 80004}

CAMPOS_ADSET = (
    "id,name,status,bid_amount,daily_budget,lifetime_budget,targeting,"
    "promoted_object,optimization_goal,billing_event,destination_type,"
    "regional_regulated_categories,regional_regulation_identities,attribution_spec"
)
CAMPOS_AD = "id,name,status,creative{effective_object_story_id,url_tags}"

TAGS_PADRAO = (
    "utm_source=facebook&utm_campaign={{campaign.name}}|{{campaign.id}}"
    "&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}"
    "&utm_term={{placement}}"
)

# erros conhecidos que NAO devem derrubar o lote inteiro — loga e segue
ERRO_SEM_PERMISSAO_PAGINA = 1885499
ERRO_CONTA_NAO_QUALIFICADA_SUBCODE = 4841021
ERRO_LIMITE_CONJUNTOS_CBO = 1885940


def carregar_token():
    tok = os.environ.get("META_ACCESS_TOKEN", "").strip()
    if tok:
        return tok
    sys.exit("ERRO: defina META_ACCESS_TOKEN no ambiente (export ou ~/Sano/.env.meta).")


TOKEN = carregar_token()


def call(method, path_ou_url, params=None, tentativas=10):
    """GET/POST com retry exponencial nos codigos transientes validados."""
    params = dict(params or {})
    params["access_token"] = TOKEN
    url = path_ou_url if path_ou_url.startswith("http") else f"{API}/{path_ou_url}"
    for tentativa in range(tentativas):
        try:
            if method == "GET":
                full = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
                req = urllib.request.Request(full)
            else:
                req = urllib.request.Request(url, data=urllib.parse.urlencode(params).encode("utf-8"))
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            corpo = e.read().decode("utf-8", "replace")
            try:
                d = json.loads(corpo)
            except Exception:
                time.sleep(20)
                continue
            err = d.get("error", {})
            if err.get("code") in CODIGOS_TRANSIENTES or err.get("is_transient"):
                espera = 30 * (tentativa + 1)
                print(f"   transiente ({err.get('code')}) — aguardando {espera}s")
                time.sleep(espera)
                continue
            return d
        except Exception:
            time.sleep(20)
    return {"error": {"message": "retry esgotado", "code": -1}}


def paginar(url, params):
    out = []
    while url:
        d = call("GET", url, params)
        if "error" in d:
            print(f"   ERRO paginando {url}: {d['error'].get('message')}")
            break
        out += d.get("data", [])
        url = (d.get("paging") or {}).get("next")
        params = None
    return out


def msg_erro(d):
    e = d.get("error", {})
    return e.get("error_user_msg") or e.get("message") or str(e)


def classificar_erro(d, relatorio):
    """Registra erros conhecidos no relatorio; devolve True se e um erro que
    deve so ser logado e seguir (nao abortar o item)."""
    e = d.get("error", {})
    if e.get("code") == ERRO_SEM_PERMISSAO_PAGINA:
        relatorio["paginas_sem_permissao"].add(e.get("error_user_msg") or e.get("message", ""))
        return True
    if e.get("error_subcode") == ERRO_CONTA_NAO_QUALIFICADA_SUBCODE:
        relatorio["conta_nao_qualificada"] = True
        return True
    return False


# --------------------------------------------------------------- estado
def carregar_estado(caminho):
    if os.path.isfile(caminho):
        return json.load(open(caminho, encoding="utf-8"))
    return {}


def salvar_estado(caminho, st):
    json.dump(st, open(caminho, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


# --------------------------------------------------------------- copia
def copiar_campanha(origem_id, destino, st, pausar_original, pagador_regulacao, relatorio):
    m = st.setdefault(origem_id, {"adsets": {}, "pausada": False})
    if m.get("pausada"):
        print(f"   {origem_id} ja movida e pausada — pulando")
        return

    camp = call("GET", origem_id, {
        "fields": "name,daily_budget,lifetime_budget,bid_strategy,status"})
    if "error" in camp:
        print(f"   ERRO lendo campanha {origem_id}: {msg_erro(camp)}")
        relatorio["erros"][msg_erro(camp)] += 1
        return

    if not m.get("camp"):
        dados = {
            "name": camp["name"],
            "objective": "OUTCOME_SALES",
            "buying_type": "AUCTION",
            "special_ad_categories": json.dumps([]),
            "is_adset_budget_sharing_enabled": "false",
            "bid_strategy": camp.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP"),
            "status": "PAUSED",
        }
        if camp.get("daily_budget"):
            dados["daily_budget"] = camp["daily_budget"]
        if camp.get("lifetime_budget"):
            dados["lifetime_budget"] = camp["lifetime_budget"]
        d = call("POST", f"{destino}/campaigns", dados)
        if "id" not in d:
            print(f"   ERRO criando campanha '{camp['name']}': {msg_erro(d)}")
            relatorio["erros"][msg_erro(d)] += 1
            return
        m["camp"] = d["id"]
        salvar_estado(st["_caminho"], st)
        relatorio["campanhas"] += 1
        print(f"   campanha criada: {d['id']} ({camp['name']})")

    campanha_atual = m["camp"]
    for oas in paginar(f"{API}/{origem_id}/adsets", {"fields": CAMPOS_ADSET, "limit": 100}):
        info = m["adsets"].setdefault(oas["id"], {"ads": {}})
        if not info.get("id"):
            reg_ident = oas.get("regional_regulation_identities")
            if not reg_ident:
                if not pagador_regulacao:
                    print(f"   ERRO conjunto '{oas['name']}': sem regional_regulation_identities "
                          f"na origem e --pagador-regulacao nao foi passado. Pulando esse conjunto.")
                    relatorio["erros"]["conjunto sem regional_regulation_identities e sem --pagador-regulacao"] += 1
                    continue
                reg_ident = {"universal_beneficiary": pagador_regulacao,
                             "universal_payer": pagador_regulacao}

            dados = {
                "name": oas["name"],
                "campaign_id": campanha_atual,
                "optimization_goal": oas["optimization_goal"],
                "billing_event": oas["billing_event"],
                "promoted_object": json.dumps(oas["promoted_object"]),
                "targeting": json.dumps(oas["targeting"]),
                "attribution_spec": json.dumps(oas.get("attribution_spec") or []),
                "regional_regulated_categories": json.dumps(
                    sorted(set((oas.get("regional_regulated_categories") or [])
                               + ["BRAZIL_REGULATION", "VOLUNTARY_VERIFICATION"]))),
                "regional_regulation_identities": json.dumps(reg_ident),
                "status": oas["status"],
            }
            if oas.get("bid_amount"):
                dados["bid_amount"] = oas["bid_amount"]
            if oas.get("daily_budget"):
                dados["daily_budget"] = oas["daily_budget"]
            if oas.get("lifetime_budget"):
                dados["lifetime_budget"] = oas["lifetime_budget"]

            d = call("POST", f"{destino}/adsets", dados)
            if "id" not in d:
                if classificar_erro(d, relatorio):
                    print(f"   AVISO conjunto '{oas['name']}': {msg_erro(d)} — seguindo")
                    continue
                e = d.get("error", {})
                if e.get("code") == ERRO_LIMITE_CONJUNTOS_CBO:
                    print(f"   limite de conjuntos por campanha CBO atingido — "
                          f"abrindo campanha de continuacao")
                    nova = call("POST", f"{destino}/campaigns", {
                        "name": camp["name"] + " (cont.)",
                        "objective": "OUTCOME_SALES", "buying_type": "AUCTION",
                        "special_ad_categories": json.dumps([]),
                        "is_adset_budget_sharing_enabled": "false",
                        "bid_strategy": camp.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP"),
                        "status": "PAUSED",
                        **({"daily_budget": camp["daily_budget"]} if camp.get("daily_budget") else {}),
                    })
                    if "id" not in nova:
                        print(f"   ERRO abrindo campanha de continuacao: {msg_erro(nova)}")
                        relatorio["erros"][msg_erro(nova)] += 1
                        continue
                    campanha_atual = nova["id"]
                    m.setdefault("campanhas_overflow", []).append(nova["id"])
                    salvar_estado(st["_caminho"], st)
                    dados["campaign_id"] = campanha_atual
                    d = call("POST", f"{destino}/adsets", dados)
                    if "id" not in d:
                        print(f"   ERRO conjunto '{oas['name']}' na campanha de continuacao: {msg_erro(d)}")
                        relatorio["erros"][msg_erro(d)] += 1
                        continue
                else:
                    print(f"   ERRO conjunto '{oas['name']}': {msg_erro(d)}")
                    relatorio["erros"][msg_erro(d)] += 1
                    continue
            info["id"] = d["id"]
            relatorio["conjuntos"] += 1
            salvar_estado(st["_caminho"], st)

        ads_origem = paginar(f"{API}/{oas['id']}/ads", {"fields": CAMPOS_AD, "limit": 100})
        for a in ads_origem:
            if a["id"] in info["ads"]:
                continue
            cr0 = a.get("creative") or {}
            post = cr0.get("effective_object_story_id")
            if not post:
                print(f"   SEM POST existente: '{a['name']}' — nao e possivel copiar por post, pulando")
                relatorio["erros"]["anuncio sem post existente (effective_object_story_id)"] += 1
                continue
            cr = call("POST", f"{destino}/adcreatives", {
                "name": a["name"], "object_story_id": post,
                "url_tags": cr0.get("url_tags") or TAGS_PADRAO})
            if "id" not in cr:
                if classificar_erro(cr, relatorio):
                    print(f"   AVISO criativo '{a['name']}': {msg_erro(cr)} — seguindo")
                    continue
                print(f"   ERRO criativo '{a['name']}': {msg_erro(cr)}")
                relatorio["erros"][msg_erro(cr)] += 1
                continue
            ad = call("POST", f"{destino}/ads", {
                "name": a["name"], "adset_id": info["id"],
                "creative": json.dumps({"creative_id": cr["id"]}), "status": a["status"]})
            if "id" not in ad:
                print(f"   ERRO anuncio '{a['name']}': {msg_erro(ad)}")
                relatorio["erros"][msg_erro(ad)] += 1
                continue
            info["ads"][a["id"]] = ad["id"]
            relatorio["anuncios"] += 1
            salvar_estado(st["_caminho"], st)
            print(f"   anuncio '{a['name']}' -> {ad['id']}")

        print(f"   conjunto ok: {oas['name'][:60]} ({len(info['ads'])} anuncios)")

    if pausar_original:
        todos_ads_origem = sum(
            len(paginar(f"{API}/{oas_id}/ads", {"fields": "id", "limit": 100}))
            for oas_id in m["adsets"])
        todos_ads_copiados = sum(len(v["ads"]) for v in m["adsets"].values())
        if todos_ads_copiados >= todos_ads_origem and todos_ads_origem > 0:
            r = call("POST", origem_id, {"status": "PAUSED"})
            if r.get("success"):
                m["pausada"] = True
                salvar_estado(st["_caminho"], st)
                print(f"   PAUSOU original {origem_id}")
        else:
            print(f"   nao pausou original: {todos_ads_copiados}/{todos_ads_origem} anuncios copiados")


# --------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    origem_grp = ap.add_mutually_exclusive_group(required=True)
    origem_grp.add_argument("--origem", nargs="+", help="um ou mais campaign_id de origem")
    origem_grp.add_argument("--origem-arquivo", help="JSON com lista de ids ou lista de {id:...}")
    ap.add_argument("--destino", required=True, help="act_X de destino")
    ap.add_argument("--estado", required=True, help="arquivo de estado para retomada")
    ap.add_argument("--pausar-original", action="store_true",
                     help="pausa a campanha de origem depois de copiar todos os anuncios")
    ap.add_argument("--pagador-regulacao",
                     help="advertiser_id a usar quando o conjunto de origem nao tiver "
                          "regional_regulation_identities (conjuntos antigos)")
    ap.add_argument("--dry", action="store_true", help="mostra o plano sem escrever nada")
    args = ap.parse_args()

    if args.origem_arquivo:
        bruto = json.load(open(args.origem_arquivo, encoding="utf-8"))
        origens = [item["id"] if isinstance(item, dict) else str(item) for item in bruto]
    else:
        origens = args.origem

    if args.dry:
        print(f"[dry] {len(origens)} campanha(s) de origem -> {args.destino}")
        total_dia = 0
        for oid in origens:
            camp = call("GET", oid, {"fields": "name,daily_budget,lifetime_budget,bid_strategy,status"})
            if "error" in camp:
                print(f"  {oid}: ERRO lendo — {msg_erro(camp)}")
                continue
            nconj = len(paginar(f"{API}/{oid}/adsets", {"fields": "id", "limit": 100}))
            db = int(camp.get("daily_budget") or 0)
            total_dia += db
            print(f"  {oid}  '{camp['name']}'  {nconj} conjunto(s)  "
                  f"daily_budget={db/100:.2f}  bid_strategy={camp.get('bid_strategy')}  status={camp['status']}")
        print(f"\n[dry] orcamento diario total das origens: {total_dia/100:.2f}")
        print("[dry] rode sem --dry pra aplicar. Nada foi escrito.")
        return

    st = carregar_estado(args.estado)
    st["_caminho"] = args.estado
    relatorio = {
        "campanhas": 0, "conjuntos": 0, "anuncios": 0,
        "erros": collections.Counter(),
        "paginas_sem_permissao": set(),
        "conta_nao_qualificada": False,
    }

    for oid in origens:
        print(f"\n=== origem {oid}")
        copiar_campanha(oid, args.destino, st, args.pausar_original, args.pagador_regulacao, relatorio)
        if relatorio["conta_nao_qualificada"]:
            print("\nABORTANDO: conta de destino nao qualificada para gravacao "
                  "(pagamento pendente) — nao e possivel criar nem pausar nada ali.")
            break

    del st["_caminho"]
    salvar_estado(args.estado, st)

    print("\n=== RELATORIO FINAL ===")
    print(f"campanhas criadas: {relatorio['campanhas']}")
    print(f"conjuntos criados: {relatorio['conjuntos']}")
    print(f"anuncios criados: {relatorio['anuncios']}")
    if relatorio["paginas_sem_permissao"]:
        print("paginas sem permissao (liberar no Business Manager):")
        for p in relatorio["paginas_sem_permissao"]:
            print(f"  - {p}")
    if relatorio["erros"]:
        print("erros agrupados por motivo:")
        for motivo, n in relatorio["erros"].most_common():
            print(f"  {n}x  {motivo}")


if __name__ == "__main__":
    main()
