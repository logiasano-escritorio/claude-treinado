---
name: reference_arquitetura_tracking_gtm_yampi
description: "Arquitetura de tracking Sano — GTM-PNVRC5ZR, GA4, Meta e Google Ads; regra anti-duplicacao Purchase=Yampi server-side"
metadata: 
  node_type: memory
  type: reference
  originSessionId: b0e426cc-d652-4999-9e95-c5761e1a3fa3
---

Setup de tracking dos funis Sano (sanobrasil.com / sanooficial.com via Vercel sano-brasil + checkout Yampi).

**IDs:**
- GTM container: `GTM-PNVRC5ZR` (conta GTM 6355603079 / container 252597021). Instalado na Yampi (campo nativo) + head/body de 87 HTMLs do repo Sanologia/.
- GA4: `G-MSZ467D4KX` — ligado SO no campo nativo GA4 da Yampi (Yampi ja dispara purchase/add_to_cart/begin_checkout nativamente, nomes padrao GA4). NAO por GTM, senao duplica.
- Google Ads: `AW-18166093728`, rotulo de conversao `fzNYCOCFtq8cEKCvotZD`. Disparado SERVER-SIDE pela Yampi (pixel "PIXEL GG ADS - PRIME", so produto Prime Creme Potente, valor produtos+frete). NAO por GTM.
- Meta Pixel Prime: `1289947162723962` (fbq hardcoded em 17 HTMLs Prime + pixel Meta ativo na Yampi pro Purchase).

**REGRA DE OURO anti-duplicacao:** o evento de COMPRA (Purchase/conversao) dispara SEMPRE server-side pela Yampi (mais confiavel, nao perde venda por adblock/iOS). PageView/ViewContent/topo de funil = pixel no HTML ou GTM. NUNCA o mesmo evento nos dois lugares. Por isso NAO migrar Purchase pro GTM e NAO remover os pixels Meta/Google Ads da Yampi.

**Decisao 2026-06-18:** nao migrar nada pro GTM (fbq no HTML + Yampi server-side ja cobrem tudo). Removido gtag base `AW-18166093728` redundante de combo-ggads.html e prime-lombar/index-ggads.html (era so config base, sem conversao). Ver [[reference_pixel_prime]] e [[reference_deploy_sano_brasil]].

**Pegadinha:** `sanooficial.com` tambem serve as paginas Prime (50 ads da campanha 120244126350890442 apontam pra la, nao sanobrasil.com). GTM presente nos dois dominios.
