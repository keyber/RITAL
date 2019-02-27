import evalMesure
class NdegMin(evalMesure.EvalMesure):
    def __init__():
        pass
    def evalQuery(self,pred,querry):
        pass
    def DCG(label,rang):
        somme=label[0][2]
        for k in range(2,rang):
            somme+=label[k-1][2]/np.log2(k-1)
        return somme

    def NDCG(labelModel,labelIdeale,rang):
        return DCG(labelModel,rang)/DCG(labelIdeale,rang)
