---
name: "Trocar link/imagem/texto" = mudar + commit + push em sequência
description: Quando o user pede "troca X por Y" em página live, sempre fazer todo o ciclo (edit + commit + push), não parar só na edição
type: feedback
originSessionId: 9bd6982e-c870-4b26-bb8d-a96c2fc679cf
---
Quando o user pede pra **trocar** qualquer coisa em página/arquivo que está em produção, o esperado é o **ciclo completo**:

1. Edit no arquivo
2. `git add` + `git commit` com mensagem descritiva
3. `git push`
4. (Opcional) confirmar que o deploy refletiu no ar

**Why:** já aconteceu de eu só editar local sem commitar (em `oregano.html` pack 1, dia 2026-05-10), o user descobriu depois que o ar não atualizou porque eu nunca tinha feito push, e ele teve que cobrar de novo. Outra vez ele pediu "troca os checkout do pediluvio" e eu só editei, esperando confirmação pra push — ele bateu boca porque "trocar = subir, óbvio".

**How to apply:**
- "Troca X por Y" / "Muda esse link" / "Atualiza esse texto" / "Substitui essa imagem" → assume push automático no fim
- Só NÃO subir se o user explicitar: "edita mas não dá push ainda" / "só pra eu ver primeiro"
- Após push, é bom validar live com curl pra confirmar que Vercel deployou
- Aplica também a Relívia (`relivia-pages`) e Sano (`Sanologia`) — ambos têm auto-deploy Vercel

**Casos onde PARAR antes do push (raros):**
- Mudanças em massa (>10 arquivos) onde vale revisar antes
- Mudanças destrutivas (deletar imagens originais, etc)
- User pediu explicitamente preview
