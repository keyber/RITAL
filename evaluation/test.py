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
    # jelinek.fit(np.linspace(0, 2, 2), data_fit, labels)
    # okapi.fit((np.linspace(0, 2, 2), np.linspace(0, 2, 2)), data_fit, labels)
    
    # train test
    print(len(data_fit))
    n = 100
    jelinek.fit(np.linspace(.2, .7, 3), data_fit[:n], labels[:n])
    okapi.fit((np.linspace(0, 2, 2), np.linspace(0, 2, 2)), data_fit[:n], labels[:n])

    for i in range(len(models)):
        models.append(pagerank.PagerankMarcheAlea(indexer, models[i]))
    
    models[-2].fit(np.linspace(.2, .7, 3), data_fit[:n], labels[:n])

    print("précisions")
    for m in models:
        pred = [m.getRanking(d) for d in data_fit[n:]]
        avgPrec = 0
        for p, l in zip(pred, labels[n:]):
            avgPrec += m.avgPrec(p, l)
        print(m,avgPrec/len(pred))

testLong()
