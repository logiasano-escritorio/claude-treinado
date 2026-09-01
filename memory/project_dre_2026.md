---
name: project-dre-2026
description: "DRE Sanologia/Relívia 2026 — estrutura, produtos rastreados e próximos passos pra automação via Yampi"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3a7eb6bb-8976-4b3d-8ebe-888710ee012b
---

DRE 2026 (Mai → Dez) em Google Sheets via Apps Script. Script base em `Sanologia/_dev/dre-apps-script.js` cria 8 abas mensais + Resumo Anual.

**Produtos rastreados (apenas estes 4):** Prime Gel, Prime Gotas, Sano Kids Magnésio, ProsaFlex.

**Estrutura DRE:**
- Receita Bruta → (−) Chargeback → (−) Imposto 6% faturamento → Receita Líquida
- (−) CPV (produto + frete + taxa Yampi default 4.99%) → Lucro Bruto
- (−) Marketing Meta Ads (por funil, com ROAS) → (−) Custos Fixos (Claude, Gemini, Cursos API, Utmify) → Lucro Líquido + Margem %

**Status (2026-05-19):** versão manual entregue. Plano de automação parado aguardando Guilherme cadastrar custo de produto + frete na Yampi (no cadastro do produto, não em planilha separada).

**Why:** Guilherme já tem planilha "Controle Tráfego - Sano" que puxa receita da Yampi via Apps Script. Mais fácil cadastrar custo lá uma vez e API retornar tudo junto, do que manter VLOOKUP de custos separado.

**How to apply:** Quando ele voltar com os custos cadastrados na Yampi, pedir (1) cópia/link da planilha "Controle Tráfego - Sano" pra reusar endpoint+token da API, (2) confirmação de SKU/ID dos 4 produtos na Yampi. Aí refazer o script: receita, custo, frete, unidades = automáticos via Yampi API; marketing e custos fixos = manual. Imposto 6% e taxa Yampi continuam fórmula.
