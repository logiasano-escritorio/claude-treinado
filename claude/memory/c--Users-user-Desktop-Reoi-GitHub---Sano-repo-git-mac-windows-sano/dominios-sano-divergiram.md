---
name: dominios-sano-divergiram
description: "sanobrasil.com estava em outra CONTA Vercel e servia build congelada - resolvido em 31/08/2026, e como diagnosticar se repetir"
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-31T22:33:17.789Z
  originSessionId: ad6fa60e-13b6-40f6-b5e3-f66ecd275604
---

**RESOLVIDO em 2026-08-31.** Os dois domínios voltaram a servir o mesmo deploy
(hash idêntico confirmado). Fica registrado o diagnóstico porque a causa-raiz
pode voltar.

## A causa real (a hipótese anterior estava errada)

Não era build congelada nem deploy que falhou. O `sanobrasil.com` estava
**registrado noutra CONTA Vercel** — org `relivia-ww`, projeto `sano-brasil` —
enquanto o site vive na org SANOLOGIA, projeto `repo-git-mac-windows-sano`.
Duas contas distintas, não só dois projetos.

Sintoma: páginas antigas respondiam 200 nos dois domínios (existiam quando os
projetos divergiram), e tudo criado depois dava **404 só no sanobrasil.com**.

## Como diagnosticar isso em 30 segundos

O teste decisivo é comparar o **conteúdo servido**, não o header `Age`:

```bash
a=$(curl -s https://sanobrasil.com/UMA-PAGINA-ANTIGA | md5sum | cut -c1-16)
b=$(curl -s https://www.sanologiabr.com/UMA-PAGINA-ANTIGA | md5sum | cut -c1-16)
[ "$a" = "$b" ] && echo "mesmo deploy" || echo "DEPLOYS DISTINTOS"
```

Hash diferente na mesma URL = projetos/contas diferentes. `Age` e
`Last-Modified` enganam: os dois mostravam data de hoje mesmo servindo builds
distintas.

Outro sinal forte: procurar no HTML publicado algo que um commit removeu
(ex.: `GTM-PNVRC5ZR`). Se ainda aparece num domínio e não no outro, é domínio,
não commit.

## A solução que funcionou

A Vercel pedia verificação por TXT em `_vercel.sanobrasil.com` ("This domain is
linked to another Vercel account"). O usuário não conseguiu mexer no DNS e
**removeu o domínio do projeto na conta antiga** — isso liberou a propriedade, e
o projeto certo reivindicou sem precisar do TXT. Site fora do ar por poucos
minutos, depois "Configuring DNS" → propagou sozinho.

Ordem correta se repetir: **pausar campanhas que apontam pro domínio** →
remover do projeto antigo → Refresh/Add Existing no projeto certo.

## Pontas soltas

- `sanooficial.com` continua no projeto antigo `sano-brasil` (org relivia-ww),
  servindo a build de 28/08. Mesmo problema, ainda não resolvido.
- Confirmar que `sanobrasil.com` segue **registrado** na conta relivia-ww — foi
  removido do projeto, não do registro, mas vale checar a renovação.
- CLI da Vercel exige login por device code (navegador), então deploy e troca de
  domínio **não dá pra fazer por sessão não interativa** — é dashboard na mão.

Ver também [[repo-sano-onde-trabalhar]] e [[deploy-sano-fluxo]].
