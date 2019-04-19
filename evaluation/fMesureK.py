import evalMesure
class FMesureK(evalMesure.EvalMesure):
    def __init__(self, beta, k):
        self.beta = beta
        self.k = k
    
    def evalQuery(self, pred, labels):
        if len(pred)==0 or len(labels)==0:
            return 0
        
        labels = set(labels)
        compteur = 0
        for p in pred[:self.k]:
            if p[0] in labels:
                compteur+=1
        
        if compteur==0:
            return 0
        
        precision = compteur/len(pred[:self.k])
        rappel = compteur/len(labels)
        
        return (1 + self.beta**2) * (precision * rappel)/\
               (self.beta**2 * precision + rappel)
