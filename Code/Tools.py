import unicodedata, operator

class Tools:

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

    def SortDictionary(self, dict, value):
        sortedValues = sorted(dict.items(), key=operator.itemgetter(value), reverse=True)
        resultDict = {}

        for tuple in sortedValues:
            resultDict[tuple[0]] = tuple[1]
        return resultDict, sortedValues