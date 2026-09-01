---
name: reference_remover_site_extensions_meta_api
description: "Como remover \"Complementos para navegador\" (Ligar agora / site_extensions) de anúncios Meta em massa via API"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7c722b03-0e07-4b10-9a06-8394a9f4326c
---

O "Ligar agora" / "Complementos para navegador" que aparece automático nos ads do Meta é o enhancement **`site_extensions`** dentro de `creative.degrees_of_freedom_spec.creative_features_spec`.

**Como detectar quais ads têm:** varrer os ads e procurar `site_extensions.enroll_status == OPT_IN` OU o telefone `tel:+55...` embutido no creative (o flag nem sempre lê OPT_IN, mas o telefone persiste — procurar por `997629022`/`tel:` na estrutura pega mais casos).

**Creative no Meta é IMUTÁVEL** — não dá pra editar o dof direto (dá "anúncio incompleto"). O jeito certo:
1. Ler `object_story_spec` + `degrees_of_freedom_spec` + `url_tags` do creative atual
2. Setar `creative_features_spec.site_extensions = {"enroll_status":"OPT_OUT"}`
3. **REMOVER** `standard_enhancements` do features_spec (descontinuado pelo Meta, subcode 3858504 — só os `flex_*` tinham) — senão `POST /adcreatives` falha
4. `POST /act_XXX/adcreatives` cria creative novo idêntico
5. `POST /{ad}` com `creative:{creative_id:novo}` troca no MESMO ad (mesmo id/adset, continua ACTIVE)
6. Reforçar `status:ACTIVE` por garantia; ad entra em IN_PROCESS (revisão) e volta sozinho

**Efeito colateral:** trocar creative ZERA social proof (curtidas/comentários) e re-revisa. Por isso: ads de alta conversão (>=5 compras 30d) → desligar NA MÃO no gerenciador (preserva proof); ads com pouca/zero conversão → via API. Classificar por `/insights?date_preset=last_30d` action_type purchase.

**⚠️ NUNCA rodar o script enquanto o Guilherme edita a conta no gerenciador** — escrita simultânea dá "unknown error (empty response) #1.1357045" e ele não consegue salvar. TaskStop na hora se ele avisar.

Script + manifesto (old_creative p/ rollback): [[feedback_manifesto_antes_de_subir]] em `Sanologia/_dev/remover-ligar-agora.py` + `manifesto-remocao-ligar-agora.jsonl`. Caso: 158 ads das 2 campanhas ativas de act_2164352101016970 (jun/2026), 145 via API + 12 na mão. Conta EUA 11 [[reference_meta_ads_sano]].
