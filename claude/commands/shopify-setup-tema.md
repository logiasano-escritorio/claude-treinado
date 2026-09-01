# Setup de Tema Shopify — Novo Cliente

## Objetivo

Quando este comando for invocado, você irá documentar todas as seções de um tema Shopify novo, criando o arquivo de referência necessário para usar o comando `/shopify-page` com esse cliente.

---

## PASSO 1 — Coletar informações do cliente

Pergunte ao usuário:
1. **Nome do cliente** (ex: "Fulano Store", "Bella Cosmetics")
2. **Nome do tema** (ex: "Dawn", "Empire", "Shrine Pro", "Impulse")
3. **Caminho da pasta do tema exportado** (ex: `C:/Users/user/Downloads/tema-cliente/`)
4. **Brand colors** do cliente:
   - Cor primária (accent)
   - Cor do botão CTA
   - Cor de fundo escuro (se houver)
   - Cor das estrelas de avaliação

---

## PASSO 2 — Ler as seções do tema

Com o caminho fornecido, liste todos os arquivos `.liquid` da pasta `sections/` do tema.

Para cada seção relevante para páginas de produto (ignorar `header`, `footer`, `announcement-bar`, `cart`, `password`, `newsletter`, `404`), leia o arquivo e extraia:

1. **Nome do tipo** — o valor de `{% schema %}` → `"name"`
2. **Settings disponíveis** — lista de `id` + `type` + `label` de cada setting
3. **Block types disponíveis** — para cada block: `type`, seus `settings` (id + type + label)
4. **Settings mais importantes** — focar nos que controlam layout, cores, imagens e texto

---

## PASSO 3 — Gerar o arquivo de referência

Criar o arquivo em:
```
C:/Users/user/.claude/projects/c--Users-user--claude/memory/[nome-tema-slug]-sections.md
```

Onde `[nome-tema-slug]` é o nome do tema em lowercase com hífens (ex: `dawn`, `shrine-pro`, `empire`).

**Formato do arquivo** — seguir o mesmo padrão do `shrine-pro-sections.md`:
- Cabeçalho com nome do tema e cliente
- Notas gerais (color schemes disponíveis, como usar custom colors)
- Uma seção por bloco `###`, com: Tipo, Uso, Settings principais, Block Types

---

## PASSO 4 — Registrar o cliente

Adicionar o cliente ao arquivo `C:/Users/user/.claude/projects/c--Users-user--claude/memory/clients.md` no formato:

```markdown
## Cliente: [Nome do Cliente]
- Tema: [Nome do Tema]
- Seções: [nome-tema-slug]-sections.md
- Brand primária: #xxxxxx
- Brand CTA: #xxxxxx
- Brand fundo escuro: #xxxxxx (ou "—" se não tiver)
- Brand estrelas: #xxxxxx
- Loja Shopify: [url ou "não informado"]
```

---

## PASSO 5 — Confirmar

Informar ao usuário:
- Arquivo de seções criado: `memory/[nome-tema-slug]-sections.md`
- Quantas seções foram documentadas
- Cliente adicionado ao `clients.md`
- Que agora pode usar `/shopify-page` normalmente — ao perguntar o cliente, carregar o arquivo correto
