---
name: vercel-deployer
description: "Faz o deploy para reliviabr.shop com checklist automático — valida domínios, logos e idioma antes de commitar. Sem surpresas no ar."
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Vercel Deployer — Relívia

## Função

Prepara e executa o deploy de arquivos HTML para `reliviabr.shop` via Vercel (git push automático).

## Configuração obrigatória

```bash
git config user.email "reliviabrasil@gmail.com"
git config user.name "relivia-ww"
```

**IMPORTANTE:** O git user.email deve ser `reliviabrasil@gmail.com`. Sem isso, o deploy Vercel falha.

## Checklist pré-deploy (executar sempre)

### 1. Verificar domínios nos arquivos a commitar

```bash
grep -r "reliviaworldwide.com\|relivia.pages.dev" <arquivo.html>
```
Se encontrar: corrigir para `reliviabr.shop` antes de commitar.

### 2. Verificar logo quebrado

```bash
grep -n "relivia.pages.dev/logo.png\|http.*logo.png" <arquivo.html>
```
Se encontrar: substituir por `images/logo.png` (caminho relativo).

### 3. Verificar CTAs com domínio errado

```bash
grep -n 'href="https://reliviaworldwide.com\|href="https://relivia.pages.dev' <arquivo.html>
```
Se encontrar: substituir por `href="https://reliviabr.shop/..."`

## Processo de deploy

```bash
cd /c/projetos/relivia
git config user.email "reliviabrasil@gmail.com"
git add <arquivos específicos>
git commit -m "feat/fix: <descrição do que foi alterado>"
git push origin main
```

**Aguardar ~2 minutos** para o deploy da Vercel propagar.

## Regras

- NUNCA usar `git add -A` ou `git add .` — adicionar apenas os arquivos necessários
- SEMPRE verificar o checklist pré-deploy antes de qualquer commit
- NUNCA commitar arquivos `.env`, `config.json` com tokens ou credenciais
- Criar commit com mensagem descritiva (feat:, fix:, chore:)
- Deploy Vercel é automático via git push — não há comandos manuais extras

## URLs do projeto (para verificação pós-deploy)

Ver memory: `reference_urls_vercel.md` — lista completa por produto.

Base: `https://reliviabr.shop/`
