# /roadmap — Gerenciador de Roadmap do Relívia Editor

Quando o usuário invocar `/roadmap`, execute o seguinte fluxo:

## Passo 1 — Carregar o roadmap

Leia o arquivo de roadmap em memória:
`C:/Users/user/.claude/projects/c--projetos-relivia/memory/roadmap_relivia_editor.md`

## Passo 2 — Listar as features

Exiba as features em formato numerado com status visual:
- 🟡 PLANEJADA — feature detalhada, pronta para executar
- 🔵 IDEIA — rascunho, precisa de detalhamento
- 🟢 EM ANDAMENTO — sendo desenvolvida agora
- ✅ CONCLUÍDA — já implementada

Exemplo de output:
```
📋 ROADMAP — Relívia Editor

Features disponíveis:

1. 🟡 CMS com GitHub + Vercel integrado
   Editar advertoriais com drag & drop e publicar com 1 clique

2. 🔵 [próxima ideia]
   ...

Digite o número da feature que quer executar, ou:
- "adicionar" para registrar uma nova feature
- "concluir N" para marcar a feature N como concluída
```

## Passo 3 — Ação do usuário

### Se escolher um número:
1. Carregue o contexto completo da feature escolhida
2. Invoque o Orion (aiox-master) com o contexto já carregado
3. Orion inicia a execução pela primeira história pendente da feature

### Se digitar "adicionar":
1. Pergunte: nome da feature, resumo em 1-2 frases, qual produto/projeto
2. Salve no roadmap com status 🔵 IDEIA
3. Confirme o salvamento

### Se digitar "concluir N":
1. Atualize o status da feature N para ✅ CONCLUÍDA no arquivo de roadmap
2. Confirme

## Regras

- Sempre ler o arquivo de roadmap antes de listar (pode ter sido atualizado)
- Ao executar uma feature, carregar TODO o contexto dela (stack, histórias, arquivos afetados)
- Não inventar features — apenas o que está no arquivo
- Ao iniciar execução, chamar o skill `commands:AIOX:agents:aiox-master` com o contexto da feature como briefing
