from abc import ABC, abstractmethod

class Constraint(ABC):
    @abstractmethod
    def validate(self) -> bool:
        pass