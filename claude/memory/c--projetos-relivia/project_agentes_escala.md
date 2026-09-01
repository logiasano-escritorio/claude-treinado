---
name: Agentes IA — Otimização de Escala
description: Pipeline completo de 7 agentes end-to-end: Ads Library → Meta Ads publicado. 24 personas IA.
type: project
originSessionId: fcaefcdd-2572-41b5-9b98-5ae80a27874e
---
Pipeline completo implementado em `C:/Users/user/Desktop/Obsidian Supremo/Otimizacao de escala/`

## Agentes implementados (todos funcionais)

### Agente Funil (existente)
- `agente-funil/agente_funil.py`
- DrissionPage raspa Facebook Ads Library, rankeia por repetição, baixa criativos
- Output: `funil-data.json` (brand, top_ads, destination_urls_clean)

### Agente Análise (NOVO — 2026-04-12)
- `agente-analise/agente_analise.py`
- Etapas 2+3: engenharia reversa + awareness
- Personas: Creative Analyst, Copy Master, Eugene Schwartz, Evaldo Albuquerque
- Output: `analise-data.json` com `brief_para_agente_copy`
- Workspace: `~/.openclaw/workspace-analise/`

### Agente Clone (existente, atualizado)
- `agente-clone/agente_clone.py`
- Etapa 4: clona advertorial com DrissionPage + Claude
- ATUALIZADO: ao final dispara `agente_copy.py --html <run>/index.html` automaticamente

### Agente Copy (NOVO — 2026-04-12)
- `agente-copy/agente_copy.py`
- Etapas 5+6+7: 6 copywriters + 3 storytellers + 4 agentes de design
- 13 personas: Halbert→Georgi→Sugarman→Bencivenga→Cialdini→Lampropoulos + Kindra Hall→Blair Warren→Manifestador + UX Designer→Hormozi→Ad Midas→Visual Generator
- Output: `advertorial-com-storytelling.html`, `gemini-prompts.json`
- Workspace: `~/.openclaw/workspace-copy/`

### Agente Tradução (existente)
- `agente-traducao/agente_traducao.py`

### Agente Produto (NOVO — 2026-04-12)
- `agente-produto/agente_produto.py`
- Etapas 10+11+12: clone produto + CRO + prompts Gemini
- Personas: Brand Identity Auditor, CRO Specialist, Conversion Architect, Product Photographer, Label Designer, Lifestyle Director, Ad Integration
- Output: `produto-index.html`, `produto-otimizado.html`, `produto-gemini-prompts.json`
- Workspace: `~/.openclaw/workspace-produto/`

### Agente Publicador (NOVO — 2026-04-12)
- `agente-publicador/agente_publicador.py`
- Etapa 13: Meta Marketing API v20.0 — upload imagem → campanha → AdSet → AdCreative → Ad (PAUSED)
- Requer em config.json: `meta_access_token`, `meta_ad_account_id`, `meta_page_id`, `meta_pixel_id`
- Workspace: `~/.openclaw/workspace-publicador/`

### Agente Revisor (existente)
- `agente-revisor/agente_revisor.py`
- Chamado automaticamente ao final do Clone E do Produto

## ClickUp IDs
- List Agente 1 (Funil): 901326816107
- List Agente 2 (Clone/Copy/Produto): 901326816109

## OpenClaw
- openclaw.json atualizado com todos os 4 novos agentes
- Cron configurado (disabled) para pipeline diário 08:00 seg-sex
- 4 novos workspaces criados em `~/.openclaw/`

## Documentação
- Obsidian: `Relivia Context/Agentes/workflow-escala-implementacao-final.md`

**Why:** Operação de ecommerce multi-produto/multi-mercado — gargalo é velocidade de produção
**How to apply:** Pipeline completo funcional. Para nova brand: rodar agente_funil.py → chain automático até agente_copy → manual: tradução + produto + publicador
