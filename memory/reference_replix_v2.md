---
name: Replix v2 — Page Builder Híbrido com catálogo de slots
description: Estado atual do Replix após 2026-05-06 — pipeline catálogo de 22 slots visíveis (29 total, 7 deprecated), Auto-Imagens, persistência, slot batch, catálogo visual em HTML
type: reference
originSessionId: d2c18d3e-aab0-440a-b3c4-86d8c38e0c1d
---
# Replix v2 — Estado atual (2026-05-06)

**Localização:** `c:/Users/user/Desktop/_Projetos/replix/` (Flask, porta 5004)

⚠️ **NÃO confundir com `Desktop/Replix/`** — essa é a pasta de OUTPUTS (páginas geradas), não o código.

## Pipeline (Etapa 1→5)

1. **Analisar** — Sonnet via Claude Agent SDK ($0) extrai briefing do dump (bookmarklet) + detecta `produto_visual.perfil` (supplement|device|topical)
2. **Escolher Ângulo** — original + 3-4 alternativos, cor da paleta, idioma
3. **Editar Copy** — gera 24-28 blocos via Sonnet
4. **Renderizar HTML** — DeepSeek V4-Flash gera HTML completo (~166s, R$0,12) com `<img data-pb-slot="N">`
5. **Auto-Imagens** — Gemini Nano Banana gera cada slot do catálogo (~12s/img, R$0,20/img)

**Custo total por página:** ~R$ 5-8

## Catálogo de slots (29 total · 22 visíveis · 7 deprecated)

`c:/Users/user/Desktop/_Projetos/replix/images_catalog.py`

**Visíveis (22):** 1, 2, 3, 4, 5, 6, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29

**Deprecated (mantidos pra retro-compat de sessões antigas, mas filtrados do front):**
- 7, 8, 9, 10 (timeline 4 estágios — substituídos pelo batch slot 29)
- 11 (Selfie casual indoor) + 12 (Senior portrait poltrona) — substituídos pelo slot 28 (Persona casual auto)
- 15 (UGC selfie single) — caso particular do slot 27

**Slots especiais:**
- **Slot 27** — Carousel UGC infinito (`is_carousel=True`, gera 15 avatares via `personas.py`)
- **Slot 29** — Timeline 4 estágios (`is_batch=True`, `batch_count=4`, `batch_prompts=[...]`, gera `timeline_01.png`...`timeline_04.png`)
- **Slot 28** — Persona casual unificada (1 imagem, prompt adapta jovem/senior conforme `publico_alvo`)

**Workers especializados em `app.py`:**
- `_pb_process_carousel_slot` — slot 27 (15 avatares)
- `_pb_process_batch_slot` — slot 29 (4 timeline; reusa arquivos já existentes)
- `_pb_process_one_slot` — todos os outros (dispatch com branches `is_carousel` / `is_batch`)

## Bugs corrigidos em 2026-05-06

1. **Scroll do preview resetava no topo** ([app.py preserve scrollY]) — `pbImageReloadPreview()` salva `iframe.contentWindow.scrollY` antes de mudar src e restaura no `load`
2. **Reuso de avatares já gerados** ([app.py:3877]) — `if os.path.exists(avatar_NN.png): continue` em vez de regerar; economiza R$5-8 + 5min
3. **Bug do remove-slot deixava CSS empilhado** ([app.py:4581]) — wrappers com CSS dedicado agora têm marcador `<style data-pb-style-for-slot="N">`; remove-slot regex limpa todas as ocorrências antes de remover a section

## Catálogo visual de slots (preview HTML)

`Desktop/Replix/_catalog_previews/slots-catalog-preview.html`

HTML standalone com **22 cards** (1 por slot visível) mostrando:
- Header: `#NN` gigante + nome + descrição + tags (aspect, profiles)
- Render fiel do wrapper HTML com copy real-genérica
- Imagens reais (existentes em projetos antigos OU geradas em `_catalog_previews/images/`)

**Quando usar:** abrir como referência ANTES de inserir slot novo numa página — vê visualmente o que cada um é.

**Dor identificada (FUTURO, NÃO IMPLEMENTADO):** o catálogo só mostra a IMAGEM do slot, não a SEÇÃO COMPLETA (headline + parágrafo + bullets + img). Quando o usuário-final usar o Replix, precisa virar "Templates de seção" com placeholders de copy. Por enquanto, o GO usa só pra ele mesmo, então tá ok.

## Auto-Imagens — features

- Botão **🔄 Regenerar**, **⋯ Trocar slot**, **🗑️ Remover** por card
- **➕ Adicionar Slot** (header tela 5) — modal 2 passos
- Iframe **live preview** sticky lado direito (auto-reload preservando scroll)

## Persistência

**Sobrevive a:** refresh browser, fechar aba, restart servidor, reboot PC.

- **Frontend:** localStorage `replix_pb_session`
- **Backend:** `Replix/projetos/{idioma}/{slug}/_session.json` + index global `Replix/projetos/_sessions_index.json`

## Endpoints principais

- `GET /api/page-builder/list-slots` — agora filtra `_deprecated`, retorna `is_carousel` e `is_batch` no JSON
- Resto: render-html, process-images, regenerate-image, add-slot, remove-slot, list-anchors

## Pasta de output

`Desktop/Replix/projetos/{idioma}/{slug}/`
- `index.html`, `images/img_NN_slotNN.png`, `avatar_NN.png`, `timeline_NN.png`
- `briefing.json`, `blocos.json`, `_session.json`, `uploads/produto.png`
