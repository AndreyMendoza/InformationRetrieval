from Code.Indexer import *
from Code.SearchEngine import *
'''
Ejecución del programa
'''


start = time.clock()

a = Indexer()
a.Run()


# s = SearchEngine('tests', 'testResults', 'Introducción a los archivos especiales')
# res, values = s.BM25Search('archivos comprimidos.')
# print(res)
# print(s.documents[values[1][0]])


print('Finalizado!\nDuracion: ', time.clock() - start)