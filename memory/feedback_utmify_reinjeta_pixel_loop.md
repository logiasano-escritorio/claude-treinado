---
name: feedback_utmify_reinjeta_pixel_loop
description: "UTMify embedada no HTML reinjeta o pixel Meta ~15x/carga (PageView e Purchase duplicados); remover do HTML, não basta desativar no painel"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5f02bca4-0d16-4b7a-ab60-a5e3b0c082d6
---

A UTMify (`cdn.utmify.com.br/scripts/pixel/pixel.js` + `scripts/utms/latest.js`) embedada no `<head>` causa disparo MÚLTIPLO do pixel Meta: o `latest.js` reescreve a URL com UTMs (`/prime-pv` → `/prime?utm_source=organic...`) via history, e cada reescrita RE-EXECUTA o `<script>` do fbevents → `fbevents.js` carregava **15x por carga** → ~17 PageViews no Meta + Purchase dobrado (15 vendas viravam 30).

**Why:** Desativar o pixel no PAINEL da UTMify NÃO resolve — o script segue embedado e re-injetando no cliente. O bug é no código da página, não na config do painel. Diagnóstico cravado com DrissionPage sniffando o `initiator` stack de cada request (o culpado apareceu como `cdn.utmify.com.br/scripts/pixel/pixel.js` e a linha 142 do HTML re-executada N vezes).

**How to apply:** Remover AMBOS os scripts UTMify de TODOS os HTMLs. As páginas Sano já têm handler próprio de UTM (`readParamsFromURL`/`appendUTM`/`rewriteLinks` com MutationObserver, ~linha 40-124) que captura e propaga UTM pro checkout — então remover a UTMify NÃO perde atribuição. Removido de 48 funis em 2026-06-28 (commit d5077c5). Sobra só um comentário `// pra que Utmify e Pixel leiam...` na ~linha 58 (texto inofensivo). Validar com sniffer: `fbevents.js` deve carregar 1x. Ver [[reference_arquitetura_tracking_gtm_yampi]] e [[reference_tracking_sano_saudavel_capi]].
