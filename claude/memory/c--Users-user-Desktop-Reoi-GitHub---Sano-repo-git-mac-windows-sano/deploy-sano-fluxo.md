---
name: deploy-sano-fluxo
description: Fluxo obrigatorio de deploy do site Sano (sanologiabr.com / sanobrasil.com) e a autoria de commit que a Vercel exige
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 41fec450-a421-400d-a612-c828ac1ee256
  modified: 2026-08-28T21:43:12.863Z
---

Deploy do site Sano é **sempre** via GitHub, nunca `vercel --prod` por CLI:

```
edita → git commit → git push origin main → Vercel builda sozinha → os 2 dominios
```

**A autoria do commit tem que ser `logiasano-escritorio <logiasano@gmail.com>`.**
Commits como `Guilherme <guilhermeotaviowork@gmail.com>` (conta GitHub
`guilhermeotaviowork-oss`) são BLOQUEADOS pela Vercel — o deploy fica com
`status: UNKNOWN`, não builda, e a página fica 404 no domínio.
Antes de commitar, conferir `git config user.email`.

**Why:** em 2026-08-28 a v2 e a v3 do magnesio-intestino ficaram horas em 404
por causa disso. O usuário perdeu muito tempo até acharmos a causa. A mensagem
da Vercel é "Deployment Blocked — guilhermeotaviowork-oss is not a member of
your team". A correção definitiva seria adicionar esse usuário ao time
SANOLOGIA - MAC E WINDOWS na Vercel; enquanto isso não acontece, a identidade
do git resolve (já configurada localmente neste repo, mas NÃO vale em outra
máquina clonada).

**How to apply:** nunca fazer deploy por CLI neste projeto. Sempre commit+push.
Se um deploy ficar `UNKNOWN` ou a página der 404 no domínio, a primeira coisa a
checar é a autoria do último commit — não é o rewrite, não é o arquivo, não é
cache. Ver também [[repo-sano-onde-trabalhar]].
