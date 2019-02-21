from indexation import indexerSimple, parser
from appariement import tme2, weighter, vectoriel


def test1():
    docs = ["the new home has home been saled on top forecasts",
            "the home sales rise in july",
            "there is an increase in sales in july",
            "july encounter a new home sales rise"]

    parsed = parser.loadCollection(docs)

    indexer = indexerSimple.IndexerSimple(parsed.docs)

    #print(tme2.score("home sales top",indexer.inv))
    print(tme2.score_vectoriel("home sales top", indexer.inv))


def test2():
    docs = ["the new home has home been saled on top forecasts",
            "the home sales rise in july",
            "there is an increase in sales in july",
            "july encounter a new home sales rise"]
    parsed = parser.loadCollection(docs)
    indexer = indexerSimple.IndexerSimple(parsed.docs)
    w = weighter.c5(indexer)
    print(w.getWeightsForDoc(0))
    v = vectoriel.Vectoriel(w, False)
    print(v.getScores("home"))
    

test1()
test2()
