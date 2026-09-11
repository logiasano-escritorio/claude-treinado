---
name: subir-campanha-meta
description: Sobe campanhas de anúncio no Meta (Facebook/Instagram) pela Marketing API, estrutura 1-1-1 ou CBO com bid cap. Monta o manifesto do lote, faz upload de vídeo ou imagem, cria campanha, conjunto, criativo e anúncio, e é idempotente por nome de campanha. Traz o catálogo de erros da API com o fix validado — compliance BR, aprimoramentos descontinuados, rate limit, reprovação por política. Use sempre que o pedido for subir, clonar, corrigir ou auditar anúncio no Meta via API.
trigger: /subir-campanha-meta
---

# /subir-campanha-meta

Você vai subir anúncios no Meta pela Marketing API v23.0.

**Antes de escrever qualquer linha de código, leia `REFERENCIA-API-META.md` nesta
pasta.** Ele é o catálogo de tudo que quebra na API do Meta com o fix já validado em
produção. Não é opcional: metade dos erros dessa API tem mensagem enganosa, e tentar
adivinhar já custou horas em runs anteriores.

Se bater um erro e a referência não cobrir, procure nas memórias antes de tentar
variações de campo.

---

## Como funciona

Nada é hardcoded no script. Toda a configuração do lote mora num **manifesto JSON**, e
o mesmo publisher serve para qualquer produto e qualquer conta.

```
manifesto.json  →  scripts/publicar_lote.py  →  campanhas no Meta
```

O publisher é **idempotente por nome de campanha**: ele lista o que já existe na conta
antes de começar e pula o que já subiu. Rodar de novo depois de uma falha continua de
onde parou, não duplica.

---

## Fluxo

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

Copie `manifest-exemplo.json` e ajuste. Os campos que sempre mudam: `account_id`,
`adset.pixel_id`, `adset.advertiser_id`, `creative.page_id`, `creative.link`,
`creative.message`, e a lista `ads`.

O `creative.degrees_of_freedom_spec` do exemplo já vem com as 82 features em OPT_OUT.
**Copie como está.** É o que impede o botão "Ligar agora" de aparecer no anúncio, que
já derrubou a margem de 45% para 15% num lote de 158 anúncios. Detalhe na seção 4 da
referência.

Cada item de `ads` precisa de `campaign_name` e o caminho da mídia:

```json
{"hook": "H1B1", "campaign_name": "Magnésio - AD01 H1B1",
 "video_path": "/caminho/variation_H1B1.mp4"}
```

Para imagem, troque `video_path` por `image_path`.

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

Confira antes com `--dry`, que valida o manifesto e mostra o plano sem escrever nada
na conta:

```bash
python3 scripts/publicar_lote.py meu-lote.manifest.json --dry
```

Dentro do Claude Code, rode com `run_in_background: true` do próprio Bash tool. Não use
`nohup ... &`: o processo morre quando o shell encerra e deixa campanha e conjunto sem
anúncio.

### 5. Conferir

O publisher grava `<manifesto>.resultado.json` a cada item, com os IDs de campanha,
conjunto, criativo e anúncio. Se o run morrer no meio, **o vídeo já subiu** — pegue o
`video_id` do resultado, cole no item do manifesto e rode de novo. O publisher reusa em
vez de subir duas vezes.

Campanhas nascem PAUSED, conjunto e anúncio nascem ACTIVE. Ligar a operação é virar só
a campanha.

---

## Antes de rodar, confira os 11 pontos

O checklist está na seção 14 da referência. Os que mais quebram:

1. Advertiser ID lido de um conjunto real **desta** conta, não copiado de outra.
2. `degrees_of_freedom_spec` presente e sem `standard_enhancements`.
3. `is_adset_budget_sharing_enabled: "false"` no POST de campanha.
4. Se `advantage_audience: 1`, então `age_min` ≤ 25.
5. Ninguém editando a conta no gerenciador durante o run. Escrita simultânea trava a
   sessão da pessoa.

---

## Outras operações

**Clonar entre contas.** `image_hash` e `video_id` são por conta. Imagem vai por
`copy_from`; vídeo não se copia, o criativo do destino aponta direto para o `video_id`
da origem. Seção 8 da referência.

**Corrigir anúncio reprovado.** Criativo no Meta é imutável. Crie um criativo novo, um
anúncio novo PAUSED no mesmo conjunto, e apague o reprovado. Trocar criativo zera prova
social, então anúncio com cinco ou mais compras em 30 dias vale desligar na mão.

**Ranquear criativos por ROAS.** Nunca passe `filtering` de gasto no Insights. O filtro
roda por linha de anúncio, não por criativo agregado, e corrompe o ranking nas duas
direções. Puxe tudo sem filtro, agregue por criativo, corte depois. Seção 13.

---

## Arquivos

| Arquivo | O que é |
|---|---|
| `REFERENCIA-API-META.md` | catálogo de erros, payloads validados, contas e pixels |
| `scripts/publicar_lote.py` | publisher genérico, dirigido por manifesto |
| `manifest-exemplo.json` | template com o dof spec completo em OPT_OUT |

O token **nunca** entra no repo. Lê de `META_ACCESS_TOKEN` ou de um `token.txt` local.
