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
> - [5. Novas funcionalidades](#5-novas-funcionalidades)
>   - [5.1. Customização de cores para hábitos](#51-customização-de-cores-para-hábitos)
>   - [5.2. Relatórios com intervalo de tempo customizado](#52-relatórios-com-intervalo-de-tempo-customizado)
> - [6. Correções de bugs e refatorações](#6-correções-de-bugs-e-refatorações)
>   - [6.1. Bugs corrigidos](#61-bugs-corrigidos)
>   - [6.2. Refatorações implementadas](#62-refatorações-implementadas)

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

Os testes automatizados são uma coleção de scripts programados para testar as funcionalidades do projeto de forma automática e em larga escala, de forma com que seja possível economizar tempo. O sistema utiliza o framework **pytest** para implementação e execução dos testes unitários, garantindo cobertura abrangente das funcionalidades principais da aplicação.

**Estrutura de Testes Implementada:**

A suite de testes está organizada em três módulos principais localizados na pasta `HabitTracker/tests/`:
- `test_habit_crud.py` - Testes de CRUD de hábitos (Arthur)
- `test_habit_visualization.py` - Testes de visualização e listagem (Ian)
- `test_report_generation.py` - Testes de geração de relatórios (Silvino)

**Padrão de Nomenclatura e Assinatura:**

Todos os métodos de teste seguem o padrão de nomenclatura `test_cta_XXX_descricao_breve`, onde XXX corresponde ao identificador do cenário de teste (CTA-001 a CTA-018). Cada método de teste possui a seguinte estrutura de assinatura:

```python
@pytest.mark.<categoria>
def test_cta_XXX_descricao(self, clean_json_files, sample_habit_data=None):
    """
    CTA-XXX: Título do cenário
    
    Dado que: [pré-condição]
    Quando: [ação executada]
    Então: [resultado esperado]
    """
```

Os testes utilizam **fixtures pytest** definidas em `conftest.py` para garantir isolamento e consistência:
- `clean_json_files`: Limpa os arquivos JSON antes de cada teste
- `sample_habit_data`: Fornece dados de exemplo para testes de criação

**Configuração e Inicialização:**

Cada classe de teste implementa o método `setup_method()` que é executado antes de cada teste individual, garantindo um estado limpo e consistente. Este método realiza:
1. Criação e autenticação de usuário de teste
2. Inicialização de `HabitModel` e `UserModel`
3. Configuração de controladores necessários

**Validações e Assertions:**

Os testes utilizam assertions do pytest para validar:
- Valores de retorno (tuplas `(success, message)` dos métodos do modelo)
- Estado do sistema após operações
- Persistência de dados no arquivo JSON
- Estrutura e conteúdo dos objetos retornados

**Execução dos Testes:**

Os testes podem ser executados individualmente ou em conjunto através do script `run_all_test.py`, que executa sequencialmente todos os módulos de teste e gera um resumo consolidado dos resultados. Os resultados são salvos na pasta `test_reports/` em formato texto e HTML para análise posterior.

Os scripts de teste da aplicação estão presentes na pasta `HabitTracker/tests/` e os resultados da execução destes scripts estão disponíveis em `HabitTracker/test_reports/`. Abaixo se encontram os cenários de teste que os scripts automatizados implementam:

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
| **CTA-013** | O sistema possui 3 hábitos ativos com histórico distribuído no período de `2025-11-01` a `2025-11-15` (15 dias): `h001` concluído em 10 dias consecutivos, `h002` concluído em 7 dias alternados, `h003` concluído em 5 dias específicos | O teste automatizado chama `ReportFactory.create_report("custom", raw_data, "2025-11-01", "2025-11-15")` e obtém `report.generate_visualization_data()` | O relatório retorna estrutura com `start_date="2025-11-01"`, `end_date="2025-11-15"`, `total_days=15`, `total_completed=22`, campos `average_per_day`, `max_streak>=10`, `completion_rate`, `best_day`, `best_day_count` e `daily_data` com 15 entradas corretas |
| **CTA-014** | O sistema está inicializado com `HabitModel` e hábitos cadastrados | O teste automatizado tenta chamar `ReportFactory.create_report("custom", raw_data, "2025-11-15", "2025-11-01")` com data final anterior à data inicial | O método levanta `ValueError` com mensagem contendo "data final não pode ser menor que a data inicial", nenhum relatório é gerado e o sistema permanece estável |
| **CTA-015** | O sistema possui 2 hábitos ativos mas com histórico apenas em `2025-12-01` e `2025-12-02`, e o teste solicita período de `2024-01-01` a `2024-01-31` (período passado sem dados) | O teste automatizado chama `ReportFactory.create_report("custom", raw_data, "2024-01-01", "2024-01-31")` | O relatório retorna estrutura válida com `total_completed=0`, `completion_rate=0.0`, `max_streak=0`, `total_days=31`, e todos os 31 dias em `daily_data` com `completed=0` |
| **CTA-016** | O sistema possui 2 hábitos ativos com histórico extenso de 90 dias: `h001` concluído todos os dias, `h002` concluído a cada 3 dias | O teste automatizado gera relatórios customizados para períodos de 1 dia, 7 dias, 30 dias e 90 dias usando datas específicas | Todos os 4 relatórios retornam estrutura válida, cada um com `total_days` correto (1, 7, 31, 91 respectivamente), campos de estatísticas calculados corretamente, e `daily_data` com número de entradas correspondente ao período |
| **CTA-017** | O sistema possui 2 hábitos ativos com histórico no período `2025-11-01` a `2025-11-10`, e `ReportController` está configurado com `HabitModel` e `ConsoleView` | O teste automatizado chama `report_controller.generate_custom_report("2025-11-01", "2025-11-10")` | O método retorna tupla `(True, mensagem_sucesso, report_data)`, onde `mensagem_sucesso` contém "sucesso" ou "gerado", `report_data` é dicionário não-nulo com `start_date="2025-11-01"`, `end_date="2025-11-10"`, `total_days=10` e estatísticas corretas |
| **CTA-018** | O sistema está inicializado com hábitos cadastrados | O teste automatizado tenta chamar `ReportFactory.create_report("custom", raw_data, None, None)`, depois `("custom", raw_data, None, "2025-11-15")`, e depois `("custom", raw_data, "2025-11-01", None)` | Todos os 3 casos levantam `ValueError` com mensagem contendo "obrigatórios" ou "required", nenhum relatório é gerado em nenhum dos casos, e o sistema permanece estável |

---

## 5. Novas funcionalidades
Foram incluídas novas funcionalidades para a terceira entrega do projeto, visando aprimorar a experiência do usuário e expandir as capacidades analíticas do sistema. As funcionalidades implementadas são detalhadas a seguir:

### 5.1. Customização de cores para hábitos

A funcionalidade de customização de cores permite que o usuário personalize visualmente seus hábitos na interface gráfica, atribuindo cores específicas a cada card de hábito. Esta funcionalidade foi desenvolvida com o objetivo de facilitar a identificação visual rápida dos hábitos e permitir que o usuário organize seus hábitos por categorias através de um esquema de cores personalizado.

A personalização visual dos hábitos através de cores melhora significativamente a experiência do usuário ao permitir uma organização visual mais intuitiva. Por exemplo, o usuário pode escolher cores quentes (vermelho, laranja) para hábitos relacionados à saúde física, cores frias (azul, roxo) para hábitos mentais e intelectuais, e cores vibrantes (verde, amarelo) para hábitos sociais ou recreativos. Esta categorização visual auxilia na navegação rápida pela lista de hábitos e torna a interface mais agradável e personalizada.

A funcionalidade foi implementada através de modificações em três componentes principais do sistema:

1. **HabitModel** (`model/HabitModel.py`): Foi adicionado o atributo `color` ao modelo de dados do hábito, permitindo o armazenamento da preferência de cor escolhida pelo usuário. Este atributo é persistido no arquivo `habitos_registros.json` junto com os demais dados do hábito, garantindo que a escolha de cor seja mantida entre sessões da aplicação.

2. **HabitController** (`controller/HabitController.py`): O método `handle_update_habit_request()` foi estendido para aceitar e processar o parâmetro `color`, permitindo que as requisições de atualização de hábitos incluam a modificação da cor. O controlador valida e repassa esta informação ao modelo de forma consistente com a arquitetura MVC.

3. **MainWindow** (`view/gui/MainWindow.py`): A interface gráfica foi expandida significativamente para suportar a seleção de cores. No diálogo de edição de hábitos (`_edit_habit()`), foi adicionada uma seção dedicada à seleção de cor contendo oito opções pré-definidas (branco, azul, verde, vermelho, roxo, amarelo, laranja e rosa), cada uma representada por um RadioButton com emoji correspondente. Um componente de preview foi implementado para exibir em tempo real a cor selecionada, proporcionando feedback visual imediato ao usuário. A classe `HabitCard` foi modificada para aplicar a cor escolhida ao background do card, utilizando o dicionário `CARD_COLORS` que mapeia nomes de cores para seus códigos hexadecimais correspondentes.

### 5.2. Relatórios com intervalo de tempo customizado

A funcionalidade de relatórios customizados permite que o usuário gere análises de progresso para períodos de tempo específicos, complementando os relatórios predefinidos (diário, semanal e mensal). Esta funcionalidade foi desenvolvida para atender necessidades específicas de análise temporal que os períodos fixos não contemplam.

Relatórios com intervalos customizados são fundamentais para análises mais flexíveis e direcionadas do progresso do usuário. Por exemplo, o usuário pode desejar analisar seu desempenho durante um período de férias específico, avaliar o impacto de uma mudança de rotina ocorrida em datas específicas, ou comparar seu progresso em diferentes quinzenas do mês. Esta funcionalidade permite análises retrospectivas precisas para qualquer período de interesse, tornando o sistema mais adaptável às necessidades individuais de cada usuário.

A funcionalidade foi implementada através de modificações e adições em múltiplos componentes do sistema:

1. **ReportFactory** (`model/ReportFactory.py`): Foi criada a classe `CustomReport` que estende a hierarquia de relatórios existente. Esta classe implementa a lógica de cálculo de estatísticas para períodos arbitrários definidos pelo usuário através dos parâmetros `start_date` e `end_date`. O método `create_report()` da factory foi estendido para suportar o tipo `'custom'`, incluindo validações rigorosas das datas fornecidas (formato, ordem cronológica, obrigatoriedade dos parâmetros). A classe `CustomReport` calcula métricas abrangentes incluindo: total de dias no período, total de hábitos concluídos, média diária de conclusões, maior sequência de dias consecutivos, taxa de conclusão percentual, melhor dia do período (com maior número de conclusões), e dados diários detalhados para cada data no intervalo especificado.

2. **ReportController** (`controller/ReportController.py`): Foi adicionado o método `generate_custom_report(start_date, end_date)` que coordena a geração de relatórios customizados. Este método recebe as datas de início e fim como strings, valida os parâmetros, interage com o `HabitModel` para obter os dados necessários, invoca a `ReportFactory` para criar o relatório do tipo custom, e notifica a view apropriada com os dados gerados. O método implementa tratamento de erros robusto, retornando tuplas `(success, message, data)` que permitem à interface gráfica apresentar mensagens claras ao usuário em caso de sucesso ou falha.

## 6. Correções de bugs e refatorações

Esta seção documenta os bugs identificados e corrigidos na aplicação, bem como as refatorações implementadas para melhorar a qualidade, manutenibilidade e desempenho do código.

### 6.1. Bugs corrigidos

Durante a análise do código, foram identificados e corrigidos três bugs críticos que afetavam a funcionalidade e estabilidade da aplicação:

#### Bug #1: Erro de codificação Unicode no HabitModel.py

**Descrição do problema:**
O arquivo `HabitModel.py` utilizava emojis (⚠️) em mensagens de log nas linhas 82, 140, 160, 167 e 177. No ambiente Windows com console PowerShell, estes caracteres especiais Unicode causavam exceção `UnicodeEncodeError: 'charmap' codec can't encode characters`, impedindo a execução dos testes automatizados e causando crashes durante a operação normal do sistema.

**Impacto:**
- Falha completa na execução de testes automatizados
- Impossibilidade de debug através de mensagens de log
- Experiência degradada do usuário em ambientes Windows

**Solução implementada:**
Todos os emojis foram substituídos por prefixos ASCII entre colchetes:
- `⚠️` → `[AVISO]`
- `✅` → `[INFO]`
- `📊` → `[INFO]`

Esta mudança garante compatibilidade total com todos os sistemas operacionais e codificações de console, mantendo a clareza das mensagens de log.

**Arquivos modificados:**
- `HabitTracker/model/HabitModel.py` (linhas 82, 96-105, 140, 160-177)

**Código corrigido:**
```python
# Antes:
print(f"⚠️ Model: Usuário não encontrado")

# Depois:
print(f"[AVISO] Model: Usuario nao encontrado")
```

---

#### Bug #2: Valor de retorno ignorado na autenticação automática

**Descrição do problema:**
No arquivo `ConsoleView.py`, linha 43, após a criação bem-sucedida de um novo usuário, o sistema tentava fazer login automático chamando `self.user_model.authenticate(username, password)`, porém o valor de retorno da função (tupla `(success, message)`) não era capturado nem verificado. Isso causava dois problemas:
1. Se a autenticação falhasse silenciosamente, o usuário acreditaria estar logado quando não estava
2. Não havia feedback ao usuário sobre o status do login automático

**Impacto:**
- Estado inconsistente da aplicação
- Experiência confusa para o usuário
- Potencial acesso negado em operações subsequentes

**Solução implementada:**
O código foi refatorado para capturar o retorno da função `authenticate()` e tratar ambos os casos (sucesso e falha):

```python
# Antes:
if success:
    self.show_message(message)
    self.user_model.authenticate(username, password)
    return True

# Depois:
if success:
    self.show_message(message)
    auth_success, auth_message = self.user_model.authenticate(username, password)
    if auth_success:
        self.show_message(auth_message)
        return True
    else:
        self.show_error(f"Erro ao fazer login automático: {auth_message}")
        return False
```

**Arquivos modificados:**
- `HabitTracker/view/ConsoleView.py` (linhas 38-47)

---

#### Bug #3: Potencial divisão por zero em cálculo de taxas de conclusão

**Descrição do problema:**
No arquivo `ReportFactory.py`, o cálculo da taxa de conclusão (`completion_rate`) utilizava uma expressão ternária que verificava se `total_habits > 0`, mas retornava `0` (inteiro) em vez de `0.0` (float). Embora tecnicamente não causasse divisão por zero, esta inconsistência de tipos poderia cauar problemas em operações subsequentes que esperassem sempre valores float. Além disso, não havia validação adicional em outros pontos do código para garantir que operações matemáticas sempre tivessem denominadores não-zero.

**Impacto:**
- Inconsistência de tipos de retorno
- Potencial para erros em cálculos subsequentes
- Falta de robustez em edge cases

**Solução implementada:**
O código foi modificado para garantir retorno consistente do tipo float e adicionar comentário explicativo:

```python
# Antes:
completion_rate = round((completed_today / total_habits * 100), 1) if total_habits > 0 else 0

# Depois:
# Fix: Prevent division by zero and ensure float type consistency
completion_rate = round((completed_today / total_habits * 100), 1) if total_habits > 0 else 0.0
```

Adicionalmente, foi incluída validação preventiva no método `_migrate_data_add_color()` do `HabitModel.py` para evitar salvamento desnecessário de dados vazios:

```python
if self.data:  # Only save if there's data to save
    save_data(HABIT_DATA_FILE, self.data)
```

**Arquivos modificados:**
- `HabitTracker/model/ReportFactory.py` (linha 61)
- `HabitTracker/model/HabitModel.py` (linha 53)

---

### 6.2. Refatorações implementadas

Foram realizadas refatorações significativas para melhorar a qualidade, legibilidade e manutenibilidade do código. Abaixo estão documentadas as 4 principais refatorações:

#### Refatoração #1: Extração de métodos auxiliares no HabitController

**Motivação:**
O `HabitController` continha código repetitivo para logging de ações e detalhes em múltiplos métodos, violando o princípio DRY (Don't Repeat Yourself). Mensagens de debug estavam espalhadas e inconsistentes.

**Implementação:**
Foram extraídos dois métodos auxiliares privados para centralizar a lógica de logging:

```python
def _log_action(self, message):
    """Método auxiliar para logging centralizado."""
    print(f"[CONTROLLER] {message}")

def _log_details(self, details):
    """Método auxiliar para logging de detalhes."""
    for key, value in details.items():
        if value is not None:
            print(f"   - {key}: {value}")
```

**Benefícios:**
- Redução de duplicação de código
- Consistência em mensagens de log
- Facilidade para modificar formato de logging no futuro
- Melhor separação de responsabilidades

**Arquivo modificado:**
- `HabitTracker/controller/HabitController.py`

---

#### Refatoração #2: Melhorias na validação e documentação do UserModel

**Motivação:**
O método `create_user()` não validava adequadamente as entradas do usuário, permitindo a criação de contas com nomes vazios ou senhas fracas. A documentação dos métodos era insuficiente.

**Implementação:**
Foram adicionadas validações de entrada robustas e documentação completa:

```python
def create_user(self, username: str, password: str) -> Tuple[bool, str]:
    """
    Cria um novo usuário no sistema.
    
    Args:
        username: Nome de usuário único
        password: Senha do usuário
    
    Returns:
        Tupla (sucesso, mensagem)
    """
    # Validação de entrada
    if not username or not password:
        return False, "Erro: Nome de usuário e senha são obrigatórios."
    
    if len(username) < 3:
        return False, "Erro: Nome de usuário deve ter pelo menos 3 caracteres."
    
    if len(password) < 4:
        return False, "Erro: Senha deve ter pelo menos 4 caracteres."
    
    # ... resto do código
```

Além disso, foi adicionado campo `created_at` aos usuários para rastreabilidade:

```python
self.users[user_id] = {
    'username': username, 
    'password': password, 
    'id': user_id,
    'created_at': datetime.now().isoformat()
}
```

**Benefícios:**
- Maior segurança e integridade dos dados
- Melhor experiência do usuário com mensagens de erro claras
- Rastreabilidade de quando usuários foram criados
- Documentação completa facilitando manutenção

**Arquivo modificado:**
- `HabitTracker/model/UserModel.py`

---

#### Refatoração #3: Validação de entrada no método create_habit

**Motivação:**
O método `create_habit()` do `HabitModel` aceitava nomes vazios ou com espaços, e não validava o parâmetro `frequency`, permitindo valores inválidos que poderiam causar bugs em outras partes do sistema.

**Implementação:**
Adicionadas validações completas de entrada com mensagens de erro específicas:

```python
def create_habit(self, name, description="", frequency="daily"):
    """
    Cria um novo hábito (R1 - Create).
    
    Args:
        name: Nome do hábito
        description: Descrição do hábito (opcional)
        frequency: Frequência do hábito ('daily', 'weekly', 'monthly')
    
    Returns:
        Tupla (sucesso, mensagem)
    """
    # Validação de entrada
    if not name or not name.strip():
        return False, "Nome do hábito não pode estar vazio."
    
    valid_frequencies = ['daily', 'weekly', 'monthly']
    if frequency not in valid_frequencies:
        return False, f"Frequência inválida. Use: {', '.join(valid_frequencies)}"
    
    # ... resto do código com name.strip() e description.strip()
```

**Benefícios:**
- Prevenção de dados inválidos no sistema
- Melhor qualidade dos dados persistidos
- Mensagens de erro claras para o usuário
- Documentação completa do contrato da função

**Arquivo modificado:**
- `HabitTracker/model/HabitModel.py`

---

#### Refatoração #4: Melhoria na documentação do método authenticate

**Motivação:**
O método `authenticate()` do `UserModel` não possuía validação de entrada nem documentação adequada, tornando seu uso menos claro e potencialmente inseguro.

**Implementação:**
Adicionada validação de entrada e documentação completa:

```python
def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
    """
    Autentica um usuário no sistema.
    
    Args:
        username: Nome de usuário
        password: Senha
    
    Returns:
        Tupla (sucesso, mensagem)
    """
    if not username or not password:
        return False, "Erro: Nome de usuário e senha são obrigatórios."
    
    for user_id, user_data in self.users.items():
        if user_data['username'] == username and user_data['password'] == password:
            self.logged_in_user_id = user_id
            return True, f"Usuário '{username}' logado com sucesso."
    return False, "Erro: Credenciais inválidas."
```

**Benefícios:**
- Prevenção de tentativas de login com campos vazios
- Documentação clara do comportamento esperado
- Melhor tratamento de edge cases
- Código mais robusto e defensivo

**Arquivo modificado:**
- `HabitTracker/model/UserModel.py`

---

3. **MainWindow** (`view/gui/MainWindow.py`): Foi implementado o método `_setup_custom_report_tab()` que adiciona uma nova aba "Personalizado" à janela de relatórios. Esta aba contém campos de entrada para data inicial e final (com valores padrão sugeridos: 30 dias atrás até hoje), um botão para gerar o relatório, e uma área dinâmica para exibição dos resultados. O método `generate_custom_report()` processa a requisição do usuário, valida o formato das datas inseridas (YYYY-MM-DD), invoca o `ReportFactory` para criar o relatório customizado, e apresenta os resultados de forma estruturada incluindo texto descritivo e, quando a biblioteca matplotlib está disponível, um gráfico de barras mostrando o percentual de conclusão diário ao longo do período selecionado.