---
name: feedback_before_after_estilo_ugc
description: Before/after de produto deve usar o DNA UGC iPhone caseiro da skill gerar-avatares-ugc — não estúdio/IA
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 77ffe71b-c21b-4cb4-9a58-1bbcf8ae4fa8
---

Antes/depois de cliente NÃO pode ter cara de "foto de estúdio gerada por IA" (fundo cinza liso, pose rígida, produto colado no peito ou flutuando). O Guilherme reclamou 2x: "ficou muito IA, parece foto de estúdio, não parece ser humano real".

**Why:** before/after é prova social — se parece IA/estúdio, perde credibilidade. Tem que parecer selfie real de cliente postada no WhatsApp/Stories.

**How to apply (o que funcionou no Tônico):**
- Usar o **BASE prompt da skill `gerar-avatares-ugc`** (`~/.claude/skills/gerar-avatares-ugc/personas.md`): "Hyperrealistic amateur iPhone selfie, hand-held casual UGC, looks like a REAL customer review on WhatsApp — NOT studio, NOT brand campaign. Subtle digital noise, lens flare from window, realistic skin texture (pores/peach fuzz/fine lines), NO airbrushing, NO plastic AI skin, NO studio lighting, NO grey seamless backdrop."
- **Ambiente caseiro REAL e variado por pessoa** (banheiro com espelho/box, sala com sofá/planta, cozinha com armários, varanda) — não fundo neutro.
- **Produto na mão tamanho palma**, segurado de jeito natural (NUNCA colado no peito, NUNCA flutuando, NUNCA oversized) — âncora: "bottle height ~ width of open palm, smaller than face".
- **EXACTLY ONE person** por metade (Gemini duplica pessoa se não restringir).
- Par antes/depois = MESMA pessoa: gerar o ANTES, usar como ref de identidade do DEPOIS ("same person, same room/lighting, only the hair/skin improves"). Ver [[feedback_consistencia_personagem_advertorial]].
- 5 personas DISTINTAS entre si (idade/etnia/tom de pele/cabelo) — senão "todas iguais só muda a cor". Ver [[feedback_ugc_conferir_genero_publico]].
- SEMPRE validar olhando cada imagem (Read) antes de publicar.
- Script ref: `_dev/gen-tonico-ba-ugc.py`.
