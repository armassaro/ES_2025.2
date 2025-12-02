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
    Testes automatizados para geração de relatórios (CTA-009 a CTA-018)
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
    
    @pytest.mark.reports
    def test_cta_013_custom_report_with_valid_period_and_data(self, clean_json_files):
        """
        CTA-013: Relatório personalizado com período válido e dados
        
        Dado que: Sistema possui 3 hábitos com histórico distribuído
                 período solicitado: "2025-11-01" até "2025-11-15" (15 dias)
        Quando: Chama ReportFactory.create_report("custom", raw_data, start_date, end_date)
        Então: Retorna total_completed correto, max_streak, best_day, completion_rate e daily_data
        """
        # Definir período de teste
        start_date = "2025-11-01"
        end_date = "2025-11-15"
        
        # Criar 3 hábitos
        habits_data = [
            {"name": "Correr", "description": "5km", "frequency": "daily"},
            {"name": "Estudar", "description": "1h programação", "frequency": "daily"},
            {"name": "Yoga", "description": "30min", "frequency": "daily"}
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
        created_habits = all_habits[-3:]
        
        # Configurar histórico para o período
        # Correr: concluído em 10 dias (dias 0-9)
        correr_days = [
            "2025-11-01", "2025-11-02", "2025-11-03", "2025-11-04", "2025-11-05",
            "2025-11-06", "2025-11-07", "2025-11-08", "2025-11-09", "2025-11-10"
        ]
        
        # Estudar: concluído em 8 dias (dias 1, 3, 5, 7, 9, 11, 13, 15)
        estudar_days = [
            "2025-11-02", "2025-11-04", "2025-11-06", "2025-11-08", 
            "2025-11-10", "2025-11-12", "2025-11-14"
        ]
        
        # Yoga: concluído em 5 dias (dias 0, 4, 8, 12, 14)
        yoga_days = [
            "2025-11-01", "2025-11-05", "2025-11-09", "2025-11-13", "2025-11-15"
        ]
        
        created_habits[0]['history'] = {date: True for date in correr_days}
        created_habits[1]['history'] = {date: True for date in estudar_days}
        created_habits[2]['history'] = {date: True for date in yoga_days}
        
        # Salvar
        save_data(HABIT_DATA_FILE, self.habit_model.data)
        
        total_expected = len(correr_days) + len(estudar_days) + len(yoga_days)
        
        print(f"\n📅 Período: {start_date} a {end_date} (15 dias)")
        print(f"Correr: {len(correr_days)} conclusões")
        print(f"Estudar: {len(estudar_days)} conclusões")
        print(f"Yoga: {len(yoga_days)} conclusões")
        print(f"Total esperado: {total_expected} conclusões")
        
        # Gerar relatório personalizado
        custom_report = ReportFactory.create_report("custom", created_habits, start_date, end_date)
        report_data = custom_report.generate_visualization_data()
        
        print(f"\n📊 Dados do relatório personalizado: {report_data}")
        
        # Verificações
        assert report_data is not None, "Relatório não deveria ser None"
        assert report_data['start_date'] == start_date, f"Data inicial deveria ser {start_date}"
        assert report_data['end_date'] == end_date, f"Data final deveria ser {end_date}"
        assert report_data['total_days'] == 15, f"Total de dias deveria ser 15"
        assert report_data['total_completed'] == total_expected, \
            f"Total deveria ser {total_expected}, mas é {report_data['total_completed']}"
        
        # Verificar campos obrigatórios
        assert 'average_per_day' in report_data, "Deveria ter 'average_per_day'"
        assert 'max_streak' in report_data, "Deveria ter 'max_streak'"
        assert 'completion_rate' in report_data, "Deveria ter 'completion_rate'"
        assert 'best_day' in report_data, "Deveria ter 'best_day'"
        assert 'best_day_count' in report_data, "Deveria ter 'best_day_count'"
        assert 'daily_data' in report_data, "Deveria ter 'daily_data'"
        
        # Verificar streak máximo (Correr teve 10 dias consecutivos)
        assert report_data['max_streak'] >= 10, \
            f"Max streak deveria ser >= 10, mas é {report_data['max_streak']}"
        
        # Verificar dados diários
        assert len(report_data['daily_data']) == 15, \
            f"Deveria ter 15 dias de dados, mas tem {len(report_data['daily_data'])}"
        
        # Verificar soma dos dados diários
        total_from_daily = sum(day['completed'] for day in report_data['daily_data'].values())
        assert total_from_daily == total_expected, \
            f"Soma dos dados diários deveria ser {total_expected}, mas é {total_from_daily}"
        
        print(f"✅ CTA-013 passou: Relatório personalizado gerado corretamente com {total_expected} conclusões")
    
    @pytest.mark.reports
    def test_cta_014_custom_report_with_invalid_dates(self, clean_json_files):
        """
        CTA-014: Relatório personalizado com datas inválidas
        
        Dado que: Sistema recebe solicitação de relatório com data final anterior à data inicial
        Quando: Chama ReportFactory.create_report("custom", raw_data, "2025-11-15", "2025-11-01")
        Então: Levanta ValueError com mensagem apropriada
        """
        # Criar 1 hábito (necessário para ter dados)
        success, msg = self.habit_model.create_habit("Hábito Teste", "Teste", "daily")
        if not success:
            pytest.fail(f"Falha ao criar hábito: {msg}")
        
        all_habits = self.habit_model.get_all_habits()
        
        print("\n❌ Testando datas invertidas (fim antes do início)...")
        
        # Tentar criar relatório com datas invertidas
        with pytest.raises(ValueError) as exc_info:
            custom_report = ReportFactory.create_report(
                "custom", 
                all_habits, 
                "2025-11-15",  # Data inicial DEPOIS da final
                "2025-11-01"   # Data final ANTES da inicial
            )
        
        # Verificar mensagem de erro
        assert "data final não pode ser menor que a data inicial" in str(exc_info.value).lower(), \
            "Mensagem de erro deveria mencionar datas inválidas"
        
        print(f"✅ CTA-014 passou: ValueError levantada corretamente: {exc_info.value}")
    
    @pytest.mark.reports
    def test_cta_015_custom_report_with_no_data_in_period(self, clean_json_files):
        """
        CTA-015: Relatório personalizado sem dados no período
        
        Dado que: Sistema possui hábitos mas sem registros no período solicitado
                 período: "2024-01-01" até "2024-01-31" (período passado sem dados)
        Quando: Chama ReportFactory.create_report("custom", raw_data, start_date, end_date)
        Então: Retorna estrutura válida com total_completed=0 e completion_rate=0
        """
        # Criar 2 hábitos
        habits_data = [
            {"name": "Hábito A", "description": "Teste A", "frequency": "daily"},
            {"name": "Hábito B", "description": "Teste B", "frequency": "daily"}
        ]
        
        for habit_data in habits_data:
            success, msg = self.habit_model.create_habit(
                name=habit_data["name"],
                description=habit_data["description"],
                frequency=habit_data["frequency"]
            )
            
            if not success:
                pytest.fail(f"Falha ao criar hábito: {msg}")
        
        all_habits = self.habit_model.get_all_habits()
        created_habits = all_habits[-2:]
        
        # Configurar histórico FORA do período de teste
        created_habits[0]['history'] = {"2025-12-01": True, "2025-12-02": True}
        created_habits[1]['history'] = {"2025-12-01": True}
        
        save_data(HABIT_DATA_FILE, self.habit_model.data)
        
        # Período SEM dados
        start_date = "2024-01-01"
        end_date = "2024-01-31"
        
        print(f"\n📅 Testando período sem dados: {start_date} a {end_date}")
        print(f"   (Dados existem apenas em dezembro/2025)")
        
        # Gerar relatório
        custom_report = ReportFactory.create_report("custom", created_habits, start_date, end_date)
        report_data = custom_report.generate_visualization_data()
        
        print(f"\n📊 Relatório: {report_data}")
        
        # Verificações
        assert report_data is not None, "Relatório não deveria ser None"
        assert report_data['total_completed'] == 0, \
            f"Total deveria ser 0, mas é {report_data['total_completed']}"
        assert report_data['completion_rate'] == 0.0, \
            f"Taxa de conclusão deveria ser 0%, mas é {report_data['completion_rate']}"
        assert report_data['max_streak'] == 0, \
            f"Max streak deveria ser 0, mas é {report_data['max_streak']}"
        assert report_data['total_days'] == 31, \
            f"Total de dias deveria ser 31, mas é {report_data['total_days']}"
        
        print(f"✅ CTA-015 passou: Relatório vazio gerado corretamente para período sem dados")
    
    @pytest.mark.reports
    def test_cta_016_custom_report_with_different_periods(self, clean_json_files):
        """
        CTA-016: Relatório personalizado com diferentes tamanhos de período
        
        Dado que: Sistema possui hábitos com histórico variado
        Quando: Gera relatórios para períodos de 1, 7, 30 e 90 dias
        Então: Todos retornam estrutura válida com total_days correto
        """
        # Criar 2 hábitos
        habits_data = [
            {"name": "Hábito Diário", "description": "Todo dia", "frequency": "daily"},
            {"name": "Hábito Ocasional", "description": "Às vezes", "frequency": "daily"}
        ]
        
        for habit_data in habits_data:
            success, msg = self.habit_model.create_habit(
                name=habit_data["name"],
                description=habit_data["description"],
                frequency=habit_data["frequency"]
            )
            
            if not success:
                pytest.fail(f"Falha ao criar hábito: {msg}")
        
        all_habits = self.habit_model.get_all_habits()
        created_habits = all_habits[-2:]
        
        # Criar histórico extenso (últimos 90 dias)
        base_date = datetime(2025, 11, 15)
        
        for i in range(90):
            date = (base_date - timedelta(days=i)).strftime("%Y-%m-%d")
            
            # Hábito diário: completado todos os dias
            if 'history' not in created_habits[0]:
                created_habits[0]['history'] = {}
            created_habits[0]['history'][date] = True
            
            # Hábito ocasional: completado a cada 3 dias
            if i % 3 == 0:
                if 'history' not in created_habits[1]:
                    created_habits[1]['history'] = {}
                created_habits[1]['history'][date] = True
        
        save_data(HABIT_DATA_FILE, self.habit_model.data)
        
        # Testar diferentes períodos
        test_periods = [
            ("2025-11-15", "2025-11-15", 1, "1 dia"),
            ("2025-11-09", "2025-11-15", 7, "7 dias"),
            ("2025-10-16", "2025-11-15", 31, "30 dias"),
            ("2025-08-17", "2025-11-15", 91, "90 dias")
        ]
        
        print("\n📅 Testando diferentes tamanhos de período:")
        
        for start, end, expected_days, description in test_periods:
            print(f"\n   Período: {description} ({start} a {end})")
            
            custom_report = ReportFactory.create_report("custom", created_habits, start, end)
            report_data = custom_report.generate_visualization_data()
            
            # Verificações
            assert report_data is not None, f"Relatório não deveria ser None para {description}"
            assert report_data['total_days'] == expected_days, \
                f"Total de dias deveria ser {expected_days}, mas é {report_data['total_days']}"
            assert report_data['start_date'] == start, f"Data inicial incorreta para {description}"
            assert report_data['end_date'] == end, f"Data final incorreta para {description}"
            
            # Verificar que possui dados diários
            assert 'daily_data' in report_data, f"Deveria ter daily_data para {description}"
            assert len(report_data['daily_data']) == expected_days, \
                f"daily_data deveria ter {expected_days} entradas, mas tem {len(report_data['daily_data'])}"
            
            # Verificar campos de estatísticas
            assert 'total_completed' in report_data, f"Deveria ter total_completed para {description}"
            assert 'average_per_day' in report_data, f"Deveria ter average_per_day para {description}"
            assert 'max_streak' in report_data, f"Deveria ter max_streak para {description}"
            assert 'completion_rate' in report_data, f"Deveria ter completion_rate para {description}"
            
            print(f"      ✓ {expected_days} dias verificados")
            print(f"      ✓ Total completado: {report_data['total_completed']}")
            print(f"      ✓ Taxa de conclusão: {report_data['completion_rate']}%")
        
        print(f"\n✅ CTA-016 passou: Relatórios personalizados funcionam para diferentes períodos")
    
    @pytest.mark.reports
    def test_cta_017_custom_report_via_controller(self, clean_json_files):
        """
        CTA-017: Geração de relatório personalizado via ReportController
        
        Dado que: Sistema possui hábitos e ReportController configurado
        Quando: Chama report_controller.generate_custom_report(start_date, end_date)
        Então: Retorna tupla (sucesso=True, mensagem, dados) com relatório válido
        """
        from view.ConsoleView import ConsoleView
        
        # Criar hábitos
        habits_data = [
            {"name": "Programar", "description": "2h por dia", "frequency": "daily"},
            {"name": "Inglês", "description": "30min", "frequency": "daily"}
        ]
        
        for habit_data in habits_data:
            success, msg = self.habit_model.create_habit(
                name=habit_data["name"],
                description=habit_data["description"],
                frequency=habit_data["frequency"]
            )
            
            if not success:
                pytest.fail(f"Falha ao criar hábito: {msg}")
        
        all_habits = self.habit_model.get_all_habits()
        created_habits = all_habits[-2:]
        
        # Configurar histórico
        test_dates = ["2025-11-01", "2025-11-03", "2025-11-05", "2025-11-07", "2025-11-09"]
        
        created_habits[0]['history'] = {date: True for date in test_dates}
        created_habits[1]['history'] = {test_dates[0]: True, test_dates[2]: True}
        
        save_data(HABIT_DATA_FILE, self.habit_model.data)
        
        # Criar view e controller
        console_view = ConsoleView(None, self.user_model)
        report_controller = ReportController(self.habit_model, console_view)
        
        # Período de teste
        start_date = "2025-11-01"
        end_date = "2025-11-10"
        
        print(f"\n📊 Gerando relatório via controller: {start_date} a {end_date}")
        
        # Gerar relatório via controller
        success, message, report_data = report_controller.generate_custom_report(start_date, end_date)
        
        print(f"   Sucesso: {success}")
        print(f"   Mensagem: {message}")
        print(f"   Dados: {report_data is not None}")
        
        # Verificações
        assert success is True, f"Deveria ter sucesso, mas retornou {success}"
        assert message is not None, "Mensagem não deveria ser None"
        assert "sucesso" in message.lower() or "gerado" in message.lower(), \
            f"Mensagem deveria indicar sucesso: {message}"
        assert report_data is not None, "Dados do relatório não deveriam ser None"
        
        # Verificar estrutura do relatório
        assert isinstance(report_data, dict), "Dados deveriam ser um dicionário"
        assert report_data['start_date'] == start_date, "Data inicial incorreta"
        assert report_data['end_date'] == end_date, "Data final incorreta"
        assert report_data['total_days'] == 10, f"Total de dias deveria ser 10"
        
        expected_total = len(test_dates) + 2  # 5 + 2 = 7
        assert report_data['total_completed'] == expected_total, \
            f"Total completado deveria ser {expected_total}, mas é {report_data['total_completed']}"
        
        print(f"\n✅ CTA-017 passou: Relatório gerado com sucesso via controller")
    
    @pytest.mark.reports
    def test_cta_018_custom_report_without_required_dates(self, clean_json_files):
        """
        CTA-018: Tentativa de criar relatório personalizado sem datas obrigatórias
        
        Dado que: Sistema recebe solicitação sem start_date ou end_date
        Quando: Chama ReportFactory.create_report("custom", raw_data, None, None)
        Então: Levanta ValueError indicando que as datas são obrigatórias
        """
        # Criar 1 hábito
        success, msg = self.habit_model.create_habit("Hábito", "Teste", "daily")
        if not success:
            pytest.fail(f"Falha ao criar hábito: {msg}")
        
        all_habits = self.habit_model.get_all_habits()
        
        print("\n❌ Testando criação sem datas obrigatórias...")
        
        # Testar sem start_date e end_date
        with pytest.raises(ValueError) as exc_info:
            custom_report = ReportFactory.create_report("custom", all_habits, None, None)
        
        assert "obrigatórios" in str(exc_info.value).lower() or "required" in str(exc_info.value).lower(), \
            "Mensagem de erro deveria mencionar que as datas são obrigatórias"
        
        print(f"   ✓ ValueError levantada: {exc_info.value}")
        
        # Testar sem start_date
        with pytest.raises(ValueError) as exc_info:
            custom_report = ReportFactory.create_report("custom", all_habits, None, "2025-11-15")
        
        print(f"   ✓ ValueError sem start_date: {exc_info.value}")
        
        # Testar sem end_date
        with pytest.raises(ValueError) as exc_info:
            custom_report = ReportFactory.create_report("custom", all_habits, "2025-11-01", None)
        
        print(f"   ✓ ValueError sem end_date: {exc_info.value}")
        
        print(f"\n✅ CTA-018 passou: Validação de datas obrigatórias funcionando corretamente")

if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])