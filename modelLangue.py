import indexerSimple
import iRModel
import numpy as np

class ModelLangue(iRModel):
    """jelinek-Mercer
    Md modèle langue document: tf_t_d / Sum(tf_k_d)
    MC modèle Collection  : tf_t_c / Sum(tf_k_c)
    """
    
    def getScores(self, query, requeteLongue=False):
        #suppose indépendances
        req = indexerSimple.counter(query)
        lamb = .2 if requeteLongue else .8
        p_q_m = []
        p_q_m = []
        for d in []:
            p_q_m[d] = 1
            for t,tf in req.items():
                p_q_m[d] *= self.indexer.ind[d][t] ** tf
        
        p_q_mc = 1
        for t,tf in req.items():
            p_q_mc *= self.indexer.ind[d][t] ** tf
        
        return lamb*p(t,mc) + (1-lamb) * p(t,md)
    pass

class Okapi:
    pass
    #cf 21/42
#valeurs par défaut cf cours

#lambda k1 b par cross validation
#




    