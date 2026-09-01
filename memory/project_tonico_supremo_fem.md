---
name: project_tonico_supremo_fem
description: "Página feminina do Tônico Supremo (menopausa) — /tonico-supremo-fem, derivada da masculina v2"
metadata: 
  node_type: memory
  type: project
  originSessionId: 77ffe71b-c21b-4cb4-9a58-1bbcf8ae4fa8
---

Página feminina do Tônico Supremo, focada em **queda capilar na menopausa**, criada 2026-06-27.

- **Rota:** `sanobrasil.com/tonico-supremo-fem` (vercel.json → `/tonico-supremo-fem/tonico-supremo-fem`). Pasta minúscula (cuidado case-sensitive Vercel, ver [[feedback_pastas_case_quebram_deploy_vercel]]).
- **Derivada de** `tonico-supremo/tonico-supremo-v2.html` (a masculina). Copy 100% reescrita pro ângulo feminino: risca alargada, queda hormonal/estrogênio→DHT, rabo de cavalo fino, lenço/pó pra disfarçar. Nada de "entradas/coroa/calvície masculina".
- **Oferta idêntica à masculina:** kits 1/3/5/8 (R$199/298/398/498) + MESMOS checkouts Yampi (TN51PZ9REM / FVWH32O9UM / RJVGF0E68E / R4T81ZH1EI). É o mesmo produto físico, só muda a comunicação.
- **Imagens:** 20 regeradas com mulheres 45-62 via `_dev/gen-tonico-fem.py` (hero, 10 UGC, 5 before/after risca-alargada→cheia, 4 de seção). Before/after usa MESMA pessoa nos 2 lados (foto ANTES vira ref de identidade do DEPOIS). Mantidas as sem-pessoa: mecanismo DHT, ativos-trio, selo-garantia.
- **Visual:** acento feminino rosé `--rose:#c2185b` nos `.hl` e `.sec-tag`; verde do produto (`--rosa`=#1f9d57) preservado no CTA; navy nos textos.

Ver [[feedback_ugc_conferir_genero_publico]] (conferir gênero das imagens) e [[reference_oferta_padrao_sano]].
