from flask import Blueprint, render_template, flash
from project import db
from project.aulas.forms import CreateAulaForm, UpdateAulaForm, DeleteAulaForm
from project.aulas.model import Aula, AulaDaoImpl

aulas_blueprint = Blueprint('aulas',
                                __name__, 
                                template_folder='templates/aulas')

# HomePage del módulo Aulas
@aulas_blueprint.route('/home')
def home():
    requestProvider = AulaDaoImpl()
    aulas = requestProvider.getAulas()
    return render_template('aulas_home.html', aulas=aulas)   

# Crear nueva aula del módulo
@aulas_blueprint.route('/create', methods=['GET','POST'])
def create():
    requestProvider = AulaDaoImpl()
    form = CreateAulaForm()

    if form.validate_on_submit():
        nombre = form.nombre.data
        capacidad = form.capacidad.data
        tipo = form.tipo.data

        try_aula = Aula.query.filter_by(_nombre=nombre).first()

        if try_aula == None:
            newAula = Aula(nombre, capacidad, tipo)
            requestProvider.addAula(newAula)
            flash(u'Aula creada correctamente','success')
            form = CreateAulaForm(formdata=None)
        else:
            flash(u'Esa aula ya está registrada','error')
        
    return render_template('aulas_create.html', form=form) 

# Actualizar un aula del módulo
@aulas_blueprint.route('/update', methods=['GET','POST'])
def update():
    requestProvider = AulaDaoImpl()
    form = UpdateAulaForm()
    aula_list = db.session.query(Aula).all()
    aula_choices = [(i.getId(), i.getNombre()) for i in aula_list]

    form.aula.choices = aula_choices
    if form.validate_on_submit():
        id = int(form.aula.data)
        nombre = form.nombre.data
        capacidad = form.capacidad.data
        tipo = form.tipo.data

        exists = Aula.query.filter_by(_nombre=nombre).first()
        current_aula = Aula.query.get(id)

        if exists != None:
            if exists.getNombre() != current_aula.getNombre():
                flash(u'Ese nombre ya está registrado','error')
            else:
                requestProvider.updateAula(current_aula, nombre, capacidad, tipo)
                flash(u'Aula actualizada correctamente','success')
                form = UpdateAulaForm(formdata=None)

                aula_list = db.session.query(Aula).all()
                aula_choices = [(i.getId(), i.getNombre()) for i in aula_list]
                form.aula.choices = aula_choices
        else:
            requestProvider.updateAula(current_aula, nombre, capacidad, tipo)
            flash(u'Aula actualizada correctamente','success')
            form = UpdateAulaForm(formdata=None)

            aula_list = db.session.query(Aula).all()
            aula_choices = [(i.getId(), i.getNombre()) for i in aula_list]
            form.aula.choices = aula_choices
            
    return render_template('aulas_update.html', form=form) 

# Eliminar un aula del módulo
@aulas_blueprint.route('/delete', methods=['GET','POST'])
def delete():
    requestProvider = AulaDaoImpl()
    form = DeleteAulaForm()
    aula_list = db.session.query(Aula).all()
    aula_choices = [(i.getId(), i.getNombre()) for i in aula_list]

    form.aula.choices = aula_choices
    if form.validate_on_submit():
        id = int(form.aula.data)

        aula = Aula.query.get(id)
        requestProvider.deleteAula(aula)
        flash(u'Aula eliminada correctamente')

        aula_list = db.session.query(Aula).all()
        aula_choices = [(i.getId(), i.getNombre()) for i in aula_list]
        form.aula.choices = aula_choices

    return render_template('aulas_delete.html', form=form)