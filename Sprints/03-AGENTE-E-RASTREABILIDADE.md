# Sprint SDD 03 — Agente fundamentado e fluxo rastreável

**Status:** concluída · **Responsável:** Cleverson Madruga · **Dependências:** Sprints 01 e 02; modelo e ferramenta de embeddings validados.

## Objetivo

Construir um agente Python que resolva perguntas de catálogo e políticas com evidências, registre o caminho executado e responda com os limites da informação disponível.

## Critérios de aceite

- [x] LangGraph possui estado e nós explícitos para interpretar, consultar dados, buscar políticas, responder e tratar falhas ou fora de escopo, usando apenas as etapas necessárias.
- [x] Modelo OpenRouter configurável responde em português com tom cordial da loja; histórico e chamadas são limitados, e erros não expõem segredos.
- [x] Perguntas de catálogo, políticas e híbridas usam fontes adequadas; valores de promoção e PIX seguem a regra de não acumulação e mostram preço original e desconto quando aplicável.
- [x] Resposta distingue snapshot de informação atual; informa página do manual quando usada e reconhece dúvidas, ausência e conflitos de evidência.
- [x] Consultas individuais de clientes e pedidos, incluindo status e rastreio, são bloqueadas sem autenticação e autorização, inclusive em perguntas híbridas; o agente orienta o atendimento apropriado e não inventa informações.
- [x] Conteúdo externo é tratado como dado não confiável e tentativas de instrução maliciosa são testadas; filtros e consultas são validados em Python, sem SQL livre executado pelo modelo. O bloqueio de dados individuais é aplicado no backend e nas permissões do banco, sem depender apenas do modelo.
- [x] O projeto oferece uma forma local funcional de conversar com o agente, documentada e testada sem depender de hospedagem.
- [x] Eventos representam etapas efetivamente executadas, com duração e erros sanitizados; tokens e custos aparecem apenas quando informados ou identificados como estimativas documentadas.
- [x] Há testes dos caminhos normais e adversos, incluindo indisponibilidade do modelo/banco e limites por turno.
- [x] O atendimento considera o escopo do manual para instrumentos e acessórios, não inventa parceiros e não afirma ter registrado ou encaminhado reclamações sem ferramenta que realmente execute a ação.
- [x] Código do grafo e ferramentas é legível, com nomes claros, funções de responsabilidade definida e complexidade justificável em entrevista.

## Implementação planejada

Compor nós pequenos e interfaces de ferramentas controladas; incluir estado mínimo de conversa, política de privacidade e mecanismo de observabilidade por eventos. Implementar operações sem efeitos externos de pedido. Aplicar limites de histórico, chamadas e respostas; não inventar dados nem ações de atendimento.

## Validação planejada

Executar testes unitários e de integração adequados e uma bateria real de perguntas de catálogo, políticas, híbridas, ambíguas, fora de escopo e sobre pedidos; testar instrução maliciosa em conteúdo recuperado. Comparar eventos e fontes com o fluxo percorrido e conferir tratamento de erros e métricas ausentes.

## Evidências previstas

Código do grafo, testes, resultados sanitizados e transcrições de teste sem exposição de dados individuais. Commit sugerido: `Implementei o agente e registrei o fluxo executado`.

## Resultado

Implementei o grafo e validei suas rotas, o contexto de continuação, a fundamentação, a não cumulatividade de descontos e os bloqueios. Corrigi as falhas encontradas nas rodadas iniciais. Na rodada final, executei 16 conversas e 17 turnos sem falha de serviço e com as rotas esperadas. Os 24 testes locais e 10 testes reais de integração passaram. Documentei as limitações de injeção de instruções e preservei as evidências das conversas em evaluation/local/.

**Validação encerrada:** 2026-10-31T20:14:14-03:00.

## Evidência intermediária

Implementei o grafo com validação, interpretação, catálogo, políticas e resposta. Validei a primeira consulta real de violões e corrigi a oferta de PIX sem recuperação da política no turno. No teste de seleção, o modelo mini classificou corretamente três rotas; o nano confundiu a pergunta híbrida. Mantive o mini configurável e iniciei a avaliação das conversas reais.
