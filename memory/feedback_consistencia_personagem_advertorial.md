---
name: feedback_consistencia_personagem_advertorial
description: "Em advertorial narrativo, o MESMO personagem deve ter o MESMO rosto em todas as fotos — usar i2i com referência de identidade"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 77ffe71b-c21b-4cb4-9a58-1bbcf8ae4fa8
---

Em advertorial com narrativa em 1ª pessoa (ou personagem recorrente), TODAS as fotos do mesmo personagem têm que mostrar a MESMA pessoa. Gerar cada imagem isolada faz o rosto mudar a cada foto e quebra a imersão/credibilidade — o Guilherme pegou isso no adv-prime-gabapentina ("uma hora um senhor, outra hora outro").

**Why:** o leitor segue a história achando que é a mesma pessoa; rosto diferente a cada foto destrói a prova social/narrativa.

**How to apply:**
- Identifique quais imagens mostram o ROSTO de um personagem recorrente (narrador, familiar). Personagem que aparece 1x só não precisa de consistência.
- Gere/escolha UMA imagem-âncora do personagem (a hero costuma servir; pode recortar o rosto/torso pra ref mais limpa).
- Regenere as outras fotos dele via i2i passando a imagem-âncora como PRIMEIRA referência + prompt "the first reference shows X — keep his face/hair/identity IDENTICAL". Pode somar a ref do produto como 2ª imagem quando ele segura o produto.
- Validar lado a lado (Read) antes de publicar.
- Script exemplo: `_dev/gen-prime-gaba-consistencia.py`.

Ver [[feedback_ugc_conferir_genero_publico]] e [[feedback_gemini_i2i_preservar_produto]] (i2i preserva referência) e [[project_advertoriais_tonico]].
