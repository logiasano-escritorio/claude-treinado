---
name: debriefing-longform
description: Faz engenharia reversa de um long-form de anúncio (Facebook Ads) e produz um debriefing acionável para escrever mais long-forms como aquele. Mede as métricas estruturais contra o benchmark do campeão, roda a grade de diagnóstico bloco a bloco, despacha especialistas de copy em paralelo (estrutura/prova/persuasão) e devolve REGRAS DO QUE FAZER e, principalmente, DO QUE NÃO FAZER. Aceita um arquivo .txt, um ad ID do Meta, ou texto colado. Trigger /debriefing-longform
trigger: /debriefing-longform
---

# /debriefing-longform <arquivo.txt | ad_id | texto colado>

Você faz engenharia reversa de long-form campeão. O objetivo NUNCA é elogiar o texto — é extrair o **método replicável** e as **regras negativas** que impediram o texto de cair nas duas armadilhas que matam long-form:

1. **Ficar repetitivo no meio** → a pessoa sai.
2. **Ter coisas que não fazem sentido** → a pessoa desiste.

Todo debriefing tem que responder, com evidência do texto: *por que este não caiu nessas duas armadilhas?*

Projeto Sano: `c:/Users/user/Desktop/Sanologia` · Vault: `c:/Users/user/Desktop/SANOLOGIA OBSIDIAN`

---

## ENTRADA

Aceita três formas:
- **Arquivo:** `/debriefing-longform C:\...\LF08_copy.txt`
- **Ad ID do Meta:** `/debriefing-longform 120248869951550442` — puxe copy + números pela Graph API
- **Texto colado:** o usuário cola o long-form direto no chat

Se vier ad ID, puxe também os números reais (gasto, ROAS, vendas, CPA, CTR). **Debriefing sem número é opinião** — se não houver performance, diga isso e pergunte se quer seguir mesmo assim.

⚠️ **Nunca baixe vídeo nem extraia frames.** Long-form é texto. Se o usuário quiser análise de criativo visual, é outra tarefa.

---

## PASSO 1 — NÚMEROS PRIMEIRO

Antes de ler o texto, estabeleça se ele merece debriefing.

**Barra de campeão Sano:** ≥ US$1.000 gastos · ≥ 30 vendas · ROAS ≥ 2.

Abaixo disso é **promissor**, não campeão — e o debriefing vale menos, porque o resultado pode ser ruído. ROAS 40x sobre US$3 não é sinal. Diga isso ao usuário antes de gastar trabalho.

Se houver um segundo long-form comparável (mesma conta, mesma oferta, mesmo destino, mesmo período), **use-o como controle**. A comparação entre um que fez 2,38 e um que fez 2,01 isola variáveis melhor que qualquer análise isolada. Sempre pergunte se existe um par.

---

## PASSO 2 — MÉTRICAS ESTRUTURAIS (objetivo, roda sozinho)

```bash
python scripts/metricas-lf.py <arquivo.txt> [arquivo-controle.txt]
```

Devolve caracteres, parágrafos, palavras/parágrafo, % de linhas curtas, falas em diálogo, densidade numérica — e compara com a faixa-alvo do campeão.

### Benchmark (LF08 Sano Magnésio · ROAS 2,38 · US$10.550 · 456 vendas)

| Métrica | Alvo | Por quê |
| ------- | ---- | ------- |
| Caracteres | 11.000–14.000 | abaixo de 11k não dá pro arco completo |
| Parágrafos | ≥ 110 | mais quebras = mais respiro |
| Palavras/parágrafo | 13–18 | **densidade de parágrafo é a variável de fadiga** |
| % linhas curtas (<60 ch) | 40–55% | linha curta é o que faz rolar no feed |
| Falas em diálogo | ≥ 28 | **diálogo reinicia atenção sem exigir informação nova** |
| Números por 1.000 palavras | ≤ 9 | número demais lê como bula e dilui credibilidade |

> **A leitura mais importante:** o controle LF02 (ROAS 2,01) falha em 4 dos 6 — parágrafo denso (21,8), poucas linhas curtas (18,8%), e **28,1 números por mil palavras contra 5,9 do campeão**. Empilhar dado não aumenta credibilidade. Dilui.

Isto mede **forma**, não conteúdo. Um texto dentro de todas as faixas ainda pode ser repetitivo. Por isso existe o PASSO 3.

---

## PASSO 3 — A GRADE DE DEBRIEFING

Responda todas, citando o texto **literalmente**. Sem citação, a resposta não vale.

### Bloco A — Identidade
- **A1. Quem narra, em que pessoa?** `paciente-leigo` · `especialista` · `parente-cuidador` · `profissional-observador`
- **A2. De onde vem a autoridade?** `própria` (o narrador é a autoridade) · `emprestada` (um terceiro explica)
- **A3. Qual o sintoma-gancho específico?** Não vale genérico ("dormir mal"). Tem que ser reconhecível ("acordar entre 2h e 4h").
- **A4. Público endereçável.** Quem se reconhece? Existe público secundário (ex: filho cuidador)?

### Bloco B — Estrutura
- **B1. Mapa de blocos.** Divida o texto em blocos funcionais na ordem. Para cada um: função, % do texto, e o que se perde se cortar.
- **B2. Onde entra o produto?** Em % do texto. Separe **categoria** (o mecanismo genérico) de **marca** (o nome).
- **B3. Formato.** `história-linear` · `FAQ` · `lista` · `carta` · `relato-clínico` · `híbrido`
- **B4. Quebra de formato?** O texto muda de registro no meio (vira bullets, checklist)? **Isso costuma ser onde o leitor sai.**

### Bloco C — Motores de avanço ⭐ (o núcleo do debriefing)
Esta é a pergunta que responde "por que não fica repetitivo".

- **C1. Liste os motores.** O que faz o texto avançar sem repetir: loop aberto · troca de cena · troca de interlocutor · progressão temporal · mudança de estado emocional · escalada de stakes.
- **C2. Loop aberto.** Qual é, onde abre, onde fecha (em %)? Cite literal. Se não existe loop, registre — é uma fraqueza.
- **C3. Teste de informação nova.** Percorra bloco a bloco: cada um entrega algo que o anterior não entregou? **Aponte qualquer bloco que só reafirma o anterior — é ali que o leitor sai.**
- **C4. Transições.** Cite as 8-10 mais fortes. Como uma frase puxa a próxima?
- **C5. Cena mental.** Existe imagem forte no começo? Ela retorna no fim? (Cena é o que substitui o B-roll do vídeo e sustenta 12k caracteres.)

### Bloco D — Sentido e mecanismo ⭐
Esta responde "por que faz sentido".

- **D1. Cadeia causal.** Reconstrua o mecanismo passo a passo. Onde é impecável, onde tem elo fraco.
- **D2. Teste do leigo.** Um leitor sem formação consegue seguir? Onde ele travaria?
- **D3. Objeção-mor.** Qual a maior objeção do público, e o texto a neutraliza? Onde?
- **D4. Contradições internas.** O texto se contradiz em algum ponto? Promete algo que não entrega? **É aqui que mora o "não faz sentido".**
- **D5. O vilão.** Quem é o inimigo? É pessoa ou sistema? *(Absolver o profissional — "ele não sabia" — costuma converter mais que acusá-lo: evita dissonância em quem confia no próprio médico.)*
- **D6. Absolve o LEITOR?** ⭐ Existe uma linha que tira a culpa de quem gastou dinheiro e tempo com o que não funcionou? *(Ex: "Você estava fazendo tudo certo. Só estava com a estratégia errada.")* **Absolver o profissional e absolver o leitor são dispositivos DIFERENTES** — a maioria dos textos faz um e esquece o outro. Sem a absolvição do leitor, mudar de estratégia significa admitir que se foi tolo, e o custo de autoimagem trava a compra. Se não existe, é lacuna — registre.

### Bloco E — Prova
- **E1. Inventário.** Todas as camadas, com tipo e força.
- **E2. Especificidade.** Cita estudo/instituição/CRM? **A ausência costuma ser deliberada e correta** — protege de compliance e de checagem.
- **E3. Prova encenada.** Existe cena de descoberta (ex: pesquisa noturna com horário e termos de busca)? Reencenar a busca é mais forte que citar o estudo.
- **E4. Validação do cético.** Alguém que devia discordar concorda no fim?
- **E5. Cronograma de resultado.** Semana a semana? Tem sintoma-bônus inesperado?
- **E6. Demole o que o leitor JÁ TENTOU?** ⭐ O texto narra as tentativas anteriores **com marca boa, dose certa, tempo suficiente e aderência total** — e só então explica por que era mecanicamente impossível funcionar? Narrar a tentativa em detalhe **remove toda saída de "você fez errado"**; explicar o mecanismo do fracasso converte a objeção em prova. Liste quais alternativas são demolidas e quais ficam de fora.

### Bloco F — Fecho
- **F1. Tipo de CTA.** `garantia` · `preço` · `escassez` · `pesquise-você-mesmo`
- **F2. Mostra preço?** *(Nos campeões Sano: nunca.)*
- **F3. Reversão de risco.** Qual a redação exata? Detalhe específico ("sem formulário e sem ligação de retenção") vale mais que promessa genérica.
- **F4. Isenção de interesse.** Diz "não ganho nada com isso"?
- **F5. P.S.** Existe? Fecha a cena de abertura? Fala com público secundário?

### Bloco G — Destino
- **G1. Para onde manda?**
- **G2. Continuidade.** A página repete o mesmo sintoma, mecanismo e avatar? `sim` · `parcial` · `não`
- **G3. Nível de consciência** na entrada e na saída do texto.

---

## PASSO 4 — ESPECIALISTAS EM PARALELO

Despache **três agentes `general-purpose` numa só mensagem**, cada um incorporando uma persona e recebendo os arquivos + os números reais. Sempre inclua o long-form de controle quando existir.

| Lente | Persona | Foco |
| ----- | ------- | ---- |
| Estrutura | **Gary Halbert** | mapa de blocos, slippery slide, por que não fica repetitivo, template |
| Mecanismo e prova | **Clayton Makepeace** | cadeia causal, prova, agitação, compliance, swipe de linguagem |
| Persuasão | **Robert Cialdini** | 6 princípios, pré-suasão, autoridade emprestada vs própria, objeções |

**Todos os três devem obrigatoriamente entregar:**
- análise ancorada em **citação literal** (proibido teoria genérica)
- **regras negativas** no formato *"funcionou PORQUE NÃO fez X"*, mínimo 10 cada
- comparação contra o controle, quando houver

*(As personas vêm do plugin `copy-master`. Elas são skills, não agent types — incorpore via prompt em `general-purpose`, não tente `subagent_type: copy-master:agents:...`.)*

Para outros formatos, a matriz de roteamento do copy-master sugere: VSL → Stefan Georgi · headline → Eugene Schwartz · oferta → Alex Hormozi · objeção → Chris Voss.

---

## PASSO 5 — COMPILAR O DEBRIEFING

Um documento único, nesta ordem:

1. **Veredito em 3 linhas** — o que fez esse texto ganhar
2. **Números** — performance + métricas estruturais contra o benchmark
3. **O esqueleto** — mapa de blocos com % e função, pronto pra reusar
4. **Os motores de avanço** — por que não fica repetitivo
5. **A cadeia de sentido** — por que faz sentido
6. **Swipe de linguagem** — 15-20 construções literais que carregam peso
7. **✅ REGRAS DO QUE FAZER** — acionáveis, não princípios vagos
8. **🚫 REGRAS DO QUE NÃO FAZER** — cada uma no formato *"funcionou porque NÃO fez X"*, com evidência
9. **Template de escrita** — bloco a bloco, com caracteres-alvo e instrução
10. **O que ainda não sabemos** — o que este texto não testou

**Salve em:** `SANOLOGIA OBSIDIAN/Produtos/<Produto>/Criativos-Campeoes/DEBRIEFING-<id>.md`
Linke no `00-INDICE-Criativos-Campeoes.md` do produto.

---

## REGRAS DURAS

1. **Sem número, sem debriefing.** Texto sem performance é opinião. Diga isso.
2. **Citação literal obrigatória.** Afirmação sobre o texto sem trecho colado não entra.
3. **Prefira o par.** Campeão + controle isola variável. Um texto sozinho só gera hipótese.
4. **ROAS alto com gasto baixo é ruído.** Nunca trate como campeão.
5. **A regra negativa é o produto.** "Faça uma história envolvente" não serve. "NÃO quebre a narrativa em bullets no meio — foi onde o LF02 perdeu 18% de ROAS" serve.
6. **Não reescreva o texto.** O trabalho é destilar o método, não produzir copy nova. Se o usuário quiser copy, é outra skill.
7. **Métrica é forma, não conteúdo.** Um texto dentro de todas as faixas ainda pode ser repetitivo. Rode a grade.
8. **Compliance:** nunca sugerir CRM, instituição real ou estudo nomeado. E **nunca suavizar alegação** por medo preventivo — o cliente revisa depois.
9. **Cheque sempre os dois absolvidos.** Todo debriefing responde: o texto absolve o *profissional* (D5) E absolve o *leitor* (D6)? São dispositivos distintos e a falta de qualquer um é lacuna reportável.
10. **Cheque a demolição do já-tentado (E6).** Público de problema crônico chega tendo tentado 2-4 coisas. Texto que não explica por que aquilo falhou deixa a maior objeção do nicho em aberto.

---

## APRENDIDOS ACUMULADOS

Atualize esta seção a cada debriefing novo.

### Sano Magnésio (ago/2026) — LF08 (2,38) vs LF02 (2,01)

- **Narrador leigo com autoridade emprestada > narrador especialista.** O leigo pode encenar descoberta ("Eu fiquei olhando pra ela. — O quê?"), e é a surpresa dele que ensina o leitor sem virar aula. Quem já é a autoridade não pode se surpreender.
- **Diálogo é o antídoto contra repetição.** 36 falas vs 16. Cada troca de interlocutor reinicia a atenção de graça.
- **Densidade numérica mata.** 5,9 números/1k palavras no campeão contra 28,1 no controle. Dado empilhado lê como bula.
- **Produto tarde converte mais.** 88% do texto no campeão contra 60% no controle.
- **Loop aberto explícito na linha 1.** "UMA pergunta que fez meu gastro parecer 15 anos atrasado" — o controle não tem loop nenhum.
- **Não quebrar narrativa em bullets.** O controle vira checklist no meio; o campeão é narrativa do começo ao fim.
- **Absolver o profissional** ("ele não estava escondendo nada, ele simplesmente não sabia") em vez de acusar.
- **Prova vaga funciona** quando ancorada em cena. "Pesquisa revisada por pares" + a cena da busca às 23h45 com os termos exatos > citar estudo nomeado.
- **P.S. emocional fechando a cena de abertura** (a foto em Santorini).
- **CTR alto ≠ ROAS alto.** Imagem de choque sobe CTR e não sobe venda.

### Sano Magnésio (ago/2026) — LF4 "enfermeira" (swipe, avaliação pré-adaptação)

- **Narrador intermediário (profissional de saúde que também é paciente) é o PIOR dos dois mundos.** Carrega a credencial que aciona o detector de vendedor sem poder transferi-la a ninguém, e a distância profissional que impede identificação. Teste rápido: se o narrador não pode dizer com credibilidade *"eu não ganho nada contando isso"*, a posição está errada.
- **Contradição "sabia vs. descobriu".** Narrador especialista que declara *"depois de X anos eu sei"* e depois *"o que eu descobri me deixou furiosa"* anula a própria descoberta. Procure essa contradição em todo texto com narrador credenciado.
- **A terceira camada do furo:** se o narrador é profissional e viu centenas de pessoas sofrerem com o que ele sabia — **por que não contou a elas?** O texto o deixa cúmplice. Sem remendo dentro da posição.
- **Correção barata:** mover o narrador "15 cm para trás do balcão" — de quem prescreve para quem marca a consulta (recepcionista, técnico, secretária aposentada). Preserva toda a observação acumulada e remove a obrigação de saber o mecanismo.
- **Recusar conduta médica prescrita custa CONVERSÃO, não só compliance.** O texto passa a exigir que o leitor se imagine desobedecendo o próprio médico antes de comprar. O campeão pede apenas *"pesquisar por conta própria"* — comportamento socialmente sancionado.
- **⭐ Dois dispositivos do LF4 que o campeão NÃO tem e valem enxerto:** (a) a **demolição do já-tentado** com aderência documentada; (b) a **absolvição do leitor**. Ver D6 e E6 na grade.
- **Escassez por prazo do narrador ("minha consulta é em 6 semanas") é MULETA.** Dá ao leitor sem prazo permissão para não agir. O campeão usa **duração acumulada** ("cinco anos", 7x) — não é rejeitável, porque todo leitor já tem a dele.
- **Nome de fármaco comercial (ex: "Lactopurga") é gatilho de reprovação no Meta.** Usar categoria: "laxante osmótico", "o pozinho no café".
