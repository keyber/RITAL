import porter
import collections
import numpy as np


#stopwords
mots_vides = {'the', 'a', 'an', 'on', 'behind', 'under', 'there', 'in', 'on'}


def counter(phrase):
    l = (porter.stem(w.lower()) for w in phrase.split(" "))
    l = (w for w in l if w not in mots_vides)
    return dict(collections.Counter(l).items())


class IndexerSimple:
    def __init__(self, docs):
        self.docs = docs
    
    
    def create_indexes(self):
        """ return (ind, ind_inv) (ind_norma, ind_inv_norma)
        ind : {iDoc: {w: occ}}
        inv : {w: {iDoc: occ}}
        """
        
        all_words = set()
        ind = {}
        ind_n = {}
        for d in self.docs:
            count = counter(d.T)
            
            all_words = all_words.union(set(count.keys()))
            
            ind[d.I] = count
            
            f = 1 / sum(count.values())
            ind_n[d.I] = {key:val*f for (key,val) in count.items()}
        
        inv = {w: {d.I: ind[d.I][w] for d in self.docs if w in ind[d.I]} for w in all_words}
        inv_n = {w: {d.I: ind_n[d.I][w] for d in self.docs if w in ind_n[d.I]} for w in all_words}

        return (ind, inv), (ind_n, inv_n)
    
    
    def getTfsForDoc(self):
        pass
    
    def getTfIdfsForDoc(self):
        pass
    
    def getTfsForStem(self):
        pass
    
    def getTfIDFsForStem(self):
        pass


    def create_tf_idf(self):
        """{iDoc: {w: tf-idf}}"""
        N = len(self.docs)
        (index, index_inverse), _ = self.create_indexes()
    
        def tf(i, w):
            return index[i][w]
    
        def df(w):
            return len(index_inverse[w])
    
        def idf(w):
            return np.log((1 + N) / (1 + df(w)))
    
        def tf_idf(i, w):
            return tf(i, w) * idf(w)
    
        return {d.I: {w: tf_idf(d.I, w) for w in index[d.I].keys()} for d in self.docs}
    
