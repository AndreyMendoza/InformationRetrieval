import re, os, time, math, json as js
from Code.Tools import *

class Indexer(Tools):

    def __init__(self):#, stopwordsDir, collectionDir, prefix):

        self.stopwordsPath = '..\stopwords.txt'
        self.stopwords = []
        self.collectionDir = '..\man.es'
        self.prefix = 'tests'

        self.collection = {'name':'', 'path':'..\man.es', 'totalDocs': 0, 'average': 0}
        self.documents = {}
        self.frequencies = {}
        self.weights = {}
        self.vocabulary = {}

        self.docID = 1

#------------------------------------------------------------------------------------------------------------------------

    def Run(self):
        self.ReadStopwords()
        self.ReadCollection()
        self.SortFrequencies()
        self.Weights()
        self.WriteIndex()

#-----------------------------------------------------------------------------------------------------------------------

    def ReadStopwords(self):

        '''
        Lee un archivo y toma cada termino por linea como un stopword y lo guarda en el atributo 'stopwords'.
        :return:
        '''

        file = open(self.stopwordsPath, 'r')
        for line in file:
            word = re.findall(r'\w\w*', line)                       #Ignora los espacios para tomar solo el termino
            self.stopwords += word
        file.close()

#-----------------------------------------------------------------------------------------------------------------------

    def ReadCollection(self):

        '''
        Lee la collecion de documentos a partir de la ruta indicada.
        :return:
        '''
                                                                            #Extrae el nombre de la coleccion
        self.collection['name'] = re.findall(r'[a-zA-Z0-9][a-zA-Z0-9\.]*', self.collection['path'])[-1]
        subDir = os.listdir(self.collection['path'])                        #Obtiene los subdirectorios
        average = 0
        for dir in subDir:
            fileNames = os.listdir(self.collection['path'] + '\\' + dir)    #Rutas de los archivos de una subcarpeta
            self.collection['totalDocs'] += len(fileNames)                  #Suma al total de archivos
            largo = fileNames
            for fileName in fileNames:
                match = re.search(r'\w\w*.txt', fileName)
                if match:
                    filePath = self.collection['path'] + '\\' + dir + '\\' + fileName
                    handler = open(filePath, 'r')
                    average += self.ProcessDoc(handler, filePath)
                    handler.close()
        self.collection['average'] = average

#-----------------------------------------------------------------------------------------------------------------------

    def ProcessDoc(self, docHandler, filePath):

        '''
        Procesa todas las lineas de un documento, quitandole a cada palabra que cumpla con la Regex el acento y
        transformandolas a minusculas. Va guardando cierta informacion necesaria la indexacion.
        :param docHandler: objeto que contiene la direccion del documento abierto.
        :param filePath: ruta del archivo que se está procesando.
        :return:
        '''

        #Crear un espacio para el documento en cada diccionario.
        ID = self.docID                                                 # Numero de documento
        self.documents[ID] = {'path': filePath}
        self.frequencies[ID] = {'totalTerms': 0, 'terms':{}, 'long':0}  # Terms contiene todas las palabras con sus frecuencias

        complement = r'\.{2,}'
        regex = r'\w[\w.]*[\w]­?|\w'                                    # Regex para validar el texto valido
        long = 0

        for line in docHandler:                                         # Leer el documento linea por
            line = re.sub(complement, r' ', line, 0)
            words = re.findall(regex, line)                             # Lista de palabras leidas que cumplen con la ER

            for word in words:                                          # Quitar acentos y transformar a minusculas las palabras
                splittedWords = word.split('.')
                long += self.__AddTerm(word, ID)

                if len(splittedWords) > 1:
                    for splittedWord in splittedWords:
                        try:
                            int(splittedWord)
                        except:
                            long += self.__AddTerm(splittedWord, ID)
        self.frequencies[ID]['long'] = long
        self.docID += 1                                                 # Aumentar el contador de documentos
        return long

#-----------------------------------------------------------------------------------------------------------------------

    def __AddTerm(self, word, docID):

        word = self.DeleteAccents(word)
        word = word.lower()

        if word not in self.stopwords:

            if self.frequencies[docID]['terms'].get(word):  # Si ya aparecio en el documento, aumentar el contador
                self.frequencies[docID]['terms'][word] += 1
            else:
                self.frequencies[docID]['terms'][word] = 1  # Crear par ordenado con el termino y la frecuencia
                self.frequencies[docID]['totalTerms'] += 1  # Aumentar la cantidad de terminos distintos

                if self.vocabulary.get(word):  # Si la palabra ya existe en el vocabulario
                    self.vocabulary[word] += 1  # Contabilizar en la cantidad de documentos que aparece
                else:
                    self.vocabulary[word] = 1  # Agregar la palabra al vocabulario y apariciones en documentos
            return 1
        return 0

#-----------------------------------------------------------------------------------------------------------------------

    def Weights(self):

        N = self.collection['totalDocs']                                # Total de documentos

        for ID in self.frequencies:                                     # Para cada doc de la lista de frecuencias:
            terms = self.frequencies[ID]['terms']                       # Saca los terminos
            total = self.frequencies[ID]['totalTerms']
            self.weights[ID] = {'totalTerms':total, 'terms':{}}
            norm = 0
            for word in terms:
                Fij = terms[word]                                       # Frecuencia de 'word'
                ni =  self.vocabulary[word]                             # Documentos en los que aparece 'word'
                weight = (1 + math.log2(Fij)) * (math.log2(N/ni))       # Calcula el peso
                self.weights[ID]['terms'][word] = weight                # Se guardan las palabras sin orden alfabetico de momento
                norm += weight ** 2
            self.weights[ID]['norm'] = math.sqrt(norm)


#-----------------------------------------------------------------------------------------------------------------------

    def SortFrequencies(self):

        '''
        frecuencies = {ID: {'totalTerms': N, 'terms': {term1: asd}}}
        '''

        for ID in self.frequencies:
            self.frequencies[ID]['terms'] = self.SortDictionary(self.frequencies[ID]['terms'], 0, False)[0]

#-----------------------------------------------------------------------------------------------------------------------

    def WriteIndex(self):
        docsToWrite = {'COLECCION': self.collection,
                         'DOCUMENTOS': self.documents,
                         'FRECUENCIAS': self.frequencies,
                         'PESOS': self.weights,
                         'VOCABULARIO': self.vocabulary}

        for doc in docsToWrite:
            file = open('..\\Index\\' + self.prefix + '_' + doc[:2] + '.json', 'w')
            json = js.dumps({doc: docsToWrite[doc]})
            file.write(json)
            file.close()

        #Agregar stopwords al indexado
        file = open('..\\Index\\' + self.prefix + '_SW' + '.json', 'w')
        json = js.dumps({'STOPWORDS': self.stopwords})
        file.write(json)
        file.close()

#-----------------------------------------------------------------------------------------------------------------------