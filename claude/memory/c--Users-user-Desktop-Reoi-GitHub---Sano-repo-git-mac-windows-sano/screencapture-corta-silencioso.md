---
name: screencapture-corta-silencioso
description: PDF de screencapture corta em 14400pt sem avisar - conferir altura antes de adaptar pagina de concorrente
metadata:
  type: feedback
---

**PDF gerado por screencapture corta em 14400pt e não avisa.** A página parece
inteira: termina no meio de uma seção, sem borda, sem reticências, sem nada que
indique truncamento.

Em 2026-08-30, adaptando o advertorial de fibromialgia da SPNutrition, isso
escondeu **4 seções inteiras** do final (Picture the next few weeks · A note on
price · Try it for 30 days · If you close this page) — justamente o fecho
emocional e a oferta. Duas capturas em PDF diferentes cortaram no mesmo ponto.
Só o **PNG de 16300px** mostrou a página completa.

**Why:** entreguei a página incompleta e afirmei que "as seções conferem 1:1"
comparando contra uma referência truncada. O usuário teve que pedir de novo.

**How to apply:** ao receber captura de página de concorrente, **medir a altura
antes de adaptar**. `fitz` para PDF, `PIL` para PNG. Se a altura for exatamente
14400pt (ou outro número redondo suspeito), assumir que está cortada e pedir o
final — de preferência **em PNG**, que não tem esse limite. E ao concluir que
"não falta nada", dizer explicitamente contra qual referência isso foi checado.
