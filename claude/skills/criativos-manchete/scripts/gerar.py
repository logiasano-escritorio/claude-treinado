"""
/criativos-manchete - gerador de criativos Facebook Ads no estilo manchete jornalistica.

Recebe um arquivo JSON com a config dos criativos (produto + lista de criativos)
e gera 1080x1080 PNGs + JPGs prontos pro Meta Ads via Gemini 3.1 Flash Image Preview.

Uso:
  python gerar.py config.json

Estrutura do config.json:
{
  "produto": "Sano Calcio",
  "slug": "sano-calcio",
  "output_dir": "C:\\Users\\user\\Desktop\\criativos-manchete\\sano-calcio-2026-05-11",
  "criativos": [
    {
      "id": "01",
      "template": "A",
      "pill": "REVELACAO MEDICA",
      "headline_linhas": ["Osteoporose:", "9 em cada 10", "passam sem saber"],
      "palavras_ciano": ["9 em cada 10"],
      "subheadline": "Estudo brasileiro com 2.400 mulheres acima de 50",
      "imagem_circulo": "MRI scan of osteoporotic vertebra ...",
      "background": "subtle anatomical illustration of spine on black background",
      "footer_brand": "SAUDE NEWS"
    },
    ...
  ]
}
"""
import os
import sys
import json
import base64
import time
from pathlib import Path

# Garantir que o .env do Sanologia eh carregado
try:
    from dotenv import load_dotenv
    load_dotenv(r"C:\Users\user\Desktop\Sanologia\.env")
except Exception:
    pass

from google import genai
from PIL import Image

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERRO: GEMINI_API_KEY nao encontrada. Verifique C:\\Users\\user\\Desktop\\Sanologia\\.env")
    sys.exit(1)

MODEL = "gemini-3.1-flash-image-preview"  # OBRIGATORIO: unico que escreve PT-BR sem erro
# A chave do .env do Sanologia eh Vertex AI Express (AQ.Ab8...) -> precisa vertexai=True + api v1
from google.genai import types as _genai_types
if API_KEY.startswith("AQ."):
    client = genai.Client(vertexai=True, api_key=API_KEY,
                          http_options=_genai_types.HttpOptions(api_version="v1"))
else:
    client = genai.Client(api_key=API_KEY)

# ============================================================================
# PROMPT TEMPLATES (DNA visual extraido dos 11 criativos AlinhaFacil)
# ============================================================================

SYSTEM_PROMPT_BASE = """Você é um gerador de criativos Facebook Ads no estilo "manchete jornalística médica brasileira".

REGRAS VISUAIS FIXAS (NUNCA mude):
- Formato: quadrado 1:1 (1080x1080)
- Fundo: PRETO PURO #000000 ou degradê preto→azul-meia-noite #001833
- Cor de DESTAQUE: ciano #2DD4D8 (usado em 1-2 palavras-chave da headline + footer)
- Cor de ALERTA: vermelho #E63946 (triângulo + pill "URGENTE/CUIDADO")
- Texto principal: branco #FFFFFF, sans-serif ULTRA-BOLD (estilo Inter Black ou Montserrat ExtraBold)
- Subtexto: cinza claro #C9C9C9
- CÍRCULO DE DESTAQUE: SEMPRE no canto superior direito, borda ciano fina (4-6px), ~40% da largura da imagem
- TRIÂNGULO ALERTA VERMELHO ⚠️: canto superior esquerdo (pequeno)
- PILL SUPERIOR: pílula arredondada ciano OU vermelha com texto em caixa alta
- FOOTER: logotipo fictício de portal de notícia + seta ciano apontando direita →
  >>> O texto do footer DEVE ser EXATAMENTE o valor de footer_brand passado (ex: "SAÚDE NEWS"). NÃO invente outro nome de portal (NADA de "PORTAL SAÚDE AGORA", "G NEWS" etc). Escreva exatamente o footer_brand pedido.

CRÍTICO:
- TODO TEXTO em PORTUGUÊS BRASILEIRO com ACENTUAÇÃO CORRETA (á, ã, ç, é, í, ó, ú)
- ZERO ERROS DE ORTOGRAFIA
- A palavra/frase destacada deve aparecer em CIANO #2DD4D8 dentro da headline
- O círculo NUNCA mostra o produto — mostra o PROBLEMA/CAUSA (foto médica, render anatômico, pessoa com dor)
"""

TEMPLATE_PROMPTS = {
    "A": """TEMPLATE A — "REVELAÇÃO MÉDICA / ESTUDO"
- Pill ciano arredondada centralizada/esquerda: "{pill}"
- Triângulo vermelho ⚠️ no canto superior esquerdo
- Círculo grande no canto superior direito mostrando: {imagem_circulo}
- Background atrás da headline: {background}
- Headline na metade inferior em texto extra-bold branco gigante, 3-4 linhas:
{headline_formatado}
- Subtítulo pequeno em cinza claro abaixo da headline: "{subheadline}"
- Footer centralizado: logotipo fictício "{footer_brand}" + seta ciano →""",

    "B": """TEMPLATE B — "INVESTIGAÇÃO"
- Pill ciano arredondada: "{pill}"
- Background: cenário hospitalar/cirúrgico desfocado escuro
- Círculo grande no canto superior direito: {imagem_circulo}
- Headline GIGANTE em CAIXA ALTA, palavras-chave em ciano:
{headline_formatado}
- Subtítulo curto cinza abaixo: "{subheadline}"
- Footer: logotipo fictício "{footer_brand}" centralizado com seta laranja/ciano""",

    "C": """TEMPLATE C — "URGENTE / SINTOMA EMOCIONAL"
- Pill VERMELHA "URGENTE" no topo + triângulo amarelo pequeno
- Background: pessoa real esmaecida demonstrando dor/desconforto ({background})
- Círculo no canto superior direito: {imagem_circulo}
- Headline com 1 palavra/frase impactante em ciano:
{headline_formatado}
- Subtítulo: "{subheadline}"
- Pequeno ícone médico (caduceu) no footer + seta para baixo ↓ pra criar urgência""",

    "D": """TEMPLATE D — "PÓS-CIRURGIA / IMPACTO REAL"
- Pill ciano OU vermelha: "{pill}"
- Background escuro com silhueta de pessoa em cenário médico
- Círculo no canto superior direito mostrando imagem IMPACTANTE (cicatriz, complicação): {imagem_circulo}
- Headline LONGA multi-linha (4-6 linhas), tom "olha o que pode dar errado":
{headline_formatado}
- Subtítulo: "{subheadline}"
- Footer: logotipo fictício "{footer_brand}" + seta ciano →"""
}

def format_headline_with_cyan(linhas: list, palavras_ciano: list) -> str:
    """Mostra a headline LIMPA (sem tags) + lista separada das palavras em ciano.
    Tags inline <CIANO> vazavam pra dentro da imagem; instruçao separada e mais segura."""
    out = [f'   "{linha}"' for linha in linhas]
    bloco = "\n".join(out)
    if palavras_ciano:
        alvos = " | ".join(p for p in palavras_ciano if p)
        bloco += (
            f'\n\n   >>> PINTE EM CIANO #2DD4D8 (e SOMENTE essas) as palavras: {alvos}'
            f'\n   >>> O resto da headline fica BRANCO. NAO escreva a palavra "CIANO" nem colchetes/tags na imagem.'
        )
    return bloco


def gerar_criativo(criativo: dict, output_dir: Path) -> Path | None:
    """Gera um criativo via Gemini 3.1 Flash Image Preview."""
    cid = criativo["id"]
    template = criativo["template"]
    out_path = output_dir / f"criativo-{cid}-{template}.png"
    if out_path.exists():
        print(f"[SKIP] {out_path.name} (existe)")
        return out_path

    headline_fmt = format_headline_with_cyan(
        criativo["headline_linhas"], criativo.get("palavras_ciano", [])
    )

    template_prompt = TEMPLATE_PROMPTS[template].format(
        pill=criativo["pill"],
        imagem_circulo=criativo["imagem_circulo"],
        background=criativo.get("background", "preto puro liso"),
        headline_formatado=headline_fmt,
        subheadline=criativo["subheadline"],
        footer_brand=criativo["footer_brand"],
    )

    full_prompt = f"""{SYSTEM_PROMPT_BASE}

{template_prompt}

INSTRUÇÕES FINAIS:
- Saída: imagem quadrada 1080x1080, alta qualidade, fotorrealista mistura com tipografia precisa
- TODO texto em PT-BR com acentuação correta
- NUNCA escreva tags, colchetes ou a palavra "CIANO" na imagem — apenas pinte de ciano #2DD4D8 as palavras indicadas na headline
- ZERO erros de ortografia
- Layout: círculo sup-direita, triângulo/alerta sup-esquerda, headline no centro/rodapé, footer embaixo"""

    print(f"[GEN] criativo-{cid}-{template}...")
    max_retries = 6
    for attempt in range(1, max_retries + 1):
        try:
            resp = client.models.generate_content(model=MODEL, contents=[full_prompt])
            for cand in resp.candidates or []:
                for part in cand.content.parts:
                    if hasattr(part, "inline_data") and part.inline_data and part.inline_data.data:
                        data = part.inline_data.data
                        if isinstance(data, str):
                            data = base64.b64decode(data)
                        with open(out_path, "wb") as f:
                            f.write(data)
                        print(f"  OK -> {out_path.name}")
                        return out_path
            print("  FAIL: sem imagem na resposta")
            return None
        except Exception as e:
            msg = str(e)
            is_quota = "429" in msg or "RESOURCE_EXHAUSTED" in msg
            if is_quota and attempt < max_retries:
                wait = 20 * attempt  # backoff: 20,40,60,80,100s
                print(f"  429 (tentativa {attempt}/{max_retries}) — aguardando {wait}s...")
                time.sleep(wait)
                continue
            print(f"  ERRO: {e}")
            return None


def to_jpg(png_path: Path) -> Path:
    """Converte PNG -> JPG pra Meta Ads (arquivos menores)."""
    jpg_path = png_path.parent / "jpg" / png_path.name.replace(".png", ".jpg")
    jpg_path.parent.mkdir(exist_ok=True)
    img = Image.open(png_path).convert("RGB")
    # Garantir 1080x1080
    if img.size != (1080, 1080):
        img = img.resize((1080, 1080), Image.LANCZOS)
    img.save(jpg_path, "JPEG", quality=92, optimize=True)
    return jpg_path


def main():
    if len(sys.argv) < 2:
        print("Uso: python gerar.py <config.json>")
        sys.exit(1)

    cfg_path = Path(sys.argv[1])
    if not cfg_path.exists():
        print(f"Config nao encontrada: {cfg_path}")
        sys.exit(1)

    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    output_dir = Path(cfg["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== Gerando {len(cfg['criativos'])} criativos pro produto: {cfg['produto']} ===")
    print(f"Output: {output_dir}\n")

    success, fail = [], []
    for criativo in cfg["criativos"]:
        path = gerar_criativo(criativo, output_dir)
        if path:
            success.append(path)
            to_jpg(path)  # tambem salva JPG
        else:
            fail.append(criativo["id"])
        time.sleep(12)  # rate limit Vertex Express (imagem tem RPM baixo)

    print(f"\n=== RESUMO ===")
    print(f"Sucesso: {len(success)}/{len(cfg['criativos'])}")
    if fail:
        print(f"Falhas: {fail}")
    print(f"\nPNGs: {output_dir}")
    print(f"JPGs (pra Meta Ads): {output_dir}/jpg/")


if __name__ == "__main__":
    main()
