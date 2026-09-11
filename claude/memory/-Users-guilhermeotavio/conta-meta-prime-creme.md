---
name: conta-meta-prime-creme
description: Conta Meta dedicada do Prime Creme (act_1965476473957439) e o padrão 1-1-1 de subida de criativo
metadata: 
  node_type: memory
  type: reference
  originSessionId: 167cb0ea-699f-4f78-be3e-edf99f80d10a
  modified: 2026-09-07T03:40:14.379Z
---

Os ads do **Prime Creme** rodam na conta **`act_1965476473957439` ("USD - PRIME CREME")**, não na `act_2164352101016970` (EUA 11) que as memórias antigas citam — na EUA 11 só sobraram campanhas Prime paradas desde ago/2026.

Padrão da conta (validado no lote de 2026-09-07, campanhas `Prime - AD43..AD52 H1B1..H10B1`):

- **Estrutura 1-1-1** — 1 campanha por criativo, com 1 conjunto e 1 anúncio. Nome idêntico nos 3 níveis: `Prime - AD<nn> <hook>` (numeração de AD contínua entre lotes).
- **Campanha**: OUTCOME_SALES · AUCTION · `LOWEST_COST_WITHOUT_CAP` (essa conta **não** usa bid cap) · `daily_budget` 3000 (US$30/dia) · criada **PAUSED**; conjunto e anúncio nascem ACTIVE, então ligar = virar só a campanha. Vencedores são escalados depois via budget (13000/26000/50000).
- **Conjunto**: OFFSITE_CONVERSIONS/IMPRESSIONS · pixel Prime `1289947162723962` + PURCHASE · BR 18-65 com `targeting_automation.advantage_audience=1` · atribuição 7d clique + 1d view + **1d ENGAGED_VIDEO_VIEW** · `universal_beneficiary`/`universal_payer` = **`1228611831325801`** (não o `880756411607509` das outras contas).
- **Criativo**: Page `650163921506803` + `instagram_user_id` `17841468816354122` (aqui a Page "institucional" é a certa, ao contrário do que vale nos outros funis Sano) · CTA `SEE_DETAILS` · título "Veja agora" · link `https://sanobrasil.com/prime-pv` (PV direto, não advertorial) · corpo B1 de neuropatia de 1.033 char igual em todos os ads.
- `url_tags`: `utm_source=facebook&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}&utm_term={{placement}}`
- `degrees_of_freedom_spec` com **83 features em OPT_OUT** (copiar de um creative existente) — inclui `site_extensions`, ver [[feedback_nunca_subir_ad_com_site_extensions]].

Script + manifesto reutilizáveis: `Desktop/Repo GitHub - Sano/repo-git-mac-windows-sano/_dev/manifestos-prime/` (`publicar_prime_videos.py` lê o `.manifest.json`, é idempotente por nome de campanha).
