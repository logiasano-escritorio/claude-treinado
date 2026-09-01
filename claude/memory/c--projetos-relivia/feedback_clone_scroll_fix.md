---
name: Clone Page — Scroll Bloqueado
description: Shopify themes definem overflow:hidden no body, quebrando scroll local. Fix obrigatório em todo clone.
type: feedback
originSessionId: b24458c5-c7de-4a26-a4d7-22e9a63b7a7b
---
Sempre que gerar um clone de página Shopify (ou qualquer tema), o body recebe `overflow: hidden` via CSS do tema, o que impede scroll ao abrir o arquivo local no browser.

**Fix obrigatório no sanitize.py — já implementado:**
1. CSS injetado: `html { overflow-y: scroll !important; } body { overflow-y: auto !important; overflow-x: hidden; }`
2. Inline style no `<body>`: `overflow-y: auto !important; overflow-x: hidden;`
3. Inline style no `<html>`: `overflow-y: scroll !important;`

**Why:** O CSS do tema tem especificidade alta. Inline style + !important é a única forma confiável de sobrescrever.

**How to apply:** Toda vez que o `sanitize.py` rodar, esses três fixes devem estar presentes. Nunca remover. Se o usuário reportar "não consigo scrollar o clone", verificar se os inline styles estão no `<body>` e `<html>`.
