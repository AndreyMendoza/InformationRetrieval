from Code.SearchEngine import *
from Code.Indexer import *

'''
Ejecución del programa
'''


start = time.clock()

a = Indexer()
a.Run()

'''
s = SearchEngine('tests', 'testResults', 'Introducción a los archivos especiales')
res, values = s.VectorSearch('Introducción a órdenes de usuario')
print(res)
print(s.documents[values[0][0]])
'''

print('Finalizado!\nDuracion: ', time.clock() - start)