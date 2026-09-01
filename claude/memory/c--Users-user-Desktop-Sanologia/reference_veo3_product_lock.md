---
name: veo-3-product-lock-anti-drift-de-produto-em-v-deo-falado
description: Como impedir o Veo 3 de distorcer o rótulo do produto entre frames em vídeos de doutora/apresentador falando
metadata: 
  node_type: memory
  type: reference
  originSessionId: e5c492e8-6e6c-4ca5-aded-b576bcf39982
---

Veo 3 sofre **latent drift**: mantém o produto na 1ª frame mas reinterpreta rótulo/cor ao longo dos 8s. Validado funcionando no VSL upsell Prime (doutora + 3 tubos na mesa), jun/2026.

**A solução (3 partes no prompt):**

1. **Bloco ANCHOR descritivo no INÍCIO do prompt** — descrever o rótulo item por item "ensina" o Veo a segurar. Ex Prime Creme:
```
ABSOLUTE PRODUCT LOCK: the three tubes on the desk stay 100% IDENTICAL every frame — black matte squeeze tubes on white flip-cap bases, label top to bottom: green "POTENTE" stripe, green leaf icon, "Prime" in white, "CREME POTENTE" in gold, dark body silhouette with glowing orange pain points, "Gel Creme de Massagem", "CONTEÚDO 90 G". Do NOT redraw, recolor, or morph text. Tubes are frozen static props.
```

2. **Câmera travada** — movimento de câmera é o maior causador de drift:
```
Camera completely static on tripod, no zoom. Only the woman moves — tubes do not move or change.
```

3. **Separar o que anima do que congela** — "Subtle motion only: [expressão], blinking."

**Outras regras do pipeline de vídeo-VSL Veo 3 (doutora falando):**
- Limite ~8s = **máx ~22 palavras faladas** por clipe. Mais que isso, corta. Fatiar o roteiro em microclipes de 1 frase.
- **NÃO nomear a doutora** na fala ("Dra. Helena" buga a pronúncia). Ela fala sem se nomear.
- Imagem de referência tem que mostrar o produto NÍTIDO (tubo pequeno/de longe = Veo não tem pixels pra preservar).
- Sobra de silêncio no fim do clipe (fala acaba ~4-5s, sobram 3s): cortar o rabinho parado no CapCut, não mexer no prompt.
- Bloqueios sempre: `(no subtitles) (no text overlays) (no captions)` — legenda queima depois no CapCut com texto certo.
- Se um clipe sair com produto torto: **regenerar só ele** (cada geração é loteria).

Imagem da doutora aprovada + script: ver [[project_upsell_whatsapp_pos_compra]]. Geração via Gemini/Vertex: [[reference_vertex_ai_setup]].
