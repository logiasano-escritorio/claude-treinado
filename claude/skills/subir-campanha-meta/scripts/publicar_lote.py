#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publisher generico Meta Ads (Graph API v23.0) — dirigido por manifesto.

    python3 publicar_lote.py <manifesto.json>          sobe o lote
    python3 publicar_lote.py <manifesto.json> --dry     valida e mostra o plano

Toda a config (conta, pixel, page, advertiser, copy, link, midia) vem do
manifesto, entao o mesmo script serve pra qualquer produto e qualquer conta.

Estruturas suportadas (campo "estrutura" no manifesto):
  1-1-1   1 campanha, 1 conjunto, 1 anuncio por item de "ads" (padrao historico)
  1-1-N   1 campanha, 1 conjunto, N anuncios — "ads" e dividido em lotes de
          "anuncios_por_conjunto"
  ABO     1 campanha (sem orcamento), N conjuntos em "conjuntos", cada um com
          seu proprio orcamento (Ad Set Budget Optimization)
  CBO     1 campanha com orcamento, N conjuntos em "conjuntos" competindo
          (Campaign Budget Optimization)

Estrategias de lance (campo "lance.estrategia"):
  menor_custo   LOWEST_COST_WITHOUT_CAP, sem bid_amount
  bid_cap       LOWEST_COST_WITH_BID_CAP na campanha (ou no conjunto em ABO) +
                bid_amount em cada conjunto
  cost_cap      COST_CAP no mesmo nivel do bid_strategy + bid_amount (teto de
                custo) em cada conjunto

Fontes de midia por anuncio: video_path (arquivo local), video_drive_id
(video no Google Drive, sobe via file_url), image_path (arquivo local),
post_id (anuncio por post existente — object_story_id; preferido quando o
post ja existe, mantem curtidas/comentarios e NAO precisa de
degrees_of_freedom_spec).

MANIFESTO ANTIGO (sem "estrutura"/"orcamento"/"lance") continua funcionando
sem mudanca nenhuma: e normalizado para "1-1-1" com os campos antigos
(campanha.daily_budget_cents, campanha.bid_strategy, adset.bid_amount) lidos
automaticamente. Ver SKILL.md, secao "migracao do manifesto antigo".

Idempotente por NOME DE CAMPANHA (e, dentro dela, por nome de conjunto e de
anuncio via o .resultado.json): lista o que ja existe antes de comecar e
pula. Rodar de novo depois de uma falha continua de onde parou.

Token: variavel de ambiente META_ACCESS_TOKEN, ou um token.txt ao lado deste
arquivo. Nunca hardcodar, nunca commitar.

Trilha de video (upload -> ready -> thumb -> video_data) roda em producao
desde 2026-09. Trilha de imagem (adimages -> link_data) segue o formato
validado em 2026-05. Trilha de video por Drive (file_url) e de post
existente (object_story_id) rodam em producao desde 2026-10/11.

Orcamento TOTAL (lifetime_budget) e estrategia cost_cap sao novos nesta
versao e NAO foram testados num run real ainda — teste com uma campanha
pequena antes de confiar em lote grande. Se a API reclamar de campo
faltante, registre o erro em REFERENCIA-API-META.md.
"""
import argparse
import collections
import copy
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.request as _ur

AQUI = os.path.dirname(os.path.abspath(__file__))
API = "https://graph.facebook.com/v23.0"

CODIGOS_TRANSIENTES = {1, 2, 4, 17, 32, 613, 80004}
ESTRUTURAS = ("1-1-1", "1-1-N", "ABO", "CBO")
ESTRATEGIAS_LANCE = ("menor_custo", "bid_cap", "cost_cap")
MAX_ADS_POR_CONJUNTO = 50
ERRO_LIMITE_CONJUNTOS_CBO = 1885940
ERRO_SEM_PERMISSAO_PAGINA = 1885499
ERRO_CONTA_NAO_QUALIFICADA_SUBCODE = 4841021

EXTENSOES_VIDEO = (".mp4", ".mov", ".m4v")


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
    """GET/POST com retry exponencial nos codigos transientes (rate limit e
    afins). Devolve sempre o JSON decodificado (inclusive {"error": ...})."""
    params = dict(params or {})
    params["access_token"] = TOKEN
    for tentativa in range(6):
        try:
            if method == "GET":
                req = urllib.request.Request(f"{API}/{path}?" + urllib.parse.urlencode(params))
            else:
                req = urllib.request.Request(
                    f"{API}/{path}", data=urllib.parse.urlencode(params).encode("utf-8"))
            return json.load(urllib.request.urlopen(req, timeout=180))
        except urllib.error.HTTPError as e:
            corpo = e.read().decode("utf-8", "replace")
            try:
                err = json.loads(corpo)["error"]
            except Exception:
                raise RuntimeError(f"{path}: {corpo[:500]}")
            if err.get("code") in CODIGOS_TRANSIENTES or err.get("is_transient"):
                espera = 30 * (tentativa + 1)
                print(f"   transiente ({err.get('code')}) — aguardando {espera}s")
                time.sleep(espera)
                continue
            raise RuntimeError(f"{path}: {json.dumps(err, ensure_ascii=False)[:600]}")
        except Exception as e:
            if tentativa == 5:
                raise RuntimeError(f"{path}: falha de rede persistente ({e})")
            time.sleep(20)
    raise RuntimeError(f"{path}: retry esgotado")


def paginar(path, params):
    out = []
    url = f"{API}/{path}?" + urllib.parse.urlencode({**params, "access_token": TOKEN})
    while url:
        d = json.load(_ur.urlopen(url, timeout=180))
        out += d.get("data", [])
        url = (d.get("paging") or {}).get("next")
    return out


# --------------------------------------------------------------- midia: video local/drive, imagem
def upload_video(act, caminho):
    """Upload simples (multipart). Acima de ~90MB o Meta devolve HTTP 413 em
    0,2s (nao e timeout) — precisa de upload em partes, nao implementado aqui."""
    import subprocess
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


def upload_video_drive(act, drive_id, nome):
    """Video que mora numa pasta publica do Google Drive: sobe direto por
    file_url, sem baixar local primeiro. Validado em producao 2026-10."""
    url = f"https://drive.usercontent.google.com/download?id={drive_id}&export=download&confirm=t"
    d = call(f"{act}/advideos", {"file_url": url, "name": nome}, "POST")
    if "id" not in d:
        raise RuntimeError(f"upload drive {nome}: {d.get('error')}")
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
    import subprocess
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


# --------------------------------------------------------------- listar pasta do Drive
def listar_pasta_drive(pasta_id, prefixo="", profundidade=0, maximo_profundidade=3):
    """Lista (nome, drive_id_ou_url) de uma pasta publica do Google Drive via
    embeddedfolderview, recursivamente. Regex validado em producao: casa
    cada <a href> cujo bloco seguinte tem a classe flip-entry-title."""
    import html as _html
    url = f"https://drive.google.com/embeddedfolderview?id={pasta_id}#list"
    s = _ur.urlopen(url, timeout=60).read().decode("utf-8", "replace")
    out = []
    for m in re.finditer(r'<a href="([^"]+)"[^>]*>.*?flip-entry-title">([^<]+)<', s, re.S):
        link, nome = m.group(1), _html.unescape(m.group(2))
        if "/folders/" in link:
            sub = re.search(r"/folders/([^/?]+)", link)
            if sub and profundidade < maximo_profundidade:
                out += listar_pasta_drive(sub.group(1), prefixo + nome + "/",
                                           profundidade + 1, maximo_profundidade)
            continue
        d = re.search(r"/d/([^/]+)", link)
        out.append((prefixo + nome, d.group(1) if d else link))
    return out


def montar_ads_de_drive(cfg):
    """cfg = manifesto['drive_pasta']: {pasta_id, excluir?, incluir_apenas?}.
    Devolve itens de 'ads' no formato {nome, video_drive_id}."""
    itens = listar_pasta_drive(cfg["pasta_id"])
    excluir = [re.compile(p) for p in cfg.get("excluir", [])]
    incluir_apenas = set(cfg.get("incluir_apenas") or [])
    ads = []
    for nome, drive_id in itens:
        if not nome.lower().endswith(EXTENSOES_VIDEO):
            continue
        base = os.path.splitext(nome)[0]
        if incluir_apenas:
            if nome not in incluir_apenas and base not in incluir_apenas:
                continue
        elif any(p.search(nome) for p in excluir):
            continue
        ads.append({"nome": base, "video_drive_id": drive_id})
    return ads


# --------------------------------------------------------------- normalizacao do manifesto
def normalizar(m):
    """Traduz manifesto ANTIGO (sem estrutura/orcamento/lance) pro formato
    interno novo, sem exigir nenhuma mudanca de quem ja usa o manifesto
    antigo. Devolve uma COPIA normalizada; nunca muta o original."""
    m = copy.deepcopy(m)
    m.setdefault("estrutura", "1-1-1")
    m.setdefault("anuncios_por_conjunto", 1)

    camp_cfg = m.get("campanha", {})
    adset_cfg = m.get("adset", {})

    if "orcamento" not in m:
        if "daily_budget_cents" in camp_cfg:
            m["orcamento"] = {"tipo": "diario", "valor": camp_cfg["daily_budget_cents"]}
        elif "lifetime_budget_cents" in camp_cfg:
            m["orcamento"] = {"tipo": "total", "valor": camp_cfg["lifetime_budget_cents"],
                               "fim": camp_cfg.get("fim")}

    if "lance" not in m:
        bs = camp_cfg.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP")
        if bs == "LOWEST_COST_WITH_BID_CAP":
            m["lance"] = {"estrategia": "bid_cap", "valor": adset_cfg.get("bid_amount")}
        elif bs == "COST_CAP":
            m["lance"] = {"estrategia": "cost_cap", "valor": adset_cfg.get("bid_amount")}
        else:
            m["lance"] = {"estrategia": "menor_custo"}

    if "drive_pasta" in m and m["estrutura"] in ("1-1-1", "1-1-N"):
        m.setdefault("ads", [])
        m["ads"] = m["ads"] + montar_ads_de_drive(m["drive_pasta"])

    return m


BID_STRATEGY_POR_ESTRATEGIA = {
    "menor_custo": "LOWEST_COST_WITHOUT_CAP",
    "bid_cap": "LOWEST_COST_WITH_BID_CAP",
    "cost_cap": "COST_CAP",
}


def params_orcamento(orcamento, nivel):
    """nivel: 'campanha' ou 'conjunto'. end_time so e enviado no conjunto —
    e o campo documentado pra lifetime_budget de ad set. Lifetime_budget na
    campanha sem end_time nao foi validado em run real ainda."""
    if orcamento["tipo"] == "diario":
        return {"daily_budget": str(orcamento["valor"])}
    p = {"lifetime_budget": str(orcamento["valor"])}
    if nivel == "conjunto" and orcamento.get("fim"):
        p["end_time"] = orcamento["fim"]
    return p


def nome_ad(item, indice):
    return (item.get("nome") or item.get("hook")
            or (os.path.splitext(os.path.basename(
                item.get("video_path") or item.get("image_path") or ""))[0])
            or item.get("post_id") or f"ad-{indice:02d}")


# --------------------------------------------------------------- montar grupos (unifica as 4 estruturas)
def montar_grupos(m):
    """Devolve lista de campanhas no formato interno:
    {nome, budget_params, bid_strategy, status, conjuntos:[
        {nome, budget_params, bid_strategy, bid_amount, targeting,
         attribution_spec, pixel_id, custom_event_type, optimization_goal,
         billing_event, status, ads:[{nome, video_path?, video_drive_id?,
         image_path?, post_id?, video_id?, image_hash?}]}
    ]}"""
    adset_cfg = m["adset"]
    orcamento, lance = m["orcamento"], m["lance"]
    bid_strategy = BID_STRATEGY_POR_ESTRATEGIA[lance["estrategia"]]
    bid_amount = lance.get("valor") if lance["estrategia"] != "menor_custo" else None
    estrutura = m["estrutura"]

    def conjunto_base(nome_conjunto, overrides=None):
        ov = overrides or {}
        return {
            "nome": nome_conjunto,
            "targeting": ov.get("targeting", adset_cfg["targeting"]),
            "attribution_spec": ov.get("attribution_spec", adset_cfg["attribution_spec"]),
            "pixel_id": ov.get("pixel_id", adset_cfg["pixel_id"]),
            "custom_event_type": ov.get("custom_event_type", adset_cfg.get("custom_event_type", "PURCHASE")),
            "optimization_goal": ov.get("optimization_goal", adset_cfg["optimization_goal"]),
            "billing_event": ov.get("billing_event", adset_cfg["billing_event"]),
            "status": ov.get("status", adset_cfg.get("status", "ACTIVE")),
            "advertiser_id": ov.get("advertiser_id", adset_cfg["advertiser_id"]),
            "budget_params": {},
            "bid_strategy": None,
            "bid_amount": None,
        }

    grupos = []

    if estrutura in ("1-1-1", "1-1-N"):
        tamanho = 1 if estrutura == "1-1-1" else m["anuncios_por_conjunto"]
        ads = m["ads"]
        lotes = [ads[i:i + tamanho] for i in range(0, len(ads), tamanho)]
        for idx, lote in enumerate(lotes, 1):
            if estrutura == "1-1-1":
                nome_campanha = lote[0]["campaign_name"]
                nome_conjunto = nome_campanha
                ads_formatados = [{**lote[0], "nome": nome_campanha}]
            else:
                base = m.get("campanha_nome_base") or m.get("campanha_nome") or m.get("produto", "Lote")
                primeiro, ultimo = nome_ad(lote[0], 0), nome_ad(lote[-1], len(lote) - 1)
                nome_campanha = f"{base} - C{idx:02d} ({primeiro}-{ultimo})"
                nome_conjunto = f"CJ - C{idx:02d}"
                ads_formatados = [{**item, "nome": nome_ad(item, i)} for i, item in enumerate(lote)]

            conj = conjunto_base(nome_conjunto)
            conj["ads"] = ads_formatados
            conj["bid_amount"] = bid_amount
            grupos.append({
                "nome": nome_campanha,
                "budget_params": params_orcamento(orcamento, "campanha"),
                "bid_strategy": bid_strategy,
                "status": m["campanha"].get("status", "PAUSED"),
                "conjuntos": [conj],
            })

    elif estrutura == "ABO":
        nome_campanha = m["campanha_nome"]
        conjuntos = []
        for c in m["conjuntos"]:
            conj = conjunto_base(c["nome"], c)
            orc_conj = {"tipo": orcamento["tipo"],
                        "valor": c.get("orcamento_valor_cents", orcamento["valor"]),
                        "fim": c.get("orcamento_fim", orcamento.get("fim"))}
            conj["budget_params"] = params_orcamento(orc_conj, "conjunto")
            conj["bid_strategy"] = bid_strategy
            conj["bid_amount"] = c.get("bid_valor_cents", bid_amount)
            conj["ads"] = [{**item, "nome": nome_ad(item, i)} for i, item in enumerate(c["ads"])]
            conjuntos.append(conj)
        grupos.append({
            "nome": nome_campanha,
            "budget_params": {},
            "bid_strategy": None,
            "status": m["campanha"].get("status", "PAUSED"),
            "conjuntos": conjuntos,
        })

    elif estrutura == "CBO":
        nome_campanha = m["campanha_nome"]
        conjuntos = []
        for c in m["conjuntos"]:
            conj = conjunto_base(c["nome"], c)
            conj["budget_params"] = {}
            conj["bid_strategy"] = None
            conj["bid_amount"] = c.get("bid_valor_cents", bid_amount)
            conj["ads"] = [{**item, "nome": nome_ad(item, i)} for i, item in enumerate(c["ads"])]
            conjuntos.append(conj)
        grupos.append({
            "nome": nome_campanha,
            "budget_params": params_orcamento(orcamento, "campanha"),
            "bid_strategy": bid_strategy,
            "status": m["campanha"].get("status", "PAUSED"),
            "conjuntos": conjuntos,
        })

    return grupos


# --------------------------------------------------------------- validacao
def validar(m):
    """Pega no seco os erros que so apareceriam no meio do run."""
    problemas = []

    if m.get("estrutura") and m["estrutura"] not in ESTRUTURAS:
        problemas.append(f"estrutura '{m['estrutura']}' invalida — use um de {ESTRUTURAS}")
        return problemas

    for campo in ("account_id", "campanha", "adset", "creative"):
        if campo not in m:
            problemas.append(f"falta a chave '{campo}' no manifesto")
    if problemas:
        return problemas

    if not str(m["account_id"]).startswith("act_"):
        problemas.append("account_id precisa do prefixo 'act_'")

    estrutura = m.get("estrutura", "1-1-1")
    anuncios_por_conjunto = m.get("anuncios_por_conjunto", 1)
    if anuncios_por_conjunto > MAX_ADS_POR_CONJUNTO:
        problemas.append(
            f"anuncios_por_conjunto={anuncios_por_conjunto} > {MAX_ADS_POR_CONJUNTO} "
            "(limite da API) — divida em mais conjuntos/campanhas")

    orcamento = m.get("orcamento")
    if not orcamento or orcamento.get("tipo") not in ("diario", "total") or not orcamento.get("valor"):
        problemas.append("orcamento.tipo (diario|total) e orcamento.valor (centavos) sao obrigatorios")
    if orcamento and orcamento.get("tipo") == "total" and not orcamento.get("fim"):
        problemas.append("orcamento.tipo=total sem orcamento.fim — nao validado em producao, "
                          "teste com uma campanha pequena antes (ver REFERENCIA)")

    lance = m.get("lance")
    if not lance or lance.get("estrategia") not in ESTRATEGIAS_LANCE:
        problemas.append(f"lance.estrategia obrigatoria, uma de {ESTRATEGIAS_LANCE}")
    elif lance["estrategia"] != "menor_custo" and not lance.get("valor"):
        problemas.append(f"lance.estrategia={lance['estrategia']} precisa de lance.valor (centavos)")

    a, c = m["adset"], m["creative"]
    for campo in ("pixel_id", "advertiser_id", "targeting", "optimization_goal", "billing_event"):
        if not a.get(campo):
            problemas.append(f"adset.{campo} vazio")
    for campo in ("page_id", "link", "message"):
        if not c.get(campo):
            problemas.append(f"creative.{campo} vazio")

    if estrutura in ("1-1-1", "1-1-N"):
        if not m.get("ads"):
            problemas.append("manifesto sem 'ads' (e sem drive_pasta que gere algum)")
    else:
        if not m.get("campanha_nome"):
            problemas.append(f"estrutura={estrutura} precisa de 'campanha_nome'")
        if not m.get("conjuntos"):
            problemas.append(f"estrutura={estrutura} precisa da lista 'conjuntos'")
        else:
            nomes_conj = set()
            for i, cj in enumerate(m["conjuntos"]):
                if not cj.get("nome"):
                    problemas.append(f"conjuntos[{i}] sem 'nome'")
                elif cj["nome"] in nomes_conj:
                    problemas.append(f"nome de conjunto duplicado: '{cj['nome']}'")
                else:
                    nomes_conj.add(cj["nome"])
                if not cj.get("ads"):
                    problemas.append(f"conjuntos[{i}] ('{cj.get('nome')}') sem 'ads'")
                if estrutura == "CBO" and lance and lance.get("estrategia") != "menor_custo" \
                        and not (cj.get("bid_valor_cents") or lance.get("valor")):
                    problemas.append(f"conjuntos[{i}] ('{cj.get('nome')}') sem bid_valor_cents "
                                      "e sem lance.valor padrao")

    alvo = a.get("targeting") or {}
    aa = (alvo.get("targeting_automation") or {}).get("advantage_audience")
    if aa is None:
        problemas.append("targeting.targeting_automation.advantage_audience nao declarado — subcode 1870227")
    if aa == 1 and alvo.get("age_min", 0) > 25:
        problemas.append(
            f"advantage_audience=1 com age_min={alvo.get('age_min')} — o maximo e 25 (subcode 1870188)")

    def validar_ads(ads_lista, contexto):
        vistos = set()
        algum_sem_post = False
        for i, item in enumerate(ads_lista):
            if estrutura == "1-1-1" and not item.get("campaign_name"):
                problemas.append(f"{contexto}[{i}] sem campaign_name")
                continue
            nome = item.get("campaign_name") or item.get("nome") or f"{contexto}[{i}]"
            if nome in vistos:
                problemas.append(f"nome duplicado em '{contexto}': '{nome}'")
            vistos.add(nome)
            caminho = item.get("video_path") or item.get("image_path")
            tem_midia = caminho or item.get("video_id") or item.get("image_hash") \
                or item.get("video_drive_id") or item.get("post_id")
            if not tem_midia:
                problemas.append(f"'{nome}' sem video_path/image_path/video_drive_id/post_id")
            elif caminho and not os.path.isfile(caminho):
                problemas.append(f"'{nome}': arquivo nao existe — {caminho}")
            if not item.get("post_id"):
                algum_sem_post = True
        return algum_sem_post

    algum_sem_post = False
    if estrutura in ("1-1-1", "1-1-N"):
        algum_sem_post = validar_ads(m.get("ads", []), "ads")
    else:
        for cj in m.get("conjuntos", []):
            if validar_ads(cj.get("ads", []), f"conjuntos/{cj.get('nome')}"):
                algum_sem_post = True

    if algum_sem_post:
        dof = c.get("degrees_of_freedom_spec") or {}
        feats = dof.get("creative_features_spec") or {}
        if not feats:
            problemas.append(
                "creative.degrees_of_freedom_spec ausente — obrigatorio quando ha anuncio "
                "por video/imagem nova (nao se aplica a anuncio 100% por post_id). Sem ele a "
                "Meta liga os aprimoramentos automaticos, inclusive o 'Ligar agora'.")
        else:
            if "standard_enhancements" in feats:
                problemas.append(
                    "creative_features_spec tem 'standard_enhancements' — DESCONTINUADO, "
                    "quebra o POST com subcode 3858504. Remover so esse campo.")
            se = feats.get("site_extensions", {}).get("enroll_status")
            if se != "OPT_OUT":
                problemas.append(f"site_extensions esta '{se}', tem que ser OPT_OUT")

    return problemas


# --------------------------------------------------------------- estado / idempotencia
def carregar_resultado(path):
    """Suporta o formato antigo (lista plana) e converte pro novo (dict por
    campanha/conjunto/ad), pra nao quebrar retomada de runs antigos."""
    if not os.path.isfile(path):
        return {"campanhas": {}, "conjuntos": {}, "ads": {}}
    bruto = json.load(open(path, encoding="utf-8"))
    if isinstance(bruto, list):
        st = {"campanhas": {}, "conjuntos": {}, "ads": {}}
        for item in bruto:
            nome = item.get("campaign_name")
            if not nome:
                continue
            if item.get("campaign_id"):
                st["campanhas"][nome] = item["campaign_id"]
            if item.get("adset_id"):
                st["conjuntos"][nome] = {"id": item["adset_id"], "campanha": nome}
            if item.get("ad_id"):
                st["ads"][nome] = {"id": item["ad_id"], "conjunto": nome}
        return st
    bruto.setdefault("campanhas", {})
    bruto.setdefault("conjuntos", {})
    bruto.setdefault("ads", {})
    return bruto


def salvar_resultado(path, st):
    json.dump(st, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def campanhas_existentes(act):
    nomes = {}
    for c in paginar(f"{act}/campaigns", {"fields": "id,name", "limit": "200"}):
        nomes[c["name"]] = c["id"]
    return nomes


# --------------------------------------------------------------- criacao
def criar_campanha(act, grupo, relatorio):
    dados = {
        "name": grupo["nome"],
        "objective": "OUTCOME_SALES",
        "buying_type": "AUCTION",
        "special_ad_categories": json.dumps([]),
        "is_adset_budget_sharing_enabled": "false",
        "status": grupo["status"],
        **grupo["budget_params"],
    }
    if grupo.get("bid_strategy"):
        dados["bid_strategy"] = grupo["bid_strategy"]
    d = call(f"{act}/campaigns", dados, "POST")
    relatorio["campanhas"] += 1
    return d["id"]


def criar_conjunto(act, campanha_id, conj, relatorio):
    dados = {
        "name": conj["nome"],
        "campaign_id": campanha_id,
        "optimization_goal": conj["optimization_goal"],
        "billing_event": conj["billing_event"],
        "destination_type": "UNDEFINED",
        "promoted_object": json.dumps({
            "pixel_id": conj["pixel_id"], "custom_event_type": conj["custom_event_type"]}),
        "targeting": json.dumps(conj["targeting"]),
        "attribution_spec": json.dumps(conj["attribution_spec"]),
        # sem estes 2 campos nenhum conjunto BR e criado (subcode 3858634)
        "regional_regulated_categories": json.dumps(["BRAZIL_REGULATION", "VOLUNTARY_VERIFICATION"]),
        "regional_regulation_identities": json.dumps({
            "universal_beneficiary": conj["advertiser_id"], "universal_payer": conj["advertiser_id"]}),
        "status": conj["status"],
        **conj.get("budget_params", {}),
    }
    if conj.get("bid_strategy"):
        dados["bid_strategy"] = conj["bid_strategy"]
    if conj.get("bid_amount"):
        dados["bid_amount"] = str(conj["bid_amount"])
    d = call(f"{act}/adsets", dados, "POST")
    relatorio["conjuntos"] += 1
    return d["id"]


def criar_criativo_e_anuncio(act, adset_id, item, cre, ad_status, relatorio):
    nome = item["nome"]
    video_id = item.get("video_id")
    image_hash = item.get("image_hash")
    post_id = item.get("post_id")
    thumb = None

    oss = None
    if post_id:
        print(f"      por post existente: {post_id}")
    else:
        eh_video = bool(video_id or item.get("video_path") or item.get("video_drive_id"))
        if eh_video:
            if not video_id:
                if item.get("video_drive_id"):
                    print("      upload do video (Drive)...")
                    video_id = upload_video_drive(act, item["video_drive_id"], nome)
                else:
                    print("      upload do video (local)...")
                    video_id = upload_video(act, item["video_path"])
                print(f"          video_id={video_id}")
            print("      aguardando processamento...")
            esperar_ready(video_id)
            thumb = pegar_thumb(video_id)
        else:
            if not image_hash:
                print("      upload da imagem...")
                image_hash = upload_imagem(act, item["image_path"])
                print(f"          image_hash={image_hash}")

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
                "link": cre["link"], "message": cre["message"], "name": cre["title"],
                "image_hash": image_hash,
                "call_to_action": {"type": cre["cta_type"], "value": {"link": cre["link"]}},
            }
            if cre.get("description"):
                oss["link_data"]["description"] = cre["description"]

    params_criativo = {"name": nome, "url_tags": cre["url_tags"]}
    if post_id:
        params_criativo["object_story_id"] = post_id
    else:
        params_criativo["object_story_spec"] = json.dumps(oss, ensure_ascii=False)
        params_criativo["degrees_of_freedom_spec"] = json.dumps(cre["degrees_of_freedom_spec"])

    creative = call(f"{act}/adcreatives", params_criativo, "POST")
    ad = call(f"{act}/ads", {
        "name": nome, "adset_id": adset_id,
        "creative": json.dumps({"creative_id": creative["id"]}), "status": ad_status,
    }, "POST")
    relatorio["anuncios"] += 1
    return {"video_id": video_id, "image_hash": image_hash, "ad_id": ad["id"],
            "creative_id": creative["id"]}


# --------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifesto")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    bruto = json.load(open(args.manifesto, encoding="utf-8"))
    m = normalizar(bruto)
    problemas = validar(m)
    if problemas:
        print("MANIFESTO INVALIDO:")
        for p in problemas:
            print(f"  - {p}")
        sys.exit(1)

    act = m["account_id"]
    cre = m["creative"]
    grupos = montar_grupos(m)
    result_path = os.path.join(
        os.path.dirname(os.path.abspath(args.manifesto)),
        os.path.basename(args.manifesto).replace(".json", "") + ".resultado.json")

    conta = call(act, {"fields": "name,account_status,currency"})
    print(f"conta {conta.get('name')} ({act}) · status {conta.get('account_status')} · {conta.get('currency')}")
    if conta.get("account_status") != 1:
        print("  AVISO: account_status != 1, a conta pode estar restrita")

    ja = campanhas_existentes(act)
    total_ads = sum(len(cj["ads"]) for g in grupos for cj in g["conjuntos"])
    print(f"estrutura {m['estrutura']} · {len(grupos)} campanha(s) · "
          f"{sum(len(g['conjuntos']) for g in grupos)} conjunto(s) · {total_ads} anuncio(s)")

    if m["orcamento"]["tipo"] == "diario":
        total_dia = (sum(int(g["budget_params"].get("daily_budget", 0)) for g in grupos)
                     + sum(int(cj["budget_params"].get("daily_budget", 0))
                           for g in grupos for cj in g["conjuntos"]))
        print(f"orcamento diario total: {total_dia/100:.2f} (moeda da conta)")
    else:
        print(f"orcamento TOTAL (lifetime) por unidade: {m['orcamento']['valor']/100:.2f} — "
              "confira o numero de unidades acima para o total do lote")

    if args.dry:
        print("\n[dry] seria criado:")
        for g in grupos:
            existe = " (JA EXISTE)" if g["nome"] in ja else ""
            print(f"  campanha '{g['nome']}'{existe} · status {g['status']} · bid {g.get('bid_strategy')}")
            for cj in g["conjuntos"]:
                print(f"    conjunto '{cj['nome']}' · bid_amount={cj.get('bid_amount')} "
                      f"· {len(cj['ads'])} anuncio(s)")
                for item in cj["ads"]:
                    midia = (item.get("video_path") or item.get("image_path")
                             or item.get("video_drive_id") or item.get("post_id"))
                    print(f"      {item['nome']}  <- {midia}")
        print("\n[dry] manifesto valido. Rode sem --dry pra aplicar. Nada foi escrito.")
        return

    st = carregar_resultado(result_path)
    relatorio = {"campanhas": 0, "conjuntos": 0, "anuncios": 0, "erros": collections.Counter(),
                 "paginas_sem_permissao": set()}

    for g in grupos:
        print(f"\n=== campanha {g['nome']} ===")
        campanha_id = st["campanhas"].get(g["nome"]) or ja.get(g["nome"])
        if campanha_id:
            print(f"   ja existe ({campanha_id})")
        else:
            try:
                campanha_id = criar_campanha(act, g, relatorio)
            except RuntimeError as e:
                print(f"   ERRO criando campanha: {e}")
                relatorio["erros"][str(e)[:120]] += 1
                continue
        st["campanhas"][g["nome"]] = campanha_id
        salvar_resultado(result_path, st)

        campanha_destino_overflow = campanha_id
        conjuntos_na_campanha_atual = 0
        for cj in g["conjuntos"]:
            adset_info = st["conjuntos"].get(cj["nome"])
            if adset_info:
                print(f"   conjunto '{cj['nome']}' ja existe ({adset_info['id']})")
                adset_id = adset_info["id"]
            else:
                try:
                    adset_id = criar_conjunto(act, campanha_destino_overflow, cj, relatorio)
                except RuntimeError as e:
                    if str(ERRO_LIMITE_CONJUNTOS_CBO) in str(e):
                        print("   limite de conjuntos por campanha CBO atingido — "
                              "abrindo campanha de continuacao")
                        try:
                            campanha_destino_overflow = criar_campanha(
                                act, {**g, "nome": g["nome"] + " (cont.)"}, relatorio)
                            adset_id = criar_conjunto(act, campanha_destino_overflow, cj, relatorio)
                        except RuntimeError as e2:
                            print(f"   ERRO conjunto '{cj['nome']}' na campanha de continuacao: {e2}")
                            relatorio["erros"][str(e2)[:120]] += 1
                            continue
                    else:
                        print(f"   ERRO conjunto '{cj['nome']}': {e}")
                        relatorio["erros"][str(e)[:120]] += 1
                        continue
                st["conjuntos"][cj["nome"]] = {"id": adset_id, "campanha": g["nome"]}
                salvar_resultado(result_path, st)

            for item in cj["ads"]:
                nome_ad_ = item["nome"]
                if nome_ad_ in st["ads"]:
                    print(f"      anuncio '{nome_ad_}' ja existe ({st['ads'][nome_ad_]['id']}) — pulando")
                    continue
                try:
                    r = criar_criativo_e_anuncio(act, adset_id, item, cre,
                                                  m.get("ad_status", "ACTIVE"), relatorio)
                except RuntimeError as e:
                    msg = str(e)
                    if str(ERRO_SEM_PERMISSAO_PAGINA) in msg:
                        relatorio["paginas_sem_permissao"].add(cre.get("page_id", "?"))
                        print(f"      AVISO sem permissao na pagina — seguindo: {msg[:200]}")
                        continue
                    if str(ERRO_CONTA_NAO_QUALIFICADA_SUBCODE) in msg:
                        print("\nABORTANDO: conta nao qualificada para gravacao (pagamento pendente).")
                        salvar_resultado(result_path, st)
                        sys.exit(1)
                    print(f"      ERRO anuncio '{nome_ad_}': {msg[:300]}")
                    relatorio["erros"][msg[:120]] += 1
                    continue
                st["ads"][nome_ad_] = {"id": r["ad_id"], "conjunto": cj["nome"]}
                salvar_resultado(result_path, st)
                print(f"      OK anuncio '{nome_ad_}' -> {r['ad_id']}")

    print("\n=== RELATORIO FINAL ===")
    print(f"campanhas criadas nesta rodada: {relatorio['campanhas']}")
    print(f"conjuntos criados nesta rodada: {relatorio['conjuntos']}")
    print(f"anuncios criados nesta rodada: {relatorio['anuncios']}")
    if relatorio["paginas_sem_permissao"]:
        print("paginas sem permissao:", ", ".join(relatorio["paginas_sem_permissao"]))
    if relatorio["erros"]:
        print("erros agrupados por motivo:")
        for motivo, n in relatorio["erros"].most_common():
            print(f"  {n}x  {motivo}")
    print(f"\nresultado: {result_path}")
    print("Campanhas nascem conforme 'campanha.status' (normalmente PAUSED). "
          "Conferir no gerenciador antes de ligar.")


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
