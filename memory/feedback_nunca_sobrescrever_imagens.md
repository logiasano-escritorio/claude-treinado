---
name: feedback-nunca-sobrescrever-imagens
description: "NUNCA sobrescrever arquivos de imagem existentes — criar copia com sufixo (ex: -constipacao, -ansiedade) e atualizar SO o HTML que precisa. Sobrescrever quebra outras pags que ainda usam o arquivo original em prod."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d28dd148-1791-4d49-9f63-897f647234d1
---

NUNCA sobrescrever imagens existentes via Gemini regen ou cp. Sempre criar arquivo NOVO com sufixo descritivo (`-constipacao.jpg`, `-ansiedade.png`, `-v2.webp`) e atualizar apenas o HTML do funil novo.

**Why:** Em 2026-05-20 sobrescrevi `magnesio-gummies/images/{results1,hf1,comparisontable,magnesiumcomparison,supplement-facts}.*` ao regenerar pra contexto intestino. Mas a PDP de SONO (`magnesio-gummies.html`) está EM PRODUÇÃO rodando pros outros 3 funis (ansiedade/enxaqueca/pressão) e usa essas mesmas imagens. Resultado: PDP de sono ficou exibindo imagens de constipação/intestino, quebrando promessa do funil que está vendendo. Guilherme: "tu vai me fuder aqui".

**How to apply:**
- Antes de regen via Gemini com mesmo filename: SEMPRE checar com `grep -rn "nome-do-arquivo" /c/projetos/relivia /c/Users/user/Desktop/Sanologia` se outras páginas usam.
- Se >1 página usa: criar nome novo com sufixo do funil (`-constipacao`, `-ansiedade`, etc).
- Editar SÓ o HTML do funil novo pra apontar pro arquivo novo.
- Em scripts Gemini de regen, default = novo filename. Só sobrescrever se Guilherme pedir explícito.
- Pasta `magnesio-gummies/` é compartilhada entre TODOS os funis de magnésio. Cada funil consome `magnesio-gummies.html` (sono) OU clones dela (`magnesio-gummies-constipacao.html` etc). Imagens com mesmo nome são serviças pra TODOS.
- Quando criar PDP dedicada por funil (`magnesio-gummies-{funil}.html`), TODA imagem nova/regenerada deve ter sufixo do funil.

Veja [[reference_estrutura_pasta_deploy]] e [[reference_repo_reliviabr_shop]].
