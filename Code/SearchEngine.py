from Code.Tools import *
import json as js, re, math, sys


class SearchEngine(Tools):

    def __init__(self):
        self.prefix = ""
        self.queryFrequencies = {'totalTerms': 0, 'terms':{}}
        self.queryWeights = {}

#-----------------------------------------------------------------------------------------------------------------------

    def ReadIndexFiles(self):

        path = 'Index\\' + self.prefix
        try:
            file = open(path + '_CO.json', 'r')
        except:
            sys.exit('No existen archivos de indexación con ese prefijo.')
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

#-----------------------------------------------------------------------------------------------------------------------

    def ProcessQuery(self, query):

        regex = r'\w[\w.]*[\w]­?|\w'                                # Regex para validar el texto ingresado
        complement = r'\.{2,}'
        query = re.sub(complement, r' ', query, 0)
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

#-----------------------------------------------------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------------------------------------------------

    def VectorSearch(self, query, prefix, outputName, rankStart = 0, rankEnd = 50):
        self.prefix = prefix
        self.ReadIndexFiles()
        self.queryFrequencies = {'totalTerms': 0, 'terms': {}}
        self.queryWeights = {}
        self.ProcessQuery(query)                                    # Quitar stopwords, acentos y sacar pesos
        self.Weights()
        ranking = {}

        for ID in self.weights:
            sum = 0
            for term in self.queryWeights:
                try:
                    Wtd = self.weights[ID]['terms'][term]           #Weight de term en el doc
                    Wtq = self.queryWeights[term]                   #Weight de term en el query
                    sum += Wtd*Wtq
                except:
                    continue
            a = self.weights[ID]['norm']
            sim = sum/(self.weights[ID]['norm'] * self.queryNorm)
            ranking[ID] = sim

        ranking, sortedValues = self.SortDictionary(ranking, 1, True)

        self.GenerateHTML(ranking, outputName, query, rankStart, rankEnd)

#-----------------------------------------------------------------------------------------------------------------------

    def BM25Search(self, query, prefix, outputName, rankStart = 0, rankEnd = 50, k = 1.5, b = 1):
        self.prefix = prefix
        self.queryFrequencies = {'totalTerms': 0, 'terms': {}}
        self.queryWeights = {}
        self.ReadIndexFiles()
        self.ProcessQuery(query)                                    # Quitar stopwords, acentos y sacar pesos
        N = self.collection['totalDocs']
        average = self.collection['average'] / N
        ranking = {}

        for ID in self.weights:
            sim = 0
            for term in self.queryFrequencies['terms']:
                try:
                    Fqi = self.frequencies[ID]['terms'][term]
                    n = self.vocabulary[term]
                    if n <= (self.collection['totalDocs'] // 2):
                        idf = math.log2((N - n + 0.5) / (n + 0.5))
                        sim += idf * ((Fqi * (k + 1)) / (Fqi + k * (1 - b + b * (self.frequencies[ID]['long'] / average))))
                except:
                    continue
            ranking[ID] = sim
        ranking, sortedValues = self.SortDictionary(ranking, 1, True)

        self.GenerateHTML(ranking,outputName, query, rankStart, rankEnd)

#-----------------------------------------------------------------------------------------------------------------------

    def GenerateHTML(self, ranking, outputName, query, rankStart, rankEnd):


        topHTML = '''<html><head>
            <style>
            table, h1, p{
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            
            td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            
            th {
                background-color: #4CAF50;
                color: white;
                text-align: center;
            }
            
            tr:nth-child(even) {
                background-color: #dddddd;
            }
            </style>
            <h1><center> Escalafón </center></h1></head><body>
            <p> <b>Consulta:</b> "'''+ query+'''"</p>
            <table style="width:100%">
            <tr>
              <th>Posición</th>
              <th>Ruta del Archivo</th>
              <th>Tamaño</th>
              <th>Fecha de Creación</th>
              <th>Similitud</th>
              <th>Descripción</th>
          </tr>
        '''
        pos = 0

        for ranked in ranking:
            pos += 1
            if ranking[ranked] > 0 and (rankStart <= pos <= rankEnd):
                docPath = self.documents[ranked]['path']
                fileSize = os.stat(docPath).st_size
                creationDate = time.ctime(os.path.getctime(docPath))
                # -------------------------------------------------------------
                file = open(docPath,'r')
                regex = r'DESCRIPCIÓN[\s\w\W]{200}'
                comp = 'DESCRIPCIÓN|\s+'
                text = file.read()
                text = re.search(regex, text)
                if text is not None:
                    text = re.sub(comp, r' ', text.group(), 0)
                    descripcion = text + '[...]'
                else:
                    descripcion = "Sin descripción"

                file.close()

                topHTML += '''
                    <tr>
                        <td> <center> ''' + str(pos) + '''</center> </td>      
                        <td> <center> ''' + docPath + '''</center> </td>
                        <td> <center>''' + str(fileSize) + '''B</center> </td>
                        <td> <center>''' + creationDate + '''</center> </td>
                        <td> <center>''' + str(ranking[ranked]) + '''</center> </td>
                        <td> <center>''' + descripcion + '''</center> </td>
                    </tr>
                '''
            else:
                break
        topHTML += '''
        </table> </body> </html>        
        '''

        file = open('Search Results\\' + outputName + '.html', 'w')
        file.write(topHTML)
        file.close()



