---
name: Yampi não permite frete diferente por variação
description: No Yampi, frete é configurado a nível de PRODUTO, não de variação. Não dá pra cobrar frete só no tier "1 pote" e dar grátis nos outros — é tudo ou nada por produto.
type: feedback
originSessionId: 9bd6982e-c870-4b26-bb8d-a96c2fc679cf
---
No Yampi, regra de frete (fixo, grátis, calculado) é por **produto**, não por **variação**. Não é possível configurar:
- "1 pote: frete fixo R$13"
- "3 potes: frete grátis"
- "6 potes: frete grátis"

Tudo num mesmo produto compartilha a mesma regra de frete.

**Why:** já tentei propor isso no StrongBones-Artrose pra cobrar 50% do frete real (R$13 de R$26) só no tier 1 pote — implementei na página inteira (cards, top-banner, offer-strip, FAQ) e tive que reverter porque o Yampi não suporta. Cliente veria "+R$13 frete" na página mas o checkout cobraria outra coisa = abandono.

**How to apply:**
- Quando user pedir "cobra frete só no tier menor", responder na hora que Yampi não permite e propor alternativas:
  1. Aumentar o preço do tier menor em R$13 ("frete embutido" — ninguém percebe)
  2. Criar um **produto separado** no Yampi pra "kit 1 pote" com frete fixo, e outro produto pra os kits multi-pote com frete grátis (links de checkout diferentes)
  3. Manter frete grátis em todos e absorver o custo (mais simples mas come margem)
- Mesma regra vale pra outros produtos Sano (B12, GlowUp, Magnésio) — não tentar diferenciar frete por variação.
