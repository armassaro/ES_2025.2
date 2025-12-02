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
        # Criar UserModel
        self.user_model = UserModel()
        
        # Usar usuário que JÁ EXISTE no usuarios.json
        test_username = "teste"
        test_password = "123"
        
        # Fazer login com usuário existente
        success, msg = self.user_model.authenticate(test_username, test_password)
        
        if not success:
            pytest.fail(f"Falha no login: {msg}")
        
        print(f"Usuario logado: {self.user_model.get_logged_in_username()}")
        
        # Criar HabitModel com o UserModel já logado
        self.habit_model = HabitModel(self.user_model)
        self.habit_controller = HabitController(self.habit_model)
    
    @pytest.mark.visualization
    def test_cta_005_list_all_habits(self, clean_json_files):
        """
        CTA-005: Listar todos os hábitos do usuário
        
        Dado que: O sistema possui hábitos cadastrados
        Quando: Chamo get_all_habits()
        Então: Retorna lista com todos os hábitos do usuário logado
        """
        # Criar alguns hábitos
        habits_to_create = [
            {"name": "Beber agua", "description": "2L por dia", "frequency": "daily"},
            {"name": "Exercicios", "description": "30min diarios", "frequency": "daily"},
            {"name": "Meditar", "description": "10min manha", "frequency": "daily"}
        ]
        
        created_count = 0
        for habit_data in habits_to_create:
            success, msg = self.habit_model.create_habit(
                name=habit_data["name"],
                description=habit_data["description"],
                frequency=habit_data["frequency"]
            )
            if success:
                created_count += 1
                print(f"Criado: {habit_data['name']}")
        
        print(f"Total criado: {created_count}")
        
        # Obter todos os hábitos
        all_habits = self.habit_model.get_all_habits()
        
        # Verificações
        assert all_habits is not None, "get_all_habits() nao deveria retornar None"
        assert len(all_habits) == created_count, f"Deveria ter {created_count} habitos, encontrados: {len(all_habits)}"
        
        # Verificar que todos os hábitos têm os campos necessários
        for habit in all_habits:
            assert 'id' in habit, "Habito deveria ter 'id'"
            assert 'name' in habit, "Habito deveria ter 'name'"
            assert 'description' in habit, "Habito deveria ter 'description'"
            assert 'active' in habit, "Habito deveria ter 'active'"
        
        print(f"OK: {len(all_habits)} habitos listados corretamente")
    
    @pytest.mark.visualization
    def test_cta_006_filter_active_habits(self, clean_json_files):
        """
        CTA-006: Filtrar apenas hábitos ativos
        
        Dado que: Existem hábitos ativos e inativos
        Quando: Filtro por hábitos ativos
        Então: Retorna apenas os hábitos com active=True
        """
        # Criar 3 hábitos
        self.habit_model.create_habit("Habito Ativo 1", "Descricao 1", "daily")
        self.habit_model.create_habit("Habito Ativo 2", "Descricao 2", "daily")
        self.habit_model.create_habit("Habito Inativo", "Descricao 3", "daily")
        
        # Pegar todos os hábitos
        all_habits = self.habit_model.get_all_habits()
        assert len(all_habits) == 3, "Deveria ter 3 habitos"
        
        # Marcar o último como inativo
        inactive_habit_id = all_habits[-1]['id']
        success, msg = self.habit_model.update_habit(inactive_habit_id, active=False)
        assert success == True, f"Falha ao desativar habito: {msg}"
        
        # Filtrar apenas ativos (manualmente já que não tem método específico)
        all_habits_updated = self.habit_model.get_all_habits()
        active_habits = [h for h in all_habits_updated if h.get('active', True) == True]
        
        # Verificações
        assert len(active_habits) == 2, f"Deveria ter 2 habitos ativos, tem {len(active_habits)}"
        
        # Verificar que o inativo não está na lista
        inactive_names = [h['name'] for h in active_habits]
        assert "Habito Inativo" not in inactive_names, "Habito inativo nao deveria aparecer"
        
        print(f"OK: Filtro de habitos ativos funcionando (2 ativos de 3 totais)")
    
    @pytest.mark.visualization
    def test_cta_007_get_habits_empty_system(self, clean_json_files):
        """
        CTA-007: Sistema vazio sem hábitos
        
        Dado que: Sistema está vazio
        Quando: Chamo get_all_habits()
        Então: Retorna lista vazia sem erros
        """
        # Verificar que está vazio
        all_habits = self.habit_model.get_all_habits()
        empty_count = len(all_habits) if all_habits else 0
        print(f"Sistema possui {empty_count} habitos antes do teste")
        
        # Verificações
        assert all_habits is not None, "Nao deveria retornar None"
        assert isinstance(all_habits, list), "Deveria retornar uma lista"
        assert len(all_habits) == 0, f"Lista deveria estar vazia, tem {len(all_habits)}"
        
        print("OK: Sistema vazio retornou lista vazia")
    
    @pytest.mark.visualization
    def test_cta_008_habit_has_history(self, clean_json_files):
        """
        CTA-008: Verificar que hábito contém histórico
        
        Dado que: Existe um hábito cadastrado
        Quando: Marco o hábito como concluído em uma data
        Então: O histórico é registrado corretamente
        """
        # Criar hábito
        success, msg = self.habit_model.create_habit(
            name="Habito com Historico",
            description="Para testar historico",
            frequency="daily"
        )
        assert success == True, f"Falha ao criar habito: {msg}"
        
        # Pegar o hábito criado
        all_habits = self.habit_model.get_all_habits()
        assert len(all_habits) > 0, "Nenhum habito foi criado"
        
        habit = all_habits[-1]
        habit_id = habit['id']
        
        print(f"Habito criado: {habit['name']} (ID: {habit_id})")
        
        # Marcar como concluído em uma data específica
        test_date = "2025-11-10"
        success, msg = self.habit_model.mark_habit_done(habit_id, test_date)
        
        assert success == True, f"Falha ao marcar habito: {msg}"
        
        # Verificar que o histórico foi atualizado
        all_habits_updated = self.habit_model.get_all_habits()
        updated_habit = [h for h in all_habits_updated if h['id'] == habit_id][0]
        
        # Verificações
        assert 'history' in updated_habit, "Habito deveria ter campo 'history'"
        assert isinstance(updated_habit['history'], dict), "History deveria ser um dicionario"
        assert test_date in updated_habit['history'], f"Data {test_date} deveria estar no historico"
        assert updated_habit['history'][test_date] == True, f"Data {test_date} deveria estar marcada como True"
        
        print(f"OK: Historico registrado corretamente para {test_date}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])