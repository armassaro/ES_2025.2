class HabitController:
    """Controller: Intermediário entre View e HabitModel."""
    
    def __init__(self, model):
        self.model = model

    def handle_create_habit_request(self, name, description="", frequency="daily"):
        """Lida com a solicitação de criação de hábito."""
        print(f"🔧 Controller: Criando hábito '{name}'")
        return self.model.create_habit(name, description, frequency)

    def handle_read_habits_request(self):
        """Lida com a solicitação de leitura de hábitos."""
        print("🔧 Controller: Buscando hábitos...")
        habits = self.model.get_all_habits()
        print(f"🔧 Controller: Retornando {len(habits)} hábitos")
        return habits

    def handle_update_habit_request(self, habit_id, name=None, description=None, active=None, frequency=None):
        """Lida com a solicitação de atualização de hábito."""
        print(f"🔧 Controller: Atualizando hábito ID={habit_id}")
        print(f"   - Nome: {name}")
        print(f"   - Descrição: {description}")
        print(f"   - Ativo: {active}")
        print(f"   - Frequência: {frequency}")
        return self.model.update_habit(habit_id, name, description, active, frequency)

    def handle_delete_habit_request(self, habit_id):
        """Lida com a solicitação de exclusão de hábito."""
        print(f"🔧 Controller: Deletando hábito ID={habit_id}")
        return self.model.delete_habit(habit_id)

    def handle_mark_done_request(self, habit_id, date=None):
        """Lida com a solicitação de marcar hábito como concluído."""
        print(f"🔧 Controller: Marcando hábito ID={habit_id} como concluído em {date}")
        return self.model.mark_habit_done(habit_id, date)