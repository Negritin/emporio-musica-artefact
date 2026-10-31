# Sprint SDD 01 — Fundação segura e repositório reproduzível

**Status:** concluída · **Responsável:** Cleverson Madruga · **Dependências:** análise deste plano; acesso GitHub confirmado; prazo confirmado pelo responsável; data e horário exatos ainda não registrados.

## Objetivo

Preparar uma base Python reproduzível e um repositório Git com histórico real, protegendo credenciais e dados pessoais desnecessários.

## Critérios de aceite

- [x] Repositório Git local inicializado e identidade de autoria configurada adequadamente; nenhum commit anterior fabricado.
- [x] `.gitignore` protege `.env` reais, ambientes virtuais, caches, dados pessoais desnecessários; `.env.example` contém somente nomes e exemplos não sensíveis.
- [x] Conteúdo a ser versionado e primeiro diff revisados para segredos e dados pessoais desnecessários antes de qualquer commit e publicação.
- [x] Estrutura Python, versões de dependências e comandos locais básicos documentados e reproduzidos em ambiente limpo; criar README inicial e mantê-lo atualizado ao longo das sprints.
- [x] O relatório local das dez conversas fica fora do controle de versão; verificar `git status` e arquivos ignorados antes de qualquer commit.
- [x] Código e configuração usam nomes claros, responsabilidades simples e apenas abstrações necessárias; decisões podem ser explicadas na entrevista.
- [x] Conexão PostgreSQL ao schema `artefact` verificada sem exibir segredos; teste de acesso ao OpenRouter e escolha inicial de modelo registrados sem expor a chave.
- [x] Estratégia de rotação das credenciais expostas e impacto nos serviços existentes registrados; nenhum segredo exposto no histórico.
- [x] Commits progressivos em português e primeira pessoa; criação e visibilidade do remoto GitHub verificadas no momento adequado, antes do prazo de entrega.

## Implementação planejada

Preparar projeto Python, organização de configuração e amostra de ambiente; revisar regras de exclusão antes de `git add`; inicializar Git e, quando a revisão permitir, criar o repositório público ou torná-lo público antes da entrega. O responsável autorizou a publicação dos materiais fornecidos; revisar e tratar dados pessoais antes de versionar.

## Validação planejada

Criar ambiente limpo e executar instalação e comando de verificação; inspecionar arquivos rastreados e diff; verificar conexão com consulta inofensiva ao schema e uma chamada mínima ao OpenRouter; verificar remoto, visibilidade e histórico quando existirem. Registrar versão, comandos e resultados sem dados sensíveis.

## Evidências previstas

Configuração sem segredos, saída resumida dos comandos, commit(s) e link do repositório quando existente. Sugestões de commits: `Preparei a estrutura inicial do projeto`; `Configurei a execução local com segurança`.

## Resultado

Preparei o ambiente Python 3.10 em uma venv nova, instalei as dependências e iniciei o Git com meu nome e e-mail. Criei o repositório público https://github.com/Negritin/emporio-musica-artefact e registrei o primeiro commit be45f4c. Validei as chamadas reais ao modelo e aos embeddings após a atualização da chave. Excluí ambientes, segredos e fontes com dados individuais do Git; a verificação não encontrou valores das credenciais locais nos arquivos rastreados. A rotação das credenciais compartilhadas depende da coordenação com os demais serviços e não alterei senhas de outros projetos. Concluí a validação em 2026-10-31T19:57:07-03:00.

**Início real:** 2026-10-31T19:50:08-03:00.
