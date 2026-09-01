---
name: utm-padrao-meta-ads
description: "UTM obrigatoria em TODO anuncio subido no Meta - usar esta string exata, nunca inventar utm propria"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bdcb4f90-2361-4f86-a807-13afe17a1caf
  modified: 2026-09-01T10:25:29.841Z
---

**Todo anúncio criado no Meta leva esta string no campo `url_tags`** (o campo
"Parâmetros de URL" no Gerenciador). É esta, literal, sem alterar nada:

```
utm_source=facebook&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}&utm_term={{placement}}
```

Na Graph API é o campo `url_tags` do **adcreative** (não do ad, não do adset).

**Why:** as macros `{{...}}` são preenchidas pela própria Meta em tempo de
entrega, então o relatório sai com nome **e** id de campanha, conjunto, anúncio
e posicionamento. Isso é o que permite cruzar venda com criativo específico no
Metrito. Uma `utm_content` inventada (ex.: `utm_content=adv-magnesio-fibro`)
quebra esse cruzamento — todos os anúncios do conjunto viram a mesma linha no
relatório e não dá pra saber qual criativo vendeu.

**How to apply:** ao montar `object_story_spec` para um adcreative, incluir
sempre `"url_tags": "<a string acima>"`. Não inventar utm própria, não usar a
utm do advertorial, não "melhorar" o padrão. Se um anúncio subir sem isso,
corrigir antes de ativar.

Em 2026-09-01 subi AD-26, AD-27 e AD-29 (116 anúncios) sem esse campo — o
usuário teve que apontar. Ver [[meta-ads-conta-e-campanha-sano]].
