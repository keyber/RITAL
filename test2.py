import weighter
import vectoriel
import tme2
import indexerSimple, parser
import okapiBM25


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
    v = vectoriel.Vectoriel(indexer, w, False)
    print(v.getScores("home"))

def vraiFichier():
        parsed = parser.buildDocCollectionSimple("data/cacmShort.txt")
        indexer = indexerSimple.IndexerSimple(parsed.docs)
        tf_idf = indexer.create_tf_idf()
        m = okapiBM25.OkapiBM25(indexer)
        #w = weighter.c1(indexer)
        #m = vectoriel.Vectoriel(indexer, w, True)
        dict = m.getScores("Algebraic")
        print(dict)
        for d in indexer.docs:
            for k in range(len(dict)):
                if(d.I == list(dict.keys())[k]):
                    print(d.T)


#test1()
#test2()
vraiFichier()
