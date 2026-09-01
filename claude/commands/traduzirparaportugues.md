# Traduzir Produto [Qualquer Língua] → Português Brasileiro

Leia o megaprompt de tradução salvo na memória:
`C:/Users/user/.claude/projects/c--projetos-relivia/memory/prompt_traducao_qualquer_ptbr.md`

Aplique todas as regras e adaptações do megaprompt ao conteúdo fornecido pelo usuário.

Se o usuário ainda não colou o conteúdo a ser traduzido, peça agora:

> **"Cole o conteúdo que deseja traduzir e adaptar para o português brasileiro."**
>
> Se for uma página de produto ou copy com preços/CTAs, pergunte também:
> - O nome do produto no Brasil (ex: Relívia Orégano) — se aplicável
> - O link de checkout (para substituir CTAs) — se aplicável
> - O preço em R$ (para substituir preços estrangeiros) — se aplicável
>
> Se for um texto simples (criativo, copy de anúncio, e-mail, post etc.), apenas execute a tradução diretamente.

Ao receber o conteúdo, execute a tradução completa seguindo o megaprompt e entregue:
1. O texto traduzido e adaptado completo — pronto para publicar
2. Notas de adaptação — principais mudanças feitas (idioma de origem detectado, preços, nomes, claims ajustados) — apenas se houver adaptações relevantes a destacar
3. Alertas — pontos que precisam de informação adicional do cliente — apenas se necessário

## SALVAR ARQUIVO

Se o usuário forneceu um **arquivo** como input (ex: `produto.html`, `pagina.md`, `copy.txt`):
- Salve o resultado em um **novo arquivo** com `-ptbr` adicionado ao nome, **sem sobrescrever o original**
- Exemplos:
  - `produto.html` → `produto-ptbr.html`
  - `pagina-en.md` → `pagina-ptbr.md`
  - `copy.txt` → `copy-ptbr.txt`
- Se já existir um `produto-ptbr.html`, crie `produto-ptbr-2.html`, `produto-ptbr-3.html`, etc.
- Salve no mesmo diretório do arquivo original.

Se o usuário colou o conteúdo diretamente (sem arquivo), apenas exiba o resultado na conversa.
