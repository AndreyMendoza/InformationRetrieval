from Code.Indexer import *
from Code.SearchEngine import *
import re
'''
Ejecución del programa
'''


start = time.clock()

# a = Indexer()
# a.Run()


#print (len(a.vocabulary))

#print(list(a.frequencies[1]['terms']))


s = SearchEngine()

#Solo se instancia la clase, llama al tipo de busqueda y le pasa la consulta, el prefix y el outputName

s.BM25Search('compresión de archivos y manejo de archivos comprimidos.', 'tests', 'bmtest')
s.VectorSearch('compresión de archivos y manejo de archivos comprimidos.', 'tests', 'vectortest')


print('Finalizado!\nDuracion: ', time.clock() - start)











def tryRegex():
    docHandler = open('..\\man.es\\man1\\addr2line.1.txt', 'r')
    #regex = r'[A-Za-zñ0-9][\w.ñ]*[\wñ](-\n)?|[A-Za-zñ0-9]'  # Regex para validar el texto valido#

    regex = r'\w[\w.]*[\w]­?|\w'
    complement = r'\.{2,}'
    docWriter = open('..\\salida.txt', 'w')


    for line in docHandler:  # Leer el documento linea por linea
        #line = "".join(c for c in unicodedata.normalize('NFD', line) if unicodedata.category(c) != 'Mn')
        line = re.sub(complement, r' ', line, 0)
        words = re.findall(regex, line)
        if words != []:
            docWriter.write(str(words) + '\n')
    docHandler.close()
    docWriter.close()

#tryRegex()
