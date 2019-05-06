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


def testLong():
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
    assert parsedQuery
    assert parsedText

    assert len(parsedQuery.queries) == 112
    assert len(parsedQuery.queries["1"].pertient_list_id) == 46

    #nombre de requêtes ayant au moins un document pertinent
    assert sum(len(q.pertient_list_id) > 0 for q in parsedQuery.queries.values()) == 76

    print("calcul indexer")
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
    jelinek.fit(np.linspace(0, 2, 2), data_fit, labels)
    okapi.fit((np.linspace(0, 2, 2), np.linspace(0, 2, 2)), data_fit, labels)

    for i in range(len(models)):
        models.append(pagerank.PagerankMarcheAlea(indexer, models[i]))

    print("précisions")
    for m in models:
        pred = [m.getRanking(data_fit[k]) for k in range(len(data_fit))]
        avgPrec = 0
        for k in range(len(pred)):
            avgPrec+=m.avgPrec(pred[k], labels[k])
        print(m,avgPrec/len(pred))

testLong()
