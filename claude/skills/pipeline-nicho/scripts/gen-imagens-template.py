# -*- coding: utf-8 -*-
"""
10 imagens novas de MELASMA pro Clarilux, do zero, baseadas nos padrões campeões
raspados dos concorrentes (before/after, termográfica, produto+headline, close mancha).
Tudo PT-BR. Vertex AI Express (gemini-3-pro-image-preview).
Saída: clarilux/images/melasma-novas/*.webp. Reexecutável (pula o que já existe).
"""
import os, sys, io, time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path("c:/Users/user/Desktop/Sanologia")
load_dotenv(ROOT / ".env")
client = genai.Client(vertexai=True, api_key=os.getenv("GEMINI_API_KEY"),
                      http_options=types.HttpOptions(timeout=180_000, api_version="v1"))
MODEL = "gemini-3-pro-image-preview"
OUT = ROOT / "clarilux" / "images" / "melasma-novas"
OUT.mkdir(parents=True, exist_ok=True)
REF = ROOT / "_dev" / "produtos-foto" / "clarilux.png"

PROD = ('the EXACT Clarilux (SANO) skin-brightening serum bottle from the reference image '
        '(reproduce it 1:1 — white bottle, pump top, "SANO" logo, "CLARILUX SÉRUM FACIAL UNIFORMIZADOR" '
        'label with botanical line art, do NOT redesign, do NOT change the text on the label).')

# Before/After template (ANTES/DEPOIS em PT-BR)
BA = ("Clinical dermatology BEFORE-AFTER split photo of {who}, plain soft grey studio background, "
      "professional even lighting, photorealistic, sharp. LEFT half has a small navy badge 'ANTES': {antes}. "
      "RIGHT half has a small navy badge 'DEPOIS': the SAME person with the melasma dramatically faded, "
      "even clear uniform radiant skin tone. Same face, same angle, same lighting both halves. "
      "Realistic skin texture and pores. ONLY the navy 'ANTES' and 'DEPOIS' badges as text, nothing else. Portuguese.")

# (id, usa_ref, aspect, prompt) — 10 imagens, mix dos padrões campeões
JOBS = [
 # 1. Produto cinematográfico (padrão feline/premium)
 ("01-produto-cine", True, "1:1",
  f"Cinematic premium skincare product photography of {PROD} Standing on a clean light marble surface, "
  f"elegant soft studio lighting, a few fresh water droplets, subtle green botanical leaves, luxury dermatology mood, "
  f"shallow depth of field, high detail, photorealistic. NO text overlays, NO people."),
 # 2-6. Before/After de melasma (zonas e perfis variados — o padrão mais forte)
 ("02-ba-bochechas", False, "1:1",
  BA.format(who="a Brazilian woman around 40", antes="dark brown MELASMA patches on both CHEEKS and cheekbones, blotchy uneven pigmentation")),
 ("03-ba-buco-testa", False, "1:1",
  BA.format(who="a Brazilian woman around 44", antes="MELASMA on the UPPER LIP (buço) and FOREHEAD, symmetrical brownish patches")),
 ("04-ba-mulher-negra", False, "1:1",
  BA.format(who="a Black Brazilian woman around 38", antes="darker hyperpigmented MELASMA patches on cheeks and forehead")),
 ("05-ba-madura", False, "1:1",
  BA.format(who="a Brazilian woman around 52", antes="brown MELASMA patches on cheeks plus sun-aged uneven tone")),
 ("06-ba-gravidez", False, "1:1",
  BA.format(who="a Brazilian pregnant woman around 32", antes="pregnancy MELASMA (cloasma) mask across cheeks, nose and forehead")),
 # 7. Termográfica (padrão trytonebright "tirosinase") — texto PT-BR
 ("07-termografica", False, "4:5",
  "Split thermal/infrared style dermatology visualization of a woman's face, dramatic. LEFT half in cold blue/purple "
  "tones with a small white label 'ANTES' and below it '(EXCESSO DE MELANINA)'. RIGHT half in warm orange/yellow "
  "tones with a small white label 'DEPOIS' and below it '(MELANINA BLOQUEADA)'. Black background. Symmetrical face. "
  "Text in Portuguese, clean sans-serif, spelled EXACTLY: 'ANTES', 'DEPOIS', 'EXCESSO DE MELANINA', 'MELANINA BLOQUEADA'."),
 # 8. Close macro da mancha (padrão bienestar) — sem texto
 ("08-close-mancha", False, "3:2",
  "Extreme close-up macro photo of a Brazilian woman's cheek showing brown MELASMA patches and uneven pigmentation "
  "near the eye and cheekbone, blonde/brown hair strand, natural daylight, photorealistic, realistic skin pores. NO text."),
 # 9. Produto + headline PT-BR (padrão feline "Fade Pregnancy Melasma")
 ("09-produto-headline", True, "1:1",
  f"Skincare e-commerce ad image on a light marble background. On the RIGHT: {PROD} On the LEFT, bold black "
  f"headline text in Portuguese spelled EXACTLY: 'O fim do melasma que sempre volta'. Below it, smaller grey text: "
  f"'Fórmula de 4 ativos que ataca a mancha na raiz'. In a red circle bottom area: 'GARANTIA 180 DIAS'. "
  f"Clean, professional, high contrast readable Portuguese text, no spelling errors."),
 # 10. Mulher segurando o produto (UGC-ish, aspiracional pós-resultado)
 ("10-mulher-segurando", True, "4:5",
  f"Photorealistic photo of a happy Brazilian woman around 42 with clear even radiant skin (no melasma), smiling gently, "
  f"holding {PROD} near her face, soft natural home lighting, bathroom/vanity background slightly blurred. "
  f"She looks confident and fresh. NO text overlays."),
]

def gen(job):
    jid, use_ref, aspect, prompt = job
    out = OUT / f"clarilux-melasma-{jid}.webp"
    if out.exists():
        print(f"[skip] {jid}"); return True
    parts = [prompt]
    if use_ref and REF.exists():
        parts = [types.Part.from_bytes(data=REF.read_bytes(), mime_type="image/png"), prompt]
    for attempt in range(3):
        try:
            resp = client.models.generate_content(
                model=MODEL, contents=parts,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio=aspect)))
            for p in resp.candidates[0].content.parts:
                if getattr(p, "inline_data", None) and p.inline_data.data:
                    img = Image.open(io.BytesIO(p.inline_data.data)).convert("RGB")
                    img.save(out, "WEBP", quality=90)
                    print(f"[OK] {jid} -> {out.name} ({img.size[0]}x{img.size[1]})")
                    return True
            print(f"[retry {attempt+1}] {jid}: sem imagem na resposta")
        except Exception as e:
            print(f"[retry {attempt+1}] {jid}: {str(e)[:120]}")
        time.sleep(4)
    print(f"[FALHOU] {jid}")
    return False

def main():
    ok = 0
    for job in JOBS:
        if gen(job): ok += 1
        time.sleep(2)
    print(f"\n=== {ok}/{len(JOBS)} imagens geradas em {OUT} ===")

if __name__ == "__main__":
    main()
