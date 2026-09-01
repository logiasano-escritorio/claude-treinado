---
name: no-drop-cap-advertorial
description: "Nunca usar drop cap (primeira letra gigante) em advertoriais — fica ridículo, especialmente quando o seletor vaza pra cards/estágios internos"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c3397450-d899-4a42-b26a-2b11431d9ff3
---

**REGRA: nunca usar drop cap (`::first-letter` com font-size grande) em advertoriais Sano/Relívia.**

**Why:** O usuário reagiu visceralmente ao ver drop caps no advertorial do Prime Creme — "ridículo", "feio", "essa porra tá ridículo". Pior: o seletor `.adv-article p:first-of-type::first-letter` vaza pro primeiro `<p>` de cada `.adv-stage` (cards de estágio), criando letras gigantes "A", "D" dentro dos cards coloridos — visualmente quebrado. Drop cap é estilo "Reader's Digest anos 80" que destoa do tom editorial moderno que queremos.

**Reincidência 2026-05-17:** mesmo padrão apareceu em `adv-magnesio-bisglicinato.html` com `.article-body p:first-of-type::first-letter { font-size: 3.2em; color: #1e3a8a; ... }` + override mobile 2.8em. Usuário pediu remoção imediata. → **VARRER advertoriais existentes** procurando `first-letter` antes de qualquer revisão.

**How to apply:**
- Em qualquer advertorial novo (`adv-*.html`), NÃO incluir CSS de `::first-letter` com `font-size > 1em`.
- Se herdar template antigo que tenha drop cap, remover na primeira passada.
- Texto editorial deve abrir com o parágrafo normal — o impacto vem da lead sentence e do sub-heading, não de typography tricks.
- Aplicar pra TODOS os advertoriais — Sano, Relívia, qualquer marca.

Related: [[reference_design_guides]]
