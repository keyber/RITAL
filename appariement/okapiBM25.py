import iRModel
import numpy as np


class OkapiBM25(iRModel.IRModel):
    def __init__(self, indexer, k1=1.2, b=.75):
        super().__init__(indexer)
        self.k1 = k1 #1.2
        self.b = b #.75

    def _getScores(self, query, pertinences=None):
        if self.k1 is None or self.b is None:
            raise AttributeError("fit has not been called")

        idf_mot = {mot: self.idf(mot, pertinences) for mot in query.keys()}
        avgdl = sum(len(d.T) for d in self.indexer.docs.values()) / len(self.indexer.docs)
        scores = {}
        for mot in query.keys():
            for iDoc in self.indexer.inv[mot].keys():
                tf_i_d = self.indexer.tf(iDoc, mot)
                score = idf_mot[mot]
                
                score *= tf_i_d / (tf_i_d + self.k1 * (1 - self.b + self.b*(len(self.indexer.docs[iDoc].T)/avgdl)))
                #todo verbosité saturation L2 Poisson ?
                scores[iDoc] = scores.get(iDoc, 0) + score
        return scores

    def idf(self, query, pertinences):
        N = len(self.indexer.docs)
        n = len(query)
        if pertinences is None:
            return np.log(N/n)
        r, R = pertinences
        return np.log((r+.5) / (R-r+.5)) * (N - n - R + r + .5) / (n - r + .5)

    def fit(self, possibilities, donnees, labels):
        # from sklearn.model_selection import cross_validate
        
        rangeK = possibilities[0]
        rangeB = possibilities[1]
        k1_max, b_max, s_max = 0, 0, float("-inf")
        for k1 in rangeK:
            self.k1 = k1
            for b in rangeB:
                self.b = b
                s = 0
                for k in range(len(donnees)):
                    predictionModele = self.getRanking(donnees[k])
                    s += self.avgPrec(predictionModele, labels[k])
                    
                if s > s_max:
                    s_max = s
                    k1_max = k1
                    b_max = b
                    
        self.k1, self.b = k1_max, b_max
