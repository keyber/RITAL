import evalMesure

class PrecisionAtK(evalMesure.EvalMesure):
    def __init__(self, k):
        self.k = k
    
    def evalQuery(self, pred, labels):
        if len(labels)==0:
            return 0
        
        data = pred[:self.k + 1]
        theorique = labels[:self.k + 1]
        nbCorrect = 0
        for d in data:
            if d[0] in theorique:
                nbCorrect += 1
        return nbCorrect / len(data)
    
"""
    def evalQuery(self,pred,querry):
        label = querry.pertient_list_id
        compteur = 0
        for p in pred:
            if(p in label):
                compteur+=1
        return compteur/len(pred)
"""