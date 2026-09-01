---
description: Mostra status de todos os funis Sano (no ar, em rascunho, pendentes) com verificação ao vivo das URLs
---

# Status dos Funis Sano

## Etapa 1 — Ler vault Obsidian

Leia em paralelo os 3 arquivos:
- `c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/B12.md`
- `c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/StrongBones.md`
- `c:/Users/user/Desktop/SANOLOGIA OBSIDIAN/GlowUp.md`

E o catálogo: `C:/projetos/relivia/sano-energy-b12/CATALOGO-COPIES.md`

## Etapa 2 — Verificar URLs ao vivo

Pra cada funil com status 🟢 No ar, faça `curl -sI -o /dev/null -w "%{http_code}"` na URL do advertorial e na URL da página. Capture o código HTTP.

```bash
# Exemplo
curl -sI -o /dev/null -w "%{http_code}" -L https://sanobrasil.com/adv-strongbones-artrose
```

**Marque:**
- ✅ se retornar 200
- ⚠️ se retornar 4xx/5xx (mostre o código no output)
- ⏱️ se der timeout/erro de conexão

Faça as verificações **em paralelo** (múltiplas chamadas Bash no mesmo turno) — não sequencial. Pode haver até 30 URLs pra checar.

## Etapa 3 — Cruzar catálogo

Compare os 39 ângulos do catálogo com o que já foi produzido. Marque cada ângulo como:
- ✅ Produzido (slug bate com algum funil do Obsidian)
- ⏳ Pendente (só no catálogo)

## Output esperado (3 blocos)

### 🟢 Funis no ar (com saúde)

Tabela com:
| Produto | Slug | Adv URL | Status Adv | Pag URL | Status Pag | Última atualização |

Status: ✅ 200 OK / ⚠️ <código> / ⏱️ erro

### 🔵⚪ Em desenvolvimento

Funis com status 🔵 (teste A/B), ⚪ (rascunho) ou 🟡 (legado). Mostre o que falta (ex: "imagens Gemini pendentes", "deploy não rodou", "página de produto não existe").

### ⏳ Próximos do catálogo

Top 5 ângulos pendentes em ordem de prioridade do próprio catálogo (linha 127 do CATALOGO-COPIES.md). Pra cada um:
- Produto + # ângulo
- Slug sugerido
- Mecanismo central (1 linha)
- Comando pronto: `/sano-novo-funil <Produto> <#>`

## Etapa 4 — Detectar inconsistências

Se algum funil 🟢 no Obsidian retornou ⚠️/⏱️ no curl, **avise no topo do output**:

```
⚠️ ATENÇÃO: 2 funis marcados como 🟢 no Obsidian estão com problema:
- StrongBones / artrose / adv → 404
- B12 / diabetes-metformina / página → timeout
Sugestão: rodar `git log --oneline -5` no repo Sanologia pra ver últimos deploys.
```

## Tom

Sem rodeios. Tabelas markdown limpas. Sem floreio. **Output do bloco 4 só aparece se houver inconsistência** — caso contrário, omita.
