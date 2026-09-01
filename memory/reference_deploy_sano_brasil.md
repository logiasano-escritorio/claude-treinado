---
name: deploy-real-do-sanobrasil-com
description: "sanobrasil.com aponta pro projeto Vercel sano-brasil; auto-deploy GitHub→Vercel NÃO dispara, sempre `vercel --prod --yes`"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 89737784-d165-4547-b505-64597b316922
---

**Único projeto Vercel ativo do Sano:** `sano-brasil` (time `relivia-wws-projects`), aliased em **sanobrasil.com + www.sanobrasil.com**. Linkado ao repo `relivia-ww/sanologia`, branch main.

**Limpeza 2026-05-19:** apagados `sanobrasil-prod` e `sano-v2` que estavam buildando o mesmo repo em paralelo (heranças sem domínio público). Não recriar.

**Sintoma do problema antigo:** depois de `git push origin main`, sanobrasil.com continuava servindo HTML antigo por horas — webhook GitHub→Vercel do projeto sano-brasil não dispara automaticamente.

**Fix obrigatório a cada push que precisa ir ao ar:**

```bash
# Diretório Sanologia já está linkado a sano-brasil (.vercel/project.json)
vercel --prod --yes
```

CLI sobe arquivos locais, builda em `sano-brasil`, alias `sanobrasil.com` atualiza em ~15s-2min. `Last-Modified` no header HTTP confirma o deploy novo.

**Verificação rápida no ar (bash):**
```bash
curl -s "https://sanobrasil.com/PATH?bust=$(date +%s%N)" | grep -E "MARCADOR_NOVO"
```

**Histórico:**
- 2026-05-11 — descoberto durante GlowUp 4 tiers (commit 3e761fa não subiu sozinho)
- 2026-05-19 — recorreu com pixel `1289947162723962` em /prime-pv; limpeza dos 2 projetos duplicados
- 2026-07-06 — recorreu de novo: 2 commits (remoção bloco .prod + carrossel/troca imagem tônico-fem) fizeram `git push` OK mas `vercel ls --prod` mostrava último deploy de 49min; live servia HTML antigo. `vercel --prod --yes` resolveu. **Padrão confirmado: SEMPRE rodar `vercel --prod --yes` após push, não confiar no git push sozinho.**
