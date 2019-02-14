import re
import pdb

class Document:
    def __init__(self, identifiant, texte):
        self.I = identifiant
        self.T = texte


class Parser:
    def __init__(self, docs):
        self.docs = {Document(ident, text) for (ident, text) in docs}
    def afficher(self):
        for d in self.docs:
            print("Id : "+str(d.I) + ", Texte : "+str(d.T) )


def loadCollection(list_docs):
    return Parser(enumerate(list_docs))


balises = {'I', 'T', 'B', 'A', 'K', 'W', 'X'}
balises = {'.' + c for c in balises}
bal_i = '.I'
bal_t = '.T'


def buildDocCollectionSimple(file_path):
    """Préserve les \n"""
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
                    lines.append(s[:-1])#ne copie pas le \n
                    s = f.readline()

            res.append((idoc, lines))
    return Parser(res)


def buildDocumentCollectionRegex(file_path):
    """Ne préserve pas les \n"""
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
        txt = doc[txt.start() + 3: txt.end() - 3]
        res.append((iDoc, txt))
    return Parser(res)
