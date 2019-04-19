import string
import sys
sys.path.append('./indexation/')
import myParser
import indexerSimple
table = str.maketrans({key: None for key in string.punctuation})

class Query:
    def __init__(self, identifiant, texte, pertinences):
        self.I = identifiant
        self.T = texte
        self.pertient_list_id = pertinences


class QueryParser:
    def __init__(self, queries, pertinences):
        self.queries = {}
        for query in queries.docs.values():
            #stemme la requête, enlève la ponctuation
            
            query.T = query.T.translate(table)
            query.T = " ".join(w for w in indexerSimple.counter(query.T).keys())
            
            assert query.T != ""
            self.queries[query.I] = Query(query.I, query.T, pertinences.get(query.I, []))

        
def parse(path):
    queries = myParser.buildDocCollectionSimple(path+".qry", ".W")
    pertinences = loadPertinences(path+".rel")
    return QueryParser(queries, pertinences)


def loadPertinences(path):
    res = {}
    with open(path) as f:
        for line in f:
            iQuery, iDoc = line.split()[:2]
            if not iQuery in res:
                res[iQuery] = []
            res[iQuery].append(iDoc)
    return res

