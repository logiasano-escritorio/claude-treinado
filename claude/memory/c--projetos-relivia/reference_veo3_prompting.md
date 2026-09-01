---
name: Veo 3 Prompting Guide
description: Guia completo de prompting para geração de vídeos de anúncios no Google Veo 3 — fórmulas, técnicas, specs, erros comuns, templates para UGC e produto
type: reference
originSessionId: 291e993e-d42b-4f49-8d47-4bb208b9b2b3
---
# Veo 3 — Guia de Prompting para Anúncios

## Fórmula Base (Google DeepMind oficial)

```
[Cinematografia] + [Sujeito] + [Ação] + [Contexto/Ambiente] + [Estilo & Mood] + [Áudio]
```

## Elementos Obrigatórios

| Elemento | Exemplo |
|---|---|
| Shot type | `Close-up`, `Medium shot`, `Wide shot` |
| Camera movement | `Slow dolly in`, `Tracking shot`, `Handheld`, `Static` |
| Subject | Descrição física detalhada |
| Action | Exatamente o que faz |
| Setting | Onde + detalhes sensoriais |
| Lighting | `Warm golden hour light`, `Soft studio key light` |
| Style | `Cinematic`, `UGC authentic`, `Commercial health brand` |
| Audio | SFX, fala entre aspas, ambiente |

## Specs Técnicas

- Duração por clipe: 4s, 6s ou 8s
- Resolução: 720p ou 1080p
- Aspect Ratio: 16:9 ou 9:16
- Áudio: nativo — diálogo sincronizado, SFX, ambiente
- Acesso: Vertex AI (API) + Google AI Studio + Flow

## Técnicas Principais

### UGC Autêntico
```
A selfie video of a [descrição física], holding the bottle of [produto] 
up to the camera with genuine excitement, casual [ambiente] setting, 
ring light slightly visible, authentic handheld camera movement, 
natural eye movement, UGC style, no professional lighting.
She says: "[fala natural e curta]"
(no subtitles)
```

### Timestamp Prompting (sequência 8s)
```
[00:00-00:02] [plano + sujeito + problema]
[00:02-00:05] [transição + produto]
[00:05-00:07] [ação + resultado]
[00:07-00:08] [payoff emocional]
```

### Áudio
- Fala: `A woman says, "frase aqui"`
- SFX: `SFX: soft capsule clicking on a glass counter`
- Ambiente: `Ambient noise: quiet morning kitchen, faint birds outside`
- Sem legendas: `(no subtitles!)`
- Máximo 8s de fala por clipe
- Identifique quem fala: `The woman in blue says:`

## Movimentos de Câmera para Ads

| Movimento | Uso |
|---|---|
| `Slow dolly in` | Revelar emoção — testemunhal |
| `Tracking shot` | Lifestyle, produto em movimento |
| `Handheld subtle` | UGC autêntico |
| `Static medium shot` | Entrevista, expert |
| `360 rotation` | Produto premium |
| `Extreme close-up pan` | Detalhes produto |
| `POV shot` | Imersão |

## Erros Fatais

1. Prompt genérico — descreva o que "cinematic" significa naquele plano
2. Muita coisa num clip — uma ideia, um movimento, um momento
3. Sem especificar câmera — modelo escolhe errado para ads
4. Diálogo longo — máximo 1-2 frases diretas
5. Esquecer áudio — Veo 3 gera algo aleatório se não especificado
6. Prompt idêntico — resultados similares; mude variáveis específicas

## Consistência de Produto em Image-to-Video (problema crítico)

### O problema: "Latent Drift"
O Veo 3 não "fotografa" o objeto da imagem — ele interpreta e reconstrói frame a frame.
Quando mãos interagem com o produto, ele recria o objeto e deriva (pote muda de tamanho, rótulo distorce).
**Textos em rótulos sempre vão distorcer — limitação conhecida e sem solução no Veo 3.**

### Solução principal: Ingredients to Video (Veo 3.1)
Manda 3 imagens separadas em vez de 1:
- Imagem 1: foto da pessoa sozinha
- Imagem 2: foto do pote isolado em fundo limpo
- Imagem 3: foto da pessoa COM o pote

O modelo ancora cada elemento separadamente e mantém os dois consistentes.
**Onde usar:** Google Flow, Vertex AI, Gemini app, Google Vids.

### Técnicas complementares
- **Motion-lock hack:** foto inicial e final com ~60% do mesmo fundo — força o modelo a focar no movimento, não em reconstruir o ambiente
- **Foto do produto isolado** em fundo limpo como referência adicional = "verdade" do objeto para o modelo
- **Ângulo estratégico:** filmar de forma que o rótulo apareça parcialmente escondido pelas mãos — evita dependência de texto legível
- **Prompt de âncora explícita:**
```
Do not modify the product jar. Keep the exact blue supplement jar 
with white cap from the reference image — same proportions, same label color, 
same size relative to her hand.
```

### Para image-to-video com produto: prompt minimalista
No image-to-video NÃO descreva a pessoa nem o produto — só instrua o movimento.
Descrever de novo faz o modelo "re-imaginar" elementos.

```
Animate this photo exactly as shown.
Keep the exact [cor] supplement jar from the reference image — 
same size, same label, same proportions.
She reaches into the open jar, picks out a single gummy, 
brings it to her mouth and chews slowly with a relaxed expression.
Camera: static medium shot, no zoom, slight handheld breathing.
Lighting: keep existing natural light from the photo.
SFX: soft ambient, gentle chewing sound.
(no subtitles)(no text overlays)
```

## Workflow para Escala

```
Script do anúncio (Claude)
        ↓
Breakdown por cenas (timestamp prompting)
        ↓
Geração de cada clipe 8s (Veo 3 via Vertex AI API)
        ↓
Montagem + caption
        ↓
Upload Instagram/Meta
```

## Fontes

- https://deepmind.google/models/veo/prompt-guide/
- https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- https://replicate.com/blog/using-and-prompting-veo-3
