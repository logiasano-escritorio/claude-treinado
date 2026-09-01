---
name: reference_frete_loggi_yampi
description: "Como montar a planilha de frete dinâmico Yampi a partir da proposta Loggi (origem SC, SANO Suplementos)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4d8463a7-3496-47b7-9c62-23cc1cc3cbfd
---

Planilha de frete Yampi (modelo "Faixas de CEP", 9 colunas: regiao, cep_inicial, cep_final, peso_inicial, peso_final, valor_frete, valor_extra_por_peso, dias_para_entrega, porcentagem_adicional) preenchida com a **Proposta Comercial Loggi - SANO SUPLEMENTOS (Pulverizada)**. Origem **Itapema/SC**.

**Estrutura da proposta Loggi** (`Downloads/Proposta Comercil Loggi ... Pulverizada..xlsx`):
- Aba "Tabela de Abrangência" (30.308 faixas de CEP): cada faixa tem Estado, Região (Capital/Interior/Cap-e-Int), Abrangência (**Malha Loggi** ou **Redespacho**), Região de precificação (ex: SP CAP, GO INT 4, SP RED), %GRIS, Multiplicador de Risco (1/2/3/5), %AdValorem, Prazo.
- Aba "Tabela de Preços": 2 tabelas. **Express/Malha** (114 colunas, 1 por sub-região de precificação, faixas de peso 0-30kg + KG adicional). **Redespacho** (25 colunas = 1 por UF, exceto TO que NÃO tem preço de Redespacho).
- Cubagem: **167 kg/m³**. Cobra o MAIOR entre peso real e cubado.

**Fórmula oficial do preço (validada contra o Simulador):**
`Preço total = (tabela + GRIS + AdValorem) / (1 − ICMS%)` — ICMS "por dentro" (gross-up sobre o serviço).
- GRIS = 0,45% × ValorNF × **Multiplicador de risco** (mult só multiplica o GRIS, não o AdValorem)
- AdValorem = 0,45% × ValorNF
- ICMS origem SC por destino: **7%** (maioria N/NE/CO), **12%** (MG, PR, RJ, RS, SP), **17%** (SC interno). PIS/COFINS já inclusos na tabela.

**Decisões do Guilherme (2026-07):**
- NUNCA absorver prejuízo de Redespacho → 1 linha por faixa CEP real (não usar as 58 regiões contíguas do modelo). CEP de Redespacho paga Redespacho; cliente paga ou abandona.
- Valor de NF médio fixo = **R$300** (ticket kit 2-3 potes).
- Produtos SANO (Prime Creme etc.): caixa **20×30×4cm** → cubado 0,401kg. Kits 1-7un pesam 107g a 749g → todos ≤0,75kg. Cobre em **2 faixas de peso: 0-0,5 e 0,501-1kg**. Gerar 31 faixas até 30kg = 920k linhas (Yampi trava); 2 faixas = ~60k linhas.

**Output:** `Downloads/Frete Loggi - Yampi - SANO.xlsx`, 60.206 linhas, 0 overlaps, 27 UFs. Faltam 205 CEPs de **TO-Redespacho** (Loggi não deu preço na proposta) — deixados de fora de propósito. Script inline (não salvo em arquivo .py). Ver [[reference_yampi_api_fields_dossie]].

**Config na tela Yampi (Frete por planilha):**
- A Yampi CUBA sozinha — a planilha NÃO embute cubagem, só faixas de peso normais (0-0,5 / 0,501-1kg). Yampi pega dimensões do produto cadastrado, cuba, pega maior(real, cubado), busca a linha da planilha, aplica % adicional. Não recalcula preço.
- **Fator de cubagem Yampi = 5988** (=1.000.000÷167; a Yampi usa formato DIVISOR cm³, não kg/m³. Pode usar 6000, dá igual).
- CEP origem 88220-000 (SC, região Itapema). Peso máx/embalagem = 1kg. % adicional = 0.
- **PRÉ-REQUISITO:** cada produto na Yampi PRECISA ter dimensões (20×30×4cm) + peso real cadastrados, senão a cubagem não roda e cobra pelo peso real (menor → prejuízo).
- Versão final = 2 faixas de peso (até 1kg, 60k linhas). Até 3kg dá 120k linhas (pode travar import).
- **PEGADINHA: Yampi só importa `.xls` (BIFF/CDFV2), NÃO `.xlsx`.** Import travou em "Importando 0 de 0 / 0%" quando subi .xlsx — ela abre mas não lê linha nenhuma. Gerar com **xlwt** (não openpyxl). Aba deve se chamar "Worksheet"; CEP/pesos/valores como FLOAT (não int); coluna regiao=texto. Limite .xls = 65.536 linhas (60k cabe). Fator cubagem Yampi = **6000** (dropdown: "Peso cúbico" / "for maior que" / Peso real ou 0 Kg).
