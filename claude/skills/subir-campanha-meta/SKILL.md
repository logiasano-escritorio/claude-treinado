---
name: subir-campanha-meta
description: Sobe campanhas de anúncio no Meta (Facebook/Instagram) pela Marketing API — estruturas 1-1-1, 1-1-N, ABO e CBO, com lance de menor custo, bid cap ou cost cap. Monta o manifesto do lote, faz upload de vídeo (arquivo local ou Google Drive) ou imagem, ou reusa um post existente, cria campanha/conjunto(s)/criativo/anúncio, e é idempotente por nome. Também copia ou move campanha(s) inteiras entre contas, com os mesmos lances e pelos posts já existentes. Traz o catálogo de erros da API com o fix validado — compliance BR, aprimoramentos descontinuados, rate limit, reprovação por política, permissão de página, conta não qualificada, limite de conjuntos por campanha. Use sempre que o pedido for subir, clonar, mover, corrigir ou auditar anúncio no Meta via API.
trigger: /subir-campanha-meta
---

# /subir-campanha-meta

Você vai subir, copiar ou mover anúncios no Meta pela Marketing API v23.0.

**Antes de escrever qualquer linha de código, leia `REFERENCIA-API-META.md` nesta
pasta.** Ele é o catálogo de tudo que quebra na API do Meta com o fix já validado em
produção. Não é opcional: metade dos erros dessa API tem mensagem enganosa, e tentar
adivinhar já custou horas em runs anteriores. A seção "Aprendizados de novembro/2026"
traz o que foi validado por último — permissão de página, conta travada por pagamento
pendente, limite de conjuntos por campanha CBO.

Se bater um erro e a referência não cobrir, procure nas memórias antes de tentar
variações de campo.

---

## Quando usar cada script

| Você quer... | Script |
|---|---|
| Subir um lote novo de anúncios (vídeo, imagem ou post) | `scripts/publicar_lote.py` |
| Copiar uma campanha pra outra conta, mantendo os posts | `scripts/copiar_campanhas.py` |
| Mover uma campanha (copiar + pausar a original) | `scripts/copiar_campanhas.py --pausar-original` |

Nada é hardcoded nos scripts. Toda a configuração mora num **manifesto JSON** (para
subir) ou em **flags de linha de comando** (para copiar/mover), e o mesmo script serve
para qualquer produto e qualquer conta.

```
manifesto.json  →  scripts/publicar_lote.py       →  campanhas novas no Meta
campaign_id(s)  →  scripts/copiar_campanhas.py     →  copia pra outra conta
```

Ambos são **idempotentes**: o publisher por nome de campanha (e, dentro dela, nome de
conjunto e de anúncio, guardado no `.resultado.json`); o copiador por `campaign_id` de
origem, guardado no arquivo de `--estado`. Rodar de novo depois de uma falha continua
de onde parou, não duplica.

---

## Fluxo pra subir um lote

### 1. Levantar a configuração da conta

Nunca reaproveite configuração de outra conta. Pixel, página, Instagram e advertiser ID
mudam por conta, e às vezes por campanha. Confirme os quatro:

```bash
# conta viva?
curl -s "https://graph.facebook.com/v23.0/act_<ID>?fields=name,account_status,currency&access_token=$META_ACCESS_TOKEN"

# páginas liberadas nesta conta
curl -s "https://graph.facebook.com/v23.0/act_<ID>/promote_pages?access_token=$META_ACCESS_TOKEN"

# advertiser ID: leia de um conjunto que já está no ar NESTA conta
curl -s "https://graph.facebook.com/v23.0/<ADSET_ID>?fields=regional_regulated_categories,regional_regulation_identities&access_token=$META_ACCESS_TOKEN"
```

A seção 9 da referência tem a tabela de contas, pixels e páginas já mapeados.

### 2. Montar o manifesto

Escolha o exemplo mais parecido com o que você vai subir e copie:

| Arquivo | Caso |
|---|---|
| `manifest-exemplo.json` | 1-1-1 — uma campanha por criativo, vídeo ou imagem local |
| `manifest-exemplo-1-1-10-drive.json` | 1-1-N — um lote de vídeos de uma pasta pública do Google Drive |
| `manifest-exemplo-abo-bidcap.json` | ABO — orçamento por conjunto/ângulo, com bid cap |
| `manifest-exemplo-cbo-post.json` | CBO — orçamento único competindo entre conjuntos, anúncio por post existente |

O `creative.degrees_of_freedom_spec` dos exemplos já vem com as 82 features em
OPT_OUT. **Copie como está.** É o que impede o botão "Ligar agora" de aparecer no
anúncio, que já derrubou a margem de 45% para 15% num lote de 158 anúncios. Só não é
necessário quando **todos** os anúncios do manifesto são por `post_id` (anúncio já
existe, o criativo não é recriado). Detalhe na seção 4 da referência.

#### Estruturas

| Estrutura | Onde mora o orçamento | Onde mora o lance | Campo no manifesto |
|---|---|---|---|
| `1-1-1` | campanha (1 por criativo) | campanha + conjunto | `estrutura: "1-1-1"`, lista `ads` |
| `1-1-N` | campanha (1 por lote de N) | campanha + conjunto | `estrutura: "1-1-N"`, `anuncios_por_conjunto`, `campanha_nome_base`, lista `ads` |
| `ABO` | em cada conjunto | em cada conjunto | `estrutura: "ABO"`, `campanha_nome`, lista `conjuntos` |
| `CBO` | na campanha, conjuntos competem | em cada conjunto (se houver cap) | `estrutura: "CBO"`, `campanha_nome`, lista `conjuntos` |

`1-1-1` e `1-1-N` usam a lista plana `ads` (cada item vira um anúncio; em `1-1-N` os
itens são agrupados em lotes de `anuncios_por_conjunto`, até 50 por conjunto — limite
da API). `ABO` e `CBO` usam a lista `conjuntos`, onde cada item tem seu próprio `nome`
e sua própria lista `ads`; dá pra sobrescrever `orcamento_valor_cents`,
`bid_valor_cents`, `targeting` e outros campos por conjunto.

#### Estratégias de lance

| Estratégia | `bid_strategy` | `bid_amount` | Campo no manifesto |
|---|---|---|---|
| Menor custo (sem lance) | `LOWEST_COST_WITHOUT_CAP` | não envia | `lance: {"estrategia": "menor_custo"}` |
| Bid cap | `LOWEST_COST_WITH_BID_CAP` | no conjunto | `lance: {"estrategia": "bid_cap", "valor": <centavos>}` |
| Cost cap | `COST_CAP` | no conjunto (teto de custo) | `lance: {"estrategia": "cost_cap", "valor": <centavos>}` |

#### Orçamento

```json
"orcamento": {"tipo": "diario", "valor": 3000}
"orcamento": {"tipo": "total", "valor": 150000, "fim": "2026-12-31T23:59:59-0300"}
```

`tipo: "total"` (lifetime budget) é **novo e não validado num run real ainda** — teste
com uma campanha pequena antes de confiar num lote grande. Se a API reclamar de campo
faltante, registre o erro em `REFERENCIA-API-META.md`.

#### Fonte de criativo, por item de `ads` (ou de `conjuntos[].ads`)

| Campo | Quando usar |
|---|---|
| `video_path` | vídeo em arquivo local, até ~90MB |
| `video_drive_id` | vídeo numa pasta pública do Google Drive (sobe direto por `file_url`, sem baixar) |
| `image_path` | imagem em arquivo local |
| `post_id` | anúncio já existe como post — **preferido** quando existe, mantém curtidas/comentários, não recria o criativo |

#### Lote inteiro a partir de uma pasta do Drive

```json
"drive_pasta": {
  "pasta_id": "<id da pasta pública>",
  "excluir": ["\\(Corrigir\\)", "\\(RECRIAR\\)"],
  "incluir_apenas": []
}
```

`excluir` é uma lista de **regex** testada contra o nome do arquivo. `incluir_apenas`,
se não vazia, é uma lista fechada de nomes já validados — ignora `excluir` e só pega o
que estiver nela. Só entram arquivos `.mp4`/`.mov`/`.m4v`. Funciona só com `estrutura`
`1-1-1` ou `1-1-N`; para `ABO`/`CBO` liste os anúncios manualmente em cada conjunto
(normalmente por `post_id`, já que são campanhas maduras).

### 3. Passar a copy pelos dois filtros

**Markdown não renderiza no Facebook.** Long-form vindo do Obsidian leva `**negrito**`
literal para o feed. Limpe os asteriscos e as linhas `---`, preservando as quebras.

**Nome de ingrediente reprova por falso positivo de cannabis ou de medicamento.**
Ofusque os termos-gatilho com zero-width joiner. Nunca suavize a alegação: só o nome
técnico do ingrediente leva o caractere invisível. A lista completa e o método estão na
seção 10 da referência.

### 4. Rodar

```bash
export META_ACCESS_TOKEN="..."          # ou crie token.txt ao lado do script
python3 scripts/publicar_lote.py meu-lote.manifest.json
```

Confira antes com `--dry`, que valida o manifesto e mostra o plano — quantas
campanhas/conjuntos/anúncios e o **orçamento total por dia** — sem escrever nada na
conta:

```bash
python3 scripts/publicar_lote.py meu-lote.manifest.json --dry
```

Dentro do Claude Code, rode a versão sem `--dry` com `run_in_background: true` do
próprio Bash tool. Não use `nohup ... &`: o processo morre quando o shell encerra e
deixa campanha e conjunto sem anúncio.

### 5. Conferir

O publisher grava `<manifesto>.resultado.json` a cada objeto criado (campanha,
conjunto, anúncio), com os IDs. Se o run morrer no meio, **o vídeo já subiu** — ele
fica salvo no estado e o publisher reusa em vez de subir de novo, sem precisar editar o
manifesto na mão. Nunca delete esse arquivo entre runs: é dele que vem a idempotência
de conjunto e de anúncio (a de campanha também é conferida direto na conta, por nome).

Campanhas nascem com o `status` do manifesto (normalmente `PAUSED`); conjunto e
anúncio nascem `ACTIVE` (ou o que estiver em `ad_status`). Ligar a operação é virar só
a campanha.

O relatório final no terminal mostra criados por tipo, erros agrupados por motivo, e
páginas sem permissão — confira antes de considerar o lote completo.

---

## Antes de ativar, confira os 12 pontos

O checklist completo está na seção 14 da referência. Os que mais quebram:

1. Advertiser ID lido de um conjunto real **desta** conta, não copiado de outra.
2. `degrees_of_freedom_spec` presente e sem `standard_enhancements` (exceto se 100% por
   post existente).
3. `is_adset_budget_sharing_enabled: "false"` no POST de campanha.
4. Se `advantage_audience: 1`, então `age_min` ≤ 25.
5. **Orçamento total por dia** do lote — confira o número que o `--dry` imprime antes
   de rodar de verdade.
6. Cartão/saldo da conta de destino em dia (conta com pagamento pendente não deixa
   criar nem pausar nada — seção "Aprendizados de novembro/2026").
7. Página do criativo liberada na conta (`/promote_pages`); se faltar, o run segue e
   lista no relatório final em vez de travar o lote inteiro.
8. Página de destino (link do anúncio) no ar, com o pixel certo instalado.
9. Ninguém editando a conta no gerenciador durante o run. Escrita simultânea trava a
   sessão da pessoa.

---

## Copiar ou mover campanha(s) entre contas

```bash
export META_ACCESS_TOKEN="..."
python3 scripts/copiar_campanhas.py \
  --origem 120211111111111 120222222222222 \
  --destino act_X \
  --estado copia-magnesio.json \
  --dry
```

Tira o `--dry` pra aplicar. Pra mover (copia e pausa a original quando todos os
anúncios tiverem sido copiados):

```bash
python3 scripts/copiar_campanhas.py --origem 120211111111111 --destino act_X \
  --estado move-magnesio.json --pausar-original
```

Pra uma lista grande de campanhas (ex. top N por ROAS), use `--origem-arquivo` com um
JSON de lista de IDs ou de `{"id": ...}`:

```bash
python3 scripts/copiar_campanhas.py --origem-arquivo top20.json --destino act_X \
  --estado copia-top20.json
```

O que é copiado: campanha (orçamento, `bid_strategy`), todos os conjuntos (targeting,
`promoted_object`, `optimization_goal`, `billing_event`, `attribution_spec`,
`bid_amount`, status), e os anúncios **por post existente**
(`effective_object_story_id` + `url_tags`), com o mesmo status. `image_hash` e
`video_id` são por conta — por isso a cópia é sempre por post, nunca recriando o
criativo do zero.

Se um conjunto da origem for antigo e não tiver `regional_regulation_identities`
salvo, o script não quebra: usa `--pagador-regulacao <advertiser_id>` se você passar a
flag, ou avisa e pula aquele conjunto se você não passar. Nunca inventa um ID.

**Clonar entre contas, do zero (sem post existente).** Fora do alcance deste script —
`image_hash` vai por `copy_from`, vídeo aponta direto pro `video_id` da origem. Seção 8
da referência.

**Corrigir anúncio reprovado.** Criativo no Meta é imutável. Crie um criativo novo, um
anúncio novo PAUSED no mesmo conjunto, e apague o reprovado. Trocar criativo zera prova
social, então anúncio com cinco ou mais compras em 30 dias vale desligar na mão.

**Ranquear criativos por ROAS.** Nunca passe `filtering` de gasto no Insights. O filtro
roda por linha de anúncio, não por criativo agregado, e corrompe o ranking nas duas
direções. Puxe tudo sem filtro, agregue por criativo, corte depois. Seção 13.

---

## Migração do manifesto antigo

Manifesto sem `estrutura`/`orcamento`/`lance` (formato anterior a novembro/2026)
continua funcionando **sem nenhuma mudança**: o publisher normaliza
`campanha.daily_budget_cents` → `orcamento`, e `campanha.bid_strategy` +
`adset.bid_amount` → `lance`, e assume `estrutura: "1-1-1"`. O `.resultado.json` no
formato antigo (lista plana) também é lido e convertido automaticamente — não precisa
apagar nem converter nada na mão.

---

## Arquivos

| Arquivo | O que é |
|---|---|
| `REFERENCIA-API-META.md` | catálogo de erros, payloads validados, contas e pixels |
| `scripts/publicar_lote.py` | publisher dirigido por manifesto — 1-1-1, 1-1-N, ABO, CBO |
| `scripts/copiar_campanhas.py` | copia/move campanha(s) entre contas, por post existente |
| `manifest-exemplo.json` | template 1-1-1 |
| `manifest-exemplo-1-1-10-drive.json` | template 1-1-N a partir de pasta do Drive |
| `manifest-exemplo-abo-bidcap.json` | template ABO com bid cap por conjunto |
| `manifest-exemplo-cbo-post.json` | template CBO com anúncio por post existente |

O token **nunca** entra no repo. Lê de `META_ACCESS_TOKEN` ou de um `token.txt` local
(só o `publicar_lote.py` aceita `token.txt`; `copiar_campanhas.py` exige a variável de
ambiente).
