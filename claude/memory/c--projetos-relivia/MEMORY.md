# MEMORY INDEX

## Reference
- [reference_relivia_modelar.md](reference_relivia_modelar.md) — GitHub + Vercel do projeto relivia-modelar: token, repo, project ID, domínio relivia-modelar.vercel.app
- [reference_urls_vercel.md](reference_urls_vercel.md) — URLs completas por produto na Vercel (reliviabr.shop) — usar ao subir anúncios no Facebook Ads
- [reference_relivia_paleta.md](reference_relivia_paleta.md) — Paleta oficial Relívia: azul #2E2BFF (não verde) — botões, CTAs, wave
- [reference_openclaw.md](reference_openclaw.md) — OpenClaw gateway local: token, porta, 5 agentes configurados, protocolo WebSocket, workspaces
- [reference_openclaw_megaprompt.md](reference_openclaw_megaprompt.md) — Megaprompt completo OpenClaw: arquitetura, APIs HTTP/WS, workspaces, skills, multi-agent, CLI, configuração completa
- [reference_openclaw_estudo_completo.md](reference_openclaw_estudo_completo.md) — Resumo anterior (menos preciso) — substituído pela documentação completa abaixo
- **Documentação OpenClaw completa** em `C:\Users\user\Desktop\Obsidian Supremo\Relivia Context\Memory\References\openclaw\` — 9 arquivos: 00-INDICE, 01-arquitetura-workspace, 02-standing-orders, 03-cron-jobs, 04-hooks, 05-heartbeat, 06-agente-send, 07-model-failover, 08-memoria, 09-autonomia-pipeline (plano de implementação)
- [megaprompt_analise_copy_criativos.md](megaprompt_analise_copy_criativos.md) — Megaprompt completo para análise de copy de criativos: mecanismos, blocos de persuasão, gatilhos psicológicos, score de conversão e sugestões de split-test
- [reference_nano_banana_translate_prompt.md](reference_nano_banana_translate_prompt.md) — Megaprompt global para tradução de textos em imagens com Nano Banana + bloco de chamada à API do Google (Gemini Image)
- [reference_google_api_key.md](reference_google_api_key.md) — API Key fixa do Google AI Studio para Nano Banana / Gemini Image (<CHAVE-NO-.env-LOCAL>)
- [reference_claude_api_key.md](reference_claude_api_key.md) — Claude API Key (sk-ant-api03-MwB4...) para projetos Relivia — tradução Canva e scripts Anthropic
- [reference_facebook_token_biblioteca.md](reference_facebook_token_biblioteca.md) — Access Token Meta (ads_read + ads_management) para MCP extrator da Ad Library — análise de anúncios campeões
- [reference_cloudflare_pages.md](reference_cloudflare_pages.md) — Token + Account ID + projeto Cloudflare Pages para deploy automático do site Relívia
- [reference_vercel.md](reference_vercel.md) — Token + Project ID Vercel para deploy dos advertoriais em reliviabr.shop — git user.email obrigatório: reliviabrasil@gmail.com
- [reference_groq_api_key.md](reference_groq_api_key.md) — Groq API Key para Whisper (ytranscribe) — whisper-large-v3-turbo, 7200s/dia gratuito, configurado em ~/.claude.json
- [reference_railway.md](reference_railway.md) — Token Railway para deploy do relivia-modelar via API GraphQL
- [reference_railway_saas_v2.md](reference_railway_saas_v2.md) — Token + serviço + URLs do projeto relivia-saas-v2 no Railway
- [prompt_traducao_qualquer_ptbr.md](prompt_traducao_qualquer_ptbr.md) — Megaprompt para tradução de qualquer idioma → PT-BR: adaptações culturais, preços em R$, nomes, claims Anvisa, gatilhos brasileiros
- [reference_templates_claude_code.md](reference_templates_claude_code.md) — Pacote em [Desktop]/templates-claude-code/ com 2 slash commands genéricos (sem branding Relívia): /gerar-advertorial estilo revista + /clonar-produto-shopify com galeria/variant picker — extração 100% Console F12, prontos para distribuir

- [reference_oregano_estudos_copy.md](reference_oregano_estudos_copy.md) — Mega documento: 11 estudos científicos sobre orégano/carvacrol + copy persuasiva completa (headlines, body, bullets, objeções, claims) para Relívia Orégano
- [reference_mega_prompt_italia.md](reference_mega_prompt_italia.md) — Mega prompt completo para subir as 4 campanhas italianas no FB Ads: pixels, URLs, copies, títulos, pastas de criativos, scripts Python — arquivo em C:\Users\user\Desktop\MEGA-PROMPT-SUBIR-ADS-ITALIA.md
- [reference_elevenlabs_api_key.md](reference_elevenlabs_api_key.md) — API Key ElevenLabs para TTS/dublagem nos projetos Relívia
- [reference_dreamapi_docs.md](reference_dreamapi_docs.md) — DreamAPI (NewportAI) documentação completa: LipSync v1/2.0, DreamAvatar 3.0 Fast, Dreamact, Voice Clone, Storage, Polling — todos os endpoints, params e curl examples
- [reference_framework_vsl_suplemento.md](reference_framework_vsl_suplemento.md) — Framework VSL UGC para qualquer suplemento: 7 ingredientes obrigatórios, arquitetura de confiança progressiva, scorecard 8D, checklist Cialdini+Warren, ângulos derivados — baseado na copy campeã Orégano
- [reference_veo3_prompting.md](reference_veo3_prompting.md) — Guia completo Veo 3: fórmula base, specs (4/6/8s, 720p/1080p, 9:16), técnicas UGC, timestamp prompting, áudio nativo, movimentos de câmera, erros fatais, workflow escala
- [reference_anti_ia_image_prompt.md](reference_anti_ia_image_prompt.md) — 10 técnicas anti-IA para REF-A (avatar humano): iPhone 7 f/2.2, color temp mismatch, JPEG artifacts, vincos anatômicos, bokeh hexagonal smartphone — receita testada
- **Pipeline Criativo UGC completo** em `C:\Users\user\Desktop\Obsidian Supremo\Relivia Context\Playbooks\PIPELINE-CRIATIVO-UGC-SUPLEMENTO.md` — documento mestre: 4 fases (Análise → Evolução tripla → Roteiros Veo 3 → REFs), checklist, templates, case Relívia Orégano

## Project
- [project_relivia_editor.md](project_relivia_editor.md) — Estado completo do Relívia Editor de Criativos: porta 5003, funcionalidades, arquivos, dependências
- [roadmap_relivia_editor.md](roadmap_relivia_editor.md) — Roadmap de features planejadas para o Relívia Editor — usar `/roadmap` para listar e executar
- [roadmap_pipeline_saas.md](roadmap_pipeline_saas.md) — Roadmap do Pipeline Relívia → SaaS: FastAPI + Next.js + Celery + Railway. Fase 1 em andamento.
- [project_agentes_escala.md](project_agentes_escala.md) — Arquitetura de agentes para lançamento end-to-end: Agente 1 construído, IDs ClickUp, estrutura de 4 agentes
- [project_pendencias_agentes.md](project_pendencias_agentes.md) — Lista completa de correções pendentes nos agentes: 4 grupos por dependência, 11 itens, com arquivo e linha afetada
- [project_agente_publicador_decisao.md](project_agente_publicador_decisao.md) — Agente Publicador fora do pipeline automático até pipeline ser validado manualmente

- [feedback_resolucao_problemas_lote.md](feedback_resolucao_problemas_lote.md) — Protocolo para resolver 10+ problemas: agrupar por dependência, resolver grupo por grupo, salvar pendências no Obsidian entre sessões

## Feedback
- [feedback_facebook_ads_rascunho.md](feedback_facebook_ads_rascunho.md) — Facebook Ads: sempre criar como PAUSED, nunca publicar automaticamente
- [feedback_pipeline_data_json.md](feedback_pipeline_data_json.md) — Atualizar pipeline-data.json (Desktop) sempre que criar/alterar agente, persona ou conexão no projeto Otimizacao de escala — mapa mental vivo
- [feedback_book_notes_obsidian.md](feedback_book_notes_obsidian.md) — Consultar Obsidian (Book Notes) antes de tarefas complexas para aplicar frameworks dos melhores livros
- [feedback_gemini_variacoes_imagem.md](feedback_gemini_variacoes_imagem.md) — Geração de variações Gemini: não pedir produto sem enviar arquivo real; sempre forçar texto em PT-BR nos prompts
- [feedback_drissionpage_playwright.md](feedback_drissionpage_playwright.md) — DrissionPage substituiu Playwright em tudo — Playwright desinstalado, nunca usar
- [feedback_paginaproduto_workflow.md](feedback_paginaproduto_workflow.md) — Workflow correto para /paginaproduto com site externo: DrissionPage extrair texto+imagens → fechar browser → cp style.css → Agent gera HTML
- [feedback_gemini_image_edit_formula.md](feedback_gemini_image_edit_formula.md) — Fórmula exata (modelo + prompt + código) que gerou edição perfeita de embalagem com Gemini: modelo gemini-3.1-flash-image-preview + lista numerada com aspas + instrução anti-alucinação
- [feedback_croproduo_idioma.md](feedback_croproduo_idioma.md) — /croproduo deve manter o idioma da página analisada, não forçar italiano
- [feedback_especialista_genero.md](feedback_especialista_genero.md) — Especialistas em advertoriais devem ser sempre homens
- [feedback_editar_arquivo_aberto.md](feedback_editar_arquivo_aberto.md) — Editar sempre apenas o arquivo aberto no IDE, nunca perguntar sobre outros arquivos
- [feedback_reiniciar_servidor.md](feedback_reiniciar_servidor.md) — Sempre reiniciar o servidor Flask do mcp-designer automaticamente após qualquer alteração, sem o usuário pedir
- [feedback_clone_scroll_fix.md](feedback_clone_scroll_fix.md) — Clone de páginas Shopify: sempre aplicar overflow-y fix inline no body+html — Shopify bloqueia scroll por padrão
- [feedback_js_script_injection.md](feedback_js_script_injection.md) — Injeção de JS em HTML: nunca deixar `<script>` duplicado ao fazer slicing; nunca usar `DOMContentLoaded` sozinho — sempre usar padrão readyState
- [feedback_clone_hero_padrao.md](feedback_clone_hero_padrao.md) — Padrão obrigatório de galeria + variant picker em clones: HTML rl-*, JS readyState, imagens locais assets/*.webp — nunca usar Swiper/Rapi Bundles do Shopify
- [project_clone_page_escopo.md](project_clone_page_escopo.md) — run2.py é exclusivamente Shopify. HTML puro = pipeline separado futuro, nunca misturar
- [feedback_relatorio_urls_sumario.md](feedback_relatorio_urls_sumario.md) — Relatório do Agente 1: sumário de URLs mostra APENAS URLs com anúncios no top_ads — nunca URLs sem anúncios vinculados
- [feedback_railway_port_cmd.md](feedback_railway_port_cmd.md) — Railway: nunca usar startCommand com $PORT literal; usar CMD Python com os.environ.get; nunca *.txt no .dockerignore
- [feedback_pipeline_criativo_ugc_suplemento.md](feedback_pipeline_criativo_ugc_suplemento.md) — Pipeline canônico para escalar criativo UGC validado: Análise → trio Kennedy/Hormozi/Georgi → Veo 3 → REFs Nano Banana
- [feedback_veo3_regras_suplemento.md](feedback_veo3_regras_suplemento.md) — Regras Veo 3 para suplementos: pessoa SEM produto cenas 1-4, produto entra cena 5, autoridade científica = consultório+jaleco, REF-B só a partir da cena 5, gerar cena 5 PRIMEIRO
