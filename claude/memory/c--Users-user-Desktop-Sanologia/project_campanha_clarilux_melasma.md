---
name: project_campanha_clarilux_melasma
description: "Campanha Clarilux/melasma no Meta (EUA 11) — 10 ads single-image PAUSED + checkouts Yampi corretos na PV"
metadata:
  node_type: memory
  type: project
  originSessionId: 7c722b03-0e07-4b10-9a06-8394a9f4326c
---

Campanha **Clarilux melasma** subida no Meta 2026-07-08, PAUSED (Guilherme ativa na mão). Fruto do pipeline: raspou Ad Library → adaptou 53 long-forms → gerou 10 imagens → 6 advertoriais → campanha.

**Conta:** `act_2164352101016970` (EUA 11, USD). ⚠️ `account_status: 3` (fatura pendente, disable_reason 0) — cria PAUSED ok, mas ATIVAR pode travar até acertar pagamento.
**Pixel Clarilux:** `2873393396348834` ("SANO - Clarilux"). **Page** `759591800579421` · **IG** `17841477315620430`.

**Campanha** `CLARILUX | MELASMA | 10ADS` (`120248091848900442`): CBO, OUTCOME_SALES, LOWEST_COST_WITH_BID_CAP bid US$15 (1500), US$300/dia (30000).
**1 conjunto** `120248091849620442`: OFFSITE_CONVERSIONS/PURCHASE, BR mulheres (genders:[2]) 30-65, advantage_audience 0, compliance BR (regional BRAZIL_REGULATION+VOLUNTARY_VERIFICATION, beneficiary/payer `880756411607509`).
**10 ads single-image** (as 10 imgs de `clarilux/images/melasma-novas/`), single-image formato que gasta bem ([[project_campanha_tonico_meta]]). Cada ad = imagem + texto curto próprio + link pro advertorial do ângulo (v6/v7/v8/v9/v11). site_extensions OPT_OUT ([[feedback_nunca_subir_ad_com_site_extensions]]).

**Pegadinha resolvida:** Meta `/adimages` NÃO aceita .webp (erro subcode 1487411 "tipo não suportado") — converter pra JPG antes (as jpg ficam em `melasma-novas/jpg/`). Script `_dev/subir-clarilux-melasma.py`, manifesto `_dev/manifesto-clarilux-melasma.json`, log `_dev/manifestos-prime/clarilux-melasma-resultado.jsonl`.

**⚠️ Imagem antes/depois COM texto "ANTES/DEPOIS" = Meta reprova** (before-after idealizado em saúde/beleza). 6 das 10 imgs tinham → regeneradas SEM texto (split 2-rostos limpo, sem badge), ads recriados (creative imutável, deletar+recriar) via `_dev/trocar-imgs-clarilux.py` (2026-07-09). Prompt SEM texto: "ABSOLUTELY NO text/words/letters/labels/badges/captions". Risco residual: split de 2 rostos ainda pode ser lido como before-after; plano B = rosto único pele-bonita.

**Checkouts PV `/clarilux-v2`** (eram placeholder href=#, nunca ligados): ligados aos 3 links Yampi + preços batendo — Compre 1 Ganhe+1 R$199 `EZKR6CWEUU` / 3 Frascos Compre 2 Leve 1 R$294 `F1SJXFQOZQ` / 5 Frascos Compre 3 Leve 2 R$394 `4SE30Q1NZQ`. Tiers 4→3. Commit `1b0017b`.

**Recriada 2026-07-15 na conta própria SANO-CLARILUX** `act_1430326651782455` (USD, ativa, BM Plat4orm 1231482469162579) — campanha nova `120269315930870362`, conjunto `120269315937530362`, 10 ads, PAUSED. Página **Sano Brasil** `1044942952043640` (não tinha "Sano" nas promote_pages, mas subiu ok), mesmo pixel Clarilux, sem IG. ⚠️ conta com rate-limit agressivo (subcode 2446079) após subir/trocar em massa — verificar 1 ad por vez, não listar. ⚠️ daily_budget 30000 aqui = **US$300/dia** (USD), rever se era pra ser R$.
**Criativos trocados p/ UGC anti-IA (2026-07-15):** os 10 antes/depois de estúdio "pareciam IA" e foram rejeitados → gerados 10 UGC selfie caseira ([[reference_ugc_melasma_anti_ia]], script `gen-clarilux-ugc-melasma.py`, jpg em `clarilux/images/ugc-melasma/jpg/`) e trocados 1:1 nos 10 ads via `_dev/trocar-imgs-ugc-clarilux.py` (recria creative idêntico c/ novo image_hash + PATCH no ad; copy/link/pixel/OPT_OUT preservados). Log `_dev/manifestos-prime/clarilux-troca-ugc.jsonl`.

Manifesto Obsidian: `BACKLOG DE TRÁFEGO/Clarilux/MANIFESTO — Campanha Clarilux Melasma.md`. Pixel no GTM `GTM-PNVRC5ZR` (não no HTML). [[reference_raspar_ad_library_drissionpage]] · [[feedback_adaptar_longform_nunca_reduzir]].
