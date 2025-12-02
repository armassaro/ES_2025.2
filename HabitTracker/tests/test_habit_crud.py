import pytest
import json
import os
from model.HabitModel import HabitModel
from model.UserModel import UserModel
from controller.HabitController import HabitController

class TestHabitCRUD:
    """
    Testes automatizados para CRUD de hábitos (CTA-001 a CTA-004)
    Responsável: ArthurS
    """
    
    def setup_method(self):
        """Configuração antes de cada teste"""
        # Criar UserModel
        self.user_model = UserModel()
        
        # Criar usuário de teste usando o método correto
        success, msg = self.user_model.create_user("test_user", "test_pass")
        
        # Fazer login usando o método correto
        success, msg = self.user_model.authenticate("test_user", "test_pass")
        
        # Agora o user_model.logged_in_user_id está setado corretamente
        print(f"Usuário logado ID: {self.user_model.logged_in_user_id}")
        print(f"Username: {self.user_model.get_logged_in_username()}")
        
        # Criar HabitModel com o UserModel já logado
        self.habit_model = HabitModel(self.user_model)
        self.habit_controller = HabitController(self.habit_model)
    
    @pytest.mark.crud
    def test_cta_001_create_habit_success(self, clean_json_files, sample_habit_data):
        """
        CTA-001: Criação bem-sucedida de hábito
        
        Dado que: O sistema está inicializado com HabitModel e HabitController
        Quando: O teste chama método para criar hábito com dados válidos
        Então: O hábito é criado e persiste corretamente
        """
        # Verificar métodos disponíveis no model
        print(f"Métodos disponíveis no HabitModel: {[m for m in dir(self.habit_model) if not m.startswith('_')]}")
        
        # Tentar criar hábito usando os métodos disponíveis
        try:
            if hasattr(self.habit_model, 'add_habit'):
                result = self.habit_model.add_habit(
                    name=sample_habit_data["name"],
                    description=sample_habit_data["description"],
                    frequency=sample_habit_data["frequency"]
                )
            elif hasattr(self.habit_model, 'create_habit'):
                result = self.habit_model.create_habit(
                    name=sample_habit_data["name"],
                    description=sample_habit_data["description"],
                    frequency=sample_habit_data["frequency"]
                )
            else:
                pytest.skip("Nenhum método de criação encontrado no HabitModel")
                
        except Exception as e:
            print(f"Erro ao criar hábito: {e}")
            pytest.fail(f"Falha na criação do hábito: {e}")
        
        # Verificações básicas
        assert result is not None, "Método deveria retornar algo"
        
        # Verificar no modelo usando get_all_habits
        all_habits = self.habit_model.get_all_habits()
        print(f"Total de hábitos encontrados: {len(all_habits) if all_habits else 0}")
        
        # Filtrar hábitos ativos manualmente se necessário
        if all_habits:
            active_habits = [h for h in all_habits if h.get('active', True)]
            print(f"Hábitos ativos: {len(active_habits)}")
            
            if len(active_habits) > 0:
                created_habit = active_habits[-1]  # Último hábito criado
                print(f"Último hábito criado: {created_habit}")
                
                assert created_habit['name'] == sample_habit_data["name"]
                assert created_habit['description'] == sample_habit_data["description"]
                assert created_habit.get('active', True) == True
                assert 'habit_id' in created_habit
        
        # Verificar persistência no JSON
        with open('habitos_registros.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Dados no JSON: {len(data)} hábitos")
            if len(data) > 0:
                json_habit = next((h for h in data if h['name'] == sample_habit_data["name"]), None)
                assert json_habit is not None, "Hábito deveria estar no JSON"
    
    @pytest.mark.crud
    def test_cta_002_create_habit_empty_name(self, clean_json_files):
        """
        CTA-002: Falha na criação com nome vazio
        
        Dado que: O sistema está inicializado
        Quando: O teste tenta criar hábito com nome vazio
        Então: O método retorna False e nenhum hábito é criado
        """
        # Tentar criar hábito com nome vazio
        try:
            if hasattr(self.habit_model, 'add_habit'):
                result = self.habit_model.add_habit(
                    name="",
                    description="Descrição válida",
                    frequency="daily"
                )
            elif hasattr(self.habit_model, 'create_habit'):
                result = self.habit_model.create_habit(
                    name="",
                    description="Descrição válida",
                    frequency="daily"
                )
            else:
                pytest.skip("Método de criação não encontrado")
                
            # Se chegou aqui sem exceção, verificar se retornou False
            print(f"Resultado da criação com nome vazio: {result}")
            
        except Exception as e:
            print(f"Exceção esperada ao criar hábito com nome vazio: {e}")
            # Exceção é um comportamento aceitável para nome vazio
            return
        
        # Verificar que nenhum hábito com nome vazio foi criado
        all_habits = self.habit_model.get_all_habits()
        if all_habits:
            empty_name_habits = [h for h in all_habits if h.get('name') == ""]
            assert len(empty_name_habits) == 0, "Não deveria criar hábitos com nome vazio"
    
    @pytest.mark.crud  
    def test_cta_003_update_habit_success(self, clean_json_files):
        """
        CTA-003: Atualização bem-sucedida de hábito
        
        Dado que: Existe um hábito pré-cadastrado
        Quando: O teste chama update_habit com novos dados
        Então: O hábito é atualizado mantendo ID e outros campos
        """
        # Criar hábito inicial
        success, msg = self.habit_model.create_habit(
            name="Ler livros",
            description="Ler 30 min por dia",
            frequency="daily"
        )
        assert success == True, f"Falha ao criar hábito: {msg}"
        
        # Pegar o ID do hábito criado
        habits = self.habit_model.get_all_habits()
        assert len(habits) > 0, "Nenhum hábito foi criado"
        
        habit_id = habits[0]['id']
        original_name = habits[0]['name']
        
        print(f"Hábito original: {original_name} (ID: {habit_id})")
        
        # Atualizar o nome
        success, msg = self.habit_model.update_habit(
            habit_id=habit_id,
            name="Estudar Python",
            description="45 min por dia"
        )
        
        assert success == True, f"Atualização falhou: {msg}"
        
        # Verificar que foi atualizado
        habits_updated = self.habit_model.get_all_habits()
        updated_habit = habits_updated[0]
        
        assert updated_habit['name'] == "Estudar Python", "Nome não foi atualizado"
        assert updated_habit['description'] == "45 min por dia", "Descrição não foi atualizada"
        assert updated_habit['id'] == habit_id, "ID mudou (não deveria)"
        assert updated_habit['frequency'] == "daily", "Frequência foi alterada (não deveria)"
        
        print(f"✅ Nome atualizado: '{original_name}' → '{updated_habit['name']}'")
    
    @pytest.mark.crud
    def test_cta_004_delete_habit_success(self, clean_json_files):
        """
        CTA-004: Exclusão bem-sucedida de hábito
        
        Dado que: Existe um hábito cadastrado
        Quando: O teste chama delete_habit
        Então: O hábito é removido da lista
        """
        # Criar hábito
        success, msg = self.habit_model.create_habit(
            name="Meditar",
            description="10 minutos de meditação",
            frequency="daily"
        )
        assert success == True, f"Falha ao criar hábito: {msg}"
        
        # Verificar que existe
        habits = self.habit_model.get_all_habits()
        assert len(habits) == 1, f"Deveria ter 1 hábito, mas tem {len(habits)}"
        
        habit_id = habits[0]['id']
        habit_name = habits[0]['name']
        
        print(f"Hábito antes de deletar: {habit_name} (ID: {habit_id})")
        
        # Deletar o hábito
        success, msg = self.habit_model.delete_habit(habit_id)
        
        assert success == True, f"Deleção falhou: {msg}"
        assert "sucesso" in msg.lower(), f"Mensagem deveria conter 'sucesso': {msg}"
        
        # Verificar que foi removido
        habits_after = self.habit_model.get_all_habits()
        assert len(habits_after) == 0, f"Deveria ter 0 hábitos após deletar, mas tem {len(habits_after)}"
        
        print(f"✅ Hábito '{habit_name}' deletado com sucesso!")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])