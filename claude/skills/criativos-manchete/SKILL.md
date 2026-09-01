---
name: criativos-manchete
description: Gera criativos Facebook Ads no estilo "manchete jornalística médica" (estilo AlinhaFácil) pra QUALQUER produto. Recebe contexto do produto + problema que resolve, gera N criativos quadrados 1080x1080 com layout fixo (headline forte com palavra destacada em ciano, círculo no canto sup direito, footer estilo portal de notícia). Texto + imagem via Gemini 3.1 Flash Image (PT-BR sem erros). Trigger /criativos-manchete
---

# /criativos-manchete

Gerador reaproveitável dos criativos vencedores estilo AlinhaFácil ("manchete médica jornalística") pra qualquer produto.

## QUANDO USAR

- User pediu "criativos no estilo AlinhaFácil" / "estilo manchete"
- User digitou `/criativos-manchete`
- User mostrou um dos criativos de referência (ver `referencias/`) e quer mais nesse molde pra outro produto

## INPUT QUE PRECISO

Antes de gerar, confirmar com user:

1. **Produto** (nome + categoria) — ex: "Sano Cálcio (suplemento de cálcio pra osteoporose)"
2. **Problema que resolve** (1 frase) — ex: "osteoporose pós-menopausa / risco de fratura"
3. **Ângulo / mecanismo central** — ex: "absorção 87% via cálcio bisglicinato em vez de carbonato"
4. **Estatística-chave** (opcional mas potente) — ex: "9 de cada 10 mulheres acima de 50 perdem massa óssea sem perceber"
5. **Quantidade de criativos** (1-30, default 11)
6. **Templates a usar** (default: mix dos 4) — A (Revelação), B (Investigação), C (Sintoma), D (Pós-tratamento)

Se algum item faltar, pergunte ANTES de gerar — não invente contexto.

## TEMPLATES DISPONÍVEIS (DNA visual extraído)

### Template A — "REVELAÇÃO MÉDICA / ESTUDO" (refs: v8, v13, v10)
- Pill ciano top-left: "REVELAÇÃO MÉDICA" / "ESTUDO EUROPEU" / "ALERTA MÉDICO"
- Triângulo vermelho de alerta no canto sup-esquerdo
- Círculo grande no canto sup-direito com ressonância/render médico
- Headline 3-4 linhas no centro/rodapé, 1-2 palavras em CIANO #2DD4D8
- Sub-headline pequena cinza
- Footer: "logo NEWS" + seta ciano

### Template B — "INVESTIGAÇÃO" (refs: v11, v4)
- Pill ciano superior ou no meio
- Headline GIGANTE caixa alta, ciano em palavras-chave
- Background hospitalar/cirúrgico desfocado
- Footer: "Investigação News" / "{X} News"

### Template C — "URGENTE/SINTOMA" (refs: v12, v5)
- Pill vermelha "URGENTE" + triângulo amarelo no topo
- Pessoa com dor/desconforto (foto real esmaecida) atrás
- Círculo mostra o "ponto problemático" do corpo em vermelho
- Tom emocional, dor visível
- Headline curta com palavra ciano + "NÃO É AZAR" / "PODE SER EVITADA"

### Template D — "PÓS-CIRURGIA / PROBLEMA REAL" (refs: v7, news-01, news-02, news-03)
- Pill ciano ou vermelha (CUIDADO / EXCLUSIVO / URGENTE)
- Imagem impactante no círculo (cicatriz, parafusos cirúrgicos, complicação)
- Headline LONGA multi-linha (4-6 linhas)
- Tom: "olha o que pode dar errado se você não usar"
- Footer: "Saúde em Foco" / "GNEWS" / "Coluna Hoje"

## SISTEMA VISUAL FIXO (NÃO MUDA)

```
Formato:           1080x1080 (Meta Ads padrão)
Background:        Preto puro #000000 ou degradê preto→azul-meia-noite #001833
Cor highlight:     Ciano #2DD4D8 (usado em 1-2 palavras da headline + footer)
Cor alerta:        Vermelho #E63946 (triângulo + pills urgentes)
Texto:             Branco #FFFFFF (corpo) / Cinza claro #C9C9C9 (sub)
Tipografia:        Sans-serif extra-bold pesada (Inter Black / Montserrat ExtraBold)
Círculo destaque:  Borda fina ciano 4-6px, canto sup-direito, ~40% width
Triângulo alerta:  Vermelho #E63946, canto sup-esquerdo
Pill superior:     Ciano arredondado OU vermelho arredondado
Footer:            Logo fake "{X} NEWS" + seta ciano →
```

## PROCESSO (passo a passo)

### 1. Confirmar inputs
- Faça as 6 perguntas via AskUserQuestion (1 chamada agrupada)
- NÃO prossiga sem produto + problema + ângulo definidos

### 2. Escolher pasta de output
- Default: `C:\Users\user\Desktop\criativos-manchete\{slug-produto}-{YYYY-MM-DD}/`
- Confirme com o user

### 3. Gerar copy de cada criativo
- Use o agente `copy-master-chief` OU escreva direto seguindo padrão AlinhaFácil:
  - Headline: pergunta retórica OU revelação OU estatística
  - 1-2 palavras-chave destacáveis em ciano
  - Subheadline: validação científica/profissional
  - Pill: "REVELAÇÃO MÉDICA" / "URGENTE" / "ALERTA" / "ESTUDO" / "EXCLUSIVO"

### 4. Rodar o script Python
- Path: `~/.claude/skills/criativos-manchete/scripts/gerar.py`
- Recebe JSON com lista de criativos (texto + template + descrição imagem)
- Chama Gemini 3.1 Flash Image Preview pra cada um
- Salva PNGs 1080x1080 + JPGs comprimidos pro Meta Ads

### 5. Validação
- Após gerar, Read 3 amostras (uma de cada template usado)
- Conferir ortografia PT-BR (Gemini 3.1 normalmente acerta, mas validar)
- Se algum saiu errado, regerar individualmente

### 6. Entregar
- Listar paths absolutos
- Mostrar 1-2 amostras visualmente
- Oferecer próximos passos: subir no Meta Ads, gerar variações de italiano, etc

## CHAVE GEMINI

A chave fica em `C:\Users\user\Desktop\Sanologia\.env` (variável `GEMINI_API_KEY`).
Modelo OBRIGATÓRIO: `gemini-3.1-flash-image-preview` (única que escreve PT-BR sem erros).
NUNCA usar `gemini-2.5-flash-image` quando o criativo tem texto sobreposto.

## REGRAS CRÍTICAS

1. **Compliance Anvisa**: criativos pra suplemento NÃO podem prometer cura, prevenção ou tratamento de doença. Use linguagem de "estudo mostra", "pode ajudar", "associado a", etc.
2. **Compliance Meta Ads**: evitar before/after explícitos, evitar dor física dramatizada extrema, evitar texto que culpe corpo do usuário.
3. **Headline máx 50 caracteres por linha**: senão Gemini quebra mal.
4. **Palavra ciano**: SEMPRE 1-2 palavras-chave da headline destacadas em #2DD4D8.
5. **Sem mockups de produto**: o círculo NUNCA mostra o produto — sempre o problema/causa.

## ESTRUTURA DE OUTPUT JSON (config dos criativos)

```json
{
  "produto": "Sano Cálcio",
  "slug": "sano-calcio",
  "output_dir": "C:\\Users\\user\\Desktop\\criativos-manchete\\sano-calcio-2026-05-11",
  "criativos": [
    {
      "id": "01",
      "template": "A",
      "pill": "REVELAÇÃO MÉDICA",
      "headline_linhas": ["Osteoporose:", "9 em cada 10", "passam sem saber"],
      "palavras_ciano": ["9 em cada 10"],
      "subheadline": "Estudo brasileiro com 2.400 mulheres após os 50",
      "imagem_circulo": "MRI scan of osteoporotic vertebra with visible bone density loss, black and white medical imaging",
      "background": "subtle anatomical illustration of spine on black background, faded",
      "footer_brand": "SAÚDE NEWS"
    }
  ]
}
```

## EXEMPLO DE INTERAÇÃO IDEAL

```
User: /criativos-manchete
Claude: [AskUserQuestion com 4 perguntas agrupadas]
User: [responde]
Claude: Beleza, vou gerar 11 criativos do {produto} no estilo manchete. Pode confirmar?
[mostra 1 preview de copy]
User: pode
Claude: [roda script, salva, mostra 2 amostras]
"✅ 11 criativos em {path}. Quer que eu suba no Meta Ads ou traduza pra italiano?"
```
