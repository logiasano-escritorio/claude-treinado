---
name: feedback_pastas_case_quebram_deploy_vercel
description: Pastas CLARILUX/FUNGZERO são MAIÚSCULAS no disco — vercel.json e paths /images PRECISAM ser MAIÚSCULOS, senão 404 no Vercel
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4ec4821c-5918-4025-8e8a-3d9ccae48c1e
---

As pastas no DISCO Windows são `CLARILUX/` e `FUNGZERO/` em **MAIÚSCULO** (confirmado via PowerShell `Get-ChildItem -Directory`). É esse case maiúsculo que sobe pro Vercel. O Vercel roda Linux (case-sensitive), então rotas/imagens só funcionam se apontarem pra MAIÚSCULO. `clareia-premium`/`tonico-supremo` são minúsculas de verdade no disco → sempre funcionaram.

**🎯 CAUSA RAIZ REAL (descoberta 2026-06-27, commit c518759):** havia DOIS caminhos de deploy com cases diferentes → o case alternava ALEATORIAMENTE entre deploys:
- `vercel --prod` (CLI) sobe os arquivos **do DISCO** → disco tinha `CLARILUX`/`FUNGZERO` MAIÚSCULO.
- auto-deploy do `git push` sobe **do GIT** → git tinha `clarilux`/`fungzero` minúsculo.
Cada deploy pegava um dos dois → 404 imprevisível "que muda de lado". Fixar o vercel.json num case só NUNCA estabiliza, porque o outro caminho quebra.

**✅ SOLUÇÃO DEFINITIVA:** padronizar TUDO em minúsculo. (1) Renomear as pastas no DISCO via PowerShell 2-step: `Rename-Item FUNGZERO fungzero_tmp; Rename-Item fungzero_tmp fungzero` (idem CLARILUX). (2) vercel.json + ~140 paths `/images/` nos HTMLs em minúsculo. (3) Confirmar git já minúsculo com `git -c core.ignorecase=false ls-files | grep`. Depois disso disco=git=minúsculo, os 2 caminhos sobem o mesmo case → TODAS as rotas 200, estável, sem `--force`.

**Why o diagnóstico engana:** `core.ignorecase=true` no git do Windows faz `git ls-files`/`ls-tree`/`cat-file tree` mostrarem MINÚSCULO (mentira). Não confie neles pra decidir o case. A verdade é:
1. `powershell.exe -c "(Get-ChildItem -Directory).Name"` → mostra o case REAL do disco (= o que vai pro deploy).
2. `curl` testando os 2 cases no domínio → o que der 200 é o que o Vercel serve.

**How to apply (qualquer arquivo/rota nova em CLARILUX ou FUNGZERO):**
- Rota no vercel.json: destino sempre `/FUNGZERO/...` ou `/CLARILUX/...` MAIÚSCULO.
- Paths de imagem nos HTMLs desses funis: sempre `/FUNGZERO/images/...` MAIÚSCULO.
- Erro anterior meu (NÃO repetir): apontar pra minúsculo e ficar dando `vercel --prod --force` — o --force só mascarava por mexer no cache; o case correto é MAIÚSCULO, ponto.
- Validar PÓS-deploy (esperar o build terminar, ~6min) com `curl` em TODAS as rotas + 1 imagem antes de dizer "no ar". Build em andamento serve a versão antiga → 404 falso.
- Correção de fundo possível (não feita): renomear de vez as pastas pra minúsculo via 2-step `git mv FUNGZERO fungzero-tmp && git mv fungzero-tmp fungzero` num ambiente case-sensitive, ou padronizar todo o repo. Enquanto não fizer, MAIÚSCULO é a regra.

Relacionado: [[reference_deploy_sano_brasil]] (sanobrasil.com = projeto Vercel `sano-brasil`, precisa `vercel --prod`).
