class HabitController:
    """Controller: Intermediário entre View e HabitModel."""
    
    def __init__(self, model):
        self.model = model

    def handle_create_habit_request(self, name, description="", frequency="daily"):
        """Lida com a solicitação de criação de hábito."""
        return self.model.create_habit(name, description, frequency)

    def handle_read_habits_request(self):
        """Lida com a solicitação de leitura de hábitos."""
        return self.model.get_all_habits()

    def handle_update_habit_request(self, habit_id, name=None, description=None, active=None, frequency=None):
        """Lida com a solicitação de atualização de hábito."""
        return self.model.update_habit(habit_id, name, description, active, frequency)

    def handle_delete_habit_request(self, habit_id):
        """Lida com a solicitação de exclusão de hábito."""
        return self.model.delete_habit(habit_id)

    def handle_mark_done_request(self, habit_id, date=None):
        """Lida com a solicitação de marcar hábito como concluído."""
        return self.model.mark_habit_done(habit_id, date)