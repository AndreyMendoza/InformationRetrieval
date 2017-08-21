import re
import os
import unicodedata
import time
import math

class Indexer:

    def __init__(self):#, stopwordsDir, collectionDir, prefix):

        self.stopwordsPath = '..\stopwords.txt'
        self.stopwords = []
        self.collectionDir = '..\man.es'
        self.prefix = 'tests'

        self.collection = {'name':'', 'path':'..\man.es', 'totalDocs': 0}
        self.documents = {}
        self.frecuencies = {}
        self.weights = {}
        self.vocabulary = {}

        self.docID = 1

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
        for dir in subDir:
            fileNames = os.listdir(self.collection['path'] + '\\' + dir)    #Rutas de los archivos de una subcarpeta
            self.collection['totalDocs'] += len(fileNames)                  #Suma al total de archivos
            for fileName in fileNames:
                match = re.search(r'\w\w*.txt', fileName)
                if match:
                    filePath = self.collection['path'] + '\\' + dir + '\\' + fileName
                    handler = open(filePath, 'r')
                    self.ProcessDoc(handler, filePath)
                    handler.close()

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
        ID = self.docID                                             # Numero de documento
        self.documents[ID] = {'path': filePath}
        self.frecuencies[ID] = {'totalTerms': 0, 'terms':{}}
        self.weights[ID] = {}
        #self.docID += 1                                             # Aumentar el contador de documentos

        regex = r'[A-Za-zñ0-9]*[\w.ñ]|[A-Za-zñ]'                    # Regex para validar el texto valido


        '''
        Hay que cambiar el orden de la lógica o buscar otro metodo, no agarra palabras con tildes en la regex de momento
        '''

        for line in docHandler:                                     # Leer el documento linea por linea
            words = re.findall(regex, line)                         # Lista de palabras leidas que cumplen con la ER
            for word in words:                                      # Quitar acentos y transformar a minusculas las palabras
                if word not in self.stopwords:
                    word = self.DeleteAccents(word)
                    word = word.lower()

                    if self.frecuencies[ID].get(word):              # Si ya aparecio en el documento, aumentar el contador
                        self.frecuencies[ID][word] += 1
                    else:
                        self.frecuencies[ID][word] = 1              # Crear par ordenado con el termino y la frecuencia
                        self.frecuencies[ID]['totalTerms'] += 1     # Aumentar la cantidad de terminos distintos

                        if self.vocabulary.get(word):               # Si la palabra ya existe en el vocabulario
                            self.vocabulary[word] += 1              # Contabilizar en la cantidad de documentos que aparece
                        else:
                            self.vocabulary[word] = 1               # Agregar la palabra al vocabulario y apariciones en documentos
                else:
                    words.remove(word)
        self.docID += 1  # Aumentar el contador de documentos

#-----------------------------------------------------------------------------------------------------------------------

    def DeleteAccents(self, word):

        '''
        Elimina todos los acentos a excepcion de la 'ñ'
        :param word: palabra a la que se desea eliminar los acentos
        :return: palabra con los acentos eliminados
        '''

        pos = word.find('ñ')
        result = "".join(c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn')
        if pos != -1:
            result = result[:pos] + 'ñ' + result[pos + 1:]
        return result

#-----------------------------------------------------------------------------------------------------------------------

    def Weights(self):

        N = self.collection['totalDocs']                            #Total de documentos
        ni = 0

        for ID in self.frecuencies:                                 #Para cada doc de la lista de frecuencias:
            terms = self.frecuencies.get(ID)                        #Saca los terminos
            for word in terms:
                Fij = terms[word]                                   #Frecuencia de 'word'
                ni =  self.vocabulary[word]                         #Documentos en los que aparece 'word'
                weight = (1+ math.log2(Fij))*(math.log2(N/ni))      #Calcula el peso

                self.weights[ID][word] = weight


#-----------------------------------------------------------------------------------------------------------------------

'''
Ejecución del programa
'''
start = time.clock()
a = Indexer()
a.ReadStopwords()
a.ReadCollection()
print('Palabras contadas: ', len(a.vocabulary))
#print(a.vocabulary)
print('Finalizado!\nDuracion: ', time.clock() - start)