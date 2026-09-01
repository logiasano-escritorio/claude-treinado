---
name: DreamAPI (NewportAI) — Documentação Completa
description: Documentação completa da DreamAPI (api.newportai.com): lip sync, avatar, voz, storage, polling — todos os endpoints, parâmetros e exemplos curl para uso imediato
type: reference
originSessionId: 10ce698b-0e2a-4125-9df8-66bff1e16a08
---
# DreamAPI (NewportAI) — Documentação Completa

**Base URL:** `https://api.newportai.com`
**Autenticação:** `Authorization: Bearer {API_KEY}`
**API Key Relívia:** `<CHAVE-NO-.env-LOCAL>`
**Docs:** https://api.newportai.com/api-docs

---

## FLUXO GERAL (TODAS AS APIS ASYNC)

1. POST para o endpoint específico → recebe `taskId`
2. POST para `/api/getAsyncResult` com o `taskId` → poll até `status: 3` (sucesso)
3. Resultado fica disponível por **24 horas** e depois é deletado automaticamente

**Status codes do polling:**
- `1` = task submitted
- `2` = task in progress
- `3` = task completed ✅
- `4` = task failed ❌

---

## AVATAR

### 1. LipSync (v1)
**POST** `https://api.newportai.com/api/async/lipsync`
**Custo:** 1 crédito/segundo

Gera vídeo de avatar falante a partir de áudio + vídeo. Sincroniza expressões faciais e tom de voz.

**Request Body:**
```json
{
  "srcVideoUrl": "https://example.com/source.mp4",  // REQUIRED — URL do vídeo fonte
  "audioUrl": "https://example.com/audio.mp3",       // REQUIRED — URL do áudio original
  "vocalAudioUrl": "https://example.com/vocal.mp3",  // OPTIONAL — URL do áudio vocal separado
  "videoParams": {
    "video_width": 1920,     // REQUIRED — 0 = manter original
    "video_height": 1080,    // REQUIRED — 0 = manter original
    "video_enhance": 1,      // REQUIRED — 0=desabilitado, 1=habilitado (melhora clareza facial)
    "fps": "25"              // OPTIONAL — "25" padrão ou "original" (até 60fps; escala custo)
  }
}
```

**Response:**
```json
{ "code": 0, "message": "success", "data": { "taskId": "b08337dc08d7428daa64b3d5e61b8350" } }
```

**Polling result:**
```json
{
  "data": {
    "task": { "taskId": "...", "status": 3 },
    "videos": [{ "videoUrl": "https://...mp4", "videoType": "mp4" }]
  }
}
```

---

### 2. LipSync 2.0
**POST** `https://api.newportai.com/api/async/lipsync/2.0`
**Custo:** 2 créditos/segundo (maior qualidade e resolução)

Versão melhorada do LipSync — maior clareza e resolução de output.

**Request Body:** idêntico ao LipSync v1
```json
{
  "srcVideoUrl": "https://example.com/source.mp4",  // REQUIRED
  "audioUrl": "https://example.com/audio.mp3",       // REQUIRED
  "vocalAudioUrl": "...",                             // OPTIONAL
  "videoParams": {
    "video_width": 0,
    "video_height": 0,
    "video_enhance": 1,
    "fps": "25"
  }
}
```

**curl:**
```bash
curl -X POST 'https://api.newportai.com/api/async/lipsync/2.0' \
  -H "Authorization: Bearer <CHAVE-NO-.env-LOCAL>" \
  -H 'Content-Type: application/json' \
  -d '{
    "srcVideoUrl": "https://example.com/source.mp4",
    "audioUrl": "https://example.com/audio.mp3",
    "videoParams": { "video_width": 0, "video_height": 0, "video_enhance": 1 }
  }'
```

---

### 3. DreamAvatar 3.0 Fast
**POST** `https://api.newportai.com/api/async/dreamavatar/image_to_video/3.0fast`

Gera avatar falante a partir de **imagem + áudio** (não precisa de vídeo fonte). Mais flexível que LipSync.

**Request Body:**
```json
{
  "audio": "https://example.com/audio.mp3",   // REQUIRED — MP3, WAV ou MP4, máx 3 minutos
  "image": "https://example.com/face.jpg",    // REQUIRED — JPG, JPEG, PNG, WEBP ou GIF
  "prompt": "a woman speaking confidently",   // REQUIRED — guia a geração
  "resolution": "480p"                        // OPTIONAL — "480p" (padrão) ou "720p"
}
```

**curl:**
```bash
curl -X POST 'https://api.newportai.com/api/async/dreamavatar/image_to_video/3.0fast' \
  -H "Authorization: Bearer <CHAVE-NO-.env-LOCAL>" \
  -H 'Content-Type: application/json' \
  -d '{
    "audio": "https://example.com/audio.mp3",
    "image": "https://example.com/face.jpg",
    "prompt": "a woman speaking confidently to camera",
    "resolution": "720p"
  }'
```

---

### 4. Dreamact
**POST** `https://api.newportai.com/api/async/wan/dreamact/2.1`

Anima múltiplas imagens faciais para espelhar expressões, movimentos labiais e poses de cabeça de um **vídeo guia**. Reconstrói modelo facial e aplica sequência de movimentos.

**Request Body:**
```json
{
  "video": "https://example.com/driving.mp4",  // REQUIRED — MP4, máx 1 minuto
  "images": ["https://example.com/face.png"],  // REQUIRED — array de URLs (JPG, PNG, WEBP, GIF)
  "seed": 42                                    // OPTIONAL — para reprodutibilidade
}
```

---

## VOICE

### 5. Voice Clone
**POST** `https://api.newportai.com/api/async/voice_clone`

Clona voz de um áudio fonte. Retorna `cloneId` que pode ser reutilizado indefinidamente no TTS Clone.

**Request Body:**
```json
{ "voiceUrl": "https://example.com/voice.mp3" }  // REQUIRED — URL pública do áudio
```

**Polling result:**
```json
{ "cloneId": "fe82a0faf1444f93bd7f49a4ba745b63" }
```

---

## STORAGE (para hospedar arquivos de áudio/imagem/vídeo)

### 6. Get Upload Policy
**POST** `https://api.newportai.com/api/getUploadPolicy` (inferido)

Retorna policy, accessId, signature, dir e host para upload direto no OSS.

### 7. Upload
**POST** `https://dreamapi-oss.oss-cn-hongkong.aliyuncs.com`

Upload direto de arquivo para o OSS. Usa parâmetros da Policy.

**Request Body (multipart/form-data):**
```
success_action_status: "200"
policy: {policy_from_policy_api}
OSSAccessKeyId: {accessId}
signature: {signature}
key: {dir + filename}
callback: {callback}
file: {binary}  ← DEVE ser o ÚLTIMO campo
```

**curl:**
```bash
curl --location --request POST 'https://dreamapi-oss.oss-cn-hongkong.aliyuncs.com' \
  --form 'policy="..."' \
  --form 'OSSAccessKeyId="..."' \
  --form 'success_action_status="200"' \
  --form 'signature="..."' \
  --form 'key="tmp/dream/2024-11-19/unique/file.mp3"' \
  --form 'callback="..."' \
  --form 'file=@"/path/to/file.mp3"'
```

---

## POLLING (recuperar resultado de qualquer task)
**POST** `https://api.newportai.com/api/getAsyncResult`

**Request Body:**
```json
{ "taskId": "b08337dc08d7428daa64b3d5e61b8350" }
```

**Response completo:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "task": {
      "taskId": "...",
      "status": 3,         // 1=submitted 2=processing 3=success 4=failed
      "reason": "",        // motivo de falha se status=4
      "taskType": "lipsync",
      "executionTime": 17232,
      "expire": 1769586737611
    },
    "videos": [{ "videoUrl": "https://...mp4", "videoType": "mp4" }],
    "images": [{ "imageUrl": "https://...jpg", "imageType": "jpg" }],
    "audios": [{ "audioUrl": "https://...wav", "audioType": ".wav" }],
    "cloneId": "...",  // apenas de voice_clone
    "sceneId": "..."   // apenas de scene training
  }
}
```

**Erros comuns:**
- `13005` = key is blank
- `13006` = key is invalid
- `13007` = key prefix is wrong
- `10192` = illegal param

---

## ENDPOINTS ADICIONAIS (mapeados, doc não capturada)

| Categoria | Endpoint | Descrição |
|-----------|----------|-----------|
| Image Generator | Flux Text To Image | Gera imagem a partir de texto |
| Image Generator | Flux Image To Image | Transforma imagem com prompt |
| Image Editing | Colorize | Coloriza imagens |
| Image Editing | Enhance | Melhora qualidade |
| Image Editing | Outpainting | Expande imagem |
| Image Editing | Inpainting | Edita região da imagem |
| Image Editing | Swap Face | Troca rosto |
| Image Editing | Remove Background | Remove fundo |
| Video Generator | Text To Video (Wan2.1) | Vídeo a partir de texto |
| Video Generator | Image To Video (Wan2.1) | Vídeo a partir de imagem |
| Video Generator | Head Tail To Video (Wan2.1) | Vídeo com frames inicial/final |
| Video Editing | Swap Face For Video | Troca rosto em vídeo |
| Video Editing | Video Matting | Recorte de vídeo |
| Video Editing | Video Watermark Remover | Remove marca d'água |
| Video Translate | Video Translate 2.0 | Traduz vídeo |
| Voice | Do TTS Clone | TTS com voz clonada (requer cloneId) |
| Voice | Do TTS Common | TTS com voz padrão |
| Voice | Do TTS Pro | TTS avançado |
| Voice | Voice list | Lista vozes disponíveis |
| ByteDance | Seedance 2.0, 2.0 Fast, 1.5 Pro | Geração de vídeo ByteDance |
| ByteDance | Seedream 4.0, 4.5, 5.0 Lite | Geração de imagem ByteDance |
| User Dashboard | Available Credits | Consulta créditos disponíveis |

---

## FLUXO COMPLETO LIP SYNC PARA RELÍVIA

Para gerar vídeo de avatar da pesquisadora com os áudios do orégano:

**Opção A — LipSync (precisa de vídeo fonte):**
1. Upload do vídeo da locutora → obter URL pública
2. Upload do MP3 gerado pelo ElevenLabs → obter URL pública
3. POST `/api/async/lipsync/2.0` com srcVideoUrl + audioUrl
4. Poll `/api/getAsyncResult` até status=3
5. Download do videoUrl resultante

**Opção B — DreamAvatar 3.0 Fast (só precisa de foto):**
1. Upload de foto da locutora → obter URL pública
2. Upload do MP3 gerado pelo ElevenLabs → obter URL pública
3. POST `/api/async/dreamavatar/image_to_video/3.0fast` com image + audio + prompt
4. Poll `/api/getAsyncResult` até status=3
5. Download do videoUrl resultante

**Opção B é mais prática** — não precisa de vídeo real da locutora, só uma foto.
