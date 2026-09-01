---
name: reference-meta-upload-video-grande
description: Vídeo >90MB no Meta exige upload em partes (HTTP 413 no simples) e ad de vídeo exige miniatura (subcode 1443226)
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3253b5e5-0e32-4c52-bb7b-e19f244c3497
  modified: 2026-08-09T05:08:24.128Z
---

Duas armadilhas ao subir **ads de vídeo** via Meta Marketing API, descobertas na campanha Magnésio Sono (09/08/2026):

## 1. HTTP 413 — upload simples só vai até ~90 MB

`curl -F source=@arquivo.mp4` para `/advideos` devolve **HTTP 413 em 0,2 segundo** quando o arquivo passa de ~90 MB. Ele recusa *antes* de receber os bytes — `size_upload=0`.

**Sintoma enganoso:** o curl volta com `returncode 0` e stdout vazio, o que parece timeout. Aumentar `--max-time` não resolve nada. Diagnostique com `-w "HTTP_CODE=%{http_code}"`.

**Solução — upload em partes:**
```
upload_phase=start   + file_size=N   -> devolve upload_session_id, video_id, start/end_offset
upload_phase=transfer + upload_session_id + start_offset + video_file_chunk=@pedaco
                                      -> devolve o PRÓXIMO start/end_offset; repetir até start==end
upload_phase=finish  + upload_session_id
```
O `video_id` vem já no `start`. Um arquivo de 215 MB sobe em menos de 1 minuto.

## 2. Ad de vídeo exige miniatura

Criar adcreative com `video_data` sem miniatura falha:
`error_subcode 1443226 — "Seu anúncio precisa de uma miniatura"`.

**Solução:** o Meta gera thumbs sozinho durante o processamento. Buscar em
`GET /{video_id}/thumbnails?fields=uri,is_preferred`, pegar a `is_preferred`
(ou a primeira) e passar como `video_data.image_url`.

Esperar `video_status == "ready"` antes (via `GET /{video_id}?fields=status`) — as thumbs só existem depois do processamento.

Script de referência: `_dev/subir-magnesio-sono-videos.py`.

Relacionado: [[reference_publisher_cache_colisao_nome]], [[feedback_nunca_subir_ad_com_site_extensions]]
