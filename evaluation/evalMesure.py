from abc import ABC, abstractmethod
import numpy as np

class EvalMesure(ABC):
    @abstractmethod
    def evalQuery(self, pred, labels):
        pass
    
    def eval_list_query(self, list_pred, list_labels):
        """return """
        res = [self.evalQuery(pred, labels) for pred, labels in zip(list_pred, list_labels)]
        return np.mean(res), np.std(res)
    