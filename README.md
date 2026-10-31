# Empório da Música — desafio Artefact

Estou construindo um agente de atendimento em Python que consulta o catálogo no Supabase
e recupera as políticas da loja com embeddings e pgvector. Organizei o trabalho em
[cinco Sprints SDD](Sprints/00-PROJETO-SDD-ARTEFACT.md), com commits progressivos e
validação das entregas.

## Execução local

Uso Python 3.10 ou superior. Para preparar as dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
cp .env.example .env.local
```

Preencho o arquivo local com minha chave OpenRouter e as conexões do meu próprio banco.
O arquivo `.env.local` fica fora do Git. Os comandos de preparação dos dados e atendimento
serão incluídos conforme a implementação e os testes reais.

## Decisões iniciais

Escolhi LangGraph para tornar explícito o caminho de cada atendimento, LangChain para
integrar o modelo do OpenRouter e PostgreSQL para consultas controladas ao catálogo.
Vou extrair o PDF em trechos com páginas e armazenar embeddings no pgvector.

A interface será local. Clientes e pedidos não poderão ser consultados sem autenticação
e autorização; a primeira versão não implementará esse acesso. Os dados representam
o snapshot fornecido no desafio.

## Uso de IA

Usei o Codex para analisar o enunciado e o manual, estruturar as sprints e auxiliar na
implementação e revisão. Vou documentar os testes, decisões e limitações efetivamente
observados; não considero uma sugestão do assistente como evidência de funcionamento.
