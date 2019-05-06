import iRModel


class JelinekMercer(iRModel.IRModel):
    """jelinek-Mercer, suppose :
    indépendances termes doc
    indépendances termes requete
    termes requete distincts"""

    def __init__(self, indexer, lamb=.8):
        super().__init__(indexer)
        self.lamb = lamb

    def _getScores(self, query, pertinences=None):
        if self.lamb is None:
            raise AttributeError("fit has not been called")
        
        len_coll = sum(len(d.T) for d in self.indexer.docs.values())

        #facteurs de lissage de chaque terme de la requete (définis par la collection)
        p_q_mc = {}
        for t, tf_q in query.items():
            p_q_mc[t] = sum(self.indexer.ind[d.I].get(t, 0) for d in self.indexer.docs.values()) / len_coll

        #scores de chaque doc
        scores = {}
        for t in query.keys():
            for iDoc in self.indexer.inv[t].keys():
                scores[iDoc] = scores.get(iDoc, 1) * ((1-self.lamb) * self.indexer.ind_n[iDoc][t] + self.lamb * p_q_mc[t])

        return scores

    def fit(self, possibilities, donnees, labels):
        l_max, s_max = 0, float("-inf")
        for l in possibilities:
            self.lamb = l
            s = 0
            for k in range(len(donnees)):
                predictionModele = self.getRanking(donnees[k])
                s += self.avgPrec(predictionModele, labels[k])
            if s > s_max:
                s_max = s
                l_max = l
        
        self.lamb = l_max
