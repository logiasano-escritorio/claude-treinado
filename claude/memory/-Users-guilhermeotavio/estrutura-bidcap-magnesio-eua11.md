---
name: estrutura-bidcap-magnesio-eua11
description: "Estrutura real da campanha BIDCAP - Magnesio Bisglicinato na conta EUA 11 (CBO + bid no adset, escada de bid por ângulo)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4c6ee100-efa6-4d15-9b51-78f1091189ac
  modified: 2026-09-09T10:17:46.100Z
---

Conta **EUA 11 `act_2164352101016970`** (USD) — em 2026-09-09 está com `account_status: 1` (ATIVA). A restrição status 3 que a memória `reference_skill_meta_ads_analyzer_bidcap` cita **não vale mais**; a Graph API responde normalmente com token de usuário.

**Campanha `120248694356150442` — "BIDCAP - Magnesio Bisglicinato."** (criada 2026-08-01, ACTIVE):

- `OUTCOME_SALES` · `AUCTION` · `bid_strategy: LOWEST_COST_WITH_BID_CAP` **no nível campanha** · `pacing_type: standard` · `special_ad_categories: []`.
- **CBO puro**: `daily_budget` 2400000 (**US$24.000/dia**) na campanha e **nenhum adset com budget próprio** (102 de 102 sem `daily_budget`).
- O **bid mora no adset** (`bid_amount`), não na campanha — `bid_amount` da campanha vem vazio. É esse o desenho: um teto de lance por ângulo, orçamento único competindo entre eles.
- **102 adsets** (27 ativos / 75 pausados). 23 em `LEARNING`, só 4 em `SUCCESS`.
- Pixel único **`2738375386539927`** (≠ FUNGZERO `2024443845625153`, ≠ Prime `1289947162723962`) · `OFFSITE_CONVERSIONS` + `PURCHASE` · billing `IMPRESSIONS` · atribuição **só 7d clique**.
- BR, **age 35-65** em 80 dos 102 adsets · **`advantage_audience: 0` em 92 de 102** — targeting manual aqui, ao contrário do padrão 1-1-1 de [[conta-meta-prime-creme]] e [[conta-meta-fungzero-magnesio]], que usam advantage_audience=1.

**Escada de bid por ângulo** (cents USD, adsets ativos) — o padrão que ele usa:

| Bid | Onde | Ângulo |
|---|---|---|
| **$25,00** | 8 adsets, toda a linha `LF07..LF32` | advertorial de constipação (long-form) |
| $31,00 | LF08, ZZ TESTE | testes |
| $35,00 | LF10 v2, CJ02 | teste / direto |
| $37,00 | AD30, SONO body 2, CJ02 | sono |
| $38,60 | LF16 v2, SONO body 1, ZZ HOOK07, 02/04 ADV | sono + broad advertorial |
| $41,00 | AD29 rótulo/óxido, "03 Oito Marcas Falharam" | PV direto |

Banda completa observada: $24 a $41. Regra implícita: **advertorial long-form de constipação leva o bid mais baixo ($25); PV direto e broad levam o mais alto ($38-41)**.

Nomenclatura de adset: `LF<nn> - <primeiras palavras do lead>` (advertorial), `SONO - BODY <n> - 10 Hooks - <público>` (matriz body×hook), `AD<nn> - <ângulo>`, `CJ<nn> - AD<n> - 10Hooks`, `ZZ <teste>`, `0<n> <nome do ângulo>`.

## Clone dos campeões na FungZero (2026-09-09)

Campanha **`52654530858924` — "BIDCAP - Magnesio Bisglicinato - CAMPEOES IMAGEM"** em `act_1642921946819932`: os 27 criativos de **imagem** com ROAS ≥ 2 e gasto ≥ $100 da campanha de origem, **1 conjunto por anúncio**, CBO US$500/dia, tudo ACTIVE. Pixel trocado para `2024443845625153` ("Teste Pixel Magnésio"). 14 dos 27 remapeados para a página Sanologia porque suas páginas de origem (Nutra Care Technology, Andressa Olivia, Sano Brasil, Farma Forte) não estão liberadas nessa conta.

**Três coisas que travaram e como se resolvem** — valem pra qualquer clone entre contas:

1. **`image_hash` e `video_id` são por conta.** Precisa baixar da origem (`/act_<id>/adimages` dá a `url`) e re-subir no destino. O hash volta **idêntico**, porque a Meta hasheia o conteúdo — dá pra usar o mesmo hash no manifesto depois de subir.
2. **No upload pra `/adimages`, o nome do campo multipart tem que ser o nome do arquivo** (`-F "foo.jpg=@/path/foo.jpg"`). Usar `-F "bytes=@..."` retorna `Invalid parameter` com `file_size: 8` — erro que não diz nada sobre a causa real.
3. **Adset no Brasil exige a identidade de anunciante verificado, senão nenhum conjunto é criado**: `regional_regulated_categories=["BRAZIL_REGULATION","VOLUNTARY_VERIFICATION"]` + `regional_regulation_identities={"universal_beneficiary":"880756411607509","universal_payer":"880756411607509"}`. Sem isso o erro é "Forneça um anunciante verificado…" em 100% dos conjuntos.

Ler adsets em lote logo depois de criar 27 **estoura o rate limit** (`User request limit reached`) e fica bloqueado por vários minutos — conferir depois, não na sequência.
