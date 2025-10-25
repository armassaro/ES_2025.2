import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
import uuid
from Model.UserModel import UserModel
from Model.HabitModel import HabitModel
from controller.HabitController import HabitController
from controller.ReportController import ReportController
from View.ConsoleView import ConsoleView

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
