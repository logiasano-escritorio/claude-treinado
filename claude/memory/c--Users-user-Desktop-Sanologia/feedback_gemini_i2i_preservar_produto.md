---
name: Edição i2i — preservar produto via input fiel
description: Ao editar imagem com Gemini i2i pra trocar texto, SEMPRE use a versão com produto correto como input — nunca peça "gere novo produto"
type: feedback
originSessionId: 9bd6982e-c870-4b26-bb8d-a96c2fc679cf
---
# Edição image-to-image (Gemini 3.1 Flash Image)

**Regra:** quando o objetivo é trocar SÓ texto/copy de uma imagem mantendo o produto, layout, cores e composição:

1. **Input image** deve ser a versão com o produto correto/hi-fi (não a versão "limpa" ou genérica). Se a imagem atual tem produto errado, busque backup que preserve a embalagem original.
2. **Prompt** começa sempre com: `"Edit this image, keeping EVERYTHING about the PRODUCT exactly the same — same packaging, same label, same brand colors, same details, DO NOT redesign or replace the product..."`
3. Descrever **explicitamente** os detalhes da embalagem (nome do produto, mg, tagline, badges, ingredientes) — Gemini tem tendência de "limpar" embalagens complexas.
4. Listar mudanças de texto **uma a uma** com aspas exatas do antes/depois.
5. Sempre fazer backup do original antes (`_backup-<tema>/`).

**Why:** O Gemini i2i tem boa fidelidade em layout e estilo, mas pode regenerar o produto numa versão "idealizada" se o prompt não enfatizar preservação. Já aconteceu de trocar o sachê Relívia Orégano (com "óleo de semente preta", cápsulas, 4 badges) por uma embalagem genérica limpa quando o input usado foi a versão atual da página (que já tinha o produto errado).

**How to apply:** Em qualquer pipeline de "atualizar texto da imagem" (banner, advertorial, infográfico), sempre verificar primeiro se o INPUT tem o produto hi-fi correto. Se a versão atual está degradada, restaurar de backup ou usar pasta `_backup-<tema>/` antes de gerar.

**Casos validados:**
- 2026-05-11: 9 banners Sano (StrongBones/GlowUp/B12) editados de "Compre 1 Leve 2 / R$149,90" para "Compre 2 Ganhe 1 / R$298" — produto preservado 100%.
- 2026-05-11: 3 imagens Orégano (fungo-de-unha: resultado/info-2/produto-7) regeneradas usando `_backup-imunidade/` como input pra recuperar o sachê hi-fi.
