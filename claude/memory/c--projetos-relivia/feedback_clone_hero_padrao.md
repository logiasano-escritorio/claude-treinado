---
name: Clone — Padrão de Galeria e Variant Picker (referência oregano.html)
description: Ao adicionar interatividade a um clone, galeria e variant picker devem seguir o padrão do oregano.html — classes rl-*, HTML limpo, JS readyState. Nunca usar o Swiper/Rapi Bundles original.
type: feedback
originSessionId: b24458c5-c7de-4a26-a4d7-22e9a63b7a7b
---
Quando o clone tem galeria de imagens e seletor de variante/bundle, o padrão de referência é `c:/projetos/relivia/oregano-relivia/oregano.html`. Nunca manter o Swiper.js do Shopify nem o Rapi Bundles — são dependências externas que não funcionam offline.

**Why:** O Swiper e o Rapi Bundles dependem de JS externo e estado do tema Shopify. No clone estático local esses scripts não carregam ou ficam quebrados. O padrão oregano.html é vanilla JS puro, sem dependências, testado e funcionando.

**How to apply:** Sempre que um clone tiver galeria ou variant picker, substituir pelo padrão abaixo antes de entregar.

---

## Estrutura HTML — Galeria

```html
<div id="rl-gallery" class="rl-gallery">
  <div class="rl-gallery__main">
    <div class="rl-gallery__slide active"><img src="assets/img1.webp" alt="..." /></div>
    <div class="rl-gallery__slide"><img src="assets/img2.webp" alt="..." /></div>
    <!-- mais slides -->
  </div>
  <div class="rl-gallery__arrows">
    <button class="rl-gallery__arrow" id="rl-prev">&#8592;</button>
    <span class="rl-gallery__counter" id="rl-counter">1 / N</span>
    <button class="rl-gallery__arrow" id="rl-next">&#8594;</button>
  </div>
</div>
```

- Usar imagens locais `assets/*.webp` (as primeiras 6-8 do Swiper original)
- Primeiro slide tem classe `active`
- Contador mostra `1 / N` onde N = total de slides

---

## Estrutura HTML — Variant Picker

```html
<div class="rl-variant-grid" id="rl-variants">

  <div class="rl-variant-card active"
       data-price="$XX.00"
       data-price-original="$YY.00"
       data-checkout="#checkout-1">
    <div class="rl-variant-card__check">✓</div>
    <div class="rl-variant-card__name">Nome do pack</div>
    <div class="rl-variant-card__sub">Subtítulo / economia</div>
    <div class="rl-variant-card__price">$XX.00 <del>$YY.00</del></div>
  </div>

  <div class="rl-variant-card"
       data-price="$XX.00"
       data-price-original="$YY.00"
       data-checkout="#checkout-2">
    <div class="rl-variant-card__check">✓</div>
    <div class="rl-variant-card__popular">⭐ MAIS POPULAR</div>
    <div class="rl-variant-card__name">Nome do pack</div>
    <div class="rl-variant-card__sub">Subtítulo / economia</div>
    <div class="rl-variant-card__price">$XX.00 <del>$YY.00</del></div>
  </div>

</div>

<button class="rl-btn-atc rl-btn-atc--lg" id="rl-main-cta">
  🛒 COMPRAR — $XX.00
</button>
```

- Extrair nomes, preços e subtítulos do Rapi Bundles original (`.rapi-bundles__bar-title`, `.rapi-money`, `.rapi-bundles__bar-subtitle`)
- Primeiro card com classe `active` = opção padrão selecionada
- `data-price` e `data-price-original` são os valores que o JS usa para atualizar o preço exibido

---

## JS — padrão obrigatório (readyState)

```javascript
<script>
(function init() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
    return;
  }

  /* Galeria */
  var slides = document.querySelectorAll('.rl-gallery__slide');
  var counter = document.getElementById('rl-counter');
  var current = 0;
  var total = slides.length;

  function showSlide(idx) {
    if (!total) return;
    slides[current].classList.remove('active');
    current = (idx + total) % total;
    slides[current].classList.add('active');
    if (counter) counter.textContent = (current + 1) + ' / ' + total;
  }

  var prev = document.getElementById('rl-prev');
  var next = document.getElementById('rl-next');
  if (prev) prev.addEventListener('click', function () { showSlide(current - 1); });
  if (next) next.addEventListener('click', function () { showSlide(current + 1); });

  /* Variant picker */
  var cards = document.querySelectorAll('.rl-variant-card');
  var priceEl = document.getElementById('rl-price');
  var compareEl = document.getElementById('rl-price-compare');
  var ctaBtn = document.getElementById('rl-main-cta');

  function selectCard(card) {
    cards.forEach(function (c) { c.classList.remove('active'); });
    card.classList.add('active');
    var price = card.getAttribute('data-price') || '';
    var compare = card.getAttribute('data-price-original') || '';
    if (priceEl) priceEl.textContent = price;
    if (compareEl) compareEl.textContent = compare;
    if (ctaBtn) ctaBtn.textContent = '🛒 COMPRAR — ' + price;
  }

  cards.forEach(function (card) {
    card.addEventListener('click', function () { selectCard(card); });
  });

})();
</script>
```

**Regra crítica ao fazer slicing para substituir JS antigo:**
- O `start` do slice deve apontar para o `<script>` de abertura, nunca para o conteúdo interno
- O `new_js` já contém `<script>...</script>` completo — não deixar o `<script>` antigo sobrando
```python
# CORRETO
start = content.rfind('<script>', 0, content.find('/* comentário do bloco */'))
end = content.find('</script>', start) + len('</script>')
content = content[:start] + new_js + content[end:]
```

---

## CSS mínimo necessário

```css
.rl-gallery__main { position: relative; width: 100%; aspect-ratio: 1/1; overflow: hidden; border-radius: 12px; background: #fff; }
.rl-gallery__slide { display: none; width: 100%; height: 100%; }
.rl-gallery__slide.active { display: flex; align-items: center; justify-content: center; }
.rl-gallery__slide img { width: 100%; height: 100%; object-fit: contain !important; background: #fff; }
.rl-gallery__arrows { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 12px; }
.rl-gallery__arrow { background: #fff; border: 2px solid currentColor; border-radius: 50%; width: 36px; height: 36px; font-size: 18px; cursor: pointer; }

.rl-variant-card { border: 2px solid rgba(0,0,0,.15); border-radius: 12px; padding: 14px 18px; cursor: pointer; position: relative; background: #fff; }
.rl-variant-card.active { border-color: var(--accent, #e6a4b4); background: rgba(0,0,0,.03); }
.rl-variant-card__check { position: absolute; right: 14px; top: 50%; transform: translateY(-50%); width: 22px; height: 22px; border-radius: 50%; border: 2px solid var(--accent, #e6a4b4); display: flex; align-items: center; justify-content: center; }
.rl-variant-card.active .rl-variant-card__check { background: var(--accent, #e6a4b4); color: #fff; }
```
