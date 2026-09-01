---
name: feedback_foto_aplicando_produto_real
description: "Foto de pessoa aplicando creme/produto tem que mostrar o produto REAL na mão, nunca um pote genérico"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 77ffe71b-c21b-4cb4-9a58-1bbcf8ae4fa8
---

Qualquer imagem gerada de uma pessoa **aplicando** algo (creme, gel, óleo, spray) DEVE mostrar **o produto real da marca na mão** — embalagem fiel — NUNCA um pote/tubo genérico aleatório que o Gemini inventa.

**Why:** o objetivo da foto de aplicação é fazer o avatar associar o gesto ao SEU produto; pote branco genérico desperdiça a prova e fica amador. Caso real: `g2-aplicando-fem.webp` (advs Gabapentina) saiu com um potinho branco qualquer — Guilherme: "não é o meu creme, tem que botar o Prime Creme na mão dela".

**How to apply:** gerar a imagem de aplicação via i2i passando a foto hi-fi do produto como referência (ex: `g-produto-cine.webp` = tubo Prime preto/logo verde/tampa branca) + "reproduce this 1:1, DO NOT redesign or replace into a generic jar". Conferir lendo a imagem antes de commitar. Vale o mesmo cuidado de [[feedback_gemini_i2i_preservar_produto]] e a checagem manual de [[feedback_before_after_estilo_ugc]]. Prime Creme é TUBO (bisnaga preta), não pote.
