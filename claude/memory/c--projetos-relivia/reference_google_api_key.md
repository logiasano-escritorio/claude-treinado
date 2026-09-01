---
name: Google AI Studio — API Key
description: Chaves da API do Google AI Studio para uso com Gemini Image / Imagen — plano pago e conta gratuita
type: reference
originSessionId: 7e2a92c6-a63c-4449-b530-bdd38e7de844
---
## API Key — Conta PAGA (conta nova, projeto relivia-imagens)

```
<CHAVE-NO-.env-LOCAL>
```

- **Nome:** gemini - claude
- **Projeto:** projects/476837678188
- **Número do projeto:** 476837678188
- **Plano:** Pago (conta completa ativada em 2026-04-21, crédito R$1.786 por 90 dias)
- **Uso:** Imagen 4 (`imagen-4.0-fast-generate-001`), geração de imagens para advertoriais

## API Key — Conta GRATUITA (conta antiga)

```
<CHAVE-NO-.env-LOCAL>
```

- **Plano:** Gratuito (sem acesso a Imagen 4)
- **Uso:** Apenas Gemini Flash (texto), `/traduzirimagem` com `gemini-2.0-flash-preview-image-generation`

## Uso
- Para geração de imagens (Imagen 4): usar chave PAGA
- Para tradução de imagens (`/traduzirimagem`): usar chave gratuita ou paga
- O `IMAGE_PATH` é sempre fornecido pelo usuário no chat como caminho local do PC
