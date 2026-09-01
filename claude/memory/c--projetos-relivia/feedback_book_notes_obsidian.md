---
name: Protocolo Book Notes + Obsidian para otimizar tarefas
description: Quando executando qualquer tarefa, consultar Obsidian com base de book notes para identificar o melhor conhecimento para auxiliar naquela tarefa específica
type: feedback
originSessionId: 80713e13-777c-43b2-86f9-1f5c6bb1da7d
---
Quando executando qualquer tarefa relevante (copy, criativos, ads, agentes, processos, escala), consultar o Obsidian na base de book notes para identificar qual conhecimento dos livros pode otimizar a execução daquela tarefa.

**Why:** O Obsidian contém (ou conterá) resumos densos dos melhores livros de organização, processos, persuasão e escala. Consultar antes de executar permite aplicar frameworks já validados em vez de improvisar.

**How to apply:**

1. Antes de executar tarefas complexas, verificar se há conteúdo relevante no Obsidian em `Relivia Context/Book Notes/`
2. Usar a API local: `curl -sk -H "Authorization: Bearer ff2e82f90760294abac3ead1a6d21962723089086ec04c7f98d69564af406140" "https://127.0.0.1:27124/vault/Relivia%20Context/Book%20Notes/000-INDICE.md"`
3. Navegar para o livro/grupo mais relevante para a tarefa em questão
4. Aplicar os frameworks/bullets encontrados na execução

**Mapeamento tarefa → livros:**
- Copy / criativos → Influence, Hooked, Thinking Fast and Slow, To Sell Is Human, Never Split the Difference
- Facebook Ads / performance → Thinking Fast and Slow, The Power of Habit, Switch, Influence
- Agentes de IA / arquitetura → Thinking in Systems, An Elegant Puzzle, The Mythical Man-Month, High Scalability
- Processos / operação → Rework, The Knack, Multipliers, Drive, Seven Habits
- Escala de e-commerce → Do More Faster, Remote, Rework, Multipliers

**Protocolo para baixar os book notes (quando ainda não estão no Obsidian):**
1. Listar todos os livros relevantes com grupo e prioridade
2. Confirmar a lista com o usuário
3. Baixar via Playwright: `https://raw.githubusercontent.com/mgp/book-notes/master/[nome-do-livro].markdown`
4. Agrupar por tema (Grupo 1: Sistemas, Grupo 2: Persuasão, Grupo 3: Performance, Grupo 4: Processos)
5. Resolver grupo por grupo, confirmar entre grupos
6. Usar TodoWrite para rastrear progresso
7. Salvar cada livro no Obsidian em `Relivia Context/Book Notes/[Grupo]/[livro].md`
8. Salvar pendências no Obsidian ao final da sessão
