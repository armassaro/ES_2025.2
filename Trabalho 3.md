Trabalho 3 2025-2 ES


Trabalho 3: Engenharia de Software - Teste e Entrega 

Este trabalho corresponde à última entrega do projeto da disciplina Engenharia de 
Software. O objetivo é concluir o projeto, incluindo testes e manutenção do 

sistema proposto por sua equipe. 

Prazos 

● Entrega (limite para atualização do git): 14:00 horas de 02/12/2025. 

● Entrevistas Técnicas / Apresentação: Aula de 02/12/2025. 

Entregáveis 

Para o sistema proposto, cada equipe (3 integrantes) deverá entregar: 

1. Testes - git (60%) 

● Readme: cenários de testes das funcionalidades entregues no T2 (10%) 

● Code: testes automatizados das funcionalidades entregues no T2 (10%) 

● Readme: relatório dos testes das funcionalidades entregues no T2 (10%) 

● Readme + code: TDD (teste e desenvolvimento) de novas funcionalidades 

(20%) 

● Readme + code: cenários e testes automatizados do sistema final (10%) 

2. Manutenção - git (40%) 

● Code: correção de bugs das funcionalidades entregues no Trabalho 2 (10%) 

● Readme + code: TDD (refatoração) de novas funcionalidades (10%) 

● Readme + code: Integração de funcionalidades do Trabalho 2 + novas (10%) 

● Readme + code: Refatorações gerais no código completo (10%) 

3. Demonstração - PDF no git (10%) 

● Vídeo (até 30 segundos) demonstrando o funcionamento da aplicação (5%) 

● Conjunto de 6 slides: i) título, autores; ii) objetivo do sistema; iii) plano de 

testes; iv), v), vi) TDD para/ cada integrante (5%) 



* Nos entregáveis, respeitar orientações dos slides, aulas, atividades de 

desenvolvimento e afins, principalmente quanto à divisão de responsabilidades! 

Instruções de Entrega 

● A entrega será considerada com base no repositório Git da equipe. 

● Os entregáveis devem estar claramente identificados. 

● Cada equipe deverá enviar no Moodle apenas os links correspondentes. 

Entrevista Técnica / Apresentação 

Na aula de apresentação, as equipes participarão de uma espécie de workshop. 

Cada equipe deverá: 

● Abrir seus slides e executar a aplicação em um computador específico 

● Ficar disponível para apresentar seu trabalho ao professor e demais colegas 

● Visitar as demais equipes, conhecer sobre seus projetos e selecionar os dois 

melhores projetos. 

A equipe com mais votos será premiada! 

Além disso, o professor irá avaliar o domínio de cada grupo sobre o projeto 
desenvolvido, abordando decisões técnicas, organização do documento, 

fundamentação teórica, uso das ferramentas e justificativas de desenvolvimento. 

● Todos os integrantes deverão participar. 

● A nota final do trabalho será ponderada pelo desempenho individual na 
entrevista, de forma a garantir o domínio do conteúdo trabalhado. 

● A ponderação será no formato Nota Rubrica * Nota Entrevista. 


	Trabalho 3: Engenharia de Software - Teste e Entrega 
	Prazos 
	Entregáveis 
	1. Testes - git (60%) 
	2. Manutenção - git (40%) 
	3. Demonstração - PDF no git (10%) 

	Instruções de Entrega 
	Entrevista Técnica / Apresentação 


Com base nas funcionalidades já documentadas no README.md e seguindo o mesmo formato, aqui estão cenários de teste adicionais para testes automatizados:

## Cenários de Teste para Testes Automatizados

### 4.1.4. Cenários de teste relacionados à autenticação e gerenciamento de usuários

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CT-022** | Não existe nenhum usuário com o username **"joao123"** cadastrado no sistema | O usuário tenta criar uma conta com username **"joao123"**, senha **"senha123"** e confirmação **"senha123"** | O sistema deve criar o usuário, salvar em `usuarios.json`, exibir mensagem de sucesso e permitir login |
| **CT-023** | Já existe um usuário com username **"maria"** cadastrado | O usuário tenta criar uma nova conta com username **"maria"** | O sistema deve rejeitar a criação, exibir mensagem **"[ERRO]: Usuário já existe"** e não duplicar o registro |
| **CT-024** | Existe um usuário **"pedro"** com senha **"abc123"** cadastrado | O usuário tenta fazer login com username **"pedro"** e senha **"abc123"** | O sistema deve autenticar com sucesso, criar uma sessão válida e redirecionar para a tela principal |
| **CT-025** | Existe um usuário **"ana"** com senha **"senha456"** cadastrado | O usuário tenta fazer login com username **"ana"** e senha **"senhaerrada"** | O sistema deve rejeitar o login, exibir mensagem **"[ERRO]: Senha incorreta"** e não criar sessão |
| **CT-026** | O usuário está na tela de criação de conta | O usuário insere senha **"123"** e confirmação **"456"** | O sistema deve validar que as senhas não coincidem, exibir mensagem de erro e não criar a conta |
| **CT-027** | O usuário está autenticado no sistema | O usuário seleciona a opção **"Sair"** ou **"Logout"** | O sistema deve encerrar a sessão, limpar dados de autenticação e redirecionar para tela de login |

### 4.1.5. Cenários de teste relacionados à persistência de dados

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CT-028** | O arquivo `habitos_registros.json` existe e contém 5 hábitos do usuário **"carlos"** | A aplicação é reiniciada | O sistema deve carregar todos os 5 hábitos com seus dados (nome, descrição, histórico) preservados |
| **CT-029** | O arquivo `usuarios.json` não existe no sistema | Um novo usuário tenta se registrar | O sistema deve criar o arquivo `usuarios.json`, registrar o usuário e salvar corretamente |
| **CT-030** | O usuário **"ana"** possui 3 hábitos cadastrados | O sistema tenta salvar alterações mas o arquivo `habitos_registros.json` está com permissões somente leitura | O sistema deve capturar o erro, exibir mensagem apropriada e não perder dados em memória |
| **CT-031** | Existem dados corrompidos no arquivo `habitos_registros.json` (JSON inválido) | O sistema tenta carregar os dados | O sistema deve detectar o erro, fazer backup do arquivo corrompido, criar novo arquivo e exibir mensagem de erro ao usuário |

### 4.1.6. Cenários de teste relacionados ao padrão Observer

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CT-032** | O usuário possui o hábito **"Exercícios"** com 5 dias de sequência e está visualizando estatísticas | O usuário marca **"Exercícios"** como concluído para hoje | O sistema deve notificar todos os observers, atualizar automaticamente a sequência para 6 dias e atualizar a interface sem necessidade de refresh |
| **CT-033** | A interface de relatórios está aberta mostrando 80% de taxa de conclusão | O usuário marca um hábito pendente como concluído | O sistema deve notificar o observer de relatórios e atualizar automaticamente a taxa de conclusão exibida |
| **CT-034** | Múltiplas views (console e GUI) estão abertas simultaneamente | O usuário marca um hábito como concluído em uma das interfaces | Todas as interfaces devem ser notificadas e exibir a atualização sincronizada |

### 4.1.7. Cenários de teste relacionados à exportação de PDF (Singleton)

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CT-035** | O usuário possui o hábito **"Meditar"** com 15 dias de histórico | O usuário seleciona **"Exportar para PDF"** para o hábito **"Meditar"** | O sistema deve gerar um arquivo PDF único com cabeçalho, informações do hábito, estatísticas e histórico formatado |
| **CT-036** | É a primeira vez que o PDFExporter é instanciado no sistema | A classe PDFExporter é chamada duas vezes na mesma execução | Ambas as chamadas devem retornar a mesma instância (mesmo ID de objeto) garantindo o padrão Singleton |
| **CT-037** | O usuário exportou um PDF e tenta exportar outro PDF na mesma sessão | O segundo PDF é solicitado | O sistema deve reutilizar a mesma instância do PDFExporter, mas gerar um novo arquivo PDF com dados atualizados |
| **CT-038** | O diretório de exportação não possui permissões de escrita | O usuário tenta exportar um relatório para PDF | O sistema deve capturar o erro de permissão e exibir mensagem clara ao usuário sem quebrar a aplicação |

### 4.1.8. Cenários de teste relacionados ao padrão Factory (ReportFactory)

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CT-039** | O usuário possui hábitos com registros dos últimos 30 dias | O usuário solicita um relatório do tipo **"diario"** através da Factory | A Factory deve instanciar e retornar um objeto de relatório diário com dados apenas de hoje |
| **CT-040** | O usuário solicita um tipo de relatório inválido (ex: **"anual"**) | A requisição é enviada ao ReportFactory | O sistema deve lançar exceção apropriada ou retornar erro indicando tipo de relatório não suportado |
| **CT-041** | São solicitados sequencialmente relatórios diário, semanal e mensal | Três chamadas consecutivas à Factory | A Factory deve criar três objetos distintos, cada um com a lógica específica de seu tipo de relatório |

### 4.1.9. Cenários de teste relacionados à validação de dados

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CT-042** | O usuário está criando um novo hábito | O usuário insere um nome com mais de 100 caracteres | O sistema deve validar o tamanho, truncar ou rejeitar com mensagem de limite de caracteres |
| **CT-043** | O usuário está criando um hábito | O usuário tenta inserir caracteres especiais perigosos (ex: `<script>`) no nome | O sistema deve sanitizar a entrada, remover/escapar caracteres perigosos |
| **CT-044** | O usuário está registrando progresso | O usuário tenta marcar conclusão com data no formato incorreto (ex: "13/32/2025") | O sistema deve validar o formato de data e rejeitar com mensagem clara sobre formato esperado (YYYY-MM-DD) |
| **CT-045** | O usuário está definindo frequência de hábito | O usuário seleciona frequência "personalizada" sem especificar dias | O sistema deve exigir seleção de pelo menos 1 dia e exibir mensagem de validação |

### 4.1.10. Cenários de teste de integração

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CT-046** | O usuário criou um novo hábito **"Leitura"** | O usuário marca progresso, visualiza relatório e exporta PDF em sequência | Todas as operações devem funcionar de forma integrada, com dados consistentes em cada etapa |
| **CT-047** | O usuário possui 10 hábitos cadastrados com diferentes frequências | O usuário solicita relatório mensal | O relatório deve calcular corretamente estatísticas considerando as diferentes frequências de cada hábito |
| **CT-048** | O sistema possui múltiplos usuários com hábitos distintos | O usuário **"joao"** faz login e visualiza seus hábitos | O sistema deve isolar corretamente os dados, mostrando apenas os hábitos de **"joao"** sem vazamento de informações de outros usuários |