from random import randint

class Player:
    name: str
    
    def __init__(self, name: str) -> None:
        self.name = name
        
    def move(self, current: int, min_step: int, max_step: int, goal: int) -> int:
        raise NotImplemented

class UserPlayer(Player):
    def __init__(self, name: str) -> None:
        super().__init__(name)

class StrategicPlayer(Player):
    def __init__(self, name: str) -> None:
        super().__init__(name)

class RandomPlayer(Player):
    def __init__(self, name: str) -> None:
        super().__init__(name)