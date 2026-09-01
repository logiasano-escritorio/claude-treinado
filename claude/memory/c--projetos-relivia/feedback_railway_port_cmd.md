---
name: Railway — PORT env var e startCommand
description: Como configurar corretamente porta e CMD no Railway para evitar 502 Bad Gateway
type: feedback
originSessionId: b24458c5-c7de-4a26-a4d7-22e9a63b7a7b
---
Nunca usar `startCommand` via API Railway com `$PORT` literal — o shell não expande a variável e o uvicorn falha com "Invalid value for '--port': '$PORT' is not a valid integer".

**Why:** O `startCommand` configurado via API sobrescreve o `CMD` do Dockerfile mas é executado sem expansão de variáveis de shell. Além disso, o `.dockerignore` com `*.txt` bloqueia o `requirements.txt` no build.

**How to apply:**
1. No `Dockerfile`, usar `CMD ["python", "-c", "import os,uvicorn; uvicorn.run('app:app', host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))"]` — Python lê a env var diretamente, sem depender de shell.
2. Nunca definir `startCommand` via API quando o `CMD` do Dockerfile já resolve a porta corretamente. Se foi definido acidentalmente, limpar com `startCommand: ""`.
3. No `.dockerignore`, nunca usar `*.txt` — bloqueia `requirements.txt`. Listar arquivos específicos a ignorar.
