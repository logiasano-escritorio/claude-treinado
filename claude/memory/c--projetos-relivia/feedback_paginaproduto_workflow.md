---
name: Workflow correto para /paginaproduto com site externo
description: Passo a passo exato que funciona para recriar página de produto standalone baseada em site externo (Shopify/GemPages), sem desperdício de tokens
type: feedback
---

Quando o produto de referência é um site externo (não uma pasta local), seguir este fluxo exato:

## PASSO 1 — Extrair conteúdo via Playwright (não ler HTML local)

Navegar direto para a URL ao vivo com `mcp__playwright__browser_navigate`, depois rodar dois `evaluate` em paralelo:

```js
// Evaluate 1 — todo o texto
() => document.body.innerText

// Evaluate 2 — imagens únicas com posição y
() => {
  const imgs = Array.from(document.querySelectorAll('img'))
    .filter(img => !img.src.startsWith('data:') && img.naturalWidth > 30)
    .map((img, i) => {
      const top = Math.round(img.getBoundingClientRect().top + window.scrollY);
      const filename = img.src.split('/').pop().split('?')[0];
      return `${filename} | y=${top}px | alt: ${img.alt || '(none)'} | w=${img.naturalWidth}`;
    });
  const seen = new Set();
  return imgs.filter(l => { const f = l.split('|')[0].trim(); if(seen.has(f)) return false; seen.add(f); return true; }).join('\n');
}
```

Fechar o browser logo após extrair: `mcp__playwright__browser_close`

**Por quê:** HTML de sites Shopify/GemPages tem 2MB+, inútil para ler localmente. As URLs do CDN da Shopify são permanentes e funcionam diretamente no HTML final.

## PASSO 2 — Copiar style.css imediatamente

```bash
cp c:/projetos/relivia/beterraba-relivia/style.css c:/projetos/relivia/[handle]-relivia/style.css
```

Fazer isso ANTES de criar o HTML.

## PASSO 3 — Criar o HTML com Agent (não inline)

Usar `Agent` com subagent_type `general-purpose` passando:
- Instrução clara: "leia o beterraba.html completo e copie a estrutura IDÊNTICA"
- Todo o conteúdo extraído (textos + URLs de imagens) já no prompt
- Destino do arquivo no prompt

**Por quê:** O HTML final tem ~1100 linhas. Gerar inline no contexto principal consome tokens demais e causa "Not responding". O Agent protege o contexto principal.

## PASSO 4 — Verificar resultado

```bash
ls c:/projetos/relivia/[handle]-relivia/*.html c:/projetos/relivia/[handle]-relivia/*.css
```

---

**Why:** Na sessão do etiope-relivia, tentamos ler o HTML local (2.1MB, falhou), depois extrair via Playwright de forma fragmentada (múltiplos roundtrips), depois gerar o HTML inline (causou "Not responding"). O fluxo correto é: Playwright → fechar browser → cp style.css → Agent gera HTML.

## PASSO 2b — Baixar imagens localmente (obrigatório)

Após extrair as URLs, baixar todas as imagens para `[handle]-relivia/images/` antes de criar o HTML:

```bash
mkdir -p c:/projetos/relivia/[handle]-relivia/images
# Para cada URL extraída:
curl -s -o "c:/projetos/relivia/[handle]-relivia/images/NOME.ext" "URL_DA_IMAGEM"
```

Ou em batch com wget:
```bash
wget -P c:/projetos/relivia/[handle]-relivia/images/ URL1 URL2 URL3 ...
```

No HTML, referenciar como `images/NOME.ext` (caminho relativo).

**Por quê:** URLs do CDN Shopify caem quando o lojista deleta o produto ou fecha a loja. Imagens devem sempre ser hospedadas localmente.

---

**How to apply:** Sempre que o usuário pedir /paginaproduto com referência externa (URL ou pasta de site salvo), seguir este fluxo em vez de tentar ler o HTML local.
