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
