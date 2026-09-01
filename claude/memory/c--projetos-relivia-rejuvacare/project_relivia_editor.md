---
name: relivia_editor_auditoria
description: Auditoria e implementação completa de melhorias no Relívia Editor de Criativos (Flask + Gemini)
type: project
---

Auditoria completa e implementação de todas as melhorias no app em c:/Users/user/Desktop/relivia-editor/.

**Why:** Ferramenta interna de produção de criativos de marketing para suplementos. Usada por 1-2 pessoas na Relívia. Auditoria pedida para melhorar performance, qualidade de prompts e UX.

**How to apply:** Consultar ao trabalhar em qualquer arquivo da pasta relivia-editor.

## Stack
- Backend: Python + Flask porta 5003, `app.py`
- Frontend: HTML single-file `index.html` (~1700 linhas)
- IA: Google Gemini `gemini-3.1-flash-image-preview` via `google-genai`
- Background removal: `rembg[cpu]` com modelo u2net
- Vídeo: `moviepy` + `numpy`

## Melhorias implementadas (Março 2026)

### Backend (app.py)
- **P1**: Race condition corrigida com `threading.Semaphore(MAX_WORKERS)` no lugar de contador manual
- **P3**: `img_to_bytes()` com cache `_img_cache` e leitura direta para PNG/JPG sem re-encode PIL
- **P4**: `make_video()` na fila de jobs (tipo "video") com campo `progress` em tempo real
- **P5**: rembg warm-start com `new_session("u2net")` carregado uma vez no startup
- **P7**: Limpeza automática de `outputs/` (TTL 24h) e `jobs` dict (máx 200), via `threading.Timer` a cada hora
- **Q1**: Prompt swap melhorado com 8 regras cirúrgicas (oclusão de dedos, sombras, reflexos)
- **Q2**: Prompt translate melhorado com regras para tabela nutricional, textos curvos, ANVISA disclaimer
- **Q3**: JSON de extração mais rico (13 campos: posição produto, paleta, emoção-alvo, CTA, etc.)
- **Q4**: `SUPPLEMENT_ANGLES` — 5 ângulos curados para suplementos (dor, resultado rápido, prova social, ingrediente, estilo de vida)
- **Q6**: Prompt chat com bloco `CONSTRAINTS` de preservação de elementos não solicitados

### Frontend (index.html)
- **D1**: Navegação em 3 grupos de abas (Imagem, Em Massa, Ferramentas) — sem quebra em telas menores
- **D2**: Thumbnail inline no monitor da fila quando job está `done`
- **D3**: Barra de progresso em tempo real para animação (rota `/animate` agora async)
- **D4**: Cards de variações melhorados com checkbox de seleção, edição inline, grid 2 colunas
- **D5**: Histórico de resultados em `localStorage` (últimos 60), com grid visual na aba Fila
- **D6**: Toast notifications com diagnóstico de erro por padrão (rate limit, tamanho, timeout, etc.)
- **D7**: Drag-and-drop em todos os upload boxes + exibição de nome/tamanho do arquivo
- **D8**: Dark mode toggle com `data-theme` CSS, persistido em `localStorage`
- **P8**: Polling com backoff exponencial (500ms → 5000ms) via `pollJobWithBackoff()`
- Rotas síncronas (`/swap-product`, `/translate-label`, etc.) migradas para fila no frontend
- Botão "Baixar Todos" para jobs concluídos em lote
- Botão "Copiar URL" em todos os resultados

## Estrutura de arquivos
```
relivia-editor/
  app.py          # backend Flask (880 linhas)
  index.html      # frontend single-file HTML (~1700 linhas)
  uploads/        # uploads temporários
  outputs/        # resultados gerados (auto-limpos após 24h)
  requirements.txt
```
