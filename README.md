# ES_2025.2

## 1. Ideia do projeto
O presente projeto possui como principal intuito a criação de um sistema de gerenciamento de hábitos com capacidade de criação de conta e acompanhamento da criação e evolução pessoal dos hábitos escolhidos pelo próprio usuário, ao passo que sistemas de gameficação são apresentados na aplicação para incentivo do usuário ao desenvolvimento do hábito.

### 1.1. Descrição
Uma aplicação para registro de hábitos diários (ex: estudar, beber água, fazer exercícios), com histórico e relatórios básicos e mecanismos de incentivo ao desenvolvimetno do hábito, por meio de técnicas de gameficação com base em estudos científicos. 
    
### 1.2. Funções principais
O sistema CRUD seria para o controle de hábitos e usuários e as informações ficariam salvas em dois arquivos diferentes.    
Cadastro de hábitos (CRUD: criar, editar, excluir).
Registro diário de progresso (checkboxes ou botões).
Exibição de relatórios (ex.: gráficos simples de desempenho semanal/mensal).

### 1.3. Padrões de projeto aplicáveis
Os padrões de projeto consistem em várias arquiteturas documentadas e especializadas em determinados tipos de funções para uma aplicação. A seguir, são listados os padrões de projeto utilizados durante o desenvolvimento da aplicação proposta, assim como as referências utilizadas e explicações para a utilização de cada padrão de projeto utilizado para cada função presente na aplicação. Seguem os padrões de projeto utilizados: 

- **Observer** - também conhecido como "Event-Subscriber" ou "Listener", o padrão de projeto Observer funciona a partir de um mecanismo de assinatura com o intuito de notificar um ou mais objetos a respeito de eventos específicos que aconteçam com o objeto que está sendo "observado". O padrão de projeto Observer é composto essencialmente por duas classes, a publicadora e a assinante, onde a classe publicadora contém uma lista de assinantes e métodos como ```subscribe()```, ```unsubscribe()``` e ```notifySubscribers()```, que servem para incluir e remover assinantes e o de enviar notificação para um determinado acontecimento dentro da classe publicadora. Já a classe assinante possui um método ```update()``` que serve para notificação direta da classe publicadora para a classe assinante, onde a classe publicadora irá utilizar o método ```update()``` de forma direta.

atualização automática do painel de relatórios ao registrar progresso.
MVC (Model-View-Controller) → separar interface, dados e lógica.
Factory Method → criação de diferentes tipos de relatórios (diário, semanal, mensal).

##  2. Viabilidade Técnica
A viabilidade técnica do projeto é alta. As funcionalidades descritas são padrão em aplicações modernas e existem inúmeras ferramentas, bibliotecas e frameworks consolidados para implementá-las.

## 3. Definições relacionadas à gerência de qualidade
Abaixo são definidos os padrões de segurança e qualidade, os quais são fatores determinantes para o desenvolvimetno do projeto como um todo. 

### 3.1. Padrões de segurança
Assim como define Sommerville (2019), os padrões de segurança podem ser divididos em padrões de _Safety_ e de _Security_, sendo o primeiro o conjunto de práticas destinadas à prevenção de danos físicos e econômicos, enquanto o segundo destina-se à prevenção de acesso não autorizado ou ataques maliciosos na aplicação.
Deste modo, são definidos as seguintes premissas para os padrões de segurança:
 - O aplicativo deve solicitar apenas as permissões mínimas necessárias para seu funcionamento, evitando acesso a dados ou recursos do dispositivo que não sejam essenciais.
 - O sistema de autenticação deve usar provedores confiáveis, implementando OAuth 2.0 / OpenID Connect para logins via Google, Facebook ou e-mail.
 - O aplicativo deve ser assinado digitalmente e ter suas atualizações testadas e verificadas antes da publicação, prevenindo a introdução de novas vulnerabilidades.
 - Todas as dependências e bibliotecas externas devem ser mantidas atualizadas e provenientes de fontes seguras, evitando o uso de versões vulneráveis ou não mantidas.
 - Nenhum dado sensível deve ser exposto em logs, nem salvo em texto plano, respeitando as normas de privacidade e proteção de dados (como a LGPD).
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

### 3.3. Definições de atividades recorrentes para validação dos padrões propostos
A presente seção possui como intuito a recapitulação e resumo das atitudes a serem tomadas para a contínua validação dos padrões propostos nas seções 3.1 e 3.2, para facilitação e organização de cada reunião semanal do projeto.
Cada reunião semanal será norteada nas seguintes premissas: 
1. Cada membro deverá demonstrar as próprias contribuições feitas desde a última reunião e enviadas ao repositório para todos os outros membros, de forma a explicar no código/documentação e na prática o que foi feito. Devem ser observados os seguintes pontos para cada caso:

> **1.1. Para o caso de código**  
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

> **1.2. Para o caso de documentação**
> - **O commit que trouxe a contribuição para a documentação segue a convenção?**
    Tal ponto deve ser observado para manutenção da legibilidade e organização dos últimos _commits_ submetidos ao repositório.