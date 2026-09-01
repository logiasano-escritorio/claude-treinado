---
name: Link do anúncio sempre vai pro advertorial (não página, não checkout)
description: Em toda campanha Meta Ads Sano/Relívia, o destino do anúncio (link + CTA) é o advertorial, nunca a página de produto ou Yampi direto
type: feedback
originSessionId: 9bd6982e-c870-4b26-bb8d-a96c2fc679cf
---
**Regra dura — link de anúncio Meta Ads Sano/Relívia:**

Sempre apontar pra **advertorial** (`sanobrasil.com/adv-<funil>` ou equivalente Relívia). Nunca:
- ❌ Página de produto (`sanobrasil.com/strongbones`, `/b12`, `/pag-glowup` etc)
- ❌ Checkout Yampi direto (`sano-suplementos.pay.yampi.com.br/r/...`)
- ❌ Domínio antigo (`pagamento.reliviaonline.com`)

**Why:**
- Advertorial pré-vende (3-5 min de leitura) → cliente chega na página de produto QUENTE
- Compliance Anvisa: separa "conteúdo educacional" de "ad de venda direta" — risco menor
- Quality Score Meta: bounce rate menor → CPM reduzido
- Pixel learning melhor: audiência qualificada → otimização efetiva
- Conversão validada: 3-6% adv→checkout vs 0,5-1,5% se for direto

**How to apply:**
- Campo `link` e `call_to_action.value.link` no `object_story_spec` do creative: **sempre URL do advertorial**
- Bulk CSVs em `_Projetos/relivia-editor/outputs_sano/<produto>/<funil>/ads-import.csv` JÁ TÊM isso configurado corretamente
- Quando preparar JSON de subida de campanha nova: NUNCA usar URL de checkout/produto direto no `link`
- Vale pra Sano E pra Relívia — mesma regra
- O fluxo de tracking SanoTracking depende disso (advertorial dispara `AdvertorialView`, CTA dispara `AdvertorialCTAClick`, página de produto dispara `ProductView` — se pular o advertorial, perde 1 etapa do funil)
