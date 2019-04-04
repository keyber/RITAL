import sys
sys.path.append('./indexation/')
import weighter
import vectoriel
import indexerSimple
import myParser
import okapiBM25
import jelinekMercer
import pagerank
import random
import time


def test_ranking_veryshort():
    docs = ["the new home has home been saled on top forecasts",
            "the home sales rise in july",
            "there is an increase in sales in july",
            "july encounter a new home sales rise"]
    parsed = myParser.loadCollection(docs)
    indexer = indexerSimple.IndexerSimple(parsed.docs)
    weights_doc = []
    scores = []
    for clas in [weighter.c1, weighter.c2, weighter.c3, weighter.c4, weighter.c5]:
        w = clas(indexer)
        weights_doc.append(w.getWeightsForDoc(0))
        v = vectoriel.Vectoriel(indexer, w, False)
        scores.append(v.getScores("home sales top"))

    #documents dans le même ordre qqsoit weighter
    list0 = sorted(scores[0].keys(), key=lambda x: scores[0][x])
    for s in scores[1:]:
        assert list0 == sorted(s.keys(), key=lambda x:s[x])


def test_ranking_short():
    parsed = None
    file = "data/cacmShort.txt"
    for path in ["./", "../"]:
        try:
            parsed = myParser.buildDocCollectionSimple(path + file, ".T")
            break
        except FileNotFoundError:
            pass
    assert parsed

    indexer = indexerSimple.IndexerSimple(parsed.docs)
    requete = "home computer microphotographi"

    models = [weighter.c1, weighter.c2, weighter.c3, weighter.c4, weighter.c5]
    models = [clas(indexer) for clas in models]
    models = [vectoriel.Vectoriel(indexer, weight, False) for weight in models]
    models.append(jelinekMercer.JelinekMercer(indexer, 1))
    models.append(okapiBM25.OkapiBM25(indexer, 1.2, .75))

    rankings = [m.getRanking(requete) for m in models]

    # 5 docs ont un score non nul qqsoit modèle
    for ranking in rankings:
        assert len(ranking) == 5

    # ordre des résultats
    for ranking in rankings[:-1]:
        assert [x[0] for x in ranking] == ["7", "6", "4", "2", "10"]
    assert [x[0] for x in rankings[-1]] == ["6", "7", "4", "10", "2"]


def test_ranking_long():
    parsed = None
    file = "data/cacm/cacm.txt"
    for path in ["./", "../"]:
        try:
            parsed = myParser.buildDocCollectionSimple(path + file, ".T")
            break
        except FileNotFoundError:
            pass
    assert parsed

    indexer = indexerSimple.IndexerSimple(parsed.docs)
    requete = "home computer microphotographi"

    models = [weighter.c1, weighter.c2, weighter.c3, weighter.c4, weighter.c5]
    models = [clas(indexer) for clas in models]
    models = [vectoriel.Vectoriel(indexer, weight, False) for weight in models]
    models.append(jelinekMercer.JelinekMercer(indexer, .2))
    models.append(okapiBM25.OkapiBM25(indexer, 1.2, .75))

    rankings = [m.getRanking(requete) for m in models]

    #modèle O rang 0 à un score de 2
    assert rankings[0][0][1] == 2
    #modèle O rang 9 à un score de 1
    assert rankings[0][9][1] == 1
    #modèle 1
    assert rankings[1][0][1] == 2
    assert rankings[1][9][1] == 1

    #meilleur docs
    assert rankings[0][0][0] == "80"
    assert rankings[1][0][0] == "80"
    assert rankings[2][0][0] == "3646"
    assert rankings[3][0][0] == "3646"
    assert rankings[4][0][0] == "80"
    assert rankings[5][0][0] == "866"
    assert rankings[6][0][0] == "3156"


def test_full_pagerank(indexer):
    print("full pagerank")
    print("taille", len(indexer.points_to.keys()))
    t = time.time()
    res = pagerank.calculPr(indexer.points_to.keys(), indexer.points_to, max_iter=10)
    print("res", res, '\n')
    print("time", time.time()-t)


def test_alea_pagerank(indexer):
    print("random walk page rank")
    t = time.time()
    
    requete = "home computer microphotographi"
    
    model = vectoriel.Vectoriel(indexer, weighter.c1(indexer), normalized=False)
    
    n = 100
    k = 10
    
    rankings = model.getRanking(requete)[:n]
    graphe = set([doc[0] for doc in rankings])
    # print(len(indexer.docs))
    # print(rankings)
    # cela détermine un graphe initial de documents
    
    # on étend ce graphe en rajoutant des documents pointés par et pointant vers le graphe actuel
    for d, _ in rankings:
        # on ajoute tous les docs pointés par d
        graphe |= set(indexer.pointed_by[d])
        
        # on ajoute k docs (au plus) pointant d
        points_to = indexer.points_to[d]
        graphe |= set(random.sample(points_to, min(k, len(points_to))))
    
    res = pagerank.calculPr(graphe, indexer.points_to, max_iter=1)
    
    
    print("res", res)
    print("time", time.time()-t)
    
    
def main():
    # test_ranking_veryshort()
    # test_ranking_short()
    # test_ranking_long()
    
    parsed = None
    # exécution d'un modèle simple
    file = "data/cacm/cacm.txt"
    for path in ["./", "../"]:
        try:
            parsed = myParser.buildDocCollectionSimple(path + file, ".T", balise2=".X")
            break
        except FileNotFoundError:
            pass
    assert parsed
    
    indexer = indexerSimple.IndexerSimple(parsed.docs)
    
    # test_full_pagerank(indexer)
    test_alea_pagerank(indexer)

if __name__ == '__main__':
    main()