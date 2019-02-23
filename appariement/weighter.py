from abc import ABC, abstractmethod
import numpy as np
import sys
sys.path.append('./indexation/')
import indexerSimple


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
        return self.indexer.inv.get(stem,{})

    @abstractmethod
    def getWeightsForQuery(self, query):
        pass


class c1(TF):
    def getWeightsForQuery(self, query):
        query = indexerSimple.counter(query)
        return {i: 1.0 for i in query.keys()}


class c2(TF):
    def getWeightsForQuery(self, query):
        query = indexerSimple.counter(query)
        return {t: float(tf) for (t,tf) in query.items()}


class c3(TF):
    def getWeightsForQuery(self, query):
        query = indexerSimple.counter(query)
        result = {}
        for mot in query.keys():
            if mot in self.indexer.inv.keys():
                result[mot] = self.indexer.idf(mot)
        return result


class c4(Weighter):
    def getWeightsForDoc(self, iDoc):
        return {t: 1 + np.log(tf) for (t, tf) in self.indexer.ind[iDoc].items()}

    def getWeightsForStem(self, stem):
        return {doc: 1 + np.log(tf) for (doc, tf) in self.indexer.inv[stem].items()}

    def getWeightsForQuery(self, query):
        query = indexerSimple.counter(query)
        result = {}
        for mot in query.keys():
            if mot in self.indexer.inv.keys():
                result[mot] = self.indexer.idf(mot)
        return result


class c5(Weighter):
    def getWeightsForDoc(self, iDoc):
        idf = {mot: self.indexer.idf(mot) for mot in self.indexer.ind[iDoc].keys()}
        return {t: 1 + np.log(tf) * idf[t] for (t, tf) in self.indexer.ind[iDoc].items()}

    def getWeightsForStem(self, stem):
        if stem not in self.indexer.inv:
            print("warning: stem " + stem + " not in docs")
            return {}
        idf = self.indexer.idf(stem)
        return {doc: 1 + np.log(tf) * idf for (doc, tf) in self.indexer.inv[stem].items()}

    def getWeightsForQuery(self, query):
        query = indexerSimple.counter(query)
        idf = {mot: self.indexer.idf(mot) for mot in query.keys()}
        return {t: 1 + np.log(tf) * idf[t] for (t, tf) in query.items()}
