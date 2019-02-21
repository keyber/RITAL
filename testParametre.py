import numpy as np
import modelLangue
import modelProbabiliste


def optimisationModeleLangue(debut, fin, nbPoint, donnees, labels):
    rangeLamba = np.linspace(debut, fin, nbPoint)
    m = modelLangue.ModelLangue()
    mapLambda = []
    for l in rangeLamba:
        s = 0
        for k in range(len(donnees)):
            predictionModele = m.getRanking(donnees[k], [l])
            s += avgPrec(predictionModele, labels[k])
        mapLambda.append(s/len(donnees))
    leMeilleurLambdaDuMonde = rangeLamba[np.argmax(mapLambda)]


def optimisationOkapi(debut1, fin1, nbPoint1, debut2, fin2, nbPoint2, donnees, labels):
    rangeK = np.linspace(debut1, fin1, nbPoint1)
    rangeB = np.linspace(debut2, fin2, nbPoint2)
    m = modelProbabiliste.Okapi()
    mapKB = []
    param = []
    for k1 in rangeK:
        for b in rangeB:
            s = 0
            for k in range(len(donnees)):
                predictionModele = m.getRanking(donnees[k], [k1, b])
                s += avgPrec(predictionModele, labels[k])
            mapKB.append(s/len(donnees))
            param.append([k1, b])
    leMeilleurKBDuMonde = param[np.argmax(mapKB)]


def avgPrec(pred, lab):
    point = []
    for k in range(len(lab)):
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

#label = [numero requette, numero document , pertinence(entre 0 et 5)]
def DCG(label,rang):
    somme=label[0][2]
    for k in range(2,rang):
        somme+=label[k-1][2]/np.log2(k-1)
    return somme

def NDCG(labelModel,labelIdeale,rang):
    return DCG(labelModel,rang)/DCG(labelIdeale,rang)
