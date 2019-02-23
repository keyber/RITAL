import sys

sys.path.append('./indexation/')
import queryParser
import myParser
import indexerSimple


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

    
    indexer = indexerSimple.IndexerSimple(parsedText.docs)
    
    #TODO comparer le ranking de nos modèles au vrais documents pertients

testLong()
