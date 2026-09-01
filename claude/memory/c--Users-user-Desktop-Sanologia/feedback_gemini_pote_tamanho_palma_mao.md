---
name: feedback-gemini-pote-tamanho-palma-mao
description: Pote de suplemento Sano/Relívia tem ~9cm — Gemini renderiza GIGANTE por padrão se não ancorar tamanho explícito no prompt
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e8cd72f1-d4e6-4361-a4aa-5dde3e8e8a6c
---

# Pote de suplemento sempre cabe na palma da mão

**Regra:** Quando gerar foto i2i com pessoa segurando pote Sano/Relívia, **SEMPRE incluir âncora explícita de tamanho** no prompt — caso contrário Gemini renderiza o pote do tamanho da cabeça ou torso da pessoa.

**Dimensões reais (90g gummy):**
- ~9 cm altura
- ~6 cm largura
- Cabe confortavelmente na palma de um adulto, com dedos sobrando
- Menor que a face da pessoa
- Menor que o torso de uma criança

**Why:** Gemini 3.1 Flash Image tende a inflar o produto quando o briefing diz "holding the bottle". Sem âncora numérica e referência comparativa (palma/face/torso), o modelo gera **pote do tamanho de garrafa de água ou pote de tinta** — fica ridículo, parece anúncio de produto industrial, não suplementação doméstica.

**How to apply:** Em TODOS os prompts i2i com produto + pessoa, incluir bloco `SIZE_ANCHOR` com:

1. Tamanho absoluto em cm
2. Referência relativa ("fits comfortably in adult palm")
3. Comparativos negativos ("SMALLER than face, SMALLER than torso")
4. % máximo do frame (8-12%)
5. Postura da mão ("casually in ONE hand, NOT both hands like a trophy")
6. Posicionamento no corpo ("waist or chest level, naturally")

**Exemplo de âncora validada (testemunhos Sano Kids TDAH 2026-05-18):**
```
ABSOLUTE SIZE CONSTRAINT: The Sano Kids bottle is a SMALL supplement jar,
approximately 9 centimeters tall and 6 centimeters wide. It fits comfortably
in an adult palm with fingers extending beyond it. It is SMALLER than an
adult's face. It is SMALLER than a child's torso. Roughly the size of a small
jar of moisturizer or a tube of toothpaste standing up. NEVER render the
bottle larger than the person's hand span. NEVER render it as big as the
child's chest or head. In the composition, the bottle should occupy at most
8-12% of the frame area, held naturally in one hand — not gripped with both
hands like a trophy. The hand holding it should appear PROPORTIONATELY LARGER
than the bottle, not smaller.
```

**Casos onde isso quebrou:**
- 2026-05-18: 5 testemunhos Sano Kids TDAH (mae-camila/patricia/renata/juliana/mariana). Crianças seguraram pote com 2 mãos como troféu, pote ficou do tamanho do peito/cabeça. Regenerei com SIZE_ANCHOR + parent segurando casual em 1 mão.

**Conecta com:** [[feedback_gemini_i2i_preservar_produto]] (preservar produto via input fiel) e [[reference_workflow_avatares_ugc]] (workflow avatares iPhone 7).
