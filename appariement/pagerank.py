
def _calculSomme(Pr):
    somme = 0
    for key in Pr.keys():
        somme += Pr[key]
    return somme


def _compte(j, liste):
    compteur = 0
    for el in liste:
        if el == j:
            compteur += 1
    return compteur


def calculPr(sommet, arc, apriori=None, d=.85, max_iter=10, eps=1e-5):
    if apriori is None:
        apriori = {s: 1 for s in sommet}
    n = len(sommet)
    pr = {i: 1 / n for i in sommet}
    sommePr = _calculSomme(pr)
    sommeAncienPr = -9999999
    compteur = 0
    while abs(sommePr - sommeAncienPr) > eps and compteur < max_iter:
        tempPr = dict()
        for j in sommet:
            somme = 0
            for i in sommet:
                if j in arc[i]:
                    somme += (pr[i] / len(arc[i])) * _compte(j, arc[i])
            tempPr[j] = d * somme + (1 - d) * apriori[j]
        sommeAncienPr = _calculSomme(pr)
        sommePr = _calculSomme(tempPr)
        pr = tempPr
        compteur += 1
    return sorted(pr.items(), key=lambda x:(x[1], x[0]), reverse=True)


def main():
    #A :1,B:2,C:3,D:4
    sommet = [1, 2, 3, 4]
    #arc ex : {1 : [2,3],2:[3],3:[1],4:[3]}, 1 est relié à deux et à trois, arc orienté
    arc = {1: [2, 3], 2: [3], 3: [1], 4: [3]}
    d = 0.85
    a = {1: 1, 2: 1, 3: 1, 4: 1}
    Pr = calculPr(sommet, arc, a, d, 1000, 1e-5)
    print(Pr)
    
if __name__ == '__main__':
    main()
