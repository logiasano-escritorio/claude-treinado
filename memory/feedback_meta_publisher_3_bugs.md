---
name: 3 bugs comuns do publisher Meta Ads API
description: Bugs encontrados ao subir campanha Magnesio Bisglicinato (act_2378679385930611) — corrigir SEMPRE antes de rodar publisher novo
type: feedback
originSessionId: 3ab9d48b-9df8-4f63-9b5f-e2a1b74de5f0
---
Ao escrever publisher Python pra Meta Marketing API (Graph v23.0), evitar 3 bugs que perderam ~30min:

**1. `degrees_of_freedom_spec` com `standard_enhancements` foi DESCONTINUADO (2026).**
- Erro: `error_subcode 3858504` / "O criativo não deve incluir aprimoramentos padrão"
- Solução: NÃO incluir `degrees_of_freedom_spec` no params do `/adcreatives`. Deixar Meta gerenciar.
- Se precisar opt-out de specific enhancements, usar `creative_features_spec` individual (não o padrão).

**2. Compliance BR obrigatório (já documentado em outra memória mas reforça aqui).**
- Erro: `error_subcode 3858634` / "O anunciante está ausente" no POST de adset
- Solução: adicionar AMBOS no params do adset:
  - `regional_regulated_categories`: `["BRAZIL_REGULATION", "VOLUNTARY_VERIFICATION"]`
  - `regional_regulation_identities`: `{"universal_beneficiary": ADV_ID, "universal_payer": ADV_ID}`
- Advertiser ID GUILHERME OTAVIO DA SILVA: `880756411607509` (vale em múltiplas contas, incluindo act_2378679385930611 e act_2164352101016970)

**3. Idempotência de adset por nome NÃO PROTEGE de duplicação se o primeiro run falhou ANTES de criar ads.**
- Caso 2026-05-11: publisher rodou 2x. No 1º run criou 6 adsets vazios e morreu no bug do `degrees_of_freedom_spec`. No 2º run, `find_or_create_adset` não achou os vazios e criou MAIS 6 adsets. Resultado: 12 adsets, 6 vazios + 6 com ads.
- Solução: o `find_or_create_adset` precisa olhar pela API E retornar o existente mesmo que tenha 0 ads.

**Bonus 4: Cache de imagem por NOME colide quando arquivos diferentes têm mesmo nome.**
- Os 40 criativos manchete texto-01/02/03/04 tinham todos `criativo-01-A.png`, `criativo-02-A.png`, etc.
- Solução: passar `unique_name` no upload (`{folder}_{filename}`) pra cache não colidir.

**Bonus 5: Rate limit (código 17) aparece após ~60-100 chamadas seguidas.**
- Erro: `error_subcode 2446079` / "A conta de anúncios tem uma quantidade excessiva de chamadas de API"
- Solução: retry com backoff exponencial (60s, 120s, 180s). Rate limit é POR conta de anúncios, não global.

**Template de publisher seguro está em:**
`Sanologia/_dev/publisher/publish_magnesio_relivia.py` (com todas as correções aplicadas)
`Sanologia/_dev/publisher/cleanup_duplicates.py` (limpa adsets vazios duplicados)
