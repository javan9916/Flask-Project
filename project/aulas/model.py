from project import db
from abc import ABC, abstractmethod

# Clase Aula que gestiona tanto el objeto Aula como el modelo de la BD
class Aula(db.Model):
    __tablename__ = 'aulas'

    _id = db.Column(db.Integer, primary_key=True)
    _nombre = db.Column(db.Text, unique=True)
    _capacidad = db.Column(db.Integer)
    _tipo = db.Column(db.Text)

    def __init__(self, nombre, capacidad, tipo):
        self._nombre = nombre
        self._capacidad = capacidad
        self._tipo = tipo

    def __repr__(self):
        return f"ID: {self.getId()}, Aula: {self.getNombre()}, Capacidad: {self.getCapacidad()}, Tipo: {self.getTipo()}"
    
    def getId(self):
        return self._id
    
    def getNombre(self):
        return self._nombre

    def getCapacidad(self):
        return self._capacidad

    def getTipo(self):
        return self._tipo

    def setNombre(self, nombre):
        self._nombre = nombre

    def setCapacidad(self, capacidad):
        self._capacidad = capacidad
    
    def setTipo(self, tipo):
        self._tipo = tipo

# Interface Aula
class AulaInterface(ABC):

    @abstractmethod
    def getAulas(self):
        pass

    @abstractmethod
    def addAula(self, aula):
        pass

    @abstractmethod
    def updateAula(self, aula):
        pass

    @abstractmethod
    def deleteAula(self, aula):
        pass

# Clase AulaDaoImpl de la cual se toman las gestiones de la base de datos
class AulaDaoImpl(AulaInterface):

    def getAulas(self):
        return Aula.query.all()

    def addAula(self, aula):
        db.session.add(aula)
        db.session.commit()

    def updateAula(self, aula, nombre, capacidad, tipo):
        aula.setNombre(nombre)
        aula.setCapacidad(capacidad)
        aula.setTipo(tipo)
        
        db.session.add(aula)
        db.session.commit()

    def deleteAula(self, aula):
        db.session.delete(aula)
        db.session.commit()