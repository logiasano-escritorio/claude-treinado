---
name: feedback_push_estoura_com_midia_pesada
description: git push no repo Sanologia dava HTTP 500 por vídeos/criativos pesados commitados; .gitignore corrigido em 2026-06-24
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 51223cb4-7e88-46ec-849a-1cba305fea7b
---

`git push origin main` no repo Sanologia (github.com/relivia-ww/sanologia) falhava com `RPC failed; HTTP 500` / `remote end hung up` — o exit code do git mentia (vinha 0 com "Everything up-to-date" de retry interno; sempre conferir o output real e `git ls-remote origin main`).

**Causa:** commits antigos arrastaram mídia bruta gigante pro tracking — vídeos `.mp4`/`.mov`/`.MOV` de 60–180MB (`prime/images/Downloads/`), gifs de 12MB (`LUMEE-ADV/`), e ~107 PNGs de criativos de anúncio (`*/images/ads/`, `*/anuncios-fb/`, `TODOS OS PRODUTOS SEM FUNDO/`). Pack estourava o limite do GitHub.

**Fix aplicado (2026-06-24):** ampliei `.gitignore` com `*.mp4 *.mov *.MOV *.mp3 *.gif *.webm` + pastas de criativos/refs/assets brutos; `git reset --soft origin/main` + re-stage (respeita gitignore) + 1 commit limpo. Pack caiu de 60MB+ pra 11MB. Nada apagado do disco.

**Why:** essas pastas NÃO são servidas nas páginas de venda (confirmado por grep nos HTMLs) — só estouravam o push. Bate com [[reference_estrutura_pasta_deploy]] (só HTML/imagens usadas vão pro Vercel).

**How to apply:** se push der HTTP 500 de novo, rodar `git diff --cached --numstat --diff-filter=A` + checar tamanho via `git cat-file -s ":arquivo"`; qualquer mídia >1MB que não seja referenciada em HTML vai pro `.gitignore`. Deploy real via `npx vercel --prod --yes` (projeto `sano-brasil`), ver [[reference_deploy_sano_brasil]].
