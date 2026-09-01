---
name: Editar apenas o arquivo aberto no IDE
description: Quando o usuário pede para substituir URLs ou editar código, sempre editar apenas o arquivo atualmente aberto no IDE — nunca perguntar sobre outros arquivos nem editar múltiplos arquivos sem confirmação explícita.
type: feedback
---

Editar sempre apenas o arquivo aberto no IDE quando o usuário fizer substituições ou edições.

**Why:** O usuário explicitou "só o aberto, SEMPRE" — perguntar sobre outros arquivos é desnecessário e gera fricção.

**How to apply:** Quando o usuário pede para trocar uma URL ou imagem, verificar qual arquivo está aberto no IDE (indicado por `ide_opened_file`) e editar somente esse. Só perguntar se não houver nenhum arquivo aberto no IDE.
