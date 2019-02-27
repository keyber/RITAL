import evalMesure
class Precision(evalMesure.EvalMesure):
    def __init__():
        pass
    def evalQuery(self,pred,querry):
        label = querry.pertient_list_id
        compteur = 0
        for p in pred:
            if(p in label):
                compteur+=1
        return compteur/len(pred)
