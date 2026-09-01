# Relivia Fix Href — Trocar links relivia.pages.dev

O usuário vai fornecer:
1. Caminho do arquivo HTML (ex: `C:\Users\user\Desktop\relivia\alinhafacil\adv.html`)
2. Nome do produto (ex: `alinhafacil`)
3. Nome da page de destino (ex: `alinhafacilpage`)

**O que fazer:**

Leia o arquivo e substitua **todos** os `href` que apontam para `relivia.pages.dev` (qualquer subpath) pela URL:

```
https://relivia.pages.dev/[produto]/[page]
```

Onde `[produto]` e `[page]` são os valores fornecidos pelo usuário.

Isso inclui:
- `href="https://relivia.pages.dev/..."` em tags `<a>`
- `href='https://relivia.pages.dev/...'` (aspas simples)
- Qualquer variação de subpath — substitua tudo pelo novo destino

Use `sed` ou edite diretamente o arquivo com o Edit tool.

Após aplicar, mostre quantas substituições foram feitas e confirme o novo href.
