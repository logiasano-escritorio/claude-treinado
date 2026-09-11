# Auto-routing de Agentes

Consulte `~/.claude/AGENTS_CATALOG.md` para mapear tópico → agente/command correto.

**Regras de auto-routing — chame o agente SEM o usuário pedir:**
- Código Python, FastAPI, Django → use `fastapi-developer` ou `python-pro`
- Next.js, React, frontend → use `nextjs-developer` ou `react-specialist`
- Bug, erro, traceback → use `debugger`
- Code review explícito → use `code-reviewer`
- Deploy, CI/CD, Docker → use `devops-engineer`
- Auditoria de segurança → use `security-auditor`
- Testes → use `qa-expert`
- Banco de dados, SQL → use `sql-pro` ou `postgres-pro`
- Performance → use `performance-engineer`
- Copy, anúncio, advertorial Relívia → use agentes do pipeline (01 a 10)
- Subir/clonar/corrigir anúncio no Meta via API → use a skill `subir-campanha-meta`
- Decisão estratégica → use `advisory-board:tasks:convene-board`
- Para escolher o agente certo em qualquer outro caso → leia AGENTS_CATALOG.md

Ao usar um agente especialista via Agent tool, informe o usuário qual agente foi chamado e por quê (1 linha).

# graphify
- **graphify** (`~/.claude/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, invoke the Skill tool with `skill: "graphify"` before doing anything else.

# copy-anuncio
- **copy-anuncio** (`~/.claude/skills/copy-anuncio/SKILL.md`) - gera copy long-form para Facebook Ads + advertorial alinhado. Trigger: `/copy-anuncio`
When the user types `/copy-anuncio`, invoke the Skill tool with `skill: "copy-anuncio"` before doing anything else.

# gerar-avatares-ugc
- **gerar-avatares-ugc** (`~/.claude/skills/gerar-avatares-ugc/SKILL.md`) - gera 15 avatares UGC iPhone 7 (1080x1920) com pessoas brasileiras segurando qualquer produto. Recebe foto do produto como referência única. Trigger: `/gerar-avatares-ugc`
When the user types `/gerar-avatares-ugc`, invoke the Skill tool with `skill: "gerar-avatares-ugc"` before doing anything else.

# criativos-manchete
- **criativos-manchete** (`~/.claude/skills/criativos-manchete/SKILL.md`) - gera N criativos FB Ads 1080x1080 no estilo "manchete jornalística médica" (estilo AlinhaFácil campeão). Recebe produto + problema + ângulo, gera via Gemini 3.1 Flash Image Preview com texto PT-BR perfeito. 4 templates: A (Revelação), B (Investigação), C (Urgente/Sintoma), D (Pós-cirurgia). Trigger: `/criativos-manchete`
When the user types `/criativos-manchete`, invoke the Skill tool with `skill: "criativos-manchete"` before doing anything else.

# pipeline-nicho
- **pipeline-nicho** (`~/.claude/skills/pipeline-nicho/SKILL.md`) - pipeline completo de 1 nicho ponta a ponta: raspa a Meta Ad Library dos concorrentes campeões → extrai long-forms + imagens → adapta todos pro produto Sano → gera imagens no padrão campeão → monta advertoriais → sobe campanha no Meta. Ex: `/pipeline-nicho melasma`, `/pipeline-nicho neuropatia`. Trigger: `/pipeline-nicho`
When the user types `/pipeline-nicho`, invoke the Skill tool with `skill: "pipeline-nicho"` before doing anything else.

# subir-campanha-meta
- **subir-campanha-meta** (`~/.claude/skills/subir-campanha-meta/SKILL.md`) - sobe campanhas no Meta pela Marketing API v23.0, estrutura 1-1-1 ou CBO com bid cap. Publisher dirigido por manifesto, idempotente por nome de campanha, com upload de vídeo/imagem e o catálogo de erros da API com o fix validado. Trigger: `/subir-campanha-meta`
When the user types `/subir-campanha-meta`, invoke the Skill tool with `skill: "subir-campanha-meta"` before doing anything else.
**Antes de escrever qualquer código que chame a Graph API do Meta — subir, clonar, corrigir ou auditar anúncio — leia `~/.claude/skills/subir-campanha-meta/REFERENCIA-API-META.md`.** Metade dos erros dessa API tem mensagem enganosa; adivinhar campo já custou horas.

# adaptar-longform
- **adaptar-longform** (`~/.claude/skills/adaptar-longform/SKILL.md`) - pipeline completo de adaptação de long-form de concorrente estrangeiro: seleciona peça do benchmarking raspado da Meta Ad Library, adapta a copy (esqueleto do original + mecanismo Sano + 42 regras + português orgânico), salva como AD-NN no Obsidian com auditoria, gera imagens stop-scroll calibradas pelo avatar, varia ângulos e monta o inventário com ranking. Trigger: `/adaptar-longform`
When the user types `/adaptar-longform`, invoke the Skill tool with `skill: "adaptar-longform"` before doing anything else.
