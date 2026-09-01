---
name: Email correto do git e deploy Vercel
description: Email do git no projeto Sanologia deve ser reliviabrasil@gmail.com — outro email bloqueia deploy Vercel
type: feedback
originSessionId: 9bbd0c8a-00d5-4eda-b291-249f584c7558
---
No projeto `c:\Users\user\Desktop\Sanologia`, o git deve estar configurado com:

- `user.email = reliviabrasil@gmail.com`
- `user.name = Relívia`

**Why:** A Vercel bloqueia deploys quando o autor do commit não tem acesso ao team `relivia-ww's projects`. O usuário `guilhermeotaviowork@gmail.com` (que tava configurado por engano em sessões anteriores) NÃO tem esse acesso e foi a raiz de "deploy_failed" misterioso por dias. O email correto é `reliviabrasil@gmail.com` (a conta GitHub real do usuário).

**How to apply:**
- Antes de qualquer commit no Sanologia, verificar `git config user.email` e corrigir se necessário
- Se aparecer commit antigo com email errado, fazer `git commit --amend --reset-author` e force-push com `--force-with-lease`
- Para deploy direto sem GitHub: `vercel --prod --yes` na raiz do projeto (CLI já logado como `relivia-ww`)
- Se o deploy falhar com erro vazio "deploy_failed" sem mensagem, suspeitar primeiro do autor do commit
