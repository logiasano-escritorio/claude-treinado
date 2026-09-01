---
name: upsell-whatsapp-p-s-compra-sano-back-end-ltv
description: Estratégia de upsell pós-compra via WhatsApp (Reportana) — oferta de +unidades por R$199 com PDF de proposta e bônus de protocolo
metadata: 
  node_type: memory
  type: project
  originSessionId: e5c492e8-6e6c-4ca5-aded-b576bcf39982
---

Operação Sano roda recuperação/back-end via **Reportana** (API oficial WhatsApp conectada em jun/2026). Estratégia central de LTV: **upsell pós-compra na janela de 24h**.

**A mecânica que funciona (validada ao vivo jun/2026):**
- Cliente compra → mensagem "Pedido pago" termina com gancho: "O resultado vem de quem usa de forma contínua. Quer que eu te mostre como completar seu tratamento?"
- Cliente responde "Sim" → abre janela 24h → manda oferta de upsell (idealmente por **áudio**, converte mais).
- **Oferta:** mais unidades pelo MESMO valor da 1ª compra (ex: comprou 1 a R$199 → +2 por R$199 = tratamento 3 meses; comprou 3 → +3 por R$199 = manutenção 6 meses).

**A oferta irresistível (estilo Hormozi — empilhar valor, não baixar preço):**
Não vende "+X potes". Vende um **Protocolo/Programa de tratamento** com bônus de custo marginal zero:
- +unidades (fase de tratamento ou manutenção)
- Guia "X Dias Sem Dor" (PDF, protocolo dia a dia)
- Rotina de exercícios POR REGIÃO de dor (lombar/joelho/pés)
- Guia de alimentação anti-inflamatória
- Acompanhamento no WhatsApp durante o tratamento (= desculpa pra ficar no zap = mais back-end)
- Check-in de progresso a cada 30 dias (dor 0-10)
- Valor ancorado ~R$906 → preço R$199 + garantia 90 dias

**SEMPRE perguntar a região da dor ANTES e personalizar o PDF inteiro pra ela.** Cliente lombar = PDF 100% lombar, zero menção a outras regiões. Personalização total dispara conversão.

**Template de proposta em HTML→PDF:** `Sanologia/_propostas/proposta-prime-lombar-180-dias.html` (5 páginas: capa / por que 6 meses / entregáveis robustos com ícones SVG / oferta+garantia). Identidade Sano: navy #1e3a8a + Montserrat/Georgia. Entregáveis = blocos GRANDES com card+ícone+"o que tem dentro" (não bullets curtos). Gerar PDF: Ctrl+P → Salvar como PDF → margens nenhuma.

**Matemática que justifica priorizar isso:** 150 pedidos/dia × 30% conversão upsell × R$170 lucro/upsell = **R$229.500/mês** de lucro incremental (sem novo CAC). Empilhando recompra dia-25 + cross-sell magnésio → ~R$398k/mês. Cada +1% de conversão = +R$7.650/mês. Back-end é a maior alavanca de lucro da operação.

**Variante "vídeo Dra." (jun/2026):** upsell pós-compra Prime entregue como vídeo de uma doutora falante (ElevenLabs voz + DreamFace lip-sync, ~3min, NÃO Veo3). Roteiro adaptado de VSL de infoproduto espanhol "Protocolo dos 4 Ingredientes" (em `Downloads/...Título.docx`). **Mecanismo único reaproveitado:** "molécula da dor" (estudo Karolinska/Suécia) corrói a mielina dos nervos → ativa-se uma "vitamina amarela" (PEA/palmitoiletanolamida) via 4 ingredientes caseiros + microbiota → desativa a inflamação por dentro. Ponte com o físico: **Prime age por fora, protocolo desativa a causa por dentro.** Oferta final do vídeo: **3× Prime Creme + Protocolo (PDF/vídeo) + 3 bônus por R$199** (ancorado ~R$596). PDF do infoproduto + bônus ainda a gerar. Roteiro de locução: SEM marcações de [pausa]/direção no meio do texto — só o texto corrido (user detesta).

Relacionado: [[reference_oferta_padrao_sano]] (oferta padrão front-end 4 tiers), [[reference_workflow_avatares_ugc]], [[reference_veo3_product_lock]].
