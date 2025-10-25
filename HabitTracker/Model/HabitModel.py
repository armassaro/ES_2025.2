import json
import uuid
from datetime import datetime
from abc import ABC, abstractmethod

# Caminho do arquivo de dados
HABIT_DATA_FILE = "habitos_registros.json"

def load_data(filepath, default_value):
    """Carrega dados de um arquivo JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default_value
    except json.JSONDecodeError:
        return default_value

def save_data(filepath, data):
    """Salva dados em um arquivo JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- PADRÃO OBSERVER (Subject) ---
class Subject(ABC):
    """Sujeito (Subject): O HabitModel implementará esta interface."""
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """Adiciona um observador."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Remove um observador."""
        if observer in self._observers:
            self._observers.remove(observer)

    @abstractmethod
    def notify(self):
        """Notifica todos os observadores."""
        pass

class HabitModel(Subject):
    """Model: Gerencia hábitos e implementa Subject (Observer Pattern)."""
    
    def __init__(self, user_model):
        super().__init__()
        self.user_model = user_model
        self.data = load_data(HABIT_DATA_FILE, {})

    def notify(self):
        """Notifica todos os observers sobre mudanças."""
        for observer in self._observers:
            observer.update(self)

    def create_habit(self, name, description="", frequency="daily"):
        """
        Cria um novo hábito (R1 - Create).
        
        Args:
            name: Nome do hábito
            description: Descrição opcional
            frequency: Frequência ('daily', 'weekly', 'monthly')
        """
        username = self.user_model.get_logged_in_username()
        if not username:
            return False, "Nenhum usuário logado."

        if username not in self.data:
            self.data[username] = []

        habit = {
            "id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "frequency": frequency,  # Nova propriedade
            "active": True,
            "created_at": datetime.now().isoformat(),
            "history": {}
        }

        self.data[username].append(habit)
        save_data(HABIT_DATA_FILE, self.data)
        self.notify()
        return True, f"Hábito '{name}' criado com sucesso!"

    def get_all_habits(self):
        """Retorna todos os hábitos do usuário logado (R1 - Read)."""
        username = self.user_model.get_logged_in_username()
        if not username:
            return []
        return self.data.get(username, [])

    def update_habit(self, habit_id, name=None, description=None, active=None, frequency=None):
        """
        Atualiza um hábito existente (R1 - Update).
        
        Args:
            habit_id: ID do hábito
            name: Novo nome (opcional)
            description: Nova descrição (opcional)
            active: Novo status ativo/inativo (opcional)
            frequency: Nova frequência (opcional)
        """
        username = self.user_model.get_logged_in_username()
        if not username or username not in self.data:
            return False, "Usuário não encontrado."

        for habit in self.data[username]:
            if habit['id'] == habit_id:
                if name is not None:
                    habit['name'] = name
                if description is not None:
                    habit['description'] = description
                if active is not None:
                    habit['active'] = active
                if frequency is not None:
                    habit['frequency'] = frequency
                
                save_data(HABIT_DATA_FILE, self.data)
                self.notify()
                return True, f"Hábito '{habit['name']}' atualizado!"

        return False, "Hábito não encontrado."

    def delete_habit(self, habit_id):
        """Deleta um hábito (R1 - Delete)."""
        username = self.user_model.get_logged_in_username()
        if not username or username not in self.data:
            return False, "Usuário não encontrado."

        initial_count = len(self.data[username])
        self.data[username] = [h for h in self.data[username] if h['id'] != habit_id]

        if len(self.data[username]) < initial_count:
            save_data(HABIT_DATA_FILE, self.data)
            self.notify()
            return True, "Hábito deletado com sucesso!"

        return False, "Hábito não encontrado."

    def mark_habit_done(self, habit_id, date=None):
        """Marca um hábito como concluído em uma data (R2)."""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        username = self.user_model.get_logged_in_username()
        if not username or username not in self.data:
            return False, "Usuário não encontrado."

        for habit in self.data[username]:
            if habit['id'] == habit_id:
                if date in habit.get('history', {}) and habit['history'][date]:
                    return False, f"Hábito '{habit['name']}' já foi marcado como concluído hoje!"

                if 'history' not in habit:
                    habit['history'] = {}
                
                habit['history'][date] = True
                save_data(HABIT_DATA_FILE, self.data)
                self.notify()
                return True, f"Hábito '{habit['name']}' marcado como concluído!"

        return False, "Hábito não encontrado."