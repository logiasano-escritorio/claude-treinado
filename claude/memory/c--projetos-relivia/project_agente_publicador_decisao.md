---
name: Decisão — Agente Publicador fora do pipeline
description: Agente Publicador existe mas está fora do fluxo automático até o pipeline ser validado
type: project
originSessionId: c21e05d4-217b-4244-84d6-642f9888fa32
---
Agente Publicador (`agente-publicador/agente_publicador.py`) está fora do pipeline automático por decisão do usuário.

**Why:** Precisa revisar manualmente o output completo (advertorial + página produto + criativos + textos) antes de publicar qualquer coisa no Meta.

**How to apply:** Nunca conectar o Agente Publicador ao final de nenhum agente automaticamente. Ele só roda via chamada manual após aprovação do usuário. Quando o pipeline estiver validado e o usuário pedir para ativar, conectar ao final do Agente Produto.
