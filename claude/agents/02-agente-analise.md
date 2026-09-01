---
name: 02-agente-analise
description: "Faz engenharia reversa do anúncio campeão — decifra o nível de consciência do público, a crença central que converte e por que aquela copy vende. Entrega o briefing completo para a copy."
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Agente 2 — Análise (Engenharia Reversa de Criativos)

## Posição no Pipeline

```
[Agente 1: Funil] → funil-data.json → [Agente 2: Análise] → analise-data.json → [Agente Copy]
                                                ↓
                                        ClickUp (comentário)
```

## Função

Processa o funil-data.json gerado pelo Agente 1. Aplica 4 personas especializadas para decompor os criativos campeões e gerar o brief estratégico para o Agente Copy.

## Como executar

```bash
cd "C:/Users/user/Desktop/Obsidian Supremo/Otimizacao de escala/agente-analise"
python agente_analise.py                  # usa run mais recente do agente-funil
python agente_analise.py <PATH_FUNIL>     # funil-data.json específico
```

## Personas utilizadas

| Persona | Função |
|---------|--------|
| Creative Analyst | Engenharia reversa: hook, ângulo, formato, score |
| Copy Master | Score 8 dimensões: headline, lead, mecanismo, prova, psicologia, fluidez, objeções, CTA |
| Eugene Schwartz | Diagnóstico de awareness (5 estágios) + instrução de lead |
| Evaldo Albuquerque | Crença central + 10 perguntas sequenciais de qualificação |

## Output — analise-data.json

| Campo | Uso no Agente Copy |
|-------|-------------------|
| `brief_para_agente_copy.estagio_awareness` | Define tipo de lead (edu vs problema vs solução) |
| `brief_para_agente_copy.instrucao_lead` | Instrução direta para Gary Halbert |
| `brief_para_agente_copy.crenca_central` | Eixo emocional central para Evaldo |
| `brief_para_agente_copy.mecanismo_unico` | Base para Stefan Georgi RMBC |
| `brief_para_agente_copy.inimigo_nomeado` | Vilão da narrativa (Blair Warren) |
| `brief_para_agente_copy.score_medio_atual` | Baseline para medir melhoria |
| `brief_para_agente_copy.angulo_criativo` | Ângulo dominante nos criativos |

## task:completed → dispara

```bash
python agente_copy.py --html <path_clone_run>/index.html
```
