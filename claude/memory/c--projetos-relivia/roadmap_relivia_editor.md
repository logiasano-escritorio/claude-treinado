---
name: Roadmap — Relívia Editor (Features Planejadas)
description: Lista viva de features planejadas para o Relívia Editor SaaS — consultar antes de iniciar desenvolvimento
type: project
originSessionId: b2e7c3fd-f77f-4c2b-aca7-40016948f09f
---
## Como usar

Quando o usuário chamar `/roadmap`, listar as features abaixo com status, deixar ele escolher uma e carregar o contexto completo para executar.

---

## Features

### 🟡 PLANEJADA — CMS com GitHub + Vercel integrado

**Resumo:** Transformar o Relívia Editor em um CMS visual onde o usuário edita advertoriais com drag & drop e publica com 1 clique, fazendo commit automático no GitHub e deploy na Vercel com status em tempo real.

**Stack decidida:** GrapesJS (editor visual), GitHub REST API v3, Vercel REST API, config.json local

**Histórias planejadas (em ordem de execução):**

1. **Epic 1 — Configurações** — Aba de configurações no Editor: GitHub Token, GitHub Owner, Repo, Branch, Vercel Token, Vercel Project ID. Salva em `config.json` local. Testa conexão com ambas as APIs ao salvar.

2. **Epic 2 — Listagem** — Aba "Advertoriais": rota `GET /advertorials/list` lista todos os `.html` do repo via GitHub API. Cards com nome, pasta, botão Editar. Filtro por nome.

3. **Epic 4.1 — Commit automático** — Rota `POST /advertorials/publish`: recebe HTML final, faz commit cirúrgico via GitHub API (só o arquivo editado), retorna SHA do commit.

4. **Epic 3 — Editor GrapesJS** — Carrega HTML do advertorial no GrapesJS. Drag & drop de blocos, edição inline de textos e imagens. Botão "Trocar Imagem com IA" integrado ao Gemini já existente.

5. **Epic 4.2 — Status deploy em tempo real** — Polling Vercel API a cada 3s após commit. Painel mostra: ⏳ Build iniciado → 🔨 Building → ✅ Deployed. Link direto para URL publicada.

**Arquivos afetados:**
- `C:/Users/user/Desktop/_Projetos/relivia-editor/app.py` — adicionar rotas `/advertorials/*`
- `C:/Users/user/Desktop/_Projetos/relivia-editor/index.html` — adicionar abas Advertoriais + Configurações + integrar GrapesJS
- `C:/Users/user/Desktop/_Projetos/relivia-editor/config.json` — novo arquivo (não commitar no repo)

**Contexto adicional:** Usuário é o único usuário por ora. No futuro, outros usuários conectarão seus próprios repos e tokens.

---

### 🟡 PLANEJADA — Editor Visual de Páginas com Gemini Image

**Resumo:** Transformar o editor de advertoriais em um editor visual funcional onde o usuário clica em qualquer elemento da página para editá-lo inline — textos, imagens, links e botões — com integração direta ao Gemini para gerar novas versões de imagens via prompt e substituir automaticamente no HTML, com preview em tempo real e publicação via GitHub + Vercel.

**Stack decidida:**
- `contenteditable` injetado no body do iframe (preserva layout 100%, zero biblioteca externa)
- `MutationObserver` para detectar mudanças no DOM e sincronizar com HTML raw
- Click interceptor no iframe: `<img>` → painel Gemini | `<a>` / `<button>` → tooltip de edição
- Mini-chat lateral: textarea de prompt + upload de referência + botão Gerar
- Backend Flask: nova rota `/gemini/edit-image` (Gemini API já configurada no app)
- Imagem gerada retorna como base64 → substitui `src` da `<img>` no DOM → sincroniza no HTML
- Modo código como fallback (textarea ↔ visual bidirecional)

**Histórias planejadas (em ordem de execução):**

1. **Epic 1 — Editor contenteditable** — Carregar HTML no iframe com `contenteditable` injetado no body. Toolbar flutuante aparece sobre o elemento focado com: Bold, Italic, cor, font-size. `MutationObserver` no `document` do iframe serializa o DOM para HTML raw a cada mudança (debounce 300ms). Botão "Aplicar" força sync imediato.

2. **Epic 2 — Clique em imagem** — Click interceptor no iframe detecta clique em `<img>` e cancela o comportamento padrão. Abre painel lateral direito "Editar Imagem" com três opções: (a) campo URL para substituição direta, (b) input de upload local (FileReader → data URI), (c) botão "Gerar com Gemini" que expande o mini-chat. A imagem selecionada fica com outline azul de seleção.

3. **Epic 3 — Clique em link/botão** — Click interceptor detecta clique em `<a>` e `<button>`. Abre tooltip/popover inline (posicionado sobre o elemento) com: campo texto do elemento, campo href (só para `<a>`). Botão "Salvar" atualiza o DOM diretamente. Tecla Escape fecha sem salvar. Sync automático via MutationObserver.

4. **Epic 4 — Mini-chat Gemini Image** — Painel lateral com: (1) preview da imagem selecionada, (2) textarea de prompt livre ("Gera em português", "Troca pelo meu produto"), (3) upload opcional de imagem de referência, (4) botão "Gerar". Backend `/gemini/edit-image`: recebe `image_url` ou `image_base64` da img selecionada + `prompt` + `reference_image` opcional → chama `gemini-2.0-flash-preview-image-generation` → retorna nova imagem como base64. Frontend substitui `src` da `<img>` no iframe (data URI) e dispara sync do MutationObserver. Histórico de versões: botão "Reverter" restaura src original.

5. **Epic 5 — Modo código como fallback** — Botão "Ver código" no toolbar: extrai `innerHTML` do body do iframe → popula textarea. Botão "Aplicar código": faz parse do textarea → injeta no iframe via `document.write` → reinicia contenteditable e interceptors. Preserva o fluxo: visual é fonte da verdade, código é fallback para edições avançadas.

**Arquivos afetados:**
- `C:/Users/user/Desktop/_Projetos/relivia-editor/index.html` — substituir split-view atual por editor visual com painel Gemini lateral
- `C:/Users/user/Desktop/_Projetos/relivia-editor/app.py` — adicionar rota `/gemini/edit-image` (reutiliza Gemini API key já configurada)

**Contexto adicional:** A rota de publicação GitHub + deploy Vercel já está implementada — o Epic 5 apenas conecta ao fluxo existente de `advPublish()`. A Gemini API key já está no ambiente do app. Nenhuma biblioteca externa de editor (GrapesJS, Quill, etc.) — tudo nativo para preservar layout dos advertoriais.

---

### 🟡 PLANEJADA — Dashboard de Agentes de IA

**Resumo:** Aba "Agentes" no Relívia Editor com cards visuais de todos os agentes disponíveis em `.claude/agents/`. O usuário clica num card, preenche os inputs do agente (ex: "qual página?") e executa via Claude API — com output em tempo real na tela.

**Stack decidida:** Nova aba no `index.html` existente, Flask SSE ou polling para streaming do output, Claude API (Anthropic SDK já instalado no app), leitura dos arquivos `.claude/agents/*.md` para montar os cards dinamicamente.

**Histórias planejadas (em ordem de execução):**

1. **Epic 1 — Leitura dos agentes** — Rota `GET /agents/list`: lê todos os arquivos `.claude/agents/*.md`, extrai frontmatter (name, description) e retorna lista. Cards na UI com nome, descrição e botão "Executar".

2. **Epic 2 — Formulário de inputs** — Ao clicar num card, abre painel lateral com campos de input dinâmicos (ex: "URL da página", "Nome do produto"). Inputs definidos no próprio arquivo `.md` do agente.

3. **Epic 3 — Execução via Claude API** — Rota `POST /agents/run`: recebe agent_name + inputs, monta o prompt, chama Claude API com as instruções do agente + inputs do usuário. Retorna output via streaming (SSE).

4. **Epic 4 — Output em tempo real** — Painel de output na UI mostra o response do agente sendo gerado token a token. Botão "Copiar" e "Parar" ao finalizar.

**Arquivos afetados:**
- `C:/Users/user/Desktop/_Projetos/relivia-editor/app.py` — adicionar rotas `/agents/*`
- `C:/Users/user/Desktop/_Projetos/relivia-editor/index.html` — adicionar aba Agentes com cards + painel de execução
- `C:/Users/user/.claude/agents/*.md` — fonte dos agentes (já existente, começa com `veo2-video-producer.md`)

**Contexto adicional:** Agentes são definidos em `.claude/agents/` — o dashboard lê esses arquivos e monta a UI dinamicamente. Quando um novo agente for criado, aparece automaticamente no dashboard sem precisar alterar o código.

---

### 🟡 PLANEJADA — Pipeline Workflow Multi-Etapa

**Resumo:** Feature de orquestração do pipeline sequencial Relívia (01→02→03→04→05→06→07→08→09) como workflow visual com estado persistente. O usuário cola a URL da Ads Library, inicia o pipeline e acompanha cada etapa em cards com progresso em tempo real. Etapas críticas exigem aprovação manual antes de avançar.

**Contexto:** Análise feita com Orion (Claude Code Mastery Chief) em 2026-04-14. Infra de fila (jobs{}, queue, spawn_workers) já existe no app.py — precisa ser generalizada para suportar pipelines multi-etapa.

**Stack decidida:** Extensão do sistema de jobs existente (`pipeline_runs{}`), endpoints REST `/pipeline/*`, UI com cards de progresso por etapa, persistência em JSON local para sobreviver restart do servidor.

**Histórias planejadas (em ordem de execução):**

1. **Epic 1 — Modelo de dados** — Objeto `pipeline_runs{}` com estrutura: `{ run_id, created_by, etapa_atual, status, outputs{}, created_at }`. Definição estática `PIPELINE_STEPS` com lista ordenada de agentes + flag `approval_required` por etapa.

2. **Epic 2 — Endpoints REST** — `POST /pipeline/start` (recebe URL, cria run, dispara etapa 1), `GET /pipeline/{id}` (estado completo), `GET /pipeline/{id}/output/{etapa}` (arquivo de output), `POST /pipeline/{id}/approve` (avança etapa), `POST /pipeline/{id}/rerun/{etapa}` (reroda etapa específica).

3. **Epic 3 — UI com cards de progresso** — Aba "Pipeline" no index.html. Card por etapa: ícone de status (✅🔄⏳⏸), nome do agente, tempo decorrido, botão de preview do output. Polling a cada 3s para atualizar status.

4. **Epic 4 — Aprovação manual** — Etapas com `approval_required: true` (Clone, Copy, Produto, Publicador) pausam o pipeline e exibem o output para revisão. Botões: [Aprovar e continuar] [Editar antes] [Rerrodar].

5. **Epic 5 — Multi-usuário** — `created_by` por session_id. Dashboard "Meus Runs" com histórico. Fila compartilhada com `MAX_WORKERS=3` já suporta paralelismo entre usuários.

**Etapas do pipeline e aprovações:**
| # | Agente | Aprovação manual |
|---|--------|-----------------|
| 01 | agente-funil | Não |
| 02 | agente-analise | Não |
| 03 | agente-clone | **Sim** — revisar HTML clonado |
| 04 | agente-trafego | Não |
| 05 | agente-copy | **Sim** — revisar copy elevada |
| 06 | agente-traducao | Não |
| 07 | agente-revisor | Não |
| 08 | agente-produto | **Sim** — revisar CRO + prompts |
| 09 | agente-publicador | **Sim** — NUNCA auto-publicar |

**Arquivos afetados:**
- `app.py` — adicionar `pipeline_runs{}`, `PIPELINE_STEPS`, rotas `/pipeline/*`
- `index.html` — adicionar aba Pipeline com cards de progresso + painel de aprovação
- `pipeline_runs.json` — persistência de estado (novo arquivo, não commitar)

**Nota crítica:** Agente Publicador (09) deve SEMPRE criar anúncios como PAUSED no Meta. Nunca ativar automaticamente mesmo com aprovação do usuário no Editor — o usuário ativa manualmente no Facebook Ads Manager.

---

### 🔵 IDEIA — Agent Healer com Loop Fechado (Autocorreção em Tempo Real)

**Resumo:** Transformar o Agent Healer de diagnóstico passivo em autocorreção ativa. Hoje ele detecta e diagnostica erros, mas a correção ainda depende de invocação manual. A ideia é fechar o loop: erro ocorre → healer detecta → aplica fix automático para erros conhecidos → reroda o agente → confirma sucesso.

**Contexto:** Decidido em 2026-04-14. Hoje existe: Layer 1 (log em errors.json) + Layer 2 (diagnóstico automático via Claude no output). Falta: o loop fechado que age sem intervenção manual.

**Histórias planejadas (em ordem de execução):**

1. **Epic 1 — Background monitor** — Thread em background no `app.py` que monitora `errors.json` a cada N segundos. Quando entra um erro novo com `resolved: false`, dispara o ciclo de healing.

2. **Epic 2 — Auto-apply para erros conhecidos** — Se `errors.json` tem registro anterior com `resolved: true` e similaridade >70% com o erro novo, aplica o `fix_applied` diretamente sem chamar Claude. Campo `fix_source: memoria`.

3. **Epic 3 — Reexecução após correção** — Após aplicar fix, reroda o agente com os mesmos inputs. Se sucesso: marca `resolved: true`. Se falha de novo: incrementa `retry_count`. Máx 2 tentativas, depois escala.

4. **Epic 4 — Notificação ao usuário** — Painel no Editor mostra: "⚕️ Healer corrigiu {agente} automaticamente — {regra aplicada}". Badge vermelho na aba Agentes quando há erros não resolvidos.

**Arquivos afetados:**
- `app.py` — background thread, lógica de auto-apply, rerrodada
- `index.html` — badge de erros na aba, painel de notificação do healer
- `agent-healer.md` — já preparado com a hierarquia de 4 níveis

**Nota:** Correções automáticas só para erros conhecidos (memória). Erros novos sempre passam por diagnóstico Claude + aprovação do usuário antes de aplicar fix.

---

### 🔵 IDEIA — Editor Visual: Suporte a Páginas Sem URL Base (Assets Offline)

**Resumo:** Atualmente o editor usa `<base href="https://reliviabr.shop/...">` para carregar CSS, imagens e fontes no iframe. Funciona para páginas já publicadas. Para SaaS público, usuários vão editar páginas novas que ainda não têm URL — abrirão sem estilo e com imagens quebradas.

**Solução recomendada (2 fases):**

**Fase 1 — Proxy de assets via GitHub** (baixa complexidade, resolve fase atual):
- Nova rota Flask `GET /advertorials/asset?path=...`
- Busca o arquivo no repo GitHub (raw.githubusercontent.com) e serve localmente
- iframe usa `<base href="http://localhost:5011/advertorials/asset?base=pasta/">`
- Funciona para qualquer arquivo já commitado no GitHub, mesmo sem deploy na Vercel
- Não resolve páginas 100% novas (nunca commitadas)

**Fase 2 — Upload de pasta/ZIP** (para SaaS público):
- Usuário faz upload de `.zip` com HTML + pasta de assets (css/, images/, js/)
- Backend extrai em diretório temporário por sessão (`/tmp/editor/{session_id}/`)
- Flask serve os assets estáticos desse diretório durante a edição
- iframe usa `<base href="http://localhost:5011/editor-assets/{session_id}/">`
- Ao publicar: envia HTML + assets para o GitHub em batch
- Limpeza automática dos temporários após 24h

**Arquivos afetados:**
- `app.py` — rota `/advertorials/asset` (Fase 1) + `/editor-assets/{id}` (Fase 2)
- `index.html` — lógica de upload ZIP + progress bar de extração

**Contexto adicional:** Fase 1 pode ser implementada em ~1h. Fase 2 requer UX de upload + gestão de sessão — implementar só antes de abrir ao público.

---

### 🔵 IDEIA — (espaço para próximas features)

<!-- Adicionar novas features aqui no mesmo formato -->
