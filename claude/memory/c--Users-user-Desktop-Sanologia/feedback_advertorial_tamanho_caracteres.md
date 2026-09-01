---
name: Texto de anúncio Sano tem 7-14k caracteres (NÃO 20-30k)
description: Long-form ad copy (texto principal do post FB Ads) deve ter 7.000-14.000 caracteres — NÃO confundir com advertorial nem com playbook de análise
type: feedback
originSessionId: 3ab9d48b-9df8-4f63-9b5f-e2a1b74de5f0
---
**CORREÇÃO IMPORTANTE — REGISTRO ANTIGO ESTAVA ERRADO.**

Existem 3 tipos de documento e cada um tem tamanho diferente. NÃO confundir:

1. **Texto de anúncio (long-form ad copy)** — é o que vai no campo "Texto principal" do post do Facebook Ads. Não confundir com advertorial. Tamanho real dos campeões escalados: **7.000-14.000 caracteres**. Os 4 originais em inglês que o usuário compartilhou em 2026-05-11 tinham:
   - Texto 1 (Sedona retiro POV protagonista): 7.468 chars
   - Texto 2 (Sedona POV funcionária): 8.810 chars
   - Texto 3 (8 marcas falharam, POV oito tentativas): 10.550 chars
   - Texto 4 (GLP-1/Ozempic + cortisol, POV nicho): 13.509 chars
   - Originais salvos em: `Sanologia/magnesio-gummies/copys-advertorial/_originais-en/`

2. **Advertorial (artigo/landing intermediária pra onde o anúncio linka)** — esse SIM é mais longo (15-30k chars), formato de matéria jornalística com CTAs para checkout. NÃO é o mesmo que texto de anúncio.

3. **Playbook estrutural / análise (metadocumento)** — documento de análise que decodifica estrutura dos copies. NÃO é copy de venda. O `_ANALISE_ESTRUTURAL_PLAYBOOK.md` tem 30.442 chars — é meta-trabalho, não copy.

**Why:** Em 2026-05-11 o usuário corrigiu duas vezes. Primeiro me confundi: chamei texto de anúncio de "advertorial" quando estava implementando feature no Replix. Depois confundi de novo o tamanho — anotei "20-30k chars" baseado no tamanho do playbook (que não é texto de anúncio). Usuário pediu pra contabilizar (não estimar) — contagem real dos 4 originais ficou em 7.468 a 13.509 chars.

**How to apply:**
- Ao gerar texto de anúncio Sano (skill `/copy-anuncio`, Replix aba "Texto de Anúncio", agentes de copy): mirar **7.000-14.000 chars**
- Se o usuário pedir advertorial (artigo intermediário, página com CTAs), aí sim mira 15-30k
- Sempre CONTAR com `wc -c arquivo.txt` antes de entregar — não estimar
- Se for diferente de texto de anúncio (ex: playbook, análise estrutural), não aplicar essa regra de tamanho

**Confusão a evitar daqui pra frente:**
- "Texto de anúncio" = post do Facebook Ads (7-14k)
- "Advertorial" = página/artigo onde o anúncio linka (15-30k)
- "Playbook" = metadocumento de análise (30k+)
