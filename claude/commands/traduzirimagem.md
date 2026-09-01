# Traduzir Imagem — Substituição de Texto via Nano Banana

Leia o megaprompt e o bloco de API salvos na memória:
`C:/Users/user/.claude/projects/c--projetos-relivia/memory/reference_nano_banana_translate_prompt.md`

## CONFIGURAÇÃO FIXA (não perguntar ao usuário)

- **API Key Google**: `<CHAVE-NO-.env-LOCAL>`
- **Modelo**: `gemini-2.0-flash-preview-image-generation`
- **IMAGE_PATH**: fornecido pelo usuário no chat como caminho local
- Sempre executar via API automaticamente — não perguntar se o usuário quer usar manual ou API

---

## PASSO 1 — COLETAR IDIOMA DE DESTINO

Se o usuário não informou o idioma junto com o caminho da imagem, pergunte apenas:

> **"Qual o idioma de destino?"**
> 1. 🇺🇸 Inglês (EUA)
> 2. 🇪🇸 Espanhol (América Latina)
> 3. 🇬🇧 Inglês (Reino Unido)
> 4. 🇵🇹 Português (Portugal)
> 5. Outro — especifique

Se o usuário já informou o idioma junto ao caminho, pule direto para o Passo 2.

---

## PASSO 2 — ANALISAR A IMAGEM

1. Leia a imagem com o Read tool (caminho local)
2. Catalogue todos os elementos de texto visíveis:
   - Título, subtítulo, corpo de texto
   - Textos em embalagens (tabela nutricional, ingredientes, instruções, alertas legais)
   - Textos dentro de logos ou marcas
   - Labels, badges, tags, botões

3. Classifique cada elemento:
   - **[TRANSLATE]** — texto comum que deve ser traduzido
   - **[ADAPT]** — texto dentro de logo/marca que precisa de adaptação de idioma
   - **[KEEP]** — nome de marca, produto, modelo, número, certificação — NÃO traduzir

4. Exiba o catálogo para o usuário confirmar:
```
ELEMENTOS ENCONTRADOS:
[TRANSLATE] "Texto original" → "Tradução proposta"
[KEEP] "NomeDaMarca" → mantido
[ADAPT] "tagline do logo" → "tagline traduzida"
```

Aguarde confirmação ou correções antes de prosseguir.

---

## PASSO 3 — EXECUTAR VIA API

Após confirmação do usuário, execute o script Python abaixo diretamente:

```python
import google.generativeai as genai
from PIL import Image
import base64, io, os

API_KEY = "<CHAVE-NO-.env-LOCAL>"
IMAGE_PATH = "[SUBSTITUIR PELO CAMINHO FORNECIDO]"
SOURCE_LANG = "[IDIOMA DETECTADO]"
TARGET_LANG = "[IDIOMA DE DESTINO]"

# Mapeamento de sufixo por idioma
LANG_SUFFIX = {
    "English (US)": "en",
    "Spanish (Latin America)": "es",
    "English (UK)": "en-uk",
    "Portuguese (Portugal)": "pt-pt",
}
suffix = LANG_SUFFIX.get(TARGET_LANG, "translated")

genai.configure(api_key=API_KEY)

PROMPT = """You are a surgical image text editor. Your ONLY task is to replace text elements in the provided image. You must NOT alter any visual structure, layout, product photography, illustrations, or non-text elements.

STEP 1 — Catalog every text element: font style, weight, size, color, position, decoration.
STEP 2 — Classify each as [TRANSLATE], [ADAPT] (logo taglines), or [KEEP] (brand names, product names, model numbers).
STEP 3 — Translate all [TRANSLATE] and [ADAPT] from """ + SOURCE_LANG + """ to """ + TARGET_LANG + """.
Rules:
- Preserve marketing tone, ALL CAPS, line breaks, bold/underline emphasis
- For packaging: translate nutritional tables, ingredient lists, warnings fully maintaining structure
STEP 4 — LOGO ADAPTATION: preserve logo shape/icon exactly, swap only the text portion, match original font.
STEP 5 — RENDER: replace each text in-place, matching font/size/weight/color/position exactly.
- If translation is longer, reduce font size minimally to fit — never overflow layout
- Backgrounds behind text must remain completely untouched

TRANSLATED ELEMENTS (apply exactly as listed):
[CATALOG_BLOCK]

ABSOLUTE CONSTRAINTS:
- DO NOT change any photograph, product image, illustration, icon, or graphic element
- DO NOT change [KEEP] elements
- DO NOT add or remove any element
- DO NOT alter image dimensions or aspect ratio
- Final image must be identical to original EXCEPT for the translated text

Return the edited image only. No commentary."""

image = Image.open(IMAGE_PATH)
model = genai.GenerativeModel("gemini-2.0-flash-preview-image-generation")
response = model.generate_content(
    [PROMPT, image],
    generation_config=genai.GenerationConfig(response_modalities=["image", "text"])
)

# Salvar resultado
base, ext = os.path.splitext(IMAGE_PATH)
output_path = f"{base}-{suffix}{ext}"
counter = 2
while os.path.exists(output_path):
    output_path = f"{base}-{suffix}-{counter}{ext}"
    counter += 1

for part in response.candidates[0].content.parts:
    if part.inline_data:
        img_data = base64.b64decode(part.inline_data.data)
        result_img = Image.open(io.BytesIO(img_data))
        result_img.save(output_path)
        print(f"Imagem salva: {output_path}")
        break
```

Antes de executar:
- Substitua `[CATALOG_BLOCK]` no PROMPT pela lista de traduções confirmadas no Passo 2
- Substitua `IMAGE_PATH`, `SOURCE_LANG` e `TARGET_LANG` com os valores reais
- Verifique se `google-generativeai` e `pillow` estão instalados:
```bash
pip install google-generativeai pillow
```

---

## ENTREGA FINAL

Ao concluir, informe:
1. **Caminho da imagem salva** (ex: `fisiocare-1-en.png`)
2. **Log de traduções** — tabela: original → traduzido
3. **Alertas** — elementos com possível limitação (textos curvos, baixa resolução, sobreposição complexa)
