---
name: reference-yampi-api-fields-dossie
description: "Dossiê de campos disponíveis na API Yampi pra Sanologia/yampi-webhook — consultar ANTES de chutar nomes de campos. Tem ideias mapeadas de price_sale, token de checkout, stock_status, blocked_sale, etc."
metadata: 
  node_type: memory
  type: reference
  originSessionId: fda4c240-53cf-4717-a6b1-266a11839ad6
---

📄 **Arquivo:** `Desktop/Sanologia/_dev/yampi-webhook/YAMPI_API_FIELDS.md`

Capturei via `debugYampiSKU()` em 2026-05-19 os campos que a API Yampi devolve em `/catalog/skus` e `/catalog/products`. Organizado por prioridade (🟢 alto valor, 🟡 médio, 🔴 descartar).

**Quando consultar:**
- User pergunta "será que dá pra puxar X da Yampi?" → Ctrl+F nesse arquivo
- User pede pra adicionar coluna nova na aba Custos → confere se já tem campo pronto
- Antes de chutar nome de campo na API Yampi → consulta primeiro pra evitar erro tipo `cost` vs `price_cost`

**Campos 🟢 mapeados, prontos pra implementar quando user pedir:**
1. `price_sale` — preço de venda (margem teórica, auditoria de preço cross-página)
2. `token` + `purchase_url` — links de checkout que hoje ficam em memórias manuais (`reference_yampi_ids_glowup.md` etc) — substituir por aba auto-sync
3. `stock_status` + `total_in_stock` — alertas de estoque (todos 24 SKUs vieram out_of_stock no debug, validar com user)
4. `blocked_sale` — flag bloqueio venda

**Pegadinhas registradas:**
- Custo é `price_cost`, não `cost`
- Custo é por SKU/variação, não no produto pai
- Paginação via `meta.pagination.total_pages`

Linka [[reference_yampi_ids_glowup]] (esses IDs podem ser substituídos pelo auto-sync de `token`).
