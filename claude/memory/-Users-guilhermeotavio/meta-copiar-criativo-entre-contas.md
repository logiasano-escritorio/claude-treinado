---
name: meta-copiar-criativo-entre-contas
description: "Como clonar criativo de anuncio entre contas Meta sem baixar arquivo: copy_from para imagem, referencia direta ao video_id para video"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 56723616-4361-4caf-a6c2-752c9db7241e
  modified: 2026-09-02T20:27:05.601Z
---

Para clonar um anúncio entre duas contas de anúncio do Meta, **nunca é preciso
baixar o arquivo**. São duas rotas diferentes, uma para cada tipo de mídia.

## Imagem — `copy_from`

```
POST /act_<DESTINO>/adimages
  copy_from={"source_account_id":"<ID NUMERICO SEM act_>","hash":"<image_hash>"}
```

Testado em 2026-09-02 entre `act_2164352101016970` (EUA 11) e
`act_1642921946819932` (FUNGZERO): a resposta trouxe o **hash idêntico** ao da
origem e as mesmas dimensões (848×1264). Hash igual = bytes iguais, prova de que
não houve recompressão.

**Pegadinha:** `source_account_id` vai **sem** o prefixo `act_`. Com `act_`
retorna `(#100) Param copy_from[source_account_id] must be a valid ID string`.

## Vídeo — referenciar o `video_id`, não copiar

**O vídeo não precisa existir na conta de destino.** O creative aponta direto
para o `video_id` da conta de origem, e o Meta aceita — inclusive publicando sob
uma **página diferente** da do post original:

```
POST /act_<DESTINO>/adcreatives
  object_story_spec = {"page_id": "<pagina liberada no destino>",
                       "video_data": {"video_id": "<id da conta de origem>",
                                      "image_url": "<GET /{video_id}/thumbnails>",
                                      "message": "...",
                                      "call_to_action": {...}}}
```

A miniatura é obrigatória (sem ela, subcode 1443226) e sai de
`GET /{video_id}/thumbnails?fields=uri,is_preferred`.

**Why:** as duas alternativas óbvias não funcionam, e descobrir isso custa
tempo. `copy_from` em `/advideos` falha sempre — 9 tentativas em 3 vídeos deram
`code 390 / subcode 1363030` com a mensagem enganosa "Tempo de carregamento de
vídeo esgotado"; a falha volta em 0-1 segundo, não é timeout de rede, e
repetir não adianta. E baixar não é opção porque
`GET /{video_id}?fields=source` devolve o campo vazio para este app. A saída é
não mover o arquivo.

**How to apply:** ao clonar entre contas, imagem via `copy_from`, vídeo via
referência ao `video_id`. Nunca baixar. Se a página do anúncio original não
estiver liberada no destino (`GET /act_X/promote_pages`), as duas rotas
permitem publicar sob outra página — então falta de página **não** é bloqueio.
A exceção é `object_story_id`, que reaproveita o post inteiro e preserva a
prova social, mas fica amarrado à página e ao link originais — usar só quando a
prova social valer mais que controlar o destino.

Ver [[utm-padrao-meta-ads]] e [[feedback_nunca_subir_ad_com_site_extensions]]
para o que o creative novo precisa levar.
