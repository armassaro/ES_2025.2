class HabitController:
    """Controller: Intermediário entre View e HabitModel."""
    
    def __init__(self, model):
        self.model = model

    def handle_create_habit_request(self, name, description="", frequency="daily"):
        """Lida com a solicitação de criação de hábito."""
        self._log_action(f"Criando hábito '{name}'")
        return self.model.create_habit(name, description, frequency)

    def handle_read_habits_request(self):
        """Lida com a solicitação de leitura de hábitos."""
        self._log_action("Buscando hábitos...")
        habits = self.model.get_all_habits()
        self._log_action(f"Retornando {len(habits)} hábitos")
        return habits

    def handle_update_habit_request(self, habit_id, name=None, description=None, active=None, frequency=None, color=None):
        """Lida com a solicitação de atualização de hábito."""
        self._log_action(f"Atualizando hábito ID={habit_id}")
        self._log_details({
            'Nome': name,
            'Descrição': description,
            'Ativo': active,
            'Frequência': frequency,
            'Cor': color
        })
        return self.model.update_habit(habit_id, name, description, active, frequency, color)

    def handle_delete_habit_request(self, habit_id):
        """Lida com a solicitação de exclusão de hábito."""
        self._log_action(f"Deletando hábito ID={habit_id}")
        return self.model.delete_habit(habit_id)

    def handle_mark_done_request(self, habit_id, date=None):
        """Lida com a solicitação de marcar hábito como concluído."""
        self._log_action(f"Marcando hábito ID={habit_id} como concluído em {date}")
        result = self.model.mark_habit_done(habit_id, date)
        self._log_action(f"Resultado do model = {result}")
        return result
    
    def _log_action(self, message):
        """Método auxiliar para logging centralizado."""
        print(f"[CONTROLLER] {message}")
    
    def _log_details(self, details):
        """Método auxiliar para logging de detalhes."""
        for key, value in details.items():
            if value is not None:
                print(f"   - {key}: {value}")