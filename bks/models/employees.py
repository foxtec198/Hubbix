from datetime import date

# Modelo de Funcionario
class Employee:
    def __init__(self, name:str, day_off:str, vacation:bool = False) -> None:
        """
            Name - Nome do Colaborador
            Day_off - Seta a folga do colaborador por semana, entao se é Seg, Ter, Qua, Qui
            Vacation - Define se está de folga ou não
            History - Historico de Funções já realizadas
        """

        # Variaveis Obrigatorias
        self.name = name
        self.day_off = day_off.lower()
        self.vacation = vacation
        self.history = [] # Historico de funções
        
        
    def is_available(self, current_date: date) -> bool:
        weekday = current_date.strftime("%A").lower()
        if self.vacation or weekday == self.day_off:
            return False
        return True

    def add_history(self, task_name: str) -> None:
        self.history.append(task_name)

    def __repr__(self) -> str:
        return f"{self.name} (folga={self.day_off}, ferias={self.vacation})"
