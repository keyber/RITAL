from abc import ABC, abstractmethod
import numpy as np

class Weighter(ABC):
    def __init__(self, indexer):
        self.indexer = indexer

    @abstractmethod
    def getWeightsForDoc(self, iDoc):
        """poids des termes pour le doc"""
        pass

    @abstractmethod
    def getWeightsForStem(self, stem):
        """poids du terme pour tous les docs"""
        pass

    @abstractmethod
    def getWeightsForQuery(self, query):
        """poids des termes de la requete"""
        pass


class TF(Weighter):
    def getWeightsForDoc(self, iDoc):
        return self.indexer.ind[iDoc]

    def getWeightsForStem(self, stem):
        return self.indexer.inv[stem]

    @abstractmethod
    def getWeightsForQuery(self, query):
        pass


class c1(TF):
    def getWeightsForQuery(self, query):
        req = self.indexer.counter(query)
        return {i:1 for i in req.keys()}

class c2(TF):
    def getWeightsForQuery(self, query):
        req = self.indexer.counter(query)
        return {i:req[i] for i in req.keys()}

class c3(TF):
    def getWeightsForQuery(self, query):
        N=
        df=
        return log( (1+N) / (1+df) )


class c4(Weighter):
    def getWeightsForDoc(self, iDoc):
        return {t: 1 + np.log(tf) if t in iDoc else 0 for (t,tf) in self.indexer.ind[iDoc].items()}

    def getWeightsForStem(self, stem):
        return {iDoc: 1 + np.log(tf) if t in iDoc else 0 for (iDoc,tf) in self.indexer.inv[stem].items()}

    def getWeightsForQuery(self, query):
        pass




w = Weighter(0, 0)
print(w)
