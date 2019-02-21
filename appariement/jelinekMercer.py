from indexation import indexerSimple
import iRModel
import numpy as np


class JelinekMercer(iRModel):
    """jelinek-Mercer, suppose :
    indépendances termes doc
    indépendances termes requete
    termes requete distincts"""

    def __init__(self, indexer):
        super().__init__(indexer)
        self.lamb = None

    def getScores(self, query, params):
        lamb = params[0]
        #suppose indépendances
        query = indexerSimple.counter(query)

        len_coll = sum(len(d.T) for d in self.indexer.docs)

        #facteurs de lissage de chaque terme de la requete (définis par la collection)
        p_q_mc = {}
        for t, tf_q in query.items():
            p_q_mc[t] = sum(self.indexer.ind[d.I][t] for d in self.indexer.docs) / len_coll

        #scores de chaque doc
        scores = {}
        for d in self.indexer.docs:
            score = 1
            for t in query.keys():
                score *= (1-lamb) * self.indexer.ind_n[d][t] + lamb * p_q_mc[t]
            scores[d] = score

        return scores

    def fit(self, debut, fin, nbPoint, donnees, labels):
        rangeLamba = np.linspace(debut, fin, nbPoint)
        mapLambda = []
        for l in rangeLamba:
            s = 0
            for k in range(len(donnees)):
                predictionModele = self.getRanking(donnees[k], [l])
                s += self.avgPrec(predictionModele, labels[k])
            mapLambda.append(s/len(donnees))
        self.lamb = rangeLamba[np.argmax(mapLambda)]
