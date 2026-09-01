---
name: UTM padrão Meta Ads (Sano + Relívia)
description: Template oficial de URL Tags pro Meta Ads — usar em todo anúncio (manual ou automação de upload)
type: reference
originSessionId: 9bd6982e-c870-4b26-bb8d-a96c2fc679cf
---
**Template oficial v2 (atualizado 2026-05-10) — usar em TODO anúncio Meta Ads:**

```
utm_source=FB&utm_medium=paid&utm_campaign={{campaign.name}}&utm_term={{adset.name}}&utm_content={{ad.name}}&utm_id={{campaign.id}}&placement={{placement}}&source_name={{site_source_name}}
```

**Onde colocar:** no campo **"Parâmetros de URL"** (URL Tags) do Meta Ads Manager — NUNCA concatenado na URL final.

**O que cada parâmetro faz:**
- `utm_source=FB` (maiúsculo, padrão do projeto)
- `utm_medium=paid`
- `utm_campaign` = nome da campanha (ex: "BR-StrongBones-Artrose-Ang01")
- `utm_term` = nome do conjunto de anúncios (adset)
- `utm_content` = nome do anúncio
- `utm_id` = ID da campanha (imutável — segura tracking se renomear)
- `placement` = onde foi exibido (feed, stories, reels, marketplace…)
- `source_name` = origem (fb, ig, an, msg)

**Por que `{{}}`:** sintaxe oficial Meta. Substituídos automaticamente em runtime. Não precisa hardcode por ad.

**Decode automático no backend SanoTracking:**
Backend já decodifica `+` e `%20` automaticamente — pode usar nomes de campanha/adset/ad com espaços, acentos, símbolos. Aparece bonito no dashboard.

**Como aplicar:**
- Manual: Ads Manager → editar anúncio → "Parâmetros de URL" → cola o template
- Automação (upload via API ou bulk CSV): coluna `URL Tags` recebe a string completa com `{{}}` sem encode
- CSV bulk import: utf-8-sig (BOM)

**Compatibilidade:**
- ✅ SanoTracking dashboard (sanotracking-production.up.railway.app/dash)
- ✅ Utmify
- ✅ Google Analytics 4
- ✅ Pixel Meta nativo

**NÃO fazer:**
- Hardcode UTM por ad direto na URL → perde rastreamento dinâmico
- Concatenar UTM no Link → Meta duplica
- `utm_source=fb` lowercase → padrão é `FB`
- Renomear nomes de campanha durante run → quebra agregação histórica (use o `utm_id` como chave estável)
