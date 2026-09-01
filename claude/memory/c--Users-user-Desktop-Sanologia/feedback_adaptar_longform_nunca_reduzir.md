---
name: feedback_adaptar_longform_nunca_reduzir
description: "Ao adaptar copy de concorrente, NUNCA reduzir caracteres vs original; localizar pra BR; trocar produto mantendo ângulo"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7c722b03-0e07-4b10-9a06-8394a9f4326c
---

Ao adaptar long-forms de concorrentes (raspados da Ad Library) pra um produto Sano/Relívia, o Guilherme quer **tradução fiel + troca de dados**, não recriação:

**Why:** o long-form campeão já provou converter; mudar a estrutura/hook joga fora o que funciona.

**How to apply:**
- **NUNCA REDUZIR o tamanho.** A adaptação deve ter >= o nº de caracteres do original (`wc -m`). Aumentar tudo bem, reduzir nunca. Se faltar, EXPANDIR com detalhe fiel (mais da cena, mais prova, mais mecanismo) — nunca cortar. Regra explícita dele.
- Manter EXATO: estrutura, hook de abertura, ordem dos blocos, metáforas, números/estatísticas, CTA final.
- **Localizar pra BR:** Stanford→USP/Unicamp, nomes gringos/hispânicos→brasileiros, clínicas→BR, $/pesos→R$, cidades (Bogotá/Medellín/Miami)→BR, lojas (Falabella/Éxito/Amazon)→farmácia/Mercado Livre.
- **Trocar o produto** pelos ativos REAIS do alvo (não inventar ingrediente). Herói alheio (astaxantina/glutationa/Melaxin) → o ativo do produto Sano mantendo o MESMO argumento (ex "oral não chega no rosto" → "creme de farmácia não penetra onde a mancha nasce").
- NÃO suavizar alegações (ver [[feedback_nao_suavizar_alegacoes]] e [[feedback_nao_nerfar_compliance]]).
- Sem drop cap ([[feedback_no_drop_cap_advertorial]]), sem preço no corpo ([[feedback_advertorial_no_price]]).

Escala via 7 agentes general-purpose em paralelo, cada um com ~7-8 slugs, lendo originais quebrados em `_originais_txt/<slug>.txt` e escrevendo `.md` em Research/Clarilux-Adaptados/. Ficha do Clarilux: 4 ativos (Tranexâmico/Alfa-Arbutin/Niacinamida/Glicólico), garantia 180d, destino sanobrasil.com/clarilux-v2. Fonte dos originais: [[reference_raspar_ad_library_drissionpage]].
