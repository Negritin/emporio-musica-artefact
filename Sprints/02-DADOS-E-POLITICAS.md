# Sprint SDD 02 — Dados confiáveis e políticas consultáveis

**Status:** em especificação · **Responsável:** Cleverson Madruga · **Dependências:** Sprint 01; schema existente; arquivos locais; decisão sobre embeddings; publicação das fontes autorizada pelo responsável.

## Objetivo

Preparar dados operacionais e políticas de forma reproduzível para consultas fundamentadas, limitando a exposição de informações pessoais.

## Critérios de aceite

- [ ] Importação registra contagens, tipos, nulos, duplicatas, relacionamentos e inconsistências dos seis CSVs; preserva identificadores e não altera dados de outros schemas. Os CSVs são usados na carga; o agente consulta o Supabase em execução, sem lê-los a cada pergunta.
- [ ] Migrações e carga para `artefact` são reproduzíveis e seu comportamento em reexecução é documentado e verificado; clientes e pedidos individuais não ficam disponíveis ao agente público sem autenticação e autorização.
- [ ] Consultas de catálogo e promoções são parametrizadas, restritas a campos necessários e somente leitura; cobrem categoria, preço, status e estoque.
- [ ] A aplicação usa uma identidade de banco com permissões mínimas de leitura apenas para os objetos necessários; não usa credencial administrativa, service role nem acesso a clientes, pedidos ou outros schemas. Migrações e cargas usam uma conexão separada e restrita ao ambiente de preparação.
- [ ] Testes com a identidade da aplicação verificam tanto o acesso permitido quanto a negação efetiva a tabelas de clientes, pedidos, outros schemas e operações de escrita; registrar eventuais limitações de permissões do provedor.
- [ ] Valores representam o snapshot fornecido; `is_active` não comprova vigência por data e produtos indisponíveis ou descontinuados não são anunciados como disponíveis.
- [ ] Manual extraído e segmentado por página e seção; gerar embeddings e armazená-los no pgvector do Supabase. A busca retorna trechos rastreáveis e o teste demonstra recuperação relevante em português e resposta sem evidência quando apropriado.
- [ ] Modelo e dimensão de embeddings são compatíveis com pgvector e registrados; custos e acesso são verificados sem declarar valores inexistentes.
- [ ] Casos de avaliação cobrem parcelamento ambíguo, não cumulatividade de PIX e promoção, contatos divergentes, frete no valor exato de R$ 500 e regras de defeito/garantia. O agente reconhece ausência ou conflito e não inventa interpretação nem elegibilidade individual quando faltarem fatos.

## Implementação planejada

Inspecionar dados antes de definir tipos e restrições; criar migrações e carga segura limitada ao schema do projeto, com identidade separada para a aplicação; disponibilizar funções de leitura limitadas. Extrair e indexar o manual com metadados de página e seção, mantendo conteúdo recuperado como dado não confiável. Avaliar `pgvector` e modelo de embeddings, com limites e configuração explícitos.

## Validação planejada

Executar carga em ambiente apropriado e reexecutar com segurança, sem remover dados de outros projetos; verificar permissões com a identidade real da aplicação; comparar contagens com os arquivos e verificar relações; testar filtros, inexistência de resultados, bloqueio de dados individuais e isolamento de outros schemas; executar conjunto de perguntas sobre políticas e conferir páginas e contexto. Anotar limitações e diferenças sem dados pessoais.

## Evidências previstas

Migrações, scripts de carga, relatório sanitizado de integridade, resultados de testes e exemplos de recuperação. Commit sugerido: `Preparei os dados e a busca das políticas`.

## Resultado

Pendente de execução e validação. Registrar em primeira pessoa o que efetivamente fiz e as evidências reais.
