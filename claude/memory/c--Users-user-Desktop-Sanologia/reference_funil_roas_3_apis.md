---
name: reference_funil_roas_3_apis
description: "Pipeline funil→ROAS por advertorial cruzando GA4 + Yampi + Meta APIs (entradas, passagem, vendas, gasto)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 829a6fdb-bacc-4b83-a6f6-88ba66d09ee6
---

Raio-X completo por advertorial (entradas → passagem → vendas → ROAS) cruzando **3 APIs**, montado 2026-07-15 pro Prime/gaba:

**Credenciais (todas já no ambiente):**
- **GA4 Data API**: service account `sano-sgtm@appspot.gserviceaccount.com`, JSON em `C:/Users/user/Downloads/sano-sgtm-e126eb968912.json`, property **537962989**. Lib `google-analytics-data`. Precisou: ativar Analytics Data API no projeto `sano-sgtm` (905810116013) + dar Viewer à service account na property.
- **Yampi**: alias/token/secret no `_dev/yampi-webhook/Code.gs` (`YAMPI_ALIAS=sano-suplementos`, `YAMPI_USER_TOKEN`, `YAMPI_USER_SECRET`). Base `https://api.dooki.com.br/v2/{alias}`. Pedido tem `utm_content/campaign/medium`, `value_total`, `created_at.date`, `status_id` (3=pago).
- **Meta**: token vence ~60d (regenera no Graph API Explorer, precisa `ads_read`+`ads_management`). Conta gaba = **EUA 11 `act_2164352101016970`**. Conta Prime Creme `act_1965476473957439` roda tônico/joelho, NÃO gaba.

**As 4 métricas por advertorial:**
1. **Entradas** (GA4): `landingPage` sessions começando com `/adv-prime-gaba`.
2. **Passagem** (GA4): page_views da `/prime-pv` (pagePath EXACT) com `pageReferrer` = `/adv-...` (agrupar por PATH, ignorar querystring/fbclid). Taxa = passagem/entradas.
3. **Vendas+receita** (Yampi pagos): `utm_content` do pedido = `{{ad.name}}` do Meta → mapear pro advertorial via Meta.
4. **Gasto** (Meta insights level=ad, `spend`, USD→BRL). ROAS = receita_BRL / (spend×câmbio).

**A ponte criativo→advertorial** (essencial): o `utm_content` NÃO serve p/ atribuir passagem interna (já é ocupado pelo utm do anúncio Meta e não é sobrescrito). Mas serve p/ VENDAS: `utm_content`=`{{ad.name}}`. E cada ad tem destino em `creative.object_story_spec.link_data.link` → mapa nome_ad→advertorial. Campo pesado: pedir `object_story_spec` com `limit=25` (não 200, senão "reduce the amount of data").

**Pegadinhas:**
- Métrica `screenPageViews` incompatível com dim `manualAdContent` no GA4 → tirar.
- Rate limit Meta (erro "too many calls"): coletar tudo 1x salvando em arquivo, criar devagar (sleep 2.5s + retry 45s). Ver [[reference_publisher_cache_colisao_nome]].
- URL advertorial na live é SEM .html (com .html=308).
- ROAS usa `value_total` (inclui frete); trocar p/ `value_products` se quiser margem sem frete.

Scripts em `/tmp` da sessão; vale portar pra `_dev/` como comando. Ver [[reference_utm_content_passagem_advertorial]], [[reference_pixels_meta_por_produto]], [[reference_meta_ads_sano]].
