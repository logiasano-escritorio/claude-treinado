---
name: Sempre verificar quem mais usa uma imagem antes de sobrescrever
description: Antes de regenerar ou mover qualquer imagem, grepar a path por TODOS os HTMLs do projeto — paths compartilhadas quebram páginas irmãs
type: feedback
originSessionId: 9bd6982e-c870-4b26-bb8d-a96c2fc679cf
---
# Regra: nunca sobrescrever imagem sem grep global da path

Antes de regenerar/substituir uma imagem (ex: `images/resultado.webp`), SEMPRE grepar o nome do arquivo em todo o projeto pra ver quem mais aponta pra ela.

**Why:** Em projetos de páginas múltiplas (Relívia, Sano), várias páginas reusam as mesmas paths de imagem (`images/resultado.webp`, `images/info-2.webp`, `images/produto-7.webp`) com contextos completamente diferentes. Sobrescrever sem checar quebra páginas irmãs invisivelmente.

**Caso real (2026-05-11):** Regenerei `oregano-relivia/images/resultado.webp` com tema de "fungo de unha" pensando que era só pra `fungo-de-unha.html`. Sem perceber, `oregano.html` (sobre desparasitação intestinal) usava a mesma path — ficou com imagens fora de contexto até user reportar. Conserto: mover versões fungo pra `images/fungo/*` e restaurar parasitas do git history (3294a11).

**How to apply:**
1. Antes de qualquer i2i/regenerate de imagem, rodar:
   ```
   grep -r "nome-do-arquivo.ext" path/do/projeto/ --include="*.html"
   ```
2. Se mais de 1 HTML aponta pra essa path, criar subpasta dedicada (`images/<contexto>/`) e atualizar SÓ o HTML que precisa do novo conteúdo.
3. Sempre fazer backup git/arquivo antes (`_backup-<tema>/`).
4. Após push, abrir URL real de TODAS as páginas afetadas (não só a alvo).
