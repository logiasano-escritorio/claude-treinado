---
name: Guias de design Sano/Relívia
description: Onde achar os padrões fixos de design para advertoriais e páginas de produto Sano
type: reference
originSessionId: 9bbd0c8a-00d5-4eda-b291-249f584c7558
---
O projeto Sanologia tem 2 guias de design oficiais na raiz:

- **`c:\Users\user\Desktop\Sanologia\ADVERTORIAL_DESIGN_GUIDE.md`** — para arquivos `adv-*.html` (advertoriais editoriais). Página de referência: `adv-b12-omeprazol-b12.html`.

- **`c:\Users\user\Desktop\Sanologia\PRODUCT_PAGE_DESIGN_GUIDE.md`** — para páginas de produto Shopify-style (`pag-*.html`, `[produto].html`). Página de referência: `strongbones.html`.

**Quando usar cada um:**
- Criar/modificar `adv-*.html` → ADVERTORIAL_DESIGN_GUIDE
- Criar/modificar página de produto com galeria, variantes, preço, checkout direto → PRODUCT_PAGE_DESIGN_GUIDE

**Regras compartilhadas pelos dois guias:**
- Paleta: só azul navy `#1e3a8a` + branco + cinzas neutros (zero outras cores)
- Fonte: Montserrat (UI) + Georgia (corpo de texto longo)
- CSS sempre inline (não usar `<link href="/style.css">` — caminho absoluto quebra)
- Texto branco em fundos azuis escuros (regra absoluta de contraste)
- Sem emojis decorativos
- Avatares de comentários: sempre fotos reais via `randomuser.me/api/portraits/[men|women]/[N].jpg`

**Diferenças críticas:**
- Advertorial = modo leitura, NUNCA exibe preço
- Página de produto = modo decisão, preço SEMPRE em destaque
