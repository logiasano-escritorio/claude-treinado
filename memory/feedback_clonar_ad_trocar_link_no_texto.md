---
name: feedback_clonar_ad_trocar_link_no_texto
description: "Ao clonar ad Meta e trocar destino, trocar o link no TEXTO (message) também, não só no botão"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 829a6fdb-bacc-4b83-a6f6-88ba66d09ee6
---

Ao clonar um ad do Meta pra um novo destino (ex: campanha nova apontando pra outra PV), **trocar o link em 3 lugares**, não só 1:
1. `link_data.link` (o botão) ✅ óbvio
2. `link_data.call_to_action.value.link` (o CTA) ✅ óbvio
3. **`link_data.message` (o TEXTO do anúncio)** ← ESQUECIDO com frequência

**Why:** a copy do anúncio muitas vezes escreve a URL no corpo ("acesse sanobrasil.com/prime-pv"). Se trocar só o botão, o leitor lê a URL antiga no texto e vai pro destino errado (ticket/PV antiga), furando o teste inteiro. O Meta NÃO avisa isso.

**How to apply:** ao recriar o creative, rodar no `message` uma troca cirúrgica com fronteira de palavra pra não pegar variantes:
`re.sub(r'(sanobrasil\.com/prime-pv)(?![\w-])', r'\1-tickets', msg)` — o `(?![\w-])` evita afetar `/prime-pv-tickets`, `/prime-pv-fascite`, `/prime-pv-joelho` etc. Depois validar: 0 ocorrências do link antigo no message + link do botão certo.

Detectado 2026-07-15 pelo Guilherme nos ads da Campanha B (direto-PV): eu tinha trocado só o botão, os 13 textos ainda diziam `sanobrasil.com/prime-pv` (ticket 199). Corrigido recriando os creatives.

Ver [[reference_funil_roas_3_apis]], [[feedback_criativo_nao_pode_mentir_destino]], [[reference_publisher_cache_colisao_nome]] (creative é imutável — recriar e trocar).
