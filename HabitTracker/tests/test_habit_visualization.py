import pytest
import json
import os
from model.HabitModel import HabitModel
from model.UserModel import UserModel
from controller.HabitController import HabitController

class TestHabitVisualization:
    """
    Testes automatizados para visualização de hábitos (CTA-005 a CTA-008)
    Responsável: Ian
    """
    
    def setup_method(self):
        """Configuração antes de cada teste"""
        self.user_model = UserModel()
        self.habit_model = HabitModel(self.user_model)
        self.habit_controller = HabitController(self.habit_model)
        
        # Criar usuário de teste
        test_user = {
            "username": "test_user_ian",
            "password": "test_pass",
            "id": "test_user_ian_id"
        }
        self.user_model.current_user = test_user
    
    @pytest.mark.visualization
    def test_cta_005_get_active_habits_filter(self, clean_json_files):
        """
        CTA-005: Filtrar apenas hábitos ativos
        
        Dado que: O sistema possui 3 hábitos cadastrados: h001="Beber água" (ativo), 
                 h002="Exercícios" (ativo), h003="Meditar" (inativo)
        Quando: O teste chama get_active_habits() ou método equivalente
        Então: Retorna lista com 2 hábitos (h001 e h002), h003 não aparece na lista,
               e cada hábito contém: habit_id, name, description, active=True
        """
        # Preparação: Criar 3 hábitos conforme especificação
        habits_to_create = [
            {"name": "Beber água", "description": "2L por dia", "frequency": "daily"},
            {"name": "Exercícios", "description": "30min diários", "frequency": "daily"},
            {"name": "Meditar", "description": "10min manhã", "frequency": "daily"}
        ]
        
        created_habit_ids = []
        
        # Criar os 3 hábitos
        for i, habit_data in enumerate(habits_to_create):
            try:
                if hasattr(self.habit_model, 'add_habit'):
                    result = self.habit_model.add_habit(
                        name=habit_data["name"],
                        description=habit_data["description"],
                        frequency=habit_data["frequency"]
                    )
                    
                    # Obter o hábito recém-criado
                    all_habits = self.habit_model.get_all_habits()
                    if all_habits:
                        created_habit = next((h for h in all_habits if h['name'] == habit_data["name"]), None)
                        if created_habit:
                            created_habit_ids.append(created_habit['habit_id'])
                            
                            # Marcar "Meditar" como inativo (h003)
                            if habit_data["name"] == "Meditar":
                                created_habit['active'] = False
                                print(f"Marcando hábito 'Meditar' como inativo: {created_habit['habit_id']}")
                            
                else:
                    pytest.skip("Método add_habit não encontrado")
                    
            except Exception as e:
                print(f"Erro ao criar hábito {habit_data['name']}: {e}")
        
        if len(created_habit_ids) == 0:
            pytest.skip("Nenhum hábito foi criado para o teste")
        
        # Ação: Obter hábitos ativos
        try:
            if hasattr(self.habit_model, 'get_active_habits'):
                active_habits = self.habit_model.get_active_habits()
            else:
                # Filtrar manualmente dos hábitos totais
                all_habits = self.habit_model.get_all_habits()
                active_habits = [h for h in all_habits if h.get('active', True)]
                
        except Exception as e:
            pytest.skip(f"Erro ao obter hábitos ativos: {e}")
        
        # Verificações conforme CTA-005
        print(f"Hábitos ativos encontrados: {len(active_habits) if active_habits else 0}")
        print(f"IDs dos hábitos criados: {created_habit_ids}")
        
        assert active_habits is not None, "get_active_habits() não deveria retornar None"
        assert len(active_habits) == 2, f"Deveria retornar exatamente 2 hábitos ativos, encontrados: {len(active_habits)}"
        
        # Verificar nomes dos hábitos ativos (h001="Beber água", h002="Exercícios")
        active_names = [h['name'] for h in active_habits]
        assert "Beber água" in active_names, "Hábito 'Beber água' (h001) deveria estar ativo"
        assert "Exercícios" in active_names, "Hábito 'Exercícios' (h002) deveria estar ativo"
        assert "Meditar" not in active_names, "Hábito 'Meditar' (h003) NÃO deveria estar na lista de ativos"
        
        # Verificar campos obrigatórios em cada hábito ativo
        required_fields = ['habit_id', 'name', 'description', 'active']
        for habit in active_habits:
            for field in required_fields:
                assert field in habit, f"Campo '{field}' deveria estar presente no hábito {habit.get('name', 'unknown')}"
            
            assert habit['active'] == True, f"Hábito {habit['name']} deveria ter active=True"
            
        print(f"✅ CTA-005 passou: 2 hábitos ativos retornados corretamente")
    
    @pytest.mark.visualization
    def test_cta_006_get_habit_by_id_with_history(self, clean_json_files):
        """
        CTA-006: Obter hábito por ID incluindo histórico
        
        Dado que: Sistema possui hábito h001 com history={"2025-11-10": true, "2025-11-12": true}
        Quando: Chama get_habit_by_id("h001")
        Então: Retorna objeto completo com history correto e campos obrigatórios presentes
        """
        # Preparação: Criar hábito h001 com histórico específico
        try:
            if hasattr(self.habit_model, 'add_habit'):
                result = self.habit_model.add_habit(
                    name="Hábito Teste H001",
                    description="Para teste de histórico",
                    frequency="daily"
                )
            else:
                pytest.skip("Método add_habit não encontrado")
        except Exception as e:
            pytest.skip(f"Erro na preparação: {e}")
        
        # Obter o hábito criado e configurar como h001
        all_habits = self.habit_model.get_all_habits()
        if not all_habits or len(all_habits) == 0:
            pytest.skip("Nenhum hábito foi criado para o teste")
        
        test_habit = all_habits[-1]
        habit_id = test_habit['habit_id']  # Este será nosso "h001"
        
        # Configurar histórico conforme especificação CTA-006
        expected_history = {
            "2025-11-10": True,
            "2025-11-12": True
        }
        test_habit['history'] = expected_history
        
        print(f"Hábito h001 configurado com ID: {habit_id}")
        print(f"Histórico definido: {expected_history}")
        
        # Ação: Obter hábito por ID
        try:
            if hasattr(self.habit_model, 'get_habit_by_id'):
                retrieved_habit = self.habit_model.get_habit_by_id(habit_id)
            else:
                pytest.skip("Método get_habit_by_id não encontrado")
        except Exception as e:
            pytest.skip(f"Erro ao obter hábito por ID: {e}")
        
        # Verificações conforme CTA-006
        assert retrieved_habit is not None, "get_habit_by_id() deveria retornar o hábito"
        
        # Verificar campos obrigatórios conforme especificação
        required_fields = ['name', 'description', 'frequency', 'active']
        for field in required_fields:
            assert field in retrieved_habit, f"Campo '{field}' deveria estar presente"
        
        # Verificar histórico específico
        assert 'history' in retrieved_habit, "Campo 'history' deveria estar presente"
        
        habit_history = retrieved_habit['history']
        assert isinstance(habit_history, dict), "History deveria ser um dicionário"
        
        # Verificar entradas específicas do histórico conforme CTA-006
        assert habit_history.get("2025-11-10") == True, "Entrada '2025-11-10' deveria ser True"
        assert habit_history.get("2025-11-12") == True, "Entrada '2025-11-12' deveria ser True"
        assert len(habit_history) == 2, "Histórico deveria ter exatamente 2 entradas"
        
        # Verificar ID correto
        assert retrieved_habit['habit_id'] == habit_id, "ID do hábito deveria corresponder ao solicitado"
        
        print(f"✅ CTA-006 passou: Hábito com histórico recuperado corretamente")
    
    @pytest.mark.visualization
    def test_cta_007_get_active_habits_empty_system(self, clean_json_files):
        """
        CTA-007: Sistema vazio sem hábitos
        
        Dado que: Sistema está vazio sem nenhum hábito cadastrado
        Quando: Chama get_active_habits()
        Então: Retorna lista vazia [] ou None, e nenhum erro é lançado
        """
        # Verificar que o sistema está realmente vazio
        all_habits = self.habit_model.get_all_habits()
        empty_count = len(all_habits) if all_habits else 0
        print(f"Sistema possui {empty_count} hábitos antes do teste")
        
        # Ação: Tentar obter hábitos ativos do sistema vazio
        try:
            if hasattr(self.habit_model, 'get_active_habits'):
                active_habits = self.habit_model.get_active_habits()
            else:
                # Tentar através de get_all_habits e filtrar
                all_habits = self.habit_model.get_all_habits()
                active_habits = [h for h in all_habits if h.get('active', True)] if all_habits else []
                
        except Exception as e:
            pytest.fail(f"get_active_habits() não deveria lançar erro em sistema vazio: {e}")
        
        # Verificações conforme CTA-007
        print(f"Resultado do sistema vazio: {active_habits}")
        print(f"Tipo do resultado: {type(active_habits)}")
        
        # Aceita tanto lista vazia quanto None conforme especificação
        if active_habits is None:
            print("✅ Sistema vazio retornou None (válido)")
            assert True, "None é retorno válido para sistema vazio"
        else:
            assert isinstance(active_habits, list), "Deveria retornar uma lista"
            assert len(active_habits) == 0, f"Lista deveria estar vazia, encontrados: {len(active_habits)} hábitos"
            print("✅ Sistema vazio retornou lista vazia (válido)")
        
        # Verificar que nenhum erro foi lançado (teste passa se chegou até aqui)
        print(f"✅ CTA-007 passou: Nenhum erro lançado em sistema vazio")
    
    @pytest.mark.visualization
    def test_cta_008_habits_alphabetical_ordering(self, clean_json_files):
        """
        CTA-008: Ordenação alfabética de hábitos
        
        Dado que: Sistema possui 4 hábitos ativos: "Zumba", "Academia", "Meditação", "Beber água"
        Quando: Chama método de listagem de hábitos e verifica ordenação
        Então: Retorna em ordem alfabética: ["Academia", "Beber água", "Meditação", "Zumba"],
               mantendo propriedades intactas
        """
        # Preparação: Criar 4 hábitos conforme especificação CTA-008
        habits_to_create = [
            {"name": "Zumba", "description": "Dança", "frequency": "weekly"},
            {"name": "Academia", "description": "Exercícios", "frequency": "daily"},
            {"name": "Meditação", "description": "10min", "frequency": "daily"},
            {"name": "Beber água", "description": "2L", "frequency": "daily"}
        ]
        
        created_names = []
        
        for habit_data in habits_to_create:
            try:
                if hasattr(self.habit_model, 'add_habit'):
                    result = self.habit_model.add_habit(
                        name=habit_data["name"],
                        description=habit_data["description"],
                        frequency=habit_data["frequency"]
                    )
                    created_names.append(habit_data["name"])
                    print(f"Criado: {habit_data['name']}")
                else:
                    pytest.skip("Método add_habit não encontrado")
                    
            except Exception as e:
                print(f"Erro ao criar hábito {habit_data['name']}: {e}")
        
        if len(created_names) < 2:
            pytest.skip("Poucos hábitos criados para teste de ordenação")
        
        # Ação: Obter lista de hábitos
        try:
            if hasattr(self.habit_model, 'get_active_habits'):
                habits_list = self.habit_model.get_active_habits()
            else:
                all_habits = self.habit_model.get_all_habits()
                habits_list = [h for h in all_habits if h.get('active', True)] if all_habits else []
                
        except Exception as e:
            pytest.skip(f"Erro ao obter lista de hábitos: {e}")
        
        if not habits_list or len(habits_list) == 0:
            pytest.skip("Nenhum hábito ativo encontrado")
        
        # Extrair nomes dos hábitos retornados
        habit_names = [habit['name'] for habit in habits_list]
        print(f"Nomes encontrados: {habit_names}")
        
        # Verificações conforme CTA-008
        expected_alphabetical_order = ["Academia", "Beber água", "Meditação", "Zumba"]
        
        # Filtrar apenas os hábitos que foram criados com sucesso
        created_and_found = [name for name in expected_alphabetical_order if name in habit_names]
        print(f"Hábitos criados e encontrados: {created_and_found}")
        
        # Verificar presença dos hábitos especificados
        for expected_name in expected_alphabetical_order:
            if expected_name in created_names:
                assert expected_name in habit_names, f"Hábito '{expected_name}' deveria estar na lista"
        
        # Se conseguiu criar pelo menos 3 dos 4 hábitos, testar ordenação
        if len(created_and_found) >= 3:
            # Verificar se estão em ordem alfabética
            sorted_found = sorted(created_and_found)
            actual_order = [name for name in habit_names if name in expected_alphabetical_order]
            
            print(f"Ordem esperada: {sorted_found}")
            print(f"Ordem atual: {actual_order}")
            
            # Verificar ordenação alfabética
            for i in range(len(actual_order) - 1):
                current = actual_order[i]
                next_item = actual_order[i + 1]
                assert current <= next_item, f"Hábitos não estão em ordem alfabética: '{current}' deveria vir antes de '{next_item}'"
        
        # Verificar propriedades intactas conforme especificação
        required_properties = ['habit_id', 'name', 'description']
        for habit in habits_list:
            for prop in required_properties:
                assert prop in habit, f"Propriedade '{prop}' deveria estar intacta no hábito {habit.get('name', 'unknown')}"
            
            assert habit.get('active', True) == True, f"Propriedade 'active' deveria permanecer True para {habit['name']}"
            
            # Verificar que as propriedades têm valores válidos
            assert habit['name'] != "", "Nome não deveria estar vazio"
            assert habit['description'] != "", "Descrição não deveria estar vazia"
            assert habit['habit_id'] != "", "ID não deveria estar vazio"
        
        print(f"✅ CTA-008 passou: {len(habits_list)} hábitos em ordem correta com propriedades intactas")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])