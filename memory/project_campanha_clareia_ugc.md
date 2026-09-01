---
name: project_campanha_clareia_ugc
description: Campanha Clareia Premium (UGC problema axila/virilha) subida no Meta — conta, pixel, IDs, script
metadata:
  type: project
---

Campanha **Clareia Premium** (clareador axila/virilha) no Meta — 10 ads UGC "problema real" (axila/virilha escura), estilo foto caseira, mulheres BR 25-55.

**Conta certa: `act_2797264153984955` = "USD - Clareia Premium"** (conta dedicada do produto). ⚠️ NÃO é a `act_1430326651782455` (essa é do Clarilux) — subi errado nela primeiro e apaguei (DELETED); a conta que o Guilherme passou por engano foi a do Clarilux.

- Pixel **`966299466456560`** ("SANO - Clareia Premium", NATIVO dessa conta — sem problema de compartilhamento). Instalado nas 13 páginas do site (PageView); Purchase server-side Yampi.
- Page `1044942952043640` (Sano Brasil). Só FB (IG vazio).
- Campanha `120250013679350053` (SANO_CLAREIA_UGC_ADV) · CBO · Bid Cap US$15 (1500) · US$300/dia (30000) · PAUSED.
- Adset `120250013679590053` · BR mulheres 25-55 · advantage_audience:0 · compliance BR (benef 880756411607509).
- 10 ads PAUSED, cada um = 1 criativo UGC + copy curta + link pro advertorial do ângulo. site_extensions OPT_OUT.

**Assets:** criativos `clareia-premium/images/ugc-problema-01..10.webp` (jpg em `/jpg/` p/ Meta — rejeita webp). Copies em `clareia-premium/COPIES-UGC-META.md`. Manifesto `_dev/manifesto-clareia-ugc.json`. Script `_dev/subir-clareia-ugc.py` (test|all, REUSE_CID/REUSE_ASID/START_AD p/ retomar). Log `_dev/manifestos-prime/clareia-ugc-subida.jsonl`.

12 advertoriais no ar (`/adv-clareia-premium`, `/adv-clareia-v2..v11`). Token Meta no `.env` `META_ACCESS_TOKEN` (vence ~60d).

Relacionado: [[project_campanha_clarilux_melasma]], [[reference_pixels_meta_por_produto]], [[feedback_nunca_subir_ad_com_site_extensions]], [[feedback_manifesto_antes_de_subir]]
