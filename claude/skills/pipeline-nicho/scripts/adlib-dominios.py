# -*- coding: utf-8 -*-
"""
Extrai DOMÍNIOS de e-commerce de anúncios campeões (+30d) da Meta Ad Library.
Nicho melasma/hiperpigmentação/manchas — MERCADO GRINGO (US/GB/DE/ES).
Interface pt-BR forçada (rótulos "Veiculação iniciada em") + country do mercado alvo.
Matriz de termos por ÂNGULO × IDIOMA (fornecida pelo Guilherme).

Uso: python adlib-dominios.py
Saída: _dev/adlib-out/dominios_melasma_gringo.json + .txt (com ângulo/mercado/dias)
"""
import json, os, time, re, urllib.parse
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "adlib-out"); os.makedirs(OUTDIR, exist_ok=True)
MIN_DAYS = 30
MAX_SCROLL = 16

# (país, termo, ângulo) — interface sempre pt-BR
JOBS = []
def add(country, angle, terms): [JOBS.append((country, t, angle)) for t in terms]

# 1. MELASMA / HIPERPIGMENTAÇÃO
add("US","melasma", ["melasma treatment","dark spots face","hyperpigmentation serum","skin brightening","even skin tone","tranexamic acid serum"])
add("DE","melasma", ["Melasma behandeln","Pigmentflecken Gesicht","Hyperpigmentierung Serum","Hautaufhellung","tranexamsäure serum"])
add("ES","melasma", ["tratamiento melasma","manchas oscuras cara","hiperpigmentación serum","aclarar la piel","ácido tranexámico"])
# 2. MANCHAS DE SOL / IDADE (45+)
add("US","sol-idade", ["age spots","sun spots remover","liver spots","dark spot corrector"])
add("DE","sol-idade", ["Altersflecken","Sonnenflecken entfernen","Pigmentflecken Alter"])
add("ES","sol-idade", ["manchas de la edad","manchas del sol","corrector de manchas"])
# 3. MANCHA DE ACNE
add("US","acne", ["acne scars dark spots","post acne marks","PIH treatment"])
add("DE","acne", ["Aknenarben Flecken","Pickelmale entfernen","Aknemale"])
add("ES","acne", ["manchas de acné","marcas de acné","manchas post acné"])
# 4. MELASMA DA GRAVIDEZ
add("US","gravidez", ["pregnancy melasma","pregnancy mask face","chloasma"])
add("DE","gravidez", ["Schwangerschaftsmaske","Melasma Schwangerschaft"])
add("ES","gravidez", ["melasma embarazo","paño del embarazo","cloasma"])
# 5. POROS / TEXTURA
add("US","poros", ["glass skin serum","pore minimizer","niacinamide serum"])
add("DE","poros", ["Poren verkleinern","glass skin","Niacinamid Serum"])
add("ES","poros", ["poros dilatados","piel de cristal","niacinamida serum"])

MESES = {"jan":1,"fev":2,"mar":3,"abr":4,"mai":5,"jun":6,"jul":7,"ago":8,"set":9,"out":10,"nov":11,"dez":12}
SKIP_DOM = re.compile(r'(instagram\.com|fb\.me|facebook\.com|wa\.me|api\.whatsapp|whatsapp\.com|'
                      r'linktr\.ee|t\.me|youtu|messenger\.com|threads\.net|tiktok\.com|linktree)', re.I)

def parse_date(s):
    m = re.search(r"(\d{1,2})\s+de\s+(\w{3})\w*\s+de\s+(20\d\d)", s, re.I)
    if not m: return None
    try: return date(int(m.group(3)), MESES.get(m.group(2).lower()[:3],0), int(m.group(1)))
    except: return None

def domain_of(url):
    try:
        h = urllib.parse.urlparse(url if "//" in url else "http://"+url).netloc.lower()
        return h[4:] if h.startswith("www.") else h
    except: return None

def scrape(page, country, term, angle):
    url = ("https://www.facebook.com/ads/library/?active_status=active&ad_type=all"
           f"&country={country}&media_type=image&q={urllib.parse.quote(term)}&search_type=keyword_unordered")
    page.get(url); time.sleep(5)
    last = 0
    for s in range(MAX_SCROLL):
        page.scroll.to_bottom(); time.sleep(1.7)
        n = len(re.findall("Identifica[cç][aã]o da biblioteca", page.html))
        if n == last and s > 2: break
        last = n
    html = page.html
    idxs = [m.start() for m in re.finditer("Identifica[cç][aã]o da biblioteca", html)]
    out = []
    for k, i in enumerate(idxs):
        end = idxs[k+1] if k+1 < len(idxs) else min(i+9000, len(html))
        blk = html[i:end]
        md = re.search(r"[Vv]eicula[cç][aã]o iniciada em ([^<]+)", blk)
        start = parse_date(md.group(1)) if md else None
        days = (date.today() - start).days if start else None
        if not days or days < MIN_DAYS: continue
        dests = [urllib.parse.unquote(u) for u in re.findall(r'l\.php\?u=([^"&]+)', blk)]
        for d in [x for x in dests if not SKIP_DOM.search(x)]:
            dom = domain_of(d)
            if dom and "." in dom:
                out.append({"domain": dom, "days_active": days, "market": country,
                            "angle": angle, "term": term})
    print(f"    [{country}/{angle}] {term:<28} {len(idxs):>2} ads -> {len(out)} campeões")
    return out

def main():
    from DrissionPage import ChromiumPage, ChromiumOptions
    co = ChromiumOptions(); co.set_argument("--lang=pt-BR"); co.set_argument("--window-size=1400,1900")
    page = ChromiumPage(co)
    allrows = []
    for country, term, angle in JOBS:
        try: allrows += scrape(page, country, term, angle)
        except Exception as e: print("    erro:", country, term, e)
    page.quit()
    # dedup por domínio: guarda maior days_active, junta ângulos/mercados
    best = {}
    for r in allrows:
        d = r["domain"]
        if d not in best:
            best[d] = {**r, "angles": {r["angle"]}, "markets": {r["market"]}}
        else:
            best[d]["angles"].add(r["angle"]); best[d]["markets"].add(r["market"])
            if r["days_active"] > best[d]["days_active"]: best[d]["days_active"] = r["days_active"]
    rows = sorted(best.values(), key=lambda x: -x["days_active"])
    out = [{"domain":r["domain"],"days_active":r["days_active"],
            "markets":sorted(r["markets"]),"angles":sorted(r["angles"]),"term":r["term"]} for r in rows]
    json.dump(out, open(os.path.join(OUTDIR,"dominios_melasma_gringo.json"),"w",encoding="utf-8"),
              ensure_ascii=False, indent=2)
    with open(os.path.join(OUTDIR,"dominios_melasma_gringo.txt"),"w",encoding="utf-8") as f:
        f.write(f"# {len(out)} domínios ÚNICOS de campeões (+{MIN_DAYS}d) — melasma/manchas gringo\n\n")
        for r in out:
            f.write(f"{r['days_active']:>4}d  [{'+'.join(r['markets'])}]  {r['domain']:<34} "
                    f"{'|'.join(r['angles'])}\n")
    print(f"\n=== {len(out)} domínios ÚNICOS de campeões gringos (+{MIN_DAYS}d) ===")
    for r in out[:50]:
        print(f"  {r['days_active']:>4}d  [{'+'.join(r['markets'])}]  {r['domain']:<32} {'|'.join(r['angles'])}")

if __name__ == "__main__":
    main()
