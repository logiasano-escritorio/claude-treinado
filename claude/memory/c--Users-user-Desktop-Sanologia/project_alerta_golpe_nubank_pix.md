---
name: alerta-golpe-nubank-pix-cnpj-sano
description: "Nubank marca CNPJ recebedor da Sano (na Pagar.me) como golpe no PIX; é antifraude do banco, NÃO é bug de site — resolve com Nubank/Pagar.me, não com HTML"
metadata: 
  node_type: memory
  type: project
  originSessionId: 01183009-1ebc-40a7-aa0c-ee10a28060a5
---

**Sintoma (relatado 2026-07-06):** cliente vai pagar por PIX no checkout Yampi e o app do **Nubank mostra alerta de G.O.L.P.E** sobre o CNPJ recebedor da Sano. Derruba conversão forte. Recebedor = CNPJ da Sano cadastrado na **Pagar.me** (adquirente que a Yampi usa).

**Causa (NÃO é código):** desde fim de 2023 o BACEN permite bancos marcarem CPF/CNPJ/chave PIX com aviso de possível golpe. O antifraude do Nubank dispara o pop-up cruzando:
- denúncias de clientes contra aquela chave/CNPJ (mesmo poucas e indevidas)
- modelos de comportamento transacional "fora do comum" (pico de muitos PIX de valores parecidos de gente sem relação prévia = padrão de e-commerce novo, que o modelo confunde com golpe)
- base BACEN + base interna Nubank

Nenhuma edição de HTML/checkout/link resolve. O alerta é do lado do PAGADOR (app Nubank), atrelado ao RECEBEDOR (chave PIX Sano na Pagar.me).

**Plano de resolução (fora do código):**
1. **Nubank empresarial** — abrir chamado pelos canais oficiais informando o CNPJ da empresa e pedindo revisão do alerta indevido; eles fazem análise e removem se legítimo. Reclame Aqui também funciona como canal (Nubank responde pedindo CNPJ pra analisar). Prazo: dias.
2. **Pagar.me/Yampi (adquirente)** — abrir ticket: a chave PIX pode estar com reputação ruim no arranjo; pedir pra verificarem/rotacionarem a chave recebedora ou o subadquirente. Às vezes a chave é da Pagar.me (não da Sano direto) e o problema é reputação agregada do recebedor intermediário.
3. **Reduzir denúncias na origem** — cliente que não reconhece o nome no extrato denuncia. Garantir que o **nome que aparece na fatura/PIX (soft descriptor)** seja reconhecível ("SANO" / nome do produto), não uma razão social estranha. Configurável na Pagar.me/Yampi.
4. **MED** — se golpe real acontecer, devolução via Mecanismo Especial de Devolução (não é o caso aqui, é alerta indevido).

**Reabrir/reverificar antes de agir:** confirmar com Guilherme se a chave PIX recebedora é CNPJ Sano direto ou chave da Pagar.me; e qual soft descriptor aparece hoje na fatura do cliente.

Relacionado: [[reference_sano_dominio]] (checkout Yampi sano-suplementos.pay.yampi.com.br), [[reference_arquitetura_tracking_gtm_yampi]].
