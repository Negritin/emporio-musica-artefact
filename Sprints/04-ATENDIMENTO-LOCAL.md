# Sprint SDD 04 — Atendimento local e fluxo visível

**Status:** concluída · **Responsável:** Cleverson Madruga · **Dependências:** Sprint 03 e versão local inicial funcional.

## Objetivo

Disponibilizar uma interface local simples para conversar com o agente, visualizar fontes e compreender o fluxo executado, sem depender de hospedagem pública.

## Critérios de aceite

- [x] Interface local simples permite enviar mensagens, acompanhar o processamento, ler respostas e compreender erros; a escolha de CLI, API ou interface local é justificada no README.
- [x] Fontes e páginas utilizadas e etapas efetivamente executadas podem ser consultadas; por padrão, o fluxo é exibido ao final da resposta.
- [x] Duração e métricas disponíveis são identificadas com honestidade; tokens e custos ausentes são indicados como não informados.
- [x] Credenciais não aparecem na interface nem nos logs; o agente usa a identidade de leitura limitada validada na Sprint 02 e não consulta dados individuais de clientes ou pedidos sem autenticação e autorização.
- [x] A execução local e suas dependências são documentadas e verificadas em ambiente limpo; limites de chamadas e tratamento de falhas são testados.

## Implementação planejada

Integrar a interface local ao agente e aos eventos reais. Priorizar simplicidade, facilidade de explicação e reprodução. Não criar hospedagem nem deploy para o desafio.

## Validação planejada

Executar a interface seguindo o README, testar perguntas de catálogo e políticas, verificar fontes e fluxo, simular falha e verificar bloqueio de dados individuais e ausência de segredos na saída.

## Evidências previstas

Comandos de execução, testes, capturas ou transcrições sanitizadas e commit real. Sugestão: `Preparei o atendimento local e a visualização do fluxo`.

## Resultado

Entreguei a CLI e o chat Streamlit local com fontes, eventos reais, tokens e custos informados. Validei o envio de mensagem, o bloqueio de pedido individual e o reinício de sessão com AppTest. Também executei uma consulta real de endereço no chat: renderizei duas mensagens sem exceção. O endpoint local de saúde respondeu HTTP 200. Não há dependência de hospedagem.

**Validação encerrada:** 2026-10-31T20:14:14-03:00.

## Evidência intermediária

Criei o chat local em Streamlit, com histórico por sessão, fontes recuperadas e eventos reais. Validei o envio de pedido individual e a limpeza da conversa com o AppTest. O servidor local respondeu HTTP 200 em `/_stcore/health`.
