---
name: conta-meta-fungzero-magnesio
description: Config Meta do Sano Magnésio Bisglicinato na conta USD - FUNGZERO (act_1642921946819932)
metadata: 
  node_type: memory
  type: reference
  originSessionId: 167cb0ea-699f-4f78-be3e-edf99f80d10a
  modified: 2026-09-07T16:40:29.323Z
---

O **Sano Magnésio Bisglicinato (gomas)** roda na conta **`act_1642921946819932` ("USD - FUNGZERO")** — mesma estrutura 1-1-1 do Prime ([[conta-meta-prime-creme]]), mas com config própria:

- **Pixel** `2024443845625153` · PURCHASE · advertiser BR `880756411607509` (aqui é o padrão, não o `1228611831325801` do Prime).
- **Página** `650163921506803` (Sanologia), **sem `instagram_user_id`** — os ads dessa conta são só Facebook.
- Público **BR 25-65** (não 18-65), `advantage_audience=1`, `location_types` inclui `frequently_in`; atribuição **só 7d clique**.
- CTA `LEARN_MORE`; campanha `LOWEST_COST_WITHOUT_CAP` a US$30/dia; `degrees_of_freedom_spec` com ~82 OPT_OUT.
- Lote de 2026-09-07: 10 campanhas `Magnésio - AD01..AD10 H1B1..H10B1` → `https://www.sanobrasil.com/magnesio-intestino-cc` (página cobre intestino + sono + cãibra, então ângulo de sono/ansiedade tem continuidade lá).

**Duas armadilhas que custaram tempo nesse lote:**
1. Vídeo de ~34MB pode passar de 15 min pra ficar `ready` no Meta — usar timeout de 30 min no polling, não 15.
2. Quando o run morre no meio, o vídeo **já subiu**. Antes de re-rodar, procurar o `video_id` do log e colocar no item do manifesto (o publisher genérico reusa em vez de subir de novo).

Publisher genérico reutilizável (lê toda a config do manifesto, idempotente por nome de campanha): `Desktop/Repo GitHub - Sano/repo-git-mac-windows-sano/_dev/manifestos-magnesio/publicar_lote.py`.
