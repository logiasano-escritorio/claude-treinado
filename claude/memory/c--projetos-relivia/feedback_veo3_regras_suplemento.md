---
name: Regras Veo 3 para Roteiros UGC de Suplementos
description: Regras críticas descobertas em produção sobre quando o produto entra/sai de cena, setting de autoridade científica, ordem de geração, e quando subir cada referência no Veo 3.1 Ingredients-to-Video.
type: feedback
originSessionId: 7ddb77bf-0848-4bb2-aaf6-8086d30e2380
---
# Regras Veo 3 — Roteiros UGC para Suplementos (Relívia)

## 1. Apresentadora SEM produto nas cenas iniciais
- Cenas 1, 2, 3, 4 = mãos LIVRES, sem o produto na frame
- Produto entra a partir da cena 5 (momento "uso da [marca]")
- No CTA final (cena 7), produto SAI novamente — mãos livres para fechamento

**Why:** prende atenção pela autoridade primeiro, vende produto depois. Produto na mão desde a cena 1 ativa modo "modo defesa-anti-anúncio" do espectador.

## 2. Autoridade científica = consultório + jaleco
- Pesquisadora / bióloga / médica = consultório clínico ou laboratório, NUNCA home office
- Wardrobe: jaleco branco aberto sobre blusa neutra
- Setting: prateleira de livros médicos, microscópio desfocado, mesa branca, luz de janela

**Why:** congruência visual com a credencial. Pesquisadora em home office quebra a confiança.

## 3. Quando subir cada REF no Google Flow / Vertex AI

| Cena | REF-A (pessoa) | REF-B (produto isolado) | REF-C (pessoa+produto) |
|---|---|---|---|
| Cena 1-4 | ✅ Subir | ❌ NÃO subir | ❌ NÃO subir |
| Cena 5 | ✅ | ✅ SUBIR | ✅ SUBIR (transição) |
| Cena 6 | ✅ | ✅ | ✅ |
| Cena 7 | ✅ | ❌ Tirar | ❌ Tirar |

**Why:** se subir REF-B desde a cena 1, o Veo "alucina" e enfia o frasco em cima da mesa do fundo mesmo sem pedir. Subindo só na cena 5+ força cenas iniciais limpas.

## 4. Ordem de geração das cenas
**Gerar Cena 5 PRIMEIRO** (não a cena 1).
- Cena 5 é a mais difícil — continuidade da pessoa + consistência do produto + transição natural pegando
- Se cena 5 sai boa, as outras (mais simples) se alinham
- Se gerar cena 1 primeiro, pode chegar na cena 5 e continuidade quebrar

**Ordem ótima:** Cena 5 → 6 → 1 → 2 → 3 → 4 → 7

## 5. Anchor prompt obrigatório quando produto está em cena
Em CADA cena com produto, copiar literalmente:
```
CRITICAL ANCHOR: Do not modify the product jar. Keep the exact [marca]
supplement bottle from REF-B — same proportions, same label, same accent
color, same size relative to her hand. Hold at angle where label is
partially visible but not the focus.
```

**Why:** sem esse anchor, rótulo distorce frame a frame (latent drift).

## 6. Bloqueios obrigatórios em todo prompt Veo
- `(no subtitles)`
- `(no text overlays)`
- `(no captions)`

**Why:** Veo gosta de inventar texto se não bloquear.

## 7. Continuidade entre cenas
- Roupa: idêntica nas 7 cenas
- Cabelo: mesmo penteado, mesmos fios soltos
- Maquiagem: idêntica
- Setting: mesma mesa, mesmo fundo, mesma luz
- Câmera: selfie shot consistente, micro-zoom permitido

## How to apply
- Aplicar essas regras AUTOMATICAMENTE ao montar roteiros Veo 3 para qualquer suplemento Relívia.
- Documentação completa do processo em `Relivia Context/Playbooks/PIPELINE-CRIATIVO-UGC-SUPLEMENTO.md` no Obsidian.
- Origem das regras: sessão de produção do criativo Relívia Orégano + Nigela (2026-04-28).
