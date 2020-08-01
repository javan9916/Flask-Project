from flask import Blueprint, render_template, flash
from flask.json import jsonify
from project import db
from project.profesores.forms import (CreateProfesorForm, UpdateProfesorForm, 
                                    DeleteProfesorForm, DisponibilidadProfesorForm, 
                                    ConexionCursoForm, DeleteCursoForm)
from project.profesores.model import Disponibilidad, Profesor, Proxy
from project.profesores.facade import Facade
from project.cursos.model import Curso
from project.associations import profesores_cursos

profesores_blueprint = Blueprint('profesores',
                                __name__, 
                                template_folder='templates/profesores')

# HomePage del módulo Profesores
@profesores_blueprint.route('/home')
def home():
    profes = Profesor.query.all()
    return render_template('profesores_home.html', profes=profes)                               

# Crear un nuevo profesor del módulo
@profesores_blueprint.route('/create', methods=['GET','POST'])
def create():
    facade = Facade()
    form = CreateProfesorForm()

    if form.validate_on_submit():
        name = form.nombre.data
        ced = form.cedula.data

        if facade.checkCed(str(ced)) and facade.checkName(name): 
            try_profe = Profesor.query.filter_by(_cedula=ced).first()

            if try_profe == None:
                newProfesor = Profesor(ced, name)
                db.session.add(newProfesor)
                db.session.commit()
                flash(u'Profesor creado correctamente','success')
                form = CreateProfesorForm(formdata=None)
            else:
                flash(u'Ese profesor ya está registrado','error')

        else:
            flash(u'Los datos deben tener el formato válido','error')
        
    return render_template('profesores_create.html', form=form)

# Actualizar un profesor del módulo
@profesores_blueprint.route('/update', methods=['GET','POST'])
def update():
    facade = Facade()
    form = UpdateProfesorForm()
    profe_list = db.session.query(Profesor).all()
    profe_choices = [(i.getCedula(), i.getNombre()) for i in profe_list]

    form.cedula.choices = profe_choices
    if form.validate_on_submit():
        ced = int(form.cedula.data)
        name = form.nombre.data

        if facade.checkName(name):
            profe = Profesor.query.filter_by(_cedula=ced).first()
            profeProxy = Proxy(profe)
            profeProxy.setNombre(name)
            db.session.add(profe)
            db.session.commit()
            flash(u'Profesor actualizado correctamente','success')

            form.nombre.data = ""
            profe_list = db.session.query(Profesor).all()
            profe_choices = [(i.getCedula(), i.getNombre()) for i in profe_list]
            form.cedula.choices = profe_choices
        else: 
            flash(u'Profesor actualizado correctamente','error')

    return render_template('profesores_update.html', form=form)

# Eliminar un profesor del módulo
@profesores_blueprint.route('/delete', methods=['GET','POST'])
def delete():
    form = DeleteProfesorForm()
    profe_list = db.session.query(Profesor).all()
    profe_choices = [(i.getCedula(), i.getNombre()) for i in profe_list]

    form.cedula.choices = profe_choices
    if form.validate_on_submit():
        ced = int(form.cedula.data)
    
        profe = Profesor.query.filter_by(_cedula=ced).first()
        db.session.delete(profe)
        db.session.commit()
        flash(u'Profesor eliminado correctamente')

        profe_list = db.session.query(Profesor).all()
        profe_choices = [(i.getCedula(), i.getNombre()) for i in profe_list]
        form.cedula.choices = profe_choices

    return render_template('profesores_delete.html', form=form)

# Registrar la disponibilidad de un profesor
@profesores_blueprint.route('/disponibilidad', methods=['GET','POST'])
def disponibilidad():
    form = DisponibilidadProfesorForm()
    profe_list = db.session.query(Profesor).all()
    profe_choices = [(i.getCedula(), i.getNombre()) for i in profe_list]

    form.cedula.choices = profe_choices
    if form.validate_on_submit():
        ced = int(form.cedula.data)
        l = lunes(form)
        x = martes(form)
        m = miercoles(form)
        j = jueves(form)
        v = viernes(form)
        days = [l,x,m,j,v]

        profe = Profesor.query.filter_by(_cedula=ced).first()
        profeProxy = Proxy(profe)
        disponibilidad = Disponibilidad(_profesor=profe)
        profeProxy.setDisponibilidad(days, disponibilidad)
        flash(u'Disponibilidad registrada correctamente')

    return render_template('disponibilidad.html', form=form)

# Registrar los cursos de un profesor
@profesores_blueprint.route('/curso', methods=['GET','POST'])
def create_curso():
    form = ConexionCursoForm()
    profe_list = db.session.query(Profesor).all()
    profe_choices = [(i.getCedula(), i.getNombre()) for i in profe_list]

    curso_list = db.session.query(Curso).all()
    curso_choices = [(i.getId(), i.getNombre()) for i in curso_list]

    form.cedula.choices = profe_choices
    form.curso.choices = curso_choices

    if form.validate_on_submit():
        profesor = int(form.cedula.data)
        curso = int(form.curso.data)

        current_profe = Profesor.query.filter_by(_cedula=profesor).first()
        current_curso = Curso.query.get(curso)

        if checkExistence(current_profe, current_curso) == []:
            profeProxy = Proxy(current_profe)

            profeProxy.addCurso(current_curso)
            db.session.add(current_profe)
            db.session.commit()
            flash(u'Curso registrado correctamente','success')
            
            profe_list = db.session.query(Profesor).all()
            profe_choices = [(i.getCedula(), i.getNombre()) for i in profe_list]
            curso_list = db.session.query(Curso).all()
            curso_choices = [(i.getId(), i.getNombre()) for i in curso_list]
            form.cedula.choices = profe_choices
            form.curso.choices = curso_choices
        else:
            flash(u'El profesor ya tiene registrado ese curso','error')

    return render_template('profesores_create_curso.html', form=form)

# Registrar los cursos de un profesor
@profesores_blueprint.route('/delete_curso', methods=['GET','POST'])
def delete_curso():
    form = DeleteCursoForm()
    profe_list = db.session.query(Profesor).all()
    profe_choices = [(i.getCedula(), i.getNombre()) for i in profe_list]

    cursos = db.session.query(Curso).all()
    #filtered_list = Curso.query.join(profesores_cursos).join(Profesor).filter(profesores_cursos.c._profesor_id == profe_list[0].getId()).all()
    filtered_choices = [(i.getId(), i.getNombre()) for i in cursos]

    form.cedula.choices = profe_choices
    form.curso.choices = filtered_choices

    if form.validate_on_submit():
        profesor = int(form.cedula.data)
        curso = int(form.curso.data)

        current_profe = Profesor.query.filter_by(_cedula=profesor).first()
        current_curso = Curso.query.get(curso)

        if not(checkExistence(current_profe, current_curso) == []):
            profeProxy = Proxy(current_profe)
            
            profeProxy.deleteCurso(current_curso)
            db.session.add(current_profe)
            db.session.commit()
            flash(u'Curso eliminado correctamente','success')

            profe_list = db.session.query(Profesor).all()
            profe_choices = [(i.getCedula(), i.getNombre()) for i in profe_list]
            cursos = db.session.query(Curso).all()
            #filtered_list = Curso.query.join(profesores_cursos).join(Profesor).filter(profesores_cursos.c._profesor_id == profe_list[0].getId()).all()
            filtered_choices = [(i.getId(), i.getNombre()) for i in cursos]
            form.cedula.choices = profe_choices
            form.curso.choices = filtered_choices

        else:
            flash(u'El profesor no tiene registrado ese curso','error')

    return render_template('profesores_delete_curso.html', form=form)

# Obtener los cursos de un profesor dado
@profesores_blueprint.route('/<ced>')
def getCursos(ced):
    profe = Profesor.query.filter_by(_cedula=ced).first()
    cursos = Curso.query.join(profesores_cursos).join(Profesor).filter(profesores_cursos.c._profesor_id == profe.getId()).all()

    cursoArray = []

    for curso in cursos:
       cursoObj = {}
       cursoObj['id'] = curso.getId()
       cursoObj['nombre'] = curso.getNombre()
       cursoArray.append(cursoObj)

    return jsonify({'cursos': cursoArray})

# Valida la existencia de la relación de un profesor con un curso
def checkExistence(profe, curso):
    exists = Curso.query.join(profesores_cursos).join(Profesor).filter((profesores_cursos.c._profesor_id == profe.getId()) & (profesores_cursos.c._curso_id == curso.getId())).all()
    return exists

#---------------------------------------------------------------------------------
# Transforma los datos ingresados de disponibilidad en forma de horas en la BD
def lunes(form):
    day_list = []
    if (form.l1.data): 
        day_list.append('7:55-8:45')
    if (form.l2.data):
        day_list.append('8:50-9:40')
    if (form.l3.data):
        day_list.append('9:45-10:35')
    if (form.l4.data):
        day_list.append('10:40-11:30')
    if (form.l5.data):
        day_list.append('12:30-1:20')
    if (form.l6.data):
        day_list.append('1:25-2:15')
    if (form.l7.data):
        day_list.append('2:20-3:10')
    if (form.l8.data):
        day_list.append('3:15-4:05')
    return day_list

def martes(form):
    day_list = []
    if (form.x1.data): 
        day_list.append('7:55-8:45')
    if (form.x2.data):
        day_list.append('8:50-9:40')
    if (form.x3.data):
        day_list.append('9:45-10:35')
    if (form.x4.data):
        day_list.append('10:40-11:30')
    if (form.x5.data):
        day_list.append('12:30-1:20')
    if (form.x6.data):
        day_list.append('1:25-2:15')
    if (form.x7.data):
        day_list.append('2:20-3:10')
    if (form.x8.data):
        day_list.append('3:15-4:05')
    return day_list

def miercoles(form):
    day_list = []
    if (form.m1.data): 
        day_list.append('7:55-8:45')
    if (form.m2.data):
        day_list.append('8:50-9:40')
    if (form.m3.data):
        day_list.append('9:45-10:35')
    if (form.m4.data):
        day_list.append('10:40-11:30')
    if (form.m5.data):
        day_list.append('12:30-1:20')
    if (form.m6.data):
        day_list.append('1:25-2:15')
    if (form.m7.data):
        day_list.append('2:20-3:10')
    if (form.m8.data):
        day_list.append('3:15-4:05')
    return day_list

def jueves(form):
    day_list = []
    if (form.j1.data): 
        day_list.append('7:55-8:45')
    if (form.j2.data):
        day_list.append('8:50-9:40')
    if (form.j3.data):
        day_list.append('9:45-10:35')
    if (form.j4.data):
        day_list.append('10:40-11:30')
    if (form.j5.data):
        day_list.append('12:30-1:20')
    if (form.j6.data):
        day_list.append('1:25-2:15')
    if (form.j7.data):
        day_list.append('2:20-3:10')
    if (form.j8.data):
        day_list.append('3:15-4:05')
    return day_list

def viernes(form):
    day_list = []
    if (form.v1.data): 
        day_list.append('7:55-8:45')
    if (form.v2.data):
        day_list.append('8:50-9:40')
    if (form.v3.data):
        day_list.append('9:45-10:35')
    if (form.v4.data):
        day_list.append('10:40-11:30')
    if (form.v5.data):
        day_list.append('12:30-1:20')
    if (form.v6.data):
        day_list.append('1:25-2:15')
    if (form.v7.data):
        day_list.append('2:20-3:10')
    if (form.v8.data):
        day_list.append('3:15-4:05')
    return day_list
#---------------------------------------------------------------------------------