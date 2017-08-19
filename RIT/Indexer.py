import re
import os

class Indexer:

    def __init__(self):#, stopwordsDir, collectionDir, prefix):

        self.stopwordsDir = '..\stopwords.txt'
        self.stopwords = []
        self.collection = '..\man.es'
        self.prefix = 'tests'

    def readStopwords(self):

        '''
        Lee un archivo y toma cada termino por linea como un stopword y lo guarda en el atributo 'stopwords'.
        :return:
        '''

        file = open(self.stopwordsDir, 'r')
        for line in file:
            word = re.findall(r'\w\w*', line)            #Ignora los espacios para tomar solo el termino
            self.stopwords += word
        file.close()




a = Indexer()
a.readStopwords()
print(a.stopwords)
