import evalMesure
class FMesureK(evalMesure.EvalMesure):
    def __init__(self, k):
        self.k = k
    
    def evalQuery(self, pred, labels):
        compteur = 0
        for p in pred:
            if p in labels:
                compteur+=1
        
        if len(pred)==0 or len(labels)==0:
            return 0
        precision = compteur/len(pred)
        rappel = compteur/len(labels)
        
        if precision==0 and rappel==0:
            return 0
        return (1+self.k**2)* ( (precision*rappel)/( (self.k**2 * precision) + rappel ) )
