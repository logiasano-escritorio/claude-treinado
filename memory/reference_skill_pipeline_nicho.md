---
name: reference_skill_pipeline_nicho
description: "Skill /pipeline-nicho — pipeline completo por nicho (raspa Ad Library → adapta → imagem → advertorial → campanha Meta)"
metadata:
  node_type: memory
  type: reference
  originSessionId: 7c722b03-0e07-4b10-9a06-8394a9f4326c
---

Skill **/pipeline-nicho** (`~/.claude/skills/pipeline-nicho/SKILL.md`) automatiza o pipeline inteiro que rodamos manualmente no Clarilux/melasma. Uso: `/pipeline-nicho melasma` (ou neuropatia, queda capilar, fungo unha...).

**7 passos:** (0) matriz de termos por idioma + classifica tipo → (1) raspa domínios campeões +30d → (2) long-forms+imagens dos top domínios → (3) filtra pelo destino do produto → (4) adapta todos via agentes paralelos (nunca reduzir) → (5) gera imagens no padrão do TIPO → (6) monta advertoriais clonando design → (7) sobe campanha Meta PAUSED.

**Lógica de imagem por TIPO do nicho (chave do Guilherme):**
- **RESULTADO VISUAL** (melasma/queda capilar/fungo/acne) → padrão **ANTES/DEPOIS**.
- **DOR/SINTOMA** (neuropatia/edema/dor articular) → padrão **CENA IMPACTANTE da dor** + diagrama mecanismo.

Scripts prontos em `scripts/`: `adlib-dominios.py`, `adlib-longform.py`, `gen-imagens-template.py`, `subir-campanha-template.py` (todos testados no Clarilux). Encapsula as pegadinhas: media=all (não image) pra medir mercado; clicar "Ver mais"; img s600x600 não s60x60; webp→jpg pro Meta; site_extensions OPT_OUT; nunca reduzir long-form.

Origem: sessão que rodou o pipeline Clarilux inteiro à mão ([[project_campanha_clarilux_melasma]], [[reference_raspar_ad_library_drissionpage]], [[feedback_adaptar_longform_nunca_reduzir]]).
