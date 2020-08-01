from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired

# Form para crear un nuevo profesor
class CreateProfesorForm(FlaskForm):
    nombre = StringField(u'Nombre: ', validators=[DataRequired()], render_kw={"placeholder": "Formato: Nombre con 1 o 2 apellidos"})
    cedula = IntegerField(u'Cédula: ', validators=[DataRequired()], render_kw={"placeholder": "Formato: 102340567"})
    submit = SubmitField(u'Crear')

# Form para actualizar un profesor
class UpdateProfesorForm(FlaskForm):
    cedula = SelectField(u'Cédula: ', coerce=int, validators=[DataRequired()])
    nombre = StringField(u'Nombre: ', validators=[DataRequired()])
    submit = SubmitField(u'Actualizar')

# Form para eliminar un profesor
class DeleteProfesorForm(FlaskForm):
    cedula = SelectField(u'Cédula: ', coerce=int, validators=[DataRequired()])
    submit = SubmitField(u'Eliminar')

# Form para conectar un profesor con un curso
class ConexionCursoForm(FlaskForm):
    cedula = SelectField(u'Cédula del profesor: ', coerce=int, validators=[DataRequired()])
    curso = SelectField(u'Curso que imparte: ', coerce=int, validators=[DataRequired()])
    submit = SubmitField(u'Crear')

# Form para eliminar la conexión de un profesor con un curso
class DeleteCursoForm(FlaskForm):
    cedula = SelectField(u'Cédula del profesor: ', coerce=int, validators=[DataRequired()])
    curso = SelectField(u'Curso que imparte: ', coerce=int, validators=[DataRequired()])
    submit = SubmitField(u'Eliminar')

# Form para crear la disponibilidad de un profesor
class DisponibilidadProfesorForm(FlaskForm):
    cedula = SelectField(u'Cédula: ', coerce=int, validators=[DataRequired()])
    l1 = BooleanField()
    l2 = BooleanField()
    l3 = BooleanField()
    l4 = BooleanField()
    l5 = BooleanField()
    l6 = BooleanField()
    l7 = BooleanField()
    l8 = BooleanField()
    x1 = BooleanField()
    x2 = BooleanField()
    x3 = BooleanField()
    x4 = BooleanField()
    x5 = BooleanField()
    x6 = BooleanField()
    x7 = BooleanField()
    x8 = BooleanField()
    m1 = BooleanField()
    m2 = BooleanField()
    m3 = BooleanField()
    m4 = BooleanField()
    m5 = BooleanField()
    m6 = BooleanField()
    m7 = BooleanField()
    m8 = BooleanField()
    j1 = BooleanField()
    j2 = BooleanField()
    j3 = BooleanField()
    j4 = BooleanField()
    j5 = BooleanField()
    j6 = BooleanField()
    j7 = BooleanField()
    j8 = BooleanField()
    v1 = BooleanField()
    v2 = BooleanField()
    v3 = BooleanField()
    v4 = BooleanField()
    v5 = BooleanField()
    v6 = BooleanField()
    v7 = BooleanField()
    v8 = BooleanField()
    submit = SubmitField(u'Registrar')
    