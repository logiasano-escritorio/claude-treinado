---
name: DrissionPage substituiu Playwright
description: Playwright desinstalado — todos os projetos usam DrissionPage para browser automation
type: feedback
originSessionId: eee4c79a-9468-4f05-abe9-e209538d91c1
---
Usar sempre DrissionPage para browser automation. Playwright foi desinstalado em 2026-04-12.

**Why:** Playwright falhou 3x em coletar seções de SPAs com JS pesado (0 seções coletadas). DrissionPage coletou 10 seções na primeira tentativa sem ajuste.

**How to apply:** Qualquer agente ou script que precisar abrir browser usa `from DrissionPage import ChromiumPage, ChromiumOptions`. Nunca instalar ou importar playwright. pip install DrissionPage se não estiver instalado.
