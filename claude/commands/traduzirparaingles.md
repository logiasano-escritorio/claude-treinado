# Traduzir Produto PT-BR → English

Leia o megaprompt de tradução salvo na memória:
`C:/Users/user/.claude/projects/c--projetos-relivia-alinhafacil-cf/memory/prompt_traducao_pt_en.md`

Aplique todas as regras e adaptações do megaprompt ao conteúdo fornecido pelo usuário.

Antes de pedir o conteúdo, pergunte o mercado de destino:

> **"Para qual mercado anglófono você deseja adaptar?"**
> 1. 🇺🇸 **EUA** — inglês americano (USD, FDA, cidades americanas)
> 2. 🇨🇦 **Canadá** — inglês canadense (CAD, Health Canada, cidades canadenses)
> 3. 🇬🇧 **Reino Unido** — inglês britânico (GBP/£, MHRA, cidades britânicas)
> 4. 🇦🇺 **Austrália** — inglês australiano (AUD, TGA, cidades australianas)
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
  - EUA → `-eua`
  - Canadá → `-canada`
  - Reino Unido → `-uk`
  - Austrália → `-australia`
- Exemplos:
  - `produto.html` → `produto-eua.html` / `produto-uk.html` / etc.
  - `pagina-relivia.md` → `pagina-relivia-uk.md`
- Se o arquivo já existir, adicione numeração: `produto-uk-2.html`, `produto-uk-3.html`, etc.
- Salve no mesmo diretório do arquivo original.

Se o usuário colou o conteúdo diretamente (sem arquivo), apenas exiba o resultado na conversa.
