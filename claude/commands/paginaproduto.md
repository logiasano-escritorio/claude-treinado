# Recriar Página HTML Relívia — Baseada em Referência

Você é especialista em criar landing pages standalone em HTML para a marca Relívia.

## OBJETIVO

O usuário vai fornecer a URL de um produto de referência (ou pasta local) e o handle do novo produto. Você deve **recriar a mesma estrutura visual** do template Relívia, substituindo todo o conteúdo pelo do novo produto. Se o produto de referência tiver seções que não existem no template Relívia, **crie-as do zero** seguindo a paleta e classes do template.

**Template de referência:** `c:/projetos/relivia/beterraba-relivia/beterraba.html`
**Mapa de seções e classes:** `c:/projetos/relivia/_template/sections-map.md`

---

## PASSO 1 — Receber informações

Se o usuário não forneceu, pergunte:
1. **URL do produto de referência** (ex: `https://marca.com/pages/produto`) OU pasta local
2. **Handle do novo produto** (ex: `magnesio`, `colageno`, `vitamina-d`)
3. **Idioma de saída** — PT-BR ou manter o idioma original? (perguntar sempre que o produto for em inglês ou outro idioma)

Se já forneceu, não pergunte novamente.

**Checar se a pasta já existe antes de continuar:**
```bash
ls c:/projetos/relivia/[handle]-relivia/ 2>/dev/null
```
Se existir, avisar o usuário e perguntar se quer sobrescrever.

---

## PASSO 2 — Extrair conteúdo via Playwright

Navegar na URL com `mcp__playwright__browser_navigate`, depois:

**2a. Dispensar popup/dialog imediatamente (preventivo):**
Usar `mcp__playwright__browser_handle_dialog` com `accept: false` logo após navegar — evita que modal de email/desconto trave a extração.

**2b. Scroll para forçar lazy-load das imagens:**
```js
() => {
  return new Promise(resolve => {
    let y = 0;
    const step = () => {
      window.scrollTo(0, y);
      y += 800;
      if (y < document.body.scrollHeight) setTimeout(step, 100);
      else { window.scrollTo(0, 0); resolve(); }
    };
    step();
  });
}
```

**2c. Rodar dois evaluate em paralelo após o scroll:**

**Evaluate 1 — Todo o texto:**
```js
() => document.body.innerText
```

**Evaluate 2 — Imagens únicas com y-position e extensão real:**
```js
() => {
  const imgs = Array.from(document.querySelectorAll('img'))
    .filter(img => !img.src.startsWith('data:') && img.naturalWidth > 30)
    .map(img => {
      const top = Math.round(img.getBoundingClientRect().top + window.scrollY);
      const url = img.src;
      const filename = url.split('/').pop().split('?')[0];
      const ext = filename.includes('.') ? filename.split('.').pop().toLowerCase() : 'jpg';
      return `${filename} | y=${top}px | w=${img.naturalWidth} | ext=${ext} | src=${url}`;
    });
  const seen = new Set();
  return imgs.filter(l => {
    const f = l.split('|')[0].trim();
    if (seen.has(f)) return false;
    seen.add(f); return true;
  }).join('\n');
}
```

Após extrair, fechar o browser imediatamente: `mcp__playwright__browser_close`

---

## PASSO 3 — Mapear seções presentes

Com o texto extraído, identificar quais seções o produto de referência tem:

| Seção | Presente? |
|---|---|
| Galeria de produto | |
| Variantes/bundle | |
| Rich text com checklist | |
| Image-with-text (x quantas?) | |
| GIF row / animações | |
| Compounds/ingredientes grid | |
| Stats / números clínicos | |
| Depoimentos (x quantos?) | |
| FB comments | |
| Multirow (como usar / resultados) | |
| Tabela comparativa | |
| Garantia | |
| FAQ (x perguntas?) | |
| CTA final | |
| **Seções extras não presentes no template** → criar do zero seguindo paleta Relívia |

---

## PASSO 4 — Baixar imagens e nomear semanticamente

Checar se pasta existe, criar se não:
```bash
mkdir -p "c:/projetos/relivia/[handle]-relivia/images"
```

Usar a combinação de **y-position + largura (w)** para classificar — `w` é mais confiável que `y` para identificar o tipo de imagem:

| Critério principal | Slot | Nome do arquivo |
|---|---|---|
| w > 100, y < 100 | Logo da marca | `logo.png` |
| w > 800, primeiras ocorrências (galeria) | Slides da galeria | `produto-1.[ext]`, `produto-2.[ext]`, ... |
| w ~ 200–400, múltiplas no mesmo y (bundle icons) | Ícones de kit/bundle | `bundle-1.[ext]`, `bundle-2.[ext]`, ... |
| w > 500, y ~ 1000–1300, única | Pagamentos / trust | `pagamentos.[ext]` |
| w > 400, y ~ 1000–1400, única diferente | Caridade / missão | `missao.[ext]` |
| w > 400, primeira IWT abaixo da hero | IWT seção 1 | `info-1.[ext]` |
| w > 400, segunda IWT | IWT seção 2 | `info-2.[ext]` |
| w > 800, seção comparativo/ingredientes | Comparativo | `comparativo.[ext]` |
| w > 800, seção resultados/timeline | Resultados | `resultados.[ext]` |
| w ~ 800–1200, múltiplas, seção reviews | Fotos de depoimentos | `review-1.[ext]`, `review-2.[ext]`, ... |
| w ~ 800–1200, múltiplas, seção benefícios | Grid de benefícios | `beneficio-1.[ext]`, `beneficio-2.[ext]`, ... |
| w > 1500, próximo ao fim da página | CTA final / promessa | `cta-final.[ext]` |

**Usar a extensão real detectada no evaluate** (`.webp`, `.jpg`, `.png`, `.gif`) — nunca forçar `.png`.

**Download em batch:**
```bash
curl -sL -o "c:/projetos/relivia/[handle]-relivia/images/produto-1.webp" "URL_1"
# ... repetir para cada imagem
```

**Validar que os arquivos foram baixados (tamanho > 0):**
```bash
ls -la "c:/projetos/relivia/[handle]-relivia/images/"
```
Se algum arquivo tiver 0 bytes, tentar novamente com a URL correta.

**NÃO baixar — manter URL externa:**
- Avatares FB: `https://i.pravatar.cc/...` (gerados dinamicamente)
- Selos e GIFs checkoutchamp (CDN próprio, estável)
- Badge de garantia checkoutchamp

---

## PASSO 5 — Copiar style.css

```bash
cp "c:/projetos/relivia/beterraba-relivia/style.css" "c:/projetos/relivia/[handle]-relivia/style.css"
```

---

## PASSO 6 — Gerar o HTML via Agent

Usar `Agent` (subagent_type: general-purpose) passando:
- Instrução para ler `c:/projetos/relivia/_template/sections-map.md` (estrutura leve) — **não precisa reler o beterraba.html inteiro se o sections-map.md for suficiente**
- Todo o texto extraído
- Lista de imagens com nomes semânticos e extensões reais
- Lista de seções presentes + seções extras para criar do zero

**Prompt base para o Agent:**
> "Leia `c:/projetos/relivia/_template/sections-map.md` para entender a estrutura do template Relívia. Crie `c:/projetos/relivia/[handle]-relivia/[handle].html` com a estrutura IDÊNTICA do template (mesmas classes CSS, mesmo JS, mesmas seções na mesma ordem). Substitua apenas o conteúdo pelo do novo produto. Se houver seções do produto de referência que não existem no template, crie-as do zero seguindo a paleta e padrão de classes Relívia. Use `images/nome.ext` para todas as imagens do produto (caminhos locais). [colar texto extraído + lista de imagens nomeadas + idioma de saída]"

### Regras de substituição

**Substituir:**
- Título, subtítulo, tagline, meta title
- Copy de todas as seções — no idioma definido no PASSO 1
- Variantes: nome, preço, preço original — placeholders `LINK_CHECKOUT_1/2/3`
- Depoimentos: nome, texto, estrelas — fotos em `images/review-N.[ext]`
- FAQ: perguntas e respostas
- Tabela comparativa: características e nome do produto
- Textos do CTA e garantia
- Banner de topo
- Comentários FB: adaptar sintomas/resultados ao novo produto
- Imagens: `images/nome-semantico.[ext]` (caminhos locais, extensão real)
- Countdown/timer: se presente na referência, adaptar como badge de urgência (não recriar JS de countdown)

**Manter idêntico:**
- Todas as classes CSS
- JS (accordion, variant picker, gallery)
- `<style>` internos do `<head>`
- Trust bar, pixel FB `1853242508916971`, ondas SVG
- Selos checkoutchamp (URLs externas)
- Avatares pravatar.cc (URLs externas)
- Urgência: "17 unidades restantes" (se não informado)
- Garantia: 90 dias (se não informada)

### Seções novas (não presentes no template)
Seguir a paleta e padrão Relívia:
- Fundo: alternar `--white` e `--gray` entre seções
- Nunca usar roxo, vermelho ou fundo escuro
- Usar as mesmas classes de container, heading e tipografia do template
- Criar CSS inline no `<head>` se precisar de classes novas

### Estrutura variant-card obrigatória
```html
<div class="variant-card" data-checkout="LINK_CHECKOUT_1" data-price="R$ 97,00" data-price-original="R$ 197,00">
  <div class="variant-card__check">✓</div>
  <!-- opcional: <div class="variant-card__popular">+ POPULAR</div> ou MELHOR VALOR -->
  <div class="variant-card__name">1 Frasco</div>
  <div class="variant-card__sub">30 doses · 1 mês</div>
  <div class="variant-card__price">R$ 97,00</div>
</div>
```

---

## PASSO 7 — Verificar resultado

```bash
ls -la "c:/projetos/relivia/[handle]-relivia/"
ls -la "c:/projetos/relivia/[handle]-relivia/images/"
```

Confirmar:
- `[handle].html` existe e tem tamanho > 0
- `style.css` existe
- Todas as imagens em `images/` têm tamanho > 0
- Nenhuma imagem com 0 bytes (falha de download)

---

## PASSO 8 — Atualizar links de checkout (quando o usuário fornecer)

Substituir `LINK_CHECKOUT_1`, `LINK_CHECKOUT_2`, `LINK_CHECKOUT_3` nos atributos `data-checkout` e no `href` do CTA principal. Usar `replace_all: true`.

---

## Regras gerais

- Copy em **Português Brasileiro** persuasivo por padrão — salvo se usuário definir outro idioma no PASSO 1
- Nunca usar roxo, vermelho ou fundo escuro em seções de conteúdo
- Header: fundo branco com border-bottom sutil
- Footer: fundo `#111111` (preto)
- Logo: `images/logo.png` (caminho relativo)
- Disclaimer stats: `*Resultados baseados em pesquisa voluntária...`
- Countdown/timer da referência: converter em badge de urgência estático, não recriar JS
- Extensão de imagens: sempre usar a extensão real (`.webp`, `.jpg`, `.png`, `.gif`) — nunca forçar `.png`
