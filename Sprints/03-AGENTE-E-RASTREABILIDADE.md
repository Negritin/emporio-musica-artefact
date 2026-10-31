# Sprint SDD 03 — Agente fundamentado e fluxo rastreável

**Status:** em especificação · **Responsável:** Cleverson Madruga · **Dependências:** Sprints 01 e 02; modelo e ferramenta de embeddings validados.

## Objetivo

Construir um agente Python que resolva perguntas de catálogo e políticas com evidências, registre o caminho executado e responda com os limites da informação disponível.

## Critérios de aceite

- [ ] LangGraph possui estado e nós explícitos para interpretar, consultar dados, buscar políticas, responder e tratar falhas ou fora de escopo, usando apenas as etapas necessárias.
- [ ] Modelo OpenRouter configurável responde em português com tom cordial da loja; histórico e chamadas são limitados, e erros não expõem segredos.
- [ ] Perguntas de catálogo, políticas e híbridas usam fontes adequadas; valores de promoção e PIX seguem a regra de não acumulação e mostram preço original e desconto quando aplicável.
- [ ] Resposta distingue snapshot de informação atual; informa página do manual quando usada e reconhece dúvidas, ausência e conflitos de evidência.
- [ ] Consultas individuais de clientes e pedidos, incluindo status e rastreio, são bloqueadas sem autenticação e autorização, inclusive em perguntas híbridas; o agente orienta o atendimento apropriado e não inventa informações.
- [ ] Conteúdo externo é tratado como dado não confiável e tentativas de instrução maliciosa são testadas; filtros e consultas são validados em Python, sem SQL livre executado pelo modelo. O bloqueio de dados individuais é aplicado no backend e nas permissões do banco, sem depender apenas do modelo.
- [ ] O projeto oferece uma forma local funcional de conversar com o agente, documentada e testada sem depender de hospedagem.
- [ ] Eventos representam etapas efetivamente executadas, com duração e erros sanitizados; tokens e custos aparecem apenas quando informados ou identificados como estimativas documentadas.
- [ ] Há testes dos caminhos normais e adversos, incluindo indisponibilidade do modelo/banco e limites por turno.
- [ ] O atendimento considera o escopo do manual para instrumentos e acessórios, não inventa parceiros e não afirma ter registrado ou encaminhado reclamações sem ferramenta que realmente execute a ação.
- [ ] Código do grafo e ferramentas é legível, com nomes claros, funções de responsabilidade definida e complexidade justificável em entrevista.

## Implementação planejada

Compor nós pequenos e interfaces de ferramentas controladas; incluir estado mínimo de conversa, política de privacidade e mecanismo de observabilidade por eventos. Implementar operações sem efeitos externos de pedido. Aplicar limites de histórico, chamadas e respostas; não inventar dados nem ações de atendimento.

## Validação planejada

Executar testes unitários e de integração adequados e uma bateria real de perguntas de catálogo, políticas, híbridas, ambíguas, fora de escopo e sobre pedidos; testar instrução maliciosa em conteúdo recuperado. Comparar eventos e fontes com o fluxo percorrido e conferir tratamento de erros e métricas ausentes.

## Evidências previstas

Código do grafo, testes, resultados sanitizados e transcrições de teste sem exposição de dados individuais. Commit sugerido: `Implementei o agente e registrei o fluxo executado`.

## Resultado

Pendente de execução e validação. Registrar em primeira pessoa caminhos, evidências e limitações reais.
