from Code.TextTools import *
import json as js, re, math



class SearchEngine(TextTools):

    def __init__(self, prefix, outputName, query):

        self.prefix = prefix
        self.outputName = outputName
        self.ReadIndexFiles()
        self.queryFrequencies = {'totalTerms': 0, 'terms':{}}
        self.queryWeights = {}

        self.ProcessQuery(query)                                    # Quitar stopwords, acentos y sacar pesos
        self.Weights()


    def ReadIndexFiles(self):

        path = '..\\Index\\' + self.prefix

        file = open(path + '_CO.json', 'r')
        self.collection = js.loads(list(file)[0])['COLECCION']
        file.close()

        file = open(path + '_DO.json', 'r')
        self.documents = js.loads(list(file)[0])['DOCUMENTOS']
        file.close()

        file = open(path + '_FR.json', 'r')
        self.frequencies = js.loads(list(file)[0])['FRECUENCIAS']
        file.close()

        file = open(path + '_PE.json', 'r')
        self.weights = js.loads(list(file)[0])['PESOS']
        file.close()

        file = open(path + '_VO.json', 'r')
        self.vocabulary = js.loads(list(file)[0])['VOCABULARIO']
        file.close()

        file = open(path + '_SW.json', 'r')
        self.stopwords = js.loads(list(file)[0])['STOPWORDS']
        file.close()

    def ProcessQuery(self, query):

        regex = r'[A-Za-zñ0-9]*[\w.ñ]|[A-Za-zñ]'                    # Regex para validar el texto valido
        queryWords = re.findall(regex, query)

        for word in queryWords:
            if not word in self.stopwords:
                word = word.lower()
                word = self.DeleteAccents(word)
                if self.queryFrequencies['terms'].get(word):
                    self.queryFrequencies['terms'][word] += 1
                else:
                    self.queryFrequencies['terms'][word] = 1
                    self.queryFrequencies['totalTerms'] += 1


    def Weights(self):

        N = self.collection['totalDocs']
        norm = 0
        for word in self.queryFrequencies['terms']:
            try:
                ni = self.vocabulary[word]
            except:
                continue

            Fij = self.queryFrequencies['terms'][word]
            weight = (1 + math.log2(Fij))*(math.log2(N/ni))
            self.queryWeights[word] = weight
            norm += weight ** 2
        self.queryNorm = math.sqrt(norm)





