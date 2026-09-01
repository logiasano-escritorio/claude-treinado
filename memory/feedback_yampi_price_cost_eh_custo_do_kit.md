---
name: feedback-yampi-price-cost-eh-custo-do-kit
description: "Na API Yampi, price_cost é o custo TOTAL do kit (não custo por pote). Nunca multiplicar por Qtd Potes na planilha de custos."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fda4c240-53cf-4717-a6b1-266a11839ad6
---

🚫 **NUNCA multiplique `price_cost` da Yampi por Qtd Potes do kit.**

**Por quê:** o campo `price_cost` na variação Yampi já é o custo TOTAL do kit, não o custo por pote/unidade. Ex: kit "3 Cremes" cadastrado com `price_cost: 76.50` significa R$76,50 pelos 3 cremes (R$25,50 cada). Multiplicar por 3 dá R$229,50 — absurdo.

**Como aplicar:**
- Na aba Custos do `_dev/yampi-webhook/Code.gs` Sano/Relívia:
  - Coluna E (Custo Unitário) = `price_cost` direto da Yampi (já é total do kit)
  - Coluna F (Custo Total) = `=E{linha}` direto, NUNCA `=D*E`
- Na aba Pedidos col O (Custo Produção): fórmula `custo_kit × (potes_vendidos / potes_por_kit)` — porque H é total de potes vendidos, não kits

**Histórico:** Descoberto em 2026-05-19 quando o user reclamou que os custos da aba Custos vieram multiplicados (Cálcio 3 potes apareceu R$229,50 quando o custo cadastrado na Yampi era R$76,50).

**Onde tá documentado:** [[reference_yampi_api_fields_dossie]] — `_dev/yampi-webhook/YAMPI_API_FIELDS.md` seção "Pegadinhas #3".
