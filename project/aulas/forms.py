from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired

# Form para crear un nuevo aula
class CreateAulaForm(FlaskForm):
    nombre = StringField(u'Nombre: ', validators=[DataRequired()])
    capacidad = IntegerField(u'Capacidad máxima: ', validators=[DataRequired()])
    tipo = SelectField(u'Tipo de aula: ', validators=[DataRequired()], 
                        choices=[('aula','Aula'), ('lab','Laboratorio')])
    submit = SubmitField('Crear')

# Form para actualizar un aula
class UpdateAulaForm(FlaskForm):
    aula = SelectField(u'Aula: ', coerce=int, validators=[DataRequired()])
    nombre = StringField(u'Nombre: ', validators=[DataRequired()])
    capacidad = IntegerField(u'Capacidad máxima: ', validators=[DataRequired()])
    tipo = SelectField(u'Tipo de aula: ', validators=[DataRequired()], 
                        choices=[('aula','Aula'), ('lab','Laboratorio')])
    submit = SubmitField('Actualizar')

# Form para eliminar un aula
class DeleteAulaForm(FlaskForm):
    aula = SelectField(u'Aula: ', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Eliminar')