---
name: Pasta mestre SANO (junctions Windows)
description: Desktop/SANO/ é uma pasta-mãe com 4 atalhos (junctions) apontando pras pastas reais do projeto. Use os atalhos pra navegar, paths reais pra escrever no código.
type: reference
originSessionId: 8471fe98-4ae3-4fdb-8c7d-6978228c3857
---
**Pasta mãe:** `C:\Users\user\Desktop\SANO\`

**4 atalhos (Windows junctions) dentro:**

| Atalho | Pasta real | Conteúdo |
|---|---|---|
| `SANO/1-codigo/` | `Desktop/Sanologia/` | HTMLs adv + página, repo Git → Vercel |
| `SANO/2-vault/` | `Desktop/SANOLOGIA OBSIDIAN/` | Vault Obsidian (dashboards, planilhas) |
| `SANO/3-criativos/` | `Desktop/_Projetos/relivia-editor/outputs_sano/` | PNGs, hooks.json, ads.json |
| `SANO/4-catalogo/` | `C:/projetos/relivia/sano-energy-b12/` | Catálogo dos 39 ângulos |

**Como aplicar:**
- **Em conversas com o usuário** sobre "onde fica X": pode mencionar `SANO/1-codigo/` por simplicidade
- **No código (comandos `/sano-*`, scripts Python, paths em arquivos)**: SEMPRE usar paths REAIS (Desktop/Sanologia/, etc) — nunca os atalhos. Atalhos só servem pra navegação humana
- **Se um atalho quebrar:** recriar com `cmd /c mklink /J <atalho> <real>` (instruções no `SANO/README.md`)

**Por que junctions e não mover de verdade:** Mover Sanologia/ quebra deploy Vercel. Mover outputs_sano/ quebra scripts Python. Mover sano-energy-b12/ quebra paths nos comandos. Junctions = visualização unificada sem risco.
