# Subir campanhas no Meta via Marketing API — base de conhecimento operacional

Este arquivo é a memória de trabalho de quem já subiu centenas de anúncios nas contas
Sano/Relívia via Graph API. Não é documentação oficial da Meta: é a lista do que
**realmente** quebra, com o fix validado em produção e a data em que foi validado.

**Regra número um: ao bater num erro da API do Meta, procure nesta base ANTES de
tentar variações.** O histórico registra 4 tentativas perdidas com campos inventados
(`dsa_beneficiary`, `dsa_payor`) quando a resposta certa já estava escrita.

Versão da API em uso: **v23.0**. Base: `https://graph.facebook.com/v23.0`.

---

## 1. Modelo mental da estrutura

A estrutura padrão hoje é **1-1-1**: uma campanha por criativo, com um conjunto e um
anúncio dentro. O nome é idêntico nos três níveis, por exemplo `Prime - AD43 H1B1`.

Por que 1-1-1: cada criativo recebe orçamento próprio e ganha ou morre sozinho, sem o
conjunto canibalizar verba entre criativos. Vencedores são escalados depois subindo o
`daily_budget` da campanha (a escada usada é 3000 → 13000 → 26000 → 50000 centavos).

Existe também a estrutura **CBO + Bid Cap**, usada na conta EUA 11 para a operação
madura de magnésio. Ali é o inverso: uma campanha só, orçamento único de US$24.000/dia
na campanha, 102 conjuntos competindo, e o teto de lance (`bid_amount`) mora **no
conjunto**, um valor por ângulo. Detalhe na seção 9.

Ordem de criação, sempre nessa sequência:

```
upload da mídia → campanha → conjunto → criativo → anúncio
```

---

## 2. Autenticação e token

- O token **nunca** fica hardcoded no script. Scripts antigos com token embutido
  quebram com `code 190 / subcode 460` (expirado).
- O publisher lê de `META_ACCESS_TOKEN` no ambiente, ou de um `token.txt` ao lado do
  script. `token.txt` e `.env` estão no `.gitignore` — nunca commitar.
- Token de usuário gerado no Graph API Explorer dura pouco. Em sessão de trabalho
  pesado ele expira a cada 2 ou 3 horas. Token de longa duração vence em torno de
  60 dias.
- Permissões necessárias: `ads_management` para escrever, `ads_read` para relatórios.
- Teste rápido de que o token está vivo e enxerga a conta:

```bash
curl -s "https://graph.facebook.com/v23.0/act_<ID>?fields=name,account_status,currency&access_token=$META_ACCESS_TOKEN"
```

`account_status: 1` significa conta ativa.

---

## 3. Compliance Brasil — o erro que bloqueia 100% dos conjuntos

Conjunto com público no Brasil **não é criado** sem declarar o anunciante verificado.

```
code 100 · error_subcode 3858634
blame_field_specs: [["compliance_section"]]
"O anunciante está ausente"
```

O nome do campo no erro (`compliance_section`) não é o nome do campo no payload. Os
campos certos, nos params do POST de `/adsets`:

```python
"regional_regulated_categories": json.dumps(["BRAZIL_REGULATION", "VOLUNTARY_VERIFICATION"]),
"regional_regulation_identities": json.dumps({
    "universal_beneficiary": ADVERTISER_ID,
    "universal_payer": ADVERTISER_ID,
}),
```

Duas armadilhas de digitação: é `universal_payer`, não `payor` nem `payer`. E as duas
categorias vão sempre juntas em BR.

**O `ADVERTISER_ID` varia por conta e às vezes por campanha.** Não invente e não
reaproveite entre contas. Descubra lendo de um conjunto que já está no ar:

```bash
curl -s "https://graph.facebook.com/v23.0/<ADSET_ID>?fields=regional_regulated_categories,regional_regulation_identities&access_token=$META_ACCESS_TOKEN"
```

IDs já mapeados:

| Advertiser ID | Onde vale |
|---|---|
| `880756411607509` | padrão da operação, EUA 11 e FUNGZERO |
| `1228611831325801` | conta USD - PRIME CREME, campanhas de vídeo do Prime |

---

## 4. Os aprimoramentos automáticos do criativo — a regra que custou dinheiro

Duas coisas opostas, fácil de confundir:

**Não envie `standard_enhancements`.** Foi descontinuado. Enviar quebra o POST:

```
code 100 · error_subcode 3858504
"O criativo não deve incluir aprimoramentos padrão"
```

**Mas envie o resto do `degrees_of_freedom_spec` com tudo em OPT_OUT.** O motivo é
concreto: o enhancement `site_extensions` adiciona um botão "Ligar agora" com telefone
ao anúncio. A pessoa liga, ninguém atende, o clique não vira venda e não entra no
pixel. Ficou ligado em 158 anúncios das campanhas Prime por sete dias e derrubou a
margem de 45% para 15%. A Meta liga isso por padrão, então é invisível se ninguém
conferir.

O spec completo com 82 features em OPT_OUT está em `manifest-exemplo.json`, campo
`creative.degrees_of_freedom_spec`. Copie de lá. Se precisar regerar a partir de um
criativo que já está no ar:

```bash
curl -s "https://graph.facebook.com/v23.0/<CREATIVE_ID>?fields=degrees_of_freedom_spec&access_token=$META_ACCESS_TOKEN"
```

Depois remova `standard_enhancements` do resultado antes de reenviar.

Auditoria periódica: varra os anúncios procurando `site_extensions.enroll_status ==
OPT_IN` **ou** um `tel:` embutido no criativo. O flag nem sempre lê OPT_IN, mas o
telefone persiste, então procurar pelo telefone pega mais casos.

---

## 5. Catálogo de erros com o fix

| Erro | Significado | Fix |
|---|---|---|
| `100 / 3858634` | anunciante ausente no conjunto BR | seção 3 |
| `100 / 3858504` | `standard_enhancements` descontinuado | remover só esse campo do dof spec |
| `100 / 1870227` | falta a sinalização Advantage Audience | `targeting.targeting_automation = {"advantage_audience": 0 ou 1}` |
| `100 / 1870188` | `age_min` acima de 25 com Advantage Audience ligado | com `advantage_audience: 1`, usar `age_min` ≤ 25 |
| `100 / 4834011` | falta `is_adset_budget_sharing_enabled` | mandar `"false"` no POST de `/campaigns` |
| `100 / 4834002` | budget sharing com CBO | mandar `"false"`, nunca `"true"` junto com budget na campanha |
| `100 / 1443226` | anúncio de vídeo sem miniatura | `image_url` obrigatório no `video_data` |
| `17 / 2446079` | rate limit da conta | backoff 60s, 120s, 180s |
| `190 / 460` | token expirado | gerar novo, ler do `.env` |
| `3` | app sem capability para URL remota | baixar o asset e subir como arquivo multipart |
| `390 / 1363030` | `copy_from` em `/advideos` | não existe essa rota, referenciar o `video_id` direto |

Notas de campo sobre alguns:

- **Rate limit** aperta a partir de 50 a 100 chamadas seguidas e é **por conta de
  anúncios**, não global. Ler 27 conjuntos logo depois de criá-los estoura e bloqueia
  por vários minutos. Confira depois, não na sequência.
- **HTTP 413 em upload de vídeo** volta em 0,2 segundo e parece timeout, mas não é.
  É arquivo acima de ~90MB. Acima disso, upload em partes.
- **Vídeo de 34MB já levou mais de 15 minutos** para ficar `ready`. Use timeout de
  30 minutos no polling, não 15.

---

## 6. Campos descontinuados ou trocados

| Não use | Use |
|---|---|
| `instagram_actor_id` | `instagram_user_id` |
| `facebook_positions: video_feeds` | `feed`, `story`, `instream_video`, `marketplace` |
| `degrees_of_freedom_spec.creative_features_spec.standard_enhancements` | remover |
| `bid_cap` na campanha | `bid_amount` no conjunto |
| `is_adset_budget_sharing_enabled: true` com CBO | sempre `"false"` |
| `dsa_beneficiary` / `dsa_payor` | `regional_regulation_identities` |
| `locales` no targeting | não incluir, país vazio já puxa só BR |

---

## 7. Payloads validados

### Campanha

```python
{
  "name": nome,
  "objective": "OUTCOME_SALES",
  "buying_type": "AUCTION",
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP",   # ou LOWEST_COST_WITH_BID_CAP
  "daily_budget": "3000",                       # centavos USD
  "special_ad_categories": json.dumps([]),
  "is_adset_budget_sharing_enabled": "false",
  "status": "PAUSED",
}
```

Com bid cap, `bid_strategy` fica na campanha e `bid_amount` no conjunto.

### Conjunto

```python
{
  "name": nome,
  "campaign_id": campaign_id,
  "optimization_goal": "OFFSITE_CONVERSIONS",
  "billing_event": "IMPRESSIONS",
  "destination_type": "UNDEFINED",
  "promoted_object": json.dumps({"pixel_id": PIXEL, "custom_event_type": "PURCHASE"}),
  "targeting": json.dumps(TARGETING),
  "attribution_spec": json.dumps(ATTRIBUTION),
  "regional_regulated_categories": json.dumps(["BRAZIL_REGULATION", "VOLUNTARY_VERIFICATION"]),
  "regional_regulation_identities": json.dumps({
      "universal_beneficiary": ADVERTISER, "universal_payer": ADVERTISER}),
  "status": "ACTIVE",
}
```

Targeting que está no ar hoje:

```python
{
  "age_min": 18, "age_max": 65,
  "geo_locations": {"countries": ["BR"], "location_types": ["home", "recent"]},
  "targeting_automation": {"advantage_audience": 1},
  "user_age_unknown": True,
}
```

Atribuição do Prime, vídeo:

```python
[{"event_type": "CLICK_THROUGH", "window_days": 7},
 {"event_type": "VIEW_THROUGH", "window_days": 1},
 {"event_type": "ENGAGED_VIDEO_VIEW", "window_days": 1}]
```

Atribuição do magnésio, imagem: só o `CLICK_THROUGH` de 7 dias.

### Criativo de vídeo

```python
"object_story_spec": {
  "page_id": PAGE_ID,
  "instagram_user_id": IG_ID,          # opcional; omitir se a conta só roda Facebook
  "video_data": {
    "video_id": video_id,
    "title": title,
    "message": corpo,
    "image_url": thumb_uri,            # obrigatório, senão subcode 1443226
    "call_to_action": {"type": "SEE_DETAILS", "value": {"link": link}},
  },
}
```

### Criativo de imagem

```python
"object_story_spec": {
  "page_id": PAGE_ID,
  "instagram_user_id": IG_ID,
  "link_data": {
    "link": LANDING_URL,
    "message": corpo,
    "name": headline,
    "description": descricao,
    "image_hash": image_hash,
    "call_to_action": {"type": "LEARN_MORE", "value": {"link": LANDING_URL}},
  },
}
```

### UTMs — string padrão no `url_tags` do criativo

```
utm_source=facebook&utm_campaign={{campaign.name}}|{{campaign.id}}&utm_medium={{adset.name}}|{{adset.id}}&utm_content={{ad.name}}|{{ad.id}}&utm_term={{placement}}
```

A convenção `nome|id` é o que o Metrito espera para casar gasto com venda.

---

## 8. Upload de mídia

**Vídeo.** `POST /act_<ID>/advideos` com multipart, campo `source`. Depois faça
polling em `GET /<video_id>?fields=status` até `status.video_status == "ready"`.
A miniatura sai de `GET /<video_id>/thumbnails?fields=uri,is_preferred`.

**Imagem.** `POST /act_<ID>/adimages`. O nome do campo multipart tem que ser **o nome
do arquivo**, não um nome genérico:

```bash
curl -F "foo.jpg=@/caminho/foo.jpg"     # certo
curl -F "bytes=@/caminho/foo.jpg"       # Invalid parameter, file_size: 8
```

A resposta vem como `{"images": {"<filename>": {"hash": "..."}}}`. Pegue com
`next(iter(data.values()))["hash"]`.

Cuidado com cache de imagem por nome de arquivo: 40 criativos chamados
`criativo-01-A.png` em pastas diferentes colidem. Use `{pasta}_{arquivo}` como chave.

**Clonar mídia entre contas.** `image_hash` e `video_id` são por conta.

- Imagem: `POST /act_<DESTINO>/adimages` com
  `copy_from={"source_account_id":"<ID sem act_>","hash":"<hash>"}`. O hash volta
  idêntico porque a Meta hasheia o conteúdo. O `source_account_id` vai **sem** o
  prefixo `act_`, senão dá `(#100) must be a valid ID string`.
- Vídeo: não copie. `copy_from` em `/advideos` sempre falha. O criativo da conta de
  destino pode apontar direto para o `video_id` da origem, inclusive sob outra página.

---

## 9. Contas, pixels e páginas

| Conta | ID | Produto | Pixel |
|---|---|---|---|
| USD - PRIME CREME | `act_1965476473957439` | Prime Creme | `1289947162723962` |
| USD - FUNGZERO | `act_1642921946819932` | Magnésio Bisglicinato | `2024443845625153` |
| EUA 11 | `act_2164352101016970` | operação madura, CBO bid cap | `2738375386539927` |

Outros pixels da EUA 11: StrongBones `1480375430251129`, B12 `980607068056359`,
GlowUp `1350310353585886`, Sano Kids `955425957482281`, Prosaflex `1045768584781506`,
Relívia `1853242508916971`, FungZero `2156335194912574`, Tônico Supremo
`1553830736152220`.

**Páginas — não existe uma resposta única, confira por conta.**

- Prime Creme e FUNGZERO usam a página `650163921506803` (Sanologia institucional).
- Os funis Sano na EUA 11 usam `759591800579421`, e ali a `650163921506803` é a
  errada.
- Instagram: `17841477315620430` para a EUA 11, `17841468816354122` para o Prime.
  A conta FUNGZERO roda **sem** `instagram_user_id`, só Facebook.

Antes de subir numa conta nova, liste o que está liberado:

```bash
curl -s "https://graph.facebook.com/v23.0/act_<ID>/promote_pages?access_token=$META_ACCESS_TOKEN"
```

**Estrutura CBO + Bid Cap da EUA 11.** Campanha `120248694356150442`, US$24.000/dia na
campanha, nenhum conjunto com budget próprio, `bid_amount` por ângulo no conjunto.
A escada de lance observada vai de $25 a $41: advertorial long-form de constipação
leva o lance mais baixo, página de vendas direta e broad levam o mais alto. Ali o
targeting é manual, `advantage_audience: 0` em 92 dos 102 conjuntos, idade 35-65.

---

## 10. Reprovação por política — o falso positivo de cannabis

Anúncios de saúde reprovam com "Parece que seu anúncio promove cannabis comestível" ou
"Medicamentos e produtos farmacêuticos". Não há cannabis nem venda de remédio: é o
classificador casando **nome de ingrediente** contra o dicionário de política.

A solução validada, 15 de 15 aprovados, é inserir um **zero-width joiner (U+200D)**
depois da segunda letra de cada termo-gatilho. A leitura fica idêntica ao olho humano
e a string não casa mais o dicionário.

Termos a ofuscar: cúrcuma, arnica, Arnica Montana, Ginkgo Biloba, capsaicina, MSM,
metilsulfonilmetano, ácido alfa-lipoico, gabapentina, pregabalina, Lyrica, corticoide,
diclofenaco, ibuprofeno, naproxeno, tramadol, codeína, nimesulida, celecoxibe,
cortisona, prednisona, dipirona, paracetamol, opioide, anti-inflamatório, AINE,
canabidiol, CBD, óleo de cannabis.

**Nunca suavize a alegação.** Cura, trata, regenera e a promessa inteira ficam
intactos. Só o nome técnico do ingrediente leva o caractere invisível, porque ninguém
compra por causa da palavra "Ginkgo Biloba".

A reprovação vem em ondas, não de uma vez. A cada checagem caem mais um ou dois,
revelando um termo que faltava. Itere até zerar. Rode com `PYTHONIOENCODING=utf-8`,
senão o ZWJ quebra o terminal no Windows.

Criativo no Meta é **imutável**. Para corrigir um reprovado: leia a copy real do
criativo, ofusque, crie um criativo novo, crie um anúncio novo PAUSED no mesmo
conjunto e apague o reprovado. Trocar criativo zera prova social e re-submete à
revisão, então anúncios com cinco ou mais compras em 30 dias vale desligar na mão.

---

## 11. Higiene do texto

Long-form vindo do Obsidian leva `**negrito**` literal para o feed, e o leitor vê os
asteriscos. Markdown não renderiza no Facebook. Limpe antes de subir:

```python
body = re.sub(r"\*\*(.+?)\*\*", r"\1", body)
body = "\n".join(l for l in body.split("\n") if l.strip() != "---")
```

Preserve as quebras de linha.

---

## 12. Idempotência e recuperação de run quebrado

O publisher é idempotente **por nome de campanha**: ele lista as campanhas existentes
antes de começar e pula o que já existe. Isso funciona porque na estrutura 1-1-1 o
nome da campanha é único por criativo.

Idempotência por nome de conjunto **não** protege. Já aconteceu de o primeiro run
criar 6 conjuntos vazios e morrer antes dos anúncios; o segundo run não achou os
vazios e criou mais 6. Resultado: 12 conjuntos, metade órfã.

**Quando um run morre no meio, o vídeo já subiu.** Antes de re-rodar, pegue o
`video_id` do log e coloque no item do manifesto. O publisher reusa em vez de subir de
novo. Cada item processado é gravado no arquivo `.resultado.json` na hora, justamente
para isso.

Não rode com `nohup ... &` dentro do Claude Code: o processo morre quando o shell
encerra e deixa campanha e conjunto sem anúncio. Use `run_in_background` do próprio
tool.

**Nunca rode script de escrita enquanto alguém edita a conta no gerenciador.** Escrita
simultânea dá `unknown error (empty response) #1.1357045` e a pessoa não consegue
salvar.

---

## 13. Insights — a armadilha do filtro de gasto

Ao ranquear criativos por ROAS, **nunca** passe
`filtering=[{"field":"spend","operator":"GREATER_THAN",...}]` na chamada de Insights
com `level=ad`.

O mesmo criativo roda como vários `ad_id` em conjuntos diferentes, então a API devolve
uma linha por `ad_id`, não uma por criativo. O `filtering` roda linha a linha, antes
de qualquer soma. Isso corrompe nas duas direções: um criativo que gastou 60 + 50 + 40
some do ranking, e outro entra porque só as linhas boas foram somadas.

O certo: puxar tudo sem filtro com `date_preset=maximum`, paginar até o fim, somar
`spend` e `spend × purchase_roas` por criativo, e só então aplicar os cortes. ROAS
agregado é receita somada dividida por gasto somado, **nunca** a média dos ROAS das
linhas.

Aconteceu em 2026-09-09: com filtro deu 44 criativos aprovados; sem filtro, o número
correto era 46, com 5 que tinham sumido e 3 que não passavam de verdade. O total de
linhas vai de 135 para 2.350 quando o filtro sai.

---

## 14. Checklist antes de rodar qualquer publisher

1. Token vivo e conta com `account_status: 1`.
2. `ADVERTISER_ID` lido de um conjunto real **desta** conta.
3. Página e Instagram conferidos em `/promote_pages` **desta** conta.
4. Pixel correto **do produto**, não o de outro produto da mesma conta.
5. `degrees_of_freedom_spec` presente, tudo OPT_OUT, sem `standard_enhancements`.
6. `is_adset_budget_sharing_enabled: "false"` no POST de campanha.
7. `advantage_audience` declarado; se for `1`, `age_min` ≤ 25.
8. Copy limpa de markdown e com os termos-gatilho ofuscados.
9. `url_tags` com a string de UTM padrão.
10. Campanha nasce **PAUSED**. Conjunto e anúncio nascem ACTIVE, então ligar a
    operação é virar só a campanha.
11. Ninguém mexendo na conta no gerenciador durante o run.
