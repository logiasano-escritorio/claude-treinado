---
name: funil-prime-edema
description: "Funil Sano Prime Edema (pernas inchadas/pesadas) — página prime-pv-edema, IDs Meta do Prime (Page/IG/Pixel próprios), campanha publicada 2026-06-01"
metadata: 
  node_type: memory
  type: project
  originSessionId: 929419a0-dd64-458c-911b-ee82ae1ec9c7
---

# Funil Prime Edema (pernas inchadas e pesadas)

Ângulo do "Prime Creme de Massagem" pra EDEMA / insuficiência venosa, derivado de [[funil-prime-pv-neuropatia]] (prime/index.html).

## Página
- Arquivo: `Sanologia/prime-edema/index.html` · rota `sanobrasil.com/prime-pv-edema` (rewrite no vercel.json)
- Herói da fórmula = **Ginkgo Biloba + Centella Asiatica** (7 ativos). Centella foi ADICIONADA (não existia no de neuropatia) — imagem `ing-centella.png` gerada via Vertex.
- Copy e 6 imagens da galeria + ingredientes regeneradas pro ângulo edema (i2i). Garantia 90 dias.

## IDs Meta do PRIME (diferentes da conta institucional Sano!)
Conta: `act_2164352101016970` (USD). Mas o Prime usa Page/IG/Pixel PRÓPRIOS:
- **Page**: `1044942952043640`
- **IG (instagram_user_id)**: `17841419138065018`
- **Pixel Prime**: `1289947162723962` (mesmo do funil Prime Joelho — vale pra todos os ângulos Prime)
- advertiser_id (compliance BR): `880756411607509`
- ⚠️ NÃO confundir com a Page `759591800579421` / IG `17841477315620430` de [[meta-ads-api-fixes-2026-05]] (essas são de outros funis Sano)

## Campanha publicada (2026-06-01, PAUSED)
- Campaign `120245592196490442` — SANO_PRIME_EDEMA_CBO_BIDCAP15
- 1 adset `120245592221320442` (BR 45-65 broad) + 10 ads (criativos manchete)
- CBO US$300/dia, Bid Cap US$15, OUTCOME_SALES/PURCHASE
- Body = long-form de edema (~9.6k chars) em todos os 10 ads
- Script: `Sanologia/_dev/publicar_prime_edema_meta.py` · resultado: `_dev/prime-edema-meta-result.json`
- Criativos: `_dev/criativos-edema/` (10 PNG/JPG manchete) + `copy-longform-edema.txt`

## Trade-off conhecido
- Estrutura 1 adset / 10 ads (a pedido do user) → CBO concentra entrega em 2-3 criativos. Pra teste justo de criativo seria ABO (1 criativo/adset).
