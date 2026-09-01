---
description: Gera 30 textos FB Ads (texto principal + título + descrição) pros 30 criativos de um funil Sano. Lê hooks.json + advertorial, chama Copy Master Chief, valida compliance Anvisa+FB, gera ads.json + ads-import.csv (bulk import FB), atualiza nota Obsidian
argument-hint: <produto> <slug-funil>
---

# Gerador de 30 Textos FB Ads — Sano

`$ARGUMENTS` no formato: `<produto> <slug-funil>`

Exemplo: `/sano-anuncios StrongBones artrose`

Pré-requisito: o funil já tem que ter `/sano-criativos` rodado (precisa do `hooks.json`).

---

## ⚠️ MÉTODO

Pra cada um dos 30 hooks visuais, gera **1 texto único** que conversa com a headline da imagem (Estilo A) ou com a cena pura (Estilo B), seguindo:

- **Princípio mestre:** "A headline da imagem é o gancho. O texto principal é a vara de pesca. NUNCA dizem o mesmo, mas SEMPRE puxam o mesmo peixe."
- **3 templates por nível de consciência (Schwartz):**
  - **A — Problem Aware** (sente dor, não sabe causa) → B1, B3
  - **B — Solution Aware** (sabe que tem solução) → B2, B5
  - **C — Product/Retargeting Aware** → B4, B6
- **Matriz de sincronia headline-imagem ↔ texto:** já documentada na nota `Funis/<slug>.md`

---

## Etapa 0 — Verificações

```bash
FUNIL_DIR="c:/Users/user/Desktop/_Projetos/relivia-editor/outputs_sano/<produto-lower>/<slug>"
ls "$FUNIL_DIR/hooks.json" 2>/dev/null || echo "FUNIL SEM hooks.json — rodar /sano-criativos primeiro"
ls "$FUNIL_DIR/ads.json" 2>/dev/null && echo "JÁ EXISTE — sobrescrever?"
```

Se já existir, pergunta ao usuário.

---

## Etapa 1 — INTELIGÊNCIA: extrair contexto

Leia em paralelo:
1. `outputs_sano/<produto-lower>/<slug>/hooks.json` (30 hooks visuais já existentes)
2. `Sanologia/adv-<produto-lower>-<slug>.html` (advertorial pra extrair: mecanismo, persona, especialista, prova social numérica)
3. `Sanologia/<página-do-produto>.html` (preço, garantia, depoimentos)
4. `_Projetos/relivia-editor/sano-energy-b12/CATALOGO-COPIES.md` (entrada do ângulo)

---

## Etapa 2 — GERAÇÃO: chamar Copy Master Chief

Use a Task tool com `subagent_type: "general-purpose"` rodando o **Copy Master Chief**.

**Prompt do sub-agente:**

```
Você é o Copy Master Chief — orquestra Halbert, Schwartz, Sugarman, Bencivenga, Lampropoulos, Evaldo Albuquerque, Stefan Georgi.

Especialidade: Facebook Ads de suplemento de saúde, mercado brasileiro.

CONTEXTO:
- Produto: Sano <produto>
- Ângulo: <slug>
- 30 hooks visuais já existem em hooks.json (15 estilo A com headline + 15 estilo B cena pura)
- Cada hook = 1 anúncio. Você vai escrever 30 textos únicos, 1 por hook.

LEIA antes de escrever:
- outputs_sano/<produto-lower>/<slug>/hooks.json
- Sanologia/adv-<produto-lower>-<slug>.html
- Sanologia/<página-do-produto>.html

EXTRAIA do advertorial:
- Mecanismo único (ex: "osso subcondral", "metilcobalamina ativa")
- Persona/paciente (nome BR, idade, cidade, contexto)
- Especialista (Dr. fulano, credenciais)
- Prova social numérica (% melhorou, anos de estudo, etc)
- 3 maiores objeções

PARA CADA UM DOS 30 HOOKS:

Decida o template (A/B/C) usando a matriz:
- B1 Espelho de Dor + B3 Pattern Interrupt → A (Problem Aware)
- B2 Incongruência Científica + B5 Credibilidade → B (Solution Aware)
- B4 Antes/Depois + B6 Urgência Silenciosa → C (Product/Retargeting Aware)

Decida sincronia com a headline da imagem usando a matriz:
- Headline = descoberta científica → texto continua + persona
- Headline = dor/sintoma → texto espelha + vira chave pra causa nova
- Headline = negação contraintuitiva → amplifica com prova
- Headline = transformação → ignora + conta a origem
- CENA PURA (Estilo B) → texto carrega 100%, abre com pergunta-espelho

ESCREVA texto principal + título + descrição.

REGRAS DE COPY:
- Texto principal: 400-900 char, parágrafos curtos com \n\n entre eles
- Título: 27-40 char, sem ponto final, sem emoji
- Descrição: deixar vazio (mobile corta)
- CTA termina com seta → "Leia a explicação completa →" ou "Veja como →" ou "A história completa →"

REGRAS DE COMPLIANCE (BANIMENTO FB + MULTA ANVISA):
NUNCA usar: cura, curar, trata, tratar, elimina, eliminar, milagre, milagrosa, mágico, garantido, 100%, "antes e depois" literal
SEMPRE usar: "auxilia", "suporta", "interrompe a progressão", "matéria-prima", "modula"
Citar terceiros: "estudo da X universidade", "Dr. Y publicou em ano Z"
Especialista: SEMPRE homem (regra Relívia)

UTF-8 CRÍTICO:
Escreva todos os acentos corretamente. ZERO ? no lugar de letra. ZERO U+FFFD. Texto em PT-BR válido.

OUTPUT: array JSON com 30 entradas no formato exato:
{
  "id": "<copia do hook>",
  "bloco": "<copia do hook>",
  "estilo": "A" ou "B",
  "headline_imagem": "<copia da headline OU '(cena pura, sem texto)'>",
  "template": "A-Problem-Aware" | "B-Solution-Aware" | "C-Product-Aware",
  "texto_principal": "...",
  "titulo": "...",
  "descricao": "",
  "cta": "LEARN_MORE"
}

Salve em outputs_sano/<produto-lower>/<slug>/ads.json
```

---

## Etapa 3 — VALIDAÇÃO automática

Rode esse Python pra validar o `ads.json`:

```python
import json, re
ads = json.load(open('outputs_sano/<produto-lower>/<slug>/ads.json', encoding='utf-8'))

assert len(ads) == 30, f"Esperado 30, veio {len(ads)}"

banned = ['cura', 'curar', 'cure', 'trata ', 'tratar', 'elimina', 'eliminar',
          'milagre', 'milagrosa', 'milagroso', 'magico', 'magica',
          'garantido', 'garantida', '100%', 'cientificamente comprovado']

issues = []
for ad in ads:
    txt = (ad['texto_principal'] + ' ' + ad['titulo']).lower()
    for word in banned:
        if re.search(r'\b' + re.escape(word) + r'\b', txt):
            issues.append((ad['id'], word))
    full = ad['texto_principal'] + ad['titulo']
    if '?' in full:
        # verifica ? quebrado (letra + ? + letra sem espaço)
        if re.search(r'[a-zA-Záéíóúãõâêîôûç]\?(?=[a-zA-Z])', full):
            issues.append((ad['id'], 'UTF-8 quebrado'))
    if '�' in full:
        issues.append((ad['id'], 'replacement char'))
    if len(ad['texto_principal']) < 350 or len(ad['texto_principal']) > 1000:
        issues.append((ad['id'], f"comprimento texto {len(ad['texto_principal'])}"))
    if len(ad['titulo']) > 40:
        issues.append((ad['id'], f"titulo {len(ad['titulo'])} > 40"))

if issues:
    print("ISSUES:", issues)
    # se houver compliance issue, peça pro Copy Master Chief regerar SÓ os afetados
else:
    print("OK")
```

Se tiver issues, peça pro Copy Master Chief regerar SÓ os ads afetados (passa o ID + o problema).

---

## Etapa 4 — Gerar CSV bulk import

⚠️ **UTM IMPORTANTE:** UTMs do Meta usam **variáveis dinâmicas `{{}}`** que o próprio Meta substitui em runtime. NÃO hardcode UTM por ad — usa o template padrão:

```
utm_source=FB&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}&utm_term={{placement}}
```

Esse valor vai no **campo "URL Tags" / "Parâmetros de URL"** do Meta Ads (nativo da plataforma), **não concatenado na URL final**. O `Link` do CSV deve ser **a URL limpa** sem UTM.

```python
import csv
URL_DESTINO = "https://sanobrasil.com/adv-<produto-lower>-<slug>"
URL_TAGS = "utm_source=FB&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}&utm_term={{placement}}"

with open('outputs_sano/<produto-lower>/<slug>/ads-import.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(['Ad Name','Ad Status','Image File Name','Body','Title',
                'Description','Link','Display Link','Call to Action','URL Tags'])
    for ad in ads:
        w.writerow([
            f"sano-<produto-lower>-<slug>-{ad['id']}",
            'PAUSED',
            f"creatives/criativo_{ad['id']}.png",
            ad['texto_principal'],
            ad['titulo'],
            ad.get('descricao',''),
            URL_DESTINO,         # link LIMPO — sem UTM
            'sanobrasil.com',
            ad['cta'],
            URL_TAGS             # UTMs vão aqui, com {{}}, Meta resolve em runtime
        ])
```

CSV em **utf-8-sig** (BOM) — Facebook Ads Manager exige.

---

## Etapa 5 — Criar/atualizar `_funil.json`

Atualize/crie `outputs_sano/<produto-lower>/<slug>/_funil.json` com a seção `anuncios`:

```json
{
  "anuncios": {
    "total": 30,
    "templates": {"A-Problem-Aware": N, "B-Solution-Aware": N, "C-Product-Aware": N},
    "arquivo_json": "ads.json",
    "arquivo_csv_bulk_import": "ads-import.csv",
    "data_geracao": "<DD/MM/AAAA>"
  },
  "utm_template": {
    "_nota": "Padrao Meta — vai no campo 'URL Tags' do Ads Manager, nao na URL final. Meta substitui as {{}} em runtime.",
    "campo_meta": "URL Tags / Parametros de URL",
    "valor": "utm_source=FB&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}&utm_term={{placement}}",
    "link_destino_limpo": "https://sanobrasil.com/adv-<produto-lower>-<slug>"
  }
}
```

---

## Etapa 6 — Atualizar nota Obsidian

Edite (ou crie) `SANOLOGIA OBSIDIAN/Funis/<produto-lower>-<slug>.md` adicionando:

1. Tabela com as 30 linhas (#, bloco, estilo, headline imagem, título FB, preview texto)
2. Distribuição de templates
3. UTM template usado
4. Linha no histórico: "DD/MM — 30 textos FB Ads gerados pelo Copy Master Chief"

Use o arquivo `Funis/strongbones-artrose.md` como template de referência.

E atualize a coluna "Criativo" do `<Produto>.md` apontando pra essa nota.

---

## Output final pro usuário

- ✅ 30/30 textos gerados
- ✅ Compliance: 0 issues
- ✅ UTF-8: 0 quebrado
- 📁 `outputs_sano/<produto>/<slug>/ads.json` + `ads-import.csv`
- 📊 Nota Obsidian: `Funis/<produto>-<slug>.md`
- 🎯 UTM template aplicado
- 🚀 Próximo passo: rodar `/sano-publicar <produto> <slug>` (sobe via Meta API, status PAUSED)

---

## Regras importantes

- **30 textos = 30 hooks** (1 por imagem)
- **Cada texto é único** — não copia entre IDs
- **Compliance Anvisa+FB** validado automaticamente
- **UTF-8 obrigatório** — zero `?` quebrado, zero replacement char
- **Especialista sempre homem** (regra Relívia)
- **CTA termina com seta `→`**
- **Descrição vazia** (mobile corta)
- **CSV em utf-8-sig** (BOM obrigatório pro FB Ads Manager)
- Use TodoWrite pra trackar etapas

Comece agora pelo funil: **$ARGUMENTS**
