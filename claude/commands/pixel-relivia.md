# Pixel Relívia — Inserir no HTML

O pixel oficial da Relívia é **1853242508916971**.

O usuário vai fornecer o caminho de um arquivo HTML.

Insira o código abaixo dentro do `<head>`, logo após o último `<link>` e antes de qualquer `<style>` ou `</head>`:

```html
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1853242508916971');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1853242508916971&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
```

**Regras:**
- Se já existir um pixel antigo (qualquer `fbq('init', ...)`) no arquivo, **substitua** pelo novo — não duplique
- Se não existir nenhum pixel, **insira** após o último `<link>` no `<head>`
- Confirme ao usuário qual ação foi feita (inserido ou substituído) e qual ID foi removido caso tenha substituído
