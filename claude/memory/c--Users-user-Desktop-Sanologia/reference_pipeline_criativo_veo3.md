---
name: reference-pipeline-criativo-veo3
description: "Pipeline canonico de geracao de criativos UGC Veo 3 — 7 cenas com regra \"produto entra so na cena 5\"; usa Ingredients-to-Video (REF-A sem produto + REF-B com produto); playbook completo no Obsidian Supremo"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 404b5064-1f9d-4540-aad3-f47e91f0bd1c
---

# Pipeline Criativo UGC — Veo 3.1 (Relivia/Sano)

**Documento mestre:** `c:/Users/user/Desktop/Obsidian Supremo/Relivia Context/Playbooks/PIPELINE-CRIATIVO-UGC-SUPLEMENTO.md`

**Guia de prompting Veo 3:** `c:/Users/user/Desktop/Obsidian Supremo/Relivia Context/Memory/References/veo3-prompting-guide.md`

**Case de origem:** Relivia Oregano + Nigela (2026-04-28). 100+ conversoes, Copy Master score 8.4/10.

## A regra "produto na mao" — POR ISSO ELE PERGUNTOU

**7 cenas de 8s (56s totais)**, e o produto NAO aparece em todas:

| Cena | Tempo | Conteudo | Produto? |
|---|---|---|---|
| 1 | 0-8s | Hook + autoridade previa | **SEM** |
| 2 | 8-16s | Credencial completa | **SEM** |
| 3 | 16-24s | Big Claim + promessa | **SEM** |
| 4 | 24-32s | Beneficios densos + principio ativo | **SEM** |
| 5 | 32-40s | Stack + **pega produto** ⭐ | **COM** (entra aqui) |
| 6 | 40-48s | Marca + qualificadores + urgencia | **COM** |
| 7 | 48-56s | CTA duplo (link + pergunta) — **solta produto** | **SEM** novamente |

**Why:** produto desde cena 1 ativa modo defesa-anti-anuncio. Prende atencao pela autoridade primeiro, vende depois. Sair com maos livres no CTA mantem foco humano.

## Ingredients-to-Video (3 referencias, nao 1)

Veo 3 sofre de **latent drift** — frasco muda de tamanho/rotulo entre frames. Solucao: 3 imagens separadas.

| Ref | O que e | Quando subir |
|---|---|---|
| **REF-A** | Apresentadora SOZINHA, jaleco no consultorio | Cenas 1-4 e 7 (todas que nao tem produto) |
| **REF-B** | Apresentadora COM produto na mao, mesmo consultorio, mesma identidade | Cenas 5 e 6 |
| **REF-C** (opc) | Transicao — momento pegando o frasco | Cena 5 (se quiser refinar transicao) |

**⚠️ Critico:** se subir REF-B desde cena 1, Veo "alucina" e enfia o frasco no fundo da mesa mesmo sem pedir. Subir REF-B SO a partir da cena 5.

## Ordem de geracao (NAO sequencial)

1. **Cena 5 primeiro** (mais dificil — continuidade pessoa+produto+transicao)
2. Cena 6
3. Cenas 1, 2, 3, 4
4. Cena 7 por ultimo

**Why:** se cena 5 sai boa, demais se alinham. Se gerar cena 1 primeiro pode chegar na 5 e quebrar continuidade.

## 4 Fases do Pipeline

1. **Analise** — `copy-master:tasks:analyze-copy` faz engenharia reversa do criativo campeao
2. **Evolucao tripla em PARALELO** — Dan Kennedy (urgencia) + Alex Hormozi (oferta) + Stefan Georgi (5 var A/B)
3. **Roteirizacao** — 7 cenas timestamp prompting com regra produto na mao
4. **REFs e geracao** — REF-A sozinha + REF-B com produto via Gemini/GPT-4o → Veo 3.1 via Google Flow ou Vertex AI

## Anchor obrigatorio (cenas COM produto)

```
CRITICAL ANCHOR: Do not modify the product jar. Keep the exact [marca]
supplement bottle from REF-B — same proportions, same label, same accent
color, same size relative to her hand.
```

## Bloqueios obrigatorios em TODO prompt

```
(no subtitles)
(no text overlays)
(no captions)
```

## How to apply

Quando user pedir "criar criativos UGC Veo 3" pra um produto Sano/Relivia:
1. Ler o playbook completo em `Obsidian Supremo/Relivia Context/Playbooks/PIPELINE-CRIATIVO-UGC-SUPLEMENTO.md`
2. Aplicar as 4 fases — analise → evolucao tripla → roteirizacao 7 cenas → REFs
3. Respeitar regra produto-cenas-5-6 e ordem de geracao 5→6→1→2→3→4→7

## NAO confundir

- **Veo 2 ([[reference_workflow_videos_veo2]])** — videos AUTOPLAY pra inserir na pagina (mecanismo/sintoma/before-after, SEM pessoa segurando produto). Roda via agent `veo2-video-producer`.
- **Veo 3 (este doc)** — CRIATIVOS UGC pra Facebook Ads (apresentadora falando, 7 cenas com regra produto-na-cena-5).
- **Avatares UGC ([[reference_workflow_avatares_ugc]])** — IMAGENS estaticas Gemini 3.1 pra carrossel infinito. Sao 15 personas brasileiras com produto, formato 1080x1920.

Os 3 sao complementares: avatares estaticos no carrossel da pagina, Veo 2 autoplay no meio do scroll, Veo 3 nos anuncios Meta.
