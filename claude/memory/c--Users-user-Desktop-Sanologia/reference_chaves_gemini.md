---
name: Chaves Gemini API disponíveis
description: 3 chaves Gemini circulando no ambiente — qual está ativa e onde cada uma está configurada.
type: reference
originSessionId: 24f4ed1d-1674-4cf2-87be-5a5d4575344c
---
Chaves Gemini API (status em 2026-05-04):

| Chave | Onde está configurada | Status |
|---|---|---|
| `<CHAVE-NO-.env-LOCAL>` | copy-anuncio skill, openclaw, traduzir_imagens.py | quota free zerada |
| `<CHAVE-NO-.env-LOCAL>` | Relívia Editor (`app.py`) | quota free zerada |
| `<CHAVE-NO-.env-LOCAL>` | `Sanologia/.env` GEMINI_API_KEY | **ATIVA com saldo** |

Quando uma chave dá 503 silencioso ou timeout: NÃO é necessariamente quota. O modelo gemini-3.1-flash-image-preview tem spikes de "high demand" — testar com curl simples (sem imagem) pra distinguir 429 (quota) de 503 (congestão temporária).

Como testar uma chave:
```
curl -sS --max-time 30 "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key=KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"red dot"}]}]}'
```

Reset do free tier: 00:00 PT (≈ 04:00 BRT). Se precisar volume alto e constante: ativar billing na conta Google Cloud (~$0.04/imagem).
