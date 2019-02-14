import indexerSimple
import parser
import tme2


def test1():
    docs = ["the new home has home been saled on top forecasts",
            "the home sales rise in july",
            "there is an increase in sales in july",
            "july encounter a new home sales rise"]

    parsed = parser.loadCollection(docs)

    indexer = indexerSimple.IndexerSimple(parsed.docs)

    #print(tme2.score("home sales top",indexer.inv))
    print(tme2.score_vectoriel("home sales top",indexer.inv))
test1()
