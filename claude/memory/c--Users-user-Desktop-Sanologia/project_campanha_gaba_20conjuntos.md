---
name: project_campanha_gaba_20conjuntos
description: "20 conjuntos × 10 ads (gabapentina/neuropatia) na campanha SANO_PRIME_CREME EUA 11 — ACTIVE, 6 páginas, banco de imagens de feed"
metadata:
  node_type: memory
  type: project
  originSessionId: 7c722b03-0e07-4b10-9a06-8394a9f4326c
---

Subidos 2026-07-09 **20 conjuntos × 10 ads = 200 ads** na campanha existente **`SANO_PRIME_CREME_TODOS_OS_ANGULOS`** (`120244126350890442`, conta EUA 11 `act_2164352101016970`, CBO US$4000/dia, bid cap). Tudo **ACTIVE** (Guilherme pediu ao vivo). 0 falhas.

**Modelo:** cada conjunto = 1 advertorial de gabapentina (`/adv-prime-gaba-<slug>`), com **título+descrição+primary text próprios** casando com o ângulo, aplicados nos 10 ads. As **10 imagens de sintoma de neuropatia** (`prime/images/ads/gaba-feed-01..10`, pés queimando/formigando/choque, senhores BR estilo documentário caseiro) são **banco compartilhado** — coerência com o PROBLEMA (neuropatia), não com o personagem do advertorial. Upload 1x, reuso dos hashes.

**⚠️ Distribuir páginas pra não estourar limite de ads/página:** 20 conjuntos rodam em **6 páginas** (round-robin): Ana Caroline `829776076876379`, Andressa Olivia `778161738717128`, Bruno Willian `759591800579421`, Sano Brasil `1044942952043640`, Sanologia `650163921506803`, Nutra Care `809142178952032`. **Só Facebook** (sem instagram_user_id — evita erro de página sem IG vinculado). Nenhuma reprovou (nem a Sanologia).

**Config adset:** OFFSITE_CONVERSIONS/PURCHASE, pixel Prime `1289947162723962`, bid 2500 (US$25), BR 45-65 ambos gêneros, advantage_audience 0, compliance BR (BRAZIL_REGULATION+VOLUNTARY, beneficiary/payer `880756411607509`), site_extensions OPT_OUT ([[feedback_nunca_subir_ad_com_site_extensions]]). Meta /adimages: PNG funciona, converti pra jpg por segurança ([[project_campanha_clarilux_melasma]] tem a pegadinha do webp).

Script `_dev/subir-gaba-20conjuntos.py`, manifesto `_dev/manifesto-gaba-20conjuntos.json`, log `_dev/manifestos-prime/gaba-20conjuntos-resultado.jsonl`, IDs no Obsidian `BACKLOG DE TRÁFEGO/Prime/MANIFESTO — Campanha Gaba 20 Conjuntos.md`. Os 20 advertoriais: 16 variações antigas + 20 novas (personagem+elemento) desta sessão, imagens de personagem coerentes ([[feedback_consistencia_personagem_advertorial]]).
