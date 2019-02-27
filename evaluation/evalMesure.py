from abc import ABC, abstractmethod

class EvalMesure(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def evalQuery(liste,query):
        pass
