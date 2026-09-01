---
name: feedback-rota-amigavel-quebra-img-relativa
description: "Rota amigável no vercel.json quebra src=\"images/...\" relativo — o browser resolve a partir da raiz e dá 404; curl no caminho da pasta mente que está OK"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2d40f027-d6b6-4715-b928-8f4ee0716de3
  modified: 2026-08-21T13:57:59.768Z
---

Quando uma página ganha rota amigável no `vercel.json` (ex: `/adv-ciatica-1` →
`/magnesio-ciatica/adv-ciatica-celulas-zumbis`), todo `src="images/..."`
**relativo** quebra: o browser resolve a partir da URL visitada, ou seja
`sanobrasil.com/images/...` → **404**.

**Why:** o advertorial de ciática subiu com as 23 imagens quebradas na live
mesmo depois de eu validar com curl. O curl passou porque testei
`sanobrasil.com/magnesio-ciatica/images/x.webp` (200), mas o browser, na rota
`/adv-ciatica-1`, pedia `sanobrasil.com/images/x.webp` (404). Os dois testes
eram verdadeiros e a página estava quebrada mesmo assim.

**How to apply:**
- Página com rota amigável → usar caminho **absoluto**:
  `src="/pasta/images/x.webp"`. Sem rota amigável, o relativo funciona.
- Validar deploy **renderizando** (DrissionPage), nunca só com curl:
  `Array.from(document.images).filter(im=>!im.complete||im.naturalWidth===0)`
  — depois de remover `loading="lazy"` e esperar o carregamento.
- Testar a URL **que o anúncio vai usar** (a rota amigável), não o caminho
  interno do arquivo.

Ver [[feedback_trocar_inclui_deploy]] e
[[feedback_dois_chats_disco_compartilhado_deploy]].
