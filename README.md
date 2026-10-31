# Empório da Música — meu desafio Artefact

Construí um agente de atendimento em Python para a loja fictícia Empório da Música.
Ele consulta produtos e promoções no Supabase e recupera trechos do manual com embeddings
armazenados no pgvector. Posso conversar pelo terminal ou pelo chat local em Streamlit.

[Repositório público](https://github.com/Negritin/emporio-musica-artefact) ·
[Arquitetura](docs/arquitetura.md) · [Dados e RAG](docs/dados-e-rag.md) ·
[Avaliação](docs/avaliacao.md)

## Como executar

Uso Python 3.10 ou superior e um projeto Supabase próprio. Não incluí credenciais no Git.
O avaliador precisa de uma chave OpenRouter com saldo para os modelos e de uma conexão
PostgreSQL administrativa para preparar o banco. A aplicação usa outra identidade, de leitura.

```bash
git clone https://github.com/Negritin/emporio-musica-artefact.git
cd emporio-musica-artefact
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]' -c requirements.lock
cp .env.example .env.local
```

No Windows, ativo o ambiente com `.venv\Scripts\Activate.ps1`.

Preencho `SUPABASE_DB_URL` e `OPENROUTER_API_KEY` no `.env.local`:

| Variável | Finalidade |
|---|---|
| `SUPABASE_DB_URL` | Conexão PostgreSQL administrativa, usada somente em `prepare` |
| `ARTEFACT_APP_DB_URL` | Conexão de leitura criada pelo comando de preparação |
| `OPENROUTER_API_KEY` | Chave para geração e embeddings |
| `OPENROUTER_MODEL` | Modelo de atendimento; padrão `openai/gpt-4.1-mini` |
| `OPENROUTER_EMBEDDING_MODEL` | Padrão `openai/text-embedding-3-small`, com 1.536 dimensões |
| `MAX_RESPONSE_TOKENS` | Máximo por chamada de modelo; padrão 1.000 |
| `MAX_SESSION_TURNS` | Limite por sessão de chat/terminal; padrão 30 |

Copio a conexão em **Supabase → Connect → Session pooler** e substituo o marcador da senha.
Ela tem o formato `postgresql://USUARIO:SENHA@HOST:5432/postgres?sslmode=require`.
Codifico os caracteres reservados da senha para URL. Uso o pooler de sessão para permitir
conexões IPv4; não presumo que a conexão direta IPv6 esteja disponível.

Com o arquivo salvo, preparo o banco e verifico a carga:

```bash
emporio prepare
emporio check
```

O primeiro comando cria as tabelas em `artefact`, habilita `vector` em `extensions`, carrega
as fontes disponíveis, indexa o manual e cria o login `artefact_reader`. Gravo a conexão desse
login somente no `.env.local`. Preciso de uma conta com permissão para essas operações.
Não movo uma extensão já instalada em outro schema: nesse caso, uso um projeto compatível
ou ajusto a migração conscientemente antes de executar.

Incluí os CSVs de catálogo, categorias e promoções e o PDF necessário à reprodução.
Os arquivos individuais de clientes, pedidos e itens de pedido ficam fora do Git e são
opcionais na carga. Analisei os seis arquivos locais do desafio, mas o atendimento não usa
as três tabelas privadas. Posso apontar outra pasta com `emporio prepare --data-dir CAMINHO`.
Não preciso fornecer dados individuais ao avaliador para reproduzir o agente.
Cada execução de preparação grava seu relatório em `.local/dados-validacao.json`, fora do
Git. Os relatórios em `docs/` preservam as evidências da minha entrega.

### Conversar pelo terminal

```bash
emporio ask 'Quais violões disponíveis custam até R$1000?'
emporio ask 'Quanto custa o Yamaha C40 e quanto fica no PIX?' --json
emporio chat
```

No modo `chat`, digito `sair` para encerrar. O retorno inclui o caminho executado e as
métricas disponíveis. Em caso de falha de integração, `ask` encerra com código 1.

### Abrir o chat local

```bash
streamlit run app.py
```

Abro `http://127.0.0.1:8501`. A interface mostra as respostas e, em **Como cheguei à resposta**,
os eventos e trechos recuperados. O servidor fica ligado ao endereço local da máquina.
A solução não depende de Vercel, deploy ou link público de aplicação.

## Por que tomei estas decisões

**Framework e abordagem.** Escolhi um fluxo híbrido: consultas parametrizadas para dados
operacionais e RAG para políticas. Usei LangGraph para explicitar estado, nós e caminhos,
e LangChain com a integração oficial `ChatOpenRouter` para chamadas e saída estruturada.
Evitei SQL livre e ciclos abertos de ferramentas: o modelo propõe um plano validado por
Pydantic e Python decide quais consultas executar. Isso facilita os testes e a explicação.

**Modelo e provedor.** Usei o OpenRouter para centralizar geração e embeddings com uma chave.
Comparei `gpt-4.1-nano` e `gpt-4.1-mini` em três classificações: ambos acertaram catálogo e
política; o nano confundiu a pergunta híbrida. Mantive o mini configurável. Esse ensaio é
pequeno e não prova superioridade geral. Registrei os resultados em
[modelos-validacao.json](docs/modelos-validacao.json). Escolhi `text-embedding-3-small` e
verifiquei o vetor de 1.536 dimensões e a recuperação em português.

**Interface.** Escolhi Streamlit por permitir um chat local em Python com pouco código.
Também mantive a CLI para facilitar a reprodução e o diagnóstico. Priorizei o agente e as
instruções locais, conforme a liberdade dada pelo desafio.

**Histórico.** Não persisti conversas no banco. O histórico fica na memória da sessão do
Streamlit ou do processo da CLI. Envio ao modelo até quatro pares recentes de mensagens,
com limite de tamanho. Uma nova conversa limpa a sessão; não implementei retomada entre
execuções. Os exemplos e relatórios de avaliação foram gravados explicitamente pelo script.

**Tratamento dos dados.** Preservei IDs e fontes, converti tipos, validei relacionamentos,
duplicatas, datas e campos ausentes e mantive preços em `numeric`/`Decimal`. Não preenchi
rastreamento ou recebimento por inferência. Indexei o PDF com página, seção, hash da fonte
e modelo de embedding. Uma reexecução idêntica atualiza a carga sem duplicar as chaves e
reutiliza os vetores existentes. Não usei pandas porque o volume cabe em funções simples.

## Prompt, fontes e regras

Separei a interpretação estruturada da redação da resposta. O prompt define o tom informal
mas profissional da loja, o escopo e a obrigação de fundamentar fatos nas evidências.
Dados recuperados são conteúdo não confiável. Acrescentei um filtro para instruções
maliciosas evidentes; ele é uma defesa limitada, não uma garantia contra ataques inéditos.
A identidade do modelo não tem acesso a segredos, escrita ou consultas privadas.

Calculei preços e a não cumulatividade de PIX e promoção em Python. Para os conflitos
conhecidos do manual, preservei as duas regras em respostas controladas, condicionadas à
presença das fontes recuperadas. Explico os detalhes em [dados-e-rag.md](docs/dados-e-rag.md).
As fontes citadas são o manual fornecido, não um parecer jurídico independente.

## Suposições e limites que documentei

- Os CSVs representam um **snapshot**. Consulto o banco em cada pergunta, mas isso não
  transforma os dados fornecidos em estoque ou preços atuais de uma loja real.
- `is_active` indica o estado fornecido das promoções; não há datas de vigência para
  confirmar uma campanha pelo calendário. Mostro original, percentual e preço promocional.
- Não implementei autenticação. Por decisão de escopo, bloqueio dados individuais de
  clientes e pedidos, inclusive status e rastreamento. Nome, e-mail ou número de pedido
  digitados no chat não comprovam identidade. O enunciado permite usar somente os dados
  necessários; mantenho as políticas gerais disponíveis.
- Não efetuo compras, reservas, devoluções ou registro real de reclamações. Oriento o
  atendimento humano sem fingir que essas ações aconteceram.
- Preservo as ambiguidades de parcelamento, contatos, frete exatamente em R$500 e
  defeito/garantia. Não escolho silenciosamente uma versão do manual.
- A busca retorna até oito produtos e não implementa paginação nem busca tolerante a todos
  os erros de digitação. Quando um item encontrado está indisponível, consulto alternativas
  ativas da mesma categoria; não afirmo equivalência técnica entre elas.
- Não calculo frete por CEP, peso ou dimensões nem prometo vigência ou prazo individual
  de entrega. Também não consulto calendários de feriados ou integrações de transportadoras.
- As respostas de um LLM podem variar. Os testes e as conversas mostram casos observados,
  não uma garantia de acerto para qualquer entrada.

## Testes e exemplos

```bash
ruff check src tests app.py evaluation/run.py
pytest -q -m 'not integration'
ARTEFACT_RUN_INTEGRATION=1 pytest -q -m integration
python evaluation/run.py
```

Os testes locais não exigem credenciais. Os de integração e a avaliação usam os serviços
reais e geram custo no OpenRouter. No PowerShell, defino a variável com
`$env:ARTEFACT_RUN_INTEGRATION='1'` antes de executar `pytest -q -m integration`.

Registrei mais de dez conversas reais em Markdown localmente e selecionei cinco para
[examples/](examples/), respeitando a quantidade pedida. O relatório completo fica em
`evaluation/local/`, ignorado pelo Git. O script grava data, commit, rota, fontes, uso e
transcrições sem editar as respostas. Os resultados finais estão em
[docs/avaliacao.md](docs/avaliacao.md).
Apresento datas no formato brasileiro, `DD/MM/AAAA`, e horários no fuso de Brasília.

## Custos e falhas

Limitei cada turno a uma classificação, uma geração de resposta quando necessária e uma
chamada de embeddings quando houver busca de políticas. Respostas controladas e bloqueios
podem dispensar a geração. Não faço tentativas automáticas de modelo. Cada chamada tem
timeout de 40 segundos, a mensagem tem até 2.000 caracteres e a sessão tem limite de turnos.
Consultas SQL têm timeout de sete segundos e não executam instruções propostas pelo modelo.

Mostro tokens e custos somente quando o provedor os informa. O somatório pode ser parcial;
não substitui a cobrança da conta nem garante um teto de gastos. Limites de sessão podem
ser reiniciados pelo próprio usuário local. Em falhas, preservo um erro compreensível sem
mostrar credenciais ou detalhes de conexão.

## O que eu faria com mais tempo

Implementaria autenticação e autorização por cliente antes de liberar pedidos; ampliaria
os testes de qualidade e ataques adversariais; mediria recuperação, latência e custo em um
conjunto maior; melhoraria busca e paginação e resolveria as ambiguidades com a loja.
Também incluiria integração real de atendimento somente com confirmação de execução.

## Como utilizei IA no desenvolvimento

Usei o Codex para ler o enunciado e o manual, comparar as exigências, organizar as etapas
do desenvolvimento e auxiliar na implementação, revisão e testes. Defini o escopo e ajustei as
decisões durante a conversa, incluindo a retirada da hospedagem e a restrição de pedidos.

Não tratei o código sugerido como validação. Executei os comandos, comparei respostas
reais com as fontes e corrigi problemas encontrados: classificação de PIX, recuperação
de contatos, conflitos de políticas e uma instrução maliciosa em conteúdo recuperado.
Registrei esses limites para conseguir explicar o raciocínio e reproduzir os resultados.

## Referências técnicas

Consultei a documentação primária de [LangGraph](https://docs.langchain.com/oss/python/langgraph/graph-api),
[ChatOpenRouter](https://docs.langchain.com/oss/python/integrations/chat/openrouter),
[embeddings do OpenRouter](https://openrouter.ai/docs/api/api-reference/embeddings/submit-an-embedding-request)
e [pgvector no Supabase](https://supabase.com/docs/guides/database/extensions/pgvector).
