---
name: Imagens cross-folder Sano quebram no deploy Relívia
description: Páginas Sano portadas pra reliviabr.shop quebram refs `../strongbones/`, `../glowup/`, etc — repo Relívia não tem essas pastas. Sempre converter pra refs locais antes do deploy.
type: feedback
originSessionId: 3ab9d48b-9df8-4f63-9b5f-e2a1b74de5f0
---
Páginas geradas pela skill `/sano-pagina-v2` (ex: magnesio-gummies.html) costumam usar `../strongbones/images/swap-elare/avatar-XX.png` e `../strongbones/images/logo-sano.png` reutilizando assets do funil mestre Sano. Quando o destino do deploy é o repo **relivia-pages** (reliviabr.shop), essas pastas-irmã não existem e tudo quebra.

**Why:** Aconteceu no deploy magnesio-gummies (2026-05-11) — 6 imagens quebradas: logo header, 3 avatares do bloco social-proof-facial, 1 avatar testimonial, 1 avatar featured quote. Usuário pegou visualmente no print. Em domínio Sano não acontece porque a pasta strongbones/ está lá; em Relívia acontece silenciosamente.

**How to apply:** Antes de deploy de página Sano em repo Relívia, rodar `grep -nE '\.\./[a-z-]+/(images|assets)' <pagina>.html`. Para cada hit:
1. Avatares de UGC/depoimento → trocar por `images/ugc-carousel/ugc-XX.png` do próprio funil (já gerados pela skill `/gerar-avatares-ugc`)
2. Logo Sano → trocar por logo Relívia (`C:\projetos\relivia\pulso luz\images\logorelivia.png` é fallback confiável; copiar pra `<funil>/images/logo-relivia.png`)
3. Outras imagens cross-folder → procurar equivalente no próprio funil ou copiar fisicamente

Se for o caso oposto (página Relívia que vai pro Sano), mesma regra na direção contrária.
