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

Ian Bacchi Nascimento

Levantamento de Requisitos do Projeto: Sistema de Gerenciamento de Hábitos
1. Objetivo da Pesquisa
O objetivo desta pesquisa é realizar um levantamento de requisitos detalhado para o desenvolvimento de um aplicativo de rastreamento de hábitos. A meta é ir além de uma simples aplicação CRUD, definindo um produto com uma proposta de valor clara e fundamentada em dados de mercado, análise da concorrência e princípios da psicologia comportamental. A pesquisa busca responder a questões estratégicas sobre o mercado, os concorrentes, os fundamentos psicológicos da formação de hábitos, as estratégias de engajamento mais eficazes e os requisitos não funcionais críticos para o sucesso do projeto.
2. Análise de Mercado e Concorrentes
Os principais players no mercado de aplicativos de rastreamento de hábitos incluem Productive, Streaks, Habitica, Habitify e Loop.1 Uma análise comparativa revela as seguintes funcionalidades e lacunas:
Conjunto de Funcionalidades Principais: A maioria dos aplicativos oferece um conjunto básico de funcionalidades, como criação de hábitos, check-in diário, visualização de progresso (gráficos, calendários) e lembretes.3
Diferenciais e Nichos:
Streaks: Focado no ecossistema Apple (iOS), com um design minimalista e forte ênfase no rastreamento de "sequências" (streaks).3
Habitica: Utiliza uma abordagem de gamificação profunda, transformando o rastreamento de hábitos em um jogo de RPG para engajar os usuários.2
Habitify: Destaca-se pela sua disponibilidade multiplataforma (iOS, Android, Web) e foco em análise de dados para usuários que buscam insights detalhados.3
Loop: É uma opção popular para Android, sendo de código aberto, gratuito e focado na privacidade do usuário.5
Lacunas Estratégicas: A principal lacuna identificada é a aplicação, muitas vezes superficial, dos princípios psicológicos. Enquanto muitos apps usam gamificação, poucos estruturam a jornada do usuário em torno de modelos comportamentais comprovados ou educam o usuário sobre o processo de formação de hábitos. Há uma oportunidade para um aplicativo que se posicione como uma ferramenta "cientificamente embasada", oferecendo funcionalidades significativas que vão além de simples recompensas.6
3. Princípios Psicológicos Fundamentais
A formação de hábitos é impulsionada por mecanismos neurológicos e psicológicos que podem ser traduzidos em funcionalidades de software eficazes.
O Loop do Hábito (Deixa, Rotina, Recompensa): Os hábitos se fortalecem pela repetição de uma resposta (rotina) em um contexto estável (deixa), solidificada por um mecanismo de recompensa.8 O aplicativo deve ajudar o usuário a projetar e reforçar esse ciclo.
O Modelo Hook de Nir Eyal: Este é um framework de quatro estágios para criar produtos que formam hábitos 9:
Gatilho (Trigger): Estímulos que iniciam a ação. O aplicativo pode usar gatilhos externos (notificações, lembretes, widgets) para, eventualmente, criar uma associação com gatilhos internos do usuário (sentir-se improdutivo, precisar relaxar).9
Ação (Action): O comportamento mais simples em antecipação a uma recompensa. Para o aplicativo, a ação principal é marcar um hábito como concluído. Essa ação deve ser o mais simples e livre de atrito possível, como um toque em um widget.9
Recompensa Variável (Variable Reward): A imprevisibilidade da recompensa mantém o usuário engajado. O aplicativo deve incorporar três tipos: Recompensas da Tribo (validação social, desafios), Recompensas da Caça (desbloquear insights, dicas) e Recompensas do Eu (maestria, sensação de conclusão ao ver gráficos de progresso ou sequências).9
Investimento (Investment): Quando o usuário investe algo no produto (tempo, dados, esforço), ele aumenta seu compromisso. No aplicativo, isso se traduz em ações como configurar um novo hábito, escrever notas ou personalizar a interface.9
4. Estratégias de Engajamento e Retenção de Usuários
Para combater a baixa retenção a longo prazo, um desafio crítico no mercado 12, estratégias de engajamento baseadas em gamificação e tecnologia são fundamentais.
Conforme aponta uma reportagem recente sobre as tendências do setor, a combinação de inteligência artificial (IA) e gamificação em wearables e aplicativos móveis tem reforçado o engajamento dos usuários. Plataformas como Fitbit e Strava popularizaram desafios diários e recompensas virtuais que incentivam a prática regular de atividades. Uma pesquisa indicou que usuários que participam de desafios em grupo têm 50% mais chances de atingir suas metas. O uso de IA permite uma abordagem mais estratégica, com algoritmos que identificam padrões de comportamento e ajustam as recomendações de forma personalizada.13
As estratégias mais eficazes incluem:
Gamificação Significativa: Em vez de apenas pontos, a gamificação deve alavancar princípios psicológicos. Os elementos mais eficazes são o estabelecimento de metas (78.1%), influências sociais (78.1%) e desafios (62.5%).14
Sequências (Streaks): Alavanca o princípio da "aversão à perda", motivando os usuários pelo medo de quebrar a corrente.3
Conquistas e Distintivos (Badges): Fornecem "Recompensas do Eu", oferecendo um senso de maestria e reconhecimento por marcos alcançados.7
Funcionalidades Sociais: Ativam as "Recompensas da Tribo" através de placares de líderes, desafios em grupo e compartilhamento de progresso, usando a prova social como motivador.7
Notificações Personalizadas: Devem atuar como gatilhos externos eficazes, sendo enviadas em momentos oportunos e com conteúdo relevante para o usuário, a fim de iniciar o "loop do hábito".16
Integração com Wearables: A sincronização com dispositivos vestíveis, como smartwatches, melhora a retenção de usuários em 39%, pois automatiza o rastreamento e integra o hábito ao dia a dia do usuário de forma mais fluida.1
5. Requisitos Não Funcionais Críticos
Privacidade de Dados: A privacidade é um fator decisivo para a adoção. Cerca de 48% dos usuários hesitam em compartilhar dados pessoais, e aplicativos com políticas de privacidade pouco claras registram um engajamento 41% menor.1 Uma política de privacidade forte e transparente, com armazenamento de dados local como padrão, é uma vantagem competitiva fundamental.
Escolha da Plataforma: A decisão entre iOS e Android tem implicações estratégicas. O iOS domina em receita (46% do mercado) e favorece aplicativos premium, enquanto o Android (42% do mercado) tem uma base de usuários maior que prefere modelos gratuitos.1 Uma estratégia inicial focada em uma única plataforma pode ser mais viável.
Usabilidade: A interface deve ser intuitiva e focada em reduzir o atrito para a ação principal (marcar um hábito). Um processo de onboarding simples, que demonstre o valor do aplicativo imediatamente, é crucial para a retenção inicial.16

Fontes de Informação e Critérios de Seleção
Análise de Produtos Concorrentes: Foi realizada uma análise direta dos principais aplicativos (Productive, Streaks, Habitica, Habitify e Loop) através de suas descrições nas lojas de aplicativos, websites oficiais e análises comparativas.
Literatura Acadêmica e Científica: Foram revisados artigos sobre a psicologia da formação de hábitos, mudança de comportamento e a eficácia da gamificação, como os trabalhos de Wood & Runger e revisões sistemáticas sobre o tema.17
Relatórios de Mercado e Reportagens: Foram consultados relatórios de empresas como Straits Research e Global Growth Insights, além de reportagens sobre tendências tecnológicas no setor de saúde digital.1
Critérios de Seleção: As fontes foram escolhidas com base em Atualidade (publicações de 2023 a 2025), Autoridade (fontes com credibilidade reconhecida), Corroboração de Dados (cruzamento de estatísticas) e Relevância para o desenvolvimento do aplicativo.


