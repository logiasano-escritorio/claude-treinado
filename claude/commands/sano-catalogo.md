---
description: Mostra o catálogo completo de 39 ângulos Sano (B12, StrongBones, GlowUp) com mecanismo, prioridade e status (já produzido / pendente)
---

# Catálogo de Ângulos Sano

## Etapa 1 — Ler fontes

Leia em paralelo:
1. `C:/projetos/relivia/sano-energy-b12/CATALOGO-COPIES.md` — catálogo dos 39 ângulos
2. `c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/B12.md` — funis B12 já produzidos
3. `c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/StrongBones.md` — funis StrongBones já produzidos
4. `c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/GlowUp.md` — funis GlowUp já produzidos

## Etapa 2 — Cruzamento (matching de slug)

Para cada ângulo do catálogo, tente casar com os funis existentes do Obsidian. **Matching é por similaridade do slug** (não exato), porque slugs do catálogo e do Obsidian podem variar:

- Catálogo diz "Diabetes + Metformina" → Obsidian tem `diabetes-metformina` ✅
- Catálogo diz "Cãibras crônicas" → Obsidian tem `caimbras` ✅
- Catálogo diz "Pós-parto / amamentação" → Obsidian pode ter `pos-parto` ou `amamentacao` — **conta como produzido nos dois casos**

Se ângulo aparenta estar produzido mas o slug é muito diferente (ambíguo), marque com `❓ verificar`.

Marque cada ângulo:
- ✅ **Produzido** (slug bate ou é claramente o mesmo conceito)
- ❓ **Verificar** (parece bater mas slug diferente — usuário valida)
- ⏳ **Pendente** (só no catálogo)

## Etapa 3 — Output (3 tabelas, uma por produto)

### 🩸 B12 (8 ângulos)

| # | Ângulo | Mecanismo (1 linha) | Tier | Status | Comando ou URL |
|---|--------|---------------------|------|--------|----------------|

### 🦴 StrongBones (17 ângulos)

| # | Ângulo | Mecanismo (1 linha) | Tier | Status | Comando ou URL |
|---|--------|---------------------|------|--------|----------------|

### ✨ GlowUp (14 ângulos)

| # | Ângulo | Mecanismo (1 linha) | Tier | Status | Comando ou URL |
|---|--------|---------------------|------|--------|----------------|

**Coluna "Comando ou URL":**
- Se ⏳ pendente → `/sano-novo-funil <Produto> <#>`
- Se ✅ produzido → URL do advertorial (link clicável)
- Se ❓ verificar → mostra o slug encontrado e pergunta "É esse?"

## Etapa 4 — Top 5 próximos a fazer

Baseado em prioridade do catálogo (linha 127 do `CATALOGO-COPIES.md` em diante), liste 5 ângulos pendentes em ordem:

```
1. GlowUp #13 — Cabelo sem brilho/fio fino
   → /sano-novo-funil GlowUp 13

2. GlowUp #3 — Pós-parto / amamentação
   → /sano-novo-funil GlowUp 3

...
```

Se a lista de prioridade do catálogo já está toda produzida, sugira os próximos por **tamanho de audiência estimado** (Tier 1 > Tier 2 > Tier 3 do catálogo StrongBones).

## Etapa 5 — Resumo final

Linha simples no fim:
```
📊 Status: <X>/39 produzidos · <Y> pendentes · <Z> a verificar
💰 Custo total estimado pra completar tudo: ~$<Y * 0.60>
```

## Tom

Sem rodeios. Tabelas markdown limpas. Sem floreio. **Não inventa ângulo** que não está no catálogo — se o catálogo só tem 39, mostra 39.
