from appariement import iRModel


class Vectoriel(iRModel.IRModel):
    def __init__(self,w,n):
        self.weighter = w
        self.normalized = n
    def getScores(self,query):
        if(self.normalized == False):
            ind_inv = self.weighter.indexer.inv
            req = self.weighter.getWeightsForQuery(query)
            cle_index_inv = ind_inv.keys()
            result={}
            for mot in req:
                if(mot in cle_index_inv):
                    for cle in ind_inv[mot].keys():
                        #result[cle] = result.get(cle,0) + ind_inv[mot][cle]*req[mot]
                        result[cle] = result.get(cle,0) + getWeightsForStem(mot)[cle]*req[mot]
            return result
        else:
            req = indexerSimple.counter(req)
            cle_index_inv = ind_inv.keys()
            result={}
            normeR = np.sqrt(np.sum(np.power(list(req.values()))))
            for mot in req:
                if(mot in cle_index_inv):
                    for cle in ind_inv[mot].keys():
                        normeDoc = np.sqrt(np.sum(np.power(list(ind[cle].values()))))
                        #result[cle] = result.get(cle,0) + (ind_inv[mot][cle]*req[mot])/(normeR+normeDoc)
                        result[cle] = result.get(cle,0) + (getWeightsForStem(mot)[cle]*req[mot])/(normeR+normeDoc)
            return result
