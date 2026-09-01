---
name: repo-reliviabr-shop
description: "reliviabr.shop é deployado de C:\\projetos\\relivia (repo relivia-pages), NÃO de Desktop\\Sanologia"
metadata: 
  node_type: memory
  type: reference
  originSessionId: e8cd72f1-d4e6-4361-a4aa-5dde3e8e8a6c
---

`reliviabr.shop` serve do repo **`C:\projetos\relivia\`** (remote `relivia-ww/relivia-pages`), NÃO de `Desktop\Sanologia` (remote `relivia-ww/sanologia`).

Vários funis (magnesio-gummies, prime, strongbones, etc.) existem em **ambos os repos** com conteúdo divergente — Sanologia/ parece ser o de dev/scratch, relivia-pages/ é o de produção do reliviabr.shop.

**Antes de editar pra deployar em reliviabr.shop:**
1. `curl -sL "https://reliviabr.shop/<funil>/<pagina>.html" | grep -A2 "data-price"` — pega um trecho único da live
2. Grep esse trecho em `C:\projetos\relivia` E `C:\Users\user\Desktop\Sanologia` pra confirmar qual repo bate
3. Edita o repo certo e push

Sintoma típico: edição em Sanologia/ commitada e pushada mas reliviabr.shop não muda → tá no repo errado, vai pra `C:\projetos\relivia\`.

Relacionado: [[reference_deploy_sano_brasil]] (sanobrasil.com tem armadilha parecida — projeto Vercel `sano-brasil` ≠ `sano-v2`).
