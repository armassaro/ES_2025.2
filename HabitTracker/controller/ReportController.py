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
        """Implementação do Observer: Chamado quando o HabitModel muda (ex: CRUD ou progresso)."""
        print("\n[Sistema]: Notificação recebida. Atualizando relatórios...")
        self.generate_and_display_all_reports()

    def generate_and_display_all_reports(self):
        """Gera e envia todos os dados de relatório para a View."""
        from model.ReportFactory import ReportFactory
        
        raw_data = self.model.get_user_data()
        if raw_data is None:
            return  # Não gera relatório se não houver usuário

        # Usa o Factory Method para gerar os relatórios (Factory Client)
        daily_report = ReportFactory.create_report("daily", raw_data)
        weekly_report = ReportFactory.create_report("weekly", raw_data)
        monthly_report = ReportFactory.create_report("monthly", raw_data)

        # Prepara dados para a View
        report_data = {
            "daily": daily_report.generate_visualization_data(),
            "weekly": weekly_report.generate_visualization_data(),
            "monthly": monthly_report.generate_visualization_data(),
        }

        self.view.render_reports(report_data)