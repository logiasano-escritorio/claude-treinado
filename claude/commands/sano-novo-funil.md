---
description: Pipeline completo Sano — clona advertorial + página de produto pra um ângulo novo, gera imagens via Gemini, faz deploy
argument-hint: <produto> <#angulo-do-catalogo>
---

# Novo Funil Sano — Pipeline Completo

Você vai executar o pipeline completo de criação de funil Sano que foi validado manualmente. **Faça TUDO sem perguntar — exceto se algo crítico estiver ambíguo.**

## Argumentos

`$ARGUMENTS` no formato: `<produto> <#angulo>`

Exemplos:
- `B12 1` → B12 ângulo #1 (Diabetes + Metformina)
- `StrongBones 11` → StrongBones #11 (Artrose / Osteoartrite)
- `GlowUp 3` → GlowUp #3 (Pós-parto)

Se o usuário não passou número de ângulo, **leia o catálogo e pergunte qual ângulo escolher** mostrando a lista numerada.

---

## Etapa 0 — VERIFICAÇÃO (antes de qualquer coisa)

### 0.1 Slug do ângulo
Defina `<slug>` em kebab-case sem acento. Exemplos: `artrose`, `diabetes-metformina`, `pos-parto`, `cabelo-sem-brilho`.

### 0.2 Checar duplicata
```bash
cd "c:/Users/user/Desktop/Sanologia"
ls adv-<produto-lower>-<slug>.html 2>/dev/null && echo "JÁ EXISTE — abortar ou sobrescrever?"
```
Se existir, **PARE e pergunte** ao usuário se quer sobrescrever (vai regerar imagens, gasta $0.60 de novo). Só siga se ele confirmar.

### 0.3 Forçar email correto do git (não só verificar)
```bash
cd "c:/Users/user/Desktop/Sanologia"
git config user.email "reliviabrasil@gmail.com"
git config user.name "Relívia"
```
Sempre rodar — não basta checar, força-setar pra evitar bloqueio silencioso de deploy Vercel.

### 0.4 Checar se outro processo git está ativo
```bash
ls "c:/Users/user/Desktop/Sanologia/.git/index.lock" 2>/dev/null
```
**Se EXISTIR:** outro chat/processo está commitando em paralelo. **NÃO REMOVA o lock** — espere ~30s e tente de novo. Se persistir após 2min, avise o usuário antes de remover (risco de perder staging de outro processo).

---

## Etapa 1 — INTELIGÊNCIA: ler o catálogo

Leia `C:/projetos/relivia/sano-energy-b12/CATALOGO-COPIES.md` e identifique:
- Mecanismo central do ângulo escolhido
- Persona / paciente exemplo (se já estiver na copy detalhada)
- Tier de prioridade

Em seguida abra o arquivo de copy detalhada do produto:
- B12: `C:/projetos/relivia/sano-energy-b12/copies-facebook-ads.txt`
- StrongBones: `C:/projetos/relivia/sano-energy-b12/strongbones-copies-17-angulos.txt`
- GlowUp: `C:/projetos/relivia/sano-energy-b12/glowup-copies-10-angulos.txt`

Encontre a copy específica do ângulo (procure por "COPY <NN>" ou "ANGULO <NN>"). Use isso como base de conteúdo.

---

## Etapa 2 — CLONAGEM: criar HTMLs

### Arquivos de referência (clone byte-por-byte)

| Produto | SKU checkout | Adv referência | Página referência | Convenção nome página nova |
|---|---|---|---|---|
| B12 | `energy-b12` | `Sanologia/adv-b12-omeprazol-b12.html` | `Sanologia/b12/b12-v2.html` | `b12-<slug>.html` (raiz) |
| StrongBones | `strongbones` | `Sanologia/adv-strongbones-caimbras.html` | `Sanologia/strongbones.html` | `strongbones-<slug>.html` (raiz) |
| GlowUp | `glowup` | `Sanologia/adv-glowup-40mais.html` | `Sanologia/pag-glowup.html` | `pag-glowup-<slug>.html` (raiz, prefixo `pag-` por convenção histórica) |

> **Por que GlowUp tem prefixo `pag-`?** Foi a convenção do primeiro funil GlowUp (`pag-glowup.html`). Mantemos pra não quebrar histórico Vercel/UTMs já rodando. B12 e StrongBones nunca tiveram esse prefixo.

### Procedimento

1. `cp` do adv referência para `adv-<produto-lower>-<slug>.html`
2. `cp` da página referência para o nome da convenção (vide tabela acima)
3. **Editar os 2 arquivos** trocando APENAS:
   - `<title>` e `<meta description>`
   - H1 e subtítulo
   - Nome do especialista (manter regra Relívia: especialistas SEMPRE masculinos. Ex: Dr. Hélio Rocha, Dr. Fernando Leite, Dr. Eduardo Sampaio, Dr. Marcos Aurélio)
   - Persona (nome, idade, cidade)
   - Cada bloco de copy do corpo
   - Comentários do leitor no advertorial (geralmente 5)
   - **TODOS os comentários estilo Facebook** que existirem na página de produto — quantidade varia por produto:
     - B12: ~22 comentários
     - GlowUp: ~23 comentários
     - StrongBones: ~29 comentários
     - **Conte com `grep -c 'fb-comment\b' <arquivo>` antes de começar pra saber quantos**
   - Stats e percentuais (ajustar pro contexto do ângulo)
   - Tabela comparativa (concorrentes adequados ao ângulo)
   - Timeline de semanas
   - FAQ
   - CTA final
4. **NÃO TOQUE em:**
   - CSS (linhas iniciais até `<body>`)
   - Scripts
   - Galeria de produto (8 packshots)
   - Avatars de depoimento (`randomuser.me`)
   - Logos, ícones SVG, selos
   - Footer + garantia + variant cards + checkout URL

### Imagens — substituir por placeholder com nome FINAL já

⚠️ **CRÍTICO:** o nome do placeholder deve ser **idêntico ao nome final** que o Gemini vai gerar. Assim a substituição depois é automática e zero erro.

Formato do placeholder (mesmo nome em adv + página + JSON Gemini):

```html
<!-- No advertorial (path relativo) -->
<img src="<produto-lower>/images/generated/<slug>/NN-tema.png"
     alt="<descrição PT-BR curta>"
     data-prompt-gemini="<prompt EN com paleta navy #1e3a8a + branco + dourado #d4af37, no text, hyperrealistic>"
     data-tamanho="1024x1024">

<!-- Na página de produto (path absoluto, com / inicial) -->
<img src="/<produto-lower>/images/generated/<slug>/NN-tema.png"
     alt="<descrição PT-BR curta>"
     data-prompt-gemini="<prompt EN>"
     data-tamanho="1024x1024">
```

**Padronização de paths:**
- Advertorial: `<produto-lower>/images/generated/<slug>/NN-tema.png` (relativo)
- Página de produto: `/<produto-lower>/images/generated/<slug>/NN-tema.png` (absoluto, com `/` inicial)

> Por que a diferença? Adv mora em `/Sanologia/adv-<...>.html` (raiz), página também (`/Sanologia/<produto>-<slug>.html`). Mas a página historicamente usa path absoluto. Mantenha — está em produção assim.

**Quantidade de placeholders:** ajuste conforme complexidade do ângulo. Faixa típica: **12 a 18 totais**. Não force 15 se não precisa, não corte pra 7 se o mecanismo precisa de mais ilustração.

`NN` é numeração sequencial (01, 02, 03...) começando do advertorial e continuando na página.

`<tema>` é kebab-case curto identificando a imagem (ex: `especialista`, `hero-joelho`, `mecanismo-osso-subcondral`).

### Compliance

- ZERO menção de preço no advertorial (preço só na página + checkout)
- Sem "cura/trata/elimina" — usar "suporte nutricional", "matéria-prima", "modula"
- Disclaimer "não substitui o reumatologista/médico"
- CTA aponta pra `https://pagamento.reliviaonline.com/sano-<sku>` (vide tabela acima)
- Texto branco em fundo azul escuro (regra mobile/design Relívia — `.product-box`, `.cta-final`, `footer`)

---

## Etapa 3 — EXECUÇÃO: imagens + deploy

### 3.1 Criar JSON de prompts

Crie `c:/Users/user/Desktop/Sanologia/prompts/<produto-lower>-<slug>.json` no formato exato dos JSONs existentes (vide `prompts/strongbones-artrose.json` como modelo).

⚠️ **CRÍTICO:** o `tema` de cada bloco do JSON DEVE ser **idêntico** ao `<tema>` usado no nome do placeholder no HTML. O Gemini vai gerar arquivo `NN-<tema>.png` — esse nome tem que casar com `src` dos `<img>` que você colocou nos HTMLs.

```json
{
  "id": 1,
  "tema": "especialista",      // ← bate com NN-especialista.png nos HTMLs
  "trecho_copy": "...",
  "emocao": "...",
  "elemento_tecnico": "...",
  "ideia_visual": "...",
  "elemento_choque": "...",
  "prompt": "<prompt EN com paleta navy + branco + dourado>",
  "tamanho": "1024x1024"
}
```

### 3.2 Rodar Gemini (em background)

```bash
cd "c:/Users/user/Desktop/Sanologia" && node gerar-imagens-gemini.js prompts/<produto-lower>-<slug>.json
```

**Rode em background** (`run_in_background: true`). Você será notificado quando terminar (~5min pra 15 imagens, custo ~$0.60).

**Enquanto espera:** confira o HTML — releia copy, ajuste depoimentos, valide tabela comparativa. Não fique parado.

### 3.3 Mover imagens pro path padrão

Imagens saem em `images/_generated/<produto-lower>-<slug>/NN-tema.png`. Mova:

```bash
cd "c:/Users/user/Desktop/Sanologia"
mkdir -p "<produto-lower>/images/generated/<slug>"
mv "images/_generated/<produto-lower>-<slug>/"*.png "<produto-lower>/images/generated/<slug>/"
rmdir "images/_generated/<produto-lower>-<slug>" 2>/dev/null
```

### 3.4 Verificar que não tem placeholder quebrado

Como os `src` dos HTMLs já estão apontando pro caminho final desde a Etapa 2, **não precisa fazer `sed`**. Só conferir:

```bash
cd "c:/Users/user/Desktop/Sanologia"
# Verificar se todas as imagens referenciadas existem
grep -oE "<produto-lower>/images/generated/<slug>/[0-9]+-[a-z0-9-]+\.png" \
  adv-<produto-lower>-<slug>.html <página-do-produto>.html | sort -u
ls <produto-lower>/images/generated/<slug>/
```
As listas devem bater. Se algum src referencia imagem que não foi gerada, fazer Edit manual no HTML.

### 3.5 Deploy

```bash
cd "c:/Users/user/Desktop/Sanologia"

# 1. Confirmar que NÃO existe lock de outro processo
ls .git/index.lock 2>/dev/null && echo "⚠️ ESPERAR — outro chat commitando" && exit 1

# 2. Verificar status atual
git status --porcelain | head -20

# 3. Stage SÓ os arquivos do funil novo (cirúrgico)
git add adv-<produto-lower>-<slug>.html \
        <página-do-produto>.html \
        prompts/<produto-lower>-<slug>.json \
        <produto-lower>/images/generated/<slug>/

# 4. Verificar staging
git diff --cached --name-only

# 5. Commit + push
git commit -m "feat(<produto-lower>): novo funil ângulo <slug>"
git push
```

Vercel detecta push e deploya em ~30s.

### 3.6 Verificar produção (NÃO atualize Obsidian antes disso)

```bash
sleep 45  # espera Vercel deployar
curl -sI https://sanobrasil.com/adv-<produto-lower>-<slug> | head -3
curl -sI https://sanobrasil.com/<página-do-produto-sem-html> | head -3
```

**AMBAS devem retornar `HTTP/1.1 200 OK`.** Se uma der 404, **PARE** — algo deu errado no deploy. Investigue antes de seguir.

### 3.7 Atualizar planilha Obsidian (SÓ depois do 200 OK confirmado)

Edite `c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/<Produto>.md` adicionando linha na tabela "Funis":

```
| N | 🟢 | <slug> | https://sanobrasil.com/adv-<produto-lower>-<slug> | https://sanobrasil.com/<página-sem-html> | https://pagamento.reliviaonline.com/sano-<sku> | — | no ar — N imgs Gemini, deploy <DD/MM> |
```

> Marca 🟢 **só depois do `curl 200 OK` confirmado**. Se algum endpoint não respondeu 200, marca 🔵 (em teste) com nota explicando o que falhou — nunca 🟢 sem confirmação.

---

## Output final pro usuário

Quando terminar, mostre:
- ✅ Funil deployado e respondendo 200 OK
- 🔗 URLs ativas (adv + página) clicáveis
- 💰 Custo Gemini gasto (~$0.60 por 15 imagens)
- 📊 Linha adicionada na planilha Obsidian
- ⏭️ Próximo ângulo sugerido do catálogo (mesma prioridade Tier ou próximo da lista 127 do CATALOGO-COPIES.md)

---

## Regras importantes

- **Use o catálogo, não invente ângulo.** Se não tem no `CATALOGO-COPIES.md`, peça pro usuário escolher um existente.
- **Especialista SEMPRE homem** (regra Relívia).
- **Nunca preço no advertorial.**
- **Domínio é `sanobrasil.com`** (não `sano-v2.vercel.app`).
- **Email do git: `reliviabrasil@gmail.com`** (force-set sempre antes de commit).
- **CSS/JS intactos.** Bate na cara se for tentado a "melhorar" alguma coisa.
- **Texto branco em fundo azul escuro** (`.product-box`, `.cta-final`, `footer`).
- **Placeholder = nome final já.** Nunca mais use formato `placeholder-XXX-NN.png` que requer `sed` posterior.
- **Marca 🟢 só com `curl 200 OK` confirmado.**
- **Nunca remova `.git/index.lock`** sem antes esperar 2min e avisar o usuário.
- Use TodoWrite pra trackar as 3 etapas (+ Etapa 0 de verificação).

Comece agora pelo ângulo: **$ARGUMENTS**
