---
name: OpenClaw — Estudo Completo (docs + aplicação Relivia)
description: Estudo técnico de docs.openclaw.ai: arquitetura, memória, Standing Orders, TaskFlow, Hooks, Cron, Model Failover, Plugins — com recomendações práticas mapeadas ao pipeline Relivia
type: reference
originSessionId: eee4c79a-9468-4f05-abe9-e209538d91c1
---
Ver documento completo no Obsidian:
`Memory/References/reference_openclaw_estudo_completo.md`

## Pontos-chave para consulta rápida

**Bootstrap**: 6 arquivos injetados automaticamente no workspace no início de cada sessão (SOUL, AGENTS, TOOLS, IDENTITY, USER, MEMORY).

**Standing Orders**: programas permanentes no AGENTS.md — o agente executa sem ser pedido. Pattern: Execute-Verify-Report.

**Hooks relevantes para o pipeline**:
- `agent:bootstrap` → carregar memory.json e injetar aprendizados no contexto
- `task:completed` → notificar Revisor quando Agente 3 termina
- `task:failed` → acionar correção cirúrgica automaticamente
- `session:compact` → salvar resumo no MEMORY.md antes de compactar

**Cron**: sintaxe `every day at 09:00` | `cron: 0 9 * * 1-5` | `isolated` session para runs autônomos.

**TaskFlow (futuro)**: modo Managed para orquestrar A1→A2→A3→Revisor como fluxo único com detecção de conflito.

**Model Failover**: fallback chain com backoff exponencial (1→5→25→60 min). Adicionar haiku como fallback para Agentes 1 e 2.

**Plugins**: `api.registerHttpRoute("POST", "/pipeline/run", ...)` para expor pipeline como REST (futuro).

**O que já implementamos que equivale à plataforma**:
- Nossa `memory_store.py` = engine de memória builtin (SQLite) — mantemos o nosso, já integrado
- Nossos AGENTS.md = Standing Orders — já corretos
- `io_contracts.py` = validação de I/O que o TaskFlow nativo faria implicitamente
