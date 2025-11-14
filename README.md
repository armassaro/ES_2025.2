# ES_2025.2

> **Sumário**
> - [1. Ideia do projeto](#1-ideia-do-projeto)
>    - [1.1. Descrição](#11-descrição)
>    - [1.2. Funções principais](#12-funções-principais)
>    - [1.3. Padrões de projeto e estrutura geral](#13-padrões-de-projeto-e-estrutura-geral)
>       - [1.3.1. Padrão de Arquitetura: MVC (Model-View-Controller)](#131-padrão-de-arquitetura-mvc-model-view-controller)
>       - [1.3.2. Padrão de Criação: Factory Method](#132-padrão-de-criação-factory-method)
>       - [1.3.3. Padrão Comportamental: Observer](#133-padrão-comportamental-observer)
>       - [1.3.4. Padrão de Criação: Singleton](#134-padrão-de-criação-singleton)
>       - [1.3.5. Persistência de Dados](#135-persistência-de-dados)
>       - [1.3.6. Estrutura de Pacotes](#136-estrutura-de-pacotes)
>       - [1.3.7. Diagrama de classes](#137-diagrama-de-classes)
>       - [1.3.8. Diagramas de sequência](#138-diagramas-de-sequência)
>          - [1.3.8.1. Registro de progresso (Observer)](#1381-registro-de-progresso-observer)
>          - [1.3.8.2. Geração de relatórios (Factory)](#1382-geração-de-relatórios-factory)
>          - [1.3.8.3. Exportação de PDF (Singleton)](#1383-exportação-de-pdf-singleton)
> - [2. Viabilidade técnica](#2-viabilidade-técnica)
> - [3. Definições relacionadas à gerência de qualidade](#3-definições-relacionadas-à-gerência-de-qualidade)
>   - [3.1. Padrões de segurança](#31-padrões-de-segurança)
>   - [3.2. Padrões de qualidade](#32-padrões-de-qualidade)
>   - [3.3. Papéis e atividades](#33-papéis-e-atividades)
>   - [3.4. Definições de atividades recorrentes para validação dos padrões propostos](#34-definições-de-atividades-recorrentes-para-validação-dos-padrões-propostos)
>       - [3.4.1. Para o caso de código](#para_o_caso_de_codigo)
>       - [3.4.2. Para o caso de documentação](#para_o_caso_de_documentacao)
> - [4. Testes e validação](#4-testes-e-validação)
>   - [4.1. Cenários de testes](#41-cenários-de-testes)
>       - [4.1.1. Cenários de teste relacionados ao CRUD de criação de hábitos (Arthur)](#411-cenários-de-teste-relacionados-ao-crud-de-criação-de-hábitos-arthur)  
>       - [4.1.2. Cenários de teste relacionados a marcação de conclusão de hábitos (Ian)](#412-cenários-de-teste-relacionados-a-marcação-de-conclusão-de-hábitos-ian)
>       - [4.1.3. Cenários de teste relacionados a geração de relatórios (Silvino)](#413-cenários-de-teste-relacionados-a-geração-de-relatórios-silvino)
>   - [4.2. Registros de testes](#42-registro-dos-testes)
>   - [4.3. Testes automatizados](#43-testes-automatizados)
>       - [4.3.1. Cenários de teste automatizados relacionados ao CRUD de criação de hábitos (Arthur)](#431-cenários-de-teste-automatizados-relacionados-ao-crud-de-criação-de-hábitos-arthur)
>       - [4.3.2. Cenários de teste automatizados relacionados a visualização de hábitos (Ian)](#432-cenários-de-teste-automatizados-relacionados-a-visualização-de-hábitos-ian)
>       - [4.3.3. Cenários de teste automatizados relacionados a geração de relatórios (Silvino)](#433-cenários-de-teste-automatizados-relacionados-a-geração-de-relatórios-silvino)

## 1. Ideia do projeto
O presente projeto possui como principal intuito a criação de um sistema de gerenciamento de hábitos com capacidade de criação de conta e acompanhamento da criação e evolução pessoal dos hábitos escolhidos pelo próprio usuário.

### 1.1. Descrição
Uma aplicação para registro de hábitos diários (ex: estudar, beber água, fazer exercícios), com histórico e relatórios básicos e mecanismos de incentivo ao desenvolvimetno do hábito, por meio de técnicas de gameficação com base em estudos científicos. 
    
### 1.2. Funções principais
A aplicação proposta seria composta por 3 principais funções: 
1. Cadastro de hábitos (CRUD: criar, editar, excluir e modificar).
2. Registro diário de progresso (checkboxes ou botões).
3. Exibição e exportação de relatórios diário, mensal e semanal

### 1.3. Padrões de projeto e estrutura geral
Os padrões de projeto consistem em várias arquiteturas documentadas e especializadas em determinados tipos de funções para uma aplicação. A seguir, são listados os padrões de projeto e arquitetura utilizados durante o desenvolvimento da aplicação proposta, assim como as explicações para a utilização de cada padrão de projeto utilizado para cada função presente na aplicação.

#### 1.3.1. Padrão de Arquitetura: MVC (Model-View-Controller)
O padrão **MVC** foi escolhido como arquitetura base do sistema de gerenciamento de hábitos por proporcionar uma clara separação de responsabilidades entre as camadas da aplicação:

- **Model (Modelo)**: Responsável pela lógica de negócio e manipulação de dados. No projeto, os modelos (`HabitModel`, `UserModel`, `ReportFactory`) gerenciam as operações relacionadas a hábitos, usuários e relatórios, incluindo validações e persistência em arquivos JSON.

- **View (Visão)**: Responsável pela apresentação dos dados ao usuário. O sistema possui duas interfaces: `ConsoleView` para interação via terminal e `GUI` (LoginWindow e MainWindow) para interface gráfica, permitindo flexibilidade na forma de interação.

- **Controller (Controlador)**: Atua como intermediário entre Model e View, processando as entradas do usuário e coordenando as operações. Os controladores (`HabitController`, `ReportController`) recebem comandos da interface, invocam os modelos apropriados e atualizam as visualizações.

O MVC foi escolhido porque facilita a manutenção e evolução do código, permite o desenvolvimento paralelo de diferentes componentes, facilita testes unitários (cada camada pode ser testada independentemente) e possibilita a criação de múltiplas interfaces (console e GUI) compartilhando a mesma lógica de negócio.

--- 

O material utilizado para escolha e estudo do modelo MVC pode ser encontrado em: [https://www.devmedia.com.br/padrao-mvc-java-magazine/21995]

---

#### 1.3.2. Padrão de Criação: Factory Method
O padrão **Factory Method** foi implementado através da classe `ReportFactory` para a criação de diferentes tipos de relatórios:

- Permite criar relatórios diários, semanais e mensais de forma padronizada
- Encapsula a lógica de criação, facilitando a adição de novos tipos de relatórios
- Centraliza a responsabilidade de instanciação em um único local

Este padrão foi escolhido porque o sistema precisa gerar diferentes tipos de relatórios com estruturas e cálculos variados. O Factory Method permite adicionar novos formatos de relatório sem modificar o código cliente, seguindo o princípio Open/Closed (aberto para extensão, fechado para modificação).

---

O material utilizado para escolha e estudo do padrão de projeto Factory está disponível em: [https://www.devmedia.com.br/padrao-mvc-java-magazine/21995]

---

#### 1.3.3. Padrão Comportamental: Observer
O padrão **Observer** é utilizado para notificação de mudanças no estado dos hábitos e atualização automática das interfaces:

- Quando um progresso é registrado em um hábito, os componentes de visualização (relatórios, estatísticas) são automaticamente notificados
- Permite que múltiplos observadores (diferentes views) sejam atualizados simultaneamente
- Implementa um mecanismo de assinatura/publicação para desacoplamento entre componentes

O Observer foi implementado para garantir que todas as visualizações do sistema se mantenham sincronizadas com o estado atual dos dados. Quando o usuário registra progresso em um hábito, os painéis de estatísticas, gráficos e relatórios são atualizados automaticamente sem necessidade de recarregamento manual, melhorando a experiência do usuário e mantendo a consistência dos dados exibidos.

---

O material utilizado para escolha e estudo do padrão de projeto Observer está disponível em: [https://www.devmedia.com.br/padrao-mvc-java-magazine/21995]

---

#### 1.3.4. Padrão de Criação: Singleton
O padrão **Singleton** foi implementado na classe `PDFExporter` para garantir que apenas uma única instância do exportador de PDF exista durante toda a execução da aplicação:

- **Instância única**: O Singleton garante que apenas um objeto `PDFExporter` seja criado, independentemente de quantas vezes a classe seja instanciada
- **Controle de inicialização**: A inicialização dos estilos e configurações do PDF ocorre apenas uma vez, evitando processamento desnecessário
- **Acesso global controlado**: Fornece um ponto de acesso global à instância através do método `get_instance()` ou através do construtor padrão

A implementação do Singleton foi feita em `PDFExporter` e utiliza das seguintes variáveis e métodos:
- Atributo de classe `_instance`: armazena a única instância da classe
- Atributo de classe `_initialized`: controla se a inicialização já foi realizada
- Método `__new__()`: para controlar a criação de instâncias
- Método `get_instance()`: método alternativo para obter a instância única

O fluxo geral da função implementada no código é feita da seguinte forma:
1. O usuário solicita a exportação de um relatório através da interface
2. O sistema obtém a instância única do `PDFExporter`
3. O exportador formata os dados do hábito em um relatório estruturado
4. O PDF é gerado com informações detalhadas:
   - Cabeçalho com nome do hábito
   - Informações gerais , como descrição, frequência, status, data de criação
   - Resumo de progresso, como dias registrados, taxa de conclusão, sequência atual
   - Histórico detalhado dos últimos 30 dias
   - Rodapé com data e hora de geração

Este padrão foi escolhido para a exportação de PDF por conta da economia de memória, evitando a criação de várias instâncias da mesma classe, consistência visual nos PDFs gerados e do gerenciamento centralizado que o padrão de projeto é capaz de oferecer ao limitar a criação de objetos.

---

O material utilizado para escolha e estudo do padrão de projeto Singleton está disponível em: [https://refactoring.guru/design-patterns/singleton]

---

#### 1.3.5. Persistência de Dados
O sistema utiliza **arquivos JSON** para armazenamento de dados:

- `usuarios.json`: Armazena informações de usuários e autenticação
- `habitos_registros.json`: Mantém o histórico de hábitos e registros de progresso

A escolha por JSON foi feita considerando a simplicidade do projeto, facilidade de leitura e edição manual dos dados (útil para debugging), portabilidade entre diferentes sistemas, e não necessidade de um servidor de banco de dados complexo para um sistema de uso individual/local.

#### 1.3.6. Estrutura de Pacotes

O projeto segue uma organização modular em pacotes:

```
HabitTracker/
├── Model/          # Classes de modelo e lógica de negócio
├── view/           # Interfaces de usuário (console e GUI)
├── controller/     # Controladores que coordenam Model e View
└── *.json          # Arquivos de persistência de dados
```

Esta estrutura facilita a localização de componentes, manutenção do código, implementação de testes unitários por camada, e permite que diferentes membros da equipe trabalhem em paralelo em diferentes camadas sem conflitos significativos.

#### 1.3.7. Diagrama de classes
![Diagrama de classes utilizado no projeto proposto](./imagens/diagrama_de_classes.png)

#### 1.3.8. Diagramas de sequência
Abaixo se encontram os diagramas de sequência utilizados para o desenvolvimento do projeto, para eclucidação do que seria feito posteriormente na programação das funções: 

##### 1.3.8.1. Registro de progresso (Observer)
![](./imagens/diagrama_registro_progresso.png)

##### 1.3.8.2. Geração de relatórios (Factory)
![](./imagens/diagrama_geracao_relatorios.png)

##### 1.3.8.3. Exportação de PDF (Singleton)
![](./imagens/diagrama_exportacao_pdf.png)

## 2. Viabilidade Técnica
Dados os estudos científicos recolhidos e a crescente demanda para o desenvolvimento de hábitos, é possível considerar como altamente viável o desenvolvimento de uma aplicação com o intuito do desenvolvimento pessoal, com foco na criação e mantenimento de hábitos. Além disso, todos os padrões estão devidamente descritos e é possível obter uma visão clara do funcionamento do sistema a partir da presente documentação.

## 3. Definições relacionadas à gerência de qualidade
Abaixo são definidos os padrões de segurança e qualidade, os quais são fatores determinantes para o desenvolvimetno do projeto como um todo. 

### 3.1. Padrões de segurança
Assim como define Sommerville (2019), os padrões de segurança podem ser divididos em padrões de _Safety_ e de _Security_, sendo o primeiro o conjunto de práticas destinadas à prevenção de danos físicos e econômicos, enquanto o segundo destina-se à prevenção de acesso não autorizado ou ataques maliciosos na aplicação.
Deste modo, são definidos as seguintes premissas para os padrões de segurança:
 - O aplicativo deve solicitar apenas as permissões mínimas necessárias para seu funcionamento, evitando acesso a dados ou recursos do dispositivo que não sejam essenciais.
 - O aplicativo deve ser assinado digitalmente e ter suas atualizações testadas e verificadas antes da publicação, prevenindo a introdução de novas vulnerabilidades.
 - Todas as dependências e bibliotecas externas devem ser mantidas atualizadas e provenientes de fontes seguras, evitando o uso de versões vulneráveis ou não mantidas.
 - Nenhum dado sensível deve ser exposto em logs, nem salvo em texto plano, respeitando as normas de privacidade e proteção de dados, como a LGPD (Lei Geral de Proteção de Dados).
 - O aplicativo deve evitar funcionalidades não autorizadas e garantir que seu comportamento seja transparente e previsível para o usuário.  

**Como os padrões listados serão validados?**  
Os padrões de segurança acima listados serão validados a partir de reuniões semanais para revisão dos últimos _commits_ lançados na branch ```main``` do repositório do Github, a qual é reservada para a disponibilização da última versão estável da aplicação.  

---

Todas as funcionalidades apresentadas estão disponíveis no documento de normas de segurança do NIST (National Institute of Standards and Techonology) do departamento de comércio dos Estados Unidos. O respectivo documento possui como título "Vetting the Secutiry of Mobile Applications", foi redigido por Steve Quirolgico, Jeffrey Voas, Tom Karygiannis, Christoph Micheal e Karen Scarfone e está disponível no seguinte link: [http://dx.doi.org/10.6028/NIST.SP.800-163].

---

### 3.2. Padrões de qualidade
Conforme Sommerville (2019), os padrões de qualidade podem ser divididos em duas categorias: de produto e de processo. Os padrões de produtos definem características de qualidade do produto ou à documentação desenvovlida durante a produção do produto, podendo incluir padrões relacionados à: 

- A estrutura do documento de requisitos
- Padrões de documentação, como comentários padrão na criação de determinadas classes
- Padrões de codificação, como o estilo de variáveis e classes a serem codificadas

Já os padrões de processo definem o conjunto de processos relacionados a especificação, projeto e validação durante o desenvolvimento do software. 
Logo, abaixo se encontram os padrões de qualidade que pautarão o desenvolvimento da aplicação: 

- Utilização da linguagem Python, por conta da rápida implementação e vasta quantidade de bibliotecas.
- Utilização do padrão PEP8, para manutenção de um código legível e baseado em premissas objetivas e simples. A documentação do padrão PEP8 se encontra no seguinte link: [https://peps.python.org/pep-0008/].
- As descrições dos _commits_ devem ser redigidas de modo claro, objetivo e breve, para organização de cada branch e do repositório como um todo. 
- Os _commits_ a serem enviados devem ser o mais modulares possíveis, ou seja, devem englobar apenas ao que se propõe na descrição do mesmo, para o caso da necessidade de voltar a um determinado ponto do desenvolvimento, sem maiores perdas de progresso no desenvolvimento.
- As descrições dos _commits_ devem seguir a convenção descrita abaixo, para facilitação da identificação do tipo de _commit_ e na construção do changelog: 
```
    <tipo>: <mensagem curta>
    Sendo que <tipo> pode ser: 
        - feat: representa a adição de uma função ou arquivo
        - fix: correção de um erro, bug ou lógica no código
        - docs: atualização na documentação
        - style: atualização de formatação em um ou mais arquivos de código
        - refactor: reescrita de código visando melhoria de performance ou lógica
        - test: adição de teste unitário 
        - chore: atualização de dependências do projeto
```

**Como os padrões listados serão validados?**
Os padrões de qualidade acima listados serão validados a partir da observação do histórico de _commits_ durante a produção, assim como nas reuniões semanais.

--- 

As menções às definições de padrão de qualidade e padrões de segurança se encontram na décima edição do livro "Engenharia de Software" escrito por Ian Sommerville, estando disponível em [https://archive.org/details/sommerville-engenharia-de-software-10e]

---

### 3.3. Papéis e atividades 
O método **SCRUM** é um framework ágil de gerenciamento de projetos que visa promover a colaboração contínua, a entrega incremental de valor e a adaptação rápida às mudanças. Ele é estruturado em ciclos curtos chamados **sprints**, nos quais a equipe trabalha em um conjunto definido de tarefas, buscando entregar incrementos funcionais do produto a cada iteração. O SCRUM baseia-se em três pilares principais: **transparência**, **inspeção** e **adaptação**, garantindo que o processo seja constantemente aprimorado por meio de reuniões regulares, como as *daily meetings* e *reviews*.

Dentro do contexto do projeto, os papéis foram distribuídos da seguinte forma:

* **Arthur** atuará como *Scrum Master*, sendo responsável por facilitar as cerimônias do SCRUM, remover impedimentos e garantir que o time siga os princípios e práticas ágeis estabelecidas.
* **Ian** assumirá o papel de *Product Owner*, ficando encarregado de definir as prioridades do produto, gerenciar o backlog e assegurar que as entregas estejam alinhadas às necessidades e objetivos do projeto.
* **Silvino** desempenhará o papel de *Developer*, sendo responsável pela implementação das funcionalidades, manutenção do código e colaboração direta nas revisões e planejamentos semanais.

Essa estrutura garante uma comunicação eficaz entre os membros, favorece a organização do trabalho e assegura entregas consistentes e alinhadas com os objetivos do sistema de gerenciamento de hábitos.

### 3.4. Definições de atividades recorrentes para validação dos padrões propostos
A presente seção possui como intuito a recapitulação e resumo das atitudes a serem tomadas para a contínua validação dos padrões propostos nas seções 3.1 e 3.2, para facilitação e organização de cada reunião semanal do projeto.
Cada reunião semanal será norteada nas seguintes premissas: 
1. Cada membro deverá demonstrar as próprias contribuições feitas desde a última reunião e enviadas ao repositório para todos os outros membros, de forma a explicar no código/documentação e na prática o que foi feito. Devem ser observados os seguintes pontos para cada caso:

<div id="para_o_caso_de_codigo"></div> 

> **3.4.1. Para o caso de código**
> - **As contribuições trazidas necessitam de alguma permissão a ser concedida por parte do usuário?**  
    Tal ponto deve ser observado por questões de segurança e por questões de transparência de permissões para o usuário, para que o usuário tenha ciência do tipo de informação que a aplicação possui acesso. 
> - **O _commit_ obedece a convenção estabelecida e possui descrição curta e objetiva?**  
    Tal ponto deve ser observado para manutenção da legibilidade e organização dos últimos _commits_ submetidos ao repositório.
> - **A contribuição trouxe a utilização de uma nova biblioteca não instalada no projeto anteriormente? A biblioteca é segura e está atualizada?**   
    Tal ponto deve ser observado para que haja transparência entre os membros e a manutenção da segurança da aplicação.
> - **A contribuição utiliza alguma forma de _logging_? Caso positivo, as mensagens de _log_ expõem alguma informação sensível?**  
    Tal ponto deve ser observado para que hajam menores chances de vazamento de dados sensíveis dos usuários da aplicação.
> - **O novo recurso trazido pela contribuição possui alguma situação onde é possível quebrar a aplicação?**  
    Tal ponto deve ser observado para que não haja uma quebra na fluidez da experiência do usuário e possíveis brehcas de segurança.
> - **O novo recurso trazido pela contribuição lida com dados sensíveis?**  
    Tal ponto deve ser observado para que hajam outras verificações como a de permissões e mensagens de _log_, assim como verificações para encapsulamento das informações sensíveis sendo manuseadas.

<div id="para_o_caso_de_documentacao"></div> 

> **3.4.2. Para o caso de documentação**
> - **O commit que trouxe a contribuição para a documentação segue a convenção?**  
    Tal ponto deve ser observado para manutenção da legibilidade e organização dos últimos _commits_ submetidos ao repositório.
> - **A documentação trazida pela contribuição coincide exatamente com as contribuições no código?**  
    Tal ponto deve ser observado para que a documentação possa continuamente refletir no código.

## 4. Testes e validação
Esta seção se reserva a compilar as práticas de testes e validação que serão aplicadas durante o desenvolvimento do projeto para validação das funcionalidades e melhoria contínua das funcionalidades propostas.

### 4.1. Cenários de testes
Os cenários de testes se tratam de determinados cenários estruturados a partir de uma pré-condição, uma ação e o resultado esperado a partir do teste executado. Os testes a seguir são documentados pelos membros e cada membro está encarregado de um escopo diferente dentro da aplicação, estando dividido em 3 principais escopos: testes para CRUD de criação de hábitos, testes para marcação de conclusão dos hábitos e testes para geração de relatórios.   
Os cenários de teste serão executados pelos membros a cada **1 semana**, a fim de atestar o funcionamento de cada escopo da aplicação.  
São listados abaixo os cenários de teste separados por escopo: 

#### 4.1.1. Cenários de teste relacionados ao CRUD de criação de hábitos (Arthur)

**Como um** usuário do sistema de gerenciamento de hábitos  
**Eu quero** criar, visualizar, atualizar e excluir meus hábitos  
**De modo que** eu possa gerenciar efetivamente minha rotina e acompanhar meu progresso pessoal

---

**Cenários Funcionais**

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CT-001** | O usuário está autenticado no sistema e está na tela de gerenciamento de hábitos | O usuário seleciona a opção **"Criar Novo Hábito"**, preenche o campo **"Nome"** com *"Beber água"*, o campo **"Descrição"** com *"Beber 2 litros de água por dia"*, seleciona a frequência **"diária"** e confirma a criação | O sistema exibe a mensagem **"✅ Hábito criado com sucesso"**, o hábito *"Beber água"* aparece na lista de hábitos cadastrados e é persistido no arquivo `habitos_registros.json` |
| **CT-002** | O usuário está autenticado no sistema e está na tela de criação de hábito | O usuário deixa o campo **"Nome"** em branco, preenche o campo **"Descrição"** com *"Exercícios matinais"* e tenta confirmar a criação | O sistema exibe a mensagem de erro **"[ERRO]: Nome do hábito não pode estar vazio"**, o hábito não é criado e o usuário permanece na tela de criação |
| **CT-003** | O usuário está autenticado no sistema e possui um hábito cadastrado com nome *"Beber água"* | O usuário seleciona a opção **"Atualizar Hábito"**, escolhe o hábito *"Beber água"*, altera o nome para *"Beber 3 litros de água"*, altera a descrição para *"Aumentar hidratação diária"* e confirma | O sistema exibe mensagem de sucesso, o hábito tem os dados atualizados na lista e as alterações são persistidas no arquivo JSON |
| **CT-004** | O usuário está autenticado no sistema e possui um hábito *"Exercícios"* com histórico de 10 dias de progresso | O usuário seleciona **"Deletar Hábito"**, escolhe *"Exercícios"* e confirma a exclusão | O hábito é marcado como inativo (**active: false**) no sistema, o histórico de progresso é mantido no arquivo JSON, o hábito não aparece na lista de hábitos ativos e os dados ficam disponíveis para restauração futura |

---

#### 4.1.2. Cenários de teste relacionados a marcação de conclusão de hábitos (Ian)

**Como um** usuário do sistema de gerenciamento de hábitos  
**Eu quero** marcar meus hábitos como concluídos em diferentes datas  
**De modo que** eu possa acompanhar meu progresso e manter meu histórico atualizado

---

**Cenários Funcionais**

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CT-005** | O usuário **"ana"** está autenticado e possui o hábito **"Beber 2L de água"** ativo para hoje | O usuário solicita **"marcar concluído"** para o hábito *"Beber 2L de água"* sem especificar data (padrão = hoje) | O sistema cria/registra uma entrada de conclusão para a data de hoje, retorna confirmação de sucesso e atualiza o contador/sequência do hábito |
| **CT-006** | O usuário **"ana"** está autenticado e o hábito **"Caminhar 30min"** existe e permite marcações em datas passadas | O usuário solicita **"marcar concluído"** para *"Caminhar 30min"* na data **"2025-11-09"** | O sistema registra a conclusão para **2025-11-09**, atualiza as estatísticas correspondentes e retorna confirmação |
| **CT-007** | O usuário **"ana"** já marcou **"Meditar 10min"** como concluído para hoje | O usuário tenta marcar novamente **"Meditar 10min"** como concluído para hoje | O sistema rejeita a operação, não duplica o registro e retorna mensagem de erro **"Hábito já marcado para esta data"** |
| **CT-008** | A política do sistema não permite marcar conclusões para datas futuras | O usuário solicita marcar **"Estudar 1h"** como concluído na data **"2025-12-31"** (futura) | O sistema rejeita a solicitação com mensagem **"Data inválida: não é permitida marcação futura"** e não cria registro |

---

#### 4.1.3. Cenários de teste relacionados a geração de relatórios (Silvino)

**Como um** usuário do sistema de gerenciamento de hábitos  
**Eu quero** visualizar relatórios de diferentes períodos (diário, semanal, mensal)  
**De modo que** eu possa analisar meu desempenho e identificar padrões nos meus hábitos

---

## C.2 Cenários Funcionais

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CT-009** | O usuário está na tela de Relatórios e possui hábitos cadastrados com registros de conclusão na data de hoje | O usuário seleciona a opção **"Diário"** (último 1 dia) | O sistema exibe um relatório contendo apenas os dados (concluído/não concluído) dos hábitos referentes à data de hoje |
| **CT-010** | O usuário está na tela de Relatórios e possui hábitos cadastrados com registros de conclusão nos últimos 7 dias | O usuário seleciona a opção **"Semanal"** (últimos 7 dias) | O sistema exibe um relatório abrangendo o período dos últimos 7 dias, mostrando a performance (taxa de conclusão) de todos os hábitos nesse intervalo |
| **CT-011** | O usuário está na tela de Relatórios e possui hábitos cadastrados com registros de conclusão nos últimos 30 dias | O usuário seleciona a opção **"Mensal"** (últimos 30 dias) | O sistema exibe um relatório abrangendo o período dos últimos 30 dias, mostrando a performance geral e tendências dos hábitos nesse intervalo |
| **CT-012** | O usuário gera um Relatório (Diário, Semanal ou Mensal) com múltiplos hábitos cadastrados | O relatório é exibido na tela | Os hábitos devem estar ordenados de forma consistente (por ordem alfabética do nome) e apresentar dados corretos de conclusão para o período selecionado |

### 4.2. Registro dos testes
Os testes serão armazenados em um arquivo .md na pasta [3a entrega](/3a%20entrega/) como [Logs de testes.md](/3a%20entrega/Logs%20de%20testes.md). A estrutura de cada teste documentado no arquivo de log de testes está estruturada abaixo:  

```
## Teste #00

> **Data de execução**: 13/11/2025 14:00 
> **ID do cenário**: CT-001  
> **Membro**: Arthur  
> **Foram apontados erros?**: True/False

### Descrição do teste
Nesta seção deve ser descrito como o teste ocorreu e se foram detectados quaisquer tipos de erro. Para o caso de erros estéticos, é importante arquivar imagens ou vídeos que apontem claramente o erro e a explicação do que possivelmente levou ao erro. É importante também documentar por meio de imagens ou vídeos quaisquer mensagens de erro vindas da execução do Python como linguagem ou erro de lógica do código.

### Ações tomadas para correção do erro
Aqui devem ser listadas as ações que foram tomadas para corrigir o erro. 
Ex.: 
- Otimização da lógica do código
- Correção do erro estético relatado
```

A estrutura do registro de teste colocado acima possui como principais características a possibilidade da documentação dos testes de forma objetiva e clara, bem como pela busca fácil a partir da seção de tags em cada teste.

### 4.3. Testes automatizados
Os testes automatizados são uma coleção de scripts programados para testar as funcionalidades do projeto de forma automática e em larga escala, de forma com que seja possível economizar tempo.  
Os scripts de teste da aplicação estão presentes na pasta [scripts](/3a%20entrega/scripts/) e os resultados da execução destes scripts também estarão listados no [Logs de testes.md](/3a%20entrega/Logs%20de%20testes.md).  
Abaixo se encontram os cenários de teste que os scripts automatizados se baseiam: 

#### 4.3.1. Cenários de teste automatizados relacionados ao CRUD de criação de hábitos (Arthur)

**Como um** desenvolvedor do sistema de gerenciamento de hábitos  
**Eu quero** automatizar os testes de CRUD de hábitos  
**De modo que** possa garantir a integridade das operações básicas do sistema de forma contínua

---

**Cenários Funcionais - Testes Automatizados**

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CTA-001** | O sistema está inicializado com `HabitModel` e `HabitController` instanciados, e o arquivo `habitos_registros.json` está vazio ou com estado conhecido | O teste automatizado chama o método `create_habit(name="Beber água", description="Beber 2L por dia", frequency="daily")` | O método retorna `True`, o hábito é adicionado ao modelo com ID único, o atributo `active` é `True`, e o arquivo JSON contém o novo hábito com todos os campos corretos |
| **CTA-002** | O sistema está inicializado com `HabitModel` e `HabitController` instanciados | O teste automatizado tenta chamar `create_habit(name="", description="Desc", frequency="daily")` com nome vazio | O método retorna `False` ou lança exceção, nenhum hábito é criado no modelo, e o arquivo JSON permanece inalterado |
| **CTA-003** | O sistema possui um hábito pré-cadastrado com `habit_id="h001"`, `name="Exercícios"`, `description="30min diários"` | O teste automatizado chama `update_habit(habit_id="h001", name="Exercícios Intensos", description="45min diários")` | O método retorna `True`, os dados do hábito `h001` são atualizados no modelo, o arquivo JSON reflete as alterações, e os demais campos (ID, created_at, active) permanecem inalterados |
| **CTA-004** | O sistema possui um hábito `habit_id="h002"` com `active=True` e histórico de 10 registros em `history` | O teste automatizado chama `delete_habit(habit_id="h002")` | O método retorna `True`, o atributo `active` do hábito é alterado para `False`, o histórico é preservado no JSON, e o hábito não aparece em consultas de hábitos ativos |

---

#### 4.3.2. Cenários de teste automatizados relacionados a visualização de hábitos (Ian)

**Como um** desenvolvedor do sistema de gerenciamento de hábitos  
**Eu quero** automatizar os testes de visualização e listagem de hábitos  
**De modo que** possa validar a correta exibição e filtragem de hábitos no sistema

---

**Cenários Funcionais - Testes Automatizados**

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CTA-005** | O sistema possui 3 hábitos cadastrados: `h001="Beber água"` (ativo), `h002="Exercícios"` (ativo), `h003="Meditar"` (inativo) | O teste automatizado chama `get_active_habits()` ou método equivalente que retorna apenas hábitos ativos | O método retorna lista com 2 hábitos (`h001` e `h002`), o hábito `h003` não aparece na lista, e cada hábito contém os campos: `habit_id`, `name`, `description`, `active=True` |
| **CTA-006** | O sistema possui um hábito `h001` com histórico `history={"2025-11-10": true, "2025-11-12": true}` | O teste automatizado chama `get_habit_by_id("h001")` | O método retorna o objeto do hábito completo, incluindo o campo `history` com todas as entradas corretas, e os campos `name`, `description`, `frequency`, `active` estão presentes |
| **CTA-007** | O sistema está vazio sem nenhum hábito cadastrado | O teste automatizado chama `get_active_habits()` | O método retorna lista vazia `[]` ou `None`, e nenhum erro é lançado durante a execução |
| **CTA-008** | O sistema possui 4 hábitos ativos com nomes: "Zumba", "Academia", "Meditação", "Beber água" | O teste automatizado chama método de listagem de hábitos e verifica a ordenação | Os hábitos são retornados em ordem alfabética: ["Academia", "Beber água", "Meditação", "Zumba"], mantendo todas as propriedades de cada hábito intactas |

---

#### 4.3.3. Cenários de teste automatizados relacionados a geração de relatórios (Silvino)

**Como um** desenvolvedor do sistema de gerenciamento de hábitos  
**Eu quero** automatizar os testes de geração de relatórios  
**De modo que** possa validar a correta geração e cálculo de estatísticas para diferentes períodos

---

**Cenários Funcionais - Testes Automatizados**

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CTA-009** | O sistema possui 3 hábitos ativos, a data atual é `2025-11-14`, e existe histórico: `h001` marcado hoje (concluído), `h002` não marcado hoje, `h003` marcado hoje | O teste automatizado chama `ReportFactory.create_report("daily", raw_data)` e obtém `report.generate_visualization_data()` | O relatório retorna estrutura com `date="2025-11-14"`, `completed=2`, `total_habits=3`, e lista de hábitos com status correto para cada um |
| **CTA-010** | O sistema possui 2 hábitos ativos com histórico dos últimos 7 dias: `h001` concluído em 5 dias, `h002` concluído em 3 dias | O teste automatizado chama `ReportFactory.create_report("weekly", raw_data)` e obtém `report.generate_visualization_data()` | O relatório retorna estrutura com período dos últimos 7 dias, `total_completed=8`, cálculo de estatísticas semanais, e dados diários (`daily_data`) com contagens corretas |
| **CTA-011** | O sistema possui 3 hábitos ativos com histórico distribuído nos últimos 30 dias com padrões variados de conclusão | O teste automatizado chama `ReportFactory.create_report("monthly", raw_data)` e obtém `report.generate_visualization_data()` | O relatório retorna estrutura com período dos últimos 30 dias, `total_completed` correto, cálculo de sequência máxima (`max_streak`), e resumo semanal (`weekly_summary`) com dados agregados |
| **CTA-012** | O sistema possui hábitos sem nenhum registro de conclusão (histórico vazio) | O teste automatizado gera relatórios diário, semanal e mensal | Todos os relatórios retornam estrutura válida sem erros, com `completed=0`, `total_habits` correto, e campos de estatísticas zerados ou com valores padrão |

---

#### 4.3.4. Cenários de teste automatizados relacionados a exportação de PDF (Todos)

**Como um** desenvolvedor do sistema de gerenciamento de hábitos  
**Eu quero** automatizar os testes de exportação de PDF com padrão Singleton  
**De modo que** possa garantir a geração correta de relatórios e a unicidade da instância do exportador

---

**Cenários Funcionais - Testes Automatizados**

| ID | Dado que (pré-condição) | Quando (ação) | Então (resultado esperado) |
|----|--------------------------|----------------|-----------------------------|
| **CTA-013** | O sistema está inicializado e nenhuma instância de `PDFExporter` foi criada ainda | O teste automatizado cria duas variáveis: `exporter1 = PDFExporter()` e `exporter2 = PDFExporter()` | Ambas as variáveis apontam para a mesma instância (`exporter1 is exporter2 == True`), a mensagem "PDFExporter inicializado (Singleton)" aparece apenas uma vez nos logs, e `PDFExporter._instance` não é `None` |
| **CTA-014** | O sistema possui um hábito com dados completos: `name="Exercícios"`, `description="30min"`, `history` com 15 dias de registros variados | O teste automatizado chama `exporter.export_habit_report(habit, "test_report.pdf")` | O método retorna sem erros, o arquivo `test_report.pdf` é criado no sistema de arquivos, o arquivo tem tamanho > 0 bytes, e contém estrutura PDF válida (pode ser aberto) |
| **CTA-015** | O sistema possui um hábito válido e `PDFExporter` já foi instanciado | O teste automatizado chama `export_habit_report()` para o mesmo hábito em dois arquivos diferentes: `"report1.pdf"` e `"report2.pdf"` | Ambos os arquivos são criados com sucesso, ambos contêm os mesmos dados do hábito formatados, e a mesma instância de `PDFExporter` é utilizada (verificado por logs ou ID da instância) |
| **CTA-016** | O sistema possui um hábito com histórico dos últimos 30 dias com padrão misto (dias concluídos e pendentes) | O teste automatizado gera PDF e verifica o conteúdo através de biblioteca de parsing (ex: PyPDF2) | O PDF contém seções obrigatórias: "Informações Gerais", "Resumo de Progresso", "Histórico Detalhado", e os dados numéricos (dias registrados, taxa de conclusão, sequência) correspondem aos cálculos esperados |

---

**Observações sobre os testes automatizados:**

- Os testes CTA-001 a CTA-004 são **totalmente viáveis** e podem ser implementados imediatamente
- Os testes CTA-005 a CTA-008 substituem os testes originais de marcação de conclusão por testes de **visualização de hábitos**, pois a implementação atual usa `input()` que dificulta automação
- Os testes CTA-009 a CTA-012 são **viáveis** e testam a geração de relatórios através do padrão Factory
- Os testes CTA-013 a CTA-016 são **totalmente viáveis** e validam o padrão Singleton do `PDFExporter`
- Todos os cenários foram ajustados para refletir a **implementação real** do sistema, garantindo que possam ser executados sem modificações significativas no código base