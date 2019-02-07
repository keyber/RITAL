import numpy as np
import collections
import porter

docs = ["the new home has been saled on top forecasts",
        "the home sales rise in july","there is an increase in home sales in july",
        "july encounter a new home sales rise"]
mots_vides = {'the', 'a', 'an', 'on', 'behind', 'under', 'there', 'in', 'on'}

def counter(phrase):
    l = (porter.stem(w.lower()) for w in phrase.split(" ") if w not in mots_vides)
    return dict(collections.Counter(l).items())


def create_ind_indInv(list_docs):
    """
    {iDoc: {w: occ}}
    {w: {iDoc: occ}}
    """
    index = {i: counter(d) for (i,d) in enumerate(list_docs)}
    
    all_words = set().union(*(set(counter(d).keys()) for d in list_docs))
    
    indinv = {w: {i:index[i][w] for i in range(len(list_docs)) if w in index[i]} for w in all_words}
    
    return index, indinv


def create_tf_idf(list_docs):
    """{iDoc: {w: tf-idf}}"""
    N = len(list_docs)
    index, index_inverse = create_ind_indInv(list_docs)
    
    def tf(i, w):
        return index[i][w]
    
    def df(w):
        return len(index_inverse[w])
    
    def idf(w):
        return np.log((1 + N) / (1 + df(w)))
    
    def tf_idf(i, w):
        return tf(i, w) * idf(w)
    
    return {i: {w: tf_idf(i, w) for w in index[i].keys()} for i in range(len(list_docs))}

#print(create_tf_idf(docs))



##########   2) PARSING FICHIER        #######
balises = {'I', 'T', 'B', 'A', 'K', 'W', 'X'}
balises = {'.'+c for c in balises}
bal_i = '.I'
bal_t = '.T'

def buildDocCollectionSimple(file_path):
    res = []
    with open(file_path) as f:
        s = f.readline()
        
        while s:
            #se place à la première balise I
            while s[:2] != bal_i and s:
                s = f.readline()
            
            #pas de balise I, fin du doc
            if not s:
                break
            
            #l'indice du document est sur la même ligne que la balise I
            idoc = s.split()[1]
            
            lines = []
            
            s = f.readline()
            #cherche balise T (ou I, auquel cas il n'y a pas de T)
            while s[:2] != bal_t and s[:2] != bal_i and s:
                s = f.readline()
                
            if s[:2] == bal_t:
                s = f.readline()
                #copie tout jusqu'à rencontrer n'importe quelle balise
                while s[:2] not in balises and s:
                    lines.append(s)
                    s = f.readline()
            
            res.append((idoc, lines))
    return res


#print(buildDocCollectionSimple("data/cacmShort.txt"))


import re
def buildDocumentCollectionRegex(file_path):
    res = []
    with open(file_path) as f:
        texte = f.read().replace("\n", " ").split(bal_i)
    for doc in texte[1:2]:
        iDoc = re.search("\.[ITBAKWX]", doc)
        req = re.findall("\.T .* \.[ITBAKWX]", doc)
        print(req)
        T = ""
        if len(req):
            T = req[0][3:-3]
        res.append((iDoc, T))
    return res

buildDocumentCollectionRegex("data/cacmShort.txt")



#normaliser sur index qui contient nb occ
#inverse ne somme pas à un



class Document:
    def __init__(self, identifiant, texte):
        self.I = identifiant
        self.T = texte

class Parser:
    def __init__(self, docs):
        self.docs = docs
        
class IndexerSimple:
    def indexation(self):
        pass
    def getTfsForDoc(self):
        pass
    def getTfIdfsForDoc(self):
        pass
    def getTfsForStem(self):
        pass
    def getTfIDFsForStem(self):
        pass
    