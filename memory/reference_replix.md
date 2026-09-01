---
name: Replix — gerador de avatares UGC
description: SaaS local em C:\Users\user\Desktop\_Projetos\replix\ (port 5004) que gera 15 avatares brasileiros via Gemini com prompts agressivos de "foto caseira"
type: reference
originSessionId: dae4ca24-9a86-4074-bc63-c8d6e766bc7f
---
**Path:** `C:\Users\user\Desktop\_Projetos\replix\`
**Port:** 5004
**Start:** `python -u app.py` (rodar com unbuffered)

## Stack
- Backend: Flask + google-genai
- Frontend: HTML/CSS/JS vanilla, dark + roxo `#7C3AED`
- Modelos: `gemini-3.1-flash-image-preview` (Nano Banana, primário) → `gemini-2.5-flash-image` (fallback)
- Timeouts agressivos: [20s, 25s, 30s] com backoffs [0s, 5s, 8s]
- Workers: 3 (5 piorou — rate limit)

## Regra crítica de modelo por tipo de tarefa
- **Tradução de texto na imagem** (template `translate`, feature "Traduzir Embalagem", regen com texto curvo): trava SÓ no `gemini-3.1-flash-image-preview` (Nano Banana). Lista `GEMINI_MODELS_TEXT_QUALITY` em app.py. Reason: gemini-2.5-flash-image inventa palavras em texto curvo/decorativo (ex: "Hy Congiue" em vez de "Pode"). Validado 2026-05-04 com magnesio-gummies/photo.webp.
- **Outras tarefas** (avatares, swap-product, trocar pessoa, casa BR, melhorar qualidade): fallback Nano→2.5 OK.

## Features (5)
1. Trocar Produto (swap)
2. Traduzir Embalagem EN→PT-BR
3. Avatares UGC (15 personas brasileiros 50+, filtros dinâmicos)
4. Fila em Massa (workers paralelos, prioridade, retry, cancel)
5. Configurações (API key + modelo + workers)

## Prompt engineering — "foto caseira agressiva" (validado 2026-05-04)
- `BASE_PROMPT` / `BASE_PROMPT_NO_PRODUCT` em `personas.py` com 30+ marcadores amadores: JPEG artifacts, luz amarela 2700K-3500K, clutter de casa brasileira, sem maquiagem, câmera tortinha 3-8°, skin texture visível
- Hard negatives: NO stock photo, NO professional headshot, NO studio lighting, NO HDR, NO airbrushed skin
- Target: "Brazilian person's WhatsApp Status photo, regular Tuesday afternoon"
- `enquadramento_map` em `app.py` — selfie/medio/aberto, todos com "ENTIRE HEAD always fully in frame, NEVER cropped"
- 3 formatos: 9:16, 1:1, 16:9 via `FORMAT_RULES` placeholder

## Frontend
- `MAX_AUTO_RETRIES = 0` (backend já cobre via model fallback, não duplica jobs)
- Modal "Gerar 15 personas novas" com 5 grupos de filtros (gênero, idade, etnia, ambiente, enquadramento, vibe)
- Botão "↺ Padrão" → `/personas/reset`
- Botão "🔄 Refazer todos com erro" no header de resultados

## Decisão: edições de TEXTO/HTML feitas via Claude Code, não via API
- Replix **NÃO** integra chat IA pra editar HTML (trocar links, headlines, etc)
- User tem plano Claude → editar via Claude Code direto custa zero, vs API extra que duplica gasto
- Replix fica focado em **manipular imagens** (gerar com Gemini, swap, traduzir, drag-drop, file picker)
- Edições de texto: usuário pede aqui no Claude Code, edito via Edit tool
