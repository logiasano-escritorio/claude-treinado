---
name: OpenClaw — Megaprompt de Contexto Completo
description: Contexto completo do OpenClaw para reutilizar em qualquer sessão Claude: arquitetura, APIs, configuração, workspaces, skills, multi-agent
type: reference
originSessionId: eee4c79a-9468-4f05-abe9-e209538d91c1
---
# OpenClaw — Contexto Completo

## O que é

OpenClaw é um gateway self-hosted que conecta plataformas de mensagem (WhatsApp, Telegram, Discord, etc.) a agentes de AI. Roda localmente em Node.js 24 na porta 18789.

---

## Arquitetura

```
[Canal (WhatsApp/Discord/etc.)]
        ↓
[Gateway — porta 18789]
        ↓
[Agent Runtime (Pi core)]
        ↓
[Modelo (Claude/Gemini/GPT)]
```

- **Gateway**: processo único que roda na máquina local. Gerencia canais, roteamento, sessões, tools.
- **Agente**: entidade isolada com workspace próprio, sessões próprias, modelo próprio.
- **Workspace**: diretório com arquivos markdown que definem o agente.
- **Skills**: plugins markdown/python que estendem o que o agente pode fazer.

---

## Setup desta instalação

- **Porta**: 18789
- **Token**: `ca9eb83f815a13ecad9f04f973d651e5cf1c2bdc59c741af`
- **Config**: `C:\Users\user\.openclaw\openclaw.json`
- **Dashboard**: `http://127.0.0.1:18789` (após `openclaw gateway run`)
- **Iniciar gateway**: `openclaw gateway run`
- **Dashboard com token**: `openclaw dashboard`

---

## Agentes configurados

| ID | Nome | Workspace | Modelo |
|----|------|-----------|--------|
| relay | Relay — Orquestrador | `~/.openclaw/workspace` | claude-opus-4-6 |
| agente-funil | Agente 1 — Inteligência de Funil | `~/.openclaw/workspace-funil` | claude-sonnet-4-6 |
| agente-clone | Agente 2 — Clone Relívia | `~/.openclaw/workspace-clone` | claude-sonnet-4-6 |
| agente-traducao | Agente 3 — Tradução por Mercado | `~/.openclaw/workspace-traducao` | claude-sonnet-4-6 |
| agente-qa | Agente 4 — QA e Entrega | `~/.openclaw/workspace-qa` | claude-haiku-4-5 |

---

## Estrutura de Workspace (arquivos de cada agente)

Cada workspace é uma pasta com estes arquivos markdown:

| Arquivo | Função |
|---------|--------|
| `SOUL.md` | Persona, tom, limites, instruções de comportamento |
| `IDENTITY.md` | Nome, emoji, vibe do agente |
| `USER.md` | Perfil do usuário (nome, preferências, contexto) |
| `TOOLS.md` | Notas de ferramentas específicas do ambiente (IPs, paths, aliases) |
| `AGENTS.md` | Instruções operacionais + memória de contexto |
| `BOOTSTRAP.md` | Ritual de setup inicial (removido após execução) |
| `MEMORY.md` | Memória de longo prazo — carregada em toda sessão DM |
| `HEARTBEAT.md` | Instrução recorrente executada periodicamente |
| `memory/YYYY-MM-DD.md` | Notas diárias — hoje e ontem são carregadas automaticamente |

O sistema prompt do agente é montado assim:
1. Base prompt do OpenClaw
2. Lista compacta de skills disponíveis
3. Arquivos bootstrap (SOUL, IDENTITY, USER, TOOLS, AGENTS, MEMORY)
4. Overrides por run

---

## Skills

Skills são plugins que estendem o agente. Estrutura:

```
skill-name/
  skill.md       # descrição + instruções (carregado no system prompt)
  script.py      # lógica Python (opcional)
```

Hierarquia de carregamento:
1. `workspace/skills/` (workspace do agente)
2. `~/.openclaw/skills/` (skills pessoais)
3. Skills bundled do OpenClaw

Para habilitar por agente no `openclaw.json`:
```json
"agents": {
  "list": [{
    "id": "agente-funil",
    "skills": { "allow": ["nome-da-skill"] }
  }]
}
```

---

## API HTTP — Chat Completions (OpenAI-compatible)

```
POST http://127.0.0.1:18789/v1/chat/completions
Authorization: Bearer ca9eb83f815a13ecad9f04f973d651e5cf1c2bdc59c741af
Content-Type: application/json
```

**Body:**
```json
{
  "model": "openclaw/<agentId>",
  "messages": [{"role": "user", "content": "mensagem"}],
  "stream": false
}
```

**Roteamento pelo model field:**
| Valor | Rota para |
|-------|-----------|
| `"openclaw"` | Agente default |
| `"openclaw/default"` | Agente default |
| `"openclaw/relay"` | Agente Relay |
| `"openclaw/agente-funil"` | Agente 1 |
| `"openclaw/agente-clone"` | Agente 2 |

**Headers opcionais:**
- `x-openclaw-session-key: <key>` — controla roteamento de sessão
- `x-openclaw-model: <provider/model>` — override do modelo backend

---

## API HTTP — Tools Invoke

```
POST http://127.0.0.1:18789/tools/invoke
Authorization: Bearer ca9eb83f815a13ecad9f04f973d651e5cf1c2bdc59c741af
Content-Type: application/json
```

**Body:**
```json
{
  "tool": "nome_da_ferramenta",
  "args": {},
  "sessionKey": "main"
}
```

Usar para acionar ferramentas diretamente sem passar pelo LLM.

---

## Protocolo WebSocket

Comunicação principal via WebSocket em `ws://127.0.0.1:18789`.

**Frame tipos:**
- Request: `{type:"req", id, method, params}`
- Response: `{type:"res", id, ok, payload|error}`
- Event: `{type:"event", event, payload}`

**Métodos principais:**
- `sessions.send` — envia mensagem para sessão existente
- `chat.send` — executa chat (legacy, ainda funciona)
- `sessions.subscribe` — assina eventos de transcrição

---

## Multi-Agent

Para agente acionar outro agente, habilitar no `openclaw.json`:
```json
"tools": {
  "agentToAgent": {
    "enabled": true,
    "allow": ["agente-funil", "agente-clone", "agente-traducao", "agente-qa"]
  }
}
```

**Roteamento:** determinístico, mais específico ganha:
1. Peer exato (ID de DM/canal)
2. ParentPeer (herança de thread)
3. Guild/Team ID
4. AccountId
5. Fallback para agente default

---

## Memória

- `MEMORY.md` — fatos duráveis, carregado em toda sessão DM
- `memory/YYYY-MM-DD.md` — notas diárias, hoje e ontem carregados automaticamente
- Salvar: pedir ao agente "remember that..."
- Buscar: ferramenta `memory_search` (semântica) ou `memory_get` (arquivo específico)

---

## Canais configurados

- **WhatsApp**: `+5549989135058` — selfChatMode, allowlist

---

## Plugins ativos

- **anthropic**: Claude API
- **google**: Gemini web search (key: `<CHAVE-NO-.env-LOCAL>`)

---

## Tools profile

- `"coding"` — profile atual. Inclui: read, write, edit, exec, web search, browser.

---

## Comandos CLI úteis

```bash
openclaw gateway run          # inicia o gateway
openclaw gateway stop         # para o gateway
openclaw gateway status       # status atual
openclaw dashboard            # abre dashboard com token no browser
openclaw agents list          # lista agentes
openclaw agents list --format json  # formato JSON para scripts
```

---

## openclaw.json desta instalação

```json
{
  "agents": {
    "defaults": {
      "workspace": "C:\\Users\\user\\.openclaw\\workspace",
      "models": {
        "anthropic/claude-sonnet-4-6": {},
        "anthropic/claude-opus-4-6": {}
      },
      "model": { "primary": "anthropic/claude-sonnet-4-6" }
    },
    "list": [
      { "id": "relay", "name": "Relay — Orquestrador", "workspace": "...\\workspace", "model": { "primary": "anthropic/claude-opus-4-6" } },
      { "id": "agente-funil", "name": "Agente 1 — Inteligência de Funil", "workspace": "...\\workspace-funil" },
      { "id": "agente-clone", "name": "Agente 2 — Clone Relívia", "workspace": "...\\workspace-clone" },
      { "id": "agente-traducao", "name": "Agente 3 — Tradução por Mercado", "workspace": "...\\workspace-traducao" },
      { "id": "agente-qa", "name": "Agente 4 — QA e Entrega", "workspace": "...\\workspace-qa", "model": { "primary": "anthropic/claude-haiku-4-5-20251001" } }
    ]
  },
  "gateway": { "port": 18789, "bind": "loopback", "auth": { "mode": "token", "token": "ca9eb83f..." } },
  "tools": { "profile": "coding", "web": { "search": { "provider": "gemini", "enabled": true } } },
  "channels": { "whatsapp": { "selfChatMode": true, "dmPolicy": "allowlist", "allowFrom": ["+5549989135058"], "enabled": true } }
}
```
