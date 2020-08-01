import re

# Clase que contiene los métodos para validar el formato del nombre de un profesor 
class NameRegex:
    _name_pattern = "^([a-zA-Z]{2,}\s[a-zA-Z]{1,}'?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)$"

    def checkName(self, name):
        if re.search(self.getPattern(), name):
            return True
        else:
            return False
        
    def getPattern(self):
        return self._name_pattern

# Clase que contiene los métodos para validar el formato de la cédula de un profesor 
class CedRegex:
    _ced_pattern = "[1-7]0\d{3}0\d{3}"

    def checkCed(self, ced):
        if re.search(self.getPattern(), ced):
            return True
        else:
            return False
        
    def getPattern(self):
        return self._ced_pattern

# Clase Facade para hacer uso de los métodos para validar formato de cedula y nombre
# del profesor
class Facade:
    def __init__(self):
        self._name_regex = NameRegex()
        self._ced_regex = CedRegex()

    def checkName(self, name):
        return self._name_regex.checkName(name)

    def checkCed(self, ced):
        return self._ced_regex.checkCed(ced)
