import random
from datetime import date, timedelta

class SchedularService:
    def __init__(self, employees, tasks) -> None:
        self.employees = employees
        self.tasks = tasks

    def _get_available_employees(self, current_date):
        return [e for e in self.employees if e.is_available(current_date)]

    def _get_absent_employees(self, current_date):
        folga = []
        ferias = []
        for e in self.employees:
            weekday = current_date.strftime("%A").lower()
            if e.ferias:
                ferias.append(e.name)
            elif e.folga == weekday:
                folga.append(e.name)
        return {"folga": folga, "ferias": ferias}

    def _avoid_repetition(self, employees, task_name):
        """Filtra quem não fez a mesma função no último dia."""
        return [e for e in employees if not e.history or e.history[-1] != task_name]

    def generate_schedule(self, start_date: date, days: int):
        schedule = {}

        for i in range(days):
            current_date = start_date + timedelta(days=i)
            day_key = current_date.strftime("%Y-%m-%d")
            available = self._get_available_employees(current_date)
            print(available)
            day_schedule = {
                'Folga':[],
                'Ferias':[]
            }
            random.shuffle(available)

            for e in self.employees:
                weekday = current_date.strftime("%A").lower()
                if e.vacation:
                    day_schedule['Ferias'].append(e.name)
                elif e.day_off == weekday:
                    day_schedule['Folga'].append(e.name)

            # WASH 
            wash_candidates = self._avoid_repetition(available, "Wash")
            random.shuffle(wash_candidates)
            if wash_candidates:
                chosen = wash_candidates.pop(0)
                day_schedule["Wash"] = [chosen.name]
                chosen.add_history("Wash")
                available.remove(chosen)

            # Maquina de Sorvete
            maquina_candidates = self._avoid_repetition(available, "Maquina")
            random.shuffle(maquina_candidates)
            if maquina_candidates:
                chosen = maquina_candidates.pop(0)
                day_schedule["Maquina"] = [chosen.name]
                chosen.add_history("Maquina")
                available.remove(chosen)

            # Cozinha (Restante)
            cozinha_task = next(t for t in self.tasks if t.name == "Cozinha")
            cozinha_people = self._avoid_repetition(available, "Cozinha")
            random.shuffle(cozinha_people)

            cozinha_selected = cozinha_people[:cozinha_task.max_people]
            for c in cozinha_selected:
                c.add_history("Cozinha")

            day_schedule["Cozinha"] = [c.name for c in cozinha_selected]

            schedule[day_key] = day_schedule
        return schedule
