import unicodedata, operator, time, os

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

    def SortDictionary(self, dict, value, reverse):
        sortedValues = sorted(dict.items(), key=operator.itemgetter(value), reverse=reverse)
        resultDict = {}

        for tuple in sortedValues:
            resultDict[tuple[0]] = tuple[1]
        return resultDict, sortedValues







