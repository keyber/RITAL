import sys
sys.path.append('./indexation/')
import weighter
import vectoriel
import indexerSimple
import myParser
import okapiBM25
import jelinekMercer


def testVeryShort():
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

def vraiFichier():
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
    models.append(okapiBM25.OkapiBM25(indexer, 1.2, .75))
    models.append(jelinekMercer.JelinekMercer(indexer, 1))
    
    rankings=[]
    for m in models:
        rankings.append(m.getRanking(requete))

    # 5 docs ont un score non nul qqsoit modèle
    for ranking in rankings:
        assert len(ranking)==5
    
    # ordre des résultats
    for ranking in rankings[:5] + rankings[6:6]:
        assert [x[0] for x in ranking] == ["7","6","4","2","10"]
    assert [x[0] for x in rankings[5]] == ["6","7","4","10","2"]
    
testVeryShort()
vraiFichier()
