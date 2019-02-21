from indexation import indexerSimple
import iRModel
import numpy as np


class OkapiBM25(iRModel):
    def __init__(self, indexer):
        super().__init(indexer)
        self.k1 = None #1.2
        self.b = None #.75
        
    def getScores(self, query, pertinences=None):
        query = indexerSimple.counter(query)
        
        idf_mot = {mot: self.idf(mot, pertinences) for mot in query.keys()}
        avgdl = sum(len(d.T) for d in self.indexer.docs) / len(self.indexer.docs)
        scores = {}
        for d in self.indexer.docs:
            s = 0
            for mot in query.keys():
                tf_i_d = self.indexer.tf(d, mot)
                score = idf_mot[mot]
                score *= tf_i_d / (tf_i_d + self.k1 * (1 - self.b + self.b*(len(d.T)/avgdl)))
                #todo verbosité saturation L2 Poisson
                s += score
            scores[d] = s
        return scores

    def idf(self, query, pertinences):
        N = len(self.indexer.docs)
        n = len(query)
        if pertinences is None:
            return np.log(N/n)
        r, R = pertinences
        return np.log((r+.5) / (R-r+.5)) * (N - n - R + r + .5) / (n - r + .5)

    def fit(self, debut1, fin1, nbPoint1, debut2, fin2, nbPoint2, donnees, labels):
        rangeK = np.linspace(debut1, fin1, nbPoint1)
        rangeB = np.linspace(debut2, fin2, nbPoint2)
        mapKB = []
        param = []
        for k1 in rangeK:
            for b in rangeB:
                s = 0
                for k in range(len(donnees)):
                    predictionModele = self.getRanking(donnees[k], [k1, b])
                    s += self.avgPrec(predictionModele, labels[k])
                mapKB.append(s/len(donnees))
                param.append([k1, b])
        self.k1, self.b = param[np.argmax(mapKB)]
