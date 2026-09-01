---
name: reference_utm_content_passagem_advertorial
description: "Medir passagem advertorial→PV no GA4 via ?utm_content=<slug-do-ângulo> no botão, sem duplicar a PV"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 829a6fdb-bacc-4b83-a6f6-88ba66d09ee6
---

Para saber **quantas pessoas passaram de cada advertorial pra página de venda** (a PV é compartilhada — ex: todos os adv-prime apontam pra `sanobrasil.com/prime-pv`), NÃO duplicar a PV. Em vez disso, cada botão do advertorial leva `?utm_content=<slug>`:

- Slug = **nome do arquivo** (o ângulo), não a pasta. Ex: `gaba-dor.html` → `?utm_content=gaba-dor`. `index.html` usa o nome da pasta (ex: `adv-prime-gabapentina`).
- No GA4: relatório da PV → breakdown por **"Manual content"** (dimensão do utm_content) → views por ângulo = passagens de cada advertorial.
- Vantagem sobre duplicar a PV: 1 só PV pra manter (preço/oferta muda em 1 arquivo), muda só a linha do `href`.

**Testado e comprovado (2026-07-14):** curl mantém o param (sem redirect que raspa), e DrissionPage capturou o hit GA4 `en=page_view tid=G-MSZ467D4KX` com `utm_content=gaba-dor` na `dl`. Funciona ponta a ponta.

Aplicar em massa (git bash, `**` não expande — usar grep pra listar):
```bash
for f in $(grep -rl 'href="https://sanobrasil.com/prime-pv"' adv-prime-gabapentina/*.html); do
  slug=$(basename "$f" .html); [ "$slug" = "index" ] && slug=$(basename "$(dirname "$f")")
  sed -i "s|prime-pv\"|prime-pv?utm_content=$slug\"|g" "$f"
done
```

**Pegadinha da URL na live:** `sanobrasil.com/adv-.../gaba-dor` (SEM `.html`) → 200; com `.html` → 308 redirect. Ao validar na live, bater sem `.html`.

Ver [[feedback_link_anuncio_sempre_advertorial]], [[reference_pixels_meta_por_produto]].
