---
name: Clone Page — Escopo limitado a Shopify
description: O pipeline run2.py é exclusivamente para páginas Shopify. HTML puro será uma funcionalidade separada futura.
type: project
originSessionId: b24458c5-c7de-4a26-a4d7-22e9a63b7a7b
---
O `clone-page/worker/run2.py` e o módulo `enhance/` são focados exclusivamente em páginas **Shopify**.

**Why:** Shopify tem estrutura previsível (Swiper.js para galeria, Rapi Bundles para variant picker) — isso permite detecção automática confiável. HTML puro tem estrutura arbitrária por loja, o que tornaria o código frágil e cheio de heurísticas que falham.

**How to apply:** Não adicionar detecção de estruturas não-Shopify no `enhance/`. Se surgir demanda para clonar páginas em HTML puro (ex: CheckoutChamp, ClickFunnels, páginas custom), criar um pipeline separado (`run3.py` ou pasta `enhance-html/`) com sua própria lógica de extração — sem misturar com o pipeline Shopify.
