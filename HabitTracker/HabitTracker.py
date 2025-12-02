import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
import uuid
from model.UserModel import UserModel
from model.HabitModel import HabitModel
from controller.HabitController import HabitController
from controller.ReportController import ReportController
from view.ConsoleView import ConsoleView

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

def setup_architecture(user_model, view_type='console'):
    """Inicializa todos os componentes e estabelece as conexões MVC/Padrões."""
    
    # Models
    habit_model = HabitModel(user_model)
    
    # Controllers
    habit_controller = HabitController(habit_model)
    
    # Views (escolhe entre Console ou GUI)
    if view_type == 'gui':
        from view.gui.MainWindow import GUIReportView
        report_view = GUIReportView()
    else:
        report_view = ConsoleView(None, user_model)
        report_view.habit_controller = habit_controller
    
    # ReportController é o Observer
    report_controller = ReportController(habit_model, report_view)
    
    return report_view, habit_controller, report_controller

def run_main_menu(console_view, report_controller):
    """Loop principal da aplicação após o login (apenas para Console)."""
    while True:
        logged_in_username = console_view.user_model.get_logged_in_username()
        
        print("\n--- MENU PRINCIPAL ---")
        print(f"Usuário Logado: {logged_in_username}") 
        
        print("1. Ver Meus Hábitos (Read - R1)")
        print("2. Criar Novo Hábito (Create - R1)")
        print("3. Atualizar Hábito (Update - R1)")
        print("4. Deletar Hábito (Delete - R1)")
        print("5. REGISTRAR PROGRESSO (R2)")
        print("6. Gerar Relatórios Padrão (Diário, Semanal, Mensal) (R3)")
        print("7. Gerar Relatório Personalizado por Período (R3)")
        print("8. Exportar Relatório em PDF")
        print("9. Sair")
        
        choice = input("Escolha uma opção (1-9): ")

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
            console_view.habit_controller.model.notify()
        elif choice == '7':
            console_view.handle_custom_report_input(report_controller)
        elif choice == '8':
            console_view.handle_export_pdf_input()
        elif choice == '9':
            print("Saindo do Habit Tracker. Volte sempre!")
            break
        else:
            console_view.show_error("Opção inválida. Tente novamente.")


def run_app_console():
    """Função de entrada para versão Console."""
    user_model = UserModel()
    console_view, habit_controller, report_controller = setup_architecture(user_model, view_type='console')
    #                                 ^^^^^^^^^^^^^^^^ NÃO DESCARTE ISSO!

    if console_view.handle_initial_auth():
        run_main_menu(console_view, report_controller)
    else:
        console_view.show_error("Falha na autenticação. Encerrando o aplicativo.")


def run_app_gui():
    """Função de entrada para versão GUI."""
    from view.gui.LoginWindow import LoginWindow
    from view.gui.MainWindow import MainWindow
    
    user_model = UserModel()
    
    print(f"[HabitTracker.py] Usuários cadastrados: {list(user_model.users.keys())}")
    
    login_window = LoginWindow(user_model)
    authenticated = login_window.run()
    
    if not authenticated:
        print("❌ Login cancelado.")
        return
    
    print(f"[SUCESSO] Usuário autenticado: {user_model.get_logged_in_username()}")
    print(f"   ID: {user_model.get_logged_in_user_id()}")
    
    report_view, habit_controller, report_controller = setup_architecture(user_model, view_type='gui')
    
    # DEBUG: Verificar hábitos carregados
    habits = habit_controller.handle_read_habits_request()
    print(f"[INFO] Hábitos carregados: {len(habits)}")
    for i, h in enumerate(habits):
        print(f"   {i+1}. {h.get('name')} (ID: {h.get('id')})")
    
    main_window = MainWindow(habit_controller, user_model)
    main_window.run()


if __name__ == "__main__":
    # Permite escolher qual interface usar
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--gui':
        run_app_gui()
    else:
        run_app_console()
