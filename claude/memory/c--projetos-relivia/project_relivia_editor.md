---
name: Relívia Editor de Criativos — Estado do Projeto
description: SaaS local de edição de criativos com Gemini, rembg e moviepy — localização, porta, funcionalidades e dependências
type: project
originSessionId: d45cb7c5-9d54-4527-a81a-c75581f9bec8
---
## Fato

App local Flask em `C:/Users/user/Desktop/_Projetos/relivia-editor/` rodando na porta **5011**.

**Why:** Porta configurada no app.py — verificada em 2026-04-22.

**How to apply:** Ao retomar o projeto, iniciar com `python app.py` dentro da pasta e acessar http://localhost:5003.

---

## Arquivos principais

- `app.py` — backend Flask completo
- `index.html` — frontend single-file (todas as abas)
- `requirements.txt` — dependências para instalar com `pip install -r requirements.txt`
- `INICIAR.md` — guia completo de como subir o servidor

---

## Funcionalidades implementadas

1. 🔄 Trocar Produto na Foto (Gemini IMAGE)
2. 🌎 Traduzir Embalagem EN→PT-BR (Gemini IMAGE)
3. ✨ Traduzir + Colocar na Foto (pipeline 2 passos)
4. 🎨 Recriar Criativo (TEXT→JSON + IMAGE)
5. 📋 Fila em Massa — produto fixo, upload de pasta, instrução extra, 3 workers paralelos (ajustável 1-5)
6. 🔀 Variações — analisa benefícios, gera N copies diferentes, enfileira cada um
7. 🎬 Animar — gera MP4 com zoom/ken burns/fade/pulse via moviepy local
8. ✂️ Remover Fundo — rembg[cpu], transparência real RGBA
9. 💬 Chat — com imagem (edição) ou sem imagem (texto livre, tradução, dúvidas)

---

## Configurações técnicas

- Modelo Gemini: `gemini-3.1-flash-image-preview`
- API Key: `<CHAVE-NO-.env-LOCAL>`
- MAX_WORKERS: 3 (padrão, ajustável em runtime via UI)
- Análise de variações: assíncrona com polling (thread separada + `/variations/analyze/<job_id>`)
- Queue: deque + threading.Lock + daemon threads

---

## Dependências

```
Flask==3.1.3
google-genai==1.67.0
Pillow==12.1.1
rembg[cpu]==2.0.73
moviepy==1.0.3
numpy==2.4.3
```
