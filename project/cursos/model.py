from project import db
from project.associations import profesores_cursos

# Clase Curso que gestiona tanto el objeto Curso como el modelo de la BD
class Curso(db.Model):
    __tablename__ = 'cursos'

    _id = db.Column(db.Integer, primary_key=True)
    _nombre = db.Column(db.Text, unique=True)
    _tipo = db.Column(db.Text)
    _creditos = db.Column(db.Integer)
    _semestre = db.Column(db.Integer)
    _lecciones = db.Column(db.Integer)
    _profesores = db.relationship("Profesor", secondary=profesores_cursos, back_populates="_cursos")

    def __init__(self, nombre, tipo, creditos, semestre, lecciones):
        self._nombre = nombre
        self._tipo = tipo
        self._creditos = creditos
        self._semestre = semestre
        self._lecciones = lecciones

    def __repr__(self):
        return (f"ID: {self.getId()}, Curso: {self.getNombre()}, Tipo: {self.getTipo()}," 
                + f" Creditos: {self.getCreditos()}, Semestre: {self.getSemestre()}, Lecciones: {self.getLecciones()}")

    def getId(self):
        return self._id
    
    def getNombre(self):
        return self._nombre

    def getTipo(self):
        return self._tipo
    
    def getCreditos(self):
        return self._creditos
    
    def getSemestre(self):
        return self._semestre

    def getLecciones(self):
        return self._lecciones

    def setNombre(self, nombre):
        self._nombre = nombre
    
    def setTipo(self, tipo):
        self._tipo = tipo
    
    def setCreditos(self, creditos):
        self._creditos = creditos
    
    def setSemestre(self, semestre):
        self._semestre = semestre

    def setLecciones(self, lecciones):
        self._lecciones = lecciones