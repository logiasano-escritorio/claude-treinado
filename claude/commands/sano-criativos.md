---
description: Gera 30 criativos Facebook Ads pra um funil Sano (15 estilo jornalístico com texto integrado + 15 estilo cena pura sem texto). Usa megaprompt embutido — não depende de imagem-referência. Chama Copy Master pra hooks, gera via Gemini Flash Image
argument-hint: <produto> <slug-funil>
---

# Gerador de 30 Criativos Sano (Facebook Ads)

`$ARGUMENTS` no formato: `<produto> <slug-funil>`

Exemplos:
- `StrongBones artrose` → 30 criativos
- `B12 diabetes-metformina` → 30 criativos
- `GlowUp pos-parto` → 30 criativos

Se não passou os 2 args, pergunte qual funil. Liste os disponíveis lendo o vault Obsidian.

---

## ⚠️ MÉTODO — IMPORTANTE LER

Esse comando usa **megaprompts auto-suficientes** — o Gemini gera do zero seguindo regras escritas, sem precisar de imagem de referência (mais barato, mais rápido, sem dependência de arquivo local).

Os megaprompts traduzem em texto **toda a identidade visual** que estaria numa imagem-template:
- Aspect ratio
- Paleta de cor (com hex codes)
- Tipografia (peso, alinhamento, hierarquia)
- Estrutura de layout (faixa preta, posição do texto)
- Estilo fotográfico (editorial photorealistic, não stock)

**Há 2 megaprompts (1 por estilo).** Cada hook recebe o megaprompt do seu estilo + variáveis específicas (cena, headline, subheadline).

---

## Etapa 0 — Verificações

### 0.1 Confirmar funil existe
```bash
cd "c:/Users/user/Desktop/Sanologia"
ls adv-<produto-lower>-<slug>.html 2>/dev/null || echo "FUNIL NÃO EXISTE — rodar /sano-novo-funil <Produto> <#> primeiro"
```
Se não existe, **PARE** e sugira `/sano-novo-funil`.

### 0.2 Output dir
```bash
OUT="c:/Users/user/Desktop/_Projetos/relivia-editor/outputs_sano/<produto-lower>/<slug>"
mkdir -p "$OUT"
```

### 0.3 Skip se já existe
Se `$OUT/criativo_30_*.png` já existir, **PARE** e pergunte se quer regerar (~$1.20).

---

## Etapa 1 — INTELIGÊNCIA: extrair hooks via Copy Master

Use a Task tool com `subagent_type: "general-purpose"` chamando os agentes do Copy Master via Skill (ou diretamente).

**Recomendação:** chame em paralelo `copy-master:agents:gary-halbert` e `copy-master:agents:evaldo-albuquerque`. Halbert traz hooks de venda direta tipo FB Ads. Evaldo traz copy popular brasileira.

**Prompt do sub-agente:**

```
Você é Gary Halbert + Evaldo Albuquerque escrevendo 30 hooks de Facebook Ads
pro produto Sano <produto> no ângulo "<slug>".

LEIA antes de escrever:
- c:/Users/user/Desktop/Sanologia/adv-<produto-lower>-<slug>.html
- c:/Users/user/Desktop/Sanologia/<página-do-produto>.html
- C:/projetos/relivia/sano-energy-b12/CATALOGO-COPIES.md (entrada do ângulo)

EXTRAIA:
- Dor central
- Mecanismo único proprietário (ex: "osso subcondral", "metilcobalamina ativa")
- Persona/paciente (nome BR, idade, cidade)
- Transformação (antes → depois sutil)
- Prova social numérica
- 3 maiores objeções

GERE 30 HOOKS, divididos em 6 BLOCOS de 5:

B1 — ESPELHO DE DOR — cena íntima da dor cotidiana, "quiet recognition"
B2 — INCONGRUÊNCIA CIENTÍFICA — macro/diagrama do problema oculto
B3 — PATTERN INTERRUPT EMOCIONAL — cena que para o scroll
B4 — ANTES/DEPOIS IMPLÍCITO — sutil, não-Hollywood
B5 — CREDIBILIDADE — médico, jornal, produto macro
B6 — URGÊNCIA SILENCIOSA — "isso está acontecendo agora"

DISTRIBUIÇÃO ESTILO (15 A + 15 B):
- B1 (5 hooks) → Estilo A (texto integrado)
- B2 (5 hooks) → Estilo B (cena pura, científica)
- B3 (5 hooks) → Estilo A
- B4 (5 hooks) → Estilo A
- B5 (5 hooks) → Estilo B (cena pura, médica/produto)
- B6 (5 hooks) → Estilo B (cena pura, urgência visual)

Pode ajustar 1-2 se um hook específico funcionar melhor no outro estilo.

PARA CADA HOOK, JSON:
{
  "id": "NN_bloco_tema",       // ex: "01_espelho_escritorio"
  "bloco": "B1-Espelho-de-Dor",
  "estilo": "A" ou "B",
  "cena_visual": "<descrição cinematográfica EM INGLÊS — pessoa BR, ação, ambiente, expressão, lighting, framing, ~50-80 palavras>",
  "headline": "<6-12 PALAVRAS UPPERCASE BOLD em PT-BR>",       // só Estilo A
  "subheadline": "<frase explicativa branca menor em PT-BR>",  // só Estilo A
  "racional": "<por que esse hook converte — 1 linha>"
}

REGRAS DE COPY:
- Headline UPPERCASE BOLD (vai virar amarelo #FFC700 na imagem)
- Sem "cura/trata/elimina" (Anvisa)
- Persona Brasil (nome brasileiro, cidade BR real)
- Especialista SEMPRE homem (Dr. fulano)
- Tom íntimo, documental, NÃO Hollywood
- Cena visual em inglês (Gemini funciona melhor com EN), copy dos textos em PT-BR

OUTPUT: array JSON com 30 itens, salve em
c:/Users/user/Desktop/_Projetos/relivia-editor/outputs_sano/<produto-lower>/<slug>/hooks.json
```

Espere terminar. Confirme que `hooks.json` tem 30 entradas válidas (15 estilo A + 15 estilo B).

---

## Etapa 2 — GERAÇÃO via Gemini com megaprompts embutidos

### 2.1 Criar script Python

Crie `c:/Users/user/Desktop/_Projetos/relivia-editor/gerar_sano_<produto-lower>_<slug>.py`:

```python
import requests, json, base64, os, time, threading
from pathlib import Path

# Lê API key do .env do projeto Sanologia
ENV = open("c:/Users/user/Desktop/Sanologia/.env").read()
GOOGLE_KEY = [l.split("=",1)[1].strip().strip('"\'') for l in ENV.split("\n") if l.startswith("GEMINI_API_KEY")][0]

MODEL = "gemini-3.1-flash-image-preview"
OUTPUT_DIR = Path("c:/Users/user/Desktop/_Projetos/relivia-editor/outputs_sano/<produto-lower>/<slug>")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_DIR / "hooks.json", encoding="utf-8") as f:
    HOOKS = json.load(f)

URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GOOGLE_KEY}"

# ===== MEGAPROMPT ESTILO A (jornalístico, texto integrado) =====
MEGAPROMPT_A = """You are generating a Brazilian Facebook Ads creative.

CRITICAL OUTPUT SPECIFICATIONS — follow EXACTLY:

ASPECT RATIO: vertical 4:5 (1080x1350px) — Facebook feed format.

LAYOUT (top to bottom):
- TOP 70% of frame: photographic SCENE (described below)
- BOTTOM 30% of frame: solid black bar (#000000) covering full width
  - Inside the black bar, top portion: HEADLINE in YELLOW (#FFC700), bold, uppercase, sans-serif font (Impact / Anton / Bebas Neue style), centered, large size, 6-12 words, 2 lines maximum
  - Inside the black bar, bottom portion: SUBHEADLINE in WHITE (#FFFFFF), regular weight, smaller size, centered, 1-2 lines

PHOTOGRAPHIC STYLE OF THE SCENE:
- Editorial photography quality, like Magnum or Reuters photojournalism
- Photorealistic, NOT stock photo, NOT illustration
- Natural lighting (warm afternoon / soft window / clinical depending on context)
- Shallow depth of field where appropriate
- Real Brazilian person — olive skin, dark hair, age and details as specified
- Emotion is ALWAYS quiet, contained, intimate — NEVER dramatic, NEVER Hollywood, NEVER smiling for camera
- No filters, no retouching that looks fake
- Canon 5D / Sony A7 quality

TEXT RENDERING (CRITICAL):
- Both headline (yellow) and subheadline (white) must be rendered cleanly INSIDE the image
- Text must be in BRAZILIAN PORTUGUESE
- No spelling errors
- No additional text anywhere else (no watermark, no logo, no caption)

COPY (this specific creative):
- HEADLINE (yellow #FFC700, bold uppercase): "{headline}"
- SUBHEADLINE (white): "{subheadline}"

SCENE (top 70% photographic area):
{cena_visual}

Generate the final composed creative as a single image: photographic scene on top + black bar with yellow headline + white subheadline at the bottom. The black bar is part of the SAME image, not a separate overlay."""

# ===== MEGAPROMPT ESTILO B (cena pura, sem texto) =====
MEGAPROMPT_B = """You are generating a Brazilian Facebook Ads creative — pure scene style, NO TEXT.

CRITICAL OUTPUT SPECIFICATIONS:

ASPECT RATIO: vertical 4:5 (1080x1350px) — Facebook feed format. Or square 1:1 if scene composition needs it.

PHOTOGRAPHIC STYLE:
- Editorial photography quality, like a National Geographic / The Atlantic / scientific journal cover
- Photorealistic, NOT stock photo, NOT illustration unless the scene specifically calls for medical/scientific 3D render
- For HUMAN scenes: real Brazilian person, olive skin, natural details, intimate framing, emotion quiet and contained, never dramatic
- For SCIENTIFIC/MACRO scenes: clinical lighting, slight blue tint, medical-grade detail, looks like a real microscopy or 3D medical render
- Composition stops the scroll because the IMAGE itself is striking — NOT because of text

ABSOLUTE RULE — NO TEXT WHATSOEVER:
- No headline, no caption, no subheadline, no watermark, no logo, no number, no brand name
- No black bar, no yellow text, nothing
- The image must work as pure visual storytelling
- This is the scene only

SCENE:
{cena_visual}

Generate the final image as a pure photographic / photorealistic scene with absolutely no text overlay or rendered text inside the image."""

# ===== BUILD PROMPT POR HOOK =====
def build_prompt(hook):
    if hook["estilo"] == "A":
        return MEGAPROMPT_A.format(
            cena_visual=hook["cena_visual"],
            headline=hook["headline"],
            subheadline=hook["subheadline"]
        )
    else:
        return MEGAPROMPT_B.format(cena_visual=hook["cena_visual"])

# ===== GERAÇÃO =====
def gerar(hook):
    out = OUTPUT_DIR / f"criativo_{hook['id']}.png"
    if out.exists():
        return "skip"

    prompt = build_prompt(hook)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
    }

    for tentativa in range(2):
        try:
            r = requests.post(URL, json=payload, timeout=120)
            d = r.json()
            parts = d.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            img_part = next((p for p in parts if "inlineData" in p), None)
            if img_part:
                img_data = base64.b64decode(img_part["inlineData"]["data"])
                with open(out, "wb") as f:
                    f.write(img_data)
                return "ok"
            time.sleep(2)
        except Exception as e:
            print(f"erro {hook['id']}: {e}")
            time.sleep(3)
    return "fail"

# ===== 3 WORKERS PARALELOS =====
queue = list(HOOKS)
lock = threading.Lock()
stats = {"ok": 0, "fail": 0, "skip": 0}

def worker(wid):
    while True:
        with lock:
            if not queue: return
            item = queue.pop(0)
        result = gerar(item)
        with lock:
            stats[result] += 1
        print(f"[W{wid}] {item['id']} ({item['estilo']}) → {result}")
        time.sleep(1)

threads = [threading.Thread(target=worker, args=(w,), daemon=True) for w in range(1, 4)]
for t in threads:
    t.start()
    time.sleep(0.5)
for t in threads:
    t.join()

print(f"\n✅ {stats['ok']}/30  ⏭️ {stats['skip']}  ❌ {stats['fail']}")
print(f"Output: {OUTPUT_DIR}")
print(f"Custo: ~${stats['ok'] * 0.04:.2f}")
```

### 2.2 Rodar em background

```bash
cd "c:/Users/user/Desktop/_Projetos/relivia-editor"
python gerar_sano_<produto-lower>_<slug>.py
```

`run_in_background: true`. Tempo: ~6min pra 30 imagens. Custo: ~$1.20.

Enquanto roda, escreva a documentação da Etapa 4.

---

## Etapa 3 — Validação

```bash
ls "c:/Users/user/Desktop/_Projetos/relivia-editor/outputs_sano/<produto-lower>/<slug>/"*.png | wc -l
```

Tem que retornar 30. Se faltou, rerode o script (skip dos existentes).

Mostre 2-3 imagens de exemplo via Read pro usuário validar:
- 1 do Estilo A (com texto)
- 1 do Estilo B (cena pura)
- 1 do bloco mais forte (B5 Credibilidade ou B3 Pattern Interrupt)

**Verifique no resultado:**
- Estilo A: tem faixa preta + headline amarelo + subheadline branco? Texto em PT-BR sem erro de digitação?
- Estilo B: zero texto na imagem?

Se algum criativo saiu errado (Gemini às vezes ignora a regra do "no text"), peça pro usuário aprovar regerar só o que falhou.

---

## Etapa 4 — Documentação no Obsidian (CATÁLOGO VISUAL)

Objetivo: deixar tudo organizado pra depois rodar Cloud Code falando "sobe essa estrutura aqui da planilha" — a nota Criativos serve de manifest.

### 4.1 Copiar 30 PNGs + hooks.json pro vault

```bash
mkdir -p "c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/Criativos/<produto-lower>-<slug>"
cp "c:/Users/user/Desktop/_Projetos/relivia-editor/outputs_sano/<produto-lower>/<slug>/"criativo_*.png \
   "c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/Criativos/<produto-lower>-<slug>/"
cp "c:/Users/user/Desktop/_Projetos/relivia-editor/outputs_sano/<produto-lower>/<slug>/hooks.json" \
   "c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/Criativos/<produto-lower>-<slug>/"
```

Por que copiar: Obsidian renderiza preview nativamente, vault fica autocontido, Cloud Code lê tudo de uma pasta única sem cruzar `_Projetos`.

### 4.2 Atualizar coluna "Criativo" na planilha-mestre

`c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/<Produto>.md` — coluna Criativo da linha do funil vira **1 link só**:

```
[[Criativos/<produto-lower>-<slug>|30 imgs ✓]]
```

Limpo. Tudo o que importa tá dentro da nota.

### 4.3 Criar a nota Criativos como CATÁLOGO VISUAL

Caminho: `c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/Criativos/<produto-lower>-<slug>.md`

```markdown
---
produto: <Produto Completo>
sku: <produto-lower>
funil: <slug>
quantidade: 30
estilo-A-manchete-cientifica: 15
estilo-B-cena-pura: 15
advertorial-url: https://sanobrasil.com/adv-<produto-lower>-<slug>
pagina-url: https://sanobrasil.com/<slug-pagina>
checkout-url: https://pagamento.reliviaonline.com/sano-<produto-lower>
pasta-criativos: SANOLOGIA OBSIDIAN/Criativos/<produto-lower>-<slug>/
data-geracao: <YYYY-MM-DD>
custo-gemini: $X.XX
cssclasses:
  - wide-page
---

# 🎨 Criativos — <Produto> / <slug>

## 🚀 Para subir campanha (resumo Cloud Code)

| Campo                | Valor                                         |
| -------------------- | --------------------------------------------- |
| **Produto**          | <Produto>                                     |
| **Funil**            | <slug + ângulo>                               |
| **Advertorial**      | <url advertorial>                             |
| **Página produto**   | <url pagina>                                  |
| **Checkout**         | <url checkout>                                |
| **Pasta criativos**  | `SANOLOGIA OBSIDIAN/Criativos/<...>/`         |
| **Total criativos**  | 30 PNGs (15 Estilo A · 15 Estilo B)           |
| **URL destino dos ads** | <url advertorial>                          |

---

## 🎯 Estratégia recomendada
- **Estilo A — Manchete Científica (15 imgs)** → público frio/topo de funil.
- **Estilo B — Cena Pura sem texto (15 imgs)** → remarketing e variação criativa.
Sugestão: 2 ad sets (1 por estilo), 6 criativos iniciais por ad set.

---

## 🅰️ ESTILO A — Manchete Científica (15 imagens)

| ID | Preview | Headline | Subheadline | Racional |
| -- | ------- | -------- | ----------- | -------- |
| 01 | ![](<produto-lower>-<slug>/criativo_01_<...>.png) | **<HEADLINE>** | <subheadline> | <racional> |
| ... |

## 🅱️ ESTILO B — Cena Pura sem texto (15 imagens)

| ID | Preview | Bloco | Tema visual | Racional |
| -- | ------- | ----- | ----------- | -------- |
| 06 | ![](<produto-lower>-<slug>/criativo_06_<...>.png) | B2 Incongruência | <tema> | <racional> |
| ... |

---

## 📂 Arquivos físicos

- **PNGs:** `SANOLOGIA OBSIDIAN/Criativos/<produto-lower>-<slug>/criativo_*.png` (30)
- **Hooks JSON:** `SANOLOGIA OBSIDIAN/Criativos/<produto-lower>-<slug>/hooks.json`
- **Origem (build):** `_Projetos/relivia-editor/outputs_sano/<produto-lower>/<slug>/`
- **Script gerador:** `_Projetos/relivia-editor/gerar_sano_<produto-lower>_<slug>.py`

## 📝 Histórico
- <YYYY-MM-DD> — geração inicial via Gemini 3.1 (custo ~$1.20)
```

**Importante na tabela:** o caminho do preview é RELATIVO à nota (`<produto-lower>-<slug>/criativo_XX.png`), não absoluto. Obsidian resolve assim.

---

## Output final pro usuário

- ✅ 30/30 criativos gerados
- 💰 Custo total Gemini (~$1.20)
- 📁 Pasta no vault: `SANOLOGIA OBSIDIAN/Criativos/<produto-lower>-<slug>/`
- 📋 Catálogo visual: `[[Criativos/<produto-lower>-<slug>]]` com frontmatter de URLs + tabela com 30 previews
- 🎨 2-3 imagens de exemplo via Read pra aprovação
- 🚀 Próximo passo: rodar Cloud Code apontando pra essa nota — ele lê frontmatter + tabela e sobe campanha automaticamente

---

## Regras importantes

- **Megaprompt embutido** — NÃO carrega imagem-referência. Tudo está em texto no script.
- **Estilo A — MANCHETE CIENTÍFICA (Wealth-style):** 3D médico macro hyper-realista (osso/cartilagem/articulação), fundo navy/preto, ZERO pessoas. Faixa amarela fina + logo "Sano" serif itálica + headline amarela UPPERCASE GRANDE começando com "CIENTISTAS DESCOBREM..." / "ESTUDO REVELA..." / "PESQUISADORES IDENTIFICAM..." / "NOVA DESCOBERTA..." / "MEDICINA REPENSA..." / "PESQUISA EXPÕE..." / "MITO DESMENTIDO...". Subheadline branca curta opcional. **NÃO use formato depoimento íntimo (rejeitado em StrongBones/artrose 30/04/2026).** Megaprompt v2 calibrado em `_Projetos/relivia-editor/gerar_sano_strongbones_artrose_v2.py`.
- **Estilo B:** ZERO texto. Cena pura. O gancho é a incongruência/cena chocante.
- **15 + 15 = 30.** Não mexa na proporção sem o usuário pedir.
- **Hooks vêm do Copy Master** (Halbert + Evaldo). Não invente do zero — eles leem o advertorial e a página.
- **Cena visual em inglês** (Gemini funciona melhor). Headline e subheadline em PT-BR.
- **Especialista sempre homem** (regra Relívia).
- **Sem "cura/trata/elimina"** (Anvisa) — use "alívio", "mobilidade", "voltar a", "recuperar".
- **Catálogo visual obrigatório (Etapa 4)** — copiar 30 PNGs pro vault Obsidian, criar nota com frontmatter rico (URLs advertorial/página/checkout/pasta) + tabela com 30 previews embedados. Coluna Criativo na planilha-mestre vira só `[[Criativos/<produto>-<slug>|30 imgs ✓]]`.
- Use TodoWrite pra trackar as 4 etapas (0 verificação / 1 hooks via Copy Master / 2 geração Gemini / 3 validação / 4 docs Obsidian: copy PNGs + nota catálogo + planilha).

Comece agora pelo funil: **$ARGUMENTS**
