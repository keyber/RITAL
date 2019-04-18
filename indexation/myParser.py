import re


class Document:
    def __init__(self, doc):
        self.I = doc[0]
        self.T = doc[1]
        self.P = doc[2] if len(doc)==3 else None
    

class Parser:
    def __init__(self, docs):
        self.docs = {d[0]: Document(d) for d in docs if d[1]!=""}
        if len(docs) != len(self.docs):
            print("Parser removed", len(docs) - len(self.docs), "empty documents")

    def afficher(self):
        for d in self.docs:
            print("Id : " + str(d.I) + ", Texte : " + str(d.T))


def loadCollection(list_docs):
    return Parser(list(enumerate(list_docs)))


balises = {'I', 'T', 'B', 'A', 'K', 'W', 'X'}
balises = {'.' + c for c in balises}
bal_i = '.I'
bal_t = '.T'


def buildDocCollectionSimple(file_path, balise=bal_t, balise2=None):
    """travaille ligne par ligne"""
    res = []
    with open(file_path) as f:
        s = f.readline()

        while s:
            # se place à la première balise I
            while s[:2] != bal_i and s:
                s = f.readline()

            # pas de balise I, fin du doc
            if not s:
                break

            # l'indice du document est sur la même ligne que la balise I
            iDoc = s.split()[1]

            lines = []
            pointed = []

            s = f.readline()
            # cherche balise T (ou I, auquel cas il n'y a pas de T)
            # ou balise X
            for _ in range(2): #cherche jusqu'a deux balises
                while s[:2] != balise and s[:2] != bal_i and s[:2] != balise2 and s:
                    s = f.readline()
    
                if s[:2] == balise:
                    s = f.readline()
                    # copie tout jusqu'à rencontrer n'importe quelle balise
                    while s[:2] not in balises and s:
                        lines.append(s[:-1])  #ne copie pas le \n
                        s = f.readline()
                
                if s[:2] == balise2:
                    s = f.readline()
                    # jusqu'à rencontrer n'importe quelle balise
                    while s[:2] not in balises and s:
                        l = s.split()
                        if len(l)>0:
                            pointed.append(l[0])
                        s = f.readline()

            res.append((iDoc, " ".join(lines), set(pointed)))
    return Parser(res)


def buildDocumentCollectionRegex(file_path):
    """travaille sur le document vu comme un grande chaîne
    Ne marche pas sur les grands fichiers"""
    res = []
    with open(file_path) as f:
        texte = f.read().replace("\n", " ").split(bal_i)
    #On commence à 1 car le premier split est vide
    for doc in texte[1:]:
        #On récupere l'id du document
        iDoc = re.search("(.*?)(([.][I])|([.][T])|([.][B])|([.][A])|([.][K])|([.][W])|([.][X]))", doc)
        iDoc = doc[iDoc.start() + 1: iDoc.end() - 3]
        #On récupere le texte du document
        txt = re.search("[.][T](.*?)(([.][I])|([.][B])|([.][A])|([.][K])|([.][W])|([.][X]))", doc)
        if txt is not None:
            txt = doc[txt.start() + 3: txt.end() - 3]
        else:
            print("format non supporté (balise dans texte)")
            print("le idoc est "+str(iDoc))
            print("##########################")
        res.append((iDoc, txt))
    return Parser(res)
