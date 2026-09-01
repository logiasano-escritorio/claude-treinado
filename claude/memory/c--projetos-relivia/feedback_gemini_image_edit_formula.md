---
name: Fórmula Gemini Image — Edição Perfeita de Embalagem
description: Prompt estrutura + modelo + código Python que gerou resultado perfeito na tradução e recoloração de embalagem de produto (comp_beetroot_main → RELÍVIA PT-BR azul)
type: feedback
originSessionId: b65fe925-8232-4e2e-8a45-fc9c6dae8174
---
## Regra

Usar o modelo `gemini-3.1-flash-image-preview` (não o `gemini-2.5-flash-image`) para edição de texto em embalagens. O modelo mais novo acerta os textos pequenos sem alucinar.

**Why:** Os modelos anteriores (`gemini-2.5-flash-image`, `gemini-2.0-flash-preview-image-generation`) alucinavam nos textos menores da embalagem — inventavam palavras e misturavam inglês/português. O `gemini-3.1-flash-image-preview` seguiu as instruções character by character e gerou resultado perfeito.

**How to apply:** Sempre usar `gemini-3.1-flash-image-preview` para tarefas de substituição de texto em embalagens/rótulos de produto.

---

## Estrutura do prompt que funcionou

O segredo está em 3 elementos combinados:

### 1. Framing cirúrgico + instrução anti-alucinação
```
You are a surgical image editor. Replace text in this bottle image EXACTLY as listed. Copy each replacement character by character — do not invent or alter spelling.
```

### 2. Lista numerada com aspas duplas e seta →
Cada item no formato exato: `"TEXTO ORIGINAL" → "TEXTO TRADUZIDO"`
```
1. "VIRAL ON" → "VIRAL NO"
2. "TikTok" → "TikTok" (unchanged)
3. "Rosabella" → "RELÍVIA"
...
```

### 3. Regra explícita de não improvisar
```
Rules:
- Write ONLY the exact replacement text shown above — no extra words, no paraphrasing
- Preserve font, size, weight, color, position of each text element
- Do NOT translate differently or improvise
```

---

## Código Python completo (template reutilizável)

```python
from google import genai
from google.genai import types
from PIL import Image
import base64, io

API_KEY = "<CHAVE-NO-.env-LOCAL>"
IMAGE_PATH = "caminho/para/imagem.webp"
OUTPUT_PATH = "caminho/para/saida.png"

client = genai.Client(api_key=API_KEY)

image = Image.open(IMAGE_PATH)
buf = io.BytesIO()
image.save(buf, format="PNG")
img_bytes = buf.getvalue()

PROMPT = """You are a surgical image editor. Replace text in this bottle image EXACTLY as listed. Copy each replacement character by character — do not invent or alter spelling.

EXACT TEXT REPLACEMENTS:
1. "TEXTO ORIGINAL" → "TEXTO TRADUZIDO"
2. "OUTRO TEXTO" → "OUTRA TRADUÇÃO"
[... listar todos ...]

Rules:
- Write ONLY the exact replacement text shown above — no extra words, no paraphrasing
- Preserve font, size, weight, color, position of each text element
- Do NOT translate differently or improvise

COLOR: [descrever mudança de cor se necessário]

Return only the edited image."""

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[
        PROMPT,
        types.Part.from_bytes(data=img_bytes, mime_type="image/png")
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"]
    )
)

saved = False
for part in response.candidates[0].content.parts:
    if part.inline_data:
        raw = part.inline_data.data
        if isinstance(raw, str):
            img_bytes_out = base64.b64decode(raw)
        else:
            img_bytes_out = raw
        result_img = Image.open(io.BytesIO(img_bytes_out))
        result_img.save(OUTPUT_PATH)
        print(f"Salvo: {OUTPUT_PATH} — {result_img.size}")
        saved = True
        break
    elif part.text:
        print(f"Texto: {part.text[:200]}")

if not saved:
    print("Nenhuma imagem retornada")
```

---

## Regra: imagem real de produto sempre via Part.from_bytes

Quando o criativo precisa mostrar uma foto real do produto (ex: passo3.webp), SEMPRE enviar o arquivo como `types.Part.from_bytes` no `contents=[]` — nunca descrever a foto em texto no prompt. O Gemini vai gerar uma pessoa/produto diferente se não receber o arquivo real.

```python
with open(PASSO3, "rb") as f:
    passo3_bytes = f.read()
contents = [
    types.Part.from_bytes(data=passo3_bytes, mime_type="image/webp"),
    prompt
]
```

**Why:** Sem a imagem real, o Gemini inventa uma pessoa genérica com um dispositivo de pescoço diferente — não o produto real. Isso gerou 15 criativos errados com produto falso.

**How to apply:** Sempre que o prompt diz "usa a foto fornida" ou "lato destro = foto real", enviar o arquivo junto no contents.

---

## O que NÃO funcionou (evitar)

| Modelo | Problema |
|---|---|
| `gemini-2.0-flash-preview-image-generation` | SDK deprecated, erro de API |
| `gemini-2.5-flash-image` | Alucinava textos menores ("Auxilao Athetic Performa Fisico*") |
| Prompt sem numeração e aspas | Gemini interpretava livremente e traduzia diferente |
| Prompt sem "do not invent" | Misturava inglês e português nos bullets |

---

## Notas técnicas
- Saída limitada a 1024×1024 independente do input (limitação do modelo)
- Para inspecionar textos pequenos: fazer crop + upscale 3x com PIL antes de ler
- Instalação: `pip install google-genai pillow`
