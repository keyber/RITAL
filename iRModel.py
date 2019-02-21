from abc import ABC, abstractmethod
import numpy as np


class IRModel(ABC):
    def __init__(self, indexer):
        self.indexer = indexer
    
    @abstractmethod
    def getScores(self, query, pertinences=None):
        """{doc : score}"""
        pass
    
    def getRanking(self, query):
        """[(doc, score)] triée"""
        return sorted(self.getScores(query).items(), key=lambda x: x[1], reverse=True)

    def avgPrec(self, pred, lab):
        point = []
        for k in range(len(lab)):
            data = pred[:k]
            theorique = lab[:k]
            nbCorrect = 0
            for d in data:
                if d in theorique:
                    nbCorrect += 1
            rappel = nbCorrect / len(lab)
            precision = nbCorrect / len(data)
            point.append([rappel, precision])
        pointRappel = np.linspace(0, 1, 11)
        pointFinal = []
        for p in pointRappel:
            pointFinal.append(np.interp(p, [p[0] for p in point], [p[1] for p in point]))
        return np.mean(pointFinal)
