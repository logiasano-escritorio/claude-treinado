---
name: repo-sano-onde-trabalhar
description: "Qual repo, qual conta Vercel e qual projeto servem sanologiabr.com / sanobrasil.com"
metadata: 
  node_type: memory
  type: project
  originSessionId: 41fec450-a421-400d-a612-c828ac1ee256
  modified: 2026-08-28T21:43:29.962Z
---

O site Sano é servido por **um único** projeto Vercel, que atende os dois domínios
(`sanologiabr.com` e `sanobrasil.com`):

- **Repo/pasta:** `c:\Users\user\Desktop\Reoi GitHub - Sano\repo-git-mac-windows-sano`
- **GitHub:** `github.com/logiasano-escritorio/repo-git-mac-windows-sano` (branch `main`)
- **Vercel:** conta `logiasano-escritorio`, time **SANOLOGIA - MAC E WINDOWS**,
  projeto `repo-git-mac-windows-sano` (`prj_3Y37SpLuV95BwMb2pmlJ0FVtVb0V`)

**Armadilhas que já custaram horas (2026-08-28):**

1. Existe `C:\Users\user\Desktop\Sanologia` (15 GB) com uma cópia do mesmo site.
   NÃO é o ativo. Não trabalhar lá, não migrar conteúdo dela pro repo bom —
   o usuário quer o repo novo limpo.
2. Existe uma conta Vercel antiga `relivia-ww` / `relivia-wws-projects` com um
   projeto de **nome idêntico** `repo-git-mac-windows-sano`. Não usar para nada.
   Deployar nela não afeta os domínios e parece funcionar.
3. Projeto novo nasce com **SSO/Deployment Protection ligado** → tudo responde
   302 pro login da Vercel. Desligar com
   `vercel project protection disable --sso`.

**Why:** o usuário quer tudo no GitHub para poder trabalhar de qualquer
computador sem depender de arquivo local.

**How to apply:** antes de qualquer deploy, confirmar `vercel whoami`
(= logiasano-escritorio) e o `.vercel/project.json`. Ver [[deploy-sano-fluxo]].

**Pendência conhecida:** o repo tem 1,9 GB, sendo 864 MB em 725 PNGs que
converteriam para ~40 MB em WebP (96% de redução, medida em arquivos reais).
Isso é o que faz cada build demorar. O usuário adiou a conversão; vale
reofertar quando a lentidão incomodar.
