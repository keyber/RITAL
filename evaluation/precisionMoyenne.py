import evalMesure
class PrecisionMoyenne(evalMesure.EvalMesure):
    def __init__():
        pass
    def evalQuery(self,pred,querry):
        label = query.pertient_list_id
        point = []
        for k in range(1,len(lab)+1):
            data = pred[:k]
            theorique = lab[:k]
            nbCorrect = 0
            for d in data:
                if d in theorique:
                    nbCorrect += 1
            rappel = nbCorrect/len(lab)
            precision = nbCorrect/len(data)
            point.append([rappel, precision])
        pointRappel = np.linspace(0, 1, 11)
        pointFinal = []
        for p in pointRappel:
            pointFinal.append(np.interp(p, [p[0] for p in point], [p[1] for p in point]))
        return np.mean(pointFinal)
