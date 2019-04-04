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
        self.n = 100
        self.k = 10
        self.max_iter = 10
        
    def _getScores(self, query, pertinences=None):
        rankings = sorted(self.model._getScores(query).items(), key=lambda x: (x[1], x[0]), reverse=True)[:self.n]
        
        graphe = set([doc[0] for doc in rankings])
        # cela détermine un graphe initial de documents
    
        # on étend ce graphe en rajoutant des documents pointés par et pointant vers le graphe actuel
        for d, _ in rankings:
            # on ajoute tous les docs pointés par d
            graphe |= set(self.indexer.pointed_by[d])
        
            # on ajoute k docs (au plus) pointant d
            points_to = self.indexer.points_to[d]
            graphe |= set(random.sample(points_to, min(self.k, len(points_to))))
        
        return self.calculPr(graphe, self.indexer.points_to, max_iter=self.max_iter)
    
    def calculPr(self, sommet, arc, apriori=None, d=.85, max_iter=10, eps=1e-5):
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
        print(pr)
        return pr
        # return sorted(pr.items(), key=lambda x:(x[1], x[0]), reverse=True)
