# Adaptar Página de Produto HTML — Estilo Shopify / Pulso Luz

Você é especialista em criar landing pages standalone em HTML para marcas de produto direto ao consumidor, no estilo de páginas de produto Shopify de alta conversão.

## PASSO 0 — Leitura obrigatória antes de iniciar

Leia o arquivo:
`C:/Users/user/.claude/projects/c--Users-user--claude/memory/MEMORY.md`

---

## PASSO 1 — Coletar dados do usuário

Pergunte ao usuário todos de uma vez:

1. **Nome da marca** (ex: "Relívia", "VitaMax", "BioFlex")
2. **Nome do produto** (ex: "PulsoLuz™", "FlexiBack Pro™")
3. **Handle/slug do produto** (ex: `pulsoluz`, `flexiback-pro`) — usado para nomes de pasta e arquivo
4. **Variantes e preços** — ex: "1 un R$197 / 3 un R$397 / 6 un R$597"
5. Os **4 inputs de conteúdo**:
   - **HTML da página de referência** — colar ou fornecer o arquivo
   - **Textos extraídos** via console:
     `copy(document.getElementById('MainContent')?.innerText || document.body.innerText)`
   - **Imagens extraídas** via console:
     `copy(Array.from(document.querySelectorAll('img')).map(i=>i.src).filter(s=>!s.includes('svg')&&s.length>10).join('\n'))`
   - **Headings extraídos** via console:
     `copy(Array.from(document.querySelectorAll('h1,h2,h3')).map(h=>h.tagName+': '+h.innerText.trim()).join('\n'))`

---

## PASSO 2 — Analisar o conteúdo recebido

Com o HTML + textos + imagens + headings, extrair:

- Título principal e tagline do produto
- Proposta de valor e benefícios principais
- Seções presentes e sua ordem (seguir a estrutura da referência — não usar ordem fixa)
- Depoimentos (nomes, textos, estrelas)
- FAQ (perguntas e respostas)
- Dados técnicos / especificações
- Estudos ou estatísticas citadas
- Nomes de médicos/especialistas mencionados
- Textos de garantia
- Todas as imagens com URL — usar diretamente no HTML

---

## PASSO 3 — Gerar o HTML completo

### Estrutura de saída
- HTML: `C:/Users/user/Desktop/[handle]/[handle].html`
- CSS: `C:/Users/user/Desktop/[handle]/style.css`

### Visual — estilo Shopify de alta conversão

A página deve ter aparência profissional de produto Shopify:
- Header fixo com logo + botão de compra
- Hero em grid 2 colunas: galeria de produto à esquerda, bloco de compra à direita
- Seções content marketing alternando fundo branco/cinza
- Cards de depoimento em grid 3 colunas
- Tabela comparativa com destaque na coluna do produto
- FAQ em accordion limpo
- CTA final em fundo verde com urgência
- Footer escuro com 3 colunas

### Seções disponíveis (ordenar conforme referência)

| Seção | Classe/estrutura |
|---|---|
| Header fixo | `.site-header` |
| Hero / produto | `.product-section` → `.product-grid` → `.gallery` + `.product-info` |
| Image-with-text | `.iwt-section.iwt-section--gray` ou `--white` → `.iwt-grid` |
| Rich text centralizado | `.rtext-section.rtext-section--white` ou `--gray` → `.rtext` |
| Stats / estudos | `.stats-grid` → `.stat-card` |
| Médico / especialista | `.doctor-section` → `.doctor-grid` |
| Como usar (3 passos) | `.multirow-section` → `.multirow` → `.multirow-row` |
| Depoimentos | `.section.section--gray` → `.tgrid` → `.tcard` |
| Tabela comparativa | `.comparison-section` → `.ctable-wrap` → `.ctable` |
| Accordion specs/FAQ | `.accordion-section` → `.accordion` → `.acc-item` |
| Garantia | `.iwt-section` com imagem de garantia |
| Quem somos | `.section.section--gray` → `.about-grid` |
| Wave divider | `.wave` com SVG verde |
| CTA final | `.cta-section` |
| Footer | `.site-footer` |

### Paleta padrão (SEMPRE usar — não alterar)

```css
--green:      #00C853   /* botões, preços, badges, acentos, CTA bg */
--green-dark: #00A846   /* hover, wave fill */
--black:      #111111   /* texto, footer bg */
--white:      #ffffff
--gray:       #F5F6F8   /* seções alternadas, cards */
--text:       #111111
--muted:      #666666
--border:     #e2e4e9
--stars:      #ffcc00
```

### Regras de geração

1. **Imagens:** usar as URLs extraídas diretamente — nunca placeholders quando URL disponível
2. **Textos:** adaptar copy da referência com nome do produto/marca fornecidos — manter tom persuasivo PT-BR
3. **Variantes:** `data-checkout="LINK_CHECKOUT_1"` etc. como placeholder
4. **Especialistas/médicos:** sempre Dr. + nome masculino brasileiro
5. **Galeria:** usar imagens de produto extraídas nos slides
6. **Estrutura:** seguir a ordem das seções da referência

### Hero — padrão obrigatório

```html
<section class="product-section">
  <div class="product-grid">
    <div class="gallery">
      <div class="gallery__main">
        <div class="gallery__slide active"><img src="[URL_IMG_1]" alt="[produto] 1" /></div>
        <!-- slides adicionais -->
      </div>
      <div class="gallery__arrows">
        <button class="gallery__arrow" onclick="galleryNav(-1)">&#8592;</button>
        <span class="gallery__counter" id="js-counter">1 / N</span>
        <button class="gallery__arrow" onclick="galleryNav(1)">&#8594;</button>
      </div>
    </div>
    <div class="product-info">
      <h1 class="product-title">[TÍTULO PRINCIPAL]</h1>
      <p class="product-subtitle">[TAGLINE]</p>
      <div class="stars-row"><span class="stars">★★★★★</span><span class="stars-label"><strong>([N] Avaliações Verificadas)</strong></span></div>
      <div class="badge--social">🔥 <strong>100+ pedidos</strong>&nbsp;nas últimas 24 horas</div>
      <div class="price-block">
        <span class="badge--discount">🏷️ [X]% DESCONTO</span>
        <div class="price-row">
          <span class="price-current" id="js-price">R$ [PREÇO]</span>
          <span class="price-original">R$ [ORIGINAL]</span>
        </div>
      </div>
      <div class="variant-label">Escolha seu kit:</div>
      <div class="variant-grid" id="js-variants">
        <!-- variant-cards -->
      </div>
      <a href="LINK_CHECKOUT_1" class="btn btn--green btn--green-lg js-cta-btn">🛒 [CTA PRINCIPAL]</a>
      <div class="trust-bar">
        <div class="trust-bar__item"><span class="icon">🔒</span> Pagamento 100% Seguro</div>
        <div class="trust-bar__item"><span class="icon">🚚</span> Frete Grátis</div>
        <div class="trust-bar__item"><span class="icon">↩️</span> 90 Dias ou Seu Dinheiro de Volta</div>
      </div>
      <div class="badge--urgency">⚠️ ACABANDO! | 17 Unidades Restantes</div>
    </div>
  </div>
</section>
```

### Wave divider — cor verde

```html
<div class="wave" style="background:var(--gray);">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 90" preserveAspectRatio="none">
    <path fill="#00C853" d="M0,45 C180,90 360,0 540,45 C720,90 900,0 1080,45 C1260,90 1380,18 1440,45 L1440,90 L0,90 Z"/>
  </svg>
</div>
```

### CTA final — fundo verde

```html
<section class="cta-section">
  <h2>[TÍTULO CTA FINAL]</h2>
  <p>[SUBTÍTULO PERSUASIVO]</p>
  <a href="LINK_CHECKOUT_1" class="btn btn--white js-cta-btn">🛒 [CTA TEXTO]</a>
  <div class="urgency-note">⚠️ ACABANDO! | Apenas 17 unidades restantes</div>
</section>
```

### Footer — Relívia (padrão)

```html
<footer class="site-footer">
  <div class="footer-grid">
    <div class="footer-col">
      <div class="footer-brand"><img src="https://reliviaonline.shop/images/logorelivia.png" alt="Relívia" /></div>
      <p class="footer-tagline">Saúde, bem-estar e qualidade de vida há mais de 14 anos.</p>
    </div>
    <div class="footer-col">
      <div class="footer-title">📞 Atendimento Relívia</div>
      <p class="footer-sub">Central de Suporte ao Cliente</p>
      <ul class="footer-info">
        <li>📧 <a href="mailto:suporte@relivia.com.br">suporte@relivia.com.br</a></li>
        <li>📱 <a href="https://wa.me/551151995945">(11) 5199-5945</a></li>
        <li>🕐 Seg–Sex: 08h às 18h · Sáb: 09h às 13h</li>
      </ul>
    </div>
    <div class="footer-col">
      <div class="footer-title">📍 Centro de Distribuição</div>
      <ul class="footer-info">
        <li>Av. Dr. Antonio João Abdalla, 2010</li>
        <li>Empresarial Colina — Cajamar/SP</li>
        <li>CEP 07.750-020</li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2025 Relívia — Todos os direitos reservados</p>
    <p><a href="#">Política de Privacidade</a> · <a href="#">Termos de Uso</a> · <a href="#">Trocas e Devoluções</a></p>
  </div>
</footer>
```

Para outras marcas, adaptar com dados fornecidos pelo usuário.

### JS obrigatório no final do body

```js
/* Accordion */
function toggleAcc(btn) {
  const item = btn.closest('.acc-item');
  const isOpen = item.classList.contains('open');
  document.querySelectorAll('.acc-item').forEach(i => i.classList.remove('open'));
  if (!isOpen) item.classList.add('open');
}

/* Variant picker */
document.querySelectorAll('.variant-card').forEach(card => {
  card.addEventListener('click', () => {
    document.querySelectorAll('.variant-card').forEach(c => c.classList.remove('active'));
    card.classList.add('active');
    const url = card.dataset.checkout;
    const price = card.dataset.price;
    const priceOriginal = card.dataset.priceOriginal;
    document.querySelectorAll('.js-cta-btn').forEach(btn => btn.href = url);
    const priceEl = document.getElementById('js-price');
    if (priceEl && price) priceEl.textContent = price;
    const originalEl = document.querySelector('.price-original');
    if (originalEl && priceOriginal) originalEl.textContent = priceOriginal;
  });
});

/* Galeria com setas */
const galleryImages = document.querySelectorAll('.gallery__slide');
let currentSlide = 0;
function galleryNav(dir) {
  if (galleryImages.length === 0) return;
  galleryImages[currentSlide].classList.remove('active');
  currentSlide = (currentSlide + dir + galleryImages.length) % galleryImages.length;
  galleryImages[currentSlide].classList.add('active');
  document.getElementById('js-counter').textContent = (currentSlide + 1) + ' / ' + galleryImages.length;
}
```

---

## PASSO 4 — Gerar o style.css

Gerar o `style.css` completo com a paleta verde. Usar exatamente este CSS como base:

```css
/*
 * ============================================================
 *  Design System — Páginas de Produto
 *  Paleta: Verde #00C853 + Preto #111111
 * ============================================================
 */

/* ===== RESET ===== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: 'Poppins', sans-serif;
  color: #111111;
  background: #fff;
  line-height: 1.6;
}
img { max-width: 100%; display: block; }
a { text-decoration: none; }

/* ===== CSS VARIABLES ===== */
:root {
  --green:      #00C853;
  --green-dark: #00A846;
  --white:      #ffffff;
  --gray:       #F5F6F8;
  --border:     #e2e4e9;
  --text:       #111111;
  --muted:      #666666;
  --stars:      #ffcc00;
}

/* ===== TIPOGRAFIA ===== */
h1, h2, h3, h4 { line-height: 1.3; color: var(--text); }
p { line-height: 1.75; }

/* ===== LAYOUT ===== */
.container { max-width: 1200px; margin: 0 auto; }
.section       { padding: 56px 24px; }
.section--white { background: var(--white); }
.section--gray  { background: var(--gray); }

/* ============================================================
   HEADER
   ============================================================ */
.site-header {
  position: sticky;
  top: 0;
  z-index: 200;
  background: var(--white);
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.site-logo img {
  height: 44px;
  width: auto;
  display: block;
}

/* ============================================================
   BOTÕES
   ============================================================ */
.btn {
  display: inline-block;
  border: none;
  cursor: pointer;
  font-family: 'Poppins', sans-serif;
  transition: all .2s ease;
  text-align: center;
  font-weight: 700;
  letter-spacing: .5px;
}

.btn--green {
  background: var(--green);
  color: var(--white);
  padding: 12px 28px;
  border-radius: 7px;
  font-size: 15px;
  text-transform: uppercase;
  box-shadow: 0 4px 14px rgba(0,200,83,.28);
}
.btn--green:hover {
  background: var(--green-dark);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0,200,83,.38);
}

.btn--green-lg {
  display: block;
  width: 100%;
  padding: 18px 24px;
  font-size: 18px;
  border-radius: 8px;
}

.btn--white {
  background: var(--white);
  color: var(--green);
  padding: 18px 52px;
  border-radius: 8px;
  font-size: 18px;
  text-transform: uppercase;
  box-shadow: 0 4px 20px rgba(0,0,0,.15);
}
.btn--white:hover {
  transform: translateY(-2px);
  box-shadow: 0 7px 26px rgba(0,0,0,.22);
}

/* ============================================================
   BADGES & SELOS
   ============================================================ */
.badge--discount {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--green);
  color: var(--white);
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 700;
  width: fit-content;
}

.badge--social {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--green);
  color: var(--white);
  padding: 6px 16px;
  border-radius: 30px;
  font-size: 13px;
  font-weight: 600;
  width: fit-content;
}

.badge--urgency {
  background: var(--green);
  color: var(--white);
  padding: 11px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  text-align: center;
  animation: pulse 2.2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.72} }

.trust-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
  padding: 12px 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}
.trust-bar__item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--muted);
}
.trust-bar__item .icon { font-size: 18px; }

/* ============================================================
   ESTRELAS & AVALIAÇÃO
   ============================================================ */
.stars-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.stars { color: var(--stars); font-size: 20px; letter-spacing: 1px; }
.stars-label { font-size: 14px; color: var(--muted); }

/* ============================================================
   PREÇO
   ============================================================ */
.price-block { display: flex; flex-direction: column; gap: 8px; }
.price-row   { display: flex; align-items: baseline; gap: 12px; }
.price-current  { font-size: 38px; font-weight: 700; color: var(--green); }
.price-original { font-size: 20px; color: #b4b4b4; text-decoration: line-through; }

/* ============================================================
   SELETOR DE VARIANTE
   ============================================================ */
.variant-label {
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: var(--muted);
  margin-bottom: 10px;
}
.variant-grid { display: flex; gap: 12px; flex-wrap: wrap; }
.variant-card {
  flex: 1;
  min-width: 130px;
  border: 2px solid var(--border);
  border-radius: 10px;
  padding: 14px 12px;
  cursor: pointer;
  transition: all .2s;
  text-align: center;
  position: relative;
  background: var(--white);
}
.variant-card:hover,
.variant-card.active {
  border-color: var(--green);
  background: rgba(0,200,83,.04);
}
.variant-card__name   { font-weight: 700; font-size: 15px; color: var(--text); }
.variant-card__sub    { font-size: 12px; color: var(--muted); margin-top: 2px; }
.variant-card__price  { font-size: 17px; font-weight: 700; color: var(--green); margin-top: 8px; }
.variant-card__popular {
  background: var(--green);
  color: var(--white);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .8px;
  padding: 2px 10px;
  border-radius: 30px;
  width: fit-content;
  margin: 0 auto 6px;
}
.variant-card__check  {
  position: absolute;
  top: -10px; right: -10px;
  width: 22px; height: 22px;
  background: var(--green);
  border-radius: 50%;
  color: var(--white);
  font-size: 11px;
  display: none;
  align-items: center;
  justify-content: center;
}
.variant-card.active .variant-card__check { display: flex; }

/* ============================================================
   GALERIA DE PRODUTO
   ============================================================ */
.gallery { display: flex; flex-direction: column; gap: 10px; }
.gallery__main {
  border-radius: 14px;
  overflow: hidden;
  aspect-ratio: 1 / 1;
  background: var(--gray);
}
.gallery__main img { width: 100%; height: 100%; object-fit: cover; }
.gallery__arrows {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 8px 0;
}
.gallery__arrow {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: var(--white);
  color: var(--text);
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all .2s;
  line-height: 1;
}
.gallery__arrow:hover {
  border-color: var(--green);
  color: var(--green);
  background: rgba(0,200,83,.05);
}
.gallery__counter {
  font-size: 13px;
  color: var(--muted);
  min-width: 36px;
  text-align: center;
}
.gallery__slide { display: none; width: 100%; height: 100%; }
.gallery__slide.active { display: block; }
.gallery__slide img { width: 100%; height: 100%; object-fit: cover; }

/* ============================================================
   SEÇÃO PRODUTO (HERO)
   ============================================================ */
.product-section { padding: 36px 24px; background: var(--white); }
.product-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 52px;
  max-width: 1200px;
  margin: 0 auto;
  align-items: start;
}
.product-info { display: flex; flex-direction: column; gap: 18px; }
.product-title { font-size: 27px; font-weight: 700; line-height: 1.3; color: var(--text); }
.product-subtitle { font-size: 15px; color: var(--muted); }

/* ============================================================
   SEÇÃO SOBRE / QUEM SOMOS
   ============================================================ */
.about-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 52px;
  max-width: 1200px;
  margin: 0 auto;
  align-items: center;
}
.about-img { border-radius: 16px; overflow: hidden; aspect-ratio: 4/3; background: var(--border); }
.about-img img { width:100%; height:100%; object-fit:cover; }
.about-content h2 { font-size: 32px; font-weight: 700; color: var(--text); margin-bottom: 18px; }
.about-content h2 em { color: var(--green); font-style: normal; }
.about-content p { font-size: 15px; color: #444; margin-bottom: 12px; }
.about-content strong { color: var(--text); }

/* ============================================================
   DEPOIMENTOS
   ============================================================ */
.section-heading { text-align: center; font-size: 30px; font-weight: 700; margin-bottom: 6px; color: var(--text); }
.section-sub {
  text-align: center;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  color: var(--muted);
  margin-bottom: 36px;
}
.tgrid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}
.tcard {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.tcard__img     { aspect-ratio: 1; border-radius: 10px; overflow: hidden; background: var(--gray); }
.tcard__img img { width:100%; height:100%; object-fit:cover; }
.tcard__stars   { color: var(--stars); font-size: 17px; }
.tcard__title   { font-size: 15px; font-weight: 700; line-height: 1.4; color: var(--text); }
.tcard__text    { font-size: 14px; color: #555; line-height: 1.65; }
.tcard__author  { font-size: 13px; color: var(--muted); font-style: italic; }

/* ============================================================
   RICH TEXT
   ============================================================ */
.rtext-section        { padding: 52px 24px; }
.rtext-section--gray  { background: var(--gray); }
.rtext-section--white { background: var(--white); }
.rtext { max-width: 780px; margin: 0 auto; text-align: center; }
.rtext h2 { font-size: 30px; font-weight: 700; line-height: 1.35; margin-bottom: 20px; color: var(--text); }
.rtext h2 em { color: var(--green); font-style: normal; }
.rtext p { font-size: 16px; color: #444; margin-bottom: 12px; }
.rtext strong { color: var(--text); }
.rtext__checklist { list-style: none; text-align: left; display: inline-block; margin-top: 10px; }
.rtext__checklist li { font-size: 16px; font-weight: 600; color: var(--text); padding: 4px 0; }

/* ============================================================
   IMAGE-WITH-TEXT
   ============================================================ */
.iwt-section { padding: 56px 24px; }
.iwt-section--white { background: var(--white); }
.iwt-section--gray  { background: var(--gray); }
.iwt-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 52px;
  max-width: 1200px;
  margin: 0 auto;
  align-items: center;
}
.iwt-media { border-radius: 16px; overflow: hidden; background: var(--border); aspect-ratio: 4/3; }
.iwt-media img, .iwt-media video { width: 100%; height: 100%; object-fit: cover; }
.iwt-content h2 { font-size: 28px; font-weight: 700; color: var(--text); margin-bottom: 16px; }
.iwt-content h2 em { color: var(--green); font-style: normal; }
.iwt-content p { font-size: 15px; color: #444; margin-bottom: 10px; }
.iwt-content strong { color: var(--text); }

/* ============================================================
   MULTIROW (como usar)
   ============================================================ */
.multirow-section { padding: 56px 24px; background: var(--gray); }
.multirow { display: flex; flex-direction: column; gap: 64px; max-width: 1200px; margin: 0 auto; }
.multirow-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
}
.multirow-row--reverse { direction: rtl; }
.multirow-row--reverse > * { direction: ltr; }
.multirow-media { border-radius: 16px; overflow: hidden; aspect-ratio: 16/10; background: var(--border); }
.multirow-media img, .multirow-media video { width:100%; height:100%; object-fit:cover; }
.multirow-content { color: var(--text); }
.multirow-content__caption {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--green);
  margin-bottom: 10px;
  font-weight: 700;
}
.multirow-content h3 { font-size: 26px; font-weight: 700; margin-bottom: 18px; color: var(--text); }
.multirow-content h3 em { color: var(--green); font-style: normal; }
.multirow-content p { font-size: 15px; color: #444; margin-bottom: 10px; }

/* ============================================================
   MÉDICO / ESPECIALISTA
   ============================================================ */
.doctor-section { padding: 56px 24px; background: var(--white); border-top: 1px solid var(--border); }
.doctor-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 52px;
  max-width: 1200px;
  margin: 0 auto;
  align-items: center;
}
.doctor-img { border-radius: 16px; overflow: hidden; aspect-ratio: 4/5; background: var(--gray); }
.doctor-img img { width:100%; height:100%; object-fit:cover; }
.doctor-content { color: var(--text); }
.doctor-content h2 { font-size: 26px; font-weight: 700; margin-bottom: 22px; color: var(--text); }
.doctor-content h2 em { color: var(--green); font-style: normal; }
.doctor-content p { font-size: 15px; color: #444; margin-bottom: 12px; }
.doctor-content strong { color: var(--text); font-weight: 700; }

/* ============================================================
   STATS
   ============================================================ */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 1000px;
  margin: 0 auto;
}
.stat-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px 20px;
  text-align: center;
}
.stat-card__number { font-size: 42px; font-weight: 700; color: var(--green); line-height: 1.1; }
.stat-card__label  { font-size: 14px; color: var(--muted); margin-top: 6px; }

/* ============================================================
   TABELA COMPARATIVA
   ============================================================ */
.comparison-section { padding: 56px 24px; background: var(--white); }
.comparison-title {
  text-align: center;
  font-size: 30px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 36px;
  line-height: 1.3;
}
.comparison-title em { color: var(--green); font-style: normal; }
.ctable-wrap { max-width: 860px; margin: 0 auto; overflow-x: auto; }
.ctable {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 480px;
}
.ctable th {
  padding: 16px 12px;
  font-size: 13px;
  font-weight: 700;
  text-align: center;
  background: var(--white);
  border-bottom: 2px solid var(--border);
  color: var(--text);
}
.ctable th:first-child { text-align: left; width: 44%; }
.ctable th.ctable__us-head {
  background: var(--green);
  color: var(--white);
  border-bottom-color: var(--green-dark);
  border-radius: 10px 10px 0 0;
}
.ctable td {
  padding: 13px 12px;
  font-size: 14px;
  text-align: center;
  background: var(--white);
  border-bottom: 1px solid var(--border);
}
.ctable td:first-child { text-align: left; font-weight: 500; color: var(--text); background: var(--gray); }
.ctable td.ctable__us-cell { background: rgba(0,200,83,.05); }
.ctable__check { color: #26a65b; font-size: 18px; font-weight: 900; }
.ctable__x { color: #ccc; font-size: 18px; }

/* ============================================================
   ACCORDION
   ============================================================ */
.accordion-section { padding: 16px 24px 56px; background: var(--gray); }
.accordion-intro { max-width: 760px; margin: 0 auto 28px; text-align: center; font-size: 16px; color: #444; }
.accordion { max-width: 760px; margin: 0 auto; }
.acc-item  { border-top: 1px solid var(--border); }
.acc-item:last-child { border-bottom: 1px solid var(--border); }
.acc-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 17px 0;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  font-family: 'Poppins', sans-serif;
}
.acc-icon  { color: var(--green); font-size: 20px; flex-shrink: 0; }
.acc-label { flex: 1; font-size: 15px; font-weight: 600; color: var(--text); }
.acc-arrow { color: #aaa; font-size: 13px; flex-shrink: 0; transition: transform .3s; }
.acc-item.open .acc-arrow { transform: rotate(180deg); }
.acc-body  { overflow: hidden; max-height: 0; transition: max-height .35s ease; }
.acc-item.open .acc-body { max-height: 400px; }
.acc-body__inner { padding: 0 0 16px 32px; font-size: 14px; color: #555; line-height: 1.7; }

/* ============================================================
   WAVE DIVIDER
   ============================================================ */
.wave { line-height: 0; }
.wave svg { display: block; width: 100%; }

/* ============================================================
   CTA FINAL — fundo verde
   ============================================================ */
.cta-section {
  background: var(--green);
  padding: 64px 24px;
  text-align: center;
  color: var(--white);
}
.cta-section h2 { font-size: 34px; font-weight: 700; margin-bottom: 12px; color: var(--white); }
.cta-section p  { font-size: 16px; opacity: .88; margin-bottom: 36px; }
.cta-section .urgency-note { margin-top: 20px; font-size: 14px; opacity: .72; }

/* ============================================================
   FOOTER
   ============================================================ */
.site-footer { background: var(--text); color: rgba(255,255,255,.55); font-size: 13px; line-height: 1.8; }
.site-footer a { color: rgba(255,255,255,.55); transition: color .2s; }
.site-footer a:hover { color: var(--white); }
.footer-grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr 1fr;
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 48px 24px 36px;
  border-bottom: 1px solid rgba(255,255,255,.1);
}
.footer-brand img { height: 36px; width: auto; margin-bottom: 12px; opacity: .85; }
.footer-tagline { font-size: 13px; color: rgba(255,255,255,.45); line-height: 1.6; }
.footer-title { font-size: 13px; font-weight: 700; color: var(--white); margin-bottom: 6px; letter-spacing: .3px; }
.footer-sub { font-size: 12px; color: rgba(255,255,255,.4); margin-bottom: 10px; }
.footer-info { list-style: none; display: flex; flex-direction: column; gap: 6px; }
.footer-info li { font-size: 13px; color: rgba(255,255,255,.55); }
.footer-info a  { color: rgba(255,255,255,.75); }
.footer-info a:hover { color: var(--white); }
.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 12px;
  color: rgba(255,255,255,.35);
}
.footer-bottom a { color: rgba(255,255,255,.35); }
.footer-bottom a:hover { color: rgba(255,255,255,.7); }

/* ============================================================
   RESPONSIVO
   ============================================================ */
@media (max-width: 900px) {
  .product-grid,
  .about-grid,
  .tgrid,
  .multirow-row,
  .doctor-grid,
  .iwt-grid,
  .stats-grid { grid-template-columns: 1fr; gap: 28px; }

  .multirow-row--reverse { direction: ltr; }
  .footer-grid { grid-template-columns: 1fr; gap: 28px; padding: 36px 20px 28px; }
  .footer-bottom { flex-direction: column; text-align: center; }

  .product-title    { font-size: 22px; }
  .price-current    { font-size: 30px; }
  .rtext h2         { font-size: 24px; }
  .about-content h2 { font-size: 26px; }
  .section-heading  { font-size: 24px; }
  .cta-section h2   { font-size: 26px; }
  .comparison-title { font-size: 22px; }
}

@media (max-width: 480px) {
  .site-header { padding: 10px 16px; }
  .btn--green  { padding: 10px 18px; font-size: 13px; }

  .product-section,
  .section,
  .rtext-section,
  .multirow-section,
  .doctor-section,
  .accordion-section { padding-left: 16px; padding-right: 16px; }
}
```

O `style.css` deve ser gerado **exatamente assim** — sem referência a `--blue` ou `.btn--red` em nenhum lugar.

Adicionar no `<head>` do HTML quaisquer estilos extras específicos da página em um bloco `<style>` inline.

---

## PASSO 5 — Salvar os arquivos

Salvar ambos:
- `C:/Users/user/Desktop/[handle]/[handle].html`
- `C:/Users/user/Desktop/[handle]/style.css`

Após salvar, informar:
1. Arquivos criados e localização
2. **Placeholders de checkout** a substituir: `LINK_CHECKOUT_1`, `LINK_CHECKOUT_2`, etc.
3. Qualquer imagem que ficou sem URL (se houver)
4. Como abrir: clicar duas vezes no `.html` (o `style.css` precisa estar na mesma pasta)

---

## Regras gerais

- Copy sempre em **Português Brasileiro** persuasivo
- Especialistas sempre do sexo masculino (Dr. + sobrenome)
- Paleta padrão: verde `#00C853` + preto `#111111` — não usar azul nem vermelho
- Urgência padrão: "17 Unidades Restantes"
- Garantia: 90 dias (salvo indicação contrária)
- Desconto: calcular com base nos preços fornecidos ou usar "50% DESCONTO" como padrão
- Logo: usar a URL fornecida pela marca, ou perguntar se não informada
- Imagens: usar URLs diretas da referência — nunca placeholders quando URL disponível
