import json
import uuid
from abc import ABC
from datetime import datetime
from typing import Tuple, Dict, List, Any

HABIT_DATA_FILE = "habitos_registros.json"

def load_data(filepath: str, default_value):
    """Carrega dados de um arquivo JSON. Se o arquivo não existir, retorna um valor padrão."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default_value
    except json.JSONDecodeError:
        print(f"Aviso: Arquivo {filepath} corrompido. Usando valor padrão.")
        return default_value

def save_data(filepath: str, data) -> None:
    """Salva dados em um arquivo JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


# --- PADRÃO OBSERVER (Para notificação de relatórios) ---

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
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self):
        """Notifica todos os observadores sobre uma mudança de estado."""
        for observer in self._observers:
            observer.update(self)


class HabitModel(Subject):
    """Model de Hábito: Gerencia dados e progresso (R1, R2, R5). É o Sujeito Observer."""
    def __init__(self, user_model):
        super().__init__()
        self.user_model = user_model
        # Estrutura de dados: {user_id: {habits: [...], progress: {...}}}
        self.data: Dict[str, Dict[str, Any]] = load_data(HABIT_DATA_FILE, {})

    def _get_user_data_structure(self) -> Dict[str, Any]:
        """
        Garante que a estrutura de dados para o usuário logado exista.
        Deve ser usado internamente (por isso o '_').
        """
        user_id = self.user_model.get_logged_in_user_id()
        if not user_id:
            raise PermissionError("Nenhum usuário logado.")
        
        if user_id not in self.data:
            self.data[user_id] = {"habits": [], "progress": {}}
        
        return self.data[user_id]

    def get_user_data(self) -> Dict[str, Any] | None:
        """
        Método público para o ReportController acessar os dados do usuário.
        Retorna os dados do usuário logado ou None se não houver.
        """
        try:
            return self._get_user_data_structure()
        except PermissionError:
            return None

    def _find_habit_index(self, user_data: Dict[str, Any], habit_id: str) -> int:
        """Encontra o índice de um hábito pelo ID."""
        for i, habit in enumerate(user_data['habits']):
            if habit['id'] == habit_id:
                return i
        return -1

    def create_habit(self, name: str, description: str) -> Tuple[bool, str]:
        """Implementar R1 (C-Create): Criação de novo hábito para o usuário logado."""
        try:
            user_data = self._get_user_data_structure()
            
            new_habit = {
                "id": str(uuid.uuid4()),
                "name": name,
                "description": description,
                "created_at": datetime.now().isoformat(),
                "active": True
            }
            
            user_data["habits"].append(new_habit)
            
            self.notify() # Notifica observadores (ReportController)
            save_data(HABIT_DATA_FILE, self.data)
            return True, f"Hábito '{name}' criado com sucesso (ID: {new_habit['id']})."
            
        except PermissionError as e:
            return False, f"Erro de permissão: {e}"

    def get_habits(self) -> List[Dict[str, Any]]:
        """Implementar R1 (R-Read): Retorna a lista de hábitos do usuário logado."""
        try:
            user_data = self._get_user_data_structure()
            return user_data.get("habits", [])
        except PermissionError:
            return []

    def update_habit(self, habit_id: str, name: str = None, description: str = None, active: bool = None) -> Tuple[bool, str]:
        """Implementar R1 (U-Update): Atualiza os detalhes de um hábito."""
        try:
            user_data = self._get_user_data_structure()
            index = self._find_habit_index(user_data, habit_id)
            
            if index == -1:
                return False, f"Erro: Hábito com ID {habit_id} não encontrado."
            
            habit = user_data['habits'][index]
            
            if name is not None:
                habit['name'] = name
            if description is not None:
                habit['description'] = description
            if active is not None:
                habit['active'] = active
            
            self.notify() # Notifica observadores (ReportController)
            save_data(HABIT_DATA_FILE, self.data)
            return True, f"Hábito '{habit['name']}' atualizado com sucesso."
            
        except PermissionError as e:
            return False, f"Erro de permissão: {e}"

    def delete_habit(self, habit_id: str) -> Tuple[bool, str]:
        """Implementar R1 (D-Delete): Remove um hábito e seu histórico de registros (simplificado)."""
        try:
            user_data = self._get_user_data_structure()
            index = self._find_habit_index(user_data, habit_id)
            
            if index == -1:
                return False, f"Erro: Hábito com ID {habit_id} não encontrado para exclusão."
            
            deleted_habit = user_data['habits'].pop(index)
            
            # TODO: Lógica de exclusão do histórico de progresso (R2)
            
            self.notify() # Notifica observadores (ReportController)
            save_data(HABIT_DATA_FILE, self.data)
            return True, f"Hábito '{deleted_habit['name']}' excluído com sucesso."
            
        except PermissionError as e:
            return False, f"Erro de permissão: {e}"

    def mark_habit_done(self, habit_id: str, date: str = None) -> Tuple[bool, str]:
        """Implementar R2: Registro diário de progresso."""
        try:
            user_data = self._get_user_data_structure()
            date_str = date if date else datetime.now().strftime("%Y-%m-%d")
            
            index = self._find_habit_index(user_data, habit_id)
            if index == -1:
                return False, f"Erro: Hábito com ID {habit_id} não encontrado."

            # Estrutura: progress = { "YYYY-MM-DD": [habit_id_1, habit_id_2, ...] }
            if date_str not in user_data['progress']:
                user_data['progress'][date_str] = []
            
            if habit_id not in user_data['progress'][date_str]:
                user_data['progress'][date_str].append(habit_id)
                self.notify() # Notifica o ReportController que houve uma mudança
                save_data(HABIT_DATA_FILE, self.data)
                return True, f"Progresso registrado para '{user_data['habits'][index]['name']}' em {date_str}."
            else:
                return False, f"Progresso já registrado para este hábito hoje ({date_str})."

        except PermissionError as e:
            return False, f"Erro de permissão: {e}"