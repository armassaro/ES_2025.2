import json
import uuid
from typing import Tuple, Dict, Any

USER_FILE = "usuarios.json"

def load_data(filepath: str, default_value):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default_value
    except json.JSONDecodeError:
        print(f"Aviso: Arquivo {filepath} corrompido. Usando valor padrão.")
        return default_value

def save_data(filepath: str, data) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


class UserModel:
    """Model de Usuário: Gerencia dados de usuários (R4, R5)."""
    def __init__(self) -> None:
        self.users: Dict[str, Dict[str, Any]] = load_data(USER_FILE, {})
        self.logged_in_user_id: str | None = None

    def _generate_user_id(self) -> str:
        """Gera um ID de usuário simples para simulação."""
        return str(uuid.uuid4())

    def create_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Implementar R4: Lógica de criação de usuário."""
        if any(user['username'] == username for user in self.users.values()):
            return False, f"Erro: Usuário '{username}' já existe."

        user_id = self._generate_user_id()
        self.users[user_id] = {'username': username, 'password': password, 'id': user_id}
        save_data(USER_FILE, self.users)
        return True, f"Usuário '{username}' criado com sucesso."

    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """Lógica de autenticação e definição de usuário logado."""
        for user_id, user_data in self.users.items():
            if user_data['username'] == username and user_data['password'] == password:
                self.logged_in_user_id = user_id
                return True, f"Usuário '{username}' logado com sucesso."
        return False, "Erro: Credenciais inválidas."

    def get_logged_in_user_id(self) -> str | None:
        return self.logged_in_user_id

    def get_logged_in_username(self) -> str | None:
        """
        Retorna o username do usuário logado.
        Usado pela View para exibir informações amigáveis.
        """
        user_id = self.get_logged_in_user_id()
        if user_id and user_id in self.users:
            return self.users[user_id]['username']
        return None