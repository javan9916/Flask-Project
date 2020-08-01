from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, SelectMultipleField, BooleanField, widgets
from wtforms.validators import DataRequired

# Form para hacer la consulta 1
class Consulta1Form(FlaskForm):
    profesor = SelectField(u'Profesor: ', coerce=int, validators=[DataRequired()])
    todos = BooleanField(u'Todos')
    submit = SubmitField('Consultar')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# Form para hacer la consulta 2
class Consulta2Form(FlaskForm):
    cursos = MultiCheckboxField('Cursos', coerce=int)
    submit = SubmitField("Consultar")

# Form para hacer la consulta 3
class Consulta3Form(FlaskForm):
    semestre = SelectField(u'Semestre: ', coerce=int, validators=[DataRequired()],
                            choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7')])
    todos = BooleanField(u'Todos')
    submit = SubmitField('Consultar')


    