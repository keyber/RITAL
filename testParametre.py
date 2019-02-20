import numpy as np
import modelLangue

def optimisationModeleLangue(debut,fin,nbPoint, donnees,labels):
    rangeLamba = np.linespace(debut,fin,nbPoint)
    m = modelLangue.ModelLangue()
    maxi = -999999
    mapLambda=[]
    for l in rangeLamba:
        s=0
        for k in range(len(donnees)):
            predictionModele = m.getRanking(query,[l])
            s+=avgPrec(predictionModele,labels[k])
        mapLambda.append(s/len(donnees))
    leMeilleurLambdaDuMonde = rangeLamba[np.argmax(mapLambda)]

def optimisationOkapi(debut1,fin1,nbPoint1,debut2,fin2,nbPoint2, donnees,labels):
    rangeK = np.linespace(debut1,fin1,nbPoint1)
    rangeB = np.linespace(debut2,fin2,nbPoint2)
    m = modelLangue.Okapi()
    maxi = -999999
    mapKB=[]
    param=[]
    for k in rangeK:
        for b in rangeB:
            s=0
            for k in range(len(donnees)):
                predictionModele = m.getRanking(query,[k,b])
                s+=avgPrec(predictionModele,labels[k])
            mapKB.append(s/len(donnees))
            param.append([k,b])
    leMeilleurKBDuMonde = param[np.argmax(mapLambda)]


def avgPrec(pred,lab):
    point = []
    for k in range(len(lab)):
        data = pred[:k]
        theorique = lab[:k]
        nbCorrect = 0
        for d in data :
            if(d in theorique):
                nbCorrect+=1
        rappel = nbCorrect/len(lab)
        precision = nbCorrect/len(data)
        point.append([rappel,precision])
    pointRappel = np.linespace(0,1,11)
    pointFinal=[]
    for p in pointRappel:
        pointFinal.append(np.interp(p,[p[0] for p in point],[p[1] for p in point]))
    return np.mean(pointFinal)
