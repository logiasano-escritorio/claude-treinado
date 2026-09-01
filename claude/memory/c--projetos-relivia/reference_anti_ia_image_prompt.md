---
name: Técnicas Anti-IA para Geração de REF-A (avatar humano)
description: Receita testada de prompt para gerar fotos de avatar UGC que não parecem feitas por IA — iPhone 7 casual, color temp mismatch, JPEG artifacts, vincos anatômicos, bokeh hexagonal de smartphone.
type: reference
originSessionId: 7ddb77bf-0848-4bb2-aaf6-8086d30e2380
---
# Técnicas Anti-IA para REF-A — Avatar Humano

## Filosofia
Foto que não parece IA = foto com IMPERFEIÇÃO REALISTA, não foto bonita. Modelo default sempre tende a polish comercial. Cada técnica abaixo é uma instrução explícita anti-polish.

## 10 técnicas obrigatórias (cada uma faz diferença)

### 1. Câmera "iPhone 7 front camera, f/2.2"
Especificar geração de iPhone real força o modelo a replicar degradação característica daquele sensor. iPhone 7 = sweet spot — boa o suficiente pra ser crível, ruim o suficiente pra não parecer DSLR.

### 2. Tilt 2-3 graus + descentramento
Composição perfeita centrada = IA. Tilt sutil + sujeito off-center = humano segurando phone.

### 3. JPEG compression artifacts em high-contrast edges
"Subtle JPEG compression artifacts at edges where white coat meets background" — degradação digital crível, não estilizada.

### 4. Luminance grain de sensor (NÃO film grain)
Distinção crítica: film grain é estética reconhecida que IA sabe gerar. Luminance noise de smartphone é diferente — irregular, sem padrão romântico.

### 5. Color temperature mismatch (5500K + 3200K)
Especificar duas temperaturas Kelvin incompatíveis no mesmo prompt cria desequilíbrio cromático típico de ambientes reais — IA homogeneíza por default.

### 6. Imperfeições anatômicas POSICIONADAS
Não dizer "cabelo bagunçado". Dizer "3-4 fios soltos no templo esquerdo, 1 fio cruzando a fronte". Sardas? "2-3 sardas assimétricas no nariz". Especificidade força distribuição irregular.

### 7. Vincos de roupa em locais físicos específicos
"Jaleco com vinco horizontal mid-chest (de sentar) + vinco no punho direito (de dobrar braço)". Isso é física real de tecido — IA tende a gerar tecido perfeito ou amassado generic.

### 8. Bokeh hexagonal de smartphone (NÃO circular DSLR)
"f/1.8 with realistic smartphone computational bokeh — slightly hexagonal noisy pattern, NOT creamy circular". Padrão de bokeh é assinatura técnica.

### 9. Setting com bagunça realista
Planta meio seca com folhas amarelando, lousa com ghost marks de escrita apagada, caneca com aro de café no exterior, mancha de caneta no quadril direito do jaleco. Detalhes de uso real.

### 10. Negative prompt agressivo
Bloquear: studio lighting, ring light, beauty dish, portrait mode bokeh, skin retouching, symmetrical face, editorial composition, magazine lighting, color grading, LUT, Instagram filter, AI glamour photography.

## Estrutura de prompt em 10 blocos
1. SHOT TYPE & DEVICE (iPhone 7 explícito)
2. SUBJECT (com imperfeições posicionadas)
3. WARDROBE (vincos físicos)
4. SETTING (bagunça realista)
5. LIGHTING (color temp mismatch)
6. CAMERA SPECS (f-stop + JPEG + grain)
7. ANTI-AI INSTRUCTIONS (lista negativa estrutural)
8. ASPECT RATIO (9:16 para Veo 3)
9. STYLE DIRECTIVE ("from a researcher's WhatsApp camera roll")
10. NEGATIVE PROMPT

## Modelos por ranking (para esse tipo de prompt)
1. **GPT-4o Image** — melhor para naturalidade skin/lighting, respeita anti-IA
2. **Imagen 3** (Google AI Studio / Vertex) — melhor para etnia parda/morena brasileira
3. **Gemini 2.5 Flash Image (Nano Banana)** — mais rápido, prompts simplificados (150-200 palavras)
4. **Midjourney v7** — EVITAR, polish comercial conflita com pegada camera roll

## Iteração se ficar "muito IA"
- Pele perfeita → adicionar "open pores at nose tip, slight T-zone shine, one off-center blemish"
- Jaleco engomado → "fabric shows contact shadows, horizontal fold at elbow, slight bagging at lower back"
- Cabelo estilizado → "individual hairs at different frizz levels, NOT uniform wave"
- Setting set-de-foto → "dust on top of books, scuff marks at chair height, electrical outlet with white cable"
- Expressão posada → "micro-expression mid-thought, lips slightly parted, eyebrow asymmetry 2-3mm"

## Variação direcionada (manter identidade, ajustar detalhe)
```
Keep this image exactly as generated — same person, same face, same hair,
same lighting, same composition — and make ONLY these changes: [item].
Do not alter any other element. Treat this as a targeted edit.
```

## Origem
Sessão de produção REF-A para criativos Relívia Orégano + Nigela (2026-04-28). Prompts master completos para 3 avatares (séria/amigável/vivida) documentados em `Relivia Context/Playbooks/PIPELINE-CRIATIVO-UGC-SUPLEMENTO.md`.
