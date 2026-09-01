# -*- coding: utf-8 -*-
"""
TEMPLATE de geracao de imagens stop-scroll — /adaptar-longform

COMO USAR:
  1. Copiar este arquivo pro scratchpad
  2. Ajustar AD (o numero da peca), BASE (calibracao) e a lista CRIATIVOS
  3. python gerar-imagens-template.py

As imagens sao salvas DENTRO DO VAULT, ao lado da nota:
  Produtos/Magnesio/Adaptacoes prontas pra subir/Adaptacoes-Externas/<AD>/imagens/
Assim elas sincronizam junto com a nota e aparecem embutidas no Obsidian.

ATENCAO — a chave certa:
  GEMINI_IMAGE_API_KEY (formato AIza...)  -> FUNCIONA
  GEMINI_API_KEY       (formato AQ...)    -> 404, o Vertex Express nao tem
                                             o modelo de imagem na regiao
"""
import os, sys, base64, time
from pathlib import Path

# ------------------------------------------------------------------ .env
# Procura o .env em varios lugares: funciona no Windows e no Mac.
# Pode fixar com a variavel de ambiente SANO_ENV.
def _carregar_env():
    try:
        from dotenv import load_dotenv
    except Exception:
        return
    home = Path.home()
    candidatos = [
        Path(os.environ["SANO_ENV"]) if os.environ.get("SANO_ENV") else None,
        home / "Desktop" / "Sanologia" / ".env",
        home / "Sanologia" / ".env",
        home / ".env",
        Path.cwd() / ".env",
    ]
    for c in candidatos:
        if c and c.is_file():
            load_dotenv(c)
            return
_carregar_env()

from google import genai
from PIL import Image

API_KEY = os.environ.get("GEMINI_IMAGE_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERRO: nenhuma chave encontrada.")
    print("Defina GEMINI_IMAGE_API_KEY no ambiente, ou aponte o .env com SANO_ENV=/caminho/.env")
    sys.exit(1)

MODEL = "gemini-3.1-flash-image"
client = genai.Client(api_key=API_KEY)

# ------------------------------------------------------- achar o vault
# Procura o vault SANOLOGIA - REMOTO na maquina (Windows ou Mac).
# Pode fixar com a variavel de ambiente SANO_VAULT.
PASTA_ADAPTACOES = os.path.join(
    "Produtos", "Magnésio", "Adaptacoes prontas pra subir", "Adaptacoes-Externas")


def achar_vault():
    if os.environ.get("SANO_VAULT"):
        p = Path(os.environ["SANO_VAULT"])
        if (p / PASTA_ADAPTACOES).is_dir():
            return p
        print("aviso: SANO_VAULT nao tem a pasta de adaptacoes -> " + str(p))

    home = Path.home()
    raizes = [home / "Desktop", home, home / "Documents",
              home / "Library" / "Mobile Documents"]
    for raiz in raizes:
        if not raiz.is_dir():
            continue
        try:
            for filho in raiz.iterdir():
                if not filho.is_dir() or "SANOLOGIA" not in filho.name.upper():
                    continue
                for cand in [filho] + [d for d in filho.iterdir() if d.is_dir()]:
                    if (cand / PASTA_ADAPTACOES).is_dir():
                        return cand
        except (PermissionError, OSError):
            continue
    return None


# ---------------------------------------------------------------- AJUSTAR
AD = "AD-NN-slug-da-peca"          # <<< o nome da nota, sem .md

vault = achar_vault()
if vault is None:
    print("ERRO: nao achei o vault 'SANOLOGIA - REMOTO'.")
    print("Rode com SANO_VAULT=/caminho/do/vault  ou ajuste OUT na mao.")
    sys.exit(1)

OUT = vault / PASTA_ADAPTACOES / AD / "imagens"
OUT.mkdir(parents=True, exist_ok=True)
print("vault:  " + str(vault))
print("saida:  " + str(OUT))
print("")

# Caminho relativo pra colar no frontmatter IMAGENS: da nota
REL = OUT.relative_to(vault).as_posix()

# BASE = DNA visual. Ajustar a calibracao conforme o que a COPY descreve.
# >>> Extraia da copy os marcadores que existem. Se a copy nao descreve
# >>> corpo, NAO invente um: calibre por idade, cansaco e ambiente.
BASE = """PHOTOREALISTIC PHOTOGRAPH, not an illustration, not a render, not AI-art aesthetic.

CRITICAL REALISM RULES:
- Shot on a smartphone camera, slightly imperfect framing, natural handheld angle
- HARSH, UNFLATTERING lighting: overhead domestic light, cheap fluorescent, or direct flash
- NO beauty retouching, NO smoothing, NO glamour. Visible skin texture, pores, blemishes, uneven skin tone
- Real ordinary Brazilian people, NOT models. Ordinary tired faces, dark circles, no makeup
- Real Brazilian middle-class setting: ceramic floor tiles, plain painted walls, MDF furniture,
  clothes draped over a white plastic chair, floral bedspread, cluttered surfaces
- Documentary/candid feel, like a photo someone took without asking permission
- Muted, slightly desaturated colors. Grainy.
- NO text, NO logos, NO watermarks, NO graphic overlays anywhere in the image
- Vertical 4:5 format

BODY CALIBRATION (follow exactly, this is critical):
She is 54, roughly 1,60m and 81kg - about 15 kilos above her healthy weight.
MODERATELY overweight, NOT morbidly obese.
- Weight concentrated in the ABDOMEN and waist. Rounded belly with a soft fold at the waistline.
- Face full and slightly puffy, SMALL soft double chin. NOT a heavy multi-fold neck.
- Upper arms soft and full but still with visible shape and wrist definition. NOT massive.
- A stranger would call her gordinha or acima do peso, NEVER obesa morbida.
- Shoulder-length brown hair, tired eyes with dark circles.

The emotional register must be UNCOMFORTABLE and RAW, not aspirational.
This is the visual equivalent of a confession, not an advertisement."""

CRIATIVOS = [
    {
        "id": "01-nome-da-cena",
        "titulo": "Descricao curta pro log",
        "prompt": """SCENE: ...

Descrever: cenario, quem esta na cena, o que cada um faz, para onde olha,
qual a luz, o que esta em foco e o que esta desfocado.

O ponto emocional da imagem deve estar explicito no final do prompt.""",
    },
    # ... repetir
]
# ---------------------------------------------------------------- /AJUSTAR


def gerar(c):
    out = OUT / f"{c['id']}.png"
    if out.exists():
        print(f"[SKIP] {out.name}")
        return out

    full = (f"{BASE}\n\n{'='*70}\n{c['prompt']}\n\n"
            "Output: single photorealistic vertical 4:5 image. Absolutely NO text anywhere.")

    print(f"[GEN] {c['id']} - {c.get('titulo','')}")
    for tent in range(1, 7):
        try:
            r = client.models.generate_content(model=MODEL, contents=[full])
            for cand in r.candidates or []:
                for p in cand.content.parts:
                    if getattr(p, "inline_data", None) and p.inline_data.data:
                        d = p.inline_data.data
                        if isinstance(d, str):
                            d = base64.b64decode(d)
                        out.write_bytes(d)
                        print(f"  OK -> {out.name}")
                        return out
            # sem imagem: pode ser recusa do modelo, mostrar o texto
            txt = ""
            for cand in r.candidates or []:
                for p in cand.content.parts:
                    if getattr(p, "text", None):
                        txt += p.text
            print(f"  SEM IMAGEM. Resposta: {txt[:250]}")
            return None
        except Exception as e:
            m = str(e)
            if ("429" in m or "RESOURCE_EXHAUSTED" in m) and tent < 6:
                w = 20 * tent
                print(f"  429 (tent {tent}/6) aguardando {w}s...")
                time.sleep(w)
                continue
            print(f"  ERRO: {str(e)[:200]}")
            return None


def to_jpg_all():
    """Gera JPGs de tudo que existe na pasta. Meta aceita PNG mas JPG q92 pesa ~1/3."""
    j = OUT / "jpg"
    j.mkdir(exist_ok=True)
    n = 0
    for f in sorted(OUT.glob("*.png")):
        Image.open(f).convert("RGB").save(
            j / f.name.replace(".png", ".jpg"), "JPEG", quality=92, optimize=True)
        n += 1
    png = sum(f.stat().st_size for f in OUT.glob("*.png"))
    jpg = sum(f.stat().st_size for f in j.glob("*.jpg"))
    print(f"\n{n} JPGs em ./jpg/  ({png/1e6:.1f} MB PNG -> {jpg/1e6:.1f} MB JPG)")


if __name__ == "__main__":
    ok, fail = [], []
    for c in CRIATIVOS:
        r = gerar(c)
        if r:
            ok.append(r)
        else:
            fail.append(c["id"])
        time.sleep(12)  # rate limit

    print(f"\n=== {len(ok)}/{len(CRIATIVOS)} geradas ===")
    if fail:
        print("falhas:", fail)
    to_jpg_all()
    print("pasta:", OUT)
