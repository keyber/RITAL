import evalMesure

class ReciprocalRank(evalMesure.EvalMesure):
    def evalQuery(self, pred, labels):
        if len(labels)==0:
            return 0
        
        best_id = pred[0]
        if best_id not in labels:
            return 0
        
        return 1 / labels.index(best_id)
