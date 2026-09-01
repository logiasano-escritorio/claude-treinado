---
name: Relatório Funil — URLs só com anúncios reais
description: Sumário de URLs do relatório deve mostrar apenas URLs que têm anúncios no top_ads
type: feedback
originSessionId: 944abb03-550d-41fa-9071-25afb02a7392
---
Nunca mostrar no sumário de URLs do relatório do Agente 1 uma URL que não tem nenhum anúncio vinculado no top_ads.

**Why:** O `destination_urls_typed` pode conter URLs com muitas aparições brutas mas que ficaram fora do top_ads por baixo score. Mostrar essas URLs no sumário confunde — parece que a marca está rodando pra aquela URL quando na prática nenhum anúncio campeão aponta pra ela.

**How to apply:** No `relatorio.py`, sempre filtrar `dest_typed` para só incluir URLs presentes em `grupos` (agrupamento por `dest_url` dos top_ads) antes de renderizar o sumário e os grupos de anúncios. Variável `dest_typed_filtrado` já implementa isso.
