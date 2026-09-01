---
name: OpenClaw — Setup e Configuração
description: Gateway local OpenClaw com 5 agentes configurados para operação Relívia — token, porta, agentes, protocolo
type: reference
originSessionId: eee4c79a-9468-4f05-abe9-e209538d91c1
---
## Gateway

- URL: `http://127.0.0.1:18789`
- WebSocket: `ws://127.0.0.1:18789`
- Token: `ca9eb83f815a13ecad9f04f973d651e5cf1c2bdc59c741af`
- Config: `C:\Users\user\.openclaw\openclaw.json`
- Iniciar: `openclaw gateway run` (ou abrir atalho "OpenClaw Dashboard" no Desktop)
- Dashboard com token: `openclaw dashboard`

## Protocolo

- Principal: **WebSocket** (não REST) — método `sessions.send` / `chat.send`
- Compatível OpenAI: `POST /v1/chat/completions` com `model: "openclaw/default"`
- Auth: `Authorization: Bearer <token>`

## Agentes configurados

| ID | Nome | Workspace | Modelo |
|----|------|-----------|--------|
| relay | Relay — Orquestrador | `~/.openclaw/workspace` | claude-opus-4-6 |
| agente-funil | Agente 1 — Inteligência de Funil | `~/.openclaw/workspace-funil` | claude-sonnet-4-6 |
| agente-clone | Agente 2 — Clone Relívia | `~/.openclaw/workspace-clone` | claude-sonnet-4-6 |
| agente-traducao | Agente 3 — Tradução por Mercado | `~/.openclaw/workspace-traducao` | claude-sonnet-4-6 |
| agente-qa | Agente 4 — QA e Entrega | `~/.openclaw/workspace-qa` | claude-haiku-4-5 |

## Canais

- WhatsApp: `+5549989135058` (selfChatMode, allowlist)

## Plugins ativos

- Google (Gemini web search): API key `<CHAVE-NO-.env-LOCAL>`
- Anthropic (Claude API)

## Workspaces

- `C:\Users\user\.openclaw\workspace\SOUL.md` — identidade do Relay
- `C:\Users\user\.openclaw\workspace\TOOLS.md` — setup da operação Relívia
- `C:\Users\user\.openclaw\workspace\USER.md` — perfil do Guilherme
- Workspaces funil/clone/traducao/qa ainda precisam de SOUL.md
