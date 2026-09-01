---
name: Facebook Ads — sempre criar como rascunho (PAUSED)
description: Nunca publicar campanhas, conjuntos ou anúncios automaticamente — sempre deixar como PAUSED para revisão manual
type: feedback
originSessionId: d1aaa8e5-ea41-4920-8cdf-267024a4c422
---
Sempre criar campanhas, conjuntos e anúncios com `status=PAUSED`.

**Why:** O usuário quer revisar antes de ativar qualquer coisa no Ads Manager. Publicar sem revisão é inaceitável.

**How to apply:** Em toda chamada à API do Facebook Ads (campaigns, adsets, ads), sempre usar `status=PAUSED`. Nunca usar `ACTIVE` na criação, mesmo que o usuário não mencione explicitamente.
