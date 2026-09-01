---
name: meta-ads-api-fixes-2026-05
description: Correções de API Meta Ads v21.0 descobertas na campanha Sano Kids Crescimento (2026-05-19) — campos descontinuados e estrutura CBO+BidCap correta
metadata: 
  node_type: memory
  type: reference
  originSessionId: e8cd72f1-d4e6-4361-a4aa-5dde3e8e8a6c
---

# Meta Ads API v21.0 — Correções validadas em 2026-05-19

Aprendido criando campanha "Sano Kids Crescimento Cold 5 Ângulos" (`120244439807340442`).
Estende [[conta-meta-ads-sano-eua-11-atualizada-2026-05-15]].

## CBO (Advantage+ Campaign Budget)
- ❌ NÃO usar `is_adset_budget_sharing_enabled=true` JUNTO com `daily_budget` na campanha — Meta retorna erro 4834002
- ✅ Pra CBO, basta `daily_budget` na campanha (não passa `is_adset_budget_sharing_enabled` em lugar nenhum)
- ✅ `bid_strategy=LOWEST_COST_WITH_BID_CAP` fica na **campanha**, mas `bid_amount` fica nos **adsets**

## Bid Cap
- ❌ Campo `bid_cap` na campanha NÃO existe (Meta ignora)
- ✅ Bid cap = `bid_amount` em centavos no **adset** (todos adsets da campanha com mesmo valor pra CBO+Bid Cap)
  - Ex: US$15 → `bid_amount: "1500"`

## Creative spec — campos descontinuados
- ❌ `degrees_of_freedom_spec.creative_features_spec.standard_enhancements.enroll_status` → DESCONTINUADO (erro 3858504)
- ✅ Solução: não passar `degrees_of_freedom_spec` nenhum (deixar default)

## Image Ads (link_data) — formato validado
```python
"object_story_spec": {
    "page_id": PAGE_ID,
    "instagram_user_id": IG_USER_ID,
    "link_data": {
        "link": LANDING_URL,
        "message": primary_text,       # corpo do anúncio
        "name": headline,              # title/headline
        "description": description,
        "image_hash": image_hash,
        "call_to_action": {
            "type": "LEARN_MORE",      # ou "SHOP_NOW"
            "value": {"link": LANDING_URL},
        },
    },
}
```

## Upload de imagem
- Endpoint: `POST /{act_id}/adimages` com `files={"filename": <file>}`
- Resposta: `{"images": {"<filename>": {"hash": "..."}}}` → pegar `next(iter(data.values()))["hash"]`

## Páginas e IG (CRÍTICO)
- Page Sano pra ads: `759591800579421` (Sano que efetivamente roda ads)
- IG: `17841477315620430` — campo **`instagram_user_id`** (não `instagram_actor_id` que é legado)
- ⚠️ Memória antiga apontava `650163921506803` mas essa é Sanologia institucional — IG `17841468816354122` rejeita

## Compliance BR (validado de novo)
```json
"regional_regulated_categories": ["BRAZIL_REGULATION", "VOLUNTARY_VERIFICATION"],
"regional_regulation_identities": {
    "universal_beneficiary": "880756411607509",
    "universal_payer": "880756411607509"
}
```

## Targeting limpo (anti-Dinamarca)
- NÃO incluir `locales` — idioma vazio puxa só usuários BR mesmo
- `genders: []` (não incluir o campo) = broad; `[2]` = só mulheres
- `facebook_positions`: NÃO usar `video_feeds` (descontinuado). Usar `["feed","story","instream_video","marketplace"]`

## NOVO (2026-06-01, v23.0) — Advantage Audience flag OBRIGATÓRIA
- ❌ Criar adset sem a flag → erro 100 / subcode 1870227 ("sinalização de público Advantage é obrigatória")
- ✅ Adicionar dentro de `targeting`: `"targeting_automation": {"advantage_audience": 0}` (0 = desligado, mantém broad manual; 1 = liga Advantage)

## NOVO (2026-06-01) — Token expira (code 190)
- ⚠️ Tokens hardcoded em scripts antigos (ex: `publicar_prime_joelho_meta.py`) EXPIRAM (code 190, subcode 460)
- ✅ Token válido fica em `Sanologia/.env` → `META_ACCESS_TOKEN` (user "Guilherme Collins", id 2397537800712513). SEMPRE ler do .env, nunca hardcodar.

## Caso concreto Crescimento
- Campaign `120244439807340442`
- 5 adsets, 10 image ads cada = 50 ads total
- Script: [[sano-kids-crescimento/_dev/subir-campanha-crescimento.py]]
- Log: `sano-kids-crescimento/_dev/campanha-crescimento-resultado.json`
