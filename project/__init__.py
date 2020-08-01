import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Creación de app
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

# Configuración de la BD
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set de la base de datos
db = SQLAlchemy(app)
Migrate(app,db)

from project.profesores.views import profesores_blueprint
from project.cursos.views import cursos_blueprint
from project.aulas.views import aulas_blueprint
from project.consultas.views import consultas_blueprint

app.register_blueprint(profesores_blueprint, url_prefix="/profesores")
app.register_blueprint(cursos_blueprint, url_prefix="/cursos")
app.register_blueprint(aulas_blueprint, url_prefix="/aulas")
app.register_blueprint(consultas_blueprint, url_prefix="/consultas")