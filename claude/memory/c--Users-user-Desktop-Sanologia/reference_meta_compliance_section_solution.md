---
name: SOLUÇÃO — compliance_section Meta Ads API (anti-Dinamarca-bug-2)
description: Como criar adset via Meta Marketing API com o anunciante verificado declarado (resolve erro 400 compliance_section)
type: reference
originSessionId: 9bd6982e-c870-4b26-bb8d-a96c2fc679cf
---
# 🎯 SOLUÇÃO DEFINITIVA — Subir Adset via API com Compliance BR

## O bug

Ao criar adset via Marketing API targeting Brasil:

```json
{
  "error": {
    "error_user_title": "O anunciante está ausente",
    "blame_field_specs": [["compliance_section"]],
    "error_subcode": 3858634
  }
}
```

## A solução

**Payload do adset precisa incluir 2 campos extras:**

```python
adset_payload = {
    "name": "...",
    "campaign_id": "...",
    # ... resto dos campos normais ...

    # 👇 ESSAS 2 LINHAS RESOLVEM O ERRO
    "regional_regulated_categories": ["BRAZIL_REGULATION", "VOLUNTARY_VERIFICATION"],
    "regional_regulation_identities": {
        "universal_beneficiary": "<ADVERTISER_ID>",
        "universal_payer": "<ADVERTISER_ID>"
    }
}
```

## Como descobrir o `<ADVERTISER_ID>` de uma conta

**Cada Ad Account tem seu próprio ID de anunciante verificado.** Não dá pra reutilizar entre contas.

**Método:** ler de um adset que já está ACTIVE na mesma conta (que foi criado pela UI).

```python
# Lista adsets ACTIVE
adsets = get(f"act_{ACCOUNT_ID}/adsets", {
    "fields": "id,name,status,regional_regulation_identities",
    "limit": 50
})
# Pega o campo regional_regulation_identities.universal_beneficiary
# Isso é o ADVERTISER_ID
```

⚠️ **O campo `regional_regulation_identities` retorna no GET** mesmo que `compliance_section` não retorne. **É o nome certo do campo no schema da API.**

## IDs conhecidos (mapeamento conta → advertiser)

| Ad Account | Nome | Advertiser ID | Nome do anunciante |
|------------|------|---------------|---------------------|
| `act_2164352101016970` | EUA 11 | `880756411607509` | GUILHERME OTAVIO DA SILVA |

**Cada conta nova precisa ter seu ID descoberto via método acima.**

## Categories possíveis

- `BRAZIL_REGULATION` — regulação BR (LGPD/Anvisa-like compliance)
- `VOLUNTARY_VERIFICATION` — verificação voluntária do anunciante

Usar AS DUAS sempre em BR.

## Outros 2 gotchas que aparecem JUNTO (subida 2026-06-28, campanha SANO_PRIME_FLEXIVEL `120247274370230442`)

Ao subir adset+ads via API na conta EUA 11, depois de passar o compliance, surgem mais 2 erros em sequência:

1. **`advantage_audience: 1` exige `age_min <= 25`** (erro_subcode 1870188 "idade mínima não pode ser >25"). Solução: targeting com `age_min: 18, age_max: 65` + `age_range: [45,65]` (o range vira só sugestão; o 18 é a trava). Copiar EXATO do adset existente.
2. **Creative NÃO pode ter `degrees_of_freedom_spec`** com `standard_enhancements` (erro_subcode 3858504 "criativo não deve incluir aprimoramentos padrão"). Solução: criar o adcreative SEM esse campo — só `name` + `object_story_spec`. O default já vem opt-out.

Campo certo é `universal_payer` (NÃO `payor` — erro fácil de digitar). Bid no adset (`bid_amount`), não na campanha CBO.

## Histórico

- **2026-05-11** — Descoberto que existe o campo `regional_regulation_identities` (não `compliance_section` como dizia o erro). Solução veio de outro chat que rodou query no adset ACTIVE e pegou o ID.
- Já validado em produção: campanha "Sano StrongBones — BidCap CBO" (`120243760400480442`) rodando com `advertiser_id=880756411607509` na conta EUA 11.
- **2026-06-28** — 36 ads PAUSED subidos (4 adsets manchete Prime) na campanha SANO_PRIME_FLEXIVEL com os 3 gotchas acima resolvidos. Script `subir_prime_36.py`/`criar_ads_only.py`. Rate limit (code 17) aperta após ~50 chamadas seguidas — espaçar.
