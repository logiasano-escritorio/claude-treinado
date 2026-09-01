---
name: Estilo A do /sano-criativos = manchete científica (não depoimento)
description: Os 15 criativos Estilo A do /sano-criativos devem ser manchete científica estilo Wealth Magazine, não depoimento íntimo
type: feedback
originSessionId: d2c18d3e-aab0-440a-b3c4-86d8c38e0c1d
---
Nos criativos Sano gerados pelo `/sano-criativos`, os 15 do **Estilo A (com texto)** devem ser **MANCHETE DE DESCOBERTA CIENTÍFICA** — não cena íntima/depoimento.

Formato aprovado (referência Wealth Magazine):
- Top 60-65%: 3D médico-grade hyper-realista (osso, cartilagem, articulação) — fundo navy/preto, ZERO pessoas
- Comparações lado-a-lado quando aplicável (esq deteriorado vermelho · dir regenerado dourado)
- Faixa amarela fina + logo "Sano" serif itálica branca pequena
- Bottom 30-35%: barra preta com headline AMARELA UPPERCASE BOLD GRANDE (Bebas/Anton/Impact), 8-14 palavras, 3-4 linhas
- Subheadline branca curta (opcional — algumas sem ficam mais fortes)
- Headline COMEÇA com: "CIENTISTAS DESCOBREM...", "ESTUDO REVELA...", "PESQUISADORES IDENTIFICAM...", "NOVA DESCOBERTA...", "DESCOBERTO POR QUE...", "MEDICINA REPENSA...", "PESQUISA EXPÕE...", "ESTUDO BRASILEIRO MOSTRA...", "MITO DESMENTIDO..."

**O que NÃO usar (formato rejeitado em 30/04/2026 no run StrongBones/artrose):**
- Cena íntima de pessoa segurando joelho/escada/cama
- Headline tipo "VOLTEI A AGACHAR PRA PLANTAR" / "ELE QUER COLO E VOCÊ FINGE QUE TÁ OCUPADA"
- Tom depoimento/testemunho

**Estilo B (15 cenas puras sem texto)** já tava ok desde o run inicial — mantém o briefing original do comando (cena científica/credibilidade/urgência sem nenhum texto).

**Why:** o cliente quer parar o scroll por curiosidade ("o que descobriram?"), não por reconhecimento de dor. Manchete científica funciona em público frio (topo de funil) porque ativa curiosidade intelectual em vez de gatilho emocional, que satura mais rápido.

**How to apply:** atualizar o template do comando `/sano-criativos` (ou o megaprompt A do script gerar_sano_*.py) pra usar este formato direto, sem precisar regerar. Os 5 hooks de B1 (Espelho de Dor) e os 5 de B3 (Pattern Interrupt) e 5 de B4 (Antes/Depois) viram todos "manchete científica" sobre mecanismos diferentes (osso subcondral, fosfato vs carbonato, D3, inflamação, hormônio, mineralização, etc). O bloco continua existindo só pra organizar o ângulo da copy, mas a forma visual é a mesma.

Referência salva: `c:/Users/user/Desktop/_Projetos/relivia-editor/gerar_sano_strongbones_artrose_v2.py` tem o megaprompt A V2 já calibrado.
