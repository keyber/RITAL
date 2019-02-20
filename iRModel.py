from abc import ABC, abstractmethod


class IRModel(ABC):
    def __init__(self, indexer):
        self.indexer = indexer
    
    @abstractmethod
    def getScores(self, query):
        """{doc : score}"""
        pass
    
    def getRanking(self, query):
        """[(doc, score)] triée"""
        return sorted(self.getScores(query, params).items(), key=lambda x: x[1], reverse=True)
    
    @abstractmethod
    def fitCrossValidation(self):
        """détermine les valeurs optimales des paramètres"""
        pass
