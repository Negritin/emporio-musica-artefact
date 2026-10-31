# Projeto SDD — Empório da Música · Desafio Artefact

**Responsável:** Cleverson Madruga  
**Situação:** em execução.  
**Prazo:** 02/11/2026 às 00:00, interpretado em `America/Sao_Paulo` conforme o fuso do responsável. Encerrar alterações antes desse horário.  
**Resultado existente:** schema `artefact` criado e confirmado no Supabase; conexão local e chave OpenRouter configuradas. A implementação foi iniciada; os resultados serão registrados nas fichas de cada sprint.

## Objetivo

Construir e apresentar um protótipo Python de atendimento textual que consulte o catálogo e as políticas da Empório da Música, documente decisões e limitações e possa ser avaliado pelo repositório público e executado localmente seguindo o README.

## Regras do processo

- Python é a única restrição técnica obrigatória do enunciado; LangGraph, OpenRouter, Supabase e interface local são decisões deste projeto; hospedagem e link público de aplicação foram retirados do escopo.
- Entregar repositório público no GitHub, README reproduzível e de três a cinco conversas reais e variadas, com pelo menos uma não trivial. Avaliar e documentar pelo menos dez conversas reais em Markdown localmente; selecionar de três a cinco para o repositório, respeitando o limite do enunciado. Manter o relatório local fora do Git e verificar arquivos rastreados e histórico.
- Usar commits reais, progressivos, em português e primeira pessoa, sem concentrar todo o trabalho em um commit nem reescrever o histórico para simular progresso.
- Respeitar prazo e fuso informados no e-mail. Não alterar o repositório após a data e o horário de entrega. Não presumir que dois dias correspondam a uma data específica.
- Justificar no README as cinco decisões indicadas no desafio: frameworks e abordagem, modelo e provedor, interface, persistência ou não do histórico e tratamento dos dados. Explicar limitações, melhorias com mais tempo e uso do Codex/IA no fluxo de trabalho. Documentar suposições e distinguir dados de snapshot de informação atual.
- O responsável confirmou que os arquivos fornecidos podem ser públicos, inclusive o manual. Revisar os arquivos e o histórico antes da publicação para não expor credenciais ou dados pessoais desnecessários; preferir anonimização ou exclusão desses dados quando aplicável.
- Credenciais administrativas servem somente à preparação e às migrações; a aplicação usará acesso de leitura com privilégios mínimos, sem acesso a clientes, pedidos ou outros schemas. O isolamento será testado no banco, não apenas no prompt.
- O responsável determinou que dados individuais de clientes e pedidos exigem autenticação. Como não há autenticação prevista na primeira versão, bloquear essas consultas, inclusive status e rastreamento; explicar a limitação no README. Eventual acesso futuro exige autenticação e autorização validadas.
- Ao encontrar ambiguidade relevante para produto, escopo ou experiência que dependa da decisão do responsável, apresentar contexto, opções e impacto para ele responder; avançar no trabalho independente. Registrar a decisão ou suposição e sua justificativa no README, sem atribuir uma decisão não tomada. Para escolhas técnicas rotineiras, tomar uma interpretação razoável e seguir, documentando-a.
- Referenciar evidências reais, sem inventar execução, tempo, custo, avaliação ou publicação.
- Escrever documentação, registros e commits em português, na primeira pessoa e com linguagem natural, direta e próxima da forma de comunicação do responsável. Separar planos de resultados concluídos.
- Manter código limpo e fácil de explicar: nomes claros, funções pequenas, responsabilidades explícitas, tratamento de erros compreensível e somente abstrações necessárias. Documentar decisões e testar comportamentos relevantes.

## Sprints

1. [Sprint SDD 01 — Fundação segura e repositório reproduzível](01-FUNDACAO-E-GIT.md).
2. [Sprint SDD 02 — Dados confiáveis e políticas consultáveis](02-DADOS-E-POLITICAS.md).
3. [Sprint SDD 03 — Agente fundamentado e fluxo rastreável](03-AGENTE-E-RASTREABILIDADE.md).
4. [Sprint SDD 04 — Atendimento local e fluxo visível](04-ATENDIMENTO-LOCAL.md).
5. [Sprint SDD 05 — Avaliação, documentação e entrega](05-AVALIACAO-E-ENTREGA.md).

## Dependências e decisões

- O responsável confirmou que estamos no prazo. Antes da entrega, registrar a data e o horário exatos do e-mail, com o fuso correspondente, sem presumir valores. Até lá, não é possível confirmar o momento de congelamento do repositório.
- Definir limites de uso e acompanhar o saldo do OpenRouter. Limites da aplicação não garantem teto absoluto de cobrança.
- Definir a exibição do grafo: ao final é a hipótese atual; acompanhamento durante a execução exige streaming e planejamento adicional.
- Comprovar acesso e limites efetivos de Supabase, OpenRouter e GitHub; não há hospedagem da aplicação no escopo.
- A senha e chaves já foram expostas na conversa: coordenar rotação e atualização dos serviços dependentes antes da publicação. Não incluir valores nem rastros nos registros.
- Testar modelos e embeddings com base em português, compatibilidade, custo e latência; não pressupor provedor, dimensão ou capacidades.

## Sequência e gestão

Executar as Sprints 01 a 03 com testes e README básico desde o início. Antes da Sprint 04, preparar uma versão local reproduzível, avaliação inicial e rascunho das conversas da Sprint 05; depois validar a interface local e concluir a avaliação e o README na Sprint 05. O período de dois dias é referência do planejamento, não garantia. Em caso de atraso, priorizar os entregáveis do desafio e registrar qualquer item do plano não concluído; registrar apenas resultados comprovados.

Status SDD: `backlog → em especificação → pronto para executar → em execução → em validação → ajustes → em validação → concluída`. Uma sprint só será concluída após passar em todos os critérios, com evidências. Registros de execução, duração e resultados serão preenchidos com dados reais, em primeira pessoa.

## Critério de conclusão

As cinco sprints obrigatórias têm aceite comprovado; a aplicação funciona localmente seguindo o README; o repositório público contém instruções e exemplos exigidos, sem segredos ou dados pessoais desnecessários; o prazo foi respeitado. Preparar resposta ao e-mail da Artefact com o link do repositório; o envio requer instrução explícita do usuário.

## Evidências e linha do tempo

- Planejamento: este documento e as fichas das sprints.
- Schema `artefact`: criação e consulta verificadas nesta sessão; registrar evidência reproduzível sem credenciais na execução.
- Início, fim, duração, commits, testes, links e demais marcos: preencher durante a execução com dados reais.

## Execução iniciada

Iniciei a implementação em 2026-10-31T19:50:08-03:00. Registrei o prazo informado pelo responsável. As chamadas POST ao OpenRouter estão retornando 401; mantive a validação real pendente enquanto avanço no código.
