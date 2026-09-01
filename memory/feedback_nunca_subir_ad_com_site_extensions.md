---
name: feedback_nunca_subir_ad_com_site_extensions
description: "REGRA CRÍTICA — ao subir ad no Meta via API, SEMPRE desligar site_extensions (Complementos p/ navegador / Ligar agora)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7c722b03-0e07-4b10-9a06-8394a9f4326c
---

**REGRA OBRIGATÓRIA:** todo ad subido no Meta via API DEVE ter `site_extensions` (e afins) em `OPT_OUT` no `degrees_of_freedom_spec.creative_features_spec`. Setar explícito no payload de criação de creative:
```
"degrees_of_freedom_spec": {"creative_features_spec": {"site_extensions": {"enroll_status": "OPT_OUT"}}}
```
Também desligar por padrão: `local_store_extension`, `product_extensions`. E NÃO enviar `standard_enhancements` (descontinuado, subcode 3858504).

**Why:** o "Complementos para navegador" adiciona um botão **"Ligar agora"** com telefone que VAZA cliques — a pessoa liga (ninguém atende) e o clique não vira venda nem entra no funil/pixel. Custou 7 DIAS de lucro ao Guilherme: margem caiu de **45% pra 15%** com isso ligado em 158 ads das campanhas Prime (act_2164352101016970, jun/2026). Ele não sabe de onde vem (Meta ativa "aprimoramentos padrão" por default), então é invisível se não checar.

**How to apply:** (1) ao gerar qualquer ad via API/skill (pipeline 01-10, publicador, sano-*), incluir o OPT_OUT no creative. (2) Antes de subir campanha, e periodicamente, auditar ads existentes procurando `site_extensions OPT_IN` OU telefone `tel:` embutido no creative. Remoção em massa: [[reference_remover_site_extensions_meta_api]]. Conta EUA 11 [[reference_meta_ads_sano]], API fixes [[reference_meta_ads_api_fixes_2026_05]].
