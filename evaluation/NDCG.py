import evalMesure
import numpy as np


class NDCG(evalMesure.EvalMesure):
    def __init__(self, rang):
        self.rang = rang
    
    def iDCG(self):
        somme = 1
        for k in range(1, self.rang):
            somme += 1 / np.log2(k + 1)
        return somme
        
    def DCG(self, pred, labels):
        labels = set(labels)
        
        somme = 1 if str(pred[0]) in labels else 0
        for k in range(1, self.rang):
            if str(pred[k]) in labels:
                somme += 1 / np.log2(k + 1)
                
        return somme

    def evalQuery(self, pred, labels):
        if len(labels)==0:
            return 0
        
        ndcg = self.DCG(pred, labels) / self.iDCG()
        return ndcg
