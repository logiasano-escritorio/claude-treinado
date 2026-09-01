---
name: project_advertoriais_clarilux_clareia
description: Levas de advertoriais Clarilux (melasma) e Clareia Premium (axila/virilha) com ângulos fortes + imagens Gemini
metadata: 
  node_type: memory
  type: project
  originSessionId: 77ffe71b-c21b-4cb4-9a58-1bbcf8ae4fa8
---

Levas de advertoriais criadas 2026-06-27 a partir de advertoriais campeões de concorrentes (Velura/ITMR + ângulos de saúde), adaptados pros produtos cosméticos da Sano.

## CLARILUX (melasma facial) — 4 advs novos, rotas `/adv-clarilux-v2..v5`
Ativos reais: **Ácido Tranexâmico** (estrela, via vascular/sinal), Niacinamida, Alfa-Arbutin, Ácido Glicólico. CTA → `/clarilux`.
- v2 ⭐⭐ "melasma está no sangue/vaso" (neovascularização, tranexâmico corta o suprimento)
- v3 "ciclo do clareador / fechar a torneira" (desligar a fábrica de melanina)
- v4 "o erro que faz voltar pior" (pele reativa, agredir = rebote)
- v5 "21 dias / abandono prematuro" (justifica kit grande)
Todos com MUITO antes/depois + **seção de comentários Facebook com fotos antes/depois** (mockup post FB) — pedido explícito do Guilherme: "muito antes e depois + sessão de comentários com fotos".
Gerador: `_dev/gen-clarilux-adv-imgs.py`. Imgs `advN-*`: produto cine, 7 antes/depois de melasma (bochecha/buço/testa/negra/madura/zoom), 3 fotos comentário FB, gráfico % (32→91%), diagrama vaso, timeline 21d, dor-corretivo.

## CLAREIA PREMIUM (axila/virilha escura) — 10 advs, rotas `/adv-clareia-v2..v11`
Ativos: Alfa-Arbutin, Ácido Mandélico, Ácido Kójico, enzimas. CTA → `/clareia-premium`.
- v2 RMI/você fez tudo errado (Velura) · v3 desodorante · v4 vergonha · v5 lâmina · v6 comparativo laser
- v7 acantose/pré-diabetes ⚠️ · v8 alumínio · v9 inflamação · v10 fungo · v11 hormonal
Ângulos de saúde (v7-v11) NÃO prometem curar doença (sinalizam, tratam a pele). Gerador `_dev/gen-clareia-adv-imgs.py`.

## ESQUELETO CAMPEÃO de melasma/mancha (validado): "você tentou X → falhou por ISSO → nosso mecanismo único resolve". É o que converte mulher cética que já gastou em laser/dermato.
## Template advs: cada produto herda `<head>`/CSS de seu `adv-{produto}.html` existente. Snippet comentários FB (com `.fb-photo` antes/depois) em scratchpad/skill `fb-comentarios`.
## Imagens com pessoa: validar gênero/idade/contexto antes de publicar [[feedback_ugc_conferir_genero_publico]]. Antes/depois de melasma = split ANTES|DEPOIS mesma mulher, label navy.

Ver [[project_advertoriais_tonico]] (mesmo padrão pro Tônico) e [[reference_vertex_ai_setup]].
