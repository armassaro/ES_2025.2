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