# Sprint SDD 05 — Avaliação, documentação e entrega

**Status:** em especificação · **Responsável:** Cleverson Madruga · **Dependências:** Sprints 01 a 03 para avaliação inicial; Sprint 04 para o aceite da interface local; prazo confirmado pelo responsável, com data e horário exatos a registrar antes da entrega.

## Objetivo

Comprovar a qualidade da solução e preparar uma entrega pública fiel ao enunciado, documentada e finalizada antes do prazo.

## Critérios de aceite

- [ ] Bateria final cobre catálogo, política, pergunta híbrida, fora de escopo, ambiguidade, bloqueio de consultas individuais de clientes e pedidos sem autenticação, tentativa de instrução maliciosa, falhas e eventos, além das ambiguidades do manual sobre parcelamento, contatos, frete e garantia; erros materiais foram corrigidos e revalidados.
- [ ] README explica instalação, configuração sem credenciais, execução, testes, arquitetura, escolhas de modelo/retrieval/prompt, limitações conhecidas, o que eu faria com mais tempo, fontes, snapshot, suposições e uso de assistentes de IA no meu fluxo de trabalho, em português, primeira pessoa e linguagem natural.
- [ ] Revisão final confirma código limpo e fácil de explicar: nomes, responsabilidades e decisões são claros, sem abstrações desnecessárias.
- [ ] Avalio pelo menos dez conversas reais, variadas e sanitizadas, documentadas em Markdown no relatório local de avaliação; registro os resultados com a versão testada.
- [ ] Seleciono três a cinco conversas reais dessa avaliação para o repositório público, conforme o limite do enunciado, incluindo ao menos uma não trivial com consulta ou política. As demais ficam como evidência local de teste, fora do Git, inclusive do histórico.
- [ ] Repositório GitHub é público, seu histórico tem commits progressivos reais em português e primeira pessoa e não contém segredos, dados pessoais desnecessários; limpeza é verificada também no histórico.
- [ ] Interface local funciona seguindo o README, e seus recursos, fontes e limitações estão descritos com honestidade.
- [ ] Data e horário de entrega do e-mail foram conferidos; versão final, commit, testes, link e horário são registrados antes do prazo; nenhuma alteração após o prazo.
- [ ] Preparo a resposta ao e-mail recebido da Artefact com o link do repositório público; o envio efetivo ocorrerá somente mediante instrução explícita do usuário.

## Decisões técnicas a justificar no README

Vou explicar minhas decisões com base na implementação e nos testes reais:

1. **Framework e abordagem do agente:** por que usei LangGraph e LangChain, como organizei o fluxo e como combinei busca de políticas e consultas controladas aos dados. Vou explicar a estratégia de prompt e as alternativas relevantes consideradas.
2. **Modelo e provedor:** qual modelo usei pelo OpenRouter, por que o escolhi após os testes, como configurá-lo e quais limitações, custos e alternativas identifiquei.
3. **Interface:** por que escolhi a interface efetivamente entregue, como iniciar e usar a aplicação, e como o backend Python se conecta a ela.
4. **Histórico da conversa:** se houver persistência, vou explicar onde, por quanto tempo e como ela funciona; se não houver, vou explicar como mantenho o contexto durante a interação e por que não persisti as conversas.
5. **Tratamento dos dados:** como importei e validei os CSVs, estruturei consultas, tratei o manual e a recuperação dos trechos, protegi os dados individuais de clientes e pedidos, preservei o isolamento de outros schemas e registrei as limitações de acesso sem autenticação.

Em todos os itens vou distinguir decisão planejada de comportamento efetivamente implementado, descrever limitações e evitar afirmar testes ou resultados que não ocorreram. Vou registrar as ambiguidades relevantes, as suposições ou decisões tomadas e o motivo, inclusive quando houver decisão do responsável. Python será a linguagem principal.

## Implementação planejada

Começar a avaliação, os exemplos e o README durante a implementação; executar a avaliação final após a Sprint 04, corrigir falhas e revalidar; consolidar documentação reproduzível, pelo menos dez conversas reais de avaliação local, três a cinco exemplos públicos e relato de uso do Codex; revisar versionamento e conteúdo público; preparar links e registrar a versão final antes do limite. Separar melhorias futuras das limitações que comprometem aceite.

## Validação planejada

Reproduzir instalação em ambiente limpo; conferir cada exemplo e fonte com a execução registrada, incluindo busca por violões até R$ 1.000, endereço, preço de produto e devolução quando os dados permitirem; executar testes apropriados e verificar manualmente a interface local; revisar o histórico Git e repositório público; conferir data, horário e fuso do e-mail.

## Evidências previstas

Relatório local de avaliação em Markdown com pelo menos dez conversas, comando, data e versão; README; três a cinco exemplos públicos; commit final; link do repositório; checklist de entrega. Commit sugerido: `Documentei e validei a entrega do desafio`.

## Resultado

Pendente de execução e validação. Registrar em primeira pessoa o que foi entregue, os testes realizados, os horários reais e as limitações remanescentes.
