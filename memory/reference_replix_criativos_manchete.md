---
name: Replix — feature Criativos Manchete
description: Aba "Criativos Manchete" no Replix gera criativos FB Ads estilo AlinhaFácil pra qualquer produto
type: reference
originSessionId: bb15eb26-1191-4282-907c-cdda71f1fccd
---
O Replix (localhost:5004) tem uma aba **"📰 Criativos Manchete"** na sidebar (categoria "Criativos") que gera N criativos no estilo AlinhaFácil pra qualquer produto.

**Fluxo:**
1. User faz upload de arquivo HTML local OU cola URL pública da página de venda
2. Backend (Sonnet via Claude Agent SDK) analisa e extrai briefing: produto / problema / ângulo / vilão / estatísticas / tags visuais
3. User revisa o briefing num form editável
4. Escolhe quantidade: 5 / 11 / 15 / 30
5. Sonnet gera a copy de cada criativo (headline + palavras_ciano + subheadline + descrição da imagem do círculo + template A/B/C/D + footer brand)
6. Gemini 3.1 Flash Image Preview gera as imagens 1080x1080
7. Grid mostra resultados, criativos salvos em `outputs/criativos-manchete/{timestamp}-{slug}/`

**Backend:**
- Módulo: `criativos_manchete.py` (análise + geração de copy + geração de imagem)
- Rotas no `app.py` (no final, antes do boot):
  - `POST /api/criativos-manchete/analyze` (file ou url)
  - `POST /api/criativos-manchete/generate-copy` (briefing + count)
  - `POST /api/criativos-manchete/generate-images` (criativos + slug)
  - `GET /outputs/criativos-manchete/<subpath>` (serve arquivos gerados)

**Frontend (index.html):**
- Botão sidebar `setTab('criativos-manchete')`
- Section `id="tab-criativos-manchete"` com 4 cards (Input → Briefing → Quantidade → Resultados)
- JS no final: cmState, cmAnalyze(), cmGenerate(), cmSetQty(), drag-drop do HTML

**Tipo de criativos:** Templates A (Revelação Médica), B (Investigação), C (Urgente/Sintoma), D (Pós-cirurgia). Mix automático.

**Modelo Gemini:** `gemini-3.1-flash-image-preview` (já é o default do Replix em `CONFIG["gemini_model"]`).
