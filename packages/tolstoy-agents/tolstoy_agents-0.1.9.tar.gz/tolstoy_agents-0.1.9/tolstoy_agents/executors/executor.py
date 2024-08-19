from abc import ABC, abstractmethod

class Executor(ABC):
    @abstractmethod
    def __init__(self, context: dict, message: dict)->None:
        pass
    
    @abstractmethod
    def run(self, context: dict, message: dict)->dict:
        pass
