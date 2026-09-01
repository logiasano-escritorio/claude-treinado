---
name: feedback_ugc_conferir_genero_publico
description: "Ao gerar avatares UGC, conferir gênero/idade de CADA imagem antes de publicar — devem casar com o público do funil"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 77ffe71b-c21b-4cb4-9a58-1bbcf8ae4fa8
---

Avatares UGC gerados devem bater com o público do funil. Caso real: carrossel do Tônico Supremo (calvície **masculina**) foi pro ar com a ugc-5 sendo **mulher** — Guilherme pegou na hora ("tem uma mulher aqui kkkk").

**Why:** uma persona do gênero/idade errado num funil de público específico destoa e quebra a prova social (mulher num funil de calvície masculina).

**How to apply:**
- A skill `/gerar-avatares-ugc` usa personas em `_dev/gen-ugc-cosmeticos.py` que são majoritariamente seniors/mistos. Pra público específico (homem 30-50, calvície), **customizar os personas** no script (homens com cabelo visível) e ajustar o BASE (produto = spray capilar, não "supplement bottle").
- SEMPRE ler/conferir cada .webp gerado com a tool Read ANTES de commitar — validar gênero, idade, cabelo (pra produto capilar), produto na palma, rótulo legível.
- Regenerar individualmente é barato: deletar o arquivo torto e rodar script de 1 imagem (mesmo nome → HTML não muda). Cuidado com 429 RESOURCE_EXHAUSTED da chave Vertex (retry com 35s).

Ver [[reference_vertex_ai_setup]] e [[feedback_gemini_pote_tamanho_palma_mao]].
