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
import pagerank
import numpy as np

import averagePrecision
import fMesureK
import NDCG
import precisionAtK
import rappelAtK
import reciprocalRank


def eval():
    parsedQuery = None
    parsedText = None
    file = "data/cisi/cisi"
    for path in ["./", "../"]:
        try:
            parsedQuery = queryParser.parse(path + file)
            parsedText = myParser.buildDocCollectionSimple(path + file + ".txt", ".W")
            break
        except FileNotFoundError:
            pass
    
    indexer = indexerSimple.IndexerSimple(parsedText.docs)

    models = [weighter.c1, weighter.c2, weighter.c3, weighter.c4, weighter.c5]
    models = [clas(indexer) for clas in models]
    models = [vectoriel.Vectoriel(indexer, weight, False) for weight in models]
    jelinek = jelinekMercer.JelinekMercer(indexer)
    models.append(jelinek)

    okapi = okapiBM25.OkapiBM25(indexer)
    models.append(okapi)

    data_fit = [q.T for q in parsedQuery.queries.values()]
    labels = [q.pertient_list_id for q in parsedQuery.queries.values()]
    
    print("fit")
    # jelinek.fit(np.linspace(0, 2, 2), data_fit, labels)
    # okapi.fit((np.linspace(0, 2, 2), np.linspace(0, 2, 2)), data_fit, labels)
    
    for i in range(len(models)):
        models.append(pagerank.PagerankMarcheAlea(indexer, models[i]))
    
    print(labels[:10])
    for x in labels[0]:
        print(type(x))
        break
    
    k = 9
    metrics = [
        averagePrecision.AveragePrecision(),
        fMesureK.FMesureK(k),
        NDCG.NDCG(k),
        precisionAtK.PrecisionAtK(k),
        rappelAtK.RappelAtK(k),
        reciprocalRank.ReciprocalRank()]
        
    print("précisions\n")
    for model in models:
        print("model : ", model)
        pred = [model.getRanking(data_fit[k]) for k in range(len(data_fit))]
        
        for metric in metrics:
            print("metric : ", metric)
            print(metric.eval_list_query(pred, labels))
    
eval()