import indexerSimple
import parser

def test1():
    docs = ["the new home has been saled on top forecasts",
            "the home sales rise in july",
            "there is an increase in home sales in july",
            "july encounter a new home sales rise"]


    parsed = parser.loadCollection(docs)

    indexer = indexerSimple.IndexerSimple(parsed.docs)

    (a,b),(c,d) = indexer.create_indexes()
    for d in a,c,b,d:
        for e in d.items():
            print(e)
        print("\n")


def test2():
    parsed = parser.buildDocCollectionSimple("data/cacmShort.txt")
    parsed2 = parser.buildDocumentCollectionRegex("data/cacmShort.txt")

    #parsed.afficher( )
    #parsed2.afficher()

    #équivalence des deux méthodes de parsing
    for d1, d2 in zip(sorted(parsed.docs, key=lambda x:x.I), sorted(parsed2.docs, key=lambda x:x.I)):
        assert d1.I == d2.I
        assert " ".join(d1.T) == d2.T


    indexer = indexerSimple.IndexerSimple(parsed2.docs)

    #contenu des indexes
    (ind, inv),(ind_n, inv_n) = indexer.create_indexes()

    assert 'algebra' in ind['1']
    assert len(ind['2']) == 6
    assert sum(ind['11'].values()) == 8

    assert 'algebra' in ind_n['1']
    assert abs(sum(ind_n['2'].values()) - 1) < 1e-4

    assert inv['matrix'] == {'3':1}
    assert len(inv['comput']) == 5
    
    assert inv_n['matrix'] == {'3':.2}
    assert len(inv_n['comput']) == 5
    
    tf_idf = indexer.create_tf_idf()

    #tfidf à la même structure que ind
    assert tf_idf.keys() == ind.keys()
    for i_doc in tf_idf.keys():
        assert tf_idf[i_doc].keys() == ind[i_doc].keys()

    #contenu de tfidf
    assert abs(tf_idf['4']['programm'] - 0.875) < 1e-3

#test1()
test2()
