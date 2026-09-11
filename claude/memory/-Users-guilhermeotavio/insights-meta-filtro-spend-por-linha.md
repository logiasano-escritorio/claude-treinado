---
name: insights-meta-filtro-spend-por-linha
description: "Nunca usar filtering spend no Insights da Meta para achar criativos campeões — o filtro roda por linha de ad, não por criativo agregado"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4c6ee100-efa6-4d15-9b51-78f1091189ac
  modified: 2026-09-09T11:24:21.527Z
---

Ao ranquear criativos por ROAS/gasto no Insights da Meta (`level=ad`), **nunca** passar `filtering=[{"field":"spend","operator":"GREATER_THAN",...}]` na chamada. Puxar **todas** as linhas sem filtro, agregar por `ad_name` (ou por creative), e só então aplicar os cortes de gasto e ROAS sobre o agregado.

**Why:** o mesmo criativo roda como vários `ad_id` em conjuntos diferentes, então o Insights devolve **uma linha por ad_id**, não uma por criativo. O `filtering` da API roda linha a linha, antes de qualquer soma. Isso corrompe o resultado nas duas direções:
- **Falso negativo:** criativo que gastou $60+$50+$40 (total $150, ROAS 2,4) tem as três linhas descartadas e some do ranking.
- **Falso positivo:** criativo aprovado porque só as linhas boas (>$100) foram somadas; as linhas menores, que puxavam o ROAS pra baixo, ficaram de fora.

Aconteceu em 2026-09-09 na campanha `120248694356150442`: com filtro deu "44 criativos com ROAS≥2 e gasto≥$100"; sem filtro, o número correto era **46** — 5 tinham sumido e 3 dos 44 não passavam de verdade (ROAS real 1,82 / 1,83 / 1,86). O total de linhas passa de 135 para 2.350 quando o filtro sai.

**How to apply:** buscar `level=ad`, `date_preset=maximum`, sem `filtering`, paginando até o fim; somar `spend` e `spend × purchase_roas` por criativo; ROAS agregado = receita somada ÷ gasto somado — **nunca** a média dos ROAS das linhas. Os cortes entram depois, em memória. Ver [[estrutura-bidcap-magnesio-eua11]].
