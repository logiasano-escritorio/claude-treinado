---
name: Reiniciar servidor clone.py automaticamente
description: Sempre reiniciar o servidor Flask do mcp-designer sem esperar o usuário pedir
type: feedback
originSessionId: b24458c5-c7de-4a26-a4d7-22e9a63b7a7b
---
Sempre que houver qualquer alteração no app.py ou clone.py, reiniciar o servidor Flask automaticamente sem precisar que o usuário peça.

Comando de reinício:
```bash
pkill -f "mcp-designer/app.py" 2>/dev/null; sleep 1
cd c:/projetos/relivia && ANTHROPIC_API_KEY=<CHAVE-NO-.env-LOCAL> python3 mcp-designer/app.py &
```

**Why:** O usuário quer que o Claude gerencie o ciclo de vida do servidor — nunca delegar isso para ele.

**How to apply:** Após qualquer edit em app.py ou clone.py, rodar o restart automaticamente.
