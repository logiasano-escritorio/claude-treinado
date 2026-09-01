---
name: reference_pixels_meta_por_produto
description: Pixels Meta por produto Sano e o padrao de tracking (fbq HTML + CAPI sGTM + Purchase Yampi)
metadata: 
  node_type: memory
  type: reference
  originSessionId: b0e426cc-d652-4999-9e95-c5761e1a3fa3
---

Cada produto Sano novo tem pixel Meta PROPRIO (não usa o GTM-PNVRC5ZR pra Meta — esse é só GA4/navegação genérica).

**Pixels por produto:**
- Prime: `1289947162723962`
- FungZero: `2156335194912574`
- Tônico Supremo: `1553830736152220`
- (Clareia e Clarilux ainda sem pixel próprio — só GTM genérico, quando for rodar Meta cadastrar igual)

**Padrão de tracking por produto (3 camadas, mesmo pros 3 acima):**
1. **fbq no HTML** (head, após `<!-- End Google Tag Manager -->`) → PageView pelo navegador. Inserir em TODAS as páginas do produto (PV masc/fem/v2, todos os advertoriais, ggads).
2. **CAPI no sGTM** (container Sano Server `GTM-56Z73HTW`) → tag "Conversions API Tag" com o Pixel ID do produto + trigger `Navegacao - sem Purchase`. PageView server-side, DEDUPLICA com o fbq (Meta junta browser+server, não conta dobrado). Marcar Extend cookies fbp/fbc + Event Enhancement. **PRECISA Submit/publicar o container.**
3. **Purchase na Yampi** → cadastrar o pixel do produto no painel Yampi (Marketing/Pixels Meta) + ligar boleto/pix. Purchase sempre server-side Yampi, nunca no GTM.

**Token CAPI:** um único token do Meta (gerado com Dataset Quality API marcando os 8 datasets) serve pra TODOS os pixels. Testar novo pixel: `POST graph.facebook.com/v23.0/{pixel}/events` → se `events_received:1`, o token cobre. (token está em env `META_CAPI_TOKEN` da funcao reportana-lead / tags do sGTM — REGENERAR, foi colado no chat).

**NUNCA** colocar tag de Pixel no GTM WEB junto com o fbq do HTML (aí sim duplica PageView browser). O certo é fbq HTML (browser) + CAPI sGTM (server) = dedup.

Relacionado: [[reference_arquitetura_tracking_gtm_yampi]], [[reference_pixel_prime]]
