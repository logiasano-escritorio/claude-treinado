---
name: reference_last30days_skill
description: "Skill /last30days instalada — pesquisa relatos reais de público (X, Reddit, HN) pra alimentar copy"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7c722b03-0e07-4b10-9a06-8394a9f4326c
---

`/last30days` (mvanhorn/last30days-skill, MIT) instalada manualmente em `~/.claude/plugins/marketplaces/mvanhorn-last30days-skill` (clonei o repo + registrei em known_marketplaces.json/installed_plugins.json, backups `.bak-l30`). Pesquisa um tópico nos últimos N dias em Reddit/X/YouTube/HN/Polymarket/GitHub em paralelo e ranqueia por engajamento real. Usada pra Voice-of-Customer research [[reference_research_doc_voice_of_customer]].

**Rodar direto (sem /plugin, que eu não consigo chamar):**
`python skills/last30days/scripts/last30days.py "<tema>" --emit md --days 90 --dedicated-subreddits "sub1,sub2" --save-dir "<path>"` (dentro da pasta do plugin, com `export XAI_API_KEY=...`).

**Aprendizados de uso:**
- GitHub polui resultado de pesquisa de PÚBLICO (issues de código aleatórias) — ignorar esses itens.
- PT-BR NÃO tem massa crítica de nicho saúde/estética no Reddit — cai em política/futebol (r/brasil). Relato denso de calvície etc. está em INGLÊS (r/tressless 500k+). Buscar em EN e adaptar.
- Usar `--dedicated-subreddits` pra mirar os subs certos; `--days 90` pega mais volume que 30.
- X/Twitter destravado via `XAI_API_KEY` (xai-...) salvo no `.env` do Sanologia. **Precisa de crédito pago** no console.x.ai (chave nova = team sem crédito dá `permission-denied`; Guilherme pôs US$5 em 2026-07-01). Validar com chat simples na api.x.ai antes de rodar.
- **Se `--search x` der "No sources are available for this run": a XAI_API_KEY NÃO foi exportada no processo.** `--preflight` mostra "Available sources" — se X não estiver lá, `export XAI_API_KEY=$(grep -hoiE "XAI_API_KEY=xai-[A-Za-z0-9_-]+" /c/Users/user/Desktop/Sanologia/.env | head -1 | cut -d= -f2)` antes de rodar. Skill tool não invoca (`Unknown skill: last30days`) — rodar o .py direto. Usa modelo `grok-4-1-fast` via api.x.ai/v1/responses.
- Raw salvo em `--save-dir` tem MUITO mais detalhe que o output resumido — ler o arquivo raw pra extrair verbatim.
