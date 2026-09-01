---
name: Oferta padrão Sano (todos produtos) — Compre X Ganhe Y
description: Estrutura oficial de 4 tiers Compre X Ganhe Y usada em TODOS os produtos Sano (atualizada 2026-05-11)
type: reference
originSessionId: 9bd6982e-c870-4b26-bb8d-a96c2fc679cf
---
**Padrão oficial v2 (2026-05-10) — 4 tiers Compre X Ganhe Y** validado em vendas reais no StrongBones-Artrose:

| # | Tier | Preço | Mecânica | R$/pote | "De" (riscado) | Selo |
|---|------|-------|----------|---------|----------------|------|
| 1 | 1 Pote (Starter) | **R$ 149** | 1 pote · 30 dias | R$ 149 | — | _opacity 0.92, parece "subdose"_ |
| 2 | 3 Potes ⭐ | **R$ 298** | Compre 2 Ganhe 1 · 90 dias | R$ 99,33 | ~~R$ 447~~ | `★ MAIS ESCOLHIDO` (dourado #c9a961, scale 1.04) |
| 3 | 6 Potes | **R$ 447** | Compre 3 Ganhe 3 · 180 dias | R$ 74,50 | ~~R$ 894~~ | `MAIS RESULTADO` |
| 4 | 10 Potes (Best) | **R$ 596** | Compre 4 Ganhe 6 · 300 dias | R$ 59,60 | ~~R$ 1.490~~ | `MELHOR VALOR` (borda navy 2.5px) |

**Mecânica chave:** a matemática fecha em R$ 149/pote (preço base). 2× R$149 = R$298, 3× R$149 = R$447, 4× R$149 = R$596. Cliente faz a conta de cabeça e a oferta parece justa. **Não inventar preços que não fecham a conta.**

**Default ativo no HTML:** tier 2 (3 potes R$ 298) — `<div class="variant-card variant-card--featured active" ...>`

**Frete:** grátis em todos os tiers (Yampi não permite frete diferente por variação — ver `feedback_yampi_frete_por_produto`).

**Order bump:** R$ 69 (1 pote extra) — configurar manualmente no Yampi por produto.

---

## CSS necessário (classes específicas)

Cada tier tem **modificador de classe** que cria a hierarquia visual:

- `.variant-card--starter` — fundo `#f8f9fb`, opacity 0.92, nome em cinza
- `.variant-card--featured` — borda dourada `#c9a961` 3px + `scale(1.04)` + sombra dourada
- `.variant-card--best` — borda navy reforçada 2.5px
- (tier 3 sem modificador especial — borda navy padrão)

**Elementos extras dentro de cada card:**
- `.variant-card__deal` — "Compre X Ganhe Y GRÁTIS" em verde uppercase
- `.variant-card__price-from` — preço cheio riscado
- `.variant-card__perpot` — "R$ XX,XX / pote"
- `.variant-card__save` — badge verde "VOCÊ ECONOMIZA R$ X"
- `.variant-card__shipping--free` — "✦ FRETE GRÁTIS"

**Hint acima dos cards** (justifica racionalmente o tier maior):
> *"A [contexto-específico] leva **5 a 8 semanas**. Por isso 73% dos clientes escolhem o kit com 3+ potes."*

Contexto muda por produto (artrose: "remineralização óssea"; B12: "reposição de B12"; etc).

---

## Yampi — IDs por produto

**Domínio:** `sano-suplementos.pay.yampi.com.br`

### StrongBones (cálcio + D3 / gomas) ✅
- 1 Pote: `5HLN6SEI05`
- 3 Potes: `I96GVFA6EC` ⭐
- 6 Potes: `CM6PL8MKLW`
- 10 Potes: `RYY48CH8QC`

### B12 (gomas) ✅
- 1 Frasco: `9YGC6ALHMQ`
- 3 Frascos: `3DWJ33INDL` ⭐
- 6 Frascos: `D3S7CKLGHF`
- 10 Frascos: `6DE5T41K8K`

### GlowUp, Magnésio — ⏳ pendente
Criar 4 produtos novos no Yampi com preços R$149/298/447/596 + frete grátis + order bump R$69.

---

## Onde está implementado

✅ `Sanologia/strongbones-artrose-v2.html` (funil artrose — vendendo)
✅ `Sanologia/strongbones.html` (funil câimbras — pronto pra escalar)

⏳ Pendente replicar em:
- `Sanologia/b12/b12.html` + `b12-diabetes-metformina.html`
- `Sanologia/pag-glowup.html` + `pag-glowup-MENOPAUSA.html`
- `Sanologia/magnesio-gummies/magnesio-gummies.html`

**Arquivo template oficial:** `Sanologia/strongbones-artrose-v2.html` — CSS em ~327, variant-grid em ~2618.

**Doc completa no Obsidian:** `SANOLOGIA OBSIDIAN/Workflows/oferta-padrao-compre-x-ganhe-y.md`

---

## Métricas esperadas (baseado em Orégano Relívia, 131 vendas reais)

- Mix esperado: 37% 1-pote · 54% 3-potes (popular) · 9% 6-potes
- AOV blended: R$ 277
- CPA-alvo (30% margem): R$ 87
- Lucro mensal projeção (500 vendas): R$ 42k sem bump · R$ 49k com bump 35% take

---

## Histórico

- **2026-05-04** — Implementado pela primeira vez em `strongbones-artrose-v2.html`
- **2026-05-10** — Validado em vendas reais (primeira venda Pix StrongBones com mix funcionando)
- **2026-05-11** — Replicado em `strongbones.html` (câimbras) + salvo como padrão oficial no Obsidian
- **Anvisa:** preço sempre só na página de venda + checkout. Advertoriais (`adv-*.html`) NUNCA exibem preço
