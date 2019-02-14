from abc import ABC, abstractmethod
import numpy as np

class Weighter(ABC):
    def __init__(self, ind, inv):
        self.ind = ind
        self.inv = inv

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
        return self.ind[iDoc]

    def getWeightsForStem(self, stem):
        return self.inv[stem]

    @abstractmethod
    def getWeightsForQuery(self, query):
        pass


class c1(TF):
    def getWeightsForQuery(self, query):
        req = indexerSimple.counter(query)
        return {i:1 for i in req.keys()}

class c2(TF):
    def getWeightsForQuery(self, query):
        req = indexerSimple.counter(query)
        return {i:req[i] for i in req.keys()}

class c3(TF):
    def getWeightsForQuery(self, query):
        N=
        df=
        return log( (1+N) / (1+df) )


class c4(Weighter):
    def getWeightsForDoc(self, iDoc):
        return {t: 1 + np.log(tf) if t in iDoc else 0 for (t,tf) in self.ind[iDoc].items()}

    def getWeightsForStem(self, stem):
        return {t: 1 + np.log(tf) if t in iDoc else 0 for (t,tf) in self.ind[iDoc].items()}

    def getWeightsForQuery(self, query):
        pass




w = Weighter(0, 0)
print(w)
