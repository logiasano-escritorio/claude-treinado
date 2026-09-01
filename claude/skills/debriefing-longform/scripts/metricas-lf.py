# -*- coding: utf-8 -*-
"""
metricas-lf.py — extrator de métricas estruturais de long-form.

Uso:
    python metricas-lf.py arquivo.txt
    python metricas-lf.py a.txt b.txt          # comparativo lado a lado

Cospe as métricas objetivas que separam long-form campeão de long-form que
cansa no meio. Benchmarks derivados de LF08 (ROAS 2,38 · US$10.550 · 456 vendas)
vs LF02 (ROAS 2,01) — Sano Magnésio, ago/2026.

Não julga conteúdo. Só mede o que dá pra medir.
"""
import sys, io, re, os

# Faixas-alvo derivadas do campeão. (min, max, "por quê")
BENCH = {
    'chars':        (11000, 14000, 'long-form de ad; abaixo de 11k nao da pro arco completo'),
    'palavras_par': (13.0,  18.0,  'densidade de paragrafo = variavel de fadiga'),
    'pct_curtos':   (40.0,  55.0,  'linha curta e o que faz rolar no feed'),
    'falas':        (28,    999,   'dialogo reinicia atencao sem exigir info nova'),
    'num_por_1k':   (0,     9.0,   'numero demais le como bula e dilui credibilidade'),
    'paragrafos':   (110,   999,   'mais quebras = mais respiro'),
}


def medir(caminho):
    s = io.open(caminho, encoding='utf-8').read()
    paras = [p for p in s.split('\n') if p.strip()]
    palavras = len(s.split())
    curtos = sum(1 for p in paras if len(p) < 60)
    # normaliza aspas curvas antes de contar, senao o mesmo trecho conta 2x
    norm = s.replace('“', '"').replace('”', '"')
    falas = len(re.findall(r'"[^"]{10,}"', norm))
    numeros = len(re.findall(r'\b\d+\b', s))
    return {
        'arquivo': os.path.basename(caminho),
        'chars': len(s),
        'palavras': palavras,
        'paragrafos': len(paras),
        'palavras_par': round(palavras / len(paras), 1) if paras else 0,
        'pct_curtos': round(100.0 * curtos / len(paras), 1) if paras else 0,
        'falas': falas,
        'perguntas': s.count('?'),
        'numeros': numeros,
        'num_por_1k': round(1000.0 * numeros / palavras, 1) if palavras else 0,
    }


def veredito(chave, valor):
    if chave not in BENCH:
        return ''
    lo, hi, _ = BENCH[chave]
    if valor < lo:
        return 'ABAIXO'
    if valor > hi:
        return 'ACIMA'
    return 'ok'


LABELS = [
    ('chars',        'Caracteres'),
    ('palavras',     'Palavras'),
    ('paragrafos',   'Paragrafos'),
    ('palavras_par', 'Palavras/paragrafo'),
    ('pct_curtos',   '% linhas curtas (<60ch)'),
    ('falas',        'Falas em dialogo'),
    ('perguntas',    'Perguntas'),
    ('numeros',      'Numeros no corpo'),
    ('num_por_1k',   'Numeros por 1000 palavras'),
]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    res = [medir(p) for p in sys.argv[1:]]

    largura = 30 + 16 * len(res)
    print('=' * largura)
    print('METRICAS ESTRUTURAIS DE LONG-FORM')
    print('=' * largura)
    cab = ' ' * 30 + ''.join(f"{r['arquivo'][:14]:>16}" for r in res)
    print(cab)
    print('-' * largura)
    for chave, label in LABELS:
        linha = f'{label:<30}'
        for r in res:
            linha += f"{r[chave]:>16}"
        print(linha)

    print()
    print('=' * largura)
    print('CONTRA O BENCHMARK DO CAMPEAO (LF08 · ROAS 2,38)')
    print('=' * largura)
    for r in res:
        print(f"\n### {r['arquivo']}")
        for chave, label in LABELS:
            if chave not in BENCH:
                continue
            lo, hi, motivo = BENCH[chave]
            v = veredito(chave, r[chave])
            marca = {'ok': '[ok]  ', 'ABAIXO': '[BAIXO]', 'ACIMA': '[ALTO] '}[v]
            alvo = f'{lo}-{hi}' if hi < 999 else f'>={lo}'
            print(f'  {marca} {label:<28} {r[chave]:>8}   alvo {alvo}')
            if v != 'ok':
                print(f'          -> {motivo}')

    print()
    print('Lembrete: isto mede FORMA, nao CONTEUDO. Um texto dentro de todas as')
    print('faixas ainda pode ser repetitivo ou nao fazer sentido — para isso, rode')
    print('a grade de debriefing (SKILL.md, PASSO 3).')


if __name__ == '__main__':
    main()
