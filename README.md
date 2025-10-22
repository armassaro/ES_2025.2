# ES_2025.2

## 1. Primeira ideia do projeto
Sistema de Gerenciamento de Hábitos (Habit Tracker) 
  - **Descrição:**  
  Um app para registrar hábitos diários (ex: estudar, beber água, fazer exercícios), com histórico e relatórios básicos.
    
  - **Funções principais:**  
    O sistema CRUD seria para o controle de hábitos e usuários e as informações ficariam salvas em dois arquivos diferentes.
    
    Cadastro de hábitos (CRUD: criar, editar, excluir).

    Registro diário de progresso (checkboxes ou botões).

    Exibição de relatórios (ex.: gráficos simples de desempenho semanal/mensal).
    
  - **Padrões de projeto aplicáveis:**  
    Observer → atualização automática do painel de relatórios ao registrar progresso.

    MVC (Model-View-Controller) → separar interface, dados e lógica.

    Factory Method → criação de diferentes tipos de relatórios (diário, semanal, mensal).

##  Viabilidade Técnica
A viabilidade técnica do projeto é alta. As funcionalidades descritas são padrão em aplicações modernas e existem inúmeras ferramentas, bibliotecas e frameworks consolidados para implementá-las.

## Definições relacionadas à gerência de qualidade
Abaixo são definidos os padrões de segurança e qualidade, os quais são fatores determinantes para o desenvolvimetno do projeto como um todo. 
### Padrões de segurança
São definidos as seguintes premissas para os padrões de segurança: 
 - O aplicativo deve solicitar apenas as permissões mínimas necessárias para seu funcionamento, evitando acesso a dados ou recursos do dispositivo que não sejam essenciais.
 - Todos os dados sensíveis (tokens, credenciais, informações pessoais) devem ser armazenados de forma segura utilizando mecanismos nativos da plataforma (Android Keystore / iOS Keychain).
 - Toda comunicação entre o app e o servidor deve ocorrer exclusivamente via HTTPS/TLS 1.2 ou superior, garantindo a confidencialidade e integridade das informações transmitidas.
 - O sistema de autenticação deve usar provedores confiáveis, implementando OAuth 2.0 / OpenID Connect para logins via Google, Facebook ou e-mail.
 - O aplicativo deve ser assinado digitalmente e ter suas atualizações testadas e verificadas antes da publicação, prevenindo a introdução de novas vulnerabilidades.
 - Todas as dependências e bibliotecas externas devem ser mantidas atualizadas e provenientes de fontes seguras, evitando o uso de versões vulneráveis ou não mantidas.
 - Nenhum dado sensível deve ser exposto em logs, nem salvo em texto plano, respeitando as normas de privacidade e proteção de dados (como a LGPD).
 - Devem ser realizados testes básicos de segurança (análise estática e dinâmica) para identificar vulnerabilidades simples antes da publicação.
 - O aplicativo deve evitar funcionalidades não autorizadas e garantir que seu comportamento seja transparente e previsível para o usuário.
Todas as funcionalidades apresentadas estão disponíveis no documento de normas de segurança do NIST (National Institute of Standards and Techonology) do departamento de comércio dos Estados Unidos. O respectivo documento possui como título "Vetting the Secutiry of Mobile Applications", foi redigido por Steve Quirolgico, Jeffrey Voas, Tom Karygiannis, Christoph Micheal e Karen Scarfone e está disponível no seguinte link: [http://dx.doi.org/10.6028/NIST.SP.800-163].
