---
name: Cloudflare Pages — Deploy Automático Relívia
description: Token, Account ID e projeto Cloudflare Pages para deploy automático do site Relívia
type: reference
originSessionId: a4819caf-f8a2-4f89-98d2-79101da7e43e
---
## Credenciais

**API Token:** `cfut_miRI3sOBkSpMrBGY2w3TS6jmCyeCxVRwGP8CtSrsa329439d`
**Account ID:** `6d6e379a67032398100cc2a6cbec7bf1`
**Projeto Pages:** `relivia`
**Domínio:** `relivia.pages.dev`

## Como fazer deploy via API

```python
import requests, json, hashlib

TOKEN   = 'cfut_miRI3sOBkSpMrBGY2w3TS6jmCyeCxVRwGP8CtSrsa329439d'
ACCOUNT = '6d6e379a67032398100cc2a6cbec7bf1'
PROJECT = 'relivia'

# 1. Ler arquivos e calcular hashes SHA256
with open('arquivo.html', 'rb') as f: content = f.read()
file_hash = hashlib.sha256(content).hexdigest()

# 2. Montar manifest (path → hash)
manifest = {'/caminho/no/site/arquivo.html': file_hash}

# 3. POST com files + manifest
files = [('files', (file_hash, content, 'text/html'))]
data  = [('manifest', json.dumps(manifest)), ('branch', 'main')]

resp = requests.post(
    f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/pages/projects/{PROJECT}/deployments',
    headers={'Authorization': f'Bearer {TOKEN}'},
    files=files, data=data,
)
dep = resp.json()['result']
print('URL:', dep['url'])
```

## Observações
- O path no manifest deve começar com `/` e refletir a estrutura de pastas do site
- Múltiplos arquivos: adicionar cada um em `files` e `manifest`
- Deploy fica disponível imediatamente após stage `deploy: success`
- URL do deployment é única por deploy — o domínio principal `relivia.pages.dev` aponta para o último deploy de produção
