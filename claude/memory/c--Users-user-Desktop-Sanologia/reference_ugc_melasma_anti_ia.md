---
name: reference_ugc_melasma_anti_ia
description: Receita de prompt UGC anti-IA (selfie caseira crua) que parou de "parecer IA" — banheiro real, celular rachado, luz feia; script gen-clarilux-ugc-melasma.py
metadata:
  type: reference
---

Criativos "antes/depois de estúdio" (fundo cinza liso, pele plástica, rosto neutro, simetria perfeita) **parecem IA/stock e não convertem** — o Guilherme rejeitou os 10 da campanha Clarilux Melasma por isso. O que funciona é UGC cru que "para o scroll": selfie de celular em casa real.

**Receita anti-IA que acertou de primeira** (`_dev/gen-clarilux-ugc-melasma.py`, modelo Vertex `gemini-3-pro-image-preview`, 4:5 vertical):
- **Câmera**: "old iPhone front camera, amateur selfie, NOT studio, NOT beauty campaign, NOT stock". Enquadramento torto, leve motion blur.
- **Luz feia proposital**: mista amarela (lâmpada de banheiro) + fria (janela); leve superexposição perto da luz; grão/noise nas sombras.
- **Pele REAL**: poros, oleosidade, linhas finas, fios soltos, tom desigual; "NO airbrushing, NO smoothing, NO plastic AI skin, NO perfect symmetry".
- **Cenário bagunçado**: banheiro com clutter, toalhas, quarto desarrumado no reflexo. Celular rachado na mão vende o realismo.
- **Emoção genuína**: incômodo/vergonha olhando a mancha, não pose de catálogo.

**Mix de 10 que testamos**: 4 só-problema (choque/identificação, sem produto) + 3 antes/depois estilo selfie (mesma pessoa, "KEEP FACE IDENTICAL") + 3 com produto na mão (i2i c/ ref, produto na palma — ver [[feedback_gemini_pote_tamanho_palma_mao]] e [[feedback_gemini_i2i_preservar_produto]]). Produto Clarilux = frasco pump branco "SANO/CLARILUX" 30ml, arte botânica rosé.

Também serve pra **antes/depois da PV e dos ADVERTORIAIS** (não só criativo Meta): split ANTES|DEPOIS mesma pessoa ("KEEP FACE 100% IDENTICAL"), 1 mulher por imagem, perfis BEM distintos (idade/tom/cabelo/cenário) pra não dar "todas iguais". Dois conjuntos corrigidos no Clarilux (todos eram clones da mesma morena em estúdio cinza):
- **PV** `pv-antes-depois-{rosto,2,3,6}` (6 total) via `_dev/gen-clarilux-ba-ugc-pv.py`, SEM badge. Backup `_dev/bkp-ba-pv/`.
- **Advertoriais** `advN-ba-*` (7: bochechas/buco-testa/mulher-madura/mulher-negra/rosto-inteiro/testa-lateral/zoom-bochecha) via `_dev/gen-clarilux-ba-ugc-adv.py`, MANTENDO badge azul ANTES/DEPOIS (pedido do Guilherme). Compartilhadas por adv v2/v3/v4/v5 → trocar arquivo corrige todos sem editar HTML. Backup `_dev/bkp-ba-adv/`. Deployado+validado na live (md5) 2026-07-16.

Reutilizável pra qualquer nicho de pele. Bate com [[feedback_before_after_estilo_ugc]] (selfie caseira, ambiente variado, validar cada uma com Read). Sempre converter webp→jpg antes de subir no Meta ([[project_campanha_clarilux_melasma]]).
