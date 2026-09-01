---
name: Advertoriais nunca exibem preço
description: Advertoriais da Relívia/Sano nunca devem mostrar preço, parcelamento ou desconto — preço fica só na landing page de checkout
type: feedback
originSessionId: 9bbd0c8a-00d5-4eda-b291-249f584c7558
---
Advertoriais (páginas tipo `adv-*.html`) NUNCA devem exibir preço, valor parcelado, valor riscado ou desconto. Tudo que envolve número monetário sai da página de advertorial.

**Why:** Advertorial é página editorial em modo leitura — o leitor está em modo informativo, não modo avaliação de compra. Mostrar preço quebra o frame editorial e ativa resistência a anúncio. O preço aparece só depois do clique no CTA, na landing page de checkout (`pagamento.reliviaonline.com/...`), onde o leitor já está em modo decisão.

**How to apply:**
- Em qualquer arquivo `adv-*.html`, remover blocos `.product-price`, `.price-old`, `.price-main`, `.price-installment` e similares
- Subtexto do CTA (`.btn-sub`): nunca mencionar valor ("R$149,90", "12x de R$14,99"). Substituir por benefício ou trust signal ("Acesso seguro", "Compra protegida", "Compre 1 leve 2 + frete grátis")
- Final CTA: tirar referências a "R$X" e parcelamento — manter apenas mecânica de oferta sem números (ex: "Compre 1 leve 2 com frete grátis")
- Vale também pra: títulos de seção, callout boxes, comentários (não inserir preço em testimonials novos)

**Onde preço PODE aparecer:**
- Landing pages de checkout/produto (`pag-*.html`, páginas Shopify do produto)
- Não em advertoriais
