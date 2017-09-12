import unicodedata, operator, time, os, re

class Tools:

#-----------------------------------------------------------------------------------------------------------------------

    def DeleteAccents(self, word):

        '''
        Elimina todos los acentos a excepcion de la 'ñ'
        :param word: palabra a la que se desea eliminar los acentos
        :return: palabra con los acentos eliminados
        '''

        word = re.sub(r'ñ', r'<n>', word, 0)              # Sustituir la ñ por <n>
        result = "".join(c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn')
        result = re.sub(r'<n>', r'ñ', word, 0)            # Sustituir <n> por ñ
        return result

#-----------------------------------------------------------------------------------------------------------------------

    def SortDictionary(self, dict, value, reverse):
        sortedValues = sorted(dict.items(), key=operator.itemgetter(value), reverse=reverse)
        resultDict = {}

        for tuple in sortedValues:
            resultDict[tuple[0]] = tuple[1]
        return resultDict, sortedValues







