---
name: 05-agente-copy
description: "Reescreve sua copy passando pelos 6 maiores copywriters da história — Halbert, Georgi, Sugarman, Bencivenga, Cialdini e Lampropoulos — até chegar no nível que vende de verdade."
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Agente 5 — Copy (Elevação + Storytelling + Prompts Gemini)

## Posição no Pipeline

```
[Agente 2: Análise] → analise-data.json ─┐
[Agente 3: Clone]   → index.html ────────┤→ [Agente 5: Copy] → advertorial-com-storytelling.html
[Agente 4: Tráfego] → campanha-brief.json┘                   → gemini-prompts.json
                                                              → ClickUp (comentário)
```

## Como executar

```bash
cd "C:/Users/user/Desktop/Obsidian Supremo/Otimizacao de escala/agente-copy"
python agente_copy.py                        # usa run mais recente do clone
python agente_copy.py --html <PATH_HTML>     # HTML específico
```

## Etapa 5 — Elevação de Copy (6 camadas sequenciais)

| # | Persona | O que faz |
|---|---------|-----------|
| 5.1 | Gary Halbert | Reescreve primeiros 4 parágrafos — lead visceral |
| 5.2 | Stefan Georgi | Seção de mecanismo único (RMBC) |
| 5.3 | Joe Sugarman | Identifica 5 pontos de abandono + reescreve transições |
| 5.4 | Gary Bencivenga | Reforça prova em cada claim + testimonials como narrativas |
| 5.5 | Robert Cialdini | Audita 7 princípios + insere escassez antes do CTA |
| 5.6 | Parris Lampropoulos | Claims de saúde/suplemento — sinaliza ilegais, reescreve mecanismo |

## Etapa 6 — Storytelling (3 camadas)

| # | Persona | O que faz |
|---|---------|-----------|
| 6.1 | Kindra Hall | 4 histórias (Value, Founder, Customer, Purpose) |
| 6.2 | Blair Warren | 5 gatilhos emocionais profundos |
| 6.3 | Manifestador | Abertura + CTA tribal |

## Etapa 7 — Prompts Gemini (4 agentes)

| # | Persona | O que faz |
|---|---------|-----------|
| 7.1 | UX Designer | Mapeia cada imagem por função de persuasão |
| 7.2 | Hormozi Hooks | 5 hook texts para imagens de topo (cold traffic) |
| 7.3 | Ad Midas | Visual creative brief completo |
| 7.4 | Visual Generator | Prompts Gemini estruturados por imagem |

## Output

| Arquivo | Uso |
|---------|-----|
| `advertorial-copy-elevada.html` | Após 6 camadas de copy |
| `advertorial-com-storytelling.html` | Após 3 camadas de storytelling — base para tradução |
| `gemini-prompts.json` | Prompts prontos para executar no Gemini Image API |

## task:completed → dispara

```bash
python agente_traducao.py --html <path>/advertorial-com-storytelling.html
```
