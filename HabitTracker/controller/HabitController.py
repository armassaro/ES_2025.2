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