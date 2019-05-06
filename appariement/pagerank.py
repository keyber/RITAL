import iRModel
import random


def _calculSomme(Pr):
    somme = 0
    for key in Pr.keys():
        somme += Pr[key]
    return somme


def _compte(j, liste):
    compteur = 0
    for el in liste:
        if el == j:
            compteur += 1
    return compteur

class PagerankMarcheAlea(iRModel.IRModel):
    def __init__(self, indexer, modelSimple):
        super().__init__(indexer)
        self.indexer = indexer
        # on ne fit pas le modèle
        self.model = modelSimple
        self.n = 10
        self.k = 5
        self.max_iter = 1000
        self.d = .85
        
    def _getScores(self, query, pertinences=None):
        apriori = self.model._getScores(query)
        rankings = sorted(apriori.items(), key=lambda x: (x[1], x[0]), reverse=True)[:self.n]
        
        graphe = set([doc[0] for doc in rankings])
        # cela détermine un graphe initial de documents
    
        # on étend ce graphe en rajoutant des documents pointés par et pointant vers le graphe actuel
        for d, _ in rankings:
            # on ajoute tous les docs pointés par d
            graphe |= set(self.indexer.pointed_by[d])
        
            # on ajoute k docs (au plus) pointant d
            points_to = self.indexer.points_to[d]
            graphe |= set(random.sample(points_to, min(self.k, len(points_to))))
        
        return calculPr(graphe, self.indexer.points_to, max_iter=self.max_iter, apriori=apriori, d=self.d)

    def fit(self, possibilities, donnees, labels):
        rangeK = possibilities
        d_max, s_max = 0, float("-inf")
        for d in rangeK:
            self.d = d
            s = 0
            for k in range(len(donnees)):
                predictionModele = self.getRanking(donnees[k])
                s += self.avgPrec(predictionModele, labels[k])

            if s > s_max:
                s_max = s
                d_max = d

        self.d = d_max
    
def calculPr(sommet, arc, apriori=None, d=.85, max_iter=100, eps=1e-9):
    if apriori is None:
        apriori = {s: 1 for s in sommet}
    n = len(sommet)
    pr = {i: 1 / n for i in sommet}
    sommePr = _calculSomme(pr)
    sommeAncienPr = -9999999
    compteur = 0
    while abs(sommePr - sommeAncienPr) > eps and compteur < max_iter:
        tempPr = dict()
        for j in sommet:
            somme = 0
            for i in sommet:
                if j in arc[i]:
                    somme += (pr[i] / len(arc[i])) * _compte(j, arc[i])
            tempPr[j] = d * somme + (1 - d) * apriori[j]
        sommeAncienPr = _calculSomme(pr)
        sommePr = _calculSomme(tempPr)
        pr = tempPr
        compteur += 1
    return pr
    # return sorted(pr.items(), key=lambda x:(x[1], x[0]), reverse=True)
