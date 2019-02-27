import evalMesure
class FMesureK(evalMesure.EvalMesure):
    def __init__(k):
        self.k=k
        pass
    def evalQuery(self,pred,querry):
        label = querry.pertient_list_id
        compteur = 0
        for p in pred:
            if(p in label):
                compteur+=1
        precision = compteur/len(pred)
        rappel = compteur/len(label)
        return (1+self.k**2)* ( (precision*rappel)/( (self.k**2 * precision) + rappel ) )
