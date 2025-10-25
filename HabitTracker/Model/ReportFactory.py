from abc import ABC, abstractmethod

# --- PADRÃO FACTORY METHOD (Para criação de relatórios) ---

class Report(ABC):
    """Produto (Product): Interface comum para todos os relatórios."""
    @abstractmethod
    def generate_visualization_data(self):
        """Método para formatar os dados para exibição no gráfico."""
        pass


class DailyReport(Report):
    """Produto Concreto: Relatório Diário."""
    def __init__(self, raw_data):
        self.raw_data = raw_data
        # Lógica de formatação diária

    def generate_visualization_data(self):
        print("Gerando dados de visualização Diária...")
        # Lógica de cálculo e retorno dos dados diários
        return {"period": "Daily", "data": self.raw_data}


class WeeklyReport(Report):
    """Produto Concreto: Relatório Semanal."""
    def __init__(self, raw_data):
        self.raw_data = raw_data
        # Lógica de formatação semanal

    def generate_visualization_data(self):
        print("Gerando dados de visualização Semanal...")
        # Lógica de cálculo e retorno dos dados semanais
        return {"period": "Weekly", "data": self.raw_data}


class MonthlyReport(Report):
    """Produto Concreto: Relatório Mensal."""
    def __init__(self, raw_data):
        self.raw_data = raw_data
        # Lógica de formatação mensal

    def generate_visualization_data(self):
        print("Gerando dados de visualização Mensal...")
        # Lógica de cálculo e retorno dos dados mensais
        return {"period": "Monthly", "data": self.raw_data}


class ReportFactory:
    """Factory: Cria diferentes tipos de relatórios."""
    
    @staticmethod
    def create_report(report_type: str, raw_data):
        """
        Cria um relatório com base no tipo especificado.
        
        Args:
            report_type: Tipo do relatório ('daily', 'weekly', 'monthly')
            raw_data: Dados brutos para gerar o relatório
            
        Returns:
            Instância de Report (DailyReport, WeeklyReport ou MonthlyReport)
            
        Raises:
            ValueError: Se o tipo de relatório for desconhecido
        """
        if report_type == "daily":
            return DailyReport(raw_data)
        elif report_type == "weekly":
            return WeeklyReport(raw_data)
        elif report_type == "monthly":
            return MonthlyReport(raw_data)
        else:
            raise ValueError(f"Tipo de relatório desconhecido: {report_type}")