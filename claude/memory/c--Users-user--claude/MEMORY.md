# Claude Memory — Relívia

> **ATENÇÃO:** Farma Vive não existe mais. O único cliente ativo é a **Relívia** (reliviaonline.shop).

## PROJETOS ATIVOS

### Editor Visual — Ferramenta Local (HTML + Node.js)
- Arquivo principal: `C:/projetos/editor-visual/editor-visual.html`
- Servidor backend: `C:/projetos/editor-visual/servidor/` (Node.js + Puppeteer)
- Scripts de manutenção: `C:/projetos/editor-visual/scripts/`
- → Ver detalhes técnicos completos: [editor-visual.md](editor-visual.md)
- Status: Funcionando — importação por URL, imagens OK, vídeos OK, botão 🔧 Produto OK

### Editor Visual — Funcionalidades adicionadas (Mar 2026):
- **👁 Preview**: publica HTML em `localhost:3001/preview` → Claude analisa via Playwright
- **🔧 Produto**: detecta seção de produto Shopify quebrada e substitui por template limpo Relívia
  - `extractProductData(doc)` — extrai imagens, título, preço, bullets, rating do DOM Shopify
  - `generateCleanProductSection(data)` — gera HTML no estilo vitalpulser (galeria slides, variantes com data-checkout, trust bar, urgência). CSS `rp-*` embutido inline
  - `convertProductSection()` — orquestra detecção + extração + substituição no GrapesJS
  - Placeholders: `LINK_CHECKOUT_1/2/3` nos cards de variante
- **Export modal**: campo de URL de checkout → substitui todos os botões de carrinho antes de baixar
- **`cleanExportHTML(html, checkoutUrl)`**: remove overlays Moonbundle, UUIDs visíveis, iframes, banners de cookie, fixa nav Shopify, desativa forms, substitui links de cart
- **`buildFullHTML(html, css)`**: encapsula HTML em página standalone com resetCSS (`pointer-events:auto!important`) e polyfillJS (galeria thumbs, accordion FAQ, disable forms)
- **`replaceCartURLs(doc, url)`**: substitui links/botões de compra por URL de checkout externo

### ATENÇÃO — Bug crítico buildFullHTML (corrigido):
- O arquivo tinha `\`` (backslash+backtick) e `\${html}` no `buildFullHTML` → SyntaxError no V8 moderno → TODO o JS parava
- Fix aplicado em Mar 2026 via `C:/projetos/editor-visual/scripts/fix-editor2.py` e `fix-editor3.py`
- **NUNCA usar `\`` para delimitar template literals** — usar `` ` `` diretamente
- **NUNCA usar `\${var}` dentro de template literals** — usar `${var}` diretamente

### Editor Visual — Injeção de código (scripts auxiliares):
- Usar `Desktop/relivia/` para scripts Python quando Write falha no Desktop
- Padrão: ler arquivo → encontrar posição → inserir/substituir → escrever de volta
- Verificar sintaxe JS: `powershell.exe -Command "& 'C:\Program Files\nodejs\node.exe' --check arquivo.js"`

### Relívia — Shopify (Tema: Shrine Pro)
- Loja: reliviaonline.shop (Shopify)
- ~~Farma Vive (afarmavive.myshopify.com) — ENCERRADA~~
- Tema exportado: `C:/Users/user/Downloads/theme_export__afarmavive-shop-theme-export-reliviaessential-online-shrine-pr__26FEB2026-0555pm/`
- Templates de produto ficam em: `templates/` (formato: `product.[handle].json`)
- Saída de arquivos criados: Desktop do usuário

### Relívia — Landing Pages HTML (fora do Shopify)
- Pasta do projeto: `C:/Users/user/Desktop/relivia/`
- CSS compartilhado: `relivia/style.css` (design system completo)
- Imagens: `relivia/imagens/`
- **Logo**: `C:/Users/user/Desktop/relivia/relivialogo.png` — arquivo local, copiar para cada projeto como `images/logo.png` e referenciar relativamente. NUNCA usar a URL externa `https://reliviaonline.shop/images/logorelivia.png`
- Total previsto: 7 páginas de produto (1 criada + 6 a criar)
- Fluxo: usuário fornece `product.[handle].json` → gerar HTML linkando `style.css`
- CTA padrão: link externo (substituir `LINK_CHECKOUT` em cada página)

### Paleta Oficial Relívia (v2.0 — FINAL):
- Azul principal: `#2E2BFF` — `--blue`       (botões, preços, badges, urgência, CTA bg)
- Azul escuro:    `#1B17FF` — `--blue-dark`  (hovers, wave divider fill)
- Branco:         `#ffffff` — `--white`
- Cinza fundo:    `#F5F6F8` — `--gray`       (seções alternadas, cards, multirow, accordion)
- Preto texto:    `#111111` — `--text`        (body, títulos, footer bg)
- Muted:          `#666666` — `--muted`       (texto secundário)
- Estrelas:       `#ffcc00` — `--stars`       (único elemento colorido além do azul)
- SEM roxo, SEM vermelho, SEM fundo escuro em seções
- Header: fundo BRANCO com border-bottom sutil
- Footer: fundo #111111 (preto texto)

---

## PROJETOS EM PLANEJAMENTO

### SaaS — Gerador Internacional de Landing Pages
→ Ver roadmap completo: [saas-roadmap.md](saas-roadmap.md)
- Construir dentro do editor-visual existente (Node.js + Puppeteer)
- Fluxo: URL Shopify → extrai conteúdo + cores + logo → Claude API → HTML localizado
- Fase atual: **Fase 1 (não iniciada)** — MVP núcleo

---

## DOCUMENTAÇÃO TÉCNICA

### Shrine Pro — Seções
→ Ver: [shrine-pro-sections.md](shrine-pro-sections.md)
Contém schemas completos de todas as seções disponíveis:
- Seções de produto: main-product, image-with-text, rich-text, collapsible-content, multirow, testimonials, related-products, section-divider
- Seções de marketing: comparison-table, pricing-table, bundle-deals, facebook-testimonials, product-features, icons-with-content, content-tabs, multicolumn, icon-bar, logo-list, horizontal-ticker, vertical-ticker
- Seções de hero/mídia: image-banner, parallax-hero, slideshow-hero, image-slider, video, comparison-slider
- Utilitários: custom-columns, custom-liquid

---

## PÁGINAS CRIADAS

### TheraWrap™ — Página de Produto (Shopify JSON)
- Arquivo: `C:/Users/user/Desktop/shopify-therawrap.json`
- Status: Criado — aguardando revisão do usuário

### AlinhaFácil™ — Landing Page HTML (Relívia)
- Arquivo: `C:/Users/user/Desktop/relivia/alinhafacil.html`
- CSS: `relivia/style.css`
- JSON fonte: `product.alinhafacil.json` (tema brasilrelivia, 03MAR2026)
- Variantes: Médio (40-80kg) e Grande (80-120kg) — ambos R$297
- Status: Criado — placeholders nos lugares de imagens/vídeos

---

## FLUXO DE TRABALHO — GEMPAGES → HTML ESTÁTICO

### Problema
GemPages salva HTML sujo (scripts Shopify, barra preview, boilerplate) → arquivo grande → queima tokens ao enviar para Claude.

### Solução: script local `gempages-limpar.py`
- Localização: `C:/Users/user/Desktop/gempages-limpar.py`
- Uso: `python gempages-limpar.py arquivo.html`
- O que faz: remove scripts, barra GemPages, preloads, comentários, meta Shopify → preserva pixel FB, CSS variables, imagens
- Redução típica: 70-80% do tamanho
- Inclui CSS fix para desktop (max-width: 860px centralizado)

### Passos para converter qualquer página GemPages:
1. Abrir a página no Chrome (mobile ou desktop)
2. Aguardar carregar completamente
3. `Ctrl+S` → **"Página da web, somente HTML"** → salvar no Desktop
4. No terminal: `python gempages-limpar.py nome-arquivo.html`
5. Arquivo `-clean.html` gerado no mesmo diretório
6. Se precisar de ajustes visuais, **enviar o arquivo -clean.html** para Claude (muito menor)

### Notas técnicas GemPages:
- CSS variables (`--ff`, `--c`, `--size`) são CSS nativo — funcionam sem JS
- Elementos `<gp-*>` renderizam como block sem JS (conteúdo visível, estilo pode variar)
- Desktop costuma quebrar por max-width não configurado — fix já está no script

---

## FLUXO DE TRABALHO — HOSPEDAR PÁGINA EXTERNA (self-host)

### Problema
Páginas de terceiros (GemPages/CheckoutChamp) carregam imagens via JS lazy load — o HTML salvo com Ctrl+S não contém as URLs reais.

### Scripts (Desktop):
- `workflow-pagina.py` — script principal (configurar e rodar)
- `nova-pagina.bat` — **comando**: abre o script para configurar e executa em sequência

### Comando para nova página:
Dar duplo clique em `nova-pagina.bat` no Desktop

### Passos:
1. **Chrome**: scroll lento topo→fim (lazy load)
2. **Console**: rodar script de extração → copiar URLs
3. **Console**: `copy(document.documentElement.outerHTML)` → colar no Bloco de Notas → salvar como `.html`
4. **`nova-pagina.bat`**: abre `workflow-pagina.py` → configurar 3 variáveis (`NOME_PROJETO`, `HTML_ENTRADA`, `URLS`) → fechar → roda automaticamente
5. Hospedar pasta de mídias + HTML gerado em `/relivia/[projeto]/`

### Chave técnica:
- `Ctrl+S` captura HTML estático (sem URLs lazy) → usar `copy(outerHTML)` no console
- Script substitui URLs externas pelas locais com regex
- Verificação final: confirma 0 URLs externas restantes

---

## FLUXO DE TRABALHO — CRIAR PÁGINA SHOPIFY

1. Usuário fornece URL de referência + produto a criar
2. Extrair conteúdo via DevTools: `document.getElementById('MainContent').innerText`
3. Traduzir para PT-BR mantendo copy persuasivo
4. Mapear conteúdo às seções do Shrine Pro (ver shrine-pro-sections.md)
5. Gerar JSON válido seguindo estrutura de template Shopify
6. Salvar em `C:/Users/user/Desktop/shopify-[nome-produto].json`

### Regras críticas do JSON:
- `type` da seção = nome do arquivo `.liquid` sem extensão
- IDs únicos alfanuméricos para seções e blocos
- `block_order` deve listar todos os blocos em ordem
- `order` deve listar todas as seções em ordem
- image_picker vazio = `""` (nunca `null`)
- Para cores customizadas: `color_scheme: "custom"` + `custom_colors_background`, `custom_colors_text`, etc.

---

## FLUXO DE TRABALHO — RECRIAR PÁGINA PARA OUTRO IDIOMA/MERCADO

### Comando
```
recrie o [Produto] para [idioma] seguindo referencias culturais, nomes, cidades e precos "[caminho do .html PT-BR]"
```

### Como extrair o HTML de uma página Shopify (quando não há .html pronto):
1. Abrir a página no Chrome com a página carregada
2. `F12` → Console → rodar:
   ```js
   copy(document.getElementById('MainContent').outerHTML)
   ```
3. Colar num `.html` e salvar no Desktop

### O que Claude faz:
1. Lê o HTML → extrai copy, seções, depoimentos, FAQ, nomes de imagens
2. **Ignora** o bloco de produto nativo do Shopify (costuma vir quebrado)
3. **Gera bloco de produto padrão Relívia** — galeria slides + cards de variante (data-checkout) + trust bar + urgência
4. Adapta culturalmente para o mercado alvo: nomes, cidades, médicos, moeda, contato
5. Salva em `relivia/[produto]/[produto]-[idioma].html` com `style.css` local

### Adaptações por mercado:
- **Italiano (IT)**: nomes IT, cidades (Roma/Milano/Napoli/Torino/etc), €, médicos Dott./Dott.ssa, telefone +39
- **Espanhol (ES)**: nomes ES, cidades (Madrid/Barcelona/Sevilla/etc), €, médicos Dr./Dra.
- **Inglês (UK)**: nomes EN, cidades (London/Manchester/etc), £
- **Inglês (US)**: nomes EN, cidades (NYC/LA/Chicago/etc), $

### Estrutura do arquivo gerado:
- `<link rel="stylesheet" href="style.css" />` — CSS local da pasta do produto
- Classes HTML idênticas ao original PT (`.product-grid`, `.gallery__slide`, `.variant-card`, `.tcard`, etc.)
- Caminhos de imagem idênticos ao PT (funcionam via editor-server localhost:3001)
- JS: `galleryNav()`, `toggleAcc()`, seletor de variantes por click

---

## SKILLS

### Seção Facebook Comments (`/fb-comentarios`)
- Comando: `/fb-comentarios`
- Uso: fornecer o HTML da página → lê o produto, gera 10-13 comentários coerentes com a copy
- CSS + HTML inseridos automaticamente no arquivo
- Posição padrão: após seção DEPOIMENTOS

### Tradução PT-BR Profissional
→ Ver: [traducao-ptbr.md](traducao-ptbr.md)
- Usar sempre que traduzir textos de páginas/produtos para o usuário
- Regras: naturalidade BR, localização cultural, moeda em R$, datas em formato BR
- Manter estrutura/formatação original, preservar nomes de instituições reais

---

## PREFERÊNCIAS DO USUÁRIO
- Comunicação: Português Brasileiro
- Arquivos de output: Desktop (`C:/Users/user/Desktop/`)
- Não fazer nada sem instrução explícita do usuário
