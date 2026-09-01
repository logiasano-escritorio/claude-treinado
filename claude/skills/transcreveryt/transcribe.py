#!/usr/bin/env python3
"""
ytranscribe — baixa áudio de um vídeo YouTube e transcreve via Groq Whisper API.
Uso: python transcribe.py <URL> [--lang pt]
"""

import sys
import os
import tempfile
import argparse
import yt_dlp
from groq import Groq

FFMPEG_PATH = r"C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"

def download_audio(url: str, output_path: str) -> str:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "64",  # qualidade baixa = arquivo menor = mais rápido
        }],
        "ffmpeg_location": FFMPEG_PATH,
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "video")
    return title

def transcribe_with_groq(audio_path: str, lang: str, api_key: str) -> str:
    client = Groq(api_key=api_key)
    with open(audio_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(audio_path), f.read()),
            model="whisper-large-v3-turbo",
            language=lang,
            response_format="verbose_json",
        )
    return transcription.text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL do vídeo YouTube")
    parser.add_argument("--lang", default="pt", help="Código do idioma (pt, en, es...)")
    args = parser.parse_args()

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERRO: variável GROQ_API_KEY não definida.", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio")
        print(f"Baixando áudio de: {args.url}")
        title = download_audio(args.url, audio_path)

        # yt-dlp adiciona .mp3 automaticamente após conversão
        mp3_path = audio_path + ".mp3"
        if not os.path.exists(mp3_path):
            # tenta encontrar o arquivo gerado
            files = os.listdir(tmpdir)
            if files:
                mp3_path = os.path.join(tmpdir, files[0])
            else:
                print("ERRO: arquivo de áudio não encontrado.", file=sys.stderr)
                sys.exit(1)

        size_mb = os.path.getsize(mp3_path) / (1024 * 1024)
        print(f"Áudio baixado: {size_mb:.1f}MB — transcrevendo com Groq Whisper...")

        transcript = transcribe_with_groq(mp3_path, args.lang, api_key)

    print(f"\n=== TRANSCRIÇÃO: {title} ===\n")
    print(transcript)
    print("\n=== FIM DA TRANSCRIÇÃO ===")

if __name__ == "__main__":
    main()
