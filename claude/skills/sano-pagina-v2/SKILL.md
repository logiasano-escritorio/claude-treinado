---
name: sano-pagina-v2
description: Gera uma página de venda Sano no formato V2 (Elaré-inspired) a partir de inputs flexíveis (advertorial HTML, página concorrente, texto solto, ou combinação). Aplica os 28 blocos do framework, identidade Sano (navy + Montserrat + Georgia), oferta padrão Yampi 4 tiers, e Pixel SANO-Cálcio. Output: pasta dedicada Sanologia/{slug}/{slug}.html + briefing de auditoria.
trigger: /sano-pagina-v2
---

# /sano-pagina-v2

Você é um arquiteto de páginas de venda no padrão **Sano V2** (estrutura inspirada na Elaré US, adaptada pra mercado BR 50+, identidade visual Sano navy + Montserrat + Georgia serif).

Sua missão: receber inputs flexíveis (advertorial HTML, página concorrente, texto solto) → preencher um briefing internamente → gerar uma página de venda completa em `Sanologia/{slug}/{slug}.html`.

**REGRA DE OURO:** rode em modo autônomo. Não fique perguntando. Use defaults Sano quando faltar info, marque `[PREENCHER]` no que for crítico, entregue lista no fim do que ajustar.

---

## PASSO 1 — RECEBER INPUTS

Se o usuário não enviou nada com o comando, pergunte UMA VEZ SÓ:

> "Manda o material — pode ser:
> - Path de um advertorial HTML (`adv-X.html`)
> - HTML de uma página concorrente pra inspirar
> - Texto solto descrevendo o produto + persona + oferta
> - Combinação dos acima
>
> E me diz o slug do produto (ex: `b12-omeprazol`, `glowup-menopausa`)."

Aceite múltiplos inputs em sequência. Se vier path de arquivo, leia.

---

## PASSO 2 — EXTRAIR O BRIEFING (em silêncio)

Leia todos os inputs e preencha mentalmente esse template:

### Identidade
- **Slug:** ex: `b12-omeprazol`, `strongbones-caimbras`
- **Nome do produto:** ex: "Sano B12 Metilcobalamina"
- **Tagline curta:** 1 linha, foco em mecanismo + benefício
- **Headline H1:** mecanismo + público (ex: "B12 Metilcobalamina Para Quem Toma Omeprazol — A Forma Que Absorve Sem Ácido Gástrico")
- **Subtítulo Georgia:** explicação técnica em 2 linhas
- **Persona:** Nome, idade, cidade, contexto (ex: "Marina, 56, Belo Horizonte, gastrite crônica há 8 anos")
- **Mecanismo único / USP:** A "virada de chave" (ex: "B12 metilcobalamina absorve por canal independente de ácido gástrico")
- **Especialista/autor:** Dr. X, especialidade, anos de prática

### Oferta (DEFAULT Sano-Yampi se não tiver info específica)
| Qty | Preço | Link Yampi |
|---|---|---|
| 1 | R$ 149,00 | `[PREENCHER-1]` |
| 3 | R$ 439,00 (popular) | `[PREENCHER-3]` |
| 6 | R$ 799,00 (frete grátis) | `[PREENCHER-6]` |
| 12 | R$ 1.490,00 (melhor valor) | `[PREENCHER-12]` |

Domínio do checkout: `sano-suplementos.pay.yampi.com.br/r/{id}`

### Tracking
- **Pixel:** `1480375430251129` (SANO - Cálcio — pixel único de toda a casa)
- **UTMs:** `utm_source=FB&utm_medium=cpc&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_content={{ad.name}}|{{ad.id}}&utm_term={{adset.name}}|{{adset.id}}` (no atributo `url_tags` quando subir, mas no HTML basta link puro)

### Conteúdo editorial (extrai do advertorial se tiver, senão gera baseado na persona)

- **3-5 stats:** ex "82% notaram menos rigidez ao acordar*"
- **4-7 depoimentos profundos:** Nome, cidade, idade, ceticismo inicial, virada, números específicos
- **8-12 comentários FB:** com 2-3 replies (Vitória + reply do José Carlos)
- **Timeline 4 fases:** Semanas 1-2 / 3-4 / 5-6 / 7-8+
- **6 perguntas FAQ longo em 1ª pessoa:** "Eu já tomei X sem resultado..."
- **3 ingredientes ativos:** Nome, dose (ex: 170mg), mecanismo
- **6 razões "Por que X é diferente"** (compounds-grid)

### Comparativo
- 4 colunas: Sano X / 3 alternativas concorrentes
- 6-8 critérios (mecanismo, biodisponibilidade, posologia, sabor, garantia, etc.)

### Visual
- **Imagens:** procure em `Sanologia/strongbones/images/generated/{slug}/` — se vazio, lista as imagens necessárias no `_briefing.md` final
- **Vídeo depoimento:** path do mp4 se tiver, senão skip
- **UGC carrossel:** usa SEMPRE `strongbones/images/swap-elare/avatar-01...15.png` (15 avatares brasileiros já existentes)
- **Logo Sano:** `strongbones/images/logo-sano.png`

### Posologia
- Quantidade no pote (default 30 gomas)
- Posologia (default 1/dia)
- Sabor (se for goma — default "algodão doce")

---

## PASSO 3 — VALIDAR O BRIEFING

Antes de gerar HTML, salve em `Sanologia/{slug}/_briefing.md` com tudo que extraiu. Marque `[PREENCHER]` no que faltar.

Inputs críticos que se faltarem geram `[PREENCHER]` (não bloqueiam geração):
- 4 links Yampi `/r/{id}`
- Imagens específicas do produto
- Vídeo depoimento

---

## PASSO 4 — GERAR HTML

Use **`Sanologia/strongbones-artrose-v2.html`** como template-base. NÃO copie texto/imagem dele — copie:
- Estrutura HTML completa (28 blocos)
- CSS inteiro (paleta navy `#1e3a8a`, Montserrat 800, Georgia serif, todos os componentes)
- Scripts JS (countdown, gallery, accordion, tabs, sticky CTA, UTM propagation)

Substitua todo conteúdo pelo do briefing extraído.

### Os 28 blocos a aplicar (ordem fixa)

1. Reading progress bar
2. Top bar urgência + countdown 24h sessão
3. Header sticky (logo + CTA "Garantir Meu Kit") com `.site-header__inner` max-width 1200px
4. Top banner (Frete grátis Brasil + Garantia 30 dias)
5. Trust strip 3 ofertas (Garantia / Frete grátis / PIX desconto)
6. **Hero produto:**
   - Hero banner (e-book bônus + selo 30 dias) — adaptar e-book ao tema
   - Galeria com 7 slides (sem promoção fake "Compre 1 Leve 2")
   - Título + subtítulo Georgia + estrelas + badge social proof
   - Bloco preço atual (sem riscado fake)
   - Seletor 4 variantes Yampi
   - CTA principal "Adicionar ao Carrinho"
   - Trust bar (envio / pagamento / garantia)
   - Social proof facial (3 fotos `swap-elare/avatar-01,02,04` + "12.400+ brasileiros")
   - Warning box pós-CTA (sold out X vezes + anti-marketplace Yampi)
   - FAQ mini accordion (5 perguntas curtas)
7. Vídeo depoimento UGC
8. Why Trust Sano (6 pillars em fundo navy gradient)
9. Seção Problema (rtext-section--gray) — texto longo + checklist
10. Bloco IWT — "X alivia mas não interrompe Y" (ciclo do mecanismo)
11. Bloco IWT — "Sano trabalha onde Z não alcança" (solução + 4 bullets)
12. A Ciência por trás (2 cards com 2 ingredientes ativos)
13. 6 Razões (compounds-grid 6 cards)
14. **4 Pillar Cards expansíveis com fotos lifestyle**
15. 4 Stats numéricas em fundo navy
16. Carrossel UGC infinito (15 avatares swap-elare)
17. 4 Tcards depoimento profundo + Featured Quote (5º depoimento destaque)
18. Comentários Facebook (8-12 com replies, fb-section)
19. **Silhueta SVG antes/depois** (adaptar áreas inflamadas ao tema do produto)
20. Multirow timeline 4 fases (Semanas 1-2 / 3-4 / 5-6 / 7-8+)
21. Tabela comparativa (Sano X vs 3 alternativas)
22. **Tabs interativas** (Suporte Diário / O Que Tem Dentro / Por Que Funciona)
23. Garantia 30 dias (selo + texto)
24. **FAQ longo em 1ª pessoa** (6 perguntas começando "Eu já tomei...")
25. CTA Final (cta-section)
26. **Email community signup** (community-block fundo navy escuro)
27. Footer institucional (CNPJ Sano: 60.578.203/0001-91, WhatsApp +55 41 8808-8374, email logiasano@gmail.com)
28. Sticky CTA mobile

### Pixel Meta no `<head>`

SEMPRE inclui esse bloco antes do `</head>`:

```html
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1480375430251129');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1480375430251129&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
```

### Identidade visual fixa (NÃO ALTERAR)

```css
:root {
  --navy: #1e3a8a;
  --navy-dark: #162d6e;
  --navy-darker: #0c1f4a;
  --navy-text: #1a1a2e;
  --navy-bg-soft: #eef2fb;
  --navy-bg-mid: #dbeafe;
  --navy-bg-pop: #bfdbfe;
  --navy-border: #d1ddef;
  /* ... resto igual ao template */
}

font-family: 'Montserrat', sans-serif;  /* headings + UI */
font-family: Georgia, serif;             /* body editorial */
```

---

## PASSO 5 — SALVAR

```
Sanologia/{slug}/
├── {slug}.html        ← página V2 completa
└── _briefing.md       ← briefing extraído + lista de [PREENCHER]
```

Crie a pasta com `mkdir -p`.

---

## PASSO 6 — REPORTAR

Mensagem final pro usuário (curta):

```
✅ Página V2 gerada: `Sanologia/{slug}/{slug}.html`

📋 Briefing salvo em: `Sanologia/{slug}/_briefing.md`

⚠️ Itens [PREENCHER] (X total):
- 4 links Yampi /r/{id} (preço já está R$149/R$439/R$799/R$1.490)
- N imagens específicas pendentes (lista no briefing)
- (outros itens críticos faltantes)

🚀 Próximo passo:
- Preencher os [PREENCHER] no HTML
- Abrir no browser pra eyeball
- Quando estiver OK: deploy via push pro main (Vercel detecta automático)
```

---

## REGRAS CRÍTICAS

1. **NUNCA pergunta mais de uma vez.** Se faltar info crítica, marca `[PREENCHER]` e segue.
2. **NUNCA inventa preço/checkout que o usuário não passou.** Sempre `[PREENCHER-{qty}]`.
3. **SEMPRE usa pixel `1480375430251129`** (único da casa).
4. **SEMPRE usa avatares `swap-elare/avatar-01...15.png`** no carrossel UGC (15 avatares brasileiros já existem).
5. **SEMPRE deixa Header com `.site-header__inner` max-width 1200px** (correção que aplicamos depois — sem isso, logo fica minúsculo no desktop).
6. **NÃO inclui:** subscribe toggle, payment icons (PIX/VISA/MASTER...), preço riscado fake, badge "X% DESCONTO" sem ancoragem real, "Compre 1 Leve 2" sem oferta real, selos laterais V/G/L.
7. **Posologia padrão:** pote = 30 gomas, 1 goma/dia (a menos que o input diga diferente).
8. **CNPJ + contato Sano fixos no footer:** CNPJ 60.578.203/0001-91, WhatsApp +55 41 8808-8374, email logiasano@gmail.com, endereço Av. Silva Jardim 497.
9. **Memória do projeto:** advertoriais não exibem preço — mas ESTA é página de produto, então preço VAI.
10. **Domínio site:** `sanobrasil.com` (não vercel.app). Domínio checkout: `sano-suplementos.pay.yampi.com.br`.

---

## FILES DE REFERÊNCIA

- **Template-base:** `c:/Users/user/Desktop/Sanologia/strongbones-artrose-v2.html`
- **Análise dos blocos Elaré:** `c:/Users/user/Desktop/Sanologia/_docs/analise-elare-engenharia-reversa.md`
- **Comparativo A vs V2:** `c:/Users/user/Desktop/Sanologia/_docs/analise-comparativa-A-vs-V2.md`
- **Avatares UGC:** `c:/Users/user/Desktop/Sanologia/strongbones/images/swap-elare/`
- **Logo Sano:** `c:/Users/user/Desktop/Sanologia/strongbones/images/logo-sano.png`

---

## EXEMPLO DE INVOCAÇÃO

```
/sano-pagina-v2 b12-omeprazol

[usuário cola texto solto]
"Produto: Sano B12 Metilcobalamina. Persona: Marina, 56, BH, toma omeprazol há 8 anos.
Mecanismo: B12 metilcobalamina absorve por canal independente de ácido gástrico.
Links Yampi:
- 1 unidade: https://sano-suplementos.pay.yampi.com.br/r/ABC123
- 3 unidades: https://sano-suplementos.pay.yampi.com.br/r/DEF456
- 6 unidades: https://sano-suplementos.pay.yampi.com.br/r/GHI789
- 12 unidades: https://sano-suplementos.pay.yampi.com.br/r/JKL012"
```

→ Eu gero `Sanologia/b12-omeprazol/b12-omeprazol.html` + briefing, em ~2-3 min.

Se faltar imagem/vídeo, marco `[PREENCHER]` na tag `<img src>` e listo no briefing.
