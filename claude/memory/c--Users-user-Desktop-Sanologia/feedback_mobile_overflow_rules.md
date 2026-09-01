---
name: Regras obrigatórias de responsividade mobile (zero overflow horizontal)
description: 4 regras CSS que TODA página Sano deve ter para evitar overflow horizontal em mobile — bug recorrente
type: feedback
originSessionId: 9bbd0c8a-00d5-4eda-b291-249f584c7558
---
Toda página Sano (advertorial OU produto) DEVE ter estas 4 regras CSS no início do `<style>` para garantir que nunca aconteça overflow horizontal em mobile.

**Why:** Já aconteceu múltiplas vezes — o último caso foi a `b12/b12.html` em produção, onde um `<video>` com 720px de largura intrínseca empurrava a página inteira pra fora do viewport mobile, fazendo o navegador encolher tudo até virar uma faixa minúscula. Vídeos sem `max-width: 100%` + grid items sem `min-width: 0` são as armadilhas mais comuns.

**How to apply (CSS obrigatório no `<style>`):**

```css
/* 1. Forçar imagens E vídeos a respeitarem o container */
img, video {
  max-width: 100%;
  height: auto;
  display: block;
}

/* 2. Grid items não devem estourar pelo conteúdo intrínseco
   (vídeos/imagens com largura natural maior que a coluna) */
.iwt-grid > *,
.product-grid > *,
.multirow-row > *,
.compounds-grid > *,
.tgrid > *,
.stats-grid > *,
.gif-row > *,
.variant-grid > * {
  min-width: 0;
}

/* 3. Defesa final: bloquear scroll horizontal globalmente */
html {
  scroll-behavior: smooth;
  overflow-x: hidden;
}
body {
  overflow-x: hidden;
}

/* 4. Tabelas largas (comparativas) DEVEM ter wrap com scroll horizontal próprio */
.ctable-wrap {
  overflow-x: auto;  /* tabela rola dentro da própria caixa, não da página */
}
.ctable {
  min-width: 640px;  /* só dentro do wrap */
}
```

**Verificação obrigatória após criar/modificar página:**

```js
// Cole no DevTools Console em viewport mobile (375px ou 390px):
({
  docW: document.documentElement.clientWidth,
  scrollW: document.body.scrollWidth,
  hasOverflow: document.body.scrollWidth > document.documentElement.clientWidth + 2
})
// hasOverflow DEVE ser false
```

**Sintomas de overflow horizontal em mobile:**
- Página inteira aparece "encolhida" (tudo minúsculo, scrollbar horizontal visível)
- Navegador adiciona scroll horizontal indesejado
- Layout aparenta funcionar mas o body é mais largo que o viewport

**Causas mais comuns (em ordem de frequência):**
1. `<video>` sem `max-width: 100%` (largura intrínseca 720px+)
2. `<img>` sem `max-width: 100%`
3. Grid items sem `min-width: 0` (default `min-content` empurra)
4. `<table>` larga sem wrap com `overflow-x: auto`
5. Elemento com `width: 100vw` dentro de container com padding (estoura por causa do scrollbar)
6. Position absolute/fixed com `right: -X` ou `left: 100%`
