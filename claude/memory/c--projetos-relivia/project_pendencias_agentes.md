---
name: Pendências — Correções nos Agentes Relivia
description: Lista completa de 11 correções pendentes nos 4 agentes, organizadas em 4 grupos por dependência, com arquivo e linha afetada
type: project
originSessionId: eee4c79a-9468-4f05-abe9-e209538d91c1
---
Ver lista completa e atualizada no Obsidian:
`Memory/Projects/project_pendencias_agentes.md`

## Grupos resumidos

**Grupo 1 — Base** (outros dependem desses):
- #13 run_manifest.json compartilhado — todos os agentes
- #5 Correlação de runs por manifesto — agente_revisor.py

**Grupo 2 — Revisor**:
- #6 JPEG placeholder corrompido — agente_revisor.py ~linha 250
- #12 Validação HTML fechado — io_contracts.py validar_output_agente2()

**Grupo 3 — Agentes individuais**:
- #4 memory.json Agente 1 — workspace-funil/memory.json
- #2 --lang arg no Agente 3 — agente_traducao.py
- #3 Validação de página real no Agente 2 — agente_clone.py

**Grupo 4 — Otimizações**:
- #11 Hook agent:bootstrap workspaces clone e traducao
- #8 Retry com backoff no Claude
- #1 Credenciais em config.json
- #15 Fallback gemini no Agente 1
- #16 Chunking HTML grande no Agente 3
- #10 Acentos no SOUL.md do Revisor

**Why:** Diagnóstico completo feito em 2026-04-12 após estudo dos 4 agentes + docs OpenClaw.
**How to apply:** Na próxima sessão de correção, começar pelo Grupo 1. Confirmar com usuário entre grupos.
