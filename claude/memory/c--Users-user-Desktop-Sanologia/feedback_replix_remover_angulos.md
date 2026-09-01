---
name: Replix — remover feature de ângulos sugeridos
description: User decidiu tirar a etapa de seleção de ângulos do pipeline Replix; só usar o original do briefing
type: feedback
originSessionId: c382f367-09fc-4bfb-9c5b-c999fb76785d
---
Remover feature de "Ângulos sugeridos" do pipeline Replix. Só rodar com o ângulo "original" (gerado direto do briefing/headline).

**Why:** User reportou recorrentemente que ângulos "estão dando maior B.O." — pipeline cai/trava na geração de ângulo, ângulos alternativos confundem mais que ajudam, e ele sempre escolhe o original na prática. Decisão tomada em 2026-05-06 enquanto finalizava um pipeline EaseFlow (próstata) — UI ainda mostrava cards de ângulos alternativos que ele ignorou.

**How to apply:** Quando for mexer no Replix (`_Projetos/replix/`):
1. Esconder/remover o card "Ângulos sugeridos (clique pra escolher)" do `index.html`
2. No fluxo, pular direto da etapa Briefing pra Copy/Render usando ângulo sintético do `headline_original`
3. Não remover os endpoints backend (deixar dormindo) — só esconder na UI por enquanto, pra reverter fácil se mudar de ideia
4. NÃO mexer agora — user disse "vou finalizar aqui, só para deixar registrado". Aplicar quando ele pedir explicitamente.
