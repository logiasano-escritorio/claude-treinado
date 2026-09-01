---
name: Railway — Token e Projeto Relívia Modelar
description: Token de acesso Railway para deploy do relivia-modelar via API GraphQL
type: reference
originSessionId: b6ef9e1c-b5df-4304-a6e5-7c1e71f877eb
---
## Railway

**Account Token:** `605bbb80-f066-46fd-98f6-d69473b33db4`
**API Endpoint:** `https://backboard.railway.com/graphql/v2`
**Workspace ID:** `83ef92a3-8a54-42c9-be38-8377253063f9`

## Projeto relivia-modelar

**Project ID:** `518161c8-62c4-42b9-9678-f9de5d69f1b3`
**Environment ID (production):** `924fce94-4425-4746-8251-f33261520e48`
**URL pública:** `https://web-production-206b62.up.railway.app`

### Serviços
- **web** (Flask + Celery via supervisord) — ID: `48e87044-2d6d-45b5-9202-2b9c168ecf06` — supervisord roda gunicorn + celery juntos
- **worker** (Celery separado, legado) — ID: `c5d88c53-1193-4652-8a74-1ab57a8add71` — pode ser desativado
- **redis** — ID: `b08a7c72-c57b-46ce-903c-50c17248ac15` — `redis://redis.railway.internal:6379`
- **postgres** — ID: `f2b13ac2-b28a-46be-8391-cb9eb4c7c5db` — `postgres.railway.internal:5432`

**Nota:** O serviço `web` original (`ad28b6fa`) foi recriado do zero como `48e87044` para forçar rebuild limpo com Dockerfile.

**Repo:** `relivia-ww/relivia-modelar`
**Dockerfile:** usa `mcr.microsoft.com/playwright/python:v1.44.0-jammy`

## Variáveis configuradas (web + worker)

```
SECRET_KEY=ab36cd9af5e97d1e2bb6b89172bcee4583021228086e863588e7654be7b48ddf
CLAUDE_API_KEY=<CHAVE-NO-.env-LOCAL>
GEMINI_API_KEY=<CHAVE-NO-.env-LOCAL>
GITHUB_TOKEN=<CHAVE-NO-.env-LOCAL>
GITHUB_REPO=relivia-ww/relivia-modelar
GITHUB_BRANCH=main
VERCEL_TOKEN=vcp_4k1CbqEZlJM199RdUjUhjwdQTTaSq19Oyhly9noucJ64XratTF4boS1W
VERCEL_PROJECT_ID=prj_m2xnASZPEAFtI6f85SjNA5IeLev1
VERCEL_DOMAIN=relivia-modelar.vercel.app
AGENTE_CLONE_RUNS_BASE=/app/runs
PORT=5050
REDIS_URL=redis://redis.railway.internal:6379
DATABASE_URL=postgresql+psycopg2://relivia:relivia2026prod@postgres.railway.internal:5432/relivia_modelar
```

## PostgreSQL credentials
- **DB:** relivia_modelar
- **User:** relivia
- **Password:** relivia2026prod
- **Host:** postgres.railway.internal:5432
