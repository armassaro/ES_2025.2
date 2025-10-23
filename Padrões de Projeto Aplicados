Padrões de Projeto Aplicados
1. Análise dos Requisitos
O sistema proposto é um Habit Tracker com as seguintes funcionalidades principais:

Cadastro de hábitos (CRUD)

Registro diário de progresso

Geração de relatórios de desempenho (gráficos simples)

Os requisitos indicam a necessidade de:

Separação clara entre interface, lógica e dados.

Atualização automática da interface quando novos dados são registrados.

Flexibilidade para criar diferentes tipos de relatórios.

2. Padrões de Projeto Escolhidos
a) MVC (Model-View-Controller)
Justificativa: O MVC será usado para separar a interface do usuário (View), os dados (Model) e a lógica de controle (Controller). Isso facilita a manutenção, o teste e a evolução do sistema.

Aplicação:

Model: Classes Habit e User (armazenam dados).

View: Telas de cadastro, registro de progresso e relatórios.

Controller: Lógica para CRUD de hábitos e geração de relatórios.

b) Observer
Justificativa: Sempre que um hábito é registrado ou atualizado, o painel de relatórios deve ser atualizado automaticamente. O Observer permite essa notificação sem acoplamento rígido.

Aplicação:

O HabitModel atua como Subject.

A ReportView atua como Observer e se atualiza quando o modelo muda.

c) Factory Method
Justificativa: Diferentes tipos de relatórios (diário, semanal, mensal) devem ser gerados de forma flexível. O Factory Method encapsula a criação desses relatórios.

Aplicação:

ReportFactory define o método createReport(type).

Subclasses como DailyReportFactory, WeeklyReportFactory implementam a criação concreta.

3. Diagramas dos Padrões
MVC
text
[View] → [Controller] → [Model]
Observer
text
[HabitModel] --notifica--> [ReportView]
       ↑                      ↑
    (Subject)              (Observer)
Factory Method
text
[ReportFactory] ← [DailyReportFactory, WeeklyReportFactory]
4. Documentação no Código
Cada padrão será devidamente comentado no código, explicando:

O papel de cada classe no padrão.

Como o padrão foi implementado.

Vantagens trazidas para o projeto.
