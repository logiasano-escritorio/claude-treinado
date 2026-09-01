---
name: adaptar-longform
description: Pipeline completo de adaptação de long-form de concorrente estrangeiro para produto Sano. Seleciona uma peça do benchmarking raspado (Meta Ad Library), adapta a copy mantendo o esqueleto vencedor mas trocando mecanismo/marca/mercado, aplica as 42 regras e o português orgânico brasileiro, salva como AD-NN no Obsidian com auditoria completa, gera imagens stop-scroll calibradas pelo avatar e monta o inventário com ranking de aposta. Trigger /adaptar-longform
---

# /adaptar-longform

Pipeline de 6 etapas que transforma um long-form de concorrente estrangeiro num criativo Sano pronto pra subir — copy + imagens + nota no Obsidian.

**Este fluxo foi validado na AD-25** (peça de 23 variações da SPNutrition). Use aquela nota como referência de output esperado: `Produtos/Magnésio/Adaptacoes prontas pra subir/Adaptacoes-Externas/AD-25-endocrinologista-nao-explicou.md`

---

## QUANDO USAR

- User digitou `/adaptar-longform`
- User pediu "adapta essa peça do concorrente", "pega esse long-form e adapta"
- User apontou um arquivo do benchmarking e pediu adaptação

## INPUT

**Obrigatório:** qual peça adaptar. Pode vir como:
- Número/nome do arquivo em `LF1SP/` (ex: "a 107", "a de 23 cópias")
- Caminho de arquivo
- Texto colado direto

**Se o user não especificou**, mostre o top 10 por `variacoes_ativas` do índice `LF1SP.md` e pergunte qual.

**Perguntar ANTES de escrever** (em bloco único, o user responde tudo de uma vez):

1. **Eixo/nicho** — qual dos eixos Sano usar. Se o eixo do original não existe no briefing, dizer isso e propor o mais próximo
2. **Destino** — PV direta ou ponte pro advertorial
3. **Gerar imagens?** — sim/não, e quantas variações por cena

Não invente essas respostas. Mas **não trave o trabalho**: se o user já respondeu no pedido inicial, siga.

---

## ⚠️ REGRA DE OURO DESTE PIPELINE

**O user decide o escopo. Você executa e registra as ressalvas UMA vez.**

Se identificar risco (compliance, alegação, eixo sem lastro), diga em 1-2 frases, registre na nota como `> [!warning]`, e **execute o que foi pedido**. Nunca:
- Remover elemento que o user mandou manter (ex: números de exame)
- Repetir a ressalva depois que o user já decidiu
- Citar de volta como argumento algo que você mesmo levantou antes

O histórico da AD-25 tem esse erro cometido e corrigido. Não repita.

---

# ETAPA 1 — SELECIONAR A PEÇA

Fonte: `Produtos/Magnésio/Benchmarking/<concorrente>/LF1SP.md` (índice) e `LF1SP/` (as notas).

**Critério de prioridade — `variacoes_ativas`:** quantas cópias do mesmo texto estão rodando ao mesmo tempo na Ad Library. É o proxy mais honesto de aposta do concorrente. Se ele replicou 23 vezes, está pagando a conta.

Ordem de leitura:
1. `variacoes_ativas` alto = aposta grande
2. `caracteres` — long-form de 10k+ tem estrutura completa pra reaproveitar
3. `tema` — casa com algum dos 6 eixos validados?

Leia a peça inteira antes de decidir qualquer coisa.

---

# ETAPA 2 — ADAPTAR A COPY

## 2.1 — DESMONTAR A PEÇA (briefing de 7 blocos)

Você não está lendo pra entender. Está fazendo **engenharia reversa de uma máquina que já está paga**.

Preencha os 7 blocos **por escrito, antes de adaptar uma linha**. Cole o preenchimento na nota, seção "Engenharia reversa do original".

---

### ⚠️ COMO USAR ESTES BLOCOS

Isto é **briefing de leitura, não auditoria de qualidade**.

O objetivo é você entender a máquina antes de trocar as peças. Nada aqui é lista de melhoria.

**Se um bloco não tem resposta no original, a resposta é `não usa`.** Ponto. Escreva `não usa` e siga.

`não usa` **não é buraco. Não é pendência. Não é convite pra você preencher.**

Uma peça com 23 variações rodando já provou que vende **sem** aquilo. Se o original não tem prova social, você não vai inventar prova social. Se não tem escassez, não cria escassez. Se não tem uma terceira voz dizendo o benefício, você não adiciona uma. O que o campeão não faz é tão parte do campeão quanto o que ele faz — muitas vezes é justamente a ausência que faz a peça soar honesta.

**Você só troca o que a lista da 2.2 manda trocar** — marca, dose, mecanismo, unidades, mercado, cabeçalhos, destino. Todo o resto é modelagem: mesma arquitetura, conteúdo novo.

As regras N (N1, N13, N16, N23-N26, N40...) aparecem aqui só como **legenda de leitura** — pra você saber o nome do que está vendo. Elas valem como filtro no que você **escrever**, na auditoria da Etapa 3. Elas não são régua pra reprovar o original.

> Se depois de tudo pronto o user pedir "agora melhora essa peça", aí sim os `não usa` viram pauta. Enquanto ele pediu **adaptar**, eles são só descrição.

---

### BLOCO 1 — A CRENÇA FALSA (o parafuso mestre)

*Framework: 16-Word Sales Letter (Evaldo Albuquerque)*

Não é o problema. É a **crença sobre o problema** que a peça ataca.

Escreva a peça inteira numa frase, neste molde:

> "[Resultado desejado] não é sobre [crença falsa que ela tem hoje]. É sobre [nova crença = o mecanismo]."

Exemplo AD-25: *"Emagrecer depois dos 50 não é sobre comer menos e se mexer mais. É sobre destravar o magnésio que está preso dentro da célula."*

Anote também:
- **A crença falsa é a que o mercado inteiro repete, ou é específica desse nicho?** (só descrição — muda o alcance da adaptação, não a qualidade da peça)
- **A frase sobrevive sem o nome da marca?** Se sim, o mecanismo é transplantável direto. Se não, a peça amarra mecanismo e marca e você vai precisar de mais cuidado na troca (N25)

Se você não consegue escrever essa frase depois de ler a peça inteira, **leia de novo** — não é que a peça não tenha eixo, é que você ainda não achou. Uma peça replicada 23 vezes tem eixo.

---

### BLOCO 2 — NÍVEL DE CONSCIÊNCIA E TIPO DE LEAD

*Framework: Schwartz (Breakthrough Advertising) + CopyTHINKING (Ry Schwartz)*

Onde está a leitora **no primeiro parágrafo do original**:

| Nível | Ela sabe | Lead típico |
|---|---|---|
| Inconsciente | nada do problema | História pura, sem promessa |
| Consciente do problema | sente o sintoma, não sabe a causa | Agitação + nomear a causa oculta |
| Consciente da solução | sabe que existe categoria | Mecanismo único diferencia |
| Consciente do produto | conhece as marcas | Prova + oferta |
| Mais consciente | só falta preço | Oferta direta |

Anote:
- **Nível de entrada do original:** ___
- **Nível de saída (onde ela está no CTA):** ___
- **Quantos níveis a peça atravessa:** ___

**Por que isso importa na adaptação:** esse trajeto é a razão da peça ser longa. Sua adaptação tem que atravessar **os mesmos níveis, na mesma ordem** — é literalmente o esqueleto. Se o original vai de "problema" a "produto" em 12k caracteres, a sua também vai.

**Único ponto de atenção real:** o avatar Sano entra no **mesmo nível** do avatar do original? Se o público Sano já é consciente da solução (já toma magnésio) e o original abre em consciente do problema, o lead precisa entrar mais adiante no trajeto. Isso não é melhorar a peça — é encaixar o mesmo trajeto num público que já andou o primeiro trecho. Registre a decisão na nota.

---

### BLOCO 3 — O MECANISMO (do problema E da solução)

*Framework: RMBC (Stefan Georgi) + E5 (Todd Brown)*

Um long-form desses costuma ter **dois mecanismos que são o mesmo mecanismo virado do avesso** (N17).

| | Original | Adaptação Sano |
|---|---|---|
| Mecanismo do PROBLEMA (por que ela falha hoje) | | cálcio contrai |
| Mecanismo da SOLUÇÃO (por que isso resolve) | | magnésio solta |
| Nome próprio do mecanismo (se tiver) | | |
| Quantos atores fisiológicos (N16) | | 2 |

Esta é a troca central do pipeline. Descreva como o original faz cada coisa — porque a adaptação vai fazer **igual, com as peças Sano**:

1. **Qual é o defeito do tratamento atual que PIORA a causa?** É o que transforma "não funcionou" em "funcionou contra você". Como o original constrói isso?
2. **Como o mecanismo sustenta a velocidade prometida?** (N18) Qual prazo o original promete e como ele justifica
3. **O mecanismo explica por que ela falhou antes?** Se sim, em que trecho
4. **Quantos traços pra desenhar?** Se o original resolve em 2, a adaptação resolve em 2. Se ele usa 4 etapas, **não simplifique** — ele está pagando por 4
5. **Em que voz o mecanismo é entregue?** Diálogo com interrupção do leigo, monólogo da autoridade, narração? Reproduza a mesma forma (N3)

---

### BLOCO 4 — O ELENCO (quem fala o quê, e por quê)

*Framework: Epiphany Bridge (Brunson) + regras N1/N23-N26 como legenda*

Preencha só a coluna do original. A adaptação repete a estrutura com nomes, cidades e contexto brasileiros — não com papéis novos.

| Papel | O que anotar | Original |
|---|---|---|
| Narrador | idade, gênero, cidade, situação, profissão (ou ausência dela — N1) | |
| A parede | qual muro ele/ela bate antes de tudo começar | |
| Autoridade | quem é, como é identificada, que credencial aparece (N23) | |
| O encontro | como narrador e autoridade se cruzam (N24) | |
| A pergunta | a pergunta da autoridade cuja resposta obrigatória é "não" | |
| O vilão | é o sistema/currículo ou uma pessoa? (N6) | |
| Terceira voz | alguém diz o benefício emocional? Quem, e em que forma (N40) | |
| Custo do narrador | ele/ela paga algum preço na história? Qual (N29, N39) | |

**Se o original não tem terceira voz, escreva `não usa`.** A adaptação também não terá. Mesma coisa pro custo do narrador, pro vilão nomeado, pra qualquer linha.

Anote também se **narrador e autoridade são a mesma pessoa** (N26). Não pra reprovar — pra você reproduzir a mesma configuração.

---

### BLOCO 5 — A JORNADA DE CRENÇA

*Framework: Epiphany Bridge (Russell Brunson)*

Mapeie os movimentos **que existem** no original. Marque `não usa` nos que não existem:

1. **Backstory** — o mundo dela antes, as crenças que tinha
2. **Jornada externa** — o que tentou, na ordem, e o que cada tentativa custou
3. **Jornada interna** — o instante em que a crença velha quebrou
4. **Conquista** — o que virou possível, em termos concretos
5. **Ponte pra oferta** — como o produto entra como veículo da mesma virada

**O movimento 3 merece atenção especial** — é o que mais se perde na tradução, porque costuma estar num detalhe pequeno e não numa frase grandiloquente. Marque **em que parágrafo do original a crença quebra** e como ele carimba o momento (relógio, lugar, gesto — N30). Reproduza esse carimbo com a mesma precisão.

---

### BLOCO 6 — ARQUITETURA DE PROVA E OBJEÇÕES

*Frameworks: Accusation Audit (Chris Voss) + Bencivenga, como grade de leitura*

**6a. O que a peça responde, e onde.** Percorra as objeções típicas do nicho e marque **onde o original as trata** — ou `não trata`:

1. "Isso é só mais um suplemento" → ___
2. "Se funcionasse meu médico teria falado" → ___
3. "Já tomei magnésio e não senti nada" → ___
4. "Isso é propaganda disfarçada" → ___
5. "É caro / não vou manter" → ___

`não trata` é dado, não tarefa. Uma peça campeã frequentemente ignora objeções de propósito — responder tudo soa defensivo e alonga sem converter. Sua adaptação ignora as mesmas.

**6b. Como o original prova.** Marque as técnicas que ele usa (N13 — normalmente sem citar estudo, revista ou CRM):

- [ ] Especificidade numérica ("81kg", "23h40") — número exato lê como verdade
- [ ] Detalhe sensorial irrelevante pra venda — o que só quem viveu saberia
- [ ] Concessão contra o próprio interesse ("demorou 3 meses, quase desisti")
- [ ] Terceiro que não ganha nada dizendo aquilo
- [ ] Custo pago pelo narrador
- [ ] Contraindicação dita em voz alta
- [ ] Cita fonte/estudo/instituição nominalmente

A última linha importa: **se o original cita estudo e a regra Sano proíbe (N13)**, essa é uma troca obrigatória — substitua por outra técnica da mesma lista, mantendo a função de prova naquele ponto do texto. É troca, não acréscimo.

**6c. Enxertos obrigatórios do briefing Sano.** Estes entram mesmo que o original não tenha equivalente — são exigência de produto/compliance, não melhoria de copy. Sempre **dentro da cena, na fala da autoridade, sem bullets**:

- Omeprazol / interação medicamentosa
- Contraindicação renal em 8 palavras
- "Menos de 1% do magnésio circula no sangue" — a dívida do intracelular

Se o original já resolve algum desses em cena, use a cena dele. Não empilhe os dois.

---

### BLOCO 7 — CAMADA PSICOLÓGICA

*Frameworks: One Sentence Persuasion (Blair Warren) + Cialdini + Voss, como grade de leitura*

Serve pra você **reconhecer e reproduzir** os movimentos do original, não pra completá-los.

**7a. Blair Warren — os 5 gatilhos.** Marque onde cada um acontece, ou `não usa`:

| Gatilho | Onde no original |
|---|---|
| Encoraja o sonho dela | |
| Justifica os fracassos (não é culpa dela — o método falhou) | |
| Acalma o medo específico | |
| Confirma a suspeita ("você sempre soube que tinha algo errado") | |
| Joga pedra no inimigo (o sistema, o currículo — N6) | |

**7b. Cialdini — o que a peça de fato usa:**
- Prova social — e de gente parecida com ela?
- Autoridade — mora no personagem ou em logotipo/credencial?
- Unidade — existe um "nós"?
- Escassez — existe? É real?
- Reciprocidade — a peça entrega algo antes de pedir?

Três `não usa` seguidos aqui é normal. Peça de saúde 45+ frequentemente vende com **um** gatilho bem executado.

**7c. Voss — o momento "é isso mesmo":**

Qual é a frase do original onde a leitora pensa *"é exatamente isso"*? Transcreva-a literalmente.

**É a frase mais importante da peça inteira.** Traduza-a por último, com mais cuidado que todas as outras, e sem decalque. Se você só acertar uma frase na adaptação, que seja essa.

---

### FECHAMENTO — O QUE VOCÊ ENTENDEU DA MÁQUINA

Responda em uma linha cada:

- **O que essa peça faz que 90% das peças não fazem?** (se não souber, você ainda não entendeu o original — releia)
- **Qual é o elemento que, se você errar na tradução, mata a adaptação?**
- **O que na peça é local demais pra sobreviver** (referência cultural, instituição, unidade, cidade) e qual é o equivalente brasileiro
- **O que o original deliberadamente NÃO faz** — e que você também não vai fazer

## 2.2 — Trocar o que precisa trocar

| Trocar | Por |
|---|---|
| Marca estrangeira | Sano Magnésio Bisglicinato (ou o produto do user) |
| Dose do original | **Rótulo Sano vigente: 200mg, 1 goma/dia** |
| Libras/polegadas/dólar | Quilos/centímetros/reais |
| Cidades e contexto | Brasil (SUS, plano de saúde, farmácia, cidades reais) |
| Mecanismo estrangeiro | Mecanismo Sano — cálcio contrai / magnésio solta |
| Cabeçalhos de seção | **Remover todos** (regra N7) |
| Destino final | PV Sano ou advertorial próprio |

**Enxertos obrigatórios do briefing Sano** — entram por exigência de produto e compliance, não como melhoria de copy. Sempre dentro da cena, na fala da autoridade, sem bullets. Se o original já resolve algum em cena, use a cena dele em vez de empilhar os dois:
- "Menos de 1% do magnésio circula no sangue" — a dívida do intracelular
- Objeções de omeprazol / interação medicamentosa **dentro da cena, na fala da autoridade, sem bullets**
- Contraindicação renal em 8 palavras

## 2.3 — As 42 regras (bloqueadoras primeiro)

Fonte completa: aba **Regras do Que NÃO Fazer** do briefing.

**Bloqueadoras — um "sim" e o texto volta pra mesa:**
- **N1** narrador leigo, sem profissão, sem credencial
- **N2** ZERO bullet, checkmark, ícone, negrito no corpo
- **N3** mecanismo 100% em diálogo, com interrupções do leigo
- **N4** não dramatizar o mesmo perigo duas vezes
- **N5** repetição só com elevação de registro
- **N6** vilão é o currículo, nunca a pessoa

**Estruturais:**
- **N7** zero cabeçalho de seção
- **N8** primeiro "você" **depois de 78%** do texto (fala de personagem não conta)
- **N13** zero nome de estudo, revista, instituição, CRM
- **N16** máximo **dois atores fisiológicos** (cálcio e magnésio)
- **N17** mecanismo do problema = mecanismo da solução
- **N18** velocidade prometida derivável do mecanismo (nada imediato)

**Autoridade e oferta:**
- **N23** credencial não inventada — sobrenome, sotaque, idade aproximada
- **N24** autoridade encontrada por acaso, nunca procurada
- **N25** autoridade valida o mecanismo, **nunca a marca**
- **N26** narrador ≠ autoridade
- **N27** produto em ≤150 caracteres
- **N28** garantia em **terceira pessoa** ("devolvem", nunca "devolvemos")
- **N29** não fingir neutralidade ("paguei do meu bolso, continuo pagando")
- **N30** carimbar o relógio (23h40, 3h10 — não "de madrugada")
- **N39** narrador paga custo
- **N40** benefício emocional dito por **terceiro**, em fala direta, sem adjetivo
- **N41** CTA sem pressão

## 2.4 — PORTUGUÊS ORGÂNICO (etapa crítica, não pule)

Fonte: `REGRAS-PORTUGUES-ORGANICO.md` na raiz do vault.

### O ritmo NÃO muda

**Frase curta, uma por linha, parágrafo de 1-2 frases.** Isso está certo no long-form e é o que segura leitura de 12 mil caracteres no celular. O CAMPEÃO 4 fez 456 vendas escrito assim.

Meta: **7 a 9 palavras por frase**. Não "corrigir" pra frase longa.

### O que muda é o que está DENTRO da frase

Traduções literais proibidas — checar uma por uma:

| ❌ Decalque | ✅ Brasileiro |
|---|---|
| "trata hormônio **para viver**" (*for a living*) | "é disso que ele vive" |
| "ele **me sentou**" (*sat me down*) | "me chamou pra conversar" |
| "me sentou **na mesa** da cozinha" | "me chamou na cozinha" |
| "a **caixa de ferramentas** errada" (*toolbox*) | "nada na mão pra resolver" |
| "**fina no meio**" (*through the middle*) | "mais magra" |
| "a química **sai do lugar**" | "desanda", "sai do eixo" |
| "não conseguiu **encostar** naquilo" (*touch it*) | "não resolveu" |
| "**tocar o alarme**" (*sounding the alarm*) | "soar o alarme" (alarme dispara) |
| "**Bem-vinda pro outro lado**" | "Bem-vinda ao clube" |
| "mais que **ninguém**" (*than anyone*) | "mais que qualquer pessoa" |
| "**do jeito difícil**" (*the hard way*) | "na marra" |
| "**Eu tenho** 54 anos" (*I'm 54*) | "Tenho 54 anos" — omitir pronome |
| "hormônio **que ele não sabia**" | "sem ele saber" |
| "**três anos atrás**" (*three years ago*) | "faz três anos" |
| "ele **disse**" (repetido) | "ele **falou**" |
| "**prescreveu** um protocolo" | "receitou", "passou" |
| "Eu **disse** que não" | "**Falei** que não" |
| "**Então** eu não entendo" | "**Aí** eu não entendo" |

Outros marcadores medidos no corpus:
- **Aspas** — manter abaixo de ~8/1.000 palavras. Se estourar, converter fala em discurso indireto ("aí ela falou que...")
- **Dois-pontos** — quase inexistente no orgânico. Vira vírgula ou frase nova
- **"pra"** é 20x mais comum que "pro"
- **Exclamação** — uma ou duas no texto todo, em pico de emoção. Zero soa frio

### Validar com o script

```
python scripts/analise-portugues.py <arquivo.txt>
```

Compara contra o corpus de 5.049 palavras de comentários orgânicos do Facebook BR (`scripts/corpus-fb.txt`). Mede palavras/frase, marcadores, decalques e inícios de frase.

**Ampliar o corpus** sempre que aparecer material orgânico bom, principalmente depoimento real de cliente 45+ feminino.

---

# ETAPA 2.5 — DESCOBRIR E CLONAR O DESTINO

**Aprendido na AD-28. É a etapa que mais mudou o resultado e a que quase foi pulada.**

O long-form não vende. Ele entrega o mecanismo e manda clicar. **Quem vende é a página do outro lado** — e o concorrente investe tanto nela quanto no criativo. Adaptar a copy e mandar pra um destino que não bate é jogar fora metade do trabalho.

## 2.5.1 — Nunca assuma qual é o destino

O fim do long-form quase sempre diz *"leia o artigo"* / *"a marca certa está lá dentro"*. **Isso não quer dizer que seja um advertorial narrativo.** Pergunte ao user qual é a URL real, ou procure na Ad Library.

Na AD-28 eu assumi que era o advertorial genérico do rótulo. O user corrigiu duas vezes:
1. Era um **listicle de ranking** (`/consumer-tested-men-listicle`)
2. E existia **também** um advertorial masculino separado (`/advertorial-magnesium-lie-for-men`)

Eram dois destinos diferentes, nenhum dos dois o que eu tinha suposto.

## 2.5.2 — Peça a captura de tela, não só a URL

`WebFetch` devolve **estrutura e texto**, mas não devolve o que a página *parece*. E o layout carrega decisões que o texto não revela.

Na AD-28, só a captura mostrou:
- Barra **laranja** no topo (eu tinha feito azul-escuro)
- **Foto real do frasco** de cada concorrente no ranking
- **Tabela comparativa verde/vermelha** logo na abertura, que não aparecia na transcrição
- Botão **amarelo** repetido dentro de cada card
- O card do #1 **ocupando um terço da página**, os outros quatro bem menores
- Depoimentos como **print de conversa**, não card de texto

> [!warning] O `WebFetch` recusa transcrição integral
> Pedir "transcreva a página inteira" é recusado por direito autoral. **Não insista e não precisa** — o pipeline clona *estrutura*, não texto. Peça a análise estrutural (seções, ordem, headlines, elementos) e escreva conteúdo novo em português.

**Peça sempre:** *"me manda o screencapture da página"*. E confira a altura — captura de página longa **corta em 14400pt sem avisar** (ver [[screencapture-corta-silencioso]]).

## 2.5.3 — O destino pode não existir ainda

Se o equivalente Sano não existe, **produza**. Na AD-28 as duas páginas foram criadas do zero e commitadas junto.

Ao clonar uma página de destino:

**Reaproveite o CSS do que já está no ar.** Pegue o `<head>` e o `<style>` de um advertorial existente (`adv-magnesio-fibromialgia.html` é boa base): Metrito, Montserrat, `.wrap` de 640-680px, masthead, `.dek` com grifo amarelo. Mantém identidade e economiza uma hora.

**Elementos que valem clonar do concorrente:**
- Barra de progresso de leitura no topo
- Anáfora de abertura (sintoma → causa, repetido 5-6 vezes)
- Diário de resultados com dias marcados (1, 3, 7, 10, 14)
- Fecho em dois caminhos (Caminho 1: você fecha a página × Caminho 2: você testa)
- Ranking com nota (A+, B, C, D) e prós/contras em duas colunas

**Elementos que devem ser recusados** — sempre os mesmos:
- Contador regressivo e "estoque acabando"
- "Recomendado por médicos/neurologistas" (aval de classe)
- Número redondo de clientes inventado
- Laboratório ou certificação como aval de autoridade

## 2.5.4 — Comparativo nominal: PERGUNTAR, não decidir

Se a página é um ranking, o concorrente provavelmente cita **marcas reais com foto do frasco**.

**Pergunte ao user: nomeia marca ou ataca categoria?** As duas são válidas.
- **Nomear** é mais concreto e mais fiel ao original
- **Categoria** ("quelado premium", "citrato", "blends", "óxido") serve pra qualquer pote que o leitor tenha em casa

Na AD-28 eu montei genérico por conta própria e depois escrevi na nota como se fosse escolha do user. **Não repita isso.** O user tem time jurídico e decide o que roda; se você achar que há risco, diga em uma frase e execute o que ele escolher.

## 2.5.5 — Marca de terceiro nas imagens: também é decisão do user

O modelo de imagem insere marca real por conta própria (Red Bull, Coca-Cola) quando a cena pede um produto. Isso pode ser **bom** — realismo documental — ou indesejado. **Pergunte antes de travar.**

Se o user quiser travar: `"NO BRAND NAMES on any product. Absolutely no branded cans, bottles or packaging."`

Na AD-28 eu descartei e regerei uma imagem por causa de uma lata de Red Bull sem perguntar nada. Foi decisão minha apresentada como padrão.

## 2.5.6 — Continuidade criativo → página

A regra do briefing é que o sintoma do criativo bata com o sintoma da página. **Verifique e registre quando não bater.**

Na AD-28 o criativo é sobre **sono e recuperação** e o advertorial abre com **cortisol e barriga**. Foi assim que o concorrente montou (a página cobre sono dentro dos benefícios). Mantivemos — mas ficou escrito na nota que, se o CTR cair depois do clique, é o primeiro lugar pra olhar.

---

# ETAPA 3 — SALVAR A NOTA

Destino: `Produtos/Magnésio/Adaptacoes prontas pra subir/Adaptacoes-Externas/AD-NN-<slug>.md`

`NN` = próximo número livre. Verificar o que já existe antes.

## Frontmatter

```yaml
---
produto: Sano Magnésio Bisglicinato Gummies
tipo: long-form
origem: <Concorrente> (<domínio>) — Library ID <id>
angulo: <slug-do-angulo>
avatar: <NN-slug-do-avatar>
sintoma-gancho: <slug>
prioridade: alta | media | baixa
status: 🟡 a produzir
caracteres: <N>
destino: <URL>
cssclasses:
  - wide-page
tags:
  - longform
  - adaptacao/<concorrente>
  - ponte/advertorial   # se for ponte
IMAGENS: Produtos/Magnésio/Adaptacoes prontas pra subir/Adaptacoes-Externas/<AD-NN-slug>/imagens
imagens_total: <N>
---
```

## Corpo da nota — seções obrigatórias

1. **Título** `# AD NN — "<frase que resume>"`
2. **Por que essa peça** — callout com nº de variações ativas e o recurso central que a torna forte
3. **Engenharia reversa do original** — os 7 blocos da Etapa 2.1 preenchidos. É o que prova que a adaptação modelou em vez de reescrever. Os `não usa` ficam registrados como característica da peça
4. **O que mudou do original** — tabela `| Original | Adaptação | Motivo |`
5. **Ressalvas** — `> [!warning]` com riscos identificados **e a decisão do user registrada**, mais um plano B
6. **Auditoria contra as 42 regras** — item a item, com ✅/⚠️ e o que prova cada um
7. **A copy na íntegra**
8. **Fluxo** — o caminho do clique até o checkout
9. **Checklist `> [!todo]`** — o que falta antes de subir
10. **Relacionado** — `[[LF1SP]]`, `[[00-INDICE-Adaptacoes-Externas]]`

Adicionar a linha no `00-INDICE-Adaptacoes-Externas.md`.

---

# ETAPA 4 — GERAR IMAGENS STOP-SCROLL

## 4.1 — CALIBRAR A PESSOA PELO QUE A COPY DIZ (erro mais comum)

**Princípio:** a pessoa na imagem tem que ser a pessoa da copy. Nem pior, nem melhor.

O modelo puxa pro extremo sozinho. Se você não travar, ele entrega a versão dramática — e aí acontecem duas coisas, as duas ruins:

- A leitora-alvo **se exclui**: "não estou nesse ponto"
- A transformação vira **inacreditável** — um caso extremo voltando ao normal não soa possível pra suplemento

### Passo 1 — Extrair da copy os marcadores que existem

Releia a copy e liste **só o que está escrito**:

- Idade, gênero, cidade
- Números literais (peso, altura, medida, tempo de sintoma, horário)
- Sintoma visível (mão trêmula, olheira, inchaço no tornozelo, marca do elástico, rigidez ao levantar)
- Estado geral (cansada, sem dormir há meses, dor ao caminhar)
- Detalhes de aparência mencionados (cabelo, roupa, o que ela veste em casa)

**Se a copy não descreve o corpo, não invente um.** Muita peça de saúde não é sobre aparência — é sobre dor, sono, energia. Nessas, o que precisa estar certo na imagem é a **idade, o cansaço e o ambiente**, não a silhueta.

### Passo 2 — Traduzir os números em instrução de contenção

Onde houver número, calcule o que ele significa e escreva o limite explícito no prompt — **sempre dizendo o que NÃO é**, porque é assim que o modelo obedece.

O molde:
```
[fato da copy]. [Grau moderado], NOT [o extremo que o modelo vai tentar].
- [marcador 1 — onde aparece]
- [marcador 2 — o que NÃO deve aparecer]
- A stranger would call her "[palavra comum]" — NEVER "[palavra extrema]"
```

> **Exemplo da AD-25** (peça sobre peso — *o cálculo é o método, os números são daquela peça*):
> 1,60m e 81kg = IMC 31,6 = obesidade grau 1, no limite de baixo. A primeira geração saiu em IMC 38 e teve que ser refeita.
> ```
> She is 54, roughly 1,60m and 81kg — about 15 kilos above her healthy weight.
> MODERATELY overweight, NOT morbidly obese.
> - Weight concentrated in the ABDOMEN and waist
> - Face full and slightly puffy, SMALL soft double chin. NOT a heavy multi-fold neck
> - Upper arms soft and full but with visible shape and wrist definition. NOT massive
> - A stranger would call her "gordinha" — NEVER "obesa mórbida"
> ```

O mesmo raciocínio em outras peças: dor articular → "moves carefully, NOT visibly disabled". Insônia → "tired and puffy, NOT ill". Cãibra → "grimacing mid-cramp, NOT in medical emergency".

### Passo 3 — Registrar na nota

A calibração usada vai num callout da nota, com o porquê. Serve pra qualquer criativo futuro da mesma peça.

---

## 4.2 — O BASE de realismo (reusar em tudo)

Este bloco é **fixo** — é o que faz a imagem parecer foto de gente real e não anúncio. Uma única linha muda por peça: o registro emocional, no final.

```
PHOTOREALISTIC PHOTOGRAPH, not an illustration, not a render, not AI-art aesthetic.

- Shot on a smartphone, slightly imperfect framing, handheld angle
- HARSH, UNFLATTERING lighting: overhead domestic light, cheap fluorescent, or direct flash
- NO beauty retouching, NO smoothing, NO glamour. Visible skin texture, pores, blemishes
- Real ordinary Brazilian people, NOT models. Tired eyes, no makeup
- Real Brazilian middle-class setting: ceramic floor tiles, plain painted walls, MDF furniture,
  clothes on a white plastic chair, floral bedspread, cluttered surfaces
- Documentary/candid feel, like a photo taken without asking permission
- Muted, desaturated, grainy
- NO text, NO logos, NO watermarks, NO graphic overlays anywhere
- Vertical 4:5 format
```

**O registro emocional deriva da copy** — não é sempre o mesmo. Escolha a linha final conforme a história:

| Se o long-form é sobre | Registro |
|---|---|
| Vergonha, comparação, corpo | `The register must be UNCOMFORTABLE and RAW. The visual equivalent of a confession, not an advertisement.` |
| Dor física, crise, sintoma agudo | `The register must be TENSE and PHYSICAL. The moment the body takes over.` |
| Insônia, exaustão, madrugada | `The register must be LONELY and STILL. The house is asleep and she is not.` |
| Alívio, o depois, retomada | `The register must be QUIET and ORDINARY. Nothing dramatic — just a normal moment that used to be impossible.` |

> A AD-25 usou o primeiro. Isso não faz dele o padrão — faz dele a escolha certa **pra uma peça sobre vergonha do corpo**.

---

## 4.3 — EXTRAIR AS CENAS DO TEXTO (não escolher de um catálogo)

⚠️ **Não existe lista padrão de cenas.** Cada long-form tem as cenas dele. Uma peça sobre cãibra às 3h da manhã não tem as mesmas imagens de uma peça sobre foto de casamento. Se você aplicar um arquétipo genérico, gera imagem bonita que não conversa com o texto — e a leitora não reconhece nada.

**As melhores imagens já estão escritas no long-form.** Ele foi construído com momentos concretos. Seu trabalho é achá-los, não inventar substitutos.

---

### PASSO 1 — Varrer o texto e listar TODO momento visualizável

Releia a copy adaptada do começo ao fim procurando **momentos com lugar, objeto e horário**. Liste tudo, sem filtrar ainda. Procure especificamente:

- **Telas** — a conversa no WhatsApp, o print do grupo da família, a foto que alguém marcou, a busca no Google às 2h
- **Objetos que acusam** — a calça que não fecha, a balança, a caixa de remédio, o copo d'água na mesa de cabeceira, a receita amassada
- **Cômodos e horários exatos** — a cozinha às 23h40, o banheiro antes do banho, o carro parado na garagem
- **Outras pessoas presentes** — quem estava junto naquele momento, e o que essa pessoa fez ou deixou de fazer
- **Eventos sociais nomeados** — a festa da empresa, o aniversário, o casamento, a consulta, a fila da farmácia
- **Gestos pequenos** — ela puxando a blusa pra baixo, evitando o espelho, virando o rosto na foto
- **O momento em que a crença quebrou** (Bloco 5 da Etapa 2) — quase sempre rende a imagem mais forte da peça

Para cada item anote: **em que trecho aparece** e **o que a leitora sente ali**.

---

### PASSO 2 — A pergunta incisiva

Com a lista na mão, pergunte a si mesmo — e responda por escrito:

> **"Quais são as 4 imagens mais desconfortáveis e específicas que EU CONSIGO TIRAR DESTE TEXTO — que fariam alguém parar o dedo no feed, e que só fazem sentido porque esta história existe?"**

As três travas dessa pergunta:

1. **Mais desconfortável, não mais bonita.** A imagem tem que ter algo errado nela. Constrangimento, solidão, flagra, o segundo depois de alguém perceber alguma coisa. Foto agradável não para o scroll
2. **Específica deste texto.** Se a imagem serviria pra qualquer anúncio de suplemento, descarte. Ela tem que carregar o detalhe que só está nesta peça
3. **Legível sozinha.** Alguém que nunca leu o long-form olha e entende a tensão em 1 segundo — mesmo sem saber a história

**Faça essa pergunta de verdade, com a copy na frente.** Não recite arquétipos. As respostas mudam completamente de peça pra peça.

---

### PASSO 3 — Testar cada candidata

Antes de escrever prompt, cada cena passa por 4 perguntas:

- **Está no texto?** Aponte o trecho. Se você não consegue apontar, é invenção — corte ou volte ao texto
- **Qual é a tensão?** Escreva em uma frase o que está errado na imagem. Se você não consegue, a imagem não tem assunto
- **Passa no teste do 1 segundo?** Sem legenda, sem contexto, o desconforto se lê?
- **É diferente das outras três?** Quatro variações do mesmo sentimento é uma cena, não quatro

---

### PASSO 4 — O ponto emocional explícito

Todo prompt termina declarando **o que a imagem tem que fazer sentir** — o modelo compõe melhor quando sabe o assunto emocional, não só os elementos.

Exemplo de fechamento de prompt:
```
The emotional point: she is the only one in the room who is aware of her body.
Nobody is looking at her. That is what makes it worse.
```

---

### Como isso se parece na prática

**Só como demonstração do raciocínio** — não como cenas pra reutilizar:

| Trecho do long-form | Cena extraída | A tensão |
|---|---|---|
| "trocando mensagem com uma amiga" | Print de conversa real no celular, dedo digitando, cozinha desfocada ao fundo, 23h47 na barra de status | O que ela digita e apaga |
| "na festa da empresa, do lado dela" | Duas mulheres da mesma idade lado a lado, uma à vontade, a outra com o braço cruzado na frente do corpo | A comparação que ninguém verbalizou |
| "olhei a foto que me marcaram" | Ela sozinha vendo o próprio rosto marcado numa foto no feed, luz do celular no escuro | Ela se vê como os outros a veem |
| "o remédio na mesa de cabeceira" | Só a mesa de cabeceira: caixa aberta, copo pela metade, despertador em 3h10 | Ninguém na foto, e mesmo assim é sobre alguém |

Repare que **nenhuma dessas serve pra outra peça**. É esse o padrão a perseguir.

---

### Se a peça tiver antes e depois

Só se o texto tiver mesmo essa virada. E aí vale uma regra técnica:

**Âncora física idêntica nos dois painéis** — mesma toalha, mesmo interruptor, mesmo azulejo, mesma blusa. Sem âncora o modelo entrega duas mulheres diferentes e a peça morre. Escreva a âncora no prompt dos dois painéis, com as mesmas palavras.

---

## 4.4 — Setup técnico

**Chave:** `GEMINI_IMAGE_API_KEY` do `.env` do Sanologia (formato `AIza...`).
⚠️ A `GEMINI_API_KEY` (formato `AQ.`, Vertex Express) **não tem o modelo de imagem na região** — dá 404.

**Modelo:** `gemini-3.1-flash-image`

Copiar `scripts/gerar-imagens-template.py`, ajustar `AD` (nome da nota) e a lista `CRIATIVOS`.

**Destino: dentro do vault**, ao lado da nota — `Adaptacoes-Externas/<AD-NN-slug>/imagens/`.
As imagens sincronizam junto com a copy e aparecem embutidas no Obsidian, então
qualquer máquina do time abre a nota completa.

O script **acha o vault sozinho** (Windows e Mac). Se tiver vault em lugar
incomum, fixar com `SANO_VAULT=/caminho/do/vault`. O `.env` também é procurado
em vários lugares — ou apontar com `SANO_ENV=/caminho/.env`.

Rate limit: `time.sleep(12)` entre chamadas + backoff de 20s×tentativa no 429.

---

# ETAPA 5 — SATURAR A CENA APROVADA

Depois que o user aprovar uma cena, gere variações dela **até esgotar os jeitos de contar aquele mesmo momento**.

**Quantas:** entre 6 e 12, conforme o que a cena aguenta. Uma cena com muitos elementos (duas pessoas, um objeto, um cômodo) rende mais ângulos que um close de objeto. Se você está forçando a variação 9 e ela já repete a 4, pare em 8. Se ainda tem ideia boa na 12, siga. *(A AD-25 fechou em 9 — número daquela cena, não regra.)*

**A regra que não muda:** manter o eixo emocional, variar cenário, enquadramento e momento. Se você mudou o que a imagem faz sentir, não é variação — é outra cena, e ela precisa da aprovação do user.

### O que varia

Percorra estes eixos e veja quais a **sua** cena comporta:

- **Distância** — o mesmo momento em plano aberto, médio e close
- **Ponto de vista** — dela, de quem observa, de ninguém (câmera de canto de cômodo)
- **Sobre o ombro** — POV de quem está vendo a cena acontecer
- **Close sem rosto** — funciona diferente no feed: não tem personagem pra leitora rejeitar
- **Reflexo** — espelho, vidro da janela, tela preta do celular
- **Deslocamento no tempo** — o segundo *antes* e o segundo *depois* do momento oficial, quando ninguém mais está olhando
- **Só o objeto** — a cena contada pelo que ficou pra trás, sem gente nenhuma
- **Troca de cômodo** — o mesmo momento em outro lugar da casa, se a história permitir
- **Altura da câmera** — plongée, altura dos olhos, de baixo

Nem toda cena aceita todos. Um print de conversa no celular não tem plongée útil; uma cena com duas pessoas num sofá tem seis enquadramentos bons.

### Erros conhecidos do modelo — travar no prompt

- Foto de grupo vira **fila diagonal** sozinha → escrever "ONE SINGLE STRAIGHT HORIZONTAL ROW, camera perpendicular, all at the SAME DISTANCE, like a school class picture"
- Reflexo sai **diferente** do corpo real (quase sempre mais favorecido) → "the reflection and the real body must be EXACTLY THE SAME. A reflection that looks different is a fatal error"
- Cena noturna sai **escura demais** pra ler no feed → pedir fonte de luz explícita e nomeada (abajur, luz do celular, luz da geladeira aberta, poste pela janela)
- Tela de celular vem com **texto ilegível ou inventado** → descrever a tela como forma e luz ("a messaging app, green and white bubbles, blurred illegible text"), nunca pedir palavras específicas

---

# ETAPA 6 — INVENTARIAR

As imagens já nascem no lugar certo — `Adaptacoes-Externas/<AD-NN-slug>/imagens/`, dentro do vault, ao lado da nota. Falta gerar os JPGs e escrever o inventário.

**Gerar JPGs** — Meta aceita PNG, mas 800 KB por criativo é peso à toa. JPG q92 dá ~1/3 e o vault não incha:

```python
from PIL import Image
from pathlib import Path
p = Path(".")                      # rodar dentro da pasta imagens/
out = p / "jpg"; out.mkdir(exist_ok=True)
for f in sorted(p.glob("*.png")):
    Image.open(f).convert("RGB").save(out / f.name.replace(".png", ".jpg"),
                                      "JPEG", quality=92, optimize=True)
```

Se o vault estiver ficando pesado, apagar os PNG depois de conferir os JPGs — os JPGs é que sobem pro Meta.

Adicionar seção `## 🖼️ Criativos stop-scroll` na nota com:

- **Pasta + total**, e o aviso de subir os JPGs (não os PNG)
- **Ranking de aposta** 🥇🥈🥉 — tabela `| # | Arquivo | Cena | Por quê |`. Não liste tudo como igual; o user precisa saber por onde começar
- **As cenas extraídas** — qual trecho do long-form deu origem a cada uma, e a tensão de cada (Etapa 4.3). É o que permite julgar se a imagem ainda conversa com a copy quando a copy mudar
- **Callout da calibração** usada e por quê — serve pra qualquer criativo futuro da mesma peça
- **Notas de produção** — quais saíram erradas, por quê, quais precisam regerar
- **Scripts e API** usados

**Embutir as melhores na própria nota.** Como as imagens vivem no vault, o Obsidian mostra direto:

```
![[<AD-NN-slug>/imagens/jpg/01-nome-da-cena.jpg]]
```

Vale pelo menos pro pódio — quem abre a nota vê a aposta sem precisar caçar pasta.

---

# ETAPA 7 — SUBIR NO META (quando o user pedir)

**Só com token que o user mandar.** Avise uma vez que ele fica no histórico em texto puro e deve ser revogado depois. Apague o arquivo do disco ao terminar.

## O que clonar da conta

Nunca invente a estrutura. Leia um adset que já roda e copie:

```
campanha  BIDCAP - Magnesio Bisglicinato   120248694356150442   (EUA 11)
conta     act_2164352101016970
página    809142178952032
pixel     2738375386539927  ·  custom_event_type PURCHASE
bid       3860 (US$ 38,60)
atribuição 7d click
```

## Três pegadinhas da API que custam tempo

**1. Regulação brasileira, não DSA.** O adset exige:
```
regional_regulated_categories: ["BRAZIL_REGULATION","VOLUNTARY_VERIFICATION"]
regional_regulation_identities: {universal_beneficiary: "880756411607509",
                                 universal_payer:       "880756411607509"}
```
O erro é *"O anunciante está ausente"* e induz a tentar `dsa_beneficiary`, que **não resolve**.

**2. `standard_enhancements` foi descontinuado.** Mandar `degrees_of_freedom_spec` com ele derruba **todo** creative. Simplesmente não envie o campo.

**3. A edge `/ads` demora a indexar.** Logo após criar, a consulta volta 0 anúncios mesmo com os IDs retornados na criação. Confira no Gerenciador.

## Regras de operação

- **Tudo PAUSED.** Adset e anúncios. O user ativa.
- **Nome do anúncio = nome do arquivo** (`AD28-f4-v07-cabine-vazia`). É o que permite cruzar performance com a cena depois.
- **Pause individualmente as imagens descartadas** que subiram no lote, e registre na nota qual é.
- **Confirme o targeting pela API**, não pelo log — texto de log herdado de script anterior mente. Na AD-28 o log dizia "BR 35-65" e o real era 40-60 masculino.
- **Restrição de gênero é decisão do user**, não sua. Corta metade do alcance; pergunte.

---

# CHECKLIST FINAL

- [ ] Copy passou nas 6 regras bloqueadoras
- [ ] `analise-portugues.py` rodado, decalques zerados
- [ ] Primeiro "você" depois de 78%
- [ ] Produto em ≤150 caracteres, garantia em terceira pessoa
- [ ] Nota salva com frontmatter completo + auditoria + ressalvas do user
- [ ] Linha adicionada no `00-INDICE-Adaptacoes-Externas.md`
- [ ] Pessoa das imagens confere com o que a copy descreve (e nada foi inventado)
- [ ] JPGs gerados dentro do vault, ao lado da nota
- [ ] Ranking de aposta escrito
- [ ] Imagens erradas sinalizadas na nota

---

## O QUE NUNCA FAZER NESTE PIPELINE

0. **Assumir qual é o destino.** Foi o maior erro da AD-28. Pergunte a URL real e peça a captura de tela antes de escrever qualquer página.

1. **Reescrever o esqueleto.** Se a peça tem 23 variações rodando, a estrutura está paga. Troque mecanismo, marca e mercado — não a arquitetura
2. **Remover o que o user mandou manter.** Registre a ressalva uma vez e execute
3. **Repetir ressalva já decidida** ou citá-la de volta como argumento
4. **"Corrigir" o ritmo picotado** pra frase longa. É long-form, não comentário de Facebook
5. **Gerar imagem sem calibrar a pessoa pelo que a copy descreve** — e nunca inventar corpo que a copy não menciona
6. **Escolher cena de catálogo em vez de extrair do texto.** As imagens estão escritas no long-form
7. **Entregar 30 imagens sem ranking.** Sem prioridade, o user não sabe por onde começar
