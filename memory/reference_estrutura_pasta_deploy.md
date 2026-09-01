---
name: Estrutura da pasta Sanologia (deploy vs dev vs lixo)
description: Sanologia/ é o repo Vercel — só fica nela o que VAI pro deploy. Tudo mais vai pra _dev/, _docs/ ou _lixo/ (todas .gitignore'd).
type: reference
originSessionId: 8471fe98-4ae3-4fdb-8c7d-6978228c3857
---
**Pasta de deploy (limpa, vai pra Vercel):**
`c:/Users/user/Desktop/Sanologia/`

**Só pode ficar na raiz / subpastas tracked:**
- `*.html` (advertoriais e páginas de produto)
- `vercel.json`, `.gitignore`, `style.css`
- `b12/`, `glowup/`, `strongbones/` — subpastas com HTMLs e imagens das páginas
- `images/` — assets compartilhados
- `videos/<produto>/*.mp4` — vídeos referenciados pelos advertoriais (4 advs usam)

**Pastas locais (NÃO vão pro Git, .gitignore'd):**

| Pasta | Conteúdo |
|---|---|
| `_dev/scripts/` | Scripts JS de geração (gerar-imagens-*.js, analisar-copy.js) |
| `_dev/prompts/` | Prompts Gemini JSON (b12.json, strongbones.json, etc) |
| `_dev/videos/` | MP3 de voz, .py de geração de vídeo, roteiros, README |
| `_dev/designs-brutos/` | Pasta "Designs e Imagens dos Produtos" — 53MB de assets fonte |
| `_docs/` | ADVERTORIAL_DESIGN_GUIDE.md, PRODUCT_PAGE_DESIGN_GUIDE.md, README.md |
| `_lixo/screenshots-debug/` | b12-mobile-*.png — screenshots de debug |
| `_lixo/placeholders-menopausa/` | placeholder-MENOPAUSA-*.png — não substituídos por imagens reais |
| `_lixo/relivia-oregano-IT/` | ad_split01*, ads_list.json, lp_mariana_it.html (não Sano) |
| `_lixo/versoes-antigas/` | adv-*-V2.html — versões anteriores |

**Regras pra próximos chats:**

1. **NUNCA criar `gerar-*.js` ou `*.py` na raiz** — sempre em `_dev/scripts/` ou `_dev/`
2. **NUNCA commitar prompts JSON de geração de imagem** — vão em `_dev/prompts/`
3. **Docs internos (DESIGN_GUIDE, README de processo)** vão em `_docs/`
4. **Placeholders e screenshots de debug** vão em `_lixo/` (até confirmar deleção)
5. **Versões antigas (V2, _backup)** vão em `_lixo/versoes-antigas/`
6. **Quando duvidar:** "isso vai aparecer em sanobrasil.com?" → se não, vai pra `_dev/` ou `_lixo/`

**Quando rodar `/sano-novo-funil` ou similar:**
- HTMLs gerados → raiz (deploy)
- Imagens da página → `<produto>/images/generated/<slug>/` (deploy)
- Prompts JSON → `_dev/prompts/` (NÃO deploy)
- Scripts auxiliares → `_dev/scripts/` (NÃO deploy)

**Antes de commitar, sempre rodar:**
```bash
cd "c:/Users/user/Desktop/Sanologia"
git status --short | grep -E "^(\?\?|A) (_dev|_docs|_lixo)/"
# se aparecer algo, NÃO commitar — ajustar .gitignore
```

**Commit cirúrgico ideal:** apenas os HTMLs novos + imagens de página geradas. Nada de scripts, prompts ou docs internos.
