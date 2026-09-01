---
name: reference_raspar_ad_library_drissionpage
description: "Raspar a Meta Ad Library de graça via DrissionPage (sem token/Apify) — mercado gringo, campeões +30d"
metadata:
  node_type: memory
  type: reference
  originSessionId: 7c722b03-0e07-4b10-9a06-8394a9f4326c
---

Dá pra extrair anúncios campeões da **Meta Ad Library** de graça, SEM token Meta, SEM Apify — a página `facebook.com/ads/library` é pública e o **DrissionPage** raspa sem bloqueio (testado 2026-07-06, nicho melasma/Clarilux). Apify (`curious_coder/facebook-ads-library-scraper`, $0.75/1k) é alternativa paga, mas não precisa.

**Truque-chave:** interface **pt-BR** (`--lang=pt-BR`) + `country=US/DE/ES` na URL → mostra ads do mercado gringo com o rótulo **"Veiculação iniciada em DD de mês de AAAA"** que o parser PT lê. Se usar `--lang=en-US`, os metadados do card (Library ID/data) NÃO vêm no HTML estático e o filtro de dias quebra.

**Filtro de campeão:** `active_status=active` + parsear a data de início → só **+30 dias ativo** = comprovadamente converte (senão já teria pausado).

**⚠️ ARMADILHA `media_type=image`:** esse filtro corta ~99% dos ads em mercados que rodam vídeo/carrossel. Ex Alemanha melasma: `media=image` mostra **4 ads**, `media=all` mostra **490**, `media=video` 300, `media=meme`(carrossel) 130. Concluí "mercado morto" errado por causa dele — Guilherme insistiu que tinha ads e estava certo. SEMPRE checar `media=all` primeiro pra medir o mercado real; só filtrar formato depois de saber onde está o volume. Pra "sem vídeo": usar `media_type=image` + `media_type=meme` (carrossel) separados. Contar volume por termo via regex `~?([\d\.]+)\s*resultado` antes de raspar (busca de UMA palavra acha mais que frase longa; `+` NÃO é OR no FB, restringe). Anchor de cada card = "Identificação da biblioteca". Link de destino vem em `l.php?u=<url>` (skipar instagram/fb.me/whatsapp = clínica local; domínio próprio = e-commerce concorrente).

**BR de melasma é lixo** (só clínica local no Insta) — o dinheiro roda em US/DE/ES. Matriz de termos por ângulo×idioma no `_dev/adlib-dominios.py` (5 ângulos: melasma/sol-idade/acne/gravidez/poros). Saída em `_dev/adlib-out/dominios_*.{json,txt}`. Fase 2 (vídeo): transcrever via ElevenLabs no Make. Pipeline DTC completo: raspa → Gemini vê padrão em 3+ ads → Claude escreve briefs.
