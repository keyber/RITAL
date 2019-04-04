from abc import ABC, abstractmethod
import numpy as np
import indexerSimple

class IRModel(ABC):
    def __init__(self, indexer):
        self.indexer = indexer

    def getScores(self, query, pertinences=None):
        """{doc : score}"""
        #les documents sont stemmés, on stemme donc aussi les mots de la requête
        query = indexerSimple.counter(query)

        #enlève les mots de la requête qui n'apparaissent dans aucun document du corpus
        query = {t:tf for (t,tf) in query.items() if t in self.indexer.inv}

        return self._getScores(query, pertinences)

    @abstractmethod
    def _getScores(self, query, pertinences=None):
        """{doc : score}"""
        pass

    def getRanking(self, query):
        """[(doc, score)] triée par score décroissant puis clé décroissante"""
        return sorted(self.getScores(query).items(), key=lambda x: (x[1], x[0]), reverse=True)

    def avgPrec(self, pred, lab):
        point = []
        for k in range(0, len(lab)):#for k in range(1, len(lab)):
            data = pred[:k+1]#data = pred[:k]
            theorique = lab[:k+1]#theorique = lab[:k]
            nbCorrect = 0
            for d in data:
                if d[0] in theorique:
                    nbCorrect += 1
            rappel = nbCorrect / len(lab)
            precision = nbCorrect / len(data)
            point.append([rappel, precision])
        pointRappel = np.linspace(0, 1, 11)
        pointFinal = []
        if(len(point)!=0):
            for p in pointRappel:
                pointFinal.append(np.interp(p, [p[0] for p in point], [p[1] for p in point]))
            return np.mean(pointFinal)
        else:
            return 0
