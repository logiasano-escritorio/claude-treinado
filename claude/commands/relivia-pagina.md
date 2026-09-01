# Criar Página de Produto HTML — Relívia

Você é especialista em criar landing pages standalone em HTML para a marca Relívia.

## PASSO 0 — Leitura obrigatória antes de iniciar

Leia o arquivo:
`C:/Users/user/.claude/projects/c--Users-user--claude/memory/MEMORY.md`

---

## PASSO 1 — Receber o JSON do produto

Pergunte ao usuário pelo arquivo `product.[handle].json` do produto.

Com o JSON em mãos, extraia:
- Nome do produto e tagline
- Descrição, benefícios, especificações técnicas
- Variantes (nome, preço, preço original)
- Depoimentos (nome, título, texto, estrelas)
- FAQ (perguntas e respostas)
- Seções especiais (médico, como usar, estudos, comparação, garantia)
- Qualquer copy persuasivo relevante

---

## PASSO 2 — Gerar o HTML completo

### Estrutura de pastas de saída
- HTML: `C:/Users/user/Desktop/relivia/[handle]/[handle].html`
- CSS: `C:/Users/user/Desktop/relivia/[handle]/style.css` (copiar de `alinha facil/style.css` se não existir — avisar o usuário)

### Estrutura obrigatória de seções (nesta ordem)
1. **Header** — logo + botão "Comprar Agora" (`.js-cta-btn`)
2. **Hero** — galeria com 5 slides + seletor de variantes + CTA + trust-bar + urgência
3. **Quem somos** — about-grid com imagem + texto Relívia padrão
4. **Doctor quote** — doctor-section com médico especialista
5. **Accordion de specs** — Especificações Técnicas / Entrega e Pagamento / Nossa Garantia
6. **Estudos clínicos** — rtext-section + stats-grid com 3 stat-cards (números grandes)
7. **Seções image-with-text** — alternando `.iwt-section--gray` e `--white`, imagem e texto lado a lado
8. **Como usar** — multirow-section com 3 passos alternados
9. **Profissionais** — segunda doctor-section
10. **Texto livre** — rtext-section (pitch final antes da tabela)
11. **Tabela comparativa** — comparison-section com `.ctable`
12. **Depoimentos** — section--gray com `.tgrid` e 3 `.tcard`
13. **Garantia** — iwt-section com imagem + texto de garantia
14. **FAQ** — accordion-section com todas as perguntas
15. **Wave divider** — `<div class="wave">` com SVG azul
16. **Final CTA** — cta-section com título + botão branco (`.js-cta-btn`)
17. **Footer** — site-footer padrão Relívia

### CSS compartilhado
Linkar `<link rel="stylesheet" href="style.css" />`.

Para classes novas (ex: `.ctable`, `.iwt-grid`, `.stats-grid`), adicionar bloco `<style>` inline no `<head>` da página — **não modificar o style.css**.

### Paleta oficial (use sempre variáveis CSS)
```css
--blue: #2E2BFF       /* botões, preços, badges, CTAs */
--blue-dark: #1B17FF  /* hover, wave fill */
--white: #ffffff
--gray: #F5F6F8       /* seções alternadas, cards */
--text: #111111       /* body, títulos, footer bg */
--muted: #666666      /* texto secundário */
--stars: #ffcc00      /* estrelas */
```

### Variantes — padrão obrigatório
```html
<div class="variant-card active" data-checkout="LINK_CHECKOUT_1" data-price="R$ 297,00">
  <span class="variant-card__check">✓</span>
  <div class="variant-card__name">1 Unidade</div>
  <div class="variant-card__sub">R$ 297,00</div>
  <div class="variant-card__price">R$ 297,00</div>
</div>
```
- Usar `LINK_CHECKOUT_1`, `LINK_CHECKOUT_2`, etc. como placeholder
- Adicionar `<div class="variant-card__popular">Mais Popular</div>` na variante mais vendida
- JS atualiza todos os `.js-cta-btn` e `#js-price` ao selecionar variante

### Imagens — placeholders descritivos
Todas as imagens ficam como `<div class="placeholder">` com nome descritivo enquanto o funcionário não faz as artes:
```html
<div class="placeholder" style="height:100%;"><span class="icon">📦</span><span>[handle]-1.jpg</span></div>
```

### Convenção de nomes de imagens (para o funcionário)
| Slot | Arquivo | Pasta servidor |
|---|---|---|
| Galeria 1–5 | `[handle]-1.jpg` … `[handle]-5.jpg` | `galeria/` |
| Imagens extras (uso, tecnologia, etc.) | `[handle]-[descricao].jpg` | `galeria/` |
| Passos (como usar) | `[handle]-passo-1.jpg` … | `video/` |
| Foto "Quem somos" | `relivia-sobre.jpg` | `video/` |
| Depoimentos 1–3 | `[handle]-depo-1.jpg` … | `depoimentos/` |
| Foto médico | `[handle]-medico.jpg` | `depoimentos/` |
| Foto profissional | `[handle]-profissional.jpg` | `depoimentos/` |

### Caminhos de servidor (após upload na Hostinger)
```
/relivia/[handle]/galeria/[handle]-1.jpg
/relivia/[handle]/depoimentos/[handle]-depo-1.jpg
/relivia/[handle]/video/[handle]-passo-1.jpg
```
Extensão sempre `.jpg` simples (sem dupla extensão).

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
    document.querySelectorAll('.js-cta-btn').forEach(btn => btn.href = url);
    const priceEl = document.getElementById('js-price');
    if (priceEl && price) priceEl.textContent = price;
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

### Texto padrão — "Quem somos"
```html
<h2>Quem <em>somos nós</em></h2>
<p><strong>Relívia</strong> é uma marca dedicada ao bem-estar e à qualidade de vida, com <strong>14 anos de história</strong> construindo confiança, credibilidade e resultados reais para milhares de clientes.</p>
<p>Ao longo dessa trajetória, desenvolvemos produtos pensados para oferecer conforto, cuidado e suporte no dia a dia, sempre com foco em qualidade, segurança e inovação.</p>
<p>Na Relívia, acreditamos que cada detalhe importa — do desenvolvimento à experiência do cliente. Nosso compromisso é evoluir continuamente, mantendo a transparência, o respeito e a excelência que nos acompanham há mais de uma década.</p>
```

### Footer padrão Relívia
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

---

## PASSO 3 — Após criar o HTML

Informar ao usuário:
1. Arquivo salvo em: `C:/Users/user/Desktop/relivia/[handle]/[handle].html`
2. **Lista de imagens para o funcionário** — tabela com: slot / nome do arquivo / pasta do servidor
3. Lembretes:
   - Copiar `style.css` para a pasta `[handle]/` (se não foi copiado)
   - Subir as imagens na Hostinger em `/relivia/[handle]/galeria/`, `/depoimentos/`, `/video/`
   - Enviar os links de checkout por variante para atualizar o HTML

---

## PASSO 4 — Atualizar imagens (quando funcionário terminar)

Quando o usuário disser que as imagens foram enviadas para o servidor:

1. Verificar pasta local de download para confirmar nomes exatos dos arquivos
2. Substituir todos os `<div class="placeholder">` por `<img src="/relivia/[handle]/[pasta]/[arquivo].jpg" alt="..." />`
3. Corrigir subpastas conforme a tabela de convenção (galeria/depoimentos/video)

---

## PASSO 5 — Atualizar links de checkout

Quando o usuário fornecer as URLs de checkout:

1. Substituir `LINK_CHECKOUT_1`, `LINK_CHECKOUT_2`, `LINK_CHECKOUT_3` pelas URLs reais
2. Atualizar nomes e preços das variantes conforme fornecido
3. Atualizar `data-checkout` e `data-price` em cada `.variant-card`
4. Usar `replace_all: true` para trocar todos os placeholders de uma vez

---

## Regras gerais

- Copy sempre em **Português Brasileiro** persuasivo
- Nunca usar roxo, vermelho ou fundo escuro em seções
- Header: fundo branco com border-bottom sutil
- Footer: fundo `#111111`
- Logo: `https://reliviaonline.shop/images/logorelivia.png`
- Urgência padrão: "17 Unidades Restantes"
- Garantia: 90 dias (salvo indicação contrária no JSON)
- Desconto: calcular com base nos preços do JSON ou usar "50% DESCONTO" como padrão
