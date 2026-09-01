---
name: Roadmap — Pipeline Relívia SaaS
description: Roadmap para transformar o pipeline de agentes em SaaS com frontend — FastAPI + Next.js + Celery
type: project
originSessionId: 944abb03-550d-41fa-9071-25afb02a7392
---
## Stack

| Camada | Tecnologia |
|---|---|
| Backend | FastAPI (Python) |
| Jobs longos | Celery + Redis |
| Frontend | Next.js 14 + Tailwind + Shadcn |
| Storage outputs | Cloudflare R2 |
| Deploy backend | Railway |
| Deploy frontend | Vercel |
| Auth MVP | Magic Link (itsdangerous + SMTP) |
| Auth produção | Clerk |
| Billing | Stripe |

## Fluxo
Browser → POST /api/jobs → FastAPI → Celery Worker → 6 agentes em sequência → Redis pub/sub → SSE → Browser

## Fase 1 — MVP Local (3–5 dias) — 🟡 EM ANDAMENTO

### E1 — Backend FastAPI
- [ ] Criar `relivia-saas/api/main.py` com FastAPI
- [ ] `POST /api/jobs` — recebe {url, lang}, cria job em memória, retorna job_id
- [ ] `GET /api/jobs/{id}` — retorna status e metadados
- [ ] `GET /api/jobs/{id}/stream` — SSE com eventos por etapa
- [ ] `GET /api/jobs/{id}/download` — serve HTML final
- [ ] Adaptar pipeline.py como função chamável com log_callback

### E2 — Frontend Next.js
- [ ] Scaffolding Next.js 14 + Tailwind
- [ ] Página `/` — form URL + select idioma + botão Rodar
- [ ] Componente PipelineProgress — SSE consumer, cards por etapa
- [ ] Componente OutputCard — iframe preview + botão download

### E3 — Integração
- [ ] CORS FastAPI para localhost:3000
- [ ] Teste end-to-end completo
- [ ] Logging estruturado por agente

## Fase 2 — Produção (5–8 dias) — ⬜ PENDENTE

- [ ] E4 — Celery + Redis
- [ ] E5 — PostgreSQL + R2
- [ ] E6 — Magic Link auth
- [ ] E7 — Deploy Railway + Vercel + CI/CD

## Fase 3 — SaaS completo (10–15 dias) — ⬜ PENDENTE

- [ ] E8 — Stripe billing
- [ ] E9 — Dashboard histórico
- [ ] E10 — Observabilidade (Sentry, métricas)
- [ ] E11 — Batch multi-idioma + export ZIP

## Arquivos críticos
- `C:/Users/user/Desktop/Obsidian Supremo/Otimizacao de escala/managed-agents/pipeline.py` — adaptar para função chamável
- `c:/projetos/relivia/mcp-designer/app.py` — template do padrão SSE + jobs
- `C:/Users/user/Desktop/Obsidian Supremo/Otimizacao de escala/managed-agents/agents_config.json` — IDs dos agentes

## Why
Operação precisa de velocidade — pipeline CLI vira produto SaaS para escalar uso interno e futuramente externo.

## How to apply
Sempre implementar fase atual antes de avançar. MVP local primeiro, deploy depois.
