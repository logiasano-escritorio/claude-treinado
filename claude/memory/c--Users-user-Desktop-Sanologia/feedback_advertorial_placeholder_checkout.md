---
name: Advertorial com [CHECKOUT_RELIVIA] precisa de fix antes do deploy
description: Advertoriais Sano gerados costumam ter href="[CHECKOUT_RELIVIA]" como placeholder não resolvido — sempre apontar pra página de venda antes de push
type: feedback
originSessionId: 3ab9d48b-9df8-4f63-9b5f-e2a1b74de5f0
---
Antes de fazer deploy de qualquer advertorial Sano/Relívia, grepar por `[CHECKOUT_RELIVIA]` (ou outros placeholders tipo `[LINK_TERMOS]`) e trocar pelos destinos reais. No funil Sano, o destino correto é SEMPRE a página de venda do próprio funil (ex: `/magnesio-gummies/magnesio-gummies.html`), nunca checkout direto — checkout sai da página de venda.

**Why:** No deploy do funil magnesio-gummies (2026-05-11), os 10 CTAs do advertorial ficaram com placeholder `[CHECKOUT_RELIVIA]` sem resolver — usuário precisou pedir explicitamente o fix. Isso mata 100% das conversões porque botão vira `#` (link quebrado).

**How to apply:** Em todo deploy de advertorial novo, rodar `grep -E '\[CHECKOUT|\[LINK_' <adv>.html` antes do commit. Se achar, substituir pelos paths reais (página de venda do mesmo funil). Memória reference_link_anuncio_sempre_advertorial.md já confirma: advertorial → página de venda → checkout, nessa ordem. CTAs do advertorial NUNCA vão direto pro checkout.
