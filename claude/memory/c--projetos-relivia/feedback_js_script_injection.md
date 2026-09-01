---
name: JS — Injeção de Script em HTML: dois bugs recorrentes
description: Dois bugs que quebram galeria e variant picker em clones ao injetar JS — script duplo e DOMContentLoaded tardio. Nunca repetir.
type: feedback
originSessionId: b24458c5-c7de-4a26-a4d7-22e9a63b7a7b
---

**Sintoma:** galeria não troca imagens ao clicar nas setas, variant picker não alterna entre cards — zero interatividade, zero erro no console.

## Bug 1 — Tag `<script>` duplicada ao substituir bloco JS por slicing

Ao substituir um bloco JS usando `content[start:end]`, a posição `start` foi definida pelo início do comentário `/* ===... */` — que estava **dentro** de um `<script>` já aberto. O `content[:start]` terminava com `<script>\n`, e o `new_js` que foi inserido começava com `<script>\n/* ...`. Resultado: `<script>\n<script>\n/* ...` — dois `<script>` abrindo, o segundo ignorado, o código inteiro quebrado silenciosamente.

**Why:** O browser trata o segundo `<script>` como texto literal dentro do primeiro. Nenhum erro visível no HTML, mas o JS nunca executa.

**How to apply:** Ao fazer slicing para substituir um bloco JS, **sempre incluir a tag `<script>` de abertura no boundary de corte**. A `start` deve apontar para o `<script>` que abre o bloco, não para o conteúdo interno. O `new_js` que substitui já contém o `<script>` — nunca deixar o antigo sobrando.

Padrão correto:
```python
# ERRADO — start aponta para dentro do <script>
start = content.find('/* meu comentário */')
# content[:start] ainda tem '<script>\n' pendurado

# CORRETO — start aponta para o <script> que abre o bloco
start = content.rfind('<script>', 0, content.find('/* meu comentário */'))
```

---

## Bug 2 — `DOMContentLoaded` não dispara quando DOM já está pronto

Script colocado no final do `<body>` usa `document.addEventListener('DOMContentLoaded', fn)`. Como o script roda depois que o parser já processou o `</body>`, o `readyState` já é `'interactive'` ou `'complete'` — o evento `DOMContentLoaded` já disparou e **nunca vai disparar de novo**. O listener é registrado, mas o callback nunca executa. A página abre sem interatividade nenhuma, sem erro no console.

**Why:** `DOMContentLoaded` só dispara uma vez, quando o parser termina. Se o script chega depois disso, o listener é inútil.

**How to apply:** Nunca usar `addEventListener('DOMContentLoaded', fn)` sozinho em scripts injetados ao final do body (nem em clones HTML estáticos). Sempre usar o padrão readyState:

```javascript
(function init() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
    return;
  }
  // DOM garantidamente pronto aqui
  var slides = document.querySelectorAll('.meu-slide');
  // ...
})();
```

Esse padrão funciona corretamente em qualquer posição do documento — no `<head>`, no meio do `<body>` ou no final.
