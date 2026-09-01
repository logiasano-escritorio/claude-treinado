---
name: transcreveryt
description: Transcreve qualquer vídeo do YouTube. Tenta legendas primeiro (MCP), cai no Groq Whisper se não tiver. Uso: /transcreveryt <url>
---

# /transcreveryt — Transcrição de Vídeos YouTube

Transcreve qualquer vídeo do YouTube. Tenta legendas primeiro (via MCP), cai no Groq Whisper se não tiver.

## Trigger
`/transcreveryt`

## Comportamento

1. O usuário fornece uma URL do YouTube
2. Tenta buscar transcrição via MCP `youtube-transcript` (rápido, sem custo)
3. Se falhar (sem legendas), executa fallback:
   - Baixa o áudio com `yt-dlp`
   - Transcreve com Groq Whisper (`whisper-large-v3-turbo`)
4. Retorna o texto completo da transcrição

## Fallback via Groq

**Script:** `C:/Users/user/.claude/skills/ytranscribe/transcribe.py`

**Dependências:**
- `yt-dlp` (já instalado via pip)
- `groq` (pip install groq)
- `ffmpeg` (necessário para conversão de áudio)
- `GROQ_API_KEY` configurada no ambiente

**Comando:**
```bash
GROQ_API_KEY=<key> python "C:/Users/user/.claude/skills/ytranscribe/transcribe.py" "<URL>" --lang pt
```

## Idiomas suportados
- `pt` — Português (padrão)
- `en` — Inglês
- `es` — Espanhol
- Qualquer código ISO 639-1

## Limites Groq (plano gratuito)
- 7.200 segundos de áudio/dia (~2h)
- 2h de áudio por requisição
- Velocidade: ~10-30x tempo real
