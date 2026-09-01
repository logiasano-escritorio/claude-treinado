---
name: Vault Obsidian SANOLOGIA
description: Onde fica o vault de gestão de funis Sano — reorganizado por produto (2026-06-11), planilha por produto atualizar a cada deploy
type: reference
originSessionId: ee4c68e7-2222-49c8-b6bc-2e69f5a65799
---
Vault Obsidian: `c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/` (com espaço, NÃO confundir com `c:/Users/user/Desktop/Sanologia/` que é o projeto HTML).

**Estrutura (reorganizada 2026-06-11 — modelo Prime-Creme replicado pra todos):**
- `Produtos/<Produto>/` — TUDO de um produto numa pasta só (B12, GlowUp, StrongBones, Magnesio, Prime-Creme)
  - `<Produto>.md` — aba/painel (planilha de funis: # | Status | Ângulo | Adv URL | Página URL | Checkout | Criativo | Notas). Exceção: Prime-Creme usa `00-Prime-Creme.md`
  - `Funis/` — 1 nota por funil (textos de anúncio, persona, mecanismo, URLs)
  - `Criativos/` — nota de preview + pasta de PNGs por funil
  - `Advertoriais/` e `Paginas-Produto/` — notas detalhadas
  - Prime-Creme tem ainda `Angulos/` e `Campanhas/` (IDs Meta reais) — replicar ao escalar outro produto
- `00-Dashboard.md` — dashboard geral (tabela de produtos + mapa "como achar qualquer coisa")
- `Workflows/`, `Research/`, `Reportana/`, `Conteudo/`, `Instagram Sano/`, `_templates/` — transversais, na raiz

Quando faço deploy de novo ângulo, atualizar a linha na aba do produto (`Produtos/<P>/<P>.md`): status ⚪ rascunho → 🟢 no ar.

Legenda status: 🟢 No ar · 🟡 Legado · 🔵 Teste A/B · 🔴 Pausado · ⚪ Rascunho

Backup pré-reorganização: `Desktop/SANOLOGIA-OBSIDIAN-backup-2026-06-11.zip`. Script da migração: `Sanologia/_dev/migrar-vault-obsidian.ps1`.
