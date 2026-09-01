# -*- coding: utf-8 -*-
"""
Valida um texto adaptado contra o corpus de portugues organico brasileiro.

USO:
  python analise-portugues.py <arquivo.txt>

Mede: palavras/frase, marcadores orais, decalques do ingles, inicios de frase.
Corpus: corpus-fb.txt (5.049 palavras de comentarios espontaneos do Facebook BR)

LEMBRE: o ritmo picotado do long-form (7-9 palavras/frase) esta CERTO.
O corpus e de comentario curto; serve pra medir VOCABULARIO e CONSTRUCAO,
nao pra "corrigir" o ritmo pra frase longa.
"""
import io, os, re, sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(AQUI, "corpus-fb.txt")


def palavras(t):
    return re.findall(r"[a-zA-ZáàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ']+", t)


def frases(t):
    t = re.sub(r'\s+', ' ', t)
    return [f.strip() for f in re.split(r'(?<=[.!?])\s+', t) if len(f.strip()) > 3]


def safe(x):
    return x.encode('ascii', 'replace').decode('ascii')


# ---------------------------------------------------------------- decalques
DECALQUES = {
    "para viver (for a living)":        r'\bpara viver\b',
    "me sentou (sat me down)":          r'\bme sent(ou|ei)\b',
    "caixa de ferramentas (toolbox)":   r'caixa de ferramenta',
    "fina no meio":                      r'fin[ao] no meio',
    "sai do lugar (goes wrong)":         r'qu[íi]mica.{0,20}sai do lugar',
    "encostar naquilo (touch it)":       r'encostar naquilo',
    "tocar o alarme (sounding)":         r'tocar o alarme',
    "pro outro lado (other side)":       r'pro outro lado',
    "do que ninguem (than anyone)":      r'do que ningu[ée]m',
    "jeito dificil (the hard way)":      r'jeito dif[íi]cil',
    "N anos atras (N years ago)":        r'\b(dois|tr[êe]s|quatro|cinco|seis|sete|oito|nove|dez|\d+)\s+anos atr[áa]s',
    "coma o que comer":                  r'coma o que comer',
    "se trate (subjuntivo empolado)":    r'\bse trate\b',
    "devolvemos (deve ser 3a pessoa)":   r'\bdevolvemos\b',
    "prescreveu / protocolo":            r'\bprescrev|\bprotocolo\b',
    "Eu tenho X anos (abertura)":        r'^Eu tenho \d+ anos',
}

METAS = {
    "aspas":       (r'"',  8.0, "<= 8 por 1000. Acima disso, converter fala em discurso indireto"),
    "dois-pontos": (r':',  2.0, "<= 2 por 1000. Quase inexistente no organico"),
    "pro":         (r'\bpro\b', 1.0, "'pra' e 20x mais comum que 'pro'"),
}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    arq = sys.argv[1]
    if not os.path.exists(arq):
        print(f"nao encontrei: {arq}")
        sys.exit(1)

    t = io.open(arq, encoding='utf-8').read()
    p = palavras(t)
    fs = frases(t)
    comp = [len(palavras(f)) for f in fs]
    n = len(p)

    print("=" * 62)
    print(f"  {os.path.basename(arq)}")
    print("=" * 62)
    print(f"  caracteres: {len(t):,}".replace(",", "."))
    print(f"  palavras:   {n}")
    print(f"  frases:     {len(fs)}")
    print(f"  palavras/frase: media {sum(comp)/len(comp):.1f} | mediana {sorted(comp)[len(comp)//2]}")
    print(f"    -> meta long-form: 7 a 9  (frase curta esta CERTA aqui)")

    # ------------------------------------------------------- bloqueadoras
    print("\n--- REGRAS BLOQUEADORAS ---")
    bullets = len(re.findall(r'[•✅✔️★▪]|^\s*[-*]\s', t, re.M))
    negrito = t.count('**')
    print(f"  N2  bullets/icones/negrito : {bullets + negrito}  {'OK' if bullets+negrito == 0 else '<<< FALHOU'}")

    i = t.lower().find('você')
    pct = (i / len(t) * 100) if i >= 0 else 100
    print(f"  N8  1o 'voce' em           : {pct:.1f}%  {'OK' if pct >= 78 else '<<< checar (fala de personagem nao conta)'}")

    dev = len(re.findall(r'\bdevolvemos\b', t))
    print(f"  N28 garantia 3a pessoa     : {'OK' if dev == 0 else '<<< FALHOU: usa devolvemos'}")

    # ------------------------------------------------------- marcadores
    print("\n--- MARCADORES (por 1.000 palavras) ---")
    for nome, (pat, meta, obs) in METAS.items():
        v = len(re.findall(pat, t)) / n * 1000
        flag = "OK " if v <= meta else "<<<"
        print(f"  {flag} {nome:14} {v:6.1f}   {obs}")

    excl = len(re.findall(r'!', t))
    print(f"  {'OK ' if excl >= 1 else '<<<'} exclamacoes    {excl:6}   1 ou 2 no texto todo. Zero soa frio")

    # ------------------------------------------------------- decalques
    print("\n--- DECALQUES DO INGLES ---")
    achou = False
    for nome, pat in DECALQUES.items():
        m = re.findall(pat, t, re.I | re.M)
        if m:
            print(f"  <<< {nome}  ->  {safe(str(m[:3]))}")
            achou = True
    if not achou:
        print("  nenhum encontrado. OK")

    # ------------------------------------------------------- inicios
    print("\n--- COMO COMECAM AS FRASES (top 12) ---")
    c = Counter(palavras(f)[0].lower() for f in fs if palavras(f))
    print("  " + safe(", ".join(f"{w}({q})" for w, q in c.most_common(12))))
    print("  -> no organico o topo e: eu, e, o, a, mas")
    print("     se o topo for 'o'/'ele', a narracao esta em 3a pessoa, distante")

    # ------------------------------------------------------- corpus
    if os.path.exists(CORPUS):
        fb = io.open(CORPUS, encoding='utf-8').read()
        pfb = palavras(fb)
        print("\n--- COMPARACAO COM O CORPUS ORGANICO ---")
        print(f"  {'marcador':<16}{'facebook':>10}{'este texto':>12}")
        for nome, pat in [("mas", r'\bmas\b'), ("se", r'\bse\b'), ("muito", r'\bmuito\b'),
                          ("ja", r'\bj[áa]\b'), ("so", r'\bs[óo]\b'), ("pra", r'\bpra\b'),
                          ("aspas", r'"'), ("reticencias", r'\.\.\.')]:
            a = len(re.findall(pat, fb, re.I)) / len(pfb) * 1000
            b = len(re.findall(pat, t, re.I)) / n * 1000
            print(f"  {nome:<16}{a:10.1f}{b:12.1f}")

    print()


if __name__ == "__main__":
    main()
