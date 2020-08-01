from project import db
from project.associations import profesores_cursos

# Clase ProfesorSubject padre de Profesor y Proxy que se utiliza para heredar los métodos
# que se van a utilizar para no tocar el objeto Profesor directamente
class ProfesorSubject:
    def __repr__(self):
        pass

    def getNombre(self):
        pass

    def getCedula(self):
        pass

    def setNombre(self, nombre):
        pass

    def setDisponibilidad(self, days, disponibilidad):
        pass

    def addCurso(self, curso):
        pass

    def deleteCurso(self, curso):
        pass

# Clase Proxy que se utiliza para no tocar el objeto Profesor directamente
class Proxy(ProfesorSubject):
    def __init__(self, objeto):
        self.objeto = objeto

    def getNombre(self):
        return self.objeto.getNombre()

    def getCedula(self):
        return self.objeto.getCedula()

    def setNombre(self, nombre):
        self.objeto.setNombre(nombre)

    def setDisponibilidad(self, days, disponibilidad):
        self.objeto.setDisponibilidad(days, disponibilidad)

    def addCurso(self, curso):
        self.objeto.addCurso(curso)
    
    def deleteCurso(self, curso):
        self.objeto.deleteCurso(curso)

# Clase Profesor que gestiona tanto el objeto Profesor como el modelo de la BD
class Profesor(db.Model, ProfesorSubject):
    __tablename__ = 'profesores'

    _id = db.Column(db.Integer, primary_key=True)
    _cedula = db.Column(db.Integer, unique=True)
    _nombre = db.Column(db.Text)
    _disponibilidad = db.relationship('Disponibilidad', back_populates="_profesor", uselist=False, cascade="all, delete-orphan")
    _cursos = db.relationship('Curso', secondary=profesores_cursos, back_populates="_profesores")

    def __init__(self, cedula, nombre):
        self._cedula = cedula
        self._nombre = nombre

    def __repr__(self):
        return f"Nombre: {self.getNombre()}, Cédula: {self.getCedula()}"

    def getId(self):
        return self._id
        
    def getCedula(self):
        return self._cedula

    def getNombre(self):
        return self._nombre

    def setNombre(self, nombre):
        self._nombre = nombre

    def setDisponibilidad(self, days, disponibilidad):
        days_name = ['Lunes','Martes','Miercoles','Jueves','Viernes']

        for i in range(len(days_name)):
            day_name = days_name[i]
            day = Dia(_nombre=day_name,_disponibilidad=disponibilidad)
            current_day = days[i]
            for j in range(len(current_day)):
                hora = Hora(_hora=current_day[j],_dia=day)
                db.session.add(hora)
            db.session.add(day)
        
        db.session.add(disponibilidad)
        db.session.commit()  

    def addCurso(self, curso):
        self._cursos.append(curso)

    def deleteCurso(self, curso):
        self._cursos.remove(curso)

# Clase disponibilidad que gestiona tanto el objeto como el modelo de la BD
class Disponibilidad(db.Model):
    __tablename__ = 'disponibilidades'

    _id = db.Column(db.Integer, primary_key=True)
    _profesor_id = db.Column(db.Integer, db.ForeignKey('profesores._id'))
    _profesor = db.relationship("Profesor", back_populates="_disponibilidad", uselist=False)
    _dias = db.relationship('Dia', back_populates='_disponibilidad', cascade="all, delete-orphan")

    def getId(self):
        return self._id

# Clase Dia que gestiona tanto el objeto como el modelo de la BD
class Dia(db.Model):
    __tablename__ = 'dias'

    _id = db.Column(db.Integer, primary_key=True)
    _nombre = db.Column(db.Text)
    _horas = db.relationship('Hora', back_populates='_dia', cascade="all, delete-orphan")
    _disponibilidad_id = db.Column(db.Integer, db.ForeignKey('disponibilidades._id'))
    _disponibilidad = db.relationship("Disponibilidad", back_populates='_dias')

    def __repr__(self):
        return f'Dia: {self.getNombre()}, Id: {self.getId()}, Disponibilidad: {self.getDisponibilidadId()}'

    def getId(self):
        return self._id

    def getNombre(self):
        return self._nombre

    def getDisponibilidadId(self):
        return self._disponibilidad_id
    
# Clase Hora que gestiona tanto el objeto como el modelo de la BD
class Hora(db.Model):
    __tablename__ = 'horas'

    _id = db.Column(db.Integer, primary_key=True)
    _hora = db.Column(db.Text)
    _dia_id = db.Column(db.Integer, db.ForeignKey('dias._id'))
    _dia = db.relationship("Dia", back_populates='_horas')

    def __repr__(self):
        return f'Hora: {self.getHora()}, Id: {self.getId()}'

    def getId(self):
        return self._id

    def getHora(self):
        return self._hora