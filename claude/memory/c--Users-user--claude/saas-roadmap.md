# Roadmap — Gerador Internacional de Landing Pages

## Contexto
Construir dentro do editor-visual existente (Node.js + Puppeteer + HTML).
Produto: lojista cola URL Shopify → escolhe idioma → recebe HTML localizado com cores/logo da marca deles + template estrutural padrão.

## Stack
- Backend: `C:/Users/user/Desktop/editor-server/` (Node.js + Puppeteer já existente)
- Frontend: `C:/Users/user/Desktop/editor-visual.html` (adicionar painel novo)
- LLM: `@anthropic-ai/sdk` — modelo `claude-sonnet-4-6` (velocidade) ou `claude-opus-4-6` (qualidade)
- Streaming: ativado para evitar timeout na geração

---

## Fase 1 — Núcleo (MVP funcional)
**Objetivo:** colar URL → escolher idioma → baixar HTML
**Status:** não iniciado

- [ ] Adicionar painel "🌍 Gerar Internacional" no `editor-visual.html`
- [ ] Rota no backend: `POST /generate-international`
- [ ] Puppeteer: busca URL → extrai `MainContent` HTML
- [ ] Puppeteer: extrai logo (`header img`) + cor primária (computed style do botão CTA)
- [ ] Instalar e integrar `@anthropic-ai/sdk` no editor-server
- [ ] Prompt estruturado para Claude API → gera HTML localizado com template padrão
- [ ] Retorna HTML para download direto no browser

---

## Fase 2 — Qualidade visual
**Objetivo:** página gerada parecer da marca do lojista
**Status:** não iniciado

- [ ] Extração completa de cores: CSS variables do tema Shopify (`--color-button`, `--color-accent`, `--color-background`)
- [ ] Fallback: extrai cor via computed style se variables não existirem
- [ ] Injeta cores extraídas como variáveis CSS no template gerado
- [ ] Injeta logo do lojista no header/footer
- [ ] Preview inline no editor antes do download

---

## Fase 3 — Mercados e idiomas
**Objetivo:** suporte robusto a múltiplos mercados
**Status:** não iniciado

- [ ] Seletor de idioma/mercado no painel (IT, ES, EN-UK, EN-US, FR, DE)
- [ ] Banco de dados cultural por mercado (nomes, cidades, médicos, moeda, telefone)
- [ ] Adaptação automática de preços por mercado (taxa de conversão configurável)
- [ ] Geração em batch: mesma URL → múltiplos idiomas de uma vez

---

## Fase 4 — SaaS multi-cliente
**Objetivo:** outros lojistas usarem via web
**Status:** não iniciado

- [ ] Frontend web standalone (fora do editor local)
- [ ] Autenticação simples (API key por cliente)
- [ ] Painel de histórico (URLs geradas por cliente)
- [ ] Tracking de uso (tokens consumidos / páginas geradas)
- [ ] Deploy em Railway ou Render

---

## Decisões tomadas
- Template estrutural fixo (baseado no design Relívia)
- Cores e logo extraídas automaticamente da URL do lojista
- Bloco de produto nativo do Shopify é ignorado — substituído pelo template padrão Relívia
- Página gerada é HTML standalone para download

## Próximo passo
Iniciar Fase 1 — adicionar painel no editor-visual.html e rota `/generate-international` no backend.
