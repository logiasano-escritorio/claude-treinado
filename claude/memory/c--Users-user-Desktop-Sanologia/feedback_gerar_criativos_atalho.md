---
name: Atalho "gera os criativos de X" → /sano-criativos
description: Quando o usuário fala "gera os criativos do <produto> [<ângulo>]", chamar /sano-criativos direto sem cerimônia
type: feedback
originSessionId: d2c18d3e-aab0-440a-b3c4-86d8c38e0c1d
---
Quando o usuário falar **"gera os criativos do <produto>"** ou **"gera os criativos do <produto> <ângulo>"** (ou qualquer variação tipo "gere os criativos pra...", "cria os criativos do..."), executar `/sano-criativos` direto, sem perguntar nada além do necessário.

**Regras de roteamento:**

1. **Produto + slug/ângulo informado** (ex: "gera os criativos do B12 diabetes", "StrongBones artrose", "GlowUp menopausa"):
   - Ler `Desktop/SANOLOGIA OBSIDIAN/<Produto>.md`
   - Match parcial do termo informado contra a coluna "Ângulo" da planilha-mestre (case-insensitive, palavra parcial). Ex: "diabetes" → linha "diabetes + metformina" → slug `diabetes-metformina`
   - Se match único → rodar `/sano-criativos <Produto> <slug>` direto
   - Se match ambíguo (mais de 1 funil casa) → listar os ângulos que casaram e perguntar qual

2. **Só produto, sem ângulo** (ex: "gera os criativos do B12"):
   - Ler `<Produto>.md` no vault
   - Listar todos os funis (linhas da planilha) com a coluna Criativo == `—`
   - Perguntar **simples**: "Qual funil? <opções>"
   - **NÃO** rodar todos automaticamente (cada run custa $1.20+ e exige aprovação visual de 4 amostras)

3. **Produto não existe ou não tem planilha**:
   - Avisar e parar

**Why:** o usuário não quer ter que lembrar do slug exato nem digitar o comando completo. "Gera os criativos do B12 diabetes" deve ser linguagem natural suficiente. Salvo após ele dizer literalmente em 30/04/2026: "eu posso te falar: gera os criativos do B12 Diabetes! Se eu não falar qual é o Slug ou aproximadamente o Slug, você só pergunta. Bem simples."

**How to apply:** essa frase ("gera/gere/cria os criativos de/do/pra <produto> [<termo>]") é gatilho 1:1 pro skill `/sano-criativos`. Não fazer auto-discovery além do match na planilha — confiar no Obsidian como fonte de verdade dos funis disponíveis. Se planilha-mestre não tem o produto, é porque ainda não foi criado (rodar `/sano-novo-funil` antes).

Produtos válidos hoje no vault (30/04/2026): **B12** (`B12.md`), **StrongBones** (`StrongBones.md`), **GlowUp** (`GlowUp.md`).
