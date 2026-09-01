---
name: conta-meta-ads-sano-eua-11-atualizada-2026-05-15
description: "Setup canônico Meta Ads Sano — conta EUA 11, pixel por produto, Page/IG corretos, compliance BR universal_payer, campos legados atualizados"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7cf5b162-4724-4387-bb65-0e66432b942b
---

# Meta Ads Sano — Setup correto (validado em campanha Sano Kids 2026-05-15)

## Conta + Business
- **Account ID:** `act_2164352101016970` (EUA 11, USD, account_status=1)
- **Business:** `740698362454699` (panda.43365909)
- **Token Meta:** em `Obsidian Supremo/Otimizacao de escala/agente-funil/agente_funil.py.bak` (linha `META_ACCESS_TOKEN`)

## Page + Instagram (CRÍTICO — usar essa Page pra ads, NÃO a Sanologia)
- **Page ID pra ADS:** `759591800579421` (Sano que efetivamente roda ads — verificada via creative do StrongBones ACTIVE)
  - ⚠️ NÃO usar `650163921506803` (Sanologia institucional — IG `17841468816354122` rejeita)
- **Instagram User ID:** `17841477315620430`
  - Campo correto agora: `instagram_user_id` (legado `instagram_actor_id` foi descontinuado)

## Pixel POR PRODUTO
- Cálcio (StrongBones) = `1480375430251129`
- B12 = `980607068056359`
- GlowUp = `1350310353585886`
- **Sano Kids = `955425957482281`** (novo, criado 2026-05-15)
- Magnésio = pendente

## Compliance BR (formato CORRETO — atualizado)
```json
"regional_regulated_categories": ["BRAZIL_REGULATION", "VOLUNTARY_VERIFICATION"],
"regional_regulation_identities": {
    "universal_beneficiary": "880756411607509",
    "universal_payer": "880756411607509"
}
```

⚠️ **Mudanças vs memória antiga:**
- Chave correta é `universal_payer` (NÃO `payer` — Meta atualizou)
- Advertiser ID: `880756411607509` (GUILHERME OTAVIO DA SILVA)

## Posicionamentos válidos (campos atualizados)
- `facebook_positions`: `feed`, `story`, `instream_video`, `marketplace` (⚠️ `video_feeds` DESCONTINUADO)
- `instagram_positions`: `stream`, `story`, `reels`

## Estrutura Campaign CBO padrão
- `objective`: `OUTCOME_SALES`
- `buying_type`: `AUCTION`
- `special_ad_categories`: `[]`
- `daily_budget`: `30000` (centavos = US$300/dia)
- `bid_strategy`: **`LOWEST_COST_WITH_BID_CAP`** ⚠️ Sano padrão é COM bid cap (US$15) — eu errei na 1ª Sano Kids e Guilherme corrigiu manualmente
- `bid_amount`: `1500` (centavos = US$15 — Bid Cap padrão Sano)
- `status`: `PAUSED` (sempre — usuário revisa manualmente)

⚠️ ERRO RECORRENTE A EVITAR: criar campanha Sano sem bid cap (`LOWEST_COST_WITHOUT_CAP`)
significa CPA descontrolado. Sano sempre roda Bid Cap US$15.

## Estrutura AdSet
- `optimization_goal`: `OFFSITE_CONVERSIONS`
- `billing_event`: `IMPRESSIONS`
- `promoted_object`: `{pixel_id, custom_event_type: "PURCHASE"}`
- Audiência Sano Kids (mãe): BR mulheres 28-65 broad
- Audiência Sano padrão (50+): BR 45-65 broad

## Criação de Ad Video — passos OBRIGATÓRIOS
1. Upload do vídeo via `/{act}/advideos` → retorna `video_id`
2. Aguardar `status.video_status == "ready"` (até 3min)
3. **Extrair thumbnail** (1º frame via ffmpeg t=00:00:01)
4. Upload da thumb via `/{act}/adimages` → retorna `image_hash`
5. Criar AdCreative com `object_story_spec.video_data` contendo `video_id` + `image_hash`
6. Criar Ad linkando `creative_id` ao `adset_id`

⚠️ Sem `image_hash` o Meta rejeita com erro `1443226` ("anúncio precisa de miniatura")

## Caso concreto: Sano Kids Campanha 1-1-11 (2026-05-15)
- Campaign: `120244224034330442`
- AdSet: `120244224367740442`
- 11 Ads criados PAUSED (range `120244224654660442` a `120244224707270442`)
- Vídeos uploaded em `c:/Users/user/Desktop/Sanologia/sano-kids criativos/`
- Log: `sano-kids/_dev/campanha-resultado.json`

## Scripts úteis (em Sanologia/sano-kids/_dev/)
- `subir-campanha.py` — pipeline completo do zero (upload vídeos + criação)
- `subir-adset-ads.py` — só adset + ads (vídeos já uploaded)
- `extrair-thumbs-e-criar-ads.py` — extrai thumb com ffmpeg + cria 11 ads
