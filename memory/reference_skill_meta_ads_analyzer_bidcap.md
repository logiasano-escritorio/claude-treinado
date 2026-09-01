---
name: reference_skill_meta_ads_analyzer_bidcap
description: Skill meta-ads-analyzer (doutrina Meta) + subagente especialista-bidcap instalados; escolher Bid Cap/Cost Cap e diagnosticar entrega
metadata: 
  node_type: memory
  type: reference
  originSessionId: f64abc87-b93c-48c7-9b1c-9744814d47df
---

Instalado em `~/.claude/`:

**Skill `meta-ads-analyzer`** (de github.com/mathiaschu/meta-ads-analyzer, @MathiasChu, MIT ~389★) — só a parte de skill, SEM o MCP server (não conectar API na conta EUA 11, que já esteve status 3; usar CSV/print). 9 docs oficiais da Meta em `references/`: `bid_strategies.md` (Bid Cap/Cost Cap/Highest Volume), `pacing.md`, `learning_phase.md`, `breakdown_effect.md` (ler primeiro — custo marginal ≠ médio, não cortar segmento por CPA médio alto), `auction_overlap.md`, `ad_auctions.md`, etc.

**Subagente `especialista-bidcap`** (`~/.claude/agents/especialista-bidcap.md`, model `opus` — alias, NÃO o id completo, senão o linter reclama). Media buyer de lances. Lê a doutrina da skill + contexto fixo Sano: USD/BR, âncoras de bid US$25 (Gaba/B12), US$35 COST_CAP (FungZero), US$15 CBO padrão; sintoma "não gasta" = Bid Cap baixo demais é suspeita nº1. Chamar quando: escolher Bid Cap vs Cost Cap, definir valor de bid, ou diagnosticar underdelivery/pacing/learning.

Tem enxertada uma **árvore de decisão** (pescada do `bid-strategy-selector` do repo ai-media-buying-skills, sem instalar o repo — só 6★): Gate1 histórico ≥30d? → Gate2 ≥50 eventos/sem? → Gate3 restrição. Transição Sano: funil novo=**Highest Volume** (sai do learning) → provado=**Cost Cap** (CPA hist +15%) → estourou teto=**Bid Cap**. NUNCA Bid Cap em pixel sem histórico (=não gasta). Descartado: `meta-ads-stack` (exige token/API na conta EUA 11 restrita, risco).

Origem: pesquisa no X via Agent Tools API da xAI (Live Search foi descontinuado — usar `/v1/responses` + `tools:[x_search,web_search]`, modelo grok-4.5). Ver [[reference_pixels_meta_por_produto]], [[project_campanha_gaba_20conjuntos]].
