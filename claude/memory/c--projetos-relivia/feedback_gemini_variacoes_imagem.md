---
name: Feedback geração de variações de imagem com Gemini
description: Problemas recorrentes ao gerar variações de imagem via Relívia Editor — produto errado e texto em inglês
type: feedback
originSessionId: a4819caf-f8a2-4f89-98d2-79101da7e43e
---
Ao gerar variações de imagem com Gemini via Relívia Editor (/queue/swap com instruction), dois problemas recorrentes aparecem e devem ser evitados nos prompts:

1. **Produto aleatório na imagem** — quando o prompt menciona "place a bottle of oregano oil supplement next to the foot", o Gemini inventa um produto genérico que não é o Relívia. Não usar esse tipo de instrução sem fornecer a imagem do produto real como referência separada.

2. **Texto em inglês** — quando o prompt usa termos em inglês como "before/after", o Gemini escreve o texto na imagem em inglês. Sempre especificar explicitamente: "all text in the image must be in Brazilian Portuguese" ou simplesmente escrever o prompt inteiro em português.

**Why:** Duas imagens descartadas da geração de 30 variações para campanha Orégano fungo de unha por esses motivos.

**How to apply:** Em qualquer geração em massa de variações para campanhas BR, adicionar no início de cada instrução: "All text in the image must be in Brazilian Portuguese." E nunca pedir para adicionar produto sem enviar a imagem do produto como arquivo separado.
