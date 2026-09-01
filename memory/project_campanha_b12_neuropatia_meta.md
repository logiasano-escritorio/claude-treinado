---
name: project_campanha_b12_neuropatia_meta
description: "Campanha Meta B12 Neuropatia publicada PAUSED na EUA 11 — 1 CBO, 5 conjuntos, 27 ads"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2fc21bf8-28c1-4d72-a138-cb0373acb1c8
---

Campanha **SANO_B12_PRINCIPAL_CBO_BIDCAP25** publicada PAUSED na conta EUA 11 (`act_2164352101016970`) em 2026-06-16. (Re-subida com slug novo `/b12-principal` — o slug antigo `/b12-diabetes-metformina` estava reprovando ads no Meta por ter "diabetes". A 1ª versão `120246701156320442` foi desativada pelo Guilherme.)

- **Campaign ID ATIVO:** `120246701372750442` (CBO, OUTCOME_SALES, USD 300/dia, bid cap USD 25)
- **5 conjuntos** (BR 45-65 broad, pixel B12 `980607068056359`, Page ads `759591800579421`):
  - C1 Mecanismo/absorção `120246701373150442` (6 ads)
  - C2 Medo/urgência `120246701373580442` (4 ads)
  - C3 Emocional/esposa `120246701373930442` (8 ads)
  - C4 Autoridade/pós-cirurgia `120246701374540442` (4 ads)
  - C5 Depoimentos/outros `120246701375070442` (5 ads)
- **27 ads** = 27 copies long-form (adaptadas dos 30 swipes de neuropatia) + imagens do banco. Link `sanobrasil.com/b12-principal`.
- **Slug:** `/b12-principal` = rewrite no `vercel.json` apontando pro arquivo físico `b12/b12-diabetes-metformina.html` (não renomeado; a URL antiga segue no ar). Trocar slug = trocar `LINK_URL` no script + links nas 27 notas + rewrite + data-funnel + re-subir campanha.
- Manifesto/backup: `_dev/b12-neuropatia-meta-result.json`. Script: `_dev/publicar_b12_neuropatia_meta.py`. Copies no Obsidian `BACKLOG DE TRÁFEGO/B12 Neuropatia/`.

**Aprendizados Meta API v23 (2026-06):** adimages NÃO aceita webp (converter pra jpg); adset agora EXIGE `targeting_automation.advantage_audience: 0|1` senão erro 1870227. Token EUA 11 do `agente_funil.py.bak` estava expirado (code 190) — Guilherme gera novo no Graph API Explorer. Ver [[reference_meta_ads_sano]] e [[reference_meta_ads_api_fixes_2026_05]].

**Pendente:** ativar quando quiser (tudo PAUSED). Confirmar checkout Yampi da página antes de escalar.
