from flask import render_template
from project import app
from project.profesores.model import Profesor
from project.cursos.model import Curso
from project.aulas.model import Aula

# Renderiza el index de la página
@app.route('/')
def index():
    profes = Profesor.query.all()
    cursos = Curso.query.all()
    aulas = Aula.query.all()
    return render_template('home.html', profes=profes, cursos=cursos, aulas=aulas)

# Método main
if __name__ == "__main__":
    app.run(debug=True)

