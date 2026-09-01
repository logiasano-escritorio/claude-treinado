---
name: pipeline-nicho
description: Pipeline completo de 1 nicho (ex "melasma", "neuropatia", "queda capilar") → raspa a Meta Ad Library dos concorrentes campeões, extrai os long-forms + imagens, adapta todos pro produto Sano/Relívia do nicho, gera imagens no padrão campeão, monta advertoriais e sobe a campanha no Meta. Ponta a ponta com 1 comando.
trigger: /pipeline-nicho
---

# /pipeline-nicho <nicho> [produto] [pais]

Você é o orquestrador do pipeline de espionagem+adaptação da Sano/Relívia. O usuário dá UM nicho e você roda o fluxo de ponta a ponta. Reaproveita os scripts em `scripts/` (já testados na campanha Clarilux/melasma). Projeto Sano fica em `c:/Users/user/Desktop/Sanologia`; vault Obsidian em `c:/Users/user/Desktop/SANOLOGIA OBSIDIAN`.

Memórias-chave: raspar Ad Library, adaptar long-form, campanha Meta, pixels, compliance — leia as que aparecem como `[[...]]`.

---

## ENTRADA
`/pipeline-nicho melasma` (ou neuropatia, queda capilar, fungo unha, edema...).
- **nicho** (obrigatório): o problema/tema.
- **produto** (opcional): produto Sano alvo. Se faltar, pergunte UMA vez qual é e **leia a página de venda em produção** (WebFetch/curl na PV) pra pegar os **ativos reais** — NUNCA inventar ingrediente.
- **pais** (opcional, default US+DE+ES): mercados gringos a raspar (BR costuma ser só clínica local).

Antes de começar, confirme com o usuário: produto alvo, conta/pixel Meta do produto, e se quer rodar tudo (raspa→adapta→imagem→advertorial→campanha) ou parar em alguma fase.

---

## PASSO 0 — MATRIZ DO NICHO + TIPO
Monte a matriz de **termos por idioma** (o que os concorrentes anunciam em cada mercado). Ex melasma: EN dark spots/hyperpigmentation, DE Pigmentflecken/Melasma/Altersflecken, ES manchas oscuras/melasma.

**⚠️ Regra dura ([[reference_raspar_ad_library_drissionpage]]):** ANTES de raspar, meça o volume de cada termo/mercado com `media_type=all` (NÃO `image` — ele esconde ~99% em mercados de vídeo/carrossel; foi o erro do melasma DE). Conte via regex `~?([\d\.]+)\s*resultado`. Descarte mercado morto (<10 ads). UMA palavra acha mais que frase longa; `+` NÃO é OR no FB.

**Classifique o TIPO do nicho** (decide o PASSO 5):
- **RESULTADO VISUAL** (melasma, queda capilar, fungo unha, acne, celulite, clareamento): padrão de imagem = **ANTES/DEPOIS**.
- **DOR/SINTOMA** (neuropatia, edema, dor articular, insônia, refluxo): padrão = **CENA IMPACTANTE da dor** (pessoa sofrendo o sintoma, região afetada, expressão) + diagrama de mecanismo.

---

## PASSO 1 — RASPAR DOMÍNIOS CAMPEÕES
Rode/adapte `scripts/adlib-dominios.py` com a matriz do nicho (edite `MARKETS`/`JOBS` + regex de LIXO). Ele raspa a Ad Library pública via DrissionPage (interface pt-BR + country=US/DE/ES pra ler "Veiculação iniciada em"), filtra ativos +30d (campeões), extrai domínios de destino. Saída: `_dev/adlib-out/dominios_<nicho>.txt/json`. Filtre falso positivo (pet/escola/igreja/clínica local).

## PASSO 2 — LONG-FORMS + IMAGENS DOS TOP DOMÍNIOS
Pegue os ~10-15 domínios campeões, rode/adapte `scripts/adlib-longform.py` (ajuste `DOMINIOS`). Ele:
- Busca frase exata do domínio (`country=ALL`, ordena por impressões).
- **CLICA em todos os "Ver mais"** antes de extrair (senão long-form vem pela metade — regra dura).
- Extrai long-forms (>500 chars) + baixa o criativo real (img `t39.35426-6` `s600x600` via nova aba+canvas; avatar `s60x60` NÃO serve).
- Salva em `Research/AdLibrary-Concorrentes/<dominio>/` (md + jpgs).

## PASSO 3 — FILTRAR (só o do nicho)
Classifique cada long-form pelo **destino do produto** (o path do URL é a verdade: `/melasma-corrector` = alvo; `/rosacea`/`/prostate` = fora). O classificador por regex de texto ERRA — confie no destino. Mova os fora pra `_FORA-DO-TEMA/`. Gere índice mestre por subtipo.

## PASSO 4 — ADAPTAR TODOS OS LONG-FORMS ([[feedback_adaptar_longform_nunca_reduzir]])
Para CADA long-form alvo, adapte pro produto:
- **Tradução fiel + troca de dados** — mantém estrutura/hook/ordem/metáforas/números/CTA. NÃO recriar o ângulo.
- **NUNCA REDUZIR**: adaptação ≥ chars do original (`wc -m`); faltou, EXPANDIR (nunca cortar).
- **Localizar BR**: Stanford→USP/Unicamp, nomes/cidades/lojas→BR, $/pesos→R$.
- **Trocar produto** pelos ativos REAIS (herói alheio → ativo herói do Sano mantendo o argumento).
- **Não suavizar alegação** ([[feedback_nao_suavizar_alegacoes]]), sem drop cap ([[feedback_no_drop_cap_advertorial]]), sem preço no corpo ([[feedback_advertorial_no_price]]).

Escale via **agentes general-purpose em paralelo** (~7-8 long-forms/agente, balanceado por chars). Cada um lê o original em `_originais_txt/<slug>.txt`, adapta, escreve `.md` em `Research/<Produto>-Adaptados/`, valida tamanho. No fim confira: total, 0 menores, destino certo, sem produto concorrente/preço no corpo.

## PASSO 5 — GERAR IMAGENS NO PADRÃO CAMPEÃO
**ANALISE primeiro** as imagens salvas em `Research/AdLibrary-Concorrentes/<dominio>/*.jpg` (leia amostra com Read) pra ver os padrões visuais do nicho. Reaproveite imagens que o produto já tem em `<produto>/images/` — só gere o que falta.

Base: `scripts/gen-imagens-template.py` (Vertex AI, `gemini-3-pro-image-preview`, chave `.env`, [[reference_vertex_ai_setup]]). Produto 1:1 fiel via i2i ("do NOT redesign the product/label"), pote no tamanho da palma ([[feedback_gemini_pote_tamanho_palma_mao]]), texto PT-BR soletrado EXATO no prompt, rostos brasileiros. **CONFIRA cada imagem lendo com Read** ([[feedback_criativo_nao_pode_mentir_destino]]).

- **RESULTADO VISUAL** → 1 produto cine + 5-6 antes/depois (zonas/idades/tons/gravidez, badges "ANTES"/"DEPOIS") + 1 termográfica/mecanismo + 1 close do problema + 1 produto+headline + 1 pessoa segurando.
- **DOR/SINTOMA** → 1 produto cine + 4-5 cenas da dor (segurando a região, à noite, expressão de dor) + 1-2 diagramas do mecanismo (nervo/vaso/inflamação, texto PT-BR) + 1 alívio/depois + 1 produto+headline + 1 pessoa segurando.

Saída: `<produto>/images/<nicho>-novas/*.webp`.

## PASSO 6 — MONTAR ADVERTORIAIS
Escolha os ~6 melhores long-forms (ângulos diversos + original mais duradouro). Clone o design de um advertorial existente do produto (ler o `<head>`/CSS inteiro + estrutura). Via agentes paralelos, 1 advertorial cada: h1 do long-form, corpo em `<p>`+`<h2>`, 4-6 `.figure` com imagens do ângulo, 2-3 CTA → PV oficial, expert box, garantia. GTM já no template (pixel via GTM, não HTML — [[reference_arquitetura_tracking_gtm_yampi]]). Valide imagens (HTTP 200), sem placeholder ([[feedback_advertorial_placeholder_checkout]]), sem case quebrado ([[feedback_pastas_case_quebram_deploy_vercel]]). Commit + `vercel --prod` ([[reference_deploy_sano_brasil]]).

## PASSO 7 — SUBIR CAMPANHA META
Base: `scripts/subir-campanha-template.py`. Confirme conta/pixel/page do produto com o usuário. Padrão:
- **10 ads single-image por conjunto** (flexível/DCO trava entrega — [[project_campanha_tonico_meta]]).
- **⚠️ Meta /adimages REJEITA .webp** (subcode 1487411) → converter pra JPG (Pillow q90) antes.
- Cada ad: imagem + **texto curto próprio** (o "primary text" do feed, chamativo, casando com o advertorial do ângulo) + link pro advertorial.
- CBO, bid cap (Sano US$15), compliance BR (regional BRAZIL_REGULATION+VOLUNTARY, beneficiary/payer `880756411607509`), advantage_audience 0, **site_extensions OPT_OUT** ([[feedback_nunca_subir_ad_com_site_extensions]]).
- **Sempre PAUSED** (usuário ativa na mão). Confira `account_status` da conta antes (status≠1 pode travar ativação).
- Registre o **manifesto** em `BACKLOG DE TRÁFEGO/<Produto>/` ([[feedback_manifesto_antes_de_subir]]) + salve os IDs na memória.

---

## SAÍDA FINAL
Tabela resumo: nº domínios campeões, long-forms adaptados (todos ≥ original), imagens, advertoriais no ar, ads na campanha (PAUSED), e todos os paths/IDs. Aponte pendências (ex: conta a destravar, checkout a ligar na PV).

## Notas
- Todo browser é DrissionPage ([[feedback_browser_automation_drission]]).
- git push estoura com mídia pesada — conferir `git ls-remote` ([[feedback_push_estoura_com_midia_pesada]]).
- Ligar os checkouts Yampi na PV oficial (botões podem estar placeholder href=#).
- Prints com emoji quebram no cp1252 do Windows — salve em arquivo e leia, ou evite emoji no `print`.
