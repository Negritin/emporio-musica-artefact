# Sprint SDD 04 — Atendimento local e fluxo visível

**Status:** em validação · **Responsável:** Cleverson Madruga · **Dependências:** Sprint 03 e versão local inicial funcional.

## Objetivo

Disponibilizar uma interface local simples para conversar com o agente, visualizar fontes e compreender o fluxo executado, sem depender de hospedagem pública.

## Critérios de aceite

- [ ] Interface local simples permite enviar mensagens, acompanhar o processamento, ler respostas e compreender erros; a escolha de CLI, API ou interface local é justificada no README.
- [ ] Fontes e páginas utilizadas e etapas efetivamente executadas podem ser consultadas; por padrão, o fluxo é exibido ao final da resposta.
- [ ] Duração e métricas disponíveis são identificadas com honestidade; tokens e custos ausentes são indicados como não informados.
- [ ] Credenciais não aparecem na interface nem nos logs; o agente usa a identidade de leitura limitada validada na Sprint 02 e não consulta dados individuais de clientes ou pedidos sem autenticação e autorização.
- [ ] A execução local e suas dependências são documentadas e verificadas em ambiente limpo; limites de chamadas e tratamento de falhas são testados.

## Implementação planejada

Integrar a interface local ao agente e aos eventos reais. Priorizar simplicidade, facilidade de explicação e reprodução. Não criar hospedagem nem deploy para o desafio.

## Validação planejada

Executar a interface seguindo o README, testar perguntas de catálogo e políticas, verificar fontes e fluxo, simular falha e verificar bloqueio de dados individuais e ausência de segredos na saída.

## Evidências previstas

Comandos de execução, testes, capturas ou transcrições sanitizadas e commit real. Sugestão: `Preparei o atendimento local e a visualização do fluxo`.

## Resultado

Pendente de implementação e validação. Registrar em primeira pessoa os resultados e evidências reais.

## Evidência intermediária

Criei o chat local em Streamlit, com histórico por sessão, fontes recuperadas e eventos reais. Validei o envio de pedido individual e a limpeza da conversa com o AppTest. O servidor local respondeu HTTP 200 em `/_stcore/health`.
