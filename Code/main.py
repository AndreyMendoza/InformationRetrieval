from Code.SearchEngine import *
from Code.Indexer import *

'''
Ejecución del programa
'''
start = time.clock()
'''a = Indexer()
a.ReadStopwords()
a.ReadCollection()

a.SortDocs()
a.WriteIndex()'''

s = SearchEngine('tests', 'testResults', 'Introducción a los archivos especiales')
print(s.queryWeights)

print('Finalizado!\nDuracion: ', time.clock() - start)