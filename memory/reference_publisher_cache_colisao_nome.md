---
name: reference_publisher_cache_colisao_nome
description: Bug do publisher Meta — cache de image_hash por nome de arquivo colide entre bancos diferentes
metadata: 
  node_type: memory
  type: reference
  originSessionId: 77ffe71b-c21b-4cb4-9a58-1bbcf8ae4fa8
---

Ao subir ads de MÚLTIPLOS bancos de imagem que têm arquivos com o MESMO nome (ex: banco masc e banco fem ambos com `criativo-06-A.jpg`), o cache de upload por `fp.name` faz o 2º banco reusar o hash do 1º — resultando em **imagem do gênero errado** no ad.

**Fix:** cachear por caminho ABSOLUTO (`str(fp.resolve())`), não por nome. E no `/adimages` usar `name` único por banco (incluir a pasta: `gaba16_<pastapai>_<arquivo>`) pra o Meta não deduplicar. Caso real: 7 adsets femininos Gabapentina pegaram criativos masculinos (o "farmacêutico" senhor no funil da mulher).

**Como flagrar antes de ativar:** depois de subir, BAIXAR a image_url real de 1 ad de cada adset e LER (não confiar no manifesto/hash) — comparar com [[feedback_criativo_nao_pode_mentir_destino]]. Validar via ad com sufixo conhecido (ex: `_06`) comparando o image_hash contra o hash esperado do banco certo.

**Rate limit Meta (code 17 "user request limit"):** subir 160 ads em rajada estoura a conta inteira (~1h bloqueado). Mitigar: (1) pré-upload das imagens UMA vez e reusar hashes; (2) criar 1 adset por vez com `time.sleep(20)` entre eles; (3) chamadas esparsas passam mesmo "em rate limit" — é rajada que trava. DELETE precisa do access_token na QUERY STRING (não no body). Ver [[feedback_manifesto_antes_de_subir]].
