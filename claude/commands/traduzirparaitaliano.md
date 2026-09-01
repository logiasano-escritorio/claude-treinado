# Traduzir Produto PT-BR → Italiano

Leia o megaprompt de tradução salvo na memória:
`C:/Users/user/.claude/projects/c--projetos-relivia-alinhafacil-cf/memory/prompt_traducao_pt_it.md`

Aplique todas as regras e adaptações do megaprompt ao conteúdo fornecido pelo usuário.

Antes de pedir o conteúdo, pergunte o mercado de destino:

> **"Para qual mercado italiano você deseja adaptar?"**
> 1. 🇮🇹 **Itália** — italiano padrão (EUR, ISS/AIFA, cidades italianas)
> 2. 🇨🇭 **Suíça Italiana** — italiano suíço (CHF, Swissmedic, cidades suíças)
>
> Após confirmar o mercado, cole o conteúdo que deseja traduzir.

Ao receber o conteúdo, execute a tradução completa seguindo o megaprompt e entregue:
1. O texto traduzido e adaptado completo — pronto para publicar
2. Notas de adaptação — principais mudanças feitas (mercado, preços, nomes, claims)
3. Alertas — pontos que precisam de informação adicional do cliente

## SALVAR ARQUIVO

Se o usuário forneceu um arquivo como input (ex: `produto.html`, `pagina.md`, `copy.txt`):
- Salve o resultado em um **novo arquivo** com o sufixo do mercado adicionado ao nome, **sem sobrescrever o original**
- Sufixos por mercado:
  - Itália → `-italia`
  - Suíça Italiana → `-suica-it`
- Exemplos:
  - `produto.html` → `produto-italia.html`
  - `pagina-relivia.md` → `pagina-relivia-italia.md`
- Se o arquivo já existir, adicione numeração: `produto-italia-2.html`, etc.
- Salve no mesmo diretório do arquivo original.

Se o usuário colou o conteúdo diretamente (sem arquivo), apenas exiba o resultado na conversa.
