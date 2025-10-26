from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from collections import defaultdict

# --- PADRÃO FACTORY METHOD (Para criação de relatórios) ---

class Report(ABC):
    """Produto (Product): Interface comum para todos os relatórios."""
    @abstractmethod
    def generate_visualization_data(self):
        """Gera dados prontos para visualização."""
        pass


class DailyReport(Report):
    """Produto Concreto: Relatório Diário."""
    def __init__(self, raw_data):
        self.habits = raw_data
        self.today = datetime.now().strftime('%Y-%m-%d')

    def generate_visualization_data(self):
        """Gera dados do relatório diário."""
        total_habits = len([h for h in self.habits if h.get('active', True)])
        completed_today = 0
        habits_detail = []
        
        for habit in self.habits:
            if not habit.get('active', True):
                continue
            
            is_done = habit.get('history', {}).get(self.today, False)
            frequency = habit.get('frequency', 'daily')
            
            # Considerar frequência
            if frequency == 'daily':
                status = "✅ Concluído" if is_done else "⏳ Pendente"
                if is_done:
                    completed_today += 1
            elif frequency == 'weekly':
                # Verificar se foi feito nos últimos 7 dias
                done_this_week = self._check_done_in_last_days(habit, 7)
                status = "✅ Concluído esta semana" if done_this_week else "⏳ Pendente (semanal)"
                if done_this_week:
                    completed_today += 1
            elif frequency == 'monthly':
                # Verificar se foi feito nos últimos 30 dias
                done_this_month = self._check_done_in_last_days(habit, 30)
                status = "✅ Concluído este mês" if done_this_month else "⏳ Pendente (mensal)"
                if done_this_month:
                    completed_today += 1
            else:
                status = "⏳ Pendente"
            
            habits_detail.append({
                'name': habit['name'],
                'status': status,
                'frequency': frequency
            })
        
        pending = total_habits - completed_today
        completion_rate = round((completed_today / total_habits * 100), 1) if total_habits > 0 else 0
        
        return {
            'date': self.today,
            'total_habits': total_habits,
            'completed': completed_today,
            'pending': pending,
            'completion_rate': completion_rate,
            'habits_detail': habits_detail
        }
    
    def _check_done_in_last_days(self, habit, days):
        """Verifica se o hábito foi concluído nos últimos N dias."""
        history = habit.get('history', {})
        today = datetime.now()
        
        for i in range(days):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            if history.get(date, False):
                return True
        return False


class WeeklyReport(Report):
    """Produto Concreto: Relatório Semanal."""
    def __init__(self, raw_data):
        self.habits = raw_data
        self.today = datetime.now()
        self.start_of_week = self.today - timedelta(days=self.today.weekday())
        self.end_of_week = self.start_of_week + timedelta(days=6)

    def generate_visualization_data(self):
        """Gera dados do relatório semanal."""
        total_completed = 0
        daily_data = defaultdict(lambda: {'completed': 0, 'total': 0})
        streak = 0
        max_count = 0
        best_day = ""
        
        # Contar hábitos ativos
        active_habits = [h for h in self.habits if h.get('active', True)]
        
        # Processar cada dia da semana
        for i in range(7):
            current_date = (self.start_of_week + timedelta(days=i)).strftime('%Y-%m-%d')
            day_completed = 0
            day_total = 0
            
            for habit in active_habits:
                frequency = habit.get('frequency', 'daily')
                history = habit.get('history', {})
                
                # Contar apenas hábitos relevantes para cada dia
                if frequency == 'daily':
                    day_total += 1
                    if history.get(current_date, False):
                        day_completed += 1
                        total_completed += 1
                elif frequency == 'weekly' and i == 0:  # Contar apenas no primeiro dia
                    day_total += 1
                    if self._check_done_in_week(habit):
                        day_completed += 1
                        total_completed += 1
            
            daily_data[current_date] = {
                'completed': day_completed,
                'total': day_total
            }
            
            if day_completed > max_count:
                max_count = day_completed
                best_day = current_date
        
        # Calcular sequência
        for i in range(7):
            date = (self.today - timedelta(days=i)).strftime('%Y-%m-%d')
            if self._check_any_completed(date):
                streak += 1
            else:
                break
        
        total_days = 7
        avg_per_day = round(total_completed / total_days, 1) if total_days > 0 else 0
        completion_rate = round((total_completed / (len(active_habits) * 7) * 100), 1) if active_habits else 0
        
        return {
            'start_date': self.start_of_week.strftime('%Y-%m-%d'),
            'end_date': self.end_of_week.strftime('%Y-%m-%d'),
            'total_completed': total_completed,
            'average_per_day': avg_per_day,
            'current_streak': streak,
            'completion_rate': completion_rate,
            'best_day': best_day,
            'best_day_count': max_count,
            'daily_data': dict(daily_data)
        }
    
    def _check_done_in_week(self, habit):
        """Verifica se hábito semanal foi feito na semana."""
        history = habit.get('history', {})
        for i in range(7):
            date = (self.start_of_week + timedelta(days=i)).strftime('%Y-%m-%d')
            if history.get(date, False):
                return True
        return False
    
    def _check_any_completed(self, date):
        """Verifica se algum hábito foi concluído nesta data."""
        for habit in self.habits:
            if habit.get('history', {}).get(date, False):
                return True
        return False


class MonthlyReport(Report):
    """Produto Concreto: Relatório Mensal."""
    def __init__(self, raw_data):
        self.habits = raw_data
        self.today = datetime.now()
        self.start_of_month = self.today.replace(day=1)
        # Último dia do mês
        if self.today.month == 12:
            self.end_of_month = self.today.replace(day=31)
        else:
            next_month = self.today.replace(month=self.today.month + 1, day=1)
            self.end_of_month = next_month - timedelta(days=1)

    def generate_visualization_data(self):
        """Gera dados do relatório mensal."""
        total_completed = 0
        max_streak = 0
        current_streak = 0
        weekly_summary = []
        
        active_habits = [h for h in self.habits if h.get('active', True)]
        
        # Processar cada dia do mês
        days_in_month = (self.end_of_month - self.start_of_month).days + 1
        
        for i in range(days_in_month):
            current_date = (self.start_of_month + timedelta(days=i)).strftime('%Y-%m-%d')
            day_completed = False
            
            for habit in active_habits:
                if habit.get('history', {}).get(current_date, False):
                    total_completed += 1
                    day_completed = True
            
            # Calcular streak
            if day_completed:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        
        # Resumo semanal
        week_num = 1
        week_start = self.start_of_month
        
        while week_start <= self.end_of_month:
            week_end = min(week_start + timedelta(days=6), self.end_of_month)
            week_completed = 0
            week_dates = []
            
            current = week_start
            while current <= week_end:
                date_str = current.strftime('%Y-%m-%d')
                week_dates.append(date_str)
                
                for habit in active_habits:
                    if habit.get('history', {}).get(date_str, False):
                        week_completed += 1
                
                current += timedelta(days=1)
            
            weekly_summary.append({
                'week': f'Semana {week_num}',
                'completed': week_completed,
                'dates': week_dates
            })
            
            week_start = week_end + timedelta(days=1)
            week_num += 1
        
        # Melhor semana
        best_week = max(weekly_summary, key=lambda w: w['completed']) if weekly_summary else None
        
        avg_per_day = round(total_completed / days_in_month, 1) if days_in_month > 0 else 0
        completion_rate = round((total_completed / (len(active_habits) * days_in_month) * 100), 1) if active_habits and days_in_month > 0 else 0
        
        return {
            'start_date': self.start_of_month.strftime('%Y-%m-%d'),
            'end_date': self.end_of_month.strftime('%Y-%m-%d'),
            'total_completed': total_completed,
            'average_per_day': avg_per_day,
            'max_streak': max_streak,
            'completion_rate': completion_rate,
            'best_week_start': best_week['dates'][0] if best_week else 'N/A',
            'best_week_count': best_week['completed'] if best_week else 0,
            'weekly_summary': weekly_summary
        }


class ReportFactory:
    """Criador (Creator): Factory que cria diferentes tipos de relatórios."""
    
    @staticmethod
    def create_report(report_type, raw_data):
        """
        Factory Method: Cria o relatório apropriado com base no tipo.
        
        Args:
            report_type: Tipo do relatório ('daily', 'weekly', 'monthly')
            raw_data: Dados brutos dos hábitos
        
        Returns:
            Um objeto Report (DailyReport, WeeklyReport ou MonthlyReport)
        """
        if report_type == "daily":
            return DailyReport(raw_data)
        elif report_type == "weekly":
            return WeeklyReport(raw_data)
        elif report_type == "monthly":
            return MonthlyReport(raw_data)
        else:
            raise ValueError(f"Tipo de relatório inválido: {report_type}")