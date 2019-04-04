import indexerSimple
import myParser


def testVeryShort():
    docs = ["the new home has been saled on top forecasts",
            "the home sales rise in july",
            "there is an increase in home sales in july",
            "july encounter a new home sales rise"]
    parsed = myParser.loadCollection(docs)
    indexer = indexerSimple.IndexerSimple(parsed.docs)
    
    for d in indexer.ind, indexer.inv, indexer.ind_n, indexer.inv_n:
        for e in d.items():
            print(e)
        print("\n")


def testShort():
    parsed = None
    parsed2 = None
    file = "data/cacmShort.txt"
    for path in ["./", "../"]:
        try:
            parsed = myParser.buildDocCollectionSimple(path+file)
            parsed2 = myParser.buildDocumentCollectionRegex(path+file)
            break
        except FileNotFoundError:
            pass
    assert parsed and parsed2
    
    # équivalence des deux méthodes de parsing
    for d1, d2 in zip(sorted(parsed.docs.values(), key=lambda x: x.I), sorted(parsed2.docs.values(), key=lambda x: x.I)):
        assert d1.I == d2.I
        assert d1.T == d2.T

    indexer = indexerSimple.IndexerSimple(parsed2.docs)

    assert 'algebra' in indexer.ind['1']
    assert len(indexer.ind['2']) == 6
    assert sum(indexer.ind['11'].values()) == 8

    assert 'algebra' in indexer.ind_n['1']
    assert abs(sum(indexer.ind_n['2'].values()) - 1) < 1e-4

    assert indexer.inv['matrix'] == {'3': 1}
    assert len(indexer.inv['comput']) == 5

    assert indexer.inv_n['matrix'] == {'3': .2}
    assert len(indexer.inv_n['comput']) == 5

    tf_idf = indexer.create_tf_idf()

    #tfidf à la même structure que ind
    assert tf_idf.keys() == indexer.ind.keys()
    for i_doc in tf_idf.keys():
        assert tf_idf[i_doc].keys() == indexer.ind[i_doc].keys()

    #contenu de tfidf
    assert abs(tf_idf['4']['programm'] - 0.875) < 1e-3


def testLong():
    parsed = None
    file = "data/cisi/cisi.txt"
    for path in ["./", "../"]:
        try:
            parsed = myParser.buildDocCollectionSimple(path + file, '.W')
            break
        except FileNotFoundError:
            pass
    assert parsed
    
    indexer = indexerSimple.IndexerSimple(parsed.docs)
    assert len(indexer.ind) == 2459
    
    tf_idf = indexer.create_tf_idf()
    assert len(tf_idf) == 2459
    

#testVeryShort()
testShort()
testLong()
