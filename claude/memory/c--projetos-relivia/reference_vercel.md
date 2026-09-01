---
name: Vercel — Token e Projeto Relivia Advertoriais
description: Token, Project ID e domínio Vercel para deploy automático dos advertoriais Relívia
type: reference
originSessionId: c21e05d4-217b-4244-84d6-642f9888fa32
---
## Credenciais

**Token:** `vcp_4k1CbqEZlJM199RdUjUhjwdQTTaSq19Oyhly9noucJ64XratTF4boS1W`
**Project ID:** `prj_9o8PyEFgxME8MLcZ7AJrgyzLYXAh`
**Org ID:** `team_q3vk49xbaiHoclK2RqDo7o5o`
**Projeto:** `relivia-advertoriais`
**Domínio:** `reliviabr.shop`
**URL padrão:** `https://relivia-advertoriais.vercel.app`

## Repositório GitHub conectado

**Repo:** `relivia-ww/relivia-pages`
**Branch:** `main`
**Git user.email:** `reliviabrasil@gmail.com` (OBRIGATÓRIO — Vercel bloqueia commits de outros emails)
**Git user.name:** `relivia-ww`

## Problema conhecido

Vercel bloqueia deploy com `COMMIT_AUTHOR_REQUIRED` se o email do commit não for membro verificado.
Solução: sempre usar `git config user.email reliviabrasil@gmail.com` no repo `C:/projetos/relivia`.

## Configuração salva em

`C:/Users/user/Desktop/Obsidian Supremo/Otimizacao de escala/config.json`
Chaves: `vercel_token`, `vercel_project_id`, `vercel_org_id`, `vercel_dominio`
