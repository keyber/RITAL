import evalMesure
import numpy as np

class AveragePrecision(evalMesure.EvalMesure):
    def evalQuery(self, pred, labels):
        point = []
        for k in range(0, len(labels)):
            data = pred[:k + 1]
            theorique = labels[:k + 1]
            nbCorrect = 0
            for d in data:
                if d[0] in theorique:
                    nbCorrect += 1
            rappel = nbCorrect / len(labels)
            precision = nbCorrect / len(data)
            point.append([rappel, precision])
        pointRappel = np.linspace(0, 1, 11)
        pointFinal = []
        if len(point)!=0:
            for p in pointRappel:
                pointFinal.append(np.interp(p, [p[0] for p in point], [p[1] for p in point]))
            return np.mean(pointFinal)
        else: # une requete sans label compte comme faux
            return 0

