---
name: Loop de teste do Replix usa fixtures, não roda pipeline toda vez
description: Quando trabalhando em features do Replix, NÃO peça pro usuário gerar página nova só pra validar — usa páginas já geradas em Replix/projetos/ como fixtures.
type: feedback
originSessionId: c382f367-09fc-4bfb-9c5b-c999fb76785d
---
Quando estiver implementando feature no Replix (`_Projetos/replix/`), **não force o usuário a gerar uma página nova** só pra validar mudança de prompt/parser/UI. Custa 3min + R$5-8 + esperar Gemini, e o loop "gera-valida-ajusta-gera de novo" trava o desenvolvimento.

**How to apply:**

- Pra validar mudanças de **parser/patch HTML / UI nova**: usa `index.html` de páginas já geradas em `Replix/projetos/{idioma}/{slug}/index.html`. A última gerada (Ceylon Cinnamon) tem markup completo — basta `Grep` pra ver o que tá lá.

- Pra validar mudanças no **prompt do DeepSeek**: compara o que a página existente tem com o que o prompt novo pede; se o gap é só "campos novos", confiança alta de que vai funcionar. Só roda geração nova se a mudança for **estrutural** (regex completamente diferente).

- Antes de criar tela/feature: confirma que conseguimos testar com fixture. Se não der, pensa em alternativas (endpoint debug, mock) ANTES de codar a feature toda.

**Why:**
- 2026-05-06 perdemos quase 30min planejando "Fase 3 — gerar página de teste" quando o usuário lembrou que já tinha página gerada na sessão anterior.
- Loop gera→valida→ajusta é o pior bottleneck do dev de pipeline LLM. Fixture-based testing reduz iteração de minutos pra segundos.
