import iRModel
import indexerSimple
import numpy as np


class Vectoriel(iRModel.IRModel):
    def __init__(self, indexer, weighter, normalized):
        super().__init__(indexer)
        self.weighter = weighter
        self.normalized = normalized
    
    def getScores(self, query):
        if not self.normalized:
            ind_inv = self.indexer.inv
            req = self.weighter.getWeightsForQuery(query)
            cle_index_inv = ind_inv.keys()
            result = {}
            for mot in req:
                if mot in cle_index_inv:
                    for cle in ind_inv[mot].keys():
                        #result[cle] = result.get(cle,0) + ind_inv[mot][cle]*req[mot]
                        result[cle] = result.get(cle, 0) + self.weighter.getWeightsForStem(mot)[cle] * req[mot]
            return result
        else:
            req = indexerSimple.counter(query)
            cle_index_inv = self.indexer.ind_inv.keys()
            result = {}
            normeR = np.sqrt(np.sum(np.power(list(req.values()), 2)))
            for mot in req:
                if mot in cle_index_inv:
                    for cle in self.indexer.ind_inv[mot].keys():
                        normeDoc = np.sqrt(np.sum(np.power(list(self.indexer.ind[cle].values()), 2)))
                        #result[cle] = result.get(cle,0) + (ind_inv[mot][cle]*req[mot])/(normeR+normeDoc)
                        result[cle] = result.get(cle, 0) + (self.weighter.getWeightsForStem(mot)[cle] * req[mot]) / (
                                normeR + normeDoc)
            return result
