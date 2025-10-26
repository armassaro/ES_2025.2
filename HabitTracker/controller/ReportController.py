from abc import ABC, abstractmethod

class Observer(ABC):
    """Observador (Observer): O ReportController implementará esta interface."""
    @abstractmethod
    def update(self, subject):
        """Recebe a notificação de atualização do sujeito."""
        pass


class ReportController(Observer):
    """Controller de Relatório: Lógica de geração de relatórios (R3). É um Observer."""
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.attach(self)  # Registra-se como observador

    def update(self, subject):
        """Implementação do Observer: Chamado quando o HabitModel muda."""
        print("\n[Sistema]: ✅ Notificação recebida do HabitModel")
        # NÃO gerar relatórios automaticamente na GUI
        # self.generate_and_display_all_reports()

    def generate_and_display_all_reports(self):
        """Gera e envia todos os dados de relatório para a View."""
        from model.ReportFactory import ReportFactory
        
        raw_data = self.model.get_all_habits()
        
        if not raw_data:
            print("⚠️ Nenhum hábito cadastrado ainda.")
            return

        daily_report = ReportFactory.create_report("daily", raw_data)
        weekly_report = ReportFactory.create_report("weekly", raw_data)
        monthly_report = ReportFactory.create_report("monthly", raw_data)

        report_data = {
            "daily": daily_report.generate_visualization_data(),
            "weekly": weekly_report.generate_visualization_data(),
            "monthly": monthly_report.generate_visualization_data(),
        }

        self.view.render_reports(report_data)
        self._display_console_reports(report_data)
    
    def _display_console_reports(self, report_data):
        """Exibe os relatórios no console de forma formatada."""
        print("\n" + "="*60)
        print("📊 RELATÓRIOS DE PROGRESSO")
        print("="*60)
        
        # Relatório Diário
        print("\n📈 RELATÓRIO DIÁRIO")
        print("─"*60)
        daily = report_data['daily']
        print(f"📅 Data: {daily['date']}")
        print(f"✅ Concluídos: {daily['completed']}/{daily['total_habits']}")
        print(f"📊 Taxa: {daily['completion_rate']}%")
        
        print("\nDetalhes:")
        for habit in daily['habits_detail']:
            print(f"  {habit['status']} {habit['name']}")
        
        # Relatório Semanal
        print("\n" + "─"*60)
        print("📈 RELATÓRIO SEMANAL")
        print("─"*60)
        weekly = report_data['weekly']
        print(f"📅 Período: {weekly['start_date']} a {weekly['end_date']}")
        print(f"✅ Total Concluído: {weekly['total_completed']}")
        print(f"📊 Média por Dia: {weekly['average_per_day']}")
        print(f"🔥 Sequência Atual: {weekly['current_streak']} dias")
        print(f"📈 Taxa de Conclusão: {weekly['completion_rate']}%")
        print(f"🏆 Melhor Dia: {weekly['best_day']} ({weekly['best_day_count']} hábitos)")
        
        print("\nProgresso Diário:")
        for date, day_data in sorted(weekly['daily_data'].items()):
            completed = day_data['completed']
            total = day_data['total']
            percent = (completed / total * 100) if total > 0 else 0
            print(f"  {date}: {completed}/{total} ({percent:.1f}%)")
        
        # Relatório Mensal
        print("\n" + "─"*60)
        print("📈 RELATÓRIO MENSAL")
        print("─"*60)
        monthly = report_data['monthly']
        print(f"📅 Período: {monthly['start_date']} a {monthly['end_date']}")
        print(f"✅ Total Concluído: {monthly['total_completed']}")
        print(f"📊 Média por Dia: {monthly['average_per_day']}")
        print(f"🔥 Maior Sequência: {monthly['max_streak']} dias")
        print(f"📈 Taxa de Conclusão: {monthly['completion_rate']}%")
        print(f"🏆 Melhor Semana: {monthly['best_week_start']} ({monthly['best_week_count']} hábitos)")
        
        print("\nResumo por Semana:")
        for week in monthly['weekly_summary']:
            period = f"{week['dates'][0]} a {week['dates'][-1]}"
            print(f"  {week['week']}: {week['completed']} hábitos ({period})")
        
        print("\n" + "="*60)