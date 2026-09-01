---
name: Pipeline Canônico para Escalar Criativo UGC Validado
description: Sequência de 4 fases para pegar 1 criativo UGC com conversões e gerar 3 novos roteiros + refs prontas para Veo 3.1. Aplicar quando criativo bate 100+ conversões e precisa escalar.
type: feedback
originSessionId: 7ddb77bf-0848-4bb2-aaf6-8086d30e2380
---
# Pipeline Canônico — Escalar Criativo UGC Validado (Suplementos)

## Quando aplicar
Criativo UGC já validou (mínimo 50-100 conversões) e precisa virar template para escala. NÃO aplicar para criativos não-validados — para esses, usar `/copy-anuncio` ou framework do zero.

## Sequência obrigatória (4 fases)

### Fase 1 — ANÁLISE (engenharia reversa do campeão)
- Skill: `copy-master:tasks:analyze-copy`
- Output: scorecard 8 dimensões + Cialdini/Warren + 5 hipóteses ranqueadas + esqueleto vencedor
- **Por quê:** sem entender por que converteu, próximo criativo é chute.

### Fase 2 — EVOLUÇÃO TRIPLA (3 especialistas em paralelo)
Trio canônico para evoluir um campeão:
- `copy-master:agents:dan-kennedy` → urgência ética (deadlines reais — biológico, sazonal, lote)
- `copy-master:agents:alex-hormozi` → Grand Slam Offer (stack de bônus + ancoragem + garantia agressiva)
- `copy-master:agents:stefan-georgi` → 5 variações sistemáticas com variável isolada para A/B

**Regra:** rodar os 3 em paralelo via Skill (não sequencial). Cada um cobre um vetor de otimização diferente.

### Fase 3 — ROTEIRIZAÇÃO PARA VEO 3
Estrutura: 7 cenas × 8s = 56s totais, formato timestamp prompting.
- Ver `feedback_veo3_regras_suplemento.md` para regras específicas.

### Fase 4 — REFERÊNCIAS PARA VEO 3.1 INGREDIENTS-TO-VIDEO
- REF-A (pessoa sozinha) — usar técnicas anti-IA
- REF-B (pessoa + produto) — fusão de 2 imagens
- REF-C (opcional, transição)

## Why
Esse trio (Kennedy/Hormozi/Georgi) cobre os 3 vetores que escalam um criativo validado: persuasão imediata (urgência), valor percebido (oferta), e teste sistemático (variações). Outros copywriters podem refinar, mas esses 3 são canônicos.

## How to apply
- Quando o usuário disser "esse criativo deu X conversões, gera mais" — aplicar pipeline completo, não só uma das fases.
- Documento mestre completo do processo: `Relivia Context/Playbooks/PIPELINE-CRIATIVO-UGC-SUPLEMENTO.md` no Obsidian.
- Case de referência: Relívia Orégano + Nigela (sessão de 2026-04-28).
