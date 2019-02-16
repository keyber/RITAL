import indexerSimple
import iRModel

class ModelLangue(iRModel):
    """jelinek-Mercer"""
    
    def getScores(self, query, requeteLongue=False):
        #suppose indépendances
        req = indexerSimple.counter(query)
        lamb = .2 if requeteLongue else .8
        
        len_coll = sum(len(d.T) for d in self.indexer.docs)
        
        #facteurs de lissage de chaque terme de la requete (définis par la collection)
        p_q_mc = {}
        for t, tf_q in req.items():
            p_q_mc[t] = sum(self.indexer.ind[d.I][t] for d in self.indexer.docs) / len_coll
        
        #scores de chaque doc
        scores = {}
        for d in self.indexer.docs:
            score = 1
            for t in req.keys():
                score *= (1-lamb) * self.indexer.ind_n[d][t]  +  lamb * p_q_mc[t]
            scores[d] = score
            
        return scores

class Okapi(iRModel):
    def getScores(self, query):
        scores = {}
        for d in self.indexer.docs:
            score = idf()*x
            scores[d] = score
        return scores
        
#cf 21/42
#valeurs par défaut cf cours

#lambda k1 b par cross validation
