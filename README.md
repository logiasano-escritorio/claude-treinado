# claude-treinado

O ambiente Claude Code inteiro — skills, slash commands, agentes, configuração e
memória de trabalho. Um `git pull` mantém todas as máquinas iguais.

## Instalar

```bash
git clone https://github.com/logiasano-escritorio/claude-treinado.git
cd claude-treinado
python3 instalar.py
```

Reinicie o Claude Code. Pronto.

Ver o que faria sem escrever nada:

```bash
python3 instalar.py --dry
```

Instalar só uma parte: `--skills`, `--memoria` ou `--configs`.

## O que vai instalado

| Origem no repo | Destino | Conteúdo |
|---|---|---|
| `claude/skills/` | `~/.claude/skills/` | 14 skills |
| `claude/commands/` | `~/.claude/commands/` | 67 slash commands |
| `claude/agents/` | `~/.claude/agents/` | 163 agentes |
| `claude/memory/<projeto>/` | `~/.claude/projects/<projeto>/memory/` | 184 memórias, 7 projetos |
| `claude/CLAUDE.md` | `~/.claude/CLAUDE.md` | auto-routing de agentes |
| `claude/AGENTS_CATALOG.md` | `~/.claude/` | mapa tópico → agente |
| `claude/settings.json` | `~/.claude/` | hooks e permissões |
| `claude/mcp.json` | `~/.claude/` | servidores MCP |

### As 14 skills

`subir-campanha-meta` · `adaptar-longform` · `raspar-adlibrary` · `pipeline-nicho`
`criativos-manchete` · `gerar-avatares-ugc` · `meta-ads-analyzer` · `copy-anuncio`
`analisar-vsl` · `debriefing-longform` · `sano-pagina-v2` · `transcreveryt`
`graphify` · `roadmap`

**`/subir-campanha-meta`** é a que sobe anúncio de verdade na conta. Traz o
publisher genérico dirigido por manifesto (idempotente por nome de campanha),
o manifesto de exemplo com os 82 aprimoramentos automáticos em OPT_OUT, e
`REFERENCIA-API-META.md` — o catálogo de erros da Graph API com o fix validado
em produção, as contas, os pixels e os advertiser IDs. Quem for subir campanha
lê essa referência antes de escrever código.

Duas se encaixam e vale saber a ordem: **`/raspar-adlibrary`** raspa a Meta Ad
Library de um concorrente e produz as notas de benchmarking com `variacoes_ativas`
(quantas cópias do mesmo texto ele está rodando — o proxy de aposta).
**`/adaptar-longform`** consome essas notas e adapta a peça pro produto.

### Os slash commands

67 itens, incluindo os squads: `copy-master` (33 copywriters), `traffic-masters`,
`design-squad`, `brand-squad`, `hormozi-squad`, `storytelling`, `cybersecurity`,
`advisory-board`, além dos utilitários de `deploy/`, `dev/`, `test/`, `docs/`.

### A memória

Não é skill — é o histórico de trabalho. O que já deu errado, o que nunca fazer,
como cada API se comporta, quais IDs pertencem a quê. É o que faz o Claude "já
saber" em vez de descobrir de novo. O modelo é o mesmo em toda máquina; o que
muda é o contexto acumulado.

Amostra do projeto Sanologia:

- Meta reprova saúde como cannabis → ofuscar nome de erva com ZWJ (testado 15/15)
- NUNCA subir ad com `site_extensions` — derrubou margem de 45% p/ 15% em 158 ads
- Creative do Meta é imutável: pra corrigir, recriar idêntico e trocar
- Vídeo >90MB dá HTTP 413 em 0,2s (parece timeout, não é) → upload em partes
- Ao adaptar long-form: nunca reduzir caracteres, nunca mexer na promessa

## O que NÃO vem no repo

De propósito, pra não carregar 1,2 GB de lixo:

- `projects/` — 612 MB de transcrição de sessão (só as memórias vêm)
- `plugins/` — 574 MB, reinstala sozinho
- `file-history/`, `shell-snapshots/`, `cache/`, `sessions/`, logs
- `.credentials.json` e qualquer `.env`

Resultado: **18 MB** em vez de 1,2 GB, sem perder nada que importe.

## Segurança

**Sem credenciais.** Toda chave encontrada virou `<CHAVE-NO-.env-LOCAL>` — o texto
útil em volta fica (como testar uma chave, formato `AIzaSy` vs `AQ.`, reset do free
tier), o segredo não. As chaves de verdade seguem no `.env` de cada máquina.

Quando uma skill precisar de chave, ela para com uma mensagem dizendo qual é e
onde colocar. Exemplo, no Mac:

```bash
mkdir -p ~/Desktop/Sanologia
echo 'GEMINI_IMAGE_API_KEY=AIzaSy...' >> ~/Desktop/Sanologia/.env
```

Pra subir campanha no Meta, o token vai no ambiente (nunca no repo). Gere no
Graph API Explorer com permissão `ads_management`:

```bash
export META_ACCESS_TOKEN='EAAG...'
```

Token de usuário expira rápido, às vezes em 2-3 horas de trabalho pesado; o de
longa duração vence em torno de 60 dias. Quando der `code 190`, é isso.

Ainda assim, **mantenha o repo privado**: ele carrega IDs de conta Meta, pixels,
domínios monitorados e a estratégia do negócio.

## Não destrói nada

- Backup com timestamp antes de sobrescrever qualquer pasta ou arquivo
- Rodar duas vezes não duplica
- Skills, commands e agentes que só existem na máquina local **são preservados** —
  o repo adiciona e atualiza, não substitui a pasta inteira
- `MEMORY.md` é mesclado linha a linha: memória local nunca some
- `corpus-fb.txt`: se o local for maior que o do repo, o local fica

## Memória e nome de pasta

O Claude Code nomeia a pasta de memória pelo **caminho do projeto**, então o nome
muda entre Windows e Mac (`c--Users-user-Desktop-Sanologia` vira
`-Users-<voce>-Desktop-Sanologia`). O instalador detecta o equivalente local e
traduz. Projetos que não existem na máquina nova ficam com o nome original — a
memória entra e passa a valer quando você criar a pasta do projeto.

## Dependências

Só na hora de usar cada skill:

```bash
pip3 install DrissionPage                        # /raspar-adlibrary
pip3 install google-genai pillow python-dotenv   # skills que geram imagem
```

O `/raspar-adlibrary` abre um Chrome real (precisa ter Chrome) e leva 15-30 min
numa coleta grande.

## Atualizar

Quem mexer em algo commita aqui. Nas outras máquinas:

```bash
git pull && python3 instalar.py
```

Pra levar mudanças da sua máquina de volta pro repo, copie de `~/.claude/` para
`claude/` — conferindo que nenhuma chave entrou junto.
