from flask import Blueprint, render_template, flash
from project import db
from project.cursos.forms import CreateCursoForm, UpdateCursoForm, DeleteCursoForm
from project.cursos.model import Curso

cursos_blueprint = Blueprint('cursos',
                                __name__, 
                                template_folder='templates/cursos')

# HomePage del módulo Cursos
@cursos_blueprint.route('/home')
def home():
    cursos = Curso.query.all()
    return render_template('cursos_home.html', cursos=cursos)    

# Crear nuevo curso del módulo
@cursos_blueprint.route('/create', methods=['GET','POST'])
def create():
    form = CreateCursoForm()

    if form.validate_on_submit():
        nombre = form.nombre.data
        tipo = form.tipo.data
        creditos = form.creditos.data
        semestre = form.semestre.data
        lecciones = form.lecciones.data

        try_curso = Curso.query.filter_by(_nombre=nombre).first()

        if try_curso == None:
            newCurso = Curso(nombre, tipo, creditos, semestre, lecciones)
            db.session.add(newCurso)
            db.session.commit()
            flash(u'Curso creado correctamente','success')
            form = CreateCursoForm(formdata=None)
        else:
            flash(u'Ese curso ya está registrado','error')
        
    return render_template('cursos_create.html', form=form) 

# Actualizar curso del módulo
@cursos_blueprint.route('/update', methods=['GET','POST'])
def update():
    form = UpdateCursoForm()
    curso_list = db.session.query(Curso).all()
    curso_choices = [(i.getId(), i.getNombre()) for i in curso_list]

    form.curso.choices = curso_choices
    if form.validate_on_submit():
        id = int(form.curso.data)
        nombre = form.nombre.data
        tipo = form.tipo.data
        creditos = form.creditos.data
        semestre = form.semestre.data
        lecciones = form.lecciones.data

        exists = Curso.query.filter_by(_nombre=nombre).first()
        current_curso = Curso.query.get(id)

        if exists != None:
            if exists.getNombre() != current_curso.getNombre():
                flash(u'Ese nombre ya está registrado','error')
            else:
                current_curso.setNombre(nombre)
                current_curso.setCreditos(creditos)
                current_curso.setTipo(tipo)
                current_curso.setSemestre(semestre)
                current_curso.setLecciones(lecciones)

                db.session.add(current_curso)
                db.session.commit()
                flash(u'Curso actualizado correctamente','success')
                form = UpdateCursoForm(formdata=None)

                curso_list = db.session.query(Curso).all()
                curso_choices = [(i.getId(), i.getNombre()) for i in curso_list]
                form.curso.choices = curso_choices
        else:
            current_curso.setNombre(nombre)
            current_curso.setCreditos(creditos)
            current_curso.setTipo(tipo)
            current_curso.setSemestre(semestre)
            current_curso.setLecciones(lecciones)

            db.session.add(current_curso)
            db.session.commit()
            flash(u'Curso actualizado correctamente','success')
            form = UpdateCursoForm(formdata=None)

            curso_list = db.session.query(Curso).all()
            curso_choices = [(i.getId(), i.getNombre()) for i in curso_list]
            form.curso.choices = curso_choices
        
    return render_template('cursos_update.html', form=form) 

# Eliminar curso del módulo
@cursos_blueprint.route('/delete', methods=['GET','POST'])
def delete():
    form = DeleteCursoForm()
    curso_list = db.session.query(Curso).all()
    curso_choices = [(i.getId(), i.getNombre()) for i in curso_list]

    form.curso.choices = curso_choices
    if form.validate_on_submit():
        id = int(form.curso.data)

        curso = Curso.query.get(id)
        db.session.delete(curso)
        db.session.commit()
        flash(u'Curso eliminado correctamente')

        curso_list = db.session.query(Curso).all()
        curso_choices = [(i.getId(), i.getNombre()) for i in curso_list]
        form.curso.choices = curso_choices

    return render_template('cursos_delete.html', form=form)