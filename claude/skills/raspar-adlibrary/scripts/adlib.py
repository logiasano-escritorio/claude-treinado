# -*- coding: utf-8 -*-
"""
adlib.py — raspador da Meta Ad Library (publica) via DrissionPage.
SEM token, SEM login, SEM API. Abre um Chrome real e le o HTML.

USO
  python adlib.py dominio spnutrition-us.com            # busca por dominio (frase exata)
  python adlib.py termo "magnesio glicina"              # busca por termo livre
  python adlib.py dominio exemplo.com --min 500         # baixar o piso de caracteres
  python adlib.py dominio exemplo.com --max 30          # so as 30 primeiras
  python adlib.py dominio exemplo.com --sem-imagens     # pula o download dos criativos
  python adlib.py dominio exemplo.com --scroll 40       # mais scroll = mais anuncios
  python adlib.py dominio exemplo.com --saida "<slug>"  # nome da pasta/indice

SAIDA (dentro do vault, formato que o /adaptar-longform consome)
  Produtos/<Produto>/Benchmarking/<anunciante>/
      <SLUG>.md              indice: total, dedup, temas, top por variacoes_ativas
      <SLUG>/NNN - titulo.md uma nota por long-form unico, com frontmatter

O CAMPO QUE IMPORTA: variacoes_ativas
  Quantas copias do MESMO texto estao rodando ao mesmo tempo. E o proxy mais
  honesto de aposta do concorrente: se ele replicou 23 vezes, esta pagando a conta.
  A deduplicacao CONTA as repetidas em vez de descartar.
"""
import argparse, html as ihtml, json, os, re, sys, time, urllib.parse
from collections import Counter
from datetime import date

MESES = {"jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
         "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12}

TEMAS = [
    ("sono",            ["sleep", "insomnia", "awake", "sono", "insonia", "dormir", "3am", "3 a.m"]),
    ("emagrecimento",   ["weight", "pounds", "belly", "fat", "peso", "barriga", "emagrec", "gordura"]),
    ("artrite-dor",     ["joint", "arthritis", "pain", "knee", "artrite", "articula", "dor", "joelho"]),
    ("energia-fadiga",  ["energy", "fatigue", "tired", "exhaust", "energia", "fadiga", "cansa"]),
    ("menopausa",       ["menopause", "hot flash", "hormone", "menopausa", "hormonio", "calorao"]),
    ("enxaqueca",       ["migraine", "headache", "enxaqueca", "cabeca"]),
    ("pernas-inquietas", ["restless leg", "cramp", "pernas inquietas", "caibra"]),
    ("ansiedade",       ["anxiety", "stress", "panic", "ansiedade", "estresse", "panico"]),
    ("pele-estetica",   ["skin", "wrinkle", "melasma", "pele", "ruga", "mancha"]),
    ("intestino",       ["gut", "bloat", "digest", "intestino", "incha", "digest"]),
    ("pressao-coracao", ["blood pressure", "heart", "cholesterol", "pressao", "coracao", "colesterol"]),
]


def detectar_chrome():
    """Acha o Chrome no Windows, Mac ou Linux. Retorna None se o Drission achar sozinho."""
    cands = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        "/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium",
    ]
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


def achar_vault():
    """
    Acha o vault Sanologia certo. Forcar com SANO_VAULT=/caminho.
    Prefere o vault que ja tem a arvore de trabalho (Benchmarking/ ou
    'Adaptacoes prontas pra subir/'), porque pode haver mais de um vault
    Sanologia na maquina com estruturas diferentes.
    """
    def pontua(p):
        """Quanto maior, mais parece o vault de trabalho."""
        if not os.path.isdir(os.path.join(p, "Produtos")):
            return 0
        n = 1
        for sub in ["Produtos/Magnésio/Benchmarking",
                    "Produtos/Magnesio/Benchmarking",
                    "Produtos/Magnésio/Adaptacoes prontas pra subir",
                    "REGRAS-PORTUGUES-ORGANICO.md"]:
            if os.path.exists(os.path.join(p, *sub.split("/"))):
                n += 10
        return n

    if os.environ.get("SANO_VAULT"):
        p = os.environ["SANO_VAULT"]
        if pontua(p):
            return p
        print("aviso: SANO_VAULT nao parece um vault Sanologia -> " + p)

    home = os.path.expanduser("~")
    achados = []
    for raiz in [os.path.join(home, "Desktop"), home, os.path.join(home, "Documents")]:
        if not os.path.isdir(raiz):
            continue
        try:
            for nome in os.listdir(raiz):
                if "SANOLOGIA" not in nome.upper():
                    continue
                base = os.path.join(raiz, nome)
                if not os.path.isdir(base):
                    continue
                for cand in [base] + [os.path.join(base, x) for x in os.listdir(base)
                                      if os.path.isdir(os.path.join(base, x))]:
                    s = pontua(cand)
                    if s:
                        achados.append((s, cand))
        except (PermissionError, OSError):
            continue
    if not achados:
        return None
    achados.sort(key=lambda x: -x[0])
    if len(achados) > 1 and achados[0][0] == achados[1][0]:
        print("aviso: mais de um vault candidato. Usando: " + achados[0][1])
        print("       pra escolher outro: SANO_VAULT=/caminho")
    return achados[0][1]


def parse_date(s):
    m = re.search(r"(\d{1,2})\s+de\s+(\w{3})\w*\s+de\s+(20\d\d)", s, re.I)
    if not m:
        return None
    try:
        return date(int(m.group(3)), MESES.get(m.group(2).lower()[:3], 0), int(m.group(1)))
    except ValueError:
        return None


def clean(t):
    t = re.sub(r"<br\s*/?>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"[ \t]+", " ", ihtml.unescape(t)).strip()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def detectar_tema(txt):
    t = txt.lower()[:4000]
    for nome, chaves in TEMAS:
        if any(k in t for k in chaves):
            return nome
    return "outros"


def detectar_idioma(txt):
    t = " " + txt.lower()[:3000] + " "
    pt = sum(t.count(" %s " % w) for w in ["que", "nao", "para", "como", "mais", "voce", "com"])
    en = sum(t.count(" %s " % w) for w in ["the", "and", "that", "with", "you", "was", "for"])
    return "pt" if pt > en else "en"


def titulo_de(txt):
    """Primeira linha util do corpo, pra virar nome de arquivo e H1."""
    for ln in txt.split("\n"):
        ln = ln.strip(" #*_-\u2014")
        if 15 < len(ln) < 90 and not ln.lower().startswith(("http", "www")):
            return ln
    return txt[:70].strip()


def montar_url(modo, alvo):
    base = ("https://www.facebook.com/ads/library/?active_status=active&ad_type=all"
            "&country=ALL&is_targeted_country=false&media_type=all"
            "&sort_data[direction]=desc&sort_data[mode]=total_impressions")
    q = urllib.parse.quote(alvo)
    if modo == "dominio":
        return base + "&q=%%22%s%%22&search_type=keyword_exact_phrase" % q
    return base + "&q=%s&search_type=keyword_unordered" % q


def coletar(page, url, max_scroll):
    """Abre a busca, expande todos os 'Ver mais' e devolve o HTML completo."""
    page.get(url)
    time.sleep(6)
    last, cliques = 0, 0
    for s in range(max_scroll * 2):
        for b in page.eles("text:Ver mais", timeout=0.4):
            try:
                b.click(by_js=True); cliques += 1
            except Exception:
                pass
        page.scroll.down(1400)
        time.sleep(1.0)
        n = len(re.findall("Identifica[cç][aã]o da biblioteca", page.html))
        if n == last and s > 6:
            break
        last = n
        if s % 10 == 0 and s:
            print("      ... %d cards" % n)
    for _ in range(3):     # passadas finais: revelam os ultimos "Ver mais"
        for b in page.eles("text:Ver mais", timeout=0.4):
            try:
                b.click(by_js=True); cliques += 1
            except Exception:
                pass
        time.sleep(1)
    print("      %d cards, %d cliques em 'Ver mais'" % (last, cliques))
    return page.html


def extrair(html, min_chars):
    """Fatia o HTML por card e devolve os anuncios que passam do piso de caracteres."""
    idxs = [m.start() for m in re.finditer("Identifica[cç][aã]o da biblioteca", html)]
    out = []
    for k, i in enumerate(idxs):
        end = idxs[k + 1] if k + 1 < len(idxs) else min(i + 40000, len(html))
        blk = html[i:end]

        mid = re.search(r"biblioteca:\s*(?:</?\w+>\s*)*(\d{6,})", blk)
        ad_id = mid.group(1) if mid else "idx%d" % k

        md = re.search(r"[Vv]eicula[cç][aã]o iniciada em ([^<]+)", blk)
        inicio_txt = md.group(1).strip() if md else None
        inicio = parse_date(inicio_txt) if inicio_txt else None
        days = (date.today() - inicio).days if inicio else None

        dests = [urllib.parse.unquote(u) for u in re.findall(r'l\.php\?u=([^"&]+)', blk)]
        dest = dests[0][:250] if dests else None

        # o long-form vive em _4ik4 ou em dir="auto"; pega o maior bloco
        txts = [clean(t) for t in re.findall(r'_4ik4[^>]*>(.*?)</div>', blk, re.S)]
        txts += [clean(t) for t in re.findall(r'dir="auto"[^>]*>(.*?)</div>', blk, re.S)]
        txts = [t for t in txts if len(t) > 60 and "Identifica" not in t]
        body = max(txts, key=len) if txts else ""
        if len(body) < min_chars:
            continue

        # criativo: t39.35426-6 em s600x600 (s60x60 e o avatar do anunciante)
        imgs = [u.replace("&amp;", "&") for u in
                re.findall(r'https://scontent[^\s"\\<>]+t39\.35426-6[^\s"\\<>]+', blk)]
        crea = [u for u in imgs if "s600x600" in u] or [u for u in imgs if "s60x60" not in u]

        out.append({"ad_id": ad_id, "days_active": days, "inicio": inicio_txt,
                    "dest": dest, "text": body, "img_url": crea[0] if crea else None})
    return out


def deduplicar(ads):
    """
    Agrupa por texto e CONTA as repeticoes -> variacoes_ativas.
    Mantem a ordem de chegada (= impressoes desc) e devolve ordenado por aposta.
    """
    grupos = {}
    for a in ads:
        chave = re.sub(r"\s+", " ", a["text"][:300]).strip().lower()
        if chave in grupos:
            g = grupos[chave]
            g["variacoes_ativas"] += 1
            g["ids"].append(a["ad_id"])
            if a["days_active"] and (not g["days_active"] or a["days_active"] > g["days_active"]):
                g["days_active"] = a["days_active"]        # a mais antiga do grupo
        else:
            g = dict(a); g["variacoes_ativas"] = 1; g["ids"] = [a["ad_id"]]
            grupos[chave] = g
    uniq = list(grupos.values())
    uniq.sort(key=lambda x: (-x["variacoes_ativas"], -len(x["text"])))
    return uniq


def baixar_imagem(page, url, destino):
    """fbcdn bloqueia request externo: abre numa aba e le o canvas."""
    import base64
    try:
        tab = page.new_tab(url)
        time.sleep(2.5)
        d = tab.run_js('function(){const i=document.querySelector("img");'
                       'if(!i||!i.naturalWidth)return"";const c=document.createElement("canvas");'
                       'c.width=i.naturalWidth;c.height=i.naturalHeight;'
                       'c.getContext("2d").drawImage(i,0,0);return c.toDataURL("image/jpeg",0.92)}')
        tab.close()
        if d and "," in d:
            raw = base64.b64decode(d.split(",", 1)[1])
            if len(raw) > 4000:
                open(destino, "wb").write(raw)
                return True
    except Exception:
        pass
    return False


def salvar(page, pasta_base, sl, anunciante, ads, brutos, min_chars, com_imagens):
    """Escreve o indice + uma nota por long-form, no formato do /adaptar-longform."""
    pasta_notas = os.path.join(pasta_base, sl)
    os.makedirs(pasta_notas, exist_ok=True)
    hoje = date.today().isoformat()
    tag_base = "benchmarking/" + sl.lower()
    n_img = 0

    for j, a in enumerate(ads, 1):
        tema = detectar_tema(a["text"])
        idioma = detectar_idioma(a["text"])
        titulo = titulo_de(a["text"])
        nome = re.sub(r'[\\/:*?"<>|]', "", titulo)[:70].strip()
        arq = os.path.join(pasta_notas, "%03d - %s.md" % (j, nome))

        img_linha = ""
        if com_imagens and a["img_url"]:
            imgname = "%03d.jpg" % j
            if baixar_imagem(page, a["img_url"], os.path.join(pasta_notas, imgname)):
                img_linha = "![[%s]]\n\n" % imgname
                n_img += 1

        fm = ["---",
              "fonte: Meta Ad Library",
              "anunciante: %s" % anunciante,
              'library_id: "%s"' % a["ad_id"],
              'veiculacao_inicio: "%s"' % (a["inicio"] or ""),
              "caracteres: %d" % len(a["text"]),
              "variacoes_ativas: %d" % a["variacoes_ativas"],
              "tema: %s" % tema,
              "idioma: %s" % idioma,
              "coletado_em: %s" % hoje]
        if a["days_active"]:
            fm.append("dias_ativo: %d" % a["days_active"])
        if a["dest"]:
            fm.append("destino: %s" % a["dest"])
        fm += ["tags:", "  - %s" % tag_base, "  - longform", "  - tema/%s" % tema, "---", ""]

        corpo = ["# %s" % titulo, "",
                 "> [!info] Metadados",
                 "> **%s caracteres** · %d variação(ões) ativa(s) · tema: **%s**"
                 % ("{:,}".format(len(a["text"])).replace(",", "."),
                    a["variacoes_ativas"], tema), ""]
        if a["variacoes_ativas"] > 1:
            corpo += ["> [!tip] Aposta do concorrente",
                      "> Este texto está rodando em **%d cópias simultâneas**. "
                      "Quanto mais cópias, maior a aposta." % a["variacoes_ativas"], ""]
        corpo += [img_linha + "---", "", a["text"], ""]
        open(arq, "w", encoding="utf-8").write("\n".join(fm + corpo))

    # ---------------- indice
    temas = Counter(detectar_tema(a["text"]) for a in ads)
    com_var = [a for a in ads if a["variacoes_ativas"] > 1]
    idx = ["---", "tags:", "  - %s" % tag_base, "  - indice",
           "coletado_em: %s" % hoje, "---", "",
           "# %s — Long-forms %s" % (sl, anunciante), "",
           "Raspagem da **Meta Ad Library** (`%s`, ordenado por impressões)." % anunciante, "",
           "> [!abstract] Resumo da coleta",
           "> **%d** anúncios ativos carregados · **%d** com %s+ caracteres · "
           "**%d** long-forms únicos após deduplicação."
           % (brutos, sum(1 for a in ads for _ in range(a["variacoes_ativas"])),
              "{:,}".format(min_chars).replace(",", "."), len(ads)),
           "> Coletado em %s." % hoje, ""]

    if com_var:
        idx += ["## 🎯 Maiores apostas (mais cópias rodando)", "",
                "| # | Peça | Cópias | Caracteres | Tema |", "|---|---|---|---|---|"]
        for j, a in enumerate(ads[:15], 1):
            if a["variacoes_ativas"] < 2:
                break
            t = titulo_de(a["text"])
            idx.append("| %d | [[%03d - %s]] | **%d** | %s | %s |"
                       % (j, j, re.sub(r'[\\/:*?"<>|]', "", t)[:70].strip(),
                          a["variacoes_ativas"],
                          "{:,}".format(len(a["text"])).replace(",", "."),
                          detectar_tema(a["text"])))
        idx.append("")

    idx += ["## Por tema", ""]
    for t, n in temas.most_common():
        idx.append("- **%s** — %d peças" % (t, n))
    idx += ["", "## Todas as peças", "",
            "| # | Peça | Cópias | Chars | Tema | Idioma |", "|---|---|---|---|---|---|"]
    for j, a in enumerate(ads, 1):
        t = re.sub(r'[\\/:*?"<>|]', "", titulo_de(a["text"]))[:70].strip()
        idx.append("| %d | [[%03d - %s]] | %d | %s | %s | %s |"
                   % (j, j, t, a["variacoes_ativas"],
                      "{:,}".format(len(a["text"])).replace(",", "."),
                      detectar_tema(a["text"]), detectar_idioma(a["text"])))
    open(os.path.join(pasta_base, sl + ".md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    return n_img


def main():
    ap = argparse.ArgumentParser(description="Raspa long-forms da Meta Ad Library")
    ap.add_argument("modo", choices=["dominio", "termo"])
    ap.add_argument("alvo", help="o dominio (frase exata) ou o termo de busca")
    ap.add_argument("--min", type=int, default=10000, help="piso de caracteres (default 10000)")
    ap.add_argument("--max", type=int, default=0, help="teto de pecas salvas (0 = sem teto)")
    ap.add_argument("--scroll", type=int, default=25, help="passos de scroll (default 25)")
    ap.add_argument("--produto", default="Magnésio", help="pasta do produto no vault")
    ap.add_argument("--saida", default="", help="nome do indice/pasta (default: LF + iniciais)")
    ap.add_argument("--sem-imagens", action="store_true")
    ap.add_argument("--vault", default="", help="caminho do vault (senao acha sozinho)")
    a = ap.parse_args()

    vault = a.vault or achar_vault()
    if not vault:
        print("ERRO: nao achei o vault. Rode com --vault /caminho ou SANO_VAULT=/caminho")
        sys.exit(1)

    anunciante = a.alvo
    sl = a.saida or ("LF" + "".join(w[0] for w in re.split(r"[^a-z0-9]+", a.alvo.lower()) if w)[:6].upper())
    pasta_base = os.path.join(vault, "Produtos", a.produto, "Benchmarking", slug(a.alvo))
    os.makedirs(pasta_base, exist_ok=True)

    print("vault:      " + vault)
    print("saida:      " + pasta_base)
    print("busca:      %s = %s" % (a.modo, a.alvo))
    print("filtro:     >= %d caracteres\n" % a.min)

    try:
        from DrissionPage import ChromiumPage, ChromiumOptions
    except ImportError:
        print("ERRO: falta o DrissionPage.  pip install DrissionPage")
        sys.exit(1)

    co = ChromiumOptions()
    chrome = detectar_chrome()
    if chrome:
        co.set_browser_path(chrome)
        print("chrome:     " + chrome)
    co.set_argument("--lang=pt-BR")
    co.set_argument("--window-size=1400,2000")
    page = ChromiumPage(co)

    try:
        print("\n[1/4] carregando a Ad Library (isso demora, tem muito scroll)...")
        html = coletar(page, montar_url(a.modo, a.alvo), a.scroll)

        print("[2/4] extraindo os long-forms...")
        ads = extrair(html, a.min)
        brutos = len(re.findall("Identifica[cç][aã]o da biblioteca", html))
        print("      %d anuncios carregados, %d com %d+ chars" % (brutos, len(ads), a.min))
        if not ads:
            print("\nNenhum long-form encontrado. Tente --min menor ou --scroll maior.")
            return

        print("[3/4] deduplicando e contando variacoes...")
        uniq = deduplicar(ads)
        if a.max:
            uniq = uniq[:a.max]
        multi = sum(1 for x in uniq if x["variacoes_ativas"] > 1)
        topo = uniq[0]["variacoes_ativas"] if uniq else 0
        print("      %d unicos | %d com copias | maior aposta: %dx" % (len(uniq), multi, topo))

        print("[4/4] escrevendo as notas...")
        n_img = salvar(page, pasta_base, sl, anunciante, uniq, brutos, a.min, not a.sem_imagens)
        print("\nOK: %d notas + indice %s.md" % (len(uniq), sl))
        if n_img:
            print("    %d criativos baixados" % n_img)
        print("    " + pasta_base)
    finally:
        try:
            page.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
