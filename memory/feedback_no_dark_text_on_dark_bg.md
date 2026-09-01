---
name: Nunca usar texto escuro em fundo azul escuro
description: Em qualquer elemento com fundo azul navy (product-box, cta-final, footer, etc), texto auxiliar deve ser branco ou branco translúcido — nunca azul escuro ou cinza escuro
type: feedback
originSessionId: 9bbd0c8a-00d5-4eda-b291-249f584c7558
---
Em qualquer elemento com fundo azul escuro (`#1e3a8a`, `#162d6e`, `#0c1f4a`, `#1a1a2e`), o texto deve ser branco ou branco translúcido. Texto azul navy ou cinza escuro sobre fundo azul escuro fica ilegível.

**Why:** Já aconteceu na `adv-strongbones-caimbras.html` — o `.product-desc` (descrição abaixo do nome do produto dentro do `.product-box`) ficou cinza escuro num gradient azul, virou texto invisível. O mesmo padrão pode quebrar em `cta-final`, `footer`, qualquer área com fundo escuro.

**How to apply:**
- Em `.product-box` (gradient azul), TODO texto interno deve ser `#ffffff` ou `rgba(255,255,255,X)` com X de 0.6-1.0
- Em `.cta-final` / `.final-cta` (background `#1a1a2e`), mesma regra
- Em `footer` / `.site-footer` (background `#0c1f4a`), mesma regra
- Antes de aplicar texto sobre fundo, sempre verificar contraste mínimo 4.5:1 (texto normal) ou 3:1 (texto grande/bold)
- Cinzas escuros (`#333`, `#444`, `#555`, `#666`) só em fundos brancos ou cinza muito claro
- Azul navy `#1e3a8a` em texto: só sobre branco ou `#eef2fb` (azul muito claro)

**Verificação rápida:**
- Se o background é escuro → texto branco ou branco translúcido
- Se o background é claro → texto pode ser navy ou cinza escuro
- Nunca: navy sobre navy, cinza escuro sobre navy, navy sobre cinza escuro

**Pegadinha comum (já aconteceu na strongbones-artrose-v2 tabs Suporte/Inside/Why):**
Quando o container tem fundo escuro e cor branca no `<p>`, mas o texto contém `<strong>`, `<em>` ou `<span>` — esses elementos herdam a cor escura padrão do CSS global e ficam INVISÍVEIS. Sempre forçar:
```css
.container,
.container * { color: #ffffff; }
.container strong { color: #ffffff; font-weight: 800; }
.container em { color: #ffffff; font-style: italic; }
```
Antes de marcar tarefa como concluída em qualquer seção com fundo navy, fazer ctrl+F por `<strong>` e `<em>` na seção e validar que estão estilizados.
