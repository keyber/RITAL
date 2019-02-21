from indexation import indexerSimple
from appariement import iRModel
import numpy as np


class Okapi(iRModel):
    def getScores(self, query, params):
        k1, b, pertinences = params
        if k1 is None:
            k1 = 1.2
        if b is None:
            b = .75
            
        query = indexerSimple.counter(query)
        
        idf_mot = {mot: self.idf(mot, pertinences) for mot in query.keys()}
        avgdl = sum(len(d.T) for d in self.indexer.docs) / len(self.indexer.docs)
        scores = {}
        for d in self.indexer.docs:
            s = 0
            for mot in query.keys():
                tf_i_d = self.indexer.tf(d, mot)
                score = idf_mot[mot]
                score *= tf_i_d / (tf_i_d + k1 * (1 - b + b*(len(d.T)/avgdl)))
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
