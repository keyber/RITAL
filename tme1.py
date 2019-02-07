import numpy as np
import collections
import porter

docs = ["the new home has been saled on top forecasts",
        "the home sales rise in july","there is an increase in home sales in july",
        "july encounter a new home sales rise"]
mots_vides = {'the', 'a', 'an', 'on', 'behind', 'under', 'there', 'in', 'on'}

def counter(phrase):
    l = (porter.stem(w.lower()) for w in phrase.split(" ") if w not in mots_vides)
    return dict(collections.Counter(l).items())


def create_ind_indInv(list_docs):
    """
    {iDoc: {w: occ}}
    {w: {iDoc: occ}}
    """
    index = {i: counter(d) for (i,d) in enumerate(list_docs)}
    
    all_words = set().union(*(set(counter(d).keys()) for d in list_docs))
    
    indinv = {w: {i:index[i][w] for i in range(len(list_docs)) if w in index[i]} for w in all_words}
    
    return index, indinv


def create_tf_idf(list_docs):
    """{iDoc: {w: tf-idf}}"""
    N = len(list_docs)
    index, index_inverse = create_ind_indInv(list_docs)
    
    def tf(i, w):
        return index[i][w]
    
    def df(w):
        return len(index_inverse[w])
    
    def idf(w):
        return np.log((1 + N) / (1 + df(w)))
    
    def tf_idf(i, w):
        return tf(i, w) * idf(w)
    
    return {i: {w: tf_idf(i, w) for w in index[i].keys()} for i in range(len(list_docs))}

print(create_tf_idf(docs))
