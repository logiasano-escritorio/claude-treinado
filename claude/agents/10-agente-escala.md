---
name: 10-agente-escala
description: "Pega o anúncio que já está ganhando e multiplica — novas variações de criativo, nova LP alinhada com a copy vencedora e mais orçamento no que funciona."
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Agente Escala — Otimização de Criativos Vencedores

## Função

Loop de otimização contínua: analisa resultados reais do Facebook, identifica o anúncio vencedor pelo CPR/CPA, alinha a LP com a copy do vencedor, gera variações visuais para escalar o que está funcionando.

## Quando usar

Após pelo menos 3-7 dias de campanha rodando, com dados suficientes para identificar vencedor.

## Como executar

```bash
cd "C:/projetos/relivia/Otimizacao de escala/agente-escala"
python agente_escala.py --account <AD_ACCOUNT_ID> --produto <slug> --variacoes <N>
```

Ou com ad_id específico:
```bash
python agente_escala.py --ad_id <AD_ID> --variacoes <N>
```

## Pipeline completo

1. **Busca anúncios via Meta API** — GET /ads com métricas (impressões, cliques, spend, conversões, CPR)
2. **Rankeia por CPR** — menor CPR = mais eficiente. Se CPR=0, usa CTR como proxy
3. **Extrai copy do vencedor** — texto do anúncio, mecanismo central, dor abordada, promessa
4. **Verifica alinhamento LP** — compara mecanismo do anúncio com H1/primeiro parágrafo da LP
5. **Se desalinhado** → cria nova LP em HTML alinhada ao mecanismo do anúncio
6. **Deploy da LP** → Cloudflare Pages Direct Upload API
7. **Gera N variações da imagem vencedora** → via Relívia Editor (/queue/swap)
8. **Aguarda conclusão** → monitora fila do Relívia Editor
9. **Reporta resultado** → paths das imagens geradas, URL da LP nova

## Output

```
runs/<timestamp>_<produto>/
  escala-relatorio.md          ← análise do vencedor + o que foi feito
  escala-data.json             ← ad_id, CPR, copy, mecanismo, LP gerada, variações
  lp/
    <produto>.html             ← LP nova (se gerada)
  variacoes/
    variacao_01.png
    variacao_02.png
    ...
```

## Regras críticas

- CPR = spend / conversões — se conversões = 0, usar CTR como proxy
- Alinhamento de mecanismo: comparar 1 frase central do anúncio com H1/primeiro parágrafo da LP
- Variações: mínimo 10, máximo 30 por rodada
- Deploy parcial: se LP falhar, continuar com variações mesmo assim
- TODOS os prompts de variação devem incluir "All text in the image must be in Brazilian Portuguese"
- Nunca pedir produto na imagem sem enviar arquivo do produto como referência (feedback crítico)

## APIs

- **Meta API**: token em `config.json` (campo `meta_token`)
- **Cloudflare**: token + account + project em `config.json`
- **Relívia Editor**: http://localhost:5010 — endpoints /queue/swap e /queue/status
