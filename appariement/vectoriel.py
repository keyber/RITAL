import iRModel
import numpy as np


class Vectoriel(iRModel.IRModel):
    def __init__(self, indexer, weighter, normalized):
        super().__init__(indexer)
        self.weighter = weighter
        self.normalized = normalized
    
    def _getScores(self, query, pertinences=None):
        query = " ".join(query.keys())
        query = self.weighter.getWeightsForQuery(query)
        result = {}
        
        if not self.normalized:
            for mot in query:
                dicoTi = self.weighter.getWeightsForStem(mot)
                for key, value in dicoTi.items():
                    result[key] = result.get(key, 0) + value * query[mot]
        else:
            normeR = np.sqrt(np.sum(np.power(list(query.values()), 2)))
            for mot in query:
                dicoTi = self.weighter.getWeightsForStem(mot)
                for key, value in dicoTi.items():
                    normeDoc = np.sqrt(np.sum(np.power(list(self.weighter.getWeightsForDoc(key).values()), 2)))
                    result[key] = result.get(key, 0) + (value * query[mot]) / (normeR + normeDoc)
            """
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
            """
        return result
