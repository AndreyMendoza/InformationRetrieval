from Code.Indexer import *
from Code.SearchEngine import *
import sys


def main(argv):

    if argv[0].lower() == 'generar':
        try:
            stopwordsPath = argv[1]
            collectionPath = argv[2]
            prefix = argv[3]

            start = time.clock()
            indexer = Indexer()
            indexer.Index(stopwordsPath, prefix, collectionPath)
            print('Finalizado!\nDuracion: ', time.clock() - start)
        except:
            sys.exit('Error.')
    elif argv[0].lower() == 'buscar':
        try:
            rankStart = int(argv[2])
            rankEnd = int(argv[3])
            prefix = argv[4]
            outputName = argv[5]
            query = argv[6]
            engine = SearchEngine()

            if argv[1].lower() == 'vec':
                start = time.clock()
                engine.VectorSearch(query, prefix, outputName, rankStart, rankEnd)
                print('Finalizado!\nDuracion: ', time.clock() - start)
            elif argv[1].lower() == 'bm25':
                start = time.clock()
                engine.BM25Search(query, prefix, outputName, rankStart, rankEnd)
                print('Finalizado!\nDuracion: ', time.clock() - start)
        except:
            sys.exit('Cantidad de parametros invalida')



if __name__ == '__main__':
    main(sys.argv[1:])






