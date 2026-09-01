---
name: Atualizar pipeline-data.json ao alterar agentes
description: Sempre que criar/alterar agente, persona ou conexão no projeto Otimizacao de escala, atualizar o pipeline-data.json do mapa mental
type: feedback
originSessionId: fcaefcdd-2572-41b5-9b98-5ae80a27874e
---
Ao fazer qualquer alteração no projeto `C:/Users/user/Desktop/Obsidian Supremo/Otimizacao de escala/`, atualizar obrigatoriamente:

**Arquivo:** `C:/Users/user/Desktop/pipeline-data.json`

O HTML `pipeline-agentes-relivia.html` (Desktop) lê esse JSON e re-renderiza o mapa mental automaticamente a cada 30s. É a fonte da verdade viva do pipeline.

**Quando atualizar:**
- Criar novo agente → adicionar nó em `nodes[]` + arestas em `edges[]`
- Nova persona em agente existente → atualizar `nodes[id].personas`
- Novo output → atualizar `nodes[id].outputs`
- Nova conexão entre agentes → adicionar em `edges[]` com `auto: true` (subprocess) ou `auto: false` (manual)
- Remover agente → remover do `nodes[]` e todas as arestas em `edges[]`

**Sempre incrementar:** `meta.versao`, `meta.atualizado`, `meta.stats.*`

**Why:** Usuário quer mapa mental vivo — ele e o Claude alimentam juntos o JSON, e o HTML reflete em tempo real sem precisar mexer no código do mapa.

**How to apply:** No final de cada sessão que altere agentes, verificar se o pipeline-data.json está sincronizado. Não esperar o usuário pedir.
