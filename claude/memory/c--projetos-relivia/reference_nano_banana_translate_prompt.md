---
name: Nano Banana — Megaprompt Global de Tradução de Imagens
description: Prompt universal para traduzir/substituir textos em qualquer imagem usando Nano Banana (Gemini Image), incluindo logos, embalagens complexas e tabelas. Inclui bloco de chamada à API do Google.
type: reference
---

## MEGAPROMPT GLOBAL — Tradução/Substituição de Texto em Imagens (Nano Banana)

### PROMPT (colar no Nano Banana ou via API)

```
You are a surgical image text editor. Your ONLY task is to replace text elements in the provided image. You must NOT alter any visual structure, layout, product photography, illustrations, or non-text elements.

---

## STEP 1 — SCAN & CATALOG

Before making any change, mentally catalog EVERY text element in the image:
- Identify each text block (title, subtitle, body, labels, warnings, legal text, UI text, nutritional tables, ingredient lists, barcodes labels, etc.)
- Note the exact font style (serif/sans-serif), weight (bold/regular/light), size (relative to image), color (hex or descriptive), and any decoration (underline, strikethrough, italic, shadow, outline, glow)
- Note position (top-left, center, bottom-right, overlaid on product, curved along packaging, etc.)
- Note whether it is part of a LOGO or a BRAND MARK — if yes, flag it separately

---

## STEP 2 — CLASSIFY EACH TEXT ELEMENT

For each cataloged text, assign one of these categories:

[TRANSLATE] → Regular text that carries meaning and must be translated
[ADAPT] → Text that is part of a logo or brand mark but contains words that need language adaptation (e.g., a tagline inside a logo)
[KEEP] → Proper noun, brand name, product name, model number, certification mark, barcode — do NOT change

---

## STEP 3 — TRANSLATE

Translate all [TRANSLATE] and [ADAPT] elements from [SOURCE LANGUAGE: PORTUGUESE] to [TARGET LANGUAGE: ENGLISH].

Translation rules:
- Translate meaning, not word-for-word — preserve the marketing/commercial tone of the original
- If the original uses ALL CAPS, keep ALL CAPS in translation
- If the original has a line break mid-sentence for layout reasons, try to replicate the same visual line break in the translated version
- Preserve emphasis: if a word was bold or underlined in the original, the equivalent emphasis word must be bold or underlined in the translation
- For packaging: nutritional tables, ingredient lists, warning labels, usage instructions — translate ALL fields, maintaining the same table/list structure

---

## STEP 4 — LOGO ADAPTATION

For any [ADAPT] element inside a logo or brand mark:
- Preserve the logo shape, icon, symbol, and overall visual structure exactly
- Only swap the text portion inside the logo
- Match the original font as closely as possible
- Do not resize or reposition the logo

---

## STEP 5 — RENDER

Apply all translated text back into the image:
- Replace each text element in-place, matching font, size, weight, color, and position precisely
- If the translated text is longer than the original, reduce font size minimally to fit — do not overflow or break layout
- If the translated text is shorter, maintain the same visual weight by keeping the same font size (do not stretch)
- Backgrounds behind text (panels, boxes, gradients) must remain completely untouched

---

## ABSOLUTE CONSTRAINTS

- DO NOT change any photograph, product image, illustration, icon, or graphic element
- DO NOT change any [KEEP] element
- DO NOT add new elements that were not in the original
- DO NOT remove any text element — if you cannot translate it, keep the original
- DO NOT alter image dimensions, crop, or aspect ratio
- The final image must be pixel-for-pixel identical to the original EXCEPT for the translated text

---

## INPUT

Image: [ATTACH IMAGE]
Source language: Portuguese (Brazil)
Target language: English (US)

---

## OUTPUT

Return the edited image with all text translated. No commentary needed — just the image.
```

---

## BLOCO DE CHAMADA À API DO GOOGLE (Nano Banana / Gemini Image)

> Modelo recomendado: `gemini-2.0-flash-preview-image-generation`
> Requer: Google AI Studio API Key → https://aistudio.google.com/apikey

### Python

```python
import google.generativeai as genai
from PIL import Image
import base64, io, requests

# CONFIG
API_KEY = "SUA_API_KEY_AQUI"
IMAGE_PATH = "caminho/para/imagem.png"  # ou URL
SOURCE_LANG = "Portuguese (Brazil)"
TARGET_LANG = "English (US)"

genai.configure(api_key=API_KEY)

PROMPT = """You are a surgical image text editor. Your ONLY task is to replace text elements in the provided image. You must NOT alter any visual structure, layout, product photography, illustrations, or non-text elements.

STEP 1 — SCAN & CATALOG every text element: font style, weight, size, color, position, decoration.
STEP 2 — CLASSIFY each as [TRANSLATE], [ADAPT] (logo taglines), or [KEEP] (brand names, product names, model numbers).
STEP 3 — TRANSLATE all [TRANSLATE] and [ADAPT] from """ + SOURCE_LANG + """ to """ + TARGET_LANG + """. Preserve marketing tone, ALL CAPS, line breaks, bold/underline emphasis. For packaging: translate nutritional tables, ingredient lists, warnings fully.
STEP 4 — LOGO ADAPTATION: preserve logo shape/icon, swap only the text portion, match original font.
STEP 5 — RENDER: replace each text in-place, matching font/size/weight/color/position. If translation is longer, reduce font size minimally. Backgrounds must remain untouched.

ABSOLUTE CONSTRAINTS:
- DO NOT change any photograph, product image, illustration, icon, or graphic element
- DO NOT change [KEEP] elements
- DO NOT add or remove any element
- DO NOT alter image dimensions or aspect ratio
- Final image must be identical to original EXCEPT for translated text

Return the edited image only. No commentary."""

# Carrega imagem
image = Image.open(IMAGE_PATH)

# Chama o modelo
model = genai.GenerativeModel("gemini-2.0-flash-preview-image-generation")
response = model.generate_content(
    [PROMPT, image],
    generation_config=genai.GenerationConfig(response_modalities=["image", "text"])
)

# Salva resultado
for part in response.candidates[0].content.parts:
    if part.inline_data:
        img_data = base64.b64decode(part.inline_data.data)
        result_img = Image.open(io.BytesIO(img_data))
        result_img.save("imagem_traduzida.png")
        print("Imagem salva: imagem_traduzida.png")
        break
```

### Instalação

```bash
pip install google-generativeai pillow
```

### Variáveis a trocar

| Variável | O que é |
|---|---|
| `API_KEY` | Sua chave do Google AI Studio |
| `IMAGE_PATH` | Caminho local da imagem ou URL |
| `SOURCE_LANG` | Idioma de origem |
| `TARGET_LANG` | Idioma de destino |

### Notas
- Para espanhol: `TARGET_LANG = "Spanish (Latin America)"`
- Custo: ~$0.039 por imagem (Gemini 2.0 Flash Image)
- Limite de referência: até 14 imagens por chamada
- Documentação oficial: https://ai.google.dev/gemini-api/docs/image-generation
