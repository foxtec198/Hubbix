
class Task:
    def __init__(self, name:str, min_people:int = 1, max_people:int = 1) -> None:
        self.name = name
        self.min_people = min_people
        self.max_people = max_people

    def __repr__(self) -> str:
        return f"Task({self.name}, min={self.min_people}, max={self.max_people})"