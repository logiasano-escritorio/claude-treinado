---
name: raspar-adlibrary
description: Raspa a Meta Ad Library pública (sem token, sem login, via DrissionPage) e transforma os long-forms de um concorrente em notas no Obsidian, com o campo variacoes_ativas — quantas cópias do mesmo texto estão rodando ao mesmo tempo, que é o proxy de aposta do concorrente. Produz exatamente o formato que o /adaptar-longform consome na Etapa 1. Trigger /raspar-adlibrary
---

# /raspar-adlibrary

Raspa os anúncios ativos de um concorrente na Meta Ad Library e escreve, no vault, o índice + uma nota por long-form único — com a contagem de cópias que diz onde ele está apostando.

**É a etapa anterior ao `/adaptar-longform`.** Um alimenta o outro: aqui você descobre o que o concorrente está bancando; lá você adapta.

---

## QUANDO USAR

- User digitou `/raspar-adlibrary`
- "rapa a ad library do <concorrente>", "vê o que o <domínio> está rodando"
- Antes de adaptar qualquer peça de um concorrente que ainda não foi mapeado

## INPUT

**Obrigatório:** o alvo. Duas formas:

- **domínio** — busca por frase exata. Melhor quando você sabe quem é: `spnutrition-us.com`
- **termo** — busca livre pelo nicho, pega vários anunciantes: `"magnésio glicina"`

**Perguntar antes de rodar, se não veio no pedido:**

1. **Domínio ou termo?**
2. **Produto** — em qual pasta do vault salvar (default `Magnésio`)
3. **Piso de caracteres** — default 10.000 (só long-form de verdade). Baixar pra 500 pega anúncio curto também

Não trave: se o user já disse o alvo, rode com os defaults.

---

## COMO RODAR

```bash
python scripts/adlib.py dominio spnutrition-us.com
python scripts/adlib.py termo "magnesio glicina" --min 500
```

| Flag | Pra quê |
|---|---|
| `--min N` | Piso de caracteres. Default 10000 |
| `--max N` | Teto de peças salvas. Default 0 = sem teto |
| `--scroll N` | Passos de scroll. Default 25. Mais scroll = mais anúncios = mais lento |
| `--produto X` | Pasta do produto no vault. Default `Magnésio` |
| `--saida X` | Nome do índice e da pasta. Default: `LF` + iniciais do alvo |
| `--sem-imagens` | Pula o download dos criativos (bem mais rápido) |
| `--vault X` | Caminho do vault, se a detecção falhar |

**Demora.** Uma coleta de 1.000+ anúncios leva 15-30 min: o script precisa scrollar e clicar em cada "Ver mais" pra revelar o texto completo. Avise o user antes de começar.

**Pré-requisito:** `pip install DrissionPage`. Abre um Chrome real — não feche a janela enquanto roda.

---

## O QUE ELE PRODUZ

```
Produtos/<Produto>/Benchmarking/<anunciante>/
    LF1SP.md                    índice: resumo, apostas, temas, tabela completa
    LF1SP/
        001 - Titulo da peça.md
        002 - Outra peça.md
        001.jpg                 criativo, quando existe
```

Cada nota tem o frontmatter que o `/adaptar-longform` lê:

```yaml
fonte: Meta Ad Library
anunciante: spnutrition-us.com
library_id: "1741035347069371"
veiculacao_inicio: "7 de jul de 2026"
caracteres: 32790
variacoes_ativas: 1
tema: sono
idioma: en
```

---

## O CAMPO QUE IMPORTA — `variacoes_ativas`

**Quantas cópias do mesmo texto estão rodando ao mesmo tempo.**

É o proxy mais honesto de aposta: ninguém paga pra replicar 23 vezes um anúncio que não converte. O script agrupa por texto e **conta** as repetições, em vez de descartar as duplicatas — e ordena a saída por essa contagem, então a peça no topo do índice é a maior aposta do concorrente.

O índice ganha uma seção `🎯 Maiores apostas` quando há peças replicadas. Se todas vierem com `variacoes_ativas: 1`, é sinal de que o concorrente está pulverizando — e aí o critério de escolha passa a ser `caracteres` e `tema`.

---

## COMO O SCRAPE FUNCIONA (pra depurar quando quebrar)

Sem token, sem API, sem login. Abre a Ad Library pública num Chrome de verdade e lê o HTML.

1. **URL de busca** — `active_status=active`, `country=ALL`, ordenado por `total_impressions`. Domínio vai como `search_type=keyword_exact_phrase`; termo como `keyword_unordered`
2. **Scroll + "Ver mais"** — o passo que quase todo mundo erra. Sem clicar em todos os "Ver mais", o texto vem **truncado** e o long-form se perde. O script clica a cada scroll e faz 3 passadas finais
3. **Fatiar por card** — usa `"Identificação da biblioteca"` como divisor. O texto vive em `_4ik4` ou `dir="auto"`; pega o maior bloco do card
4. **Criativo** — `t39.35426-6` em `s600x600` (o `s60x60` é o avatar do anunciante, não o criativo)
5. **Download da imagem** — o fbcdn **bloqueia requisição externa**. A saída é abrir a URL numa aba, desenhar num `<canvas>` e ler o dataURL. É por isso que o download é lento
6. **Dedup contando** — agrupa pelos 300 primeiros chars normalizados, soma as cópias, guarda a veiculação mais antiga do grupo

### Quando quebrar

O Facebook muda o HTML sem avisar. Sinais e o que olhar:

| Sintoma | Provável causa |
|---|---|
| 0 anúncios carregados | Mudou o texto `Identificação da biblioteca` (idioma da interface?) ou pediu login |
| Textos truncados | Os "Ver mais" não estão sendo clicados — conferir o seletor `text:Ver mais` |
| Nenhum long-form | O texto migrou de `_4ik4`/`dir="auto"` pra outra classe |
| Imagens não baixam | Mudou o padrão `t39.35426-6` |
| Poucos anúncios | Aumentar `--scroll` |

---

## DEPOIS DE RASPAR

1. Abrir o índice e olhar as **maiores apostas**
2. Ler a peça do topo inteira antes de decidir
3. Chamar `/adaptar-longform` apontando pra ela

> [!warning] Conteúdo de terceiros
> O que é raspado é **material de concorrente, para estudo**. Serve pra entender a arquitetura da peça — nunca pra copiar texto. A adaptação troca mecanismo, marca e mercado; o que se reaproveita é o esqueleto.

---

## O QUE NUNCA FAZER

1. **Rodar sem avisar que demora.** 15-30 min com o Chrome aberto
2. **Aumentar o scroll "por garantia".** Cada passo é ~1s + cliques; 25 já pega a maioria
3. **Descartar duplicatas.** É exatamente o dado mais valioso — a repetição É o sinal
4. **Confiar em `variacoes_ativas: 1` no meio de uma coleta grande.** Se todas deram 1, provavelmente o texto veio truncado e a dedup não casou. Conferir o `caracteres` de algumas notas
5. **Fechar a janela do Chrome no meio.** Perde a coleta inteira
