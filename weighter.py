from abc import ABC, abstractmethod
import numpy as np
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
        return self.indexer.inv[stem]

    @abstractmethod
    def getWeightsForQuery(self, query):
        pass


class c1(TF):
    def getWeightsForQuery(self, query):
        req =  indexerSimple.counter(query)
        return {i:1 for i in req.keys()}

class c2(TF):
    def getWeightsForQuery(self, query):
        req =  indexerSimple.counter(query)
        return req

class c3(TF):
    def getWeightsForQuery(self, query):
        req =  indexerSimple.counter(query)
        cle_index_inv = self.indexer.inv.keys()
        N=len(self.indexer.ind)
        result={}
        for mot in req.keys():
            if(mot in cle_index_inv):
                df=len(self.indexer.inv[mot])
                result[mot]=np.log( (1+N) / (1+df) )
        return result


class c4(Weighter):
    def getWeightsForDoc(self, iDoc):
        return {t: 1 + np.log(tf) for (t,tf) in self.indexer.ind[iDoc].items()}

    def getWeightsForStem(self, stem):
        return {doc: 1 + np.log(tf) for (doc,tf) in self.indexer.inv[stem].items()}

    def getWeightsForQuery(self, query):
        req =  indexerSimple.counter(query)
        cle_index_inv = self.indexer.inv.keys()
        N=len(self.indexer.ind)
        result={}
        for mot in req.keys():
            if(mot in cle_index_inv):
                df=len(self.indexer.inv[mot])
                result[mot]=np.log( (1+N) / (1+df) )
        return result

class c5(Weighter):
    def getWeightsForDoc(self, iDoc):
        idf={}
        N=len(self.indexer.ind)
        for mot in self.indexer.ind[iDoc].keys():
            df=len(self.indexer.inv[mot])
            idf[mot]=np.log( (1+N) / (1+df) )
        return {t: 1 + np.log(tf)*idf[t] for (t,tf) in self.indexer.ind[iDoc].items()}

    def getWeightsForStem(self, stem):
        N=len(self.indexer.ind)
        df=len(self.indexer.inv[stem])
        idf=np.log( (1+N) / (1+df) )
        return {doc: 1 + np.log(tf)*idf for (doc,tf) in self.indexer.inv[stem].items()}

    def getWeightsForQuery(self, query):
        req =  indexerSimple.counter(query)
        idf={}
        N=len(self.indexer.ind)
        for mot in req.keys():
            df=len(self.indexer.inv[mot])
            idf[mot]=np.log( (1+N) / (1+df) )
        #return {t: 1 + np.log(tf)*idf[t] for (t,tf) in self.indexer.ind[iDoc].items()}
        return {t: 1 + np.log(tf)*idf[t] for (t,tf) in req.items()}
