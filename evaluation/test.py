import sys

sys.path.append('./indexation/')
sys.path.append('./appariement/')
import queryParser
import myParser
import weighter
import vectoriel
import okapiBM25
import jelinekMercer
import indexerSimple
import numpy as np

def testLong():
    parsedQuery = None
    parsedText = None
    file = "data/cisi/cisi"
    for path in ["./", "../"]:
        try:
            #.qry add after
            parsedQuery = queryParser.parse(path + file)
            parsedText = myParser.buildDocCollectionSimple(path + file + ".txt", ".W")
            break
        except FileNotFoundError:
            pass

    assert parsedQuery
    assert parsedText


    assert len(parsedQuery.queries) == 112
    assert len(parsedQuery.queries["1"].pertient_list_id) == 46

    #nombre de requêtes ayant au moins un document pertinent
    assert sum(len(q.pertient_list_id) > 0 for q in parsedQuery.queries.values()) == 76


    indexer = indexerSimple.IndexerSimple(parsedText.docs)

    #TODO comparer le ranking de nos modèles au vrais documents pertients
    """
    m = vectoriel.Vectoriel(indexer, weighter.c1(indexer), False)
    evalOnCesi(m,parsedQuery)
    """

    models = [weighter.c1, weighter.c2, weighter.c3, weighter.c4, weighter.c5]
    models = [clas(indexer) for clas in models]
    models = [vectoriel.Vectoriel(indexer, weight, False) for weight in models]
    models.append(jelinekMercer.JelinekMercer(indexer, .2))
    models.append(okapiBM25.OkapiBM25(indexer, 1.2, .75))

    for m in models:
        print("Precision moyenne sur toute les requetes : "+str(evalOnCesi(m,parsedQuery)))

    #NDCG a faire  


def evalOnCesi(model,parsedQuery):
    rankings=[]
    for cle in parsedQuery.queries.keys():
        rankings.append(model.getRanking(parsedQuery.queries[cle].T))

    #get ranking without score
    rankNoScore = []
    for lr in rankings:
        tmp=[]
        for r in lr:
            tmp.append(r[0])
        rankNoScore.append(tmp)

    #get the label from the dataset
    dico_lab={}
    file = open("data/cisi/cisi.rel","r")
    lines = file.readlines()
    for l in lines:
        l=l.replace("     "," ")
        l=l.replace("    "," ")
        l=l.replace("   "," ")
        l=l.replace("  "," ")
        l=l.replace(" "," ")
        info = l.split(" ")
        idRequete = info[1]
        idDoc = info[2].split("\t")[0]
        if(idRequete not in dico_lab):
            dico_lab[idRequete]=[idDoc]
        else:
            dico_lab[idRequete].append(idDoc)
    #Calcul de la précision moyenne sur toute les requetes
    compteur=0
    somme=0
    for cleLab in dico_lab.keys():
        somme+=avgPrec(rankNoScore[compteur],dico_lab[cleLab])
        compteur+=1
    return somme/compteur

def avgPrec(pred, lab):
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

#label = [numero requette, numero document , pertinence(entre 0 et 5)]
def DCG(label,rang):
    somme=label[0][2]
    for k in range(2,rang):
        somme+=label[k-1][2]/np.log2(k-1)
    return somme

def NDCG(labelModel,labelIdeale,rang):
    return DCG(labelModel,rang)/DCG(labelIdeale,rang)

testLong()
