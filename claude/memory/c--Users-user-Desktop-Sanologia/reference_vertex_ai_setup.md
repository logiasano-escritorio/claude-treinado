---
name: ""
metadata: 
  node_type: memory
  originSessionId: 6c1cd7f4-3419-41a7-9f10-460f50ec0602
---

# Gemini 3.1 Flash Image Preview via Vertex AI Express

## Por que NÃO usar AI Studio direto

A chave antiga `AIzaSyB8Vo...VN7E` (que estava em `.env` Sanologia + Replix) está travada no **tier "Paid 1"** do Google AI Studio. Esse tier exige:
- $100 USD gastos em Gemini API desde criação da conta
- 3 dias passados desde primeiro pagamento

Sem cumprir os 2 critérios, modelos premium (Flash Image Preview, Imagen) retornam **403 PERMISSION_DENIED — "Your project has been denied access"**. Não é Trust & Safety nem billing — é apenas tier inicial limitado. A mensagem é enganosa.

## Solução: Vertex AI Express

O **mesmo projeto Google Cloud** (CLAUDE-SANO) tem **R$ 1.786 de crédito Cloud parado** que **NÃO consome via AI Studio** — só via Vertex AI / Cloud APIs. Vertex AI **não tem restrição de tier**.

### Chave Vertex AI Express
```
<CHAVE-NO-.env-LOCAL>
```

Gerada em https://console.cloud.google.com → Agent Platform (ex-Vertex AI) → Set up API Key.

Chaves Vertex AI Express começam com **`AQ.`** (formato diferente do `AIzaSy...` do AI Studio).

### Setup do client genai

```python
from google import genai
from google.genai import types

client = genai.Client(
    vertexai=True,                                              # roteia pra Vertex AI
    api_key="<CHAVE-NO-.env-LOCAL>",
    http_options=types.HttpOptions(
        timeout=90_000,
        api_version="v1",                                       # OBRIGATÓRIO em Vertex AI Express
    ),
)

response = client.models.generate_content(
    model='gemini-3.1-flash-image-preview',
    contents=[prompt],
    config=types.GenerateContentConfig(response_modalities=['IMAGE']),
)
```

### Diferenças críticas vs AI Studio

| Atributo | AI Studio (antigo) | Vertex AI Express (novo) |
|---|---|---|
| `vertexai=` no Client | omitido / False | **True** |
| `api_key=` formato | `AIzaSy...` | `AQ....` |
| `http_options.api_version` | default | **`"v1"`** |
| Restrição tier | Sim ($100+3d) | **Não** |
| Consome crédito Cloud | Não | **Sim** |
| Cobra cartão direto | Sim | Não (até crédito acabar) |

### Erros típicos de configuração

- **`Project/location and API key are mutually exclusive`** → não passar `project=` nem `location=` junto com `api_key=`
- **`southamerica-west1`** aparecendo como location → endpoint Vertex AI por default vai pra `us-central1` que é onde estão os modelos. Não setar location manualmente.
- **`v1beta1` 404** → usar `api_version="v1"` no http_options

## Arquivos atualizados (Sanologia + Replix)

- `Sanologia/.env` → `GEMINI_API_KEY=AQ.Ab8RN...` + `GEMINI_USE_VERTEX=true`
- `Sanologia/_dev/gerar-manchete-strongbones.py` → `USE_VERTEX = True`
- `_Projetos/replix/app.py` → `DEFAULT_CONFIG["gemini_use_vertex"] = True`, ambos `genai.Client(...)` com `vertexai=True` + `api_version="v1"`
- `_Projetos/replix/_regen_img3.py` → idem

## Quando vai poder voltar pra AI Studio (opcional)

Em 3 dias + $100 USD gastos (~R$500), o projeto sobe automaticamente pro tier "Paid 2" e Flash Image Preview destrava no AI Studio também. Mas como Vertex AI funciona melhor + consome o crédito parado, **não há motivo pra voltar**.

Relacionado: [[reference_chaves_gemini]] (chaves antigas, marcar como obsoletas)
