---
name: project_advertoriais_tonico
description: Conjunto de advertoriais do Tônico Supremo (4 ângulos × masculino+feminino) adaptados do NovaMane/KilgourMD
metadata: 
  node_type: memory
  type: project
  originSessionId: 77ffe71b-c21b-4cb4-9a58-1bbcf8ae4fa8
---

Conjunto de advertoriais do Tônico Supremo, criados 2026-06-27, adaptados de advertoriais campeões dos concorrentes NovaMane e KilgourMD/ScalpScience (capturas PNG do usuário).

**4 ângulos, cada um em versão masculina e feminina (-fem = menopausa):**
- **v3** golpe da finasterida/minoxidil (anti-Big-Pharma) — `/adv-tonico-v3` · `/adv-tonico-v3-fem`
- **v4** descoberta científica / inflamação do couro — `/adv-tonico-v4` · `/adv-tonico-v4-fem`
- **v5** "seu xampu acelera a queda" — Tônico complementar, NÃO precisa trocar de xampu (leave-in pós-banho) — `/adv-tonico-v5` · `/adv-tonico-v5-fem`
- **v6** folículo dormente / couro envelhece / 2 fases — `/adv-tonico-v6` · `/adv-tonico-v6-fem`
- (+ `/adv-tonico-supremo` original, masculino)

**Convenções:**
- Masculinos: pasta+imgs `tonico-supremo/`, CTA -> `/tonico-supremo-v2`.
- Femininos (sufixo `-fem`): HTML em `tonico-supremo/`, imgs em `tonico-supremo-fem/images/`, CTA -> `/tonico-supremo-fem`. Copy menopausa (risca alargada, queda do estrogênio→DHT).
- Todos herdam o template/CSS de `adv-tonico-supremo.html` (editorial "Portal Vida & Saúde", Georgia). Ativos reais: Café Verde/Baicapil/Beauplex. Sem preço no adv. Sem drop cap.

**Imagens novas geradas pra os advs (via `_dev/gen-adv-tonico-imgs.py` e `_dev/gen-adv-fem-imgs.py`), prefixo `adv-*`:**
- Produto cinematográfico: adv-produto-cine-dark/cafe-verde/gota (neutras, reusadas em todos)
- Diagramas: adv-diagrama-couro-inflamado, adv-diagrama-foliculo-dormente (neutras)
- Gráficos: adv-grafico-queda-semanas (barras 38→93% "satisfação relatada"), adv-comparativo-tonico-minoxidil (checks vs X)
- Dor/lifestyle COM PESSOA (versão por gênero): adv-dor-chuveiro / adv-aplicando-tonico (masc) e -fem (mulher menopausa) + adv-dor-travesseiro (neutra) + adv-dor-risca-espelho-fem
- Imagens sem pessoa foram COPIADAS pra pasta fem; só dor/lifestyle com pessoa foram regeradas como mulher.

Ver [[project_tonico_supremo_fem]] (página de venda feminina) e [[feedback_link_anuncio_sempre_advertorial]] (anúncio->advertorial->venda).
