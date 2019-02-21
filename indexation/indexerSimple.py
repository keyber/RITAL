import porter
import textRepresenter
import collections
import numpy as np


def counter(phrase):
    porter_stemer = textRepresenter.PorterStemmer()
    #ou textRepresenter.getTextRepresentation
    l = (porter.stem(w.lower()) for w in phrase.split(" "))
    l = (w for w in l if w not in porter_stemer.stopWords)
    return dict(collections.Counter(l).items())


class IndexerSimple:
    def __init__(self, docs):
        self.docs = docs
        self.N = len(docs)
        self.ind = None
        self.inv = None
        self.ind_n = None
        self.inv_n = None
        self._create_indexes()

    def _create_indexes(self):
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
            ind_n[d.I] = {key: val * f for (key, val) in count.items()}

        inv = {w: {d.I: ind[d.I][w] for d in self.docs if w in ind[d.I]} for w in all_words}
        inv_n = {w: {d.I: ind_n[d.I][w] for d in self.docs if w in ind_n[d.I]} for w in all_words}

        self.ind = ind
        self.inv = inv
        self.ind_n = ind_n
        self.inv_n = inv_n

    def tf(self, i, w):
        return self.ind[i][w]

    def df(self, w):
        return len(self.inv[w])

    def idf(self, w):
        return np.log((1 + self.N) / (1 + self.df(w)))

    def tf_idf(self, i, w):
        return self.tf(i, w) * self.idf(w)

    def create_tf_idf(self):
        """{iDoc: {w: tf-idf}}"""
        return {d.I: {w: self.tf_idf(d.I, w) for w in self.ind[d.I].keys()} for d in self.docs}

    def getTfsForDoc(self, ind, doc):
        print("à vérifier")
        return ind[doc]

    def getTfIDFsForDoc(self, ind, inv, doc):
        #pas de "inv" en paramètre normalement ?
        print("à vérifier")
        return {np.log((1 + len(ind)) / (1 + len(inv[w]))) for w in ind[doc].keys()}

    def getTfsForStem(self, inv, stem):
        print("à vérifier")
        return inv[stem]

    def getTfIDFsForStem(self, inv, stem):
        print("à vérifier")
        idf = len(inv[stem])
        return {d: tf * idf for (d, tf) in inv[stem].items()}

    def getStrDoc(self, doc):
        print("à vérifier")
        return doc.T
