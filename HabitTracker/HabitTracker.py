import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

# --- CONFIGURAÇÃO E PERSISTÊNCIA (Arquivos Locais) ---
USER_FILE = "usuarios.json"
HABIT_DATA_FILE = "habitos_registros.json"

def load_data(filepath, default_value):
    """Carrega dados de um arquivo JSON. Se o arquivo não existir, retorna um valor padrão."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default_value
    except json.JSONDecodeError:
        print(f"Aviso: Arquivo {filepath} corrompido. Usando valor padrão.")
        return default_value

def save_data(filepath, data):
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

class Observer(ABC):
    """Observador (Observer): O ReportController implementará esta interface."""
    @abstractmethod
    def update(self, subject):
        """Recebe a notificação de atualização do sujeito."""
        pass

# --- PADRÃO FACTORY METHOD (Para criação de relatórios) ---

class Report(ABC):
    """Produto (Product): Interface comum para todos os relatórios."""
    @abstractmethod
    def generate_visualization_data(self):
        """Método para formatar os dados para exibição no gráfico."""
        pass

class DailyReport(Report):
    """Produto Concreto: Relatório Diário."""
    def __init__(self, raw_data):
        self.raw_data = raw_data
        # Lógica de formatação diária

    def generate_visualization_data(self):
        print("Gerando dados de visualização Diária...")
        # Lógica de cálculo e retorno dos dados diários
        return {"period": "Daily", "data": self.raw_data}

class WeeklyReport(Report):
    """Produto Concreto: Relatório Semanal."""
    def __init__(self, raw_data):
        self.raw_data = raw_data
        # Lógica de formatação semanal

    def generate_visualization_data(self):
        print("Gerando dados de visualização Semanal...")
        # Lógica de cálculo e retorno dos dados semanais
        return {"period": "Weekly", "data": self.raw_data}

class MonthlyReport(Report):
    """Produto Concreto: Relatório Mensal."""
    def __init__(self, raw_data):
        self.raw_data = raw_data
        # Lógica de formatação mensal

    def generate_visualization_data(self):
        print("Gerando dados de visualização Mensal...")
        # Lógica de cálculo e retorno dos dados mensais
        return {"period": "Monthly", "data": self.raw_data}


class ReportFactory:
    """Creator (Fábrica): Utiliza o Factory Method para criar instâncias de Relatório."""
    @staticmethod
    def create_report(report_type, raw_data):
        """Factory Method para instanciar o tipo de relatório solicitado."""
        if report_type == "daily":
            return DailyReport(raw_data)
        elif report_type == "weekly":
            return WeeklyReport(raw_data)
        elif report_type == "monthly":
            return MonthlyReport(raw_data)
        else:
            raise ValueError(f"Tipo de relatório desconhecido: {report_type}")

# --- CAMADA MODEL (Dados e Regras de Negócio) ---

class UserModel:
    """Model de Usuário: Gerencia dados de usuários (R4, R5)."""
    def __init__(self):
        self.users = load_data(USER_FILE, {})
        self.logged_in_user_id = None

    def _generate_user_id(self):
        """Gera um ID de usuário simples para simulação."""
        return str(uuid.uuid4())

    def create_user(self, username, password):
        """Implementar R4: Lógica de criação de usuário."""
        if any(user['username'] == username for user in self.users.values()):
            return False, f"Erro: Usuário '{username}' já existe."
        
        user_id = self._generate_user_id()
        self.users[user_id] = {'username': username, 'password': password, 'id': user_id}
        save_data(USER_FILE, self.users)
        return True, f"Usuário '{username}' criado com sucesso."

    def authenticate(self, username, password):
        """Lógica de autenticação e definição de usuário logado."""
        for user_id, user_data in self.users.items():
            if user_data['username'] == username and user_data['password'] == password:
                self.logged_in_user_id = user_id
                return True, f"Usuário '{username}' logado com sucesso."
        return False, "Erro: Credenciais inválidas."
    
    def get_logged_in_user_id(self):
        return self.logged_in_user_id

    def get_logged_in_username(self):
        """
        [NOVO MÉTODO] Retorna o username do usuário logado.
        Usado pela View para exibir informações amigáveis.
        """
        user_id = self.get_logged_in_user_id()
        if user_id and user_id in self.users:
            return self.users[user_id]['username']
        return None # Ou pode retornar uma string vazia se preferir não mostrar nada

    # Implementar métodos CRUD de usuário (para R4, se necessário)

class HabitModel(Subject):
    """Model de Hábito: Gerencia dados e progresso (R1, R2, R5). É o Sujeito Observer."""
    def __init__(self, user_model):
        super().__init__()
        self.user_model = user_model
        # Estrutura de dados: {user_id: {habits: [...], progress: {...}}}
        self.data = load_data(HABIT_DATA_FILE, {})

    def _get_user_data_structure(self):
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

    def get_user_data(self):
        """
        Método público para o ReportController acessar os dados do usuário.
        Retorna os dados do usuário logado ou None se não houver.
        """
        try:
            return self._get_user_data_structure()
        except PermissionError:
            return None

    def _find_habit_index(self, user_data, habit_id):
        """Encontra o índice de um hábito pelo ID."""
        for i, habit in enumerate(user_data['habits']):
            if habit['id'] == habit_id:
                return i
        return -1

    def create_habit(self, name, description):
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

    def get_habits(self):
        """Implementar R1 (R-Read): Retorna a lista de hábitos do usuário logado."""
        try:
            user_data = self._get_user_data_structure()
            return user_data.get("habits", [])
        except PermissionError:
            return []

    def update_habit(self, habit_id, name=None, description=None, active=None):
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

    def delete_habit(self, habit_id):
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

    def mark_habit_done(self, habit_id, date=None):
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

# --- CAMADA CONTROLLER (Lógica de Controle) ---

class HabitController:
    """Controller de Hábito: Intermedia View e Model para CRUD e Registro."""
    def __init__(self, model):
        self.model = model

    # Métodos CRUD (R1)
    
    def handle_create_habit_request(self, name, desc):
        """Recebe requisição da View para criar um hábito."""
        return self.model.create_habit(name, desc)

    def handle_read_habits_request(self):
        """Recebe requisição da View para ler todos os hábitos."""
        return self.model.get_habits()

    def handle_update_habit_request(self, habit_id, name=None, description=None, active=None):
        """Recebe requisição da View para atualizar um hábito."""
        return self.model.update_habit(habit_id, name, description, active)

    def handle_delete_habit_request(self, habit_id):
        """Recebe requisição da View para deletar um hábito."""
        return self.model.delete_habit(habit_id)

    # Método de Registro (R2)
    
    def handle_mark_done_request(self, habit_id):
        """Recebe requisição da View para marcar o progresso."""
        return self.model.mark_habit_done(habit_id)

# --- CAMADA CONTROLLER e VIEW (Restante) ---

class ReportController(Observer):
    """Controller de Relatório: Lógica de geração de relatórios (R3). É um Observer."""
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.attach(self) # Registra-se como observador

    def update(self, subject):
        """Implementação do Observer: Chamado quando o HabitModel muda (ex: CRUD ou progresso)."""
        print("\n[Sistema]: Notificação recebida. Atualizando relatórios...")
        self.generate_and_display_all_reports()

    def generate_and_display_all_reports(self):
        """Gera e envia todos os dados de relatório para a View."""
        raw_data = self.model.get_user_data() 
        if raw_data is None:
            return # Não gera relatório se não houver usuário

        # Usa o Factory Method para gerar os relatórios (Factory Client)
        daily_report = ReportFactory.create_report("daily", raw_data)
        weekly_report = ReportFactory.create_report("weekly", raw_data)
        monthly_report = ReportFactory.create_report("monthly", raw_data)

        # Prepara dados para a View
        report_data = {
            "daily": daily_report.generate_visualization_data(),
            "weekly": weekly_report.generate_visualization_data(),
            "monthly": monthly_report.generate_visualization_data(),
        }

        self.view.render_reports(report_data)

class ConsoleView:
    """View: Gerencia todas as interações do console (Login, Menus e CRUD)."""
    def __init__(self, habit_controller, user_model):
        self.habit_controller = habit_controller
        self.user_model = user_model

    def show_message(self, message):
        """Exibe uma mensagem simples."""
        print(f"\n{message}")

    def show_error(self, message):
        """Exibe uma mensagem de erro."""
        print(f"\n[ERRO]: {message}")

    # --- R4: Login / Cadastro ---
    def handle_initial_auth(self):
        """Menu de autenticação inicial."""
        while True:
            print("\n--- SISTEMA DE GERENCIAMENTO DE HÁBITOS ---")
            print("1. Login")
            print("2. Criar Nova Conta")
            choice = input("Escolha uma opção (1-2): ")

            if choice == '1':
                username = input("Usuário: ")
                password = input("Senha: ")
                success, message = self.user_model.authenticate(username, password)
                if success:
                    self.show_message(message)
                    return True
                else:
                    self.show_error(message)

            elif choice == '2':
                username = input("Novo Usuário: ")
                password = input("Nova Senha: ")
                success, message = self.user_model.create_user(username, password)
                if success:
                    self.show_message(message)
                    # Tenta logar automaticamente após o cadastro
                    self.user_model.authenticate(username, password) 
                    return True
                else:
                    self.show_error(message)

            else:
                self.show_error("Opção inválida.")
    
    # --- R1: CRUD Interativo ---
    
    def display_habits(self, habits):
        """Exibe a lista de hábitos (Read - R1)."""
        print("\n--- HÁBITOS CADASTRADOS ---")
        if not habits:
            print("Nenhum hábito ativo cadastrado.")
            return

        for i, habit in enumerate(habits):
            status = " [ATIVO]" if habit.get('active', True) else " [INATIVO]"
            print(f"[{i+1}] {habit['name']} (ID: {habit['id']}){status}")
        print("----------------------------")

    def handle_create_habit_input(self):
        """Captura e envia dados para criar um hábito (Create - R1)."""
        print("\n--- CRIAR NOVO HÁBITO ---")
        name = input("Nome do Hábito: ")
        desc = input("Descrição (opcional): ")
        success, message = self.habit_controller.handle_create_habit_request(name, desc)
        if success:
            self.show_message(message)
        else:
            self.show_error(message)

    def handle_update_habit_input(self):
        """Captura e envia dados para atualizar um hábito (Update - R1)."""
        habits = self.habit_controller.handle_read_habits_request()
        if not habits:
            self.show_error("Não há hábitos para atualizar.")
            return

        self.display_habits(habits)
        habit_id = input("Digite o ID do hábito a ser atualizado: ")

        # Lógica de atualização simplificada
        print("\n--- ATUALIZAR HÁBITO ---")
        name = input("Novo Nome (deixe vazio para manter): ") or None
        desc = input("Nova Descrição (deixe vazio para manter): ") or None
        active_input = input("Status Ativo (S/N, deixe vazio para manter): ")
        active = {'S': True, 'N': False}.get(active_input.upper(), None)

        success, message = self.habit_controller.handle_update_habit_request(
            habit_id, name, desc, active
        )
        if success:
            self.show_message(message)
        else:
            self.show_error(message)

    def handle_delete_habit_input(self):
        """Captura o ID para deletar um hábito (Delete - R1)."""
        habits = self.habit_controller.handle_read_habits_request()
        if not habits:
            self.show_error("Não há hábitos para deletar.")
            return

        self.display_habits(habits)
        habit_id = input("Digite o ID do hábito a ser DELETADO: ")
        
        success, message = self.habit_controller.handle_delete_habit_request(habit_id)
        if success:
            self.show_message(message)
        else:
            self.show_error(message)

    # --- R2: Registro de Progresso ---

    def handle_mark_done_input(self):
        """Captura o ID para marcar o progresso (R2)."""
        habits = self.habit_controller.handle_read_habits_request()
        if not habits:
            self.show_error("Não há hábitos para registrar progresso.")
            return

        print("\n--- REGISTRAR PROGRESSO DIÁRIO ---")
        self.display_habits(habits)
        habit_id = input("Digite o ID do hábito que você concluiu hoje: ")
        
        success, message = self.habit_controller.handle_mark_done_request(habit_id)
        if success:
            self.show_message(message)
        else:
            self.show_error(message)

    # --- R3: Exibição de Relatórios ---
    
    def render_reports(self, report_data):
        """Simula a renderização dos gráficos com os dados formatados."""
        print("\n--- REPORT VIEW: RELATÓRIOS ATUALIZADOS ---")
        for period, data in report_data.items():
            print(f"Relatório {data['period']}: Dados de visualização gerados. (Modelo notificado)")
        print("-----------------------------------------")


def setup_architecture(user_model):
    """Inicializa todos os componentes e estabelece as conexões MVC/Padrões."""
    
    # Models
    habit_model = HabitModel(user_model)

    # Views (O ReportController precisa da ReportView, que agora é a ConsoleView)
    console_view = ConsoleView(None, user_model) 
    
    # Controllers
    habit_controller = HabitController(habit_model)
    report_controller = ReportController(habit_model, console_view) # ReportController é o Observer

    # Conecta o Controller de Hábito na View
    console_view.habit_controller = habit_controller
    
    return console_view, report_controller

def run_main_menu(console_view):
    """Loop principal da aplicação após o login."""
    while True:
        # [CORREÇÃO AQUI] Usa o novo método para obter o username
        logged_in_username = console_view.user_model.get_logged_in_username()
        
        print("\n--- MENU PRINCIPAL ---")
        # Exibe o username
        print(f"Usuário Logado: {logged_in_username}") 
        
        print("1. Ver Meus Hábitos (Read - R1)")
        print("2. Criar Novo Hábito (Create - R1)")
        print("3. Atualizar Hábito (Update - R1)")
        print("4. Deletar Hábito (Delete - R1)")
        print("5. REGISTRAR PROGRESSO (R2)")
        print("6. Gerar Relatórios (R3)")
        print("7. Sair")
        
        choice = input("Escolha uma opção (1-7): ")

        if choice == '1':
            habits = console_view.habit_controller.handle_read_habits_request()
            console_view.display_habits(habits)
        elif choice == '2':
            console_view.handle_create_habit_input()
        elif choice == '3':
            console_view.handle_update_habit_input()
        elif choice == '4':
            console_view.handle_delete_habit_input()
        elif choice == '5':
            console_view.handle_mark_done_input()
        elif choice == '6':
            # Chama o ReportController diretamente para forçar a atualização dos relatórios
            # O ReportController é notificado e dispara a geração dos relatórios
            console_view.habit_controller.model.notify()
        elif choice == '7':
            print("Saindo do Habit Tracker. Volte sempre!")
            break
        else:
            console_view.show_error("Opção inválida. Tente novamente.")


def run_app():
    """Função de entrada que inicia o processo de autenticação e o menu principal."""
    # Inicializa o Modelo de Usuário (carrega usuarios.json)
    user_model = UserModel()
    
    # Inicializa toda a arquitetura MVC e padrões
    console_view, _ = setup_architecture(user_model)

    # R4: Handle Login/Cadastro
    if console_view.handle_initial_auth():
        # Após o sucesso da autenticação, inicia o menu principal
        run_main_menu(console_view)
    else:
        console_view.show_error("Falha na autenticação. Encerrando o aplicativo.")


if __name__ == "__main__":
    # Limpa os arquivos de persistência para uma simulação limpa, se quiser:
    # if os.path.exists(USER_FILE): os.remove(USER_FILE)
    # if os.path.exists(HABIT_DATA_FILE): os.remove(HABIT_DATA_FILE)
    
    run_app()
