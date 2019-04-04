import numpy as np
import matplotlib.pyplot as plt

def calculSomme(Pr):
    somme=0
    for key in Pr.keys():
        somme+=Pr[key]
    return somme

def calculPr(sommet,arc,a,d,max_iter,condition_arret):
    n=len(sommet)
    Pr = {i:1/n for i in sommet}
    sommePr=calculSomme(Pr)
    sommeAncienPr=-9999999
    compteur=0
    while(abs(sommePr-sommeAncienPr)>1e-5 and compteur<max_iter):
        tempPr=dict()
        for j in sommet:
            somme=0
            for i in sommet:
                if(j in arc[i]):
                    somme+=Pr[i]/len(arc[i])
            tempPr[j]=d*somme+(1-d)*a[j]
        sommeAncienPr=calculSomme(Pr)
        sommePr = calculSomme(tempPr)
        Pr=tempPr
        compteur+=1
    print(compteur)
    return Pr
#A :1,B:2,C:3,D:4
sommet = [1,2,3,4]
#arc ex : {1 : [2,3],2:[3],3:[1],4:[3]}, 1 est relier à deux et à trois, arc orienté
arc = {1 : [2,3],2:[3],3:[1],4:[3]}
d = 0.85
a = {1: 1,2:1,3:1,4:1}
Pr = calculPr(sommet,arc,a,d,1000,1e-5)
print(Pr)
