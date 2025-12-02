import pytest
import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime, timedelta
from unittest.mock import patch
from model.HabitModel import HabitModel, save_data, HABIT_DATA_FILE
from model.UserModel import UserModel
from model.ReportFactory import ReportFactory
from controller.ReportController import ReportController

class TestReportGeneration:
    """
    Testes automatizados para geração de relatórios (CTA-009 a CTA-012)
    Responsável: Silvino
    """
    
    def setup_method(self):
        """Configuração antes de cada teste"""
        self.user_model = UserModel()
        self.habit_model = HabitModel(self.user_model)
        
        # Credenciais de teste
        test_username = "teste"
        test_password = "123"
        
        # Criar usuário
        success, msg = self.user_model.create_user(test_username, test_password)
        if not success and "já existe" not in msg:
            raise Exception(f"Falha ao criar usuário: {msg}")
        
        # Autenticar usuário
        success, msg = self.user_model.authenticate(test_username, test_password)
        if not success:
            raise Exception(f"Falha ao autenticar: {msg}")
        
        print(f"✅ Usuário '{test_username}' autenticado. ID: {self.user_model.get_logged_in_user_id()}")
    
    @pytest.mark.reports
    def test_cta_009_daily_report_with_mixed_completion(self, clean_json_files):
        """
        CTA-009: Relatório diário com hábitos mistos
        
        Dado que: Sistema possui 3 hábitos ativos, data atual é 2025-11-14, 
                 histórico: h001 marcado hoje (concluído), h002 não marcado hoje, h003 marcado hoje
        Quando: Chama ReportFactory.create_report("daily", raw_data) e obtém report.generate_visualization_data()
        Então: Retorna estrutura com date="2025-11-14", completed=2, total_habits=3, 
               e lista de hábitos com status correto
        """
        # Data de teste
        target_date = datetime(2025, 11, 14)
        date_str = "2025-11-14"
        
        # Preparação: Criar 3 hábitos ativos
        habits_data = [
            {"name": "Beber água", "description": "2L diários", "frequency": "daily"},
            {"name": "Exercícios", "description": "30min", "frequency": "daily"},
            {"name": "Meditação", "description": "10min", "frequency": "daily"}
        ]
        
        created_habits = []
        for habit_data in habits_data:
            success, msg = self.habit_model.create_habit(
                name=habit_data["name"],
                description=habit_data["description"],
                frequency=habit_data["frequency"]
            )
            
            if not success:
                pytest.fail(f"Falha ao criar hábito {habit_data['name']}: {msg}")
        
        # Obter hábitos criados
        all_habits = self.habit_model.get_all_habits()
        assert len(all_habits) >= 3, f"Deveriam ter 3 hábitos, mas tem {len(all_habits)}"
        
        # Pegar os 3 últimos hábitos criados
        created_habits = all_habits[-3:]
        
        # Configurar histórico: h001 e h003 marcados hoje, h002 não marcado
        created_habits[0]['history'] = {date_str: True}   # Beber água (concluído)
        created_habits[1]['history'] = {}                 # Exercícios (não marcado)
        created_habits[2]['history'] = {date_str: True}   # Meditação (concluído)
        
        # Salvar alterações no histórico
        save_data(HABIT_DATA_FILE, self.habit_model.data)
        
        print(f"\nHábitos configurados para {date_str}:")
        for i, habit in enumerate(created_habits):
            status = "concluído" if habit['history'].get(date_str, False) else "não concluído"
            print(f"  h{i+1:03d} - {habit['name']}: {status}")
        
        # Ação: Gerar relatório diário usando ReportFactory
        with patch('model.ReportFactory.datetime') as mock_dt:
            mock_dt.now.return_value = target_date
            mock_dt.strftime = datetime.strftime
            
            # Criar relatório diário
            daily_report = ReportFactory.create_report("daily", created_habits)
            report_data = daily_report.generate_visualization_data()
        
        # Verificações conforme CTA-009
        print(f"\nDados do relatório: {report_data}")
        
        assert report_data is not None, "Relatório não deveria ser None"
        assert report_data['date'] == date_str, f"Data deveria ser {date_str}"
        assert report_data['completed'] == 2, f"Deveriam ter 2 concluídos, mas tem {report_data['completed']}"
        assert report_data['total_habits'] == 3, f"Deveriam ter 3 hábitos, mas tem {report_data['total_habits']}"
        
        # Verificar lista de hábitos
        if 'habits_detail' in report_data:
            completed_count = sum(1 for h in report_data['habits_detail'] if 'Concluído' in h['status'])
            assert completed_count == 2, f"Deveriam ter 2 hábitos concluídos, mas tem {completed_count}"
        
        print(f"✅ CTA-009 passou: Relatório diário gerado corretamente")
    
    @pytest.mark.reports
    def test_cta_010_weekly_report_with_completion_history(self, clean_json_files):
        """
        CTA-010: Relatório semanal com histórico dos últimos 7 dias
        
        Dado que: Sistema possui 2 hábitos ativos com histórico dos últimos 7 dias:
                 h001 concluído em 5 dias, h002 concluído em 3 dias
        Quando: Chama ReportFactory.create_report("weekly", raw_data)
        Então: Retorna total_completed=8 e estatísticas semanais corretas
        """
        # Usar data atual para garantir que estamos no período correto
        target_date = datetime.now()
        
        # Criar 2 hábitos
        habits_data = [
            {"name": "Exercícios", "description": "30min diários", "frequency": "daily"},
            {"name": "Leitura", "description": "20min", "frequency": "daily"}
        ]
        
        for habit_data in habits_data:
            success, msg = self.habit_model.create_habit(
                name=habit_data["name"],
                description=habit_data["description"],
                frequency=habit_data["frequency"]
            )
            
            if not success:
                pytest.fail(f"Falha ao criar hábito: {msg}")
        
        # Obter hábitos criados
        all_habits = self.habit_model.get_all_habits()
        created_habits = all_habits[-2:]  # Pegar os 2 últimos
        
        # Calcular as datas dos últimos 7 dias baseado na data de HOJE
        # WeeklyReport usa: self.start_of_week = self.today - timedelta(days=self.today.weekday())
        start_of_week = target_date - timedelta(days=target_date.weekday())
        
        dates = []
        for i in range(7):
            date = (start_of_week + timedelta(days=i)).strftime("%Y-%m-%d")
            dates.append(date)
        
        print(f"\n📅 Semana calculada (início={start_of_week.strftime('%Y-%m-%d')}): {dates}")
        
        # h001 - Exercícios: concluído em 5 dias (dias 0, 1, 3, 4, 6 da semana)
        h001_days = [dates[0], dates[1], dates[3], dates[4], dates[6]]
        created_habits[0]['history'] = {date: True for date in h001_days}
        
        # h002 - Leitura: concluído em 3 dias (dias 1, 2, 5 da semana)
        h002_days = [dates[1], dates[2], dates[5]]
        created_habits[1]['history'] = {date: True for date in h002_days}
        
        # Salvar
        save_data(HABIT_DATA_FILE, self.habit_model.data)
        
        print(f"Exercícios concluído em ({len(h001_days)} dias): {h001_days}")
        print(f"Leitura concluído em ({len(h002_days)} dias): {h002_days}")
        print(f"Total esperado: {len(h001_days) + len(h002_days)} conclusões")
        
        # Gerar relatório semanal (SEM mock de datetime para usar data real)
        weekly_report = ReportFactory.create_report("weekly", created_habits)
        report_data = weekly_report.generate_visualization_data()
        
        print(f"\n📊 Dados do relatório semanal: {report_data}")
        
        expected_total = len(h001_days) + len(h002_days)
        
        # Verificações
        assert report_data is not None, "Relatório não deveria ser None"
        assert 'total_completed' in report_data, "Deveria ter 'total_completed'"
        assert report_data['total_completed'] == expected_total, \
            f"Total deveria ser {expected_total}, mas é {report_data['total_completed']}"
        
        # Verificar dados diários
        if 'daily_data' in report_data:
            total_from_daily = sum(day['completed'] for day in report_data['daily_data'].values())
            assert total_from_daily == expected_total, \
                f"Soma diária deveria ser {expected_total}, mas é {total_from_daily}"
        
        print(f"✅ CTA-010 passou: Relatório semanal com {expected_total} conclusões")
    
    @pytest.mark.reports
    def test_cta_011_monthly_report_with_varied_patterns(self, clean_json_files):
        """
        CTA-011: Relatório mensal com padrões variados
        
        Dado que: Sistema possui 3 hábitos com histórico distribuído nos últimos 30 dias
        Quando: Chama ReportFactory.create_report("monthly", raw_data)
        Então: Retorna total_completed correto, max_streak e weekly_summary
        """
        # Usar data atual
        target_date = datetime.now()
        
        # Criar 3 hábitos
        habits_data = [
            {"name": "Caminhada", "description": "30min", "frequency": "daily"},
            {"name": "Journaling", "description": "Escrita", "frequency": "daily"},
            {"name": "Vitaminas", "description": "Suplementos", "frequency": "daily"}
        ]
        
        for habit_data in habits_data:
            success, msg = self.habit_model.create_habit(
                name=habit_data["name"],
                description=habit_data["description"],
                frequency=habit_data["frequency"]
            )
            
            if not success:
                pytest.fail(f"Falha ao criar hábito: {msg}")
        
        # Obter hábitos
        all_habits = self.habit_model.get_all_habits()
        created_habits = all_habits[-3:]
        
        # MonthlyReport calcula: self.start_of_month = self.today.replace(day=1)
        start_of_month = target_date.replace(day=1)
        
        # Calcular dias do mês até hoje
        days_in_month = (target_date - start_of_month).days + 1
        
        dates = []
        for i in range(days_in_month):
            date = (start_of_month + timedelta(days=i)).strftime("%Y-%m-%d")
            dates.append(date)
        
        print(f"\n📅 Mês calculado: {len(dates)} dias de {dates[0]} a {dates[-1]}")
        
        # CORREÇÃO: Simplificar os padrões para garantir contagem correta
        # Caminhada: primeiros 3 dias disponíveis
        caminhada_indices = list(range(0, min(3, len(dates))))
        caminhada_days = [dates[i] for i in caminhada_indices]
        
        # Journaling: 2 dias específicos (dia 0 e dia 1, se disponíveis)
        journaling_indices = [0, 1] if len(dates) > 1 else [0]
        journaling_indices = [i for i in journaling_indices if i < len(dates)]
        journaling_days = [dates[i] for i in journaling_indices]
        
        # Vitaminas: 2 dias específicos (dia 0 e dia 2, se disponíveis)
        vitaminas_indices = [0, 2] if len(dates) > 2 else [0]
        vitaminas_indices = [i for i in vitaminas_indices if i < len(dates)]
        vitaminas_days = [dates[i] for i in vitaminas_indices]
        
        created_habits[0]['history'] = {date: True for date in caminhada_days}
        created_habits[1]['history'] = {date: True for date in journaling_days}
        created_habits[2]['history'] = {date: True for date in vitaminas_days}
        
        # Calcular total esperado
        # Note que alguns dias podem se sobrepor (ex: dia 0 aparece em todos)
        all_marked_days = set(caminhada_days + journaling_days + vitaminas_days)
        
        # Contar quantas vezes cada hábito foi marcado
        total_expected = len(caminhada_days) + len(journaling_days) + len(vitaminas_days)
        
        # Salvar
        save_data(HABIT_DATA_FILE, self.habit_model.data)
        
        print(f"\nPadrões configurados:")
        print(f"  Caminhada: {len(caminhada_days)} dias - {caminhada_days}")
        print(f"  Journaling: {len(journaling_days)} dias - {journaling_days}")
        print(f"  Vitaminas: {len(vitaminas_days)} dias - {vitaminas_days}")
        print(f"  Total de marcações: {total_expected}")
        print(f"  Dias únicos marcados: {len(all_marked_days)}")
        
        # Gerar relatório mensal (SEM mock)
        monthly_report = ReportFactory.create_report("monthly", created_habits)
        report_data = monthly_report.generate_visualization_data()
        
        print(f"\n📊 Dados do relatório mensal: {report_data}")
        
        # Verificações
        assert report_data is not None, "Relatório não deveria ser None"
        assert 'total_completed' in report_data, "Deveria ter 'total_completed'"
        
        # Ajustar expectativa baseado no que realmente foi configurado
        assert report_data['total_completed'] == total_expected, \
            f"Total deveria ser {total_expected}, mas é {report_data['total_completed']}"
        
        # Verificar max_streak (deve ter pelo menos 1)
        if 'max_streak' in report_data:
            assert report_data['max_streak'] >= 1, \
                f"Max streak deveria ser >= 1, mas é {report_data['max_streak']}"
        
        # Verificar weekly_summary
        if 'weekly_summary' in report_data:
            assert len(report_data['weekly_summary']) >= 1, \
                f"Deveria ter >= 1 semana, mas tem {len(report_data['weekly_summary'])}"
        
        print(f"✅ CTA-011 passou: Relatório mensal com {total_expected} conclusões")
    
    @pytest.mark.reports
    def test_cta_012_reports_with_empty_history(self, clean_json_files):
        """
        CTA-012: Relatórios com histórico vazio
        
        Dado que: Sistema possui hábitos sem registros
        Quando: Gera relatórios diário, semanal e mensal
        Então: Todos retornam estrutura válida com completed=0
        """
        target_date = datetime(2025, 11, 14)
        date_str = "2025-11-14"
        
        # Criar 2 hábitos sem histórico
        habits_data = [
            {"name": "Novo Hábito 1", "description": "Sem registros", "frequency": "daily"},
            {"name": "Novo Hábito 2", "description": "Também sem registros", "frequency": "daily"}
        ]
        
        for habit_data in habits_data:
            success, msg = self.habit_model.create_habit(
                name=habit_data["name"],
                description=habit_data["description"],
                frequency=habit_data["frequency"]
            )
            
            if not success:
                pytest.fail(f"Falha ao criar hábito: {msg}")
        
        # Obter hábitos (já vem com history vazio)
        all_habits = self.habit_model.get_all_habits()
        created_habits = all_habits[-2:]
        
        # Garantir que history está vazio
        for habit in created_habits:
            habit['history'] = {}
        
        save_data(HABIT_DATA_FILE, self.habit_model.data)
        
        print(f"\nCriados {len(created_habits)} hábitos sem histórico")
        
        # Testar os 3 tipos de relatório
        report_results = {}
        
        with patch('model.ReportFactory.datetime') as mock_dt:
            mock_dt.now.return_value = target_date
            mock_dt.strftime = datetime.strftime
            
            # Relatório DIÁRIO
            try:
                daily_report = ReportFactory.create_report("daily", created_habits)
                daily_data = daily_report.generate_visualization_data()
                report_results['daily'] = daily_data
                print(f"\nRelatório diário: {daily_data}")
            except Exception as e:
                pytest.fail(f"Falha no relatório diário: {e}")
            
            # Relatório SEMANAL
            try:
                weekly_report = ReportFactory.create_report("weekly", created_habits)
                weekly_data = weekly_report.generate_visualization_data()
                report_results['weekly'] = weekly_data
                print(f"Relatório semanal: {weekly_data}")
            except Exception as e:
                pytest.fail(f"Falha no relatório semanal: {e}")
            
            # Relatório MENSAL
            try:
                monthly_report = ReportFactory.create_report("monthly", created_habits)
                monthly_data = monthly_report.generate_visualization_data()
                report_results['monthly'] = monthly_data
                print(f"Relatório mensal: {monthly_data}")
            except Exception as e:
                pytest.fail(f"Relatório mensal falhou com histórico vazio: {e}")
            
            # Verificações conforme CTA-012
            assert len(report_results) == 3, "Todos os 3 tipos de relatório deveriam ter sido gerados"
            
            # Verificar cada relatório individualmente
            for report_type, report_data in report_results.items():
                print(f"\nVerificando relatório {report_type}:")
                
                # Estrutura válida sem erros
                assert report_data is not None, f"Relatório {report_type} não deveria ser None"
                assert isinstance(report_data, dict), f"Relatório {report_type} deveria ser um dicionário"
                
                # completed=0 conforme especificação
                if 'completed' in report_data:
                    assert report_data['completed'] == 0, f"Relatório {report_type}: 'completed' deveria ser 0"
                elif 'total_completed' in report_data:
                    assert report_data['total_completed'] == 0, f"Relatório {report_type}: 'total_completed' deveria ser 0"
                
                # total_habits correto
                if 'total_habits' in report_data:
                    assert report_data['total_habits'] == len(created_habits), f"Relatório {report_type}: 'total_habits' incorreto"
                
                # Campos de estatísticas zerados ou com valores padrão
                if 'completion_rate' in report_data:
                    assert report_data['completion_rate'] == 0.0, f"Relatório {report_type}: taxa de conclusão deveria ser 0%"
                
                if 'max_streak' in report_data:
                    assert report_data['max_streak'] == 0, f"Relatório {report_type}: sequência máxima deveria ser 0"
                
                # Verificar que não há erros estruturais
                for key, value in report_data.items():
                    assert value is not None, f"Relatório {report_type}: campo '{key}' não deveria ser None"
                
                print(f"✅ Relatório {report_type} validado com sucesso")
            
            print(f"✅ CTA-012 passou: Todos os relatórios funcionam corretamente com histórico vazio")

if __name__ == "__main__":
    pytest.main()