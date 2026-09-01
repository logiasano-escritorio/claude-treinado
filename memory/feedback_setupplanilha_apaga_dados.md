---
name: feedback-setupplanilha-apaga-dados-cuidado
description: "NUNCA recomendar rodar setupPlanilha() na planilha Controle Tráfego Sano sem AVISAR — ela faz sh.clear() em Pedidos e Custos, apagando tudo"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fda4c240-53cf-4717-a6b1-266a11839ad6
---

🚫 **NUNCA recomende rodar `setupPlanilha()` na planilha Controle Tráfego Sano sem aviso EXPLÍCITO de que vai apagar dados.**

**Por quê:** A função `setupPlanilha()` em `_dev/yampi-webhook/Code.gs` chama internamente:
- `criarAbaPedidos_(ss)` → fazia `sh.clear()` (APAGAVA pedidos)
- `criarAbaCustos_(ss)` → fazia `sh.clear()` (APAGAVA cadastro de custos da Yampi)
- `criarAbasCPA_(ss)` → também recria abas CPA
- `criarAbaDashboard_(ss)` → OK, esse só recria Dashboard

**Histórico:** Em 2026-05-19 o user reclamou que rodou setupPlanilha pra criar a aba Config (porque criarAbaConfig_ era privada) e isso apagou os 24 custos da aba Custos que ele tinha sincronizado da Yampi.

**Fix aplicado em 2026-05-19:** ambas `criarAbaPedidos_` e `criarAbaCustos_` agora PRESERVAM dados se a aba já existir com conteúdo. Só re-aplicam headers + formatação. Pra forçar reset, usar funções dedicadas (`cadastrarTodosProdutosYampi` pra Custos, `limparAbaPedidos` pra Pedidos — ambas pedem confirmação).

**Como aplicar:**
- Se user quer adicionar/recriar UMA aba específica (Config, Dashboard, etc), usar wrapper público dedicado (`criarAbaConfig`, `recriarDashboard`), NÃO setupPlanilha.
- Se realmente precisar rodar setupPlanilha, AVISAR antes: "isso vai re-aplicar headers em Pedidos/Custos mas preserva dados (correção 2026-05-19)".
- Em planilha NOVA (sem nenhuma aba), setupPlanilha é seguro.
