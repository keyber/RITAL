from indexation import indexerSimple


def score(req, ind_inv):
    req = indexerSimple.counter(req)
    cle_index_inv = ind_inv.keys()
    doc = []
    for mot in req:
        if mot in cle_index_inv:
            doc.append(list(ind_inv[mot].keys()))
    
    inter = doc[0]
    for k in range(1, len(doc)):
        inter = list(set(inter) & set(doc[k]))
    dict_inter = {i: 1 for i in inter}
    return dict_inter


def score_vectoriel(req, ind_inv):
    req = indexerSimple.counter(req)
    cle_index_inv = ind_inv.keys()
    result = {}
    for mot in req:
        if mot in cle_index_inv:
            for cle in ind_inv[mot].keys():
                result[cle] = result.get(cle, 0) + ind_inv[mot][cle] * req[mot]
    return result
