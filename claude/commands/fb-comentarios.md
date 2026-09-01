# Seção de Comentários Facebook — Relívia

Você é especialista em criar seções de prova social estilo Facebook para landing pages da marca Relívia.

---

## PASSO 1 — Ler o HTML do produto

O usuário vai fornecer o caminho de um arquivo HTML de produto.

Leia o arquivo completo e extraia:
- **Nome do produto** (para usar nos comentários)
- **Problema principal** que o produto resolve (dor, desconforto, limitação)
- **Como o produto funciona** (uso noturno? uso diário? aplicação? onde no corpo?)
- **Benefícios específicos** mencionados na página (ex: dorme melhor, sem cirurgia, reduz hérnia, etc.)
- **Público-alvo** (faixa etária, gênero predominante, perfil)
- **Promessas centrais** da copy (ex: resultado em 21 dias, sem remédio, evita cirurgia)

---

## PASSO 2 — Criar os comentários

Com base no contexto extraído, crie **10 a 13 comentários** com as seguintes características:

### Estrutura de comentários obrigatória:
1. **2-3 comentários principais fortes** — relatos detalhados, emocionais, com resultado específico
2. **1-2 respostas** a esses comentários (reforçando ou fazendo pergunta)
3. **1 comentário de ceticismo vencido** — "fui cética mas funcionou"
4. **1 comentário de terceiro** — comprou pra familiar (mãe, pai, sogra, irmã)
5. **1 comentário de expectativa** — acabou de receber, vai usar hoje
6. **1 thread de entrega** — pergunta sobre prazo + resposta com cidade e dias
7. **1 comentário de dúvida sobre cirurgia/tratamento** — com 2 respostas positivas
8. **1-2 comentários curtos de suporte** — "mal posso esperar", "quero muito tentar"

### Regras para os textos:
- Mencionar o nome do produto pelo menos 4-5 vezes no total
- **NUNCA usar símbolos de marca (™, ®, ©) no texto dos comentários** — pessoas reais não digitam isso; usar apenas o nome simples do produto (ex: "RoncoZero", não "RoncoZero™")
- Referenciar **sintomas específicos** do produto (ex: para hérnia: L4-L5, L5-S1, ciática, dor ao dormir)
- Usar linguagem natural brasileira (gírias leves: "tô", "pra", "né", emojis pontualmente)
- Nomes brasileiros comuns (não gringos)
- Likes variando de 3 a 12 (mais likes nos melhores comentários)
- Horários variando de "28 min" até "7 h"
- Nunca repetir o mesmo número de likes em comentários consecutivos

### Tom e dinâmica de conversa (seguir esse padrão):
O diferencial dessa seção é que parece uma **conversa real entre pessoas** — não comentários soltos. Replicar exatamente esse estilo:

- **Respostas diretas pelo nome**: "Oi Juliana!", "Daniela, eu tinha exatamente isso..."
- **Perguntas que geram respostas**: alguém pergunta prazo de entrega → outro responde com cidade e dias; alguém pergunta sobre cirurgia → 2 pessoas respondem com casos próprios
- **Encadeamento emocional**: um comentário forte gera uma resposta empática ("Que história linda!", "Fico feliz de saber isso!")
- **Terceiro que comprou para familiar**: "Comprei pra minha sogra/mãe/pai" → a história emocional do familiar é o resultado
- **Progressão temporal dos resultados**: comentários misturando quem acabou de receber, quem está na semana 2, quem já tem 1 mês — cria sensação de comunidade ativa
- **Ceticismo vencido com detalhes**: não só "funcionou" — dizer o que tentou antes (fisioterapia, acupuntura, remédio) e o que mudou especificamente
- **Especificidade clínica natural**: mencionar nomes técnicos como uma pessoa leiga falaria ("hérnia L4-L5", "compressão do nervo", "ressonância") — soa real sem parecer copy
- **Emojis com moderação e propósito**: 😭 em história emocionante, 🤞 em quem vai usar pela primeira vez, 🙏 em agradecimento, 😂 em situação engraçada (irmã pedindo emprestado)

---

## PASSO 3 — Gerar o HTML completo

Gere a seção completa com:

### CSS (inserir no `<head>` após o link do style.css):

```html
<style>
/* ── Facebook Comments Widget ── */
.fb-section {
  background: #F5F6F8;
  padding: 50px 20px;
}
.fb-section__heading {
  text-align: center;
  font-size: 22px;
  font-weight: 700;
  color: #111;
  margin-bottom: 6px;
}
.fb-section__sub {
  text-align: center;
  font-size: 14px;
  color: #666;
  margin-bottom: 28px;
}
.fb-widget {
  max-width: 680px;
  margin: 0 auto;
  background: #fff;
  border: 1px solid #dddfe2;
  border-radius: 8px;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
.fb-widget__header {
  background: #1877f2;
  color: #fff;
  padding: 10px 16px;
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
}
.fb-widget__header svg { width: 20px; height: 20px; fill: #fff; }
.fb-comments-list { padding: 14px 16px; }
.fb-comment {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
}
.fb-comment--reply {
  margin-left: 46px;
  margin-top: -6px;
}
.fb-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  flex-shrink: 0;
  object-fit: cover;
}
.fb-comment-body { flex: 1; min-width: 0; }
.fb-bubble {
  background: #f0f2f5;
  border-radius: 18px;
  padding: 8px 12px;
  display: inline-block;
  max-width: 100%;
}
.fb-name {
  font-weight: 700;
  font-size: 13px;
  color: #050505;
  display: block;
  margin-bottom: 2px;
}
.fb-text {
  font-size: 14px;
  color: #050505;
  line-height: 1.45;
  margin: 0;
}
.fb-text strong { font-weight: 700; font-style: normal; }
.fb-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 5px;
  padding-left: 4px;
  font-size: 12px;
  color: #65676b;
}
.fb-actions span { font-weight: 700; cursor: default; }
.fb-likes {
  display: flex;
  align-items: center;
  gap: 3px;
  margin-left: auto;
}
.fb-likes-icon {
  background: #1877f2;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.fb-likes-icon svg { width: 10px; height: 10px; fill: #fff; }
.fb-divider {
  height: 1px;
  background: #f0f2f5;
  margin: 4px 0 14px;
}
</style>
```

### Estrutura HTML de cada comentário:

**Comentário principal:**
```html
<div class="fb-comment">
  <img class="fb-avatar" src="https://i.pravatar.cc/40?img=N" alt="Nome" />
  <div class="fb-comment-body">
    <div class="fb-bubble">
      <span class="fb-name">Nome Sobrenome</span>
      <p class="fb-text">Texto do comentário com <strong>palavra em negrito</strong>.</p>
    </div>
    <div class="fb-actions">
      <span>Curtir</span><span>Responder</span>
      <div class="fb-likes"><div class="fb-likes-icon"><svg viewBox="0 0 24 24"><path d="M1 21h4V9H1v12zM23 10c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z"/></svg></div>N</div>
      <span style="color:#999;font-weight:400">X h</span>
    </div>
  </div>
</div>
```

**Resposta (aninhada):** igual ao acima mas com classe `fb-comment fb-comment--reply`

**Divisor entre grupos:** `<div class="fb-divider"></div>`

### Avatares:
- Usar `https://i.pravatar.cc/40?img=N` com N de 1 a 70
- Usar números diferentes para cada pessoa
- Usar o mesmo N para a mesma pessoa que aparece em mais de um comentário

### Wrapper da seção:
```html
<!-- ============================================================
  FACEBOOK COMMENTS
============================================================ -->
<section class="fb-section">
  <h2 class="fb-section__heading">O que estão falando sobre o [PRODUTO]</h2>
  <p class="fb-section__sub">Comentários reais de compradores verificados</p>
  <div class="fb-widget">
    <div class="fb-widget__header">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M24 12.073C24 5.405 18.627 0 12 0S0 5.405 0 12.073C0 18.1 4.388 23.094 10.125 24v-8.437H7.078v-3.49h3.047V9.41c0-3.025 1.792-4.697 4.533-4.697 1.312 0 2.686.236 2.686.236v2.97h-1.513c-1.491 0-1.956.93-1.956 1.885v2.27h3.328l-.532 3.49h-2.796V24C19.612 23.094 24 18.1 24 12.073z"/></svg>
      Comentários do Facebook
    </div>
    <div class="fb-comments-list">
      <!-- comentários aqui -->
    </div>
  </div>
</section>
```

---

## PASSO 4 — Onde inserir

- **CSS**: dentro do `<head>`, após `<link rel="stylesheet" href="style.css" />`
- **Seção HTML**: após o fechamento `</section>` da seção DEPOIMENTOS (ou onde o usuário indicar)

Aplique os edits diretamente no arquivo indicado pelo usuário.
