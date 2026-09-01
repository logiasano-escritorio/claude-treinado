---
name: Workflow avatares UGC iPhone 7
description: Skill /gerar-avatares-ugc gera 15 avatares brasileiros UGC com qualquer produto como referência. Localização e regras críticas.
type: reference
originSessionId: 24f4ed1d-1674-4cf2-87be-5a5d4575344c
---
Skill: `/gerar-avatares-ugc` (registrada em ~/.claude/CLAUDE.md, arquivos em ~/.claude/skills/gerar-avatares-ugc/).

15 personas brasileiras pré-validadas em `personas.md` da skill — independentes do produto, anexar qualquer foto comprimida de produto.

Regras críticas (descobertas na sessão 2026-05-04):
- Comprimir produto pra <150KB JPEG q88 max 1024px ANTES de mandar (ou Gemini engasga silencioso)
- Tamanho do produto na mão: ancore em "width of open palm / smaller than face / fits between thumb and pinky" — Gemini IGNORA medidas métricas (cm, ml)
- Timeout no batch: 180s por imagem (Gemini fica lento em horário de pico, não é throttle)
- Aspect ratio 9:16 (1080x1920 vertical para Stories/Reels)
- Sempre rodar batch com retry 2x + skip-se-existe pra retomar interrompido

Output validado: `strongbones/images/swap-elare/avatar-{01..15}-*.png` (sessão Sano StrongBones)
