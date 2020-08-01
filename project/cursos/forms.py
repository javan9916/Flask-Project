from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired

# Form para crear un nuevo curso
class CreateCursoForm(FlaskForm):
    nombre = StringField(u'Nombre: ', validators=[DataRequired()])
    tipo = SelectField(u'Tipo de aula: ', validators=[DataRequired()], 
                        choices=[('aula','Aula'), ('lab','Laboratorio')])
    creditos = IntegerField(u'Número de créditos: ', validators=[DataRequired()])
    semestre = SelectField(u'Semestre al que pertenece: ', coerce=int, validators=[DataRequired()],
                            choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7')])
    lecciones = SelectField(u'Cantidad de lecciones: ', coerce=int, validators=[DataRequired()],
                            choices=[(2,'2'),(4,'4')])
    submit = SubmitField('Crear')

# Form para actualizar un curso
class UpdateCursoForm(FlaskForm):
    curso = SelectField(u'Curso: ', coerce=int, validators=[DataRequired()])
    nombre = StringField(u'Nombre: ', validators=[DataRequired()])
    tipo = SelectField(u'Tipo de aula: ', validators=[DataRequired()], 
                        choices=[('aula','Aula'), ('lab','Laboratorio')])
    creditos = IntegerField(u'Número de créditos: ', validators=[DataRequired()])
    semestre = SelectField(u'Semestre al que pertenece: ', coerce=int, validators=[DataRequired()],
                            choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7')])
    lecciones = SelectField(u'Cantidad de lecciones: ', coerce=int, validators=[DataRequired()],
                            choices=[(2,'2'),(4,'4')])
    submit = SubmitField('Actualizar')

# Form para eliminar un curso
class DeleteCursoForm(FlaskForm):
    curso = SelectField(u'Curso: ', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Eliminar')