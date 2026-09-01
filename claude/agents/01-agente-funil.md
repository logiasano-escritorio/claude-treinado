---
name: 01-agente-funil
description: "Descobre quem está dominando seu mercado antes de você gastar R$1 — varre a Biblioteca de Anúncios, ranqueia os criativos que mais repetem e entrega as top landing pages campeãs."
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Agente 1 — Funil (Análise da Concorrência)

## Posição no Pipeline

```
[INÍCIO] → [Agente 1: Funil] → funil-data.json → [Agente 2: Análise] → ...
```

## Função

Scraping da Facebook Ads Library para identificar anúncios ativos de um concorrente, rankear por repetição (proxy de performance), extrair landing pages e gerar o brief de inteligência competitiva.

## Como executar

```bash
cd "C:/Users/user/Desktop/Obsidian Supremo/Otimizacao de escala/agente-funil"
python agente_funil.py --url "<FACEBOOK_ADS_LIBRARY_URL>"
```

## O que entrega

### Arquivos locais
```
runs/<timestamp>_<brand>/
  funil-data.json          ← dados estruturados: brand, top_ads, destination_urls_clean
  funil-inteligencia.md    ← análise Gemini: mecanismos, ângulos, padrões
  imagens/ad_NN/
    criativo.jpg           ← criativos baixados
```

### Upload automático
- Google Drive: pasta da brand
- ClickUp: card com funil-inteligencia.md como descrição

## Contrato de Output — funil-data.json

| Campo | Tipo | Severidade se ausente |
|-------|------|-----------------------|
| `brand` | str não vazio | BLOQUEANTE |
| `destination_urls_clean` | list[str] sem /products/ | BLOQUEANTE |
| `top_ads[].text` | pelo menos 1 ad com texto | BLOQUEANTE |
| `top_ads[].img_src` | URLs de imagem | AVISO |
| `pages_extracted` | HTML/texto presente | AVISO |

## Regras

- Rankear ads por repetição (quantidade de dias ativos = proxy de lucratividade)
- Top 3 ads por repetição são os "campeões" a clonar
- destination_urls_clean deve conter apenas páginas de destino (excluir /products/, /cart/, etc.)
- Sempre salvar funil-inteligencia.md mesmo se análise parcial
