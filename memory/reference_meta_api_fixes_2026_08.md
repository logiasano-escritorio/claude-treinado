---
name: reference-meta-api-fixes-2026-08
description: Dois erros novos da Meta API v21 ao criar adset/creative no Brasil (ago/2026) e os fixes
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0cbdd453-5054-466f-8a94-ff82df8af635
  modified: 2026-08-14T14:41:21.060Z
---

Ao publicar conjuntos na conta `act_2164352101016970` (2026-08-14), dois erros que **não estavam nos scripts antigos**:

**1. `compliance_section` — adset BR não é criado sem anunciante verificado.**
Erro: `code 100, subcode 3858634`, `blame_field_specs: [["compliance_section"]]`, "O anunciante está ausente".
Fix — mandar no POST do adset:
```
regional_regulated_categories = ["BRAZIL_REGULATION","VOLUNTARY_VERIFICATION"]
regional_regulation_identities = {"universal_beneficiary": ID, "universal_payer": ID}
```
⚠️ O ID varia por campanha. Na campanha `BID CAP - Prime Creme - Vídeos` é **`1228611831325801`**, NÃO o `880756411607509` de [[reference_meta_compliance_section_solution]]. **Sempre copiar do adset que já está no ar** via `GET /{adset_id}?fields=regional_regulated_categories,regional_regulation_identities`.

**2. `standard_enhancements` foi DESCONTINUADO.**
Erro: `code 100, subcode 3858504`, "O recurso de inclusão do campo de aprimoramentos padrão no criativo foi descontinuado."
Fix: **remover o `degrees_of_freedom_spec` inteiro** do POST de `/adcreatives`. Scripts antigos que mandavam `{'creative_features_spec':{'standard_enhancements':{'enroll_status':'OPT_OUT'}}}` agora quebram.

**3. Markdown não renderiza no Facebook.** Long-forms tirados do Obsidian levam `**negrito**` literal pro feed — o leitor vê os asteriscos. Limpar com `re.sub(r'\*\*(.+?)\*\*', r'\1', body)` e remover linhas `---`, mantendo as quebras de linha.

**4. Nome de arquivo com `:` quebra o Write no Windows** (EINVAL no rename do .tmp) e deixa um arquivo órfão de 0 byte.

Ver [[project_longforms_prime_total_relief]].
