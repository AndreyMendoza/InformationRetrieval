from Code.TextTools import *
import json as js



class SearchEngine(TextTools):



    def __init__(self, prefix, outputName, query):

        self.prefix = prefix
        self.outputName = outputName
        self.query = query


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

    #def ProcessQuery(self):

