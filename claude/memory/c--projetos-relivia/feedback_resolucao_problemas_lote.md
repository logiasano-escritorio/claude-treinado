---
name: Protocolo de resolução de problemas em lote
description: Como lidar quando há muitos problemas acumulados para resolver — ordem, agrupamento por dependência, persistência entre sessões e uso de TodoWrite
type: feedback
originSessionId: eee4c79a-9468-4f05-abe9-e209538d91c1
---
Quando há 10+ problemas para resolver, NÃO mandar tudo de uma vez nem resolver um por um isoladamente.

**Regra**: agrupar por dependência e resolver grupo por grupo, pedindo confirmação entre grupos.

**Why:** Problemas têm dependências entre si — resolver na ordem errada pode exigir retrabalho. Ex: criar manifesto de run (#13) muda como a correlação de runs (#5) deve ser corrigida. Se #5 for resolvido antes, o código fica inconsistente.

**How to apply:**

1. **Levantar todos os problemas primeiro** — listar completo antes de tocar qualquer código
2. **Identificar dependências** — qual problema bloqueia ou afeta qual
3. **Montar grupos ordenados**:
   - Grupo 1 — Base: problemas que os outros dependem
   - Grupo 2 — Correções de infraestrutura
   - Grupo 3 — Correções por agente
   - Grupo 4 — Otimizações (sem urgência)
4. **Dentro de cada grupo**: resolver em paralelo (independentes entre si)
5. **Entre grupos**: confirmar com o usuário antes de avançar
6. **Usar TodoWrite** durante a execução para rastrear progresso dentro da sessão

**Para não esquecer entre sessões:**
- Salvar a lista de pendências no Obsidian ao final de cada sessão
- Na próxima sessão: "consulte o Obsidian, há uma lista de problemas pendentes dos agentes"
- O arquivo no Obsidian deve ter: problema, grupo, status (pendente/resolvido), arquivo afetado

**Exemplo de estrutura no Obsidian:**
```
## Pendencias — Agentes Relivia (2026-04-12)

### Grupo 1 — Base
- [ ] #13 Manifesto de run compartilhado — agente_funil.py + agente_clone.py + agente_traducao.py
- [ ] #5 Correlação de runs no Revisor — agente_revisor.py

### Grupo 2 — Correções no Revisor
- [ ] #6 Placeholder JPEG corrompido — agente_revisor.py _correcao_images_vazia()
- [ ] #12 Validação HTML fechado — io_contracts.py validar_output_agente2()
...
```
