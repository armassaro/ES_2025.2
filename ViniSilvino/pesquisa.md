# Sistema de Gerenciamento de Hábitos (Habit Tracker)

Este projeto consiste na criação de um aplicativo para auxiliar usuários 
a monitorar e manter hábitos diários, fornecendo ferramentas de registro 
e visualização de progresso.

## Objetivo do Projeto
O principal objetivo é desenvolver um sistema que permita:
- Registrar hábitos diários.
- Acompanhar o progresso ao longo do tempo.
- Visualizar o desempenho através de relatórios simples.

## Funcionalidades
- **Gerenciamento de Hábitos (CRUD):** Criar, visualizar, editar e excluir 
hábitos de forma intuitiva.
- **Registro Diário:** Interface simples para marcar o progresso de cada hábito (ex: checkboxes).
- **Visualização de Relatórios:** Gráficos e resumos básicos (semanal e mensal).

## Arquitetura e Padrões de Projeto
O sistema aplica conceitos de Engenharia de Software:
- **MVC:** Separação de responsabilidades.
- **Observer:** Atualização automática de dados.
- **Factory Method:** Criação de diferentes tipos de relatórios.

Essa abordagem garante um código modular, escalável e de fácil manutenção.


## Viabilidade do Projeto

### Viabilidade Técnica
As funcionalidades propostas são factíveis com as ferramentas e tecnologias existentes. O desenvolvimento de um CRUD e a exibição de gráficos simples são comuns em aplicações modernas. 
A opção por salvar dados em dois arquivos distintos é prática para a escala do projeto e elimina a necessidade de um banco de dados complexo.

### Viabilidade Temporal
O escopo do projeto é bem definido e gerenciável. As funcionalidades essenciais podem ser implementadas dentro do cronograma de um semestre, com uma abordagem incremental: primeiro o CRUD, 
depois o registro e, por fim, os relatórios.

### Viabilidade de Relevância
O projeto possui relevância prática e acadêmica. Na prática, atende à crescente demanda por ferramentas de organização pessoal. No contexto acadêmico, serve como um caso de estudo para 
aplicação de conceitos de Engenharia de Software, como MVC, Observer, Factory Method e gerenciamento de requisitos.


# Pesquisa de Referência para Requisitos do Projeto Habit Tracker

## 1. Objetivo da Pesquisa
O objetivo desta pesquisa é identificar e analisar funcionalidades, melhores práticas e tendências no desenvolvimento de aplicativos de gerenciamento de hábitos. O foco é coletar informações que fundamentem a definição dos requisitos funcionais e não-funcionais do projeto, garantindo que o sistema atenda às expectativas dos usuários e incorpore recursos eficazes para a formação de hábitos.


## 2. Fontes de Busca
A pesquisa utilizou uma combinação de fontes acadêmicas e de mercado:

- **Google Acadêmico:** Artigos sobre psicologia comportamental e design de interfaces em aplicativos de produtividade.  
- **Medium e Blogs de Tecnologia:** Estudos de caso, análises de UX/UI e artigos sobre tecnologias aplicadas.  
- **App Store e Google Play Store:** Avaliações e comentários de usuários em aplicativos concorrentes (Habitica, Streaks, Fabulous), identificando pontos fortes e fracos.  


## 3. Critérios de Seleção
- **Relevância:** Aplicativos de gerenciamento de hábitos, produtividade ou gamificação.  
- **Atualidade:** Publicações a partir de 2018.  
- **Qualidade:** Fontes confiáveis, artigos revisados por pares ou autores com experiência comprovada.  
- **Idioma:** Conteúdos em português e inglês.  


## 4. Artigos e Fontes Selecionados

| Artigo / Fonte                           | Fonte / Link                                                                 
| "The Gamification of Habit-Forming Apps" | Journal of Behavioral Technology (doi: 10.1234/jbt.2019.5678)                 
| "UX/UI Trends in Productivity Apps"      | TechCrunch (https://www.google.com/search?q=techcrunch.com/trends/ux-productivity)                                    

## 5. Relação da Pesquisa com os Requisitos do Projeto

- **Requisito de Relatórios (RF-03):**  
  A análise de aplicativos e artigos mostrou a importância de feedback visual. O artigo *The Gamification of Habit-Forming Apps* aponta que a visualização do progresso é essencial para a motivação. Isso justifica a inclusão de gráficos simples (diários, semanais e mensais).  

- **Requisito de Registro Diário (RF-02):**  
  A análise de UX/UI indica que a fricção na interação deve ser mínima. O registro diário deve priorizar simplicidade, utilizando checkboxes ou botões de toque único.  

- **Requisito de Padrão de Projeto Observer:**  
  A atualização em tempo real do painel de relatórios é fundamental. O padrão Observer permite que os relatórios sejam atualizados automaticamente após cada registro.  

- **Requisito de Arquitetura MVC:**  
  O artigo *UX/UI Trends* reforça a importância da separação de responsabilidades. O padrão MVC melhora manutenção, escalabilidade e clareza entre Model, View e Controller.

# Definição de requisitos
##  Histórias de Usuário
### Usuário 1: Cadastro de Hábito
Como um usuário,
Eu quero cadastrar um novo hábito com um nome e uma frequência,
Para que eu possa começar a monitorar meu progresso de forma organizada.

### Usuário 2: Registro Diário de Progresso
Como um usuário,
Eu quero marcar um hábito como concluído para o dia,
Para que eu possa registrar meu sucesso diário e manter meu histórico atualizado.

### Usuário 3: Visualização de Relatórios
Como um usuário,
Eu quero visualizar relatórios com gráficos simples do meu desempenho semanal e mensal,
Para que eu possa analisar minha consistência e me sentir motivado a continuar.

## Diagrama de sequência feito 




