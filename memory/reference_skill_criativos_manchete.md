---
name: Skill /criativos-manchete
description: Gerador de criativos FB Ads estilo "manchete jornalística médica" (AlinhaFácil) reaproveitável pra qualquer produto
type: reference
originSessionId: bb15eb26-1191-4282-907c-cdda71f1fccd
---
`/criativos-manchete` — skill em `~/.claude/skills/criativos-manchete/` que gera criativos Facebook Ads no estilo AlinhaFácil (manchete jornalística com círculo no canto sup-direito, palavra-chave em ciano, footer fake-news).

**Trigger:** user digita `/criativos-manchete` OU pede "criativos no estilo AlinhaFácil/manchete" pra qualquer produto.

**Como funciona:**
- 4 templates: A (Revelação Médica), B (Investigação), C (Urgente/Sintoma), D (Pós-cirurgia)
- Geração 100% via **Gemini 3.1 Flash Image Preview** (`gemini-3.1-flash-image-preview`) — única que escreve PT-BR sem erro
- Script: `scripts/gerar.py` recebe JSON com lista de criativos
- Output: PNGs 1080x1080 + JPGs comprimidos pra Meta Ads

**Referências visuais** (11 criativos AlinhaFácil) ficam em `~/.claude/skills/criativos-manchete/referencias/`.

**Inputs obrigatórios pro user:** produto, problema resolvido, ângulo/mecanismo, estatística-chave, quantidade (1-30), templates a usar.

**Sistema visual fixo:** preto #000000 ou degradê pra #001833, ciano #2DD4D8 nos destaques, vermelho #E63946 nos alertas, sans-serif extra-bold, círculo borda ciano no canto sup-direito ~40% width, triângulo alerta sup-esquerdo, footer com logo fake-news.

**Smoke test validado em 2026-05-11** — 1 criativo de Sano Cálcio gerado com texto PT-BR perfeito, layout idêntico ao molde AlinhaFácil.
