---
name: feedback-manifesto-antes-de-subir
description: NUNCA subir anúncio no Meta sem manifesto local documentado — copy + imagem + nome do ad registrados antes de qualquer upload
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 931f846c-f489-4901-9b80-db81b355e580
---

REGRA INVIOLÁVEL: Todo anúncio Meta deve ter um manifesto local ANTES de ser subido. Nunca criar ad-hoc pelo Ads Manager.

**Por que:** O Meta pode reprovar, apagar ou bloquear qualquer anúncio a qualquer momento. Quando isso acontece, a copy e a imagem somem da interface. Sem manifesto local, o criativo campeão se perde para sempre — sem como saber qual imagem era, qual texto era, qual combinação vendia.

**Caso real:** Campanha PRIME_JOELHO teve 40 ads reprovados em massa. A copy campeã (PRIME_JOELHO_COPYC_A09-medico-apontando) e a imagem foram recuperadas APENAS porque existia o manifesto em `_dev/manifestos-prime/joelho.manifest.json`, com o campo `ad_name → image_path → message_file` para cada ad.

**Ao trocar de conta de anúncio:** o manifesto é o que permite resubir tudo — mesmo criativo, mesma copy, mesma estrutura — em conta nova sem perder nada.

**Como aplicar:**
- Estrutura obrigatória: `ad_name`, `image_path` (relativo a Sanologia/), `message_file` (relativo ao manifesto)
- Salvar em `_dev/manifestos-prime/[produto].manifest.json` antes do primeiro upload
- Script de subida deve ler do manifesto, nunca subir manual
- Padrão já validado: `joelho.manifest.json`, `lombar.manifest.json`, etc.

**Why:** "Imagina se a gente não tivesse isso organizado? Eu ia perder o meu criativo campeão e nem ia saber qual era." — Guilherme, após recuperar copy campeã que Meta havia apagado da interface.
