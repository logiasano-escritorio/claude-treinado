---
name: reference_tracking_sano_saudavel_capi
description: Arquitetura de tracking Sano confirmada saudável — pixel browser + sGTM CAPI + Purchase só Yampi; números EMQ/cobertura de referência
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5f02bca4-0d16-4b7a-ab60-a5e3b0c082d6
---

Auditoria completa do tracking Sano em 2026-06-28 (funil Prime, pixel `1289947162723962`). Estado confirmado SAUDÁVEL via Gerenciador de Eventos do Meta:

- **PageView**: pixel client-side (HTML, ~linha 145-146 `fbq init`+`track PageView`). Após remover UTMify, dispara 1x. Cobertura CAPI 87% (meta Meta ≥75%).
- **Purchase**: SÓ via Yampi (pixel no Yampi). sGTM NÃO manda Purchase — a tag "Meta CAPI Server" tem trigger `Navegacao - sem Purchase` (`{{Event Name}} does not equal purchase`). Fonte única = impossível duplicar. **EMQ 9.3/10**, Email/Telefone/IP 100%, fbc 96%.
- **+53,3% de conversões adicionais** relatadas pelo CAPI vs pixel-only (esse é o ganho concreto do sGTM próprio — recupera vendas perdidas por adblock/iOS).
- **Server**: `sgtm.sanobrasil.com` (container "Sano Server", account 6355603079). GA4 web (`GTM-PNVRC5ZR`, container 255937506) manda pro sGTM → CAPI repassa pro Meta. fbp/fbc/IP/UA/geo enviados server-side. Dedup browser+server por chave de evento (automática, OK).

**Como provar de fora**: DrissionPage sniffando rede — `facebook.com/tr` client-side = 0 (tudo vai pelo sGTM); o request server→Meta NÃO é visível no browser, só o painel Meta mostra (EMQ + % cobertura CAPI). Scripts de auditoria ficaram no scratchpad da sessão (sniff_initiator.py / sniff_capi.py).

Regra de ouro mantida: Purchase sempre server-side Yampi, nunca no GTM. Ver [[reference_arquitetura_tracking_gtm_yampi]], [[reference_pixel_prime]], [[feedback_utmify_reinjeta_pixel_loop]].
