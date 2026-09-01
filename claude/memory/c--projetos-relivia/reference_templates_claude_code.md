---
name: Templates Claude Code (advertorial + página produto)
description: Pacote em [Desktop]/templates-claude-code/ com 2 slash commands genéricos para extrair conteúdo de concorrentes via Console (F12) e gerar HTMLs prontos — advertorial estilo revista e clone de página Shopify com variant picker
type: reference
originSessionId: a1b108ee-303e-4d1c-9923-c0ec9a5ddd29
---
# Templates Claude Code

Pacote unificado salvo em `C:\Users\user\Desktop\templates-claude-code\` com 2 slash commands prontos para distribuir (versões neutralizadas, sem branding Relívia).

## Estrutura

```
templates-claude-code/
├── LEIA-ME.md
├── advertorial/
│   └── gerar-advertorial.md         ← /gerar-advertorial
└── pagina-produto-shopify/
    ├── clonar-produto-shopify.md    ← /clonar-produto-shopify
    ├── template.html                ← base da landing (897 linhas)
    ├── style.css                    ← CSS com --primary editável (655 linhas)
    └── sections-map.md              ← doc das 17 seções
```

## /gerar-advertorial

- Gera HTML único com CSS inline estilo "matéria de revista de saúde"
- 17 seções: navbar + breadcrumb + Dr. especialista + H1 + história + problema + solução + benefícios + 3 CTAs + 3 depoimentos + urgência + FAQ accordion + disclaimer ANVISA
- Paleta teal #00465a + verde #47901a + amarelo #fdcc5e
- Extração: 2 scripts no Console (F12) — texto + mídia
- Output: `[Desktop]/advertorial-[produto].html`

## /clonar-produto-shopify

- Clona página Shopify completa no padrão Relívia (sem branding)
- Pasta `[handle]/` com HTML + style.css + pasta `images/`
- Galeria com setas + variant picker funcional + FAQ accordion + UTM passthrough
- Extração: 5 scripts no Console (F12) — scroll, texto, mídia, galeria, variantes, reviews
- Cor primária editável em `:root` do `style.css` (padrão azul #2E2BFF)
- Output: `[Desktop]/[handle]/` com tudo pronto para subir em Vercel/Netlify/cPanel

## Origem

- `gerar-advertorial.md`: adaptado da versão original em `~/.claude/commands/gerar-advertorial.md` removendo Playwright (ficou 100% Console)
- Pacote shopify: derivado de `c:/projetos/relivia/beterraba-relivia/beterraba.html` + `style.css`, com placeholders genéricos substituindo "Beterraba Relívia", `pagamento.reliviaonline.com`, pixel Relívia, endereço Cajamar, selos checkoutchamp, etc.

## Quando usar este pacote

- Mandar templates prontos para colaboradores externos (sem expor branding/credenciais Relívia)
- Demonstrar fluxo de clone manual via Console quando não dá pra usar Playwright/DrissionPage
- Base para futuros comandos derivados (criar variações por nicho mantendo a mesma estrutura)
