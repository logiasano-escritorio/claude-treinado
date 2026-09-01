---
name: 08-agente-produto
description: "Transforma a página do produto em máquina de conversão — diagnóstico CRO completo, identidade visual auditada e prompts gerados para as imagens de embalagem e lifestyle."
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Agente 8 — Produto (Clone + CRO + Prompts Gemini)

## Posição no Pipeline

```
[Agente 1: Funil] → destination_url ─┐
[Agente 5: Copy]  → gemini-prompts ──┤→ [Agente 8: Produto] → produto-index.html
                                      │                      → produto-otimizado.html
                                      └──────────────────────→ produto-gemini-prompts.json
```

## Como executar

```bash
cd "C:/Users/user/Desktop/Obsidian Supremo/Otimizacao de escala/agente-produto"
python agente_produto.py                      # usa destination_url do funil-data.json mais recente
python agente_produto.py <URL>                # URL específica
python agente_produto.py --funil <PATH_JSON>  # funil-data.json específico
```

## Etapas e Personas

### Etapa 10 — Clone da Página do Produto

| Fase | Ferramenta | O que faz |
|------|-----------|-----------|
| 10.1 | DrissionPage | Abre URL, scroll lazy-load, captura DOM |
| 10.2 | DrissionPage | Screenshot full-page |
| 10.3 | HTTP | Baixa todas as imagens do produto |
| 10.4 | Claude Vision (max_tokens=32000) | Reconstrói HTML fiel ao original |

**IMPORTANTE:** Usar DrissionPage (não Playwright — desinstalado):
```python
from DrissionPage import ChromiumPage, ChromiumOptions
opts = ChromiumOptions()
opts.auto_port()
```

### Etapa 11 — Diagnóstico CRO

| # | Persona | O que faz |
|---|---------|-----------|
| 11.1 | Brand Identity Auditor | Consistência paleta/tipografia/tom vs advertorial |
| 11.2 | CRO Specialist | Identifica pontos de fricção + quick wins |
| 11.3 | Conversion Architect | Reescreve hero, benefícios, CTA final |

### Etapa 12 — Prompts Gemini para Imagens do Produto

| # | Persona | O que faz |
|---|---------|-----------|
| 12.1 | Product Photographer | Mapeia cada imagem por função (hero/embalagem/lifestyle/etc) |
| 12.2 | Label Designer | 3 variações de prompt para embalagem/rótulo |
| 12.3 | Lifestyle Director | 4 prompts de lifestyle shots |
| 12.4 | Ad Integration | 3 criativos de anúncio (1:1, 9:16, 16:9) |

## Output

| Arquivo | Uso |
|---------|-----|
| `produto-index.html` | Clone fiel da página |
| `produto-otimizado.html` | Com melhorias CRO aplicadas |
| `produto-diagnostico-cro.json` | Auditoria visual + pontos de fricção |
| `produto-gemini-prompts.json` | Prompts para embalagem + lifestyle + criativos |
| `produto-relatorio.md` | Relatório completo |

## task:completed → dispara

```bash
python agente_revisor.py --clone <run_dir> --fix
```
Depois: executar prompts Gemini via Relívia Editor para editar imagens do produto.
