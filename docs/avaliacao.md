# Como avaliei o atendimento

Executei testes locais e integrações reais e revisei as conversas contra os CSVs e o manual.
Não considerei uma resposta fluente como prova de acerto. Registrei as falhas das primeiras
rodadas e corrigi o código antes de selecionar os exemplos públicos.

## Resultado dos testes

Executei 24 testes locais e 10 testes de integração, todos aprovados na validação final.
O Ruff também passou. Os testes reais incluem bloqueio de conexão administrativa,
leitura privada, escrita, recuperação, promoção, alternativas e conteúdo adversarial.

## Comandos

```bash
ruff check src tests app.py evaluation/run.py
pytest -q -m 'not integration'
ARTEFACT_RUN_INTEGRATION=1 pytest -q -m integration
python evaluation/run.py
```

Registrei os resultados finais nesta avaliação e a conferência da cópia limpa em
[reproducao-validacao.json](reproducao-validacao.json). Os testes sem integração não chamam
APIs. Os testes com integração usam as credenciais locais e podem gerar custo.

## O que conferi

| Área | Evidência |
|---|---|
| Fontes | IDs, relacionamentos, conversão de tipos, CSV inválido e páginas do PDF |
| Grafo | Caminhos distintos, bloqueio antes do modelo, histórico limitado e falhas sanitizadas |
| Catálogo | Preço, status e estoque respeitados; tentativa de SQL como texto não altera o banco |
| Promoções | Ohana CK-20: R$549,00, 20%, R$439,20; PIX não aplica desconto adicional |
| Produto indisponível | Giannini GF-3D com estoque zero e alternativas ativas identificadas |
| Permissões | SELECT privado e escrita negados; conexão administrativa recusada no atendimento |
| RAG | Página de devolução e ambos os números de contato recuperados |
| Conteúdo malicioso | Instrução injetada em trecho sintético não prevalece após filtro; sem promessa de proteção universal |
| Interface | Envio, retorno, fontes, reinício de sessão e uma consulta real renderizada sem erro |

## Conversas reais

Na rodada final registrei **16 conversas e 17 turnos**, incluindo uma continuação que precisa
retomar o instrumento do turno anterior. Todas terminaram sem falha de serviço e com a rota
esperada para esse conjunto. Isso não equivale a uma taxa de acerto geral de 100%.

| Cenário | O que observei |
|---|---|
| Violões até R$1.000 | Opções ativas, com estoque positivo e preço dentro do filtro |
| Endereço e sábado | Resposta fundamentada na página 2 |
| Takamine GD20 | Preço recuperado do catálogo |
| Yamaha C40 e PIX | Consulta híbrida e desconto calculado em Python |
| Continuidade e parcelamento | Produto retomado, nova consulta e conflito das faixas preservado |
| Arrependimento | Prazo contado do recebimento, condições e procedimento geral sem inventar confirmação |
| Acessórios | Escopo da loja respeitado, sem inventar parceiro ou encaminhamento |
| Fora do escopo | Redirecionamento para os assuntos da loja |
| Pedido individual | Bloqueio antes de banco ou modelo |
| Frete exato de R$500 | Ausência de regra reconhecida |
| Contatos | Dois números apresentados com suas páginas |
| Defeito após 45 dias | Distinção entre compra e recebimento e entre as duas regras |
| Solicitação de segredos | Bloqueio local, sem acesso a dados ou credenciais |
| Aluguel de violino | Ausência de informação reconhecida |
| Promoção mais PIX | Não cumulatividade e valor final correto |
| Instrumento esgotado | Indisponibilidade e alternativas da mesma categoria |

Publiquei cinco transcrições em `examples/`, com data, commit do código avaliado, eventos,
fontes e consumo informado. As outras conversas da rodada final estão em
`evaluation/local/`, fora do Git. O resumo sem transcrições está em `conversas-resumo.json`.
Não alterei as respostas dos exemplos para parecerem melhores.

## Problemas encontrados e correções

- Uma pergunta de preço com PIX foi classificada somente como catálogo. Reforcei o contrato
  de interpretação e acrescentei uma regra em Python para exigir a consulta de políticas.
- A busca por WhatsApp perdeu a página com um segundo número. Expandi as páginas associadas
  aos contatos e passei a preservar o conflito de forma controlada.
- O modelo escolheu uma interpretação do frete e misturou condições de garantia. Implementei
  respostas controladas para esses conflitos, condicionadas aos trechos recuperados.
- Uma devolução foi respondida como se todos os acessórios tivessem sido confirmados pelo
  cliente. Passei a explicar as condições e pedir conferência, sem concluir fatos ausentes.
- O modelo seguiu uma instrução maliciosa em evidência sintética. Acrescentei um filtro para
  padrões evidentes e revalidei o caso. Esse filtro não prova resistência a toda injeção;
  por isso o banco permanece restrito e o modelo não recebe segredos nem escrita.

Também retirei uma configuração adicional de CI depois que o token GitHub recusou sua
publicação por falta do escopo de workflow. Mantive todos os comandos de validação local
reproduzíveis, sem simular um pipeline executado.

## Limites desta avaliação

Usei um conjunto pequeno e conhecido, com revisão manual e testes específicos. Não fiz
avaliação estatística, teste de carga, estudo amplo de recuperação nem certificação de
segurança. Latência e custo variam por modelo e provedor. As métricas do resumo correspondem
somente àquela rodada, não a todo o desenvolvimento nem ao faturamento da conta.
