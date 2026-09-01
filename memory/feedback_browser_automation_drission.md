---
name: Automação de browser usa DrissionPage, não Playwright
description: Pra qualquer teste/scraping/automação de browser, usar DrissionPage. Playwright NÃO existe mais.
type: feedback
originSessionId: d2c18d3e-aab0-440a-b3c4-86d8c38e0c1d
---
**Regra:** Para qualquer automação de browser (testar UI, scrape, simular drag-and-drop, abrir página, validar render, ler DOM, snapshot, screenshot), usar **DrissionPage** (Python). **Playwright não existe mais.**

**Why:** o usuário falou explicitamente em 2026-05-05: "coloca como regra aí dentro da porra do cloud que não existe mais Playwright, é Drissom". Os MCPs de Playwright (`mcp__playwright__*`) podem aparecer eventualmente como "deferred tools", mas são instáveis (desconectam) e não devem ser usados.

**How to apply:**
- Nunca chamar `mcp__playwright__*`. Se o tool aparecer disponível, ignorar.
- Para testes de UI / DOM / drag-and-drop / snapshots / scraping, usar **DrissionPage** via Python:
  ```python
  from DrissionPage import ChromiumPage
  page = ChromiumPage()
  page.get('http://localhost:5004')
  el = page.ele('css:[data-replix-id]')
  el.drag_to(other)
  page.console_messages()  # logs do browser
  ```
- DrissionPage controla Chrome real (não headless por padrão), é estável, não precisa de MCP. Roda dentro de um script Python normal via Bash/PowerShell.
- Pra log do console do browser, ler via `page.listen.start('Console.messageAdded')` ou checar log via DevTools API.
- Quando o usuário diz "testa no browser" / "vê se isso roda" / "verifica via browser", a expectativa é DrissionPage.

**Quando o usuário pedir testes de browser:** rodar via `python -c "..."` ou criar script `.py` na pasta do projeto — não tentar MCP.
