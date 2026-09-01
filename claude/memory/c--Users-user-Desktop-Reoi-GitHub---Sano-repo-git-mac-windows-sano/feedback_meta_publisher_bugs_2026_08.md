---
name: bugs-adicionais-do-publisher-meta-ads-ago-2026
description: Dois erros novos ao subir campanhas na act_1642921946819932 — complementa a memória dos 3 bugs do publisher
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5fa411a2-c9e5-4987-8c62-43f3e5bee369
  modified: 2026-08-29T02:44:32.725Z
---

Complementa [[feedback_meta_publisher_3_bugs]] com dois erros que apareceram em ago/2026 e não estavam documentados.

**1. `is_adset_budget_sharing_enabled` virou obrigatório no POST de campanha.**
- Erro: `error_subcode 4834011` / "É necessário especificar True ou False no campo is_adset_budget_sharing_enabled"
- Solução: incluir `"is_adset_budget_sharing_enabled": "false"` nos params de `/campaigns` quando o budget está no adset (não em CBO).

**2. Advantage+ audience não aceita `age_min` > 25.**
- Erro: `error_subcode 1870188` / "Com conjuntos de anúncios que usam o público Advantage+, o controle de idade mínima não pode ser definido como mais de 25 anos"
- Solução: com `targeting_automation.advantage_audience = 1`, usar `age_min` ≤ 25. O Meta aceita `age_max` normalmente.

**Why:** os dois quebram o publisher no meio e deixam campanhas órfãs (ver bug 3 da memória original).

**How to apply:** antes de rodar publisher novo nesta conta, conferir os 5 pontos — os 3 da memória original + estes 2.

---

**Perdi tempo por não consultar a memória primeiro.** Fiquei tentando `dsa_beneficiary`/`dsa_payor` (campos errados) e variações do nome do anunciante por 4 tentativas, quando [[feedback_meta_publisher_3_bugs]] já trazia a solução exata: `regional_regulated_categories` + `regional_regulation_identities` com o advertiser ID `880756411607509`.

**Regra:** ao encontrar erro de API do Meta, **procurar na memória antes de tentar variações**. O usuário teve que interromper e avisar que a documentação já existia.

---

## Clonagem entre contas (ago/2026)

**3. Com CBO, `is_adset_budget_sharing_enabled` tem que ser `false`.**
- Erro: `error_subcode 4834002` / "Não é possível usar o compartilhamento de orçamento do conjunto com orçamento da campanha"
- Regra: budget no adset -> `false` (obrigatório informar); budget na campanha (CBO) -> `false` também. Nunca `true` com CBO.

**4. O app não tem permissão para `POST /adimages` ou `/advideos` com URL remota.**
- Erro: `(#3) Application does not have the capability to make this API call.`
- Solução: **baixar o asset e subir como arquivo** (multipart, campo `source` para imagem e `advideos`). Funciona sem capability extra.
- Para clonar entre contas: pegar `creative{image_url}` do ad de origem (não buscar em `/adimages` da conta, que pagina e não acha) e `GET /{video_id}?fields=source` para vídeo.

**5. `nohup ... &` no Bash tool morre quando o shell encerra.**
- Sintoma: publisher para no meio, deixando campanha+adset sem ad (órfãs).
- Solução: rodar com `run_in_background: true` do próprio tool, sem `nohup &`.
