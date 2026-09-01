---
name: Calculadora de margem Relívia
description: Calculadora HTML single-file de margem/CPA/ROAS pros 3 produtos Relívia (Óleo Orégano, AlinhaFácil, RoncoZero). Espelha estrutura da Sano mas vive na pasta de projetos da Relívia.
type: reference
originSessionId: 3343f885-744a-482b-b67d-72d1507854f5
---
Localização: `C:\projetos\relivia\_dev\calc-margem-relivia.html` (NÃO em Sanologia/_dev — usuário separou explicitamente)

Estrutura: HTML+CSS+JS em arquivo único, sem build. Espelha `Sanologia/_dev/calc-margem.html` (versão Sano) mas com:
- 3 abas: Óleo de Orégano, AlinhaFácil, RoncoZero
- Tiers reais (Orégano: 1/3/5 potes; AlinhaFácil: por faixa de peso; RoncoZero: kits R$297/R$499)
- COGS reais: Orégano R$23,22 (com frete embutido); AlinhaFácil R$50; RoncoZero R$50
- Bloco extra "Cenário real do período" que a Sano não tem — mostra DRE completa do período (receita, ads em R$, COGS estimado, frete, gateway, imposto, lucro, margem) com defaults dos números 04/05–09/05/2026
- localStorage key: `relivia-calc-margem-v1` (separado da Sano `sano-calc-margem-v1`)

Câmbio default usado nos defaults: USD × 4,92.
