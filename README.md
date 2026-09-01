# claude-treinado

Skills do Claude Code + memória de trabalho do projeto Sanologia.
Um `git pull` mantém todas as máquinas iguais.

## Instalar

```bash
git clone https://github.com/logiasano-escritorio/claude-treinado.git
cd claude-treinado
python3 instalar.py
```

Reinicie o Claude Code. Pronto.

Ver o que ele faria sem escrever nada:

```bash
python3 instalar.py --dry
```

Instalar só uma parte: `--skills` ou `--memoria`.

## O que vai instalado

| O quê | Vai para | Conteúdo |
|---|---|---|
| `skills/` | `~/.claude/skills/<nome>/` | 2 skills |
| gatilhos | `~/.claude/CLAUDE.md` | as linhas que fazem `/comando` disparar |
| `memory/` | `~/.claude/projects/<projeto>/memory/` | 106 memórias do Sanologia |

### As skills

**`/raspar-adlibrary`** — raspa a Meta Ad Library pública de um concorrente
(sem token, sem login, via DrissionPage) e escreve no vault o índice + uma nota
por long-form único. O campo que importa é `variacoes_ativas`: quantas cópias do
mesmo texto estão rodando ao mesmo tempo — o proxy mais honesto de aposta do
concorrente.

**`/adaptar-longform`** — pega um long-form raspado e adapta pro produto:
briefing de 7 blocos, as 42 regras, português orgânico brasileiro, nota no
Obsidian com auditoria, e imagens stop-scroll extraídas das cenas do próprio texto.

**A ordem importa:** raspar produz o que adaptar consome.

### A memória

Não é uma skill — é o histórico de trabalho. O que já deu errado, o que nunca
fazer, como cada API se comporta, quais IDs pertencem a quê. É o que faz o Claude
"já saber" em vez de descobrir tudo de novo. O modelo é o mesmo em toda máquina;
o que muda é o contexto acumulado.

Amostra:

- Meta reprova saúde como cannabis → ofuscar nome de erva com ZWJ (testado 15/15)
- NUNCA subir ad com `site_extensions` — derrubou margem de 45% p/ 15% em 158 ads
- Creative do Meta é imutável: pra corrigir, recriar idêntico e trocar
- Vídeo >90MB dá HTTP 413 em 0,2s (parece timeout, não é) → upload em partes
- Ao adaptar long-form: nunca reduzir caracteres, nunca mexer na promessa

## Segurança

**Sem credenciais no repo.** As memórias que citavam chave entram com o valor
substituído por `<CHAVE-NO-.env-LOCAL>` — o texto útil fica (como testar uma
chave, formato `AIzaSy` vs `AQ.`, reset do free tier), o segredo não.

As chaves de verdade continuam no `.env` de cada máquina.

Ainda assim, **mantenha este repo privado**: ele carrega IDs de conta Meta,
pixels, domínios monitorados e a estratégia do negócio.

## Não destrói nada

- Backup com timestamp antes de sobrescrever qualquer coisa
- Rodar duas vezes não duplica
- `CLAUDE.md`: cada skill escreve seu bloco marcado; o que já existe é preservado
- `MEMORY.md`: mesclado linha a linha — memória local da máquina não some
- `corpus-fb.txt`: se o local for maior que o do repo, o local fica

## Dependências

Só na hora de usar cada uma:

```bash
pip3 install DrissionPage                        # /raspar-adlibrary
pip3 install google-genai pillow python-dotenv   # /adaptar-longform (só imagens)
```

O `/raspar-adlibrary` abre um Chrome real (precisa ter Chrome instalado) e leva
15-30 min numa coleta grande. A adaptação de copy roda sem instalar nada.

## Caminhos que as skills esperam

Ambas leem e escrevem no vault Obsidian `SANOLOGIA - REMOTO`, que elas detectam
sozinhas. Pra forçar: `SANO_VAULT=/caminho/do/vault`.

| Etapa | Precisa de |
|---|---|
| raspar → salva em | `Produtos/<Produto>/Benchmarking/<anunciante>/` |
| adaptar → lê de | o índice e as notas geradas acima |
| adaptar → português | `REGRAS-PORTUGUES-ORGANICO.md` na raiz do vault |
| adaptar → salva em | `Produtos/Magnésio/Adaptacoes prontas pra subir/Adaptacoes-Externas/` |

## Atualizar

Quem mexer numa skill commita aqui. Nas outras máquinas:

```bash
git pull && python3 instalar.py
```

Pra levar memória nova, copie os `.md` de
`~/.claude/projects/<projeto>/memory/` para `memory/` antes de commitar —
lembrando de tirar qualquer chave que tenha entrado.
