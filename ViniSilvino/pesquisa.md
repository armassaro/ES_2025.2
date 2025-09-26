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

# Entrevista feita
## Principais pontos
### 1: Dificuldades para mantes um hábito 
O entrevistado fala sobre a dificuldade de se manter persistente em seu objetivo (academia)

### 2: Sistema de bonificação
Sobre como nosso cérebro usa de estimulo um certo tipo de troca.

### 3: Comparação com outros como incentivo 
Assim como um sistema de gameficação, que é um tipo de comparação com outros.

## Transcrição da entrevista:
-Para a matéria de engenharia de software, estou aqui com o Lucas Dutra, que vai ser feita a entrevista. Primeiramente, queria agradecer o seu tempo, Lucas, e começar as perguntas. Você já tentou criar algum hábito novo? E como foi essa experiência? 
-Ah, já, tipo, ir para a academia, por exemplo, e foi uma experiência boa, porque depois eu peguei o costume de ir, peguei gosto pela academia, e é isso. 
-E quanto tempo você acha que leva para realmente virar um hábito? Então, dizem que tem aquela parada dos 21 dias, que se você conseguir fazer, tipo, por 21 dias alguma coisa, você cria esse hábito, mas não sei, eu acho que varia de cada pessoa, mas no geral, sei lá, um mês, por aí. 
-E o que mais te atrapalha quando você tenta manter um hábito novo? 
-Ah, eu acho que, tipo, quando tem alguma quebra na sua rotina, assim, sei lá, por exemplo, no meu caso de academia, quando tem alguma viagem para fazer, ou surge algum imprevisto no dia, algum trabalho para fazer e tal, isso acaba atrapalhando. 
-E o que te ajuda a não desistir quando você falha um dos dias? 
-Ah, eu acho que pensar em, tipo assim, que eu posso até falhar um dia, mas eu não posso falhar dois. 
-E o que você acha mais fácil, trocar um hábito ruim por outro bom, ou só tentar parar o ruim mesmo? 
-Ah, eu acho que trocar, né, com certeza é mais intuitivo, assim, para o nosso cérebro. 
-E sobre motivação, você acha que ficar repetindo a mesma coisa todo dia, ou ficar variando? O que você acha que é melhor para você? 
-Pô, é que depende muito do hábito, né, às vezes tem hábito que não dá para variar, mas se der, com certeza, acho que variar um pouco ajuda, né, tipo, por exemplo, sei lá, uma dieta, dar uma variadinha na dieta, acho que ajuda a manter, tipo, porque, sei lá, comer a mesma coisa todo dia é complicado, né. 
-E seu sistema de recompensa, como que você faz para ele funcionar? Fale a verdade, Lucas. 
-Ah, às vezes a gente se sabota um pouquinho, né, tipo assim, sei lá, pensar, tipo assim, pô, tem que estudar hoje para tomar uma no final do dia, né. 
-E você prefere só ver o seu próprio progresso ou ver mais gente como se fosse uma competição, uma coisa mais mental aí? Ah, acho que um pouco dos dois, né, tipo, querendo ou não, ajuda um pouco você querer competir com alguém ali, tipo, sei lá, ficar maior que um cara da academia, ou melhorar num esporte com seu amigo, mas é um pouco dos dois mesmo. 
-E por último aqui, o que você faz para continuar um hábito mesmo depois que aquela empolgação inicial passa? 
-Então, eu acho que, tipo assim, se passou aquela empolgação inicial, você já criou o hábito, né, assim, tipo, na academia, por exemplo. Hoje em dia virou um hábito mesmo, meu, então não tem mais aquela empolgação, mas eu vou porque eu gosto e porque virou um hábito. 
-Pô, perfeito, Lucas, muito obrigado.

