---
name: feedback_variant_card_data_checkout_navega
description: "Bug PV Sano — clicar no variant-card abre checkout direto quando handler [data-checkout] pega os cards"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 829a6fdb-bacc-4b83-a6f6-88ba66d09ee6
---

Em PVs Sano com cards de variante (`.variant-card`) que guardam o link no `data-checkout`, existe um bug recorrente: clicar no **card** (que deveria só SELECIONAR o kit) já abre o checkout, pulando o botão.

**Causa:** o handler de navegação `document.querySelectorAll('[data-checkout]')` pega TODO elemento com esse atributo — incluindo os variant-cards — e dispara `window.location.href`. Como o card tem `data-checkout` (pro handler de seleção ler `card.dataset.checkout`), ele é pego pelos dois handlers.

**Fix:** o handler de NAVEGAÇÃO deve ignorar os cards: `querySelectorAll('[data-checkout]:not(.variant-card)')`. O handler de SELEÇÃO (`.variant-card`) continua só marcando active + atualizando o CTA. Detectado 2026-07-15 no Clarilux e Clareia.

**Bug oposto no mesmo lugar (Clareia):** o CTA principal fica `href="#"` até o usuário clicar num card. Se ele for direto no botão, não vai a lugar nenhum. Fix: inicializar o CTA com o card `.active` no load:
```js
var active=document.querySelector('.variant-card.active');
var cta=document.querySelector('[data-pb-cta-main]');
if(active&&cta){cta.textContent='...'+ (active.dataset.price||''); cta.href=active.dataset.checkout||'#';}
```

**Quem NÃO tem o bug:** PVs cujo handler é `a[data-checkout]` (só tags `<a>`, não pega `<div>` card) — ex FungZero-v2, Prime. Ao gerar/revisar PV com variant-card, checar SEMPRE: (1) handler de navegação usa `:not(.variant-card)` ou `a[data-checkout]`; (2) CTA inicializado com card active no load.

Ver [[reference_design_guides]], [[feedback_no_dark_text_on_dark_bg]].
