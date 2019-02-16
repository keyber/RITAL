import indexerSimple
import iRModel
import numpy as np

class Okapi(iRModel):
    
    def getScores(self, query, k1=1.2, b=.75):
        query = indexerSimple.counter(query)
        
        avgdl = sum(len(d.T) for d in self.indexer.docs) / len(self.indexer.docs)
        scores = {}
        for d in self.indexer.docs:
            s = 0
            for mot in query.keys():
                tf_i_d = self.indexer.tf(d, mot)
                score = idf(mot)
                score *= tf_i_d / (tf_i_d + k1 * (1- b + b*(len(d.T)/avgdl)))
                #todo verbosité saturation L2 Poisson
                s += score
            scores[d] = s
        return scores
    
    def fitCrossValidation(self):
        """détermine les valeurs de lambda, k1 et b optimales"""
        pass

def idf(d, pertinences=None):
    if pertinences is None:
        return np.log(N/n)
    return log((r+.5) / (R-r+.5)) * (N - n - R + r + .5) / (n - r + .5)