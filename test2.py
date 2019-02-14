import indexerSimple
import parser
import tme2


def test1():
    docs = ["the new home has been saled on top forecasts",
            "the home sales rise in july",
            "there is an increase in home sales in july",
            "july encounter a new home sales rise"]
    
    parsed = parser.loadCollection(docs)

    indexer = indexerSimple.IndexerSimple(parsed.docs)

    #contenu des indexes
    (ind, inv), (ind_n, inv_n) = indexer.create_indexes()
    
    print(tme2.score(ind, inv, "home sales top"))
    
test1()
