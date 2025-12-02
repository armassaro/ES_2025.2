import json
import uuid
from datetime import datetime
from abc import ABC, abstractmethod

HABIT_DATA_FILE = "habitos_registros.json"

def load_data(filepath, default_value):
    """Carrega dados de um arquivo JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default_value
    except json.JSONDecodeError:
        print(f" Aviso: Arquivo {filepath} corrompido.")
        return default_value

def save_data(filepath, data):
    """Salva dados em um arquivo JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

class Subject(ABC):
    """Sujeito (Subject): O HabitModel implementará esta interface."""
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    @abstractmethod
    def notify(self):
        pass

class HabitModel(Subject):
    """Model: Gerencia hábitos e implementa Subject (Observer Pattern)."""
    
    def __init__(self, user_model):
        super().__init__()
        self.user_model = user_model
        self.data = load_data(HABIT_DATA_FILE, {})
        self._migrate_data_add_color()
    
    def _migrate_data_add_color(self):
        """Migra dados antigos para adicionar a chave 'color' se não existir."""
        for username in self.data:
            for habit in self.data[username]:
                if 'color' not in habit:
                    habit['color'] = 'blue'
        if self.data:  # Only save if there's data to save
            save_data(HABIT_DATA_FILE, self.data)

    def notify(self):
        """Notifica todos os observers sobre mudanças."""
        for observer in self._observers:
            observer.update(self)

    def create_habit(self, name, description="", frequency="daily"):
        """
        Cria um novo hábito (R1 - Create).
        
        Args:
            name: Nome do hábito
            description: Descrição do hábito (opcional)
            frequency: Frequência do hábito ('daily', 'weekly', 'monthly')
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        username = self.user_model.get_logged_in_username()
        if not username:
            return False, "Nenhum usuário logado."
        
        # Validação de entrada
        if not name or not name.strip():
            return False, "Nome do hábito não pode estar vazio."
        
        valid_frequencies = ['daily', 'weekly', 'monthly']
        if frequency not in valid_frequencies:
            return False, f"Frequência inválida. Use: {', '.join(valid_frequencies)}"

        if username not in self.data:
            self.data[username] = []

        habit = {
            "id": str(uuid.uuid4()),
            "name": name.strip(),
            "description": description.strip(),
            "frequency": frequency,
            "active": True,
            "color": "blue",
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
            print("[AVISO] Nenhum usuario logado!")
            return []
        
        habits = self.data.get(username, [])
        print(f"[INFO] Model: Buscando habitos para '{username}': {len(habits)} encontrados")
        return habits

    def update_habit(self, habit_id, name=None, description=None, active=None, frequency=None, color=None):
        """Atualiza um hábito existente (R1 - Update)."""
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
                if color is not None:
                    habit['color'] = color
                
                save_data(HABIT_DATA_FILE, self.data)
                self.notify()
                print(f"[INFO] Model: Habito '{habit['name']}' atualizado com sucesso!")
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

        print(f"[INFO] Model: Marcando habito {habit_id} em {date}")
        
        username = self.user_model.get_logged_in_username()
        if not username or username not in self.data:
            print(f"[AVISO] Model: Usuario nao encontrado ({username})")
            return False, "Usuário não encontrado."

        for habit in self.data[username]:
            if habit.get('id') == habit_id:
                # Verificar se já foi marcado
                if date in habit.get('history', {}) and habit['history'][date]:
                    print(f"[INFO] Model: Habito ja marcado em {date}")
                    return False, f"Hábito '{habit['name']}' já foi marcado como concluído em {date}!"

                # Garantir que 'history' existe
                if 'history' not in habit:
                    habit['history'] = {}
                
                # Marcar como concluído
                habit['history'][date] = True
                
                # Salvar dados
                save_data(HABIT_DATA_FILE, self.data)
                print(f"[INFO] Model: Habito '{habit['name']}' marcado em {date}")
                print(f"   History atualizado: {habit['history']}")
                
                # Notificar observers
                self.notify()
                
                return True, f"Hábito '{habit['name']}' marcado como concluído em {date}!"

        print(f"[AVISO] Model: Habito {habit_id} nao encontrado")
        print(f"   Habitos disponiveis: {[h.get('id') for h in self.data.get(username, [])]}")
        return False, "Hábito não encontrado."