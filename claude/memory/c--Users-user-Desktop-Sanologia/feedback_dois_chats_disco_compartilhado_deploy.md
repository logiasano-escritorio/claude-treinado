---
name: feedback_dois_chats_disco_compartilhado_deploy
description: Dois chats na mesma pasta = deploy Vercel publica o disco inteiro (não um diff); cuidado com timing
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 829a6fdb-bacc-4b83-a6f6-88ba66d09ee6
---

O user roda **vários chats Claude Code na mesma pasta** `Desktop/Sanologia` ao mesmo tempo (ex: um mexendo em advertoriais, outro na `prime/index.html`). O disco é **compartilhado**.

**Why:** `vercel --prod` empacota o **estado atual do disco**, não um diff git. Então:
- Um deploy de qualquer chat publica o trabalho de TODOS os chats que já salvaram no disco.
- **Risco de timing:** se o chat A começa `vercel --prod` enquanto o chat B ainda está no meio das edições, o deploy captura só as edições que B já salvou naquele instante — as posteriores ficam de fora e precisam de OUTRO deploy. (Aconteceu 2026-07-14: só `gaba-dor` subiu com UTM; os outros 38 ficaram pra trás.)

**How to apply:**
- NUNCA deployar sozinho sem avisar — o deploy pode publicar trabalho não-finalizado de outro chat. Perguntar/confirmar antes.
- Commitar só a própria parte (`git add` explícito dos próprios arquivos), deixar o resto intocado.
- Antes de deployar, checar `git status` pra ver o que os outros chats mexeram.
- DEPOIS do deploy, **validar na live com curl** que a mudança realmente subiu (URL sem `.html`) — não confiar que "o outro deploy já pegou".
- Projeto Vercel = `sano-brasil`, comando `vercel --prod --yes` (~6min).

Ver [[reference_deploy_sano_brasil]], [[feedback_trocar_inclui_deploy]].
