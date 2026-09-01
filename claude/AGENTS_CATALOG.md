# AGENTS CATALOG — Auto-routing Guide

Este catálogo mapeia tópicos/situações → agente ou command certo.
Claude deve consultar este arquivo e chamar o agente adequado automaticamente.

---

## DESENVOLVIMENTO BACKEND / APIs

| Situação | Agente/Command |
|---|---|
| Criar API REST, endpoint, servidor | `backend-developer` |
| FastAPI especificamente | `fastapi-developer` |
| Django | `django-developer` |
| Node.js / Express | `node-specialist` |
| GraphQL | `graphql-architect` |
| Microserviços | `microservices-architect` |
| Design de API (estrutura, versionamento) | `api-designer` |
| Documentar API / OpenAPI | `api-documenter` |
| `/setup:design-rest-api` | Design de contrato REST |
| `/setup:implement-graphql-api` | Implementar GraphQL |

## DESENVOLVIMENTO FRONTEND / UI

| Situação | Agente/Command |
|---|---|
| React genérico | `react-specialist` |
| Next.js | `nextjs-developer` |
| Vue.js | `vue-expert` |
| Angular | `angular-architect` |
| Componente UI | `frontend-developer` ou `/dev:create-ui-component` |
| Design system, tokens visuais | `design-bridge` |
| Acessibilidade WCAG | `accessibility-tester` |
| UX flow, wireframe | `ux-researcher` |
| UI visual / mockup | `ui-designer` |

## FULLSTACK / SAAS

| Situação | Agente/Command |
|---|---|
| Projeto fullstack completo | `fullstack-developer` |
| SaaS do zero | `fullstack-developer` + `/project:init-project` |
| Feature nova num projeto | `/project:create-feature` |
| Adicionar pacote/dependência | `/project:add-package` |
| Health check do projeto | `/project:project-health-check` |

## PYTHON

| Situação | Agente/Command |
|---|---|
| Python geral | `python-pro` |
| FastAPI | `fastapi-developer` |
| Django | `django-developer` |
| ML/Data Science em Python | `machine-learning-engineer` ou `data-scientist` |
| Script, automação Python | `python-pro` |

## LINGUAGENS ESPECÍFICAS

| Linguagem | Agente |
|---|---|
| TypeScript | `typescript-pro` |
| JavaScript | `javascript-pro` |
| Go | `golang-pro` |
| Rust | `rust-engineer` |
| C++ | `cpp-pro` |
| C# / .NET | `csharp-developer` ou `dotnet-core-expert` |
| Java / Spring | `java-architect` ou `spring-boot-engineer` |
| PHP / Laravel | `laravel-specialist` ou `php-pro` |
| Ruby on Rails | `rails-expert` |
| Swift / iOS | `swift-expert` |
| Kotlin / Android | `kotlin-specialist` |
| Flutter | `flutter-expert` |
| Elixir | `elixir-expert` |

## BANCO DE DADOS

| Situação | Agente/Command |
|---|---|
| SQL genérico | `sql-pro` |
| PostgreSQL | `postgres-pro` |
| Design de schema | `/setup:design-database-schema` |
| Migrations | `/setup:create-database-migrations` |
| Otimização de queries | `database-optimizer` ou `/performance:optimize-database-performance` |
| DBA geral | `database-administrator` |

## DEVOPS / INFRAESTRUTURA

| Situação | Agente/Command |
|---|---|
| CI/CD pipeline | `devops-engineer` ou `/deploy:ci-setup` |
| Docker | `docker-expert` ou `/deploy:containerize-application` |
| Kubernetes | `kubernetes-specialist` ou `/deploy:setup-kubernetes-deployment` |
| Terraform / IaC | `terraform-engineer` |
| AWS/Azure/GCP | `cloud-architect` ou `azure-infra-engineer` |
| Release / deploy | `/deploy:prepare-release` |
| Rollback emergência | `/deploy:rollback-deploy` |
| Hotfix | `/deploy:hotfix-deploy` |
| SRE, observabilidade | `sre-engineer` |
| Monitoramento | `/setup:setup-monitoring-observability` |
| Platform engineering | `platform-engineer` |

## TESTES / QUALIDADE

| Situação | Agente/Command |
|---|---|
| Escrever testes | `qa-expert` ou `/test:write-tests` |
| Cobertura de testes | `/test:test-coverage` |
| Testes E2E | `/test:e2e-setup` |
| Testes de carga | `/test:setup-load-testing` |
| Testes visuais | `/test:setup-visual-testing` |
| Mutation testing | `/test:add-mutation-testing` |
| Automação de testes | `test-automator` |

## CODE REVIEW / REFACTORING / DEBUG

| Situação | Agente/Command |
|---|---|
| Revisar código | `code-reviewer` ou `/dev:code-review` |
| Refatorar | `refactoring-specialist` ou `/dev:refactor-code` |
| Debug de erro | `debugger` ou `/dev:debug-error` |
| Remover código morto | `/dev:remove-dead-code` |
| Explicar código | `/dev:explain-code` |
| Analisar arquitetura | `architect-reviewer` |
| Pensar profundamente num problema | `/dev:ultra-think` |
| Modernizar deps | `/setup:modernize-deps` |
| Migrar para TypeScript | `/setup:migrate-to-typescript` |

## SEGURANÇA

| Situação | Agente/Command |
|---|---|
| Auditoria de segurança | `security-auditor` ou `/security:security-audit` |
| Hardening | `/security:security-hardening` |
| Autenticação | `/security:add-authentication-system` |
| Auditoria de dependências | `/security:dependency-audit` |
| Pentest | `penetration-tester` |
| Active Directory | `ad-security-reviewer` |

## PERFORMANCE

| Situação | Agente/Command |
|---|---|
| Otimizar bundle frontend | `/performance:optimize-bundle-size` |
| Otimizar build | `/performance:optimize-build` |
| Estratégia de cache | `/performance:implement-caching-strategy` |
| CDN | `/performance:setup-cdn-optimization` |
| Auditoria de performance | `/performance:performance-audit` |
| Monitoramento de performance | `performance-monitor` |

## DOCUMENTAÇÃO

| Situação | Agente/Command |
|---|---|
| Documentação de API | `/docs:doc-api` |
| Documentação arquitetural | `/docs:create-architecture-documentation` |
| Guia de onboarding | `/docs:create-onboarding-guide` |
| README | `readme-generator` |
| Troubleshooting guide | `/docs:troubleshooting-guide` |
| Technical writer | `technical-writer` |

## DADOS / ML / IA

| Situação | Agente/Command |
|---|---|
| Machine learning | `machine-learning-engineer` ou `ml-engineer` |
| MLOps / pipeline de ML | `mlops-engineer` |
| NLP / LLMs | `nlp-engineer` ou `llm-architect` |
| Data engineering | `data-engineer` |
| Data science / análise | `data-scientist` ou `data-analyst` |
| AI engineer (sistemas de IA) | `ai-engineer` |
| Prompt engineering | `prompt-engineer` |
| Reinforcement learning | `reinforcement-learning-engineer` |

## MARKETING / COPY / ADS (Relívia)

| Situação | Agente/Command |
|---|---|
| Anúncio Facebook, copy long-form | `/copy-anuncio` |
| Escrever headline, bullets, carta de vendas | `copy-master:tasks:write-*` |
| Analisar copy existente | `/analise-copy` ou `copy-master:tasks:analyze-copy` |
| Gerar advertorial | `/gerar-advertorial` |
| Auditar advertorial | `/auditoria-advertorial` ou `advertorial-auditor` |
| Página de produto (CRO) | `/paginaproduto` ou `08-agente-produto` |
| Traduzir página | `/traduzirparaportugues` / `/traduzirparaespanhol` etc. |
| Adaptar advertorial PT-BR | `/adaptar-advertorial` |
| Tráfego pago / Meta Ads | `04-agente-trafego` ou `traffic-masters:tasks:create-ad-strategy` |
| Subir anúncio Meta API | `09-agente-publicador` |
| Escalar campanha | `10-agente-escala` ou `traffic-masters:tasks:scale-campaign` |
| Análise de criativos | `02-agente-analise` ou `traffic-masters:agents:creative-analyst` |
| Funil de anúncios | `01-agente-funil` |
| Comentários Facebook | `/fb-comentarios` |

## PIPELINE RELIVIA (end-to-end)

| Situação | Agente |
|---|---|
| Espionar concorrentes Ads Library | `01-agente-funil` |
| Engenharia reversa anúncio | `02-agente-analise` |
| Clonar landing page | `03-agente-clone` |
| Elevar copy | `05-agente-copy` |
| Traduzir página | `06-agente-traducao` |
| QA do output | `07-agente-revisor` |
| Deploy advertorial | `vercel-deployer` |
| Auditoria pré-deploy | `advertorial-auditor` |

## PRODUTO / NEGÓCIO / ESTRATÉGIA

| Situação | Agente/Command |
|---|---|
| Product manager | `product-manager` |
| Validar ideia de produto | `project-idea-validator` |
| Business analyst | `business-analyst` |
| Estratégia de negócio (C-level) | `c-level-squad:agents:vision-chief` |
| Conselho estratégico (Ray Dalio, Naval, etc.) | `advisory-board:tasks:convene-board` |
| Precificação, ofertas (Hormozi) | `hormozi-squad:agents:hormozi-pricing` |
| Oferta irresistível | `hormozi-squad:tasks:create-offer` |
| Go-to-market | `c-level-squad:tasks:plan-go-to-market` |
| Análise competitiva | `competitive-analyst` |
| Pesquisa de mercado | `market-researcher` |

## GIT / WORKFLOW DE TIME

| Situação | Agente/Command |
|---|---|
| Status git, branches | `/dev:git-status` |
| Limpar branches antigas | `/dev:clean-branches` |
| Sprint planning | `team:sprint-planning` |
| Standup | `team:standup-report` |
| Retrospectiva | `team:retrospective-analyzer` |
| Gestão de projeto | `project-manager` ou `scrum-master` |

## MULTI-AGENTE / ORQUESTRAÇÃO

| Situação | Agente/Command |
|---|---|
| Coordenar vários agentes | `multi-agent-coordinator` ou `codebase-orchestrator` |
| Decompor tarefa complexa em paralelo | `/spec-workflow:parallel-tasks` |
| Quick spec de feature | `/spec-workflow:quick-spec` |
| Orquestrar tarefa longa | `/orchestration:start` + `/orchestration:status` |
| Montar time de agentes | `agent-organizer` |

---

## REGRA DE AUTO-ROUTING

Quando identificar um destes contextos, chamar o agente correspondente SEM esperar o usuário pedir:

- **Python/FastAPI/Django** → `python-pro` ou `fastapi-developer`
- **Next.js/React** → `nextjs-developer` ou `react-specialist`
- **Bug/erro no código** → `debugger`
- **Code review pedido** → `code-reviewer`
- **Deploy/CI** → `devops-engineer`
- **Segurança** → `security-auditor`
- **Testes** → `qa-expert`
- **Copy/anúncio Relívia** → agentes do pipeline Relívia
- **Decisão estratégica de negócio** → `advisory-board` ou `c-level-squad`
- **Performance lenta** → `performance-engineer`
- **Banco de dados** → `sql-pro` ou `postgres-pro`
