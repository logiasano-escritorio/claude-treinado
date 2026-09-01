---
name: reference-meta-ads-sync-planilha-controle-trafego
description: Planilha Controle Tráfego Sano sincroniza gasto Meta Ads automaticamente via Graph API; trigger noturno 4h + função manual; conta EUA 11 USD com câmbio em Config!B7
metadata: 
  node_type: memory
  type: reference
  originSessionId: fda4c240-53cf-4717-a6b1-266a11839ad6
---

📊 **Planilha "Controle Tráfego — Sano" puxa gastos Meta Ads automaticamente.**

**Onde:** `_dev/yampi-webhook/Code.gs` (Sano)

**Como funciona:**
- Conta: `act_2164352101016970` (Sano EUA 11 USD) — credenciais em [[reference_meta_ads_sano]]
- Token Meta: hardcoded em `META_ACCESS_TOKEN` (vence ~60 dias, renovar via Graph API Explorer com permissão `ads_read`)
- Mapeia campanha → categoria via `META_CAMPANHA_KEYWORDS` (regex no nome da campanha — Prime contém "prime/creme/gotas", etc)
- Converte USD→BRL via cotação manual em `Config!B7` (default R$5,40)
- Grava em cada aba `CPA <Categoria>` na coluna B (Gasto Meta Ads)

**Funções no Code.gs:**
- `sincronizarGastosMetaAds()` — manual, puxa ontem
- `sincronizarGastosMetaAdsRange()` — manual, prompt pra N dias (1-90)
- `instalarTriggerMetaAds()` — trigger noturno 4h
- `fetchMetaAdsGastos_(inicio, fim)` — helper interno

**Quando consultar isso:**
- User pergunta "como atualizar gasto Meta na planilha" → resposta: já é auto, conferir aba Config!B7 e logs Apps Script
- Token Meta vencer → seguir passo de renovar (Graph API Explorer)
- Campanha nova não detectada → ajustar META_CAMPANHA_KEYWORDS

**Pegadinha:**
- Trigger noturno só pega ontem completo. Pra atualizar gasto durante o dia, rodar manual `sincronizarGastosMetaAds`.
- Se nome da campanha mudar e não bater keyword → cai em "campanhas sem categoria" e gasto NÃO é gravado. Aparece no popup como warning.
