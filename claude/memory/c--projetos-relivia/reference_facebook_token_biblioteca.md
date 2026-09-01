---
name: Facebook Token - Extrator Biblioteca de Anúncios
description: Access Token do Meta para o MCP de extração da Ad Library — permissões ads_read e ads_management
type: reference
originSessionId: 7a998ecb-ae02-4d42-a6e5-cde695107a14
---
## Token de Acesso Meta (Ad Library Extractor)

**Token (longa duração ~60 dias):** `<CHAVE-NO-.env-LOCAL>`

**App ID:** `2103405117116034`

**App Secret:** `1ab047cdc12a26b498bcb8950db744af`

**Permissões:** `ads_read`, `ads_management`

**Tipo:** Token de longa duração (60 dias) — convertido via `/oauth/access_token` em 2026-04-10

**Uso:** MCP Server para extração da Meta Ad Library — análise de anúncios campeões, textos frequentes e download de criativos

**Obs:** Quando expirar, gerar novo token curto em Ferramentas > Obter token e reconverter com App ID + App Secret acima.
