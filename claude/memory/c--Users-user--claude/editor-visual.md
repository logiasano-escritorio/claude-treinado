# Editor Visual — Documentação Técnica

## Arquivos do Projeto

| Arquivo | Descrição |
|---|---|
| `C:/projetos/editor-visual/editor-visual.html` | App principal (single-file, sem dependências externas além de CDN) |
| `C:/projetos/editor-visual/servidor/server.js` | Backend Puppeteer (Express, porta 3001) |
| `C:/projetos/editor-visual/servidor/package.json` | deps: express, puppeteer, cors |
| `C:/projetos/editor-visual/servidor/1-INSTALAR.bat` | `npm install` (só na primeira vez) |
| `C:/projetos/editor-visual/servidor/2-INICIAR.bat` | `node server.js` (iniciar sempre que usar) |
| `C:/projetos/editor-visual/scripts/` | Scripts Python de manutenção do editor |

## Como Usar

1. Duplo clique em `2-INICIAR.bat` → aguarda "✅ Rodando em http://localhost:3001"
2. Abrir `editor-visual.html` no Chrome
3. Colar URL → Importar URL
4. Badge "🟢 Servidor local ativo" confirma que Puppeteer está ativo

## Arquitetura do editor-visual.html

### 3 telas (screens):
- `dashboard-screen` — lista de projetos salvos (IndexedDB)
- `upload-screen` — campo de URL + opção upload de pasta + página em branco
- `editor-screen` — GrapesJS com toolbar (salvar, exportar, copiar HTML)

### Funções principais:

**`fetchWithProxy(url)`**
- Tenta `localhost:3001/fetch?url=...` (Puppeteer) primeiro
- Fallback: `allorigins.win` e `corsproxy.io`

**`checkLocalServer()`**
- Ping em `localhost:3001/status`
- Atualiza badge 🟢/🟡

**`loadHTMLFromString(raw, baseUrl)`**
- Processa HTML recebido (URL ou pasta)
- Resolve URLs relativas para absolutas
- Fix lazy load: varre TODOS os atributos data-* buscando URLs de mídia
- Move `<source src>` para `<video src>` (compatibilidade GrapesJS)
- Adiciona `controls`, `muted`, `autoplay`, `playsinline` em `<video>`
- Chama `fixVideoComponents()` após `editor.setComponents()`

**`injectCSSIntoCanvas(css)`**
- Cria Blob URL do CSS e injeta como `<link>` direto no `<head>` do iframe do GrapesJS
- **BYPASS do parser GrapesJS** — preserva CSS variables, pseudo-seletores, animações
- Re-injeta no evento `canvas:frame:load`
- Retenta até 20x com intervalo de 100ms se canvas não estiver pronto

**`processFiles(files)`**
- Upload de pasta: constrói mapa `filename → Blob URL`
- Processa CSS resolvendo `url()` para blob URLs locais
- Detecta lazy load via `data-*` attributes

**`fixVideoComponents(components)`**
- Percorre componentes GrapesJS recursivamente
- Copia `attrs.src` → `comp.set('src', ...)` para componentes video
- Chamada após `setComponents()` nas duas telas de carregamento

**`saveCurrentProject()` / `openProject(id)`**
- Usa IndexedDB para persistência
- Converte blob URLs → base64 antes de salvar (evita expiração)

**`buildExportHTML()` / `exportHTML()`**
- Gera HTML standalone com CSS inline
- Converte todos blob URLs → base64 data URLs via FileReader

**`toggleBeautify()`**
- Liga/desliga camada de embelezamento visual
- CSS layer: border-radius em imagens, botões, inputs (via `<link>` tag separada no iframe)
- JS layer: usa `getComputedStyle()` no canvas para detectar backgrounds de classes CSS
- Adiciona `padding: 1.25rem` + `border-radius: 10px` em elementos com background não-transparente e padding < 8px
- Guarda `dataset.beautified = '1'` para reverter ao desligar

**`googleTranslate(text)`**
- Chama `localhost:3001/translate?text=...` (sem CORS)
- Retorna texto traduzido para PT-BR

**`translatePage()`**
- Seleciona elementos de texto via CSS selector (p, h1-h6, li, td, th, label, button, a, span, div[class*="rte"])
- Traduz cada um via `googleTranslate()` em sequência com progress counter no botão
- Após conclusão: `editor.setComponents(translatedHTML)` + `fixVideoComponents()` + `injectCSSIntoCanvas(currentCSS)`
- **CRÍTICO**: precisa resyncar GrapesJS com `setComponents()` — DOM manipulation direta desincroniza o component model

## CSS Fixes em `loadHTMLFromString`

```javascript
// Fix 1: URLs protocol-relative (//cdn.com/...) → https://
allCSS = allCSS.replace(/url\(\s*["']?(\/\/[^"')]+)["']?\s*\)/g, (m, u) => `url('${base.protocol}${u}')`);

// Fix 2: CSS @import cross-origin → proxear via localhost
allCSS = allCSS.replace(
  /@import url\(\s*['"]?(https?:\/\/(?!localhost)[^'")\s]+)['"]?\s*\)/gi,
  (m, cssUrl) => `@import url('http://localhost:3001/proxy?url=${encodeURIComponent(cssUrl)}')`
);

// Fix 3: Fontes cross-origin → proxy local
allCSS = allCSS.replace(
  /url\(\s*['"]?(https?:\/\/(?!localhost)[^'")\s]+\.(?:woff2?|ttf|otf|eot)[^'")\s]*)['"]?\s*\)/gi,
  (m, fontUrl) => `url('http://localhost:3001/proxy?url=${encodeURIComponent(fontUrl)}')`
);
```

## Bugs Corrigidos (histórico)

| Problema | Causa | Fix |
|---|---|---|
| CSS não carregava no editor | GrapesJS parser destrói CSS variables/pseudo-seletores | Injetar CSS como `<link>` blob no iframe, bypassa o parser |
| Imagens não apareciam | Lazy load via `data-src`, `data-lazy`, etc. | Scanner de TODOS os atributos `data-*` |
| Vídeos não apareciam | 1) GrapesJS Video Component ignora `src` do HTML; 2) `<source>` filho não suportado | `removeType('video')` no GrapesJS + mover `<source src>` para `<video src>` |
| Vídeos não reproduziam | Sem `controls`/`autoplay` | Adicionar `controls muted autoplay playsinline` em todos `<video>` |
| Imagens 100% JS (sem data-src) | Puppeteer não instalado | Backend Puppeteer com headless Chrome + scroll automático para lazy load |
| Fontes mostrando Times New Roman | URLs `//cdn.com/` viram `file://cdn.com/` no contexto file:// | Fix 1: converter `//` → `https://` no CSS |
| Layout quadrado/feio (dentalpulsepro) | @import CSS falha CORS no iframe blob: | Fix 2: proxear @import via localhost:3001/proxy |
| CSS proxy quebrando URLs internas | Root-relative `/cdn/` resolvia para `localhost:3001/cdn/` | `inlineCSSImports()` server-side: inlina CSS E corrige URLs durante fetch Puppeteer |
| Beautify não detectava backgrounds | Replo usa backgrounds em classes CSS, não inline | JS `getComputedStyle()` scan no lugar de CSS `[style*="background-color"]` |
| Tradução não funcionava (CORS) | `fetch('https://translate.googleapis.com')` bloqueado de `file://` | Endpoint `/translate` no server.js usa Node fetch sem CORS |
| Tradução retornava erro silencioso | Double URL encoding no proxy quebrava a chamada | Endpoint `/translate` dedicado (sem passar pelo /proxy genérico) |
| Textos traduzidos não editáveis | DOM manipulation direta desincroniza GrapesJS component model | Após tradução: `editor.setComponents()` + `fixVideoComponents()` + `injectCSSIntoCanvas()` |
| Editor inteiro parava de funcionar (botões sem resposta) | `buildFullHTML` tinha `\`` (backslash antes de backtick) e `\${html}` em vez de `${html}` — SyntaxError no V8 moderno impedia TODO o JS de executar | Remover o `\` de `\`` → `` ` `` e de `\${...}` → `${...}` em `buildFullHTML`. Fix: script `fix-editor2.py` + `fix-editor3.py` em `Desktop/relivia/` |

## Detalhes do Backend Puppeteer (server.js)

- Porta: 3001
- `GET /status` → `{ ok: true }` (health check)
- `GET /fetch?url=...` → `{ html: "..." }`
  - Lança Puppeteer headless
  - `waitUntil: 'networkidle2'`, timeout 30s
  - Scroll automático: +400px a cada 150ms até o fim + aguarda 1000ms
  - Volta ao topo + aguarda 500ms
  - Chama `inlineCSSImports()` antes de retornar
  - Retorna `page.content()` com CSS @imports já inlinados
- `GET /proxy?url=...` → proxy CORS-free para qualquer asset (fontes, CSS, imagens)
- `GET /translate?text=...&lang=pt-BR` → chama Google Translate unofficial API, retorna `{ translated }`
- `inlineCSSImports(html, pageUrl)`:
  - Regex busca todos `@import url(...)` no HTML
  - Fetcha cada URL server-side (sem CORS)
  - Corrige root-relative URLs dentro do CSS fetchado (`/cdn/...` → `https://origin/cdn/...`)
  - Substitui `@import` pelo conteúdo CSS inline

## GrapesJS — Notas Importantes

- **Versão**: carregada via CDN (`grapesjs@0.21.x`)
- **Plugin**: `gjs-blocks-basic` (flexGrid: true)
- **storageManager: false** — nunca salva automaticamente em localStorage
- **removeType('video')** — ESSENCIAL para vídeos funcionarem. Sem isso, GrapesJS trata `<video>` com componente próprio que ignora src do HTML
- **CSS injection**: nunca usar `editor.setStyle()` — destrói CSS. Sempre usar `injectCSSIntoCanvas()`
- **DOM manipulation**: após qualquer alteração direta no DOM, resyncar com `editor.setComponents(html)` + `fixVideoComponents()` + `injectCSSIntoCanvas(css)`
- Canvas é um `<iframe>` — CSS precisa ser injetado no `document` DESSE iframe, não na página principal
- Replo/page builders usam backgrounds em classes CSS → só `getComputedStyle()` detecta, não atributos inline
