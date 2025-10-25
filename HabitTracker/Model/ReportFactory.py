from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import defaultdict

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
        self.raw_data = raw_data  # Lista de hábitos com histórico

    def generate_visualization_data(self):
        """Calcula estatísticas do dia atual."""
        today = datetime.now().strftime('%Y-%m-%d')
        
        total_habits = len(self.raw_data)
        completed_today = 0
        pending_today = 0
        
        habits_detail = []
        
        for habit in self.raw_data:
            if not habit.get('active', True):
                continue
                
            habit_name = habit['name']
            history = habit.get('history', {})
            
            if today in history and history[today]:
                completed_today += 1
                status = "✅ Concluído"
            else:
                pending_today += 1
                status = "⏳ Pendente"
            
            habits_detail.append({
                'name': habit_name,
                'status': status,
                'completed': today in history and history[today]
            })
        
        completion_rate = (completed_today / total_habits * 100) if total_habits > 0 else 0
        
        return {
            "period": "Diário",
            "date": today,
            "total_habits": total_habits,
            "completed": completed_today,
            "pending": pending_today,
            "completion_rate": round(completion_rate, 1),
            "habits_detail": habits_detail
        }


class WeeklyReport(Report):
    """Produto Concreto: Relatório Semanal."""
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def generate_visualization_data(self):
        """Calcula estatísticas dos últimos 7 dias."""
        today = datetime.now()
        week_data = defaultdict(lambda: {'completed': 0, 'total': 0})
        
        # Últimos 7 dias
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        
        total_active_habits = sum(1 for h in self.raw_data if h.get('active', True))
        
        for date in dates:
            week_data[date]['total'] = total_active_habits
            
            for habit in self.raw_data:
                if not habit.get('active', True):
                    continue
                    
                history = habit.get('history', {})
                if date in history and history[date]:
                    week_data[date]['completed'] += 1
        
        # Calcular médias e streak
        total_completed = sum(day['completed'] for day in week_data.values())
        average_per_day = total_completed / 7 if len(dates) > 0 else 0
        
        # Calcular streak (dias consecutivos)
        current_streak = 0
        for date in reversed(dates):
            if week_data[date]['completed'] >= (week_data[date]['total'] * 0.5):  # 50% ou mais
                current_streak += 1
            else:
                break
        
        # Melhor dia
        best_day = max(dates, key=lambda d: week_data[d]['completed'])
        
        return {
            "period": "Semanal",
            "start_date": dates[0],
            "end_date": dates[-1],
            "total_active_habits": total_active_habits,
            "total_completed": total_completed,
            "average_per_day": round(average_per_day, 1),
            "current_streak": current_streak,
            "best_day": best_day,
            "best_day_count": week_data[best_day]['completed'],
            "daily_data": {date: week_data[date] for date in dates},
            "completion_rate": round((total_completed / (total_active_habits * 7) * 100) if total_active_habits > 0 else 0, 1)
        }


class MonthlyReport(Report):
    """Produto Concreto: Relatório Mensal."""
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def generate_visualization_data(self):
        """Calcula estatísticas dos últimos 30 dias."""
        today = datetime.now()
        month_data = defaultdict(lambda: {'completed': 0, 'total': 0})
        
        # Últimos 30 dias
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
        
        total_active_habits = sum(1 for h in self.raw_data if h.get('active', True))
        
        for date in dates:
            month_data[date]['total'] = total_active_habits
            
            for habit in self.raw_data:
                if not habit.get('active', True):
                    continue
                    
                history = habit.get('history', {})
                if date in history and history[date]:
                    month_data[date]['completed'] += 1
        
        # Estatísticas gerais
        total_completed = sum(day['completed'] for day in month_data.values())
        average_per_day = total_completed / 30
        
        # Melhor semana (últimos 7 dias com mais conclusões)
        best_week_start = 0
        best_week_count = 0
        
        for i in range(len(dates) - 6):
            week_count = sum(month_data[dates[j]]['completed'] for j in range(i, i + 7))
            if week_count > best_week_count:
                best_week_count = week_count
                best_week_start = i
        
        # Maior streak do mês
        max_streak = 0
        current_streak = 0
        
        for date in dates:
            if month_data[date]['completed'] >= (month_data[date]['total'] * 0.5):
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        
        # Agrupar por semana para visualização
        weekly_summary = []
        for i in range(0, 30, 7):
            week_dates = dates[i:min(i+7, 30)]
            week_completed = sum(month_data[d]['completed'] for d in week_dates)
            weekly_summary.append({
                'week': f"Semana {i//7 + 1}",
                'completed': week_completed,
                'dates': week_dates
            })
        
        return {
            "period": "Mensal",
            "start_date": dates[0],
            "end_date": dates[-1],
            "total_active_habits": total_active_habits,
            "total_completed": total_completed,
            "average_per_day": round(average_per_day, 1),
            "max_streak": max_streak,
            "best_week_start": dates[best_week_start] if best_week_start < len(dates) else dates[0],
            "best_week_count": best_week_count,
            "weekly_summary": weekly_summary,
            "completion_rate": round((total_completed / (total_active_habits * 30) * 100) if total_active_habits > 0 else 0, 1),
            "daily_data": {date: month_data[date] for date in dates}
        }


class ReportFactory:
    """Factory: Cria diferentes tipos de relatórios."""
    
    @staticmethod
    def create_report(report_type: str, raw_data):
        """
        Cria um relatório com base no tipo especificado.
        
        Args:
            report_type: Tipo do relatório ('daily', 'weekly', 'monthly')
            raw_data: Dados brutos (lista de hábitos) para gerar o relatório
            
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