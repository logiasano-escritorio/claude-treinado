---
name: reference-workflow-videos-veo2
description: "Fluxo Veo2 pra gerar videos autoplay nas paginas Relivia/Sano — agent veo2-video-producer + script Python no relivia-editor; cenas mecanismo/sintoma/before-after, NUNCA produto na mao"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 404b5064-1f9d-4540-aad3-f47e91f0bd1c
---

# Fluxo de geracao de videos Veo (Veo **2**, nao Veo 3)

Quando usuario fala "Veo3" ele esta se referindo ao MESMO pipeline que ja roda Veo2 — nao existe um pipeline Veo3 separado. O agent registrado e `veo2-video-producer` (`~/.claude/agents/veo2-video-producer.md`) usando `veo-2.0-generate-001`.

## Arquitetura

- **Agent:** `veo2-video-producer` — analisa pagina (produto ou advertorial) e decide onde inserir video
- **Editor local:** `C:/Users/user/Desktop/_Projetos/relivia-editor/` — gera scripts `gerar_videos_{nome}.py`
- **API Key Google:** em [[reference_chaves_gemini]] (mesma chave Gemini)
- **Modelo:** `veo-2.0-generate-001`
- **Output:** `outputs_{nome_pagina}/` na pasta do editor; depois copiar pra `videos/` no projeto

## As 7 cenas canonicas (referencia: orégano)

Ordem psicologica testada — nao e UGC nem produto, sao mecanismos/emocoes:

1. **vid1-hero** — macro CGI do problema invisivel (intestino, ossos, neuronios). 8s. Ativa "tenho isso".
2. **vid2-sintomas** — pessoa real espelho do sintoma. Brasileira, casa, luz fria. 6s. Reconhecimento.
3. **vid3-mecanismo** — CGI farmaceutico do ativo destruindo o problema. 8s. Credibilidade visual.
4. **vid4-beforeafter** — split-screen mesma pessoa antes/depois. 8s. Projecao identitaria.
5. **vid5-timeline** — macro do processo na semana 1. 6s. Ancora temporal.
6. **vid6-garantia** — escudo materializando em particulas. 6s. Garantia visceralmente real.
7. **vid7-urgencia** — caixas do produto somindo sob spotlight (urgencia visual). 6s. FOMO sem texto.

## Regras criticas

**Why:** sao as regras que decidem se o video converte ou afunda a pagina.

- **NUNCA** substituir foto real de produto por video CGI — perde realidade comercial
- **NUNCA** colocar produto na mao de personagem dentro do video Veo2 — Veo2 nao consegue manter consistencia do produto entre frames; cenas "com produto" sao [[reference_workflow_avatares_ugc]] (Gemini Image, imagem estatica), nao Veo2
- **NUNCA** inserir video dentro de secao "Apresentando [produto]" ou cards de produto
- **NUNCA** prompt com texto/logo/overlay — Veo2 nao suporta
- **SEMPRE** `autoplay muted loop playsinline` na tag video (obrigatorio iOS)
- **SEMPRE** prompt 80-150 palavras em ingles com camera/luz/personagem/mood especificos
- Fallback quando 429/timeout: imagem com nome equivalente (`v1-img7-*.png` pra `v1-vid7-*.mp4`), NUNCA produto.

## How to apply

Quando usuario pedir "videos pra pagina X":
1. Invocar Agent `veo2-video-producer` com path da pagina
2. Ele cria `gerar_videos_{nome}.py` em `_Projetos/relivia-editor/`
3. Usuario roda o script (Veo2 demora 2-5min por video, paralelizar nao da)
4. Quando terminar, agent copia MP4s pra `videos/` no projeto e insere `<video autoplay muted loop playsinline>` nos pontos da pagina
5. Commit + push

Custo: ~$0.50/segundo de video. 7 cenas de 6-8s = ~$25-30.

## NAO confundir com avatares UGC

Avatares UGC ([[reference_workflow_avatares_ugc]]) = **imagens estaticas** Gemini 3.1 com pessoas brasileiras segurando produto. Vai num **carrossel infinito** na pagina.

Videos Veo2 = **MP4 autoplay** com cenas SEM produto na mao (mecanismo + emocao + before/after).
