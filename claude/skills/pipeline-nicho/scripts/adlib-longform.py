# -*- coding: utf-8 -*-
"""
Raspa LONG-FORM + IMAGENS dos ads de domínios concorrentes na Meta Ad Library.
Busca por frase exata do domínio, country=ALL, ordenado por impressões.
Só ads com texto long-form (>=500 chars). Baixa a imagem do criativo (t39.35426-6).
Salva no Obsidian: Research/AdLibrary-Concorrentes/<dominio>/ (md + imgs).

Uso: python adlib-longform.py
"""
import json, os, time, re, html as ihtml, urllib.parse, urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = r"C:\Users\user\Desktop\SANOLOGIA OBSIDIAN\Research\AdLibrary-Concorrentes"
os.makedirs(VAULT, exist_ok=True)
MIN_LONGFORM = 500   # chars mínimos pra contar como long-form
MAX_SCROLL = 22
MAX_PER_DOMAIN = 20  # top N long-forms por domínio (ordenados por impressões)

DOMINIOS = [
    "try.shopeverly.shop", "selie.store", "Felineskinscience.com",
    "bienestaryculturacol.com", "puredoseskin.com", "try.feline-skinscience.com",
    "tonoperfecto.com", "Balanze.life", "trytonebright.com",
]

MESES = {"jan":1,"fev":2,"mar":3,"abr":4,"mai":5,"jun":6,"jul":7,"ago":8,"set":9,"out":10,"nov":11,"dez":12}

def parse_date(s):
    m = re.search(r"(\d{1,2})\s+de\s+(\w{3})\w*\s+de\s+(20\d\d)", s, re.I)
    if not m: return None
    try: return date(int(m.group(3)), MESES.get(m.group(2).lower()[:3],0), int(m.group(1)))
    except: return None

def clean(t):
    t=re.sub(r"<br\s*/?>","\n",t); t=re.sub(r"<[^>]+>"," ",t)
    t=ihtml.unescape(t); return re.sub(r"[ \t]+"," ",t).strip()

def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")

def dl_image_browser(page, url, path):
    """Baixa o criativo abrindo em nova aba e lendo o canvas (fbcdn bloqueia externo)."""
    import base64
    try:
        tab=page.new_tab(url); time.sleep(2.5)
        d=tab.run_js('function(){const i=document.querySelector("img");'
                     'if(!i||!i.naturalWidth)return"";const c=document.createElement("canvas");'
                     'c.width=i.naturalWidth;c.height=i.naturalHeight;'
                     'c.getContext("2d").drawImage(i,0,0);return c.toDataURL("image/jpeg",0.92)}')
        tab.close()
        if d and "," in d:
            raw=base64.b64decode(d.split(",",1)[1])
            if len(raw)>4000:
                open(path,"wb").write(raw); return True
    except Exception: pass
    return False

def scrape_domain(page, dominio):
    url=('https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL'
         '&is_targeted_country=false&media_type=all'
         f'&q=%22{urllib.parse.quote(dominio)}%22'
         '&search_type=keyword_exact_phrase&sort_data[direction]=desc&sort_data[mode]=total_impressions')
    page.get(url); time.sleep(6)
    # scroll em passos, clicando TODOS os "Ver mais" (senão o long-form vem truncado)
    last=0; total_click=0
    for s in range(MAX_SCROLL*2):
        for b in page.eles('text:Ver mais', timeout=0.4):
            try: b.click(by_js=True); total_click+=1
            except: pass
        page.scroll.down(1400); time.sleep(1.0)
        n=len(re.findall("Identifica[cç][aã]o da biblioteca", page.html))
        if n==last and s>6: break
        last=n
    # passadas finais de clique (revelam os últimos)
    for _ in range(3):
        for b in page.eles('text:Ver mais', timeout=0.4):
            try: b.click(by_js=True); total_click+=1
            except: pass
        time.sleep(1)
    print(f"      ({total_click} cliques Ver mais, {last} cards)")
    html=page.html
    idxs=[m.start() for m in re.finditer("Identifica[cç][aã]o da biblioteca", html)]
    out=[]
    for k,i in enumerate(idxs):
        end=idxs[k+1] if k+1<len(idxs) else min(i+12000,len(html))
        blk=html[i:end]
        mid=re.search(r"biblioteca:\s*(?:</?\w+>\s*)*(\d{6,})", blk)
        ad_id=mid.group(1) if mid else f"idx{k}"
        md=re.search(r"[Vv]eicula[cç][aã]o iniciada em ([^<]+)", blk)
        start=parse_date(md.group(1)) if md else None
        days=(date.today()-start).days if start else None
        dests=[urllib.parse.unquote(u) for u in re.findall(r'l\.php\?u=([^"&]+)', blk)]
        dest=dests[0][:250] if dests else None
        # texto: pega o maior bloco (long-form vive em _4ik4 ou dir=auto)
        txts=[clean(t) for t in re.findall(r'_4ik4[^>]*>(.*?)</div>', blk, re.S)]
        txts+=[clean(t) for t in re.findall(r'dir="auto"[^>]*>(.*?)</div>', blk, re.S)]
        txts=[t for t in txts if len(t)>60 and "Identifica" not in t]
        body=max(txts,key=len) if txts else ""
        if len(body) < MIN_LONGFORM:   # SÓ long-form
            continue
        # imagem do criativo: t39.35426-6 com s600x600 (s60x60 é avatar do anunciante)
        imgs=[u.replace("&amp;","&") for u in re.findall(r'https://scontent[^\s"\\<>]+t39\.35426-6[^\s"\\<>]+', blk)]
        crea=[u for u in imgs if 's600x600' in u] or [u for u in imgs if 's60x60' not in u]
        img=crea[0] if crea else None
        out.append({"ad_id":ad_id,"days_active":days,"dest":dest,"text":body,"img_url":img})
    # dedup por texto (mantém ordem = impressões desc)
    seen,uniq={},[]
    for a in out:
        k=a["text"][:150]
        if k not in seen: seen[k]=1; uniq.append(a)
    return uniq[:MAX_PER_DOMAIN]

def save(page, dominio, ads):
    d=slug(dominio); folder=os.path.join(VAULT,d)
    os.makedirs(folder, exist_ok=True)
    md=[f"# {dominio} — Long-forms (Ad Library)\n",
        f"_{len(ads)} long-forms (>{MIN_LONGFORM} chars). Ordenado por impressões. {date.today().isoformat()}_\n"]
    n_img=0
    for j,a in enumerate(ads,1):
        imgfile=""
        if a["img_url"]:
            imgname=f"{d}-{j:02d}.jpg"
            if dl_image_browser(page, a["img_url"], os.path.join(folder,imgname)):
                imgfile=imgname; n_img+=1
        md.append(f"\n---\n\n## #{j}"
                  + (f" · {a['days_active']}d ativo" if a['days_active'] else "")
                  + (f" · [destino]({a['dest']})" if a['dest'] else "") + "\n")
        if imgfile: md.append(f"![[{imgfile}]]\n")
        md.append(a["text"]+"\n")
    open(os.path.join(folder,f"{d}.md"),"w",encoding="utf-8").write("\n".join(md))
    return len(ads), n_img

def main():
    from DrissionPage import ChromiumPage, ChromiumOptions
    co=ChromiumOptions(); co.set_argument("--lang=pt-BR"); co.set_argument("--window-size=1400,2000")
    page=ChromiumPage(co)
    resumo=[]
    for dom in DOMINIOS:
        try:
            ads=scrape_domain(page,dom)
            n,ni=save(page,dom,ads)
            print(f"[OK] {dom:<32} {n} long-forms, {ni} imgs")
            resumo.append((dom,n,ni))
        except Exception as e:
            print(f"[ERR] {dom}: {str(e)[:120]}")
            resumo.append((dom,0,0))
    page.quit()
    print("\n=== RESUMO ===")
    for dom,n,ni in resumo: print(f"  {dom:<32} {n} textos / {ni} imgs")
    print(f"\nSalvo em: {VAULT}")

if __name__=="__main__": main()
