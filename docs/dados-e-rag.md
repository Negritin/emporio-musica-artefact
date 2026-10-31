# Como preparei os dados e as políticas

## CSVs e banco

Usei os arquivos fornecidos como fonte da carga, preservando os originais. A validação
confere IDs duplicados, relacionamentos, tipos numéricos e datas, JSON de especificações,
valores de ativação e campos vazios. As restrições SQL complementam a validação de preços,
quantidades e estados. O relatório sanitizado está em `dados-validacao.json`.

No ambiente de desenvolvimento carreguei 9 categorias, 65 produtos, 25 promoções,
50 clientes, 20 pedidos e 22 itens. Na cópia pública, excluí as três fontes individuais;
essa decisão não impede reproduzir o atendimento. A carga aceita sua ausência e mantém
essas tabelas indisponíveis à identidade da aplicação.

Mantive rastreamento, previsão e observações ausentes como NULL. Não inferi recebimento,
não reconciliei vendas históricas com o preço atual do catálogo e não alterei totais para
forçar correspondência. A aplicação não usa os pedidos para decidir devoluções.

Carrego com upsert por chave. Não removo linhas históricas apenas por faltarem no arquivo
reimportado. Portanto, para reproduzir exatamente um snapshot diferente, é necessário
planejar a substituição dos dados; não apresento o upsert como sincronização com uma loja.

Criei `artefact_reader` com SELECT somente em categorias, produtos, promoções e trechos
do manual. A aplicação verifica a identidade da conexão e usa transações de leitura.
Neguei acesso às tabelas individuais e testei tentativas reais de leitura e escrita.
As migrações se limitam ao schema do projeto e à instalação necessária da extensão vector;
não alterei os dados dos outros projetos. Conferi que a identidade não tem leitura de
tabelas de dados em outros schemas.

Consulto nomes, categoria, status, estoque e preço com parâmetros. Ordeno por preço final
e retorno até oito itens. Para um modelo encontrado como indisponível, busco até três
alternativas ativas da mesma categoria, identificadas como alternativas. Não afirmo que
uma opção de nylon seja tecnicamente equivalente a um modelo de aço.

Calculo descontos com `numeric` no SQL e `Decimal` em Python. Promoções não acumulam com
PIX. Caso haja mais de uma promoção ativa para um produto, a consulta escolhe a maior,
sem somá-las; não observei esse conflito nas quatro promoções ativas fornecidas. Essa é
uma suposição de implementação, não uma regra adicional comprovada pelo manual.

## PDF e pgvector

Extraí as oito páginas com pypdf, normalizei espaços e gerei 13 trechos com sobreposição.
Preservei número de página, título aproximado da seção, hash SHA-256 da fonte, identificador
do trecho e modelo de embedding. Títulos de seção são auxiliares: a página é a referência
principal. Não reescrevi o conteúdo para esconder divergências.

Usei `openai/text-embedding-3-small` via OpenRouter, com 1.536 dimensões. A coluna no
pgvector tem essa mesma dimensão. Na pergunta, gero o vetor da consulta e ordeno os
trechos por distância de cosseno. Não preciso abrir o PDF nem os CSVs em cada atendimento.

Para esse manual pequeno, usei busca exata, sem índice ANN. A partir das páginas mais
próximas, expando páginas relacionadas: pagamento com promoções, defeito com garantia e
contatos das páginas 1, 2 e 6. Isso evita perder condições que aparecem em outro lugar.
Os testes verificam recuperação e contexto; não medi precisão/recall em um corpus amplo.

Não defini um limiar universal de similaridade. A ausência de informação continua sendo
um caso de avaliação da resposta, com risco residual de erro do modelo. Para conflitos
conhecidos e regras sensíveis de devolução, uso respostas controladas quando as fontes
necessárias estão presentes. Ao mudar o manual, essas regras precisam ser revisadas.

Reuso embeddings quando hash e modelo não mudaram. Para alterar o modelo, reindexo;
a dimensão permanece fixa em 1.536 nesta versão. A troca para um modelo de outra dimensão
exige uma migração deliberada. Após uma nova fonte ser indexada, retiro os trechos da
versão anterior desse manual em uma transação.

## Ambiguidades que preservei

| Tema | Evidência | Como respondo |
|---|---|---|
| Parcelamento | Tabela e seção 3.1, página 3 | Apresento mínimo geral de R$100 e faixas específicas; peço confirmação |
| Frete exatamente R$500 | Acima/abaixo, página 4 | Informo que o valor exato não foi esclarecido |
| Contatos | Páginas 1–2 e 6 | Mostro os dois números com as páginas, sem escolher um arbitrariamente |
| Defeito e garantia | Páginas 4 e 7 | Distingo 30 dias após compra de 90 após recebimento e oriento confirmação |
| Devolução | Página 4 | Explico regras gerais sem afirmar que o cliente confirmou fatos não informados |

O calendário de campanhas não comprova uma promoção individual ativa. `is_active` pertence
ao snapshot e não tem datas de vigência. Também não invento cotação de frete por CEP ou
dados de entrega ausentes.
