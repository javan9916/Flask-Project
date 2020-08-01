from flask import Blueprint, render_template, flash
from project import db
from project.profesores.model import Profesor, Disponibilidad, Dia, Hora
from project.cursos.model import Curso
from project.aulas.model import AulaDaoImpl
from project.associations import profesores_cursos
from project.consultas.forms import Consulta1Form, Consulta2Form, Consulta3Form
from project.consultas.prolog import PrologMT
from pyswip import Functor, Atom

consultas_blueprint = Blueprint('consultas',
                                __name__, 
                                template_folder='templates/consultas')

# Renderiza la página para hacer la consulta 1
@consultas_blueprint.route('/consulta1', methods=['GET','POST'])
def consulta1():
    prolog = PrologMT()
    form = Consulta1Form()
    ced_list = db.session.query(Profesor).all()
    ced_choices = [(i.getCedula(), i.getNombre()) for i in ced_list]
    form.profesor.choices = ced_choices

    formatted_res = []

    if form.validate_on_submit and form.profesor.data != None:
        cursos = db.session.query(Curso).all()
        prolog.consult('consultas.pl')

        assertCursos(prolog, cursos)
        assertDias(prolog)
        assertHoras(prolog)
        assertLecciones(prolog)

        if form.todos.data:
            profes = db.session.query(Profesor).all()
            assertProfesores(prolog, profes)
            resultados = []

            for valor in prolog.query("consulta1(X)"):
                res = valor['X']
                resultados.append(format_atom(res))
                
        else: 
            ced = form.profesor.data
            profe = Profesor.query.filter_by(_cedula=ced).first()
            resultados = []
            
            assertProfesor(prolog, profe)

            for valor in prolog.query("consulta1_profe("+str(ced)+",X)"):
                res = valor['X']
                resultados.append(format_atom(res))

        formatted_res = formatRes(resultados)

        prolog.retractall("curso(_,_,_,_,_,_)")
        prolog.retractall("dia(_,_)")
        prolog.retractall("hora(_,_,_)")
        prolog.retractall("leccion(_,_)")
        prolog.retractall("profesor(_,_,_,_)")

        flash(u'Consulta realizada correctamente')

    return render_template('consulta1.html', form=form, resultados=formatted_res)

# Renderiza la página para hacer la consulta 2
@consultas_blueprint.route('/consulta2', methods=['GET','POST'])
def consulta2():
    prolog = PrologMT()
    form = Consulta2Form()
    course_list = db.session.query(Curso).all()
    form.cursos.choices = [(i.getId(), i.getNombre()) for i in course_list]

    formatted_res = []
    horarios = []

    if form.validate_on_submit and form.cursos.data != None:
        cursochoices = form.cursos.data
        if not(len(cursochoices) > 10):
            choices = stringThis(cursochoices)

            prolog.consult('consultas.pl')

            assertCursos(prolog, course_list)
            assertDias(prolog)
            assertHoras(prolog)
            assertLecciones(prolog)

            count = 0
        
            for valor in prolog.query("consulta2("+choices+",X)"):
                if (count <= 1000):
                    res = valor['X']
                    formatted_functor = format_functor(res)
                    formatted_res.append(formatFunctorRes(formatted_functor))
                    count = count+1
                else:
                    break

            horarios = getResults(formatted_res)
        
            prolog.retractall("curso(_,_,_,_,_,_)")
            prolog.retractall("dia(_,_)")
            prolog.retractall("hora(_,_,_)")
            prolog.retractall("leccion(_,_)")

            flash(u'Consulta realizada correctamente', 'success')
        else:
            flash(u'El número de cursos debe ser menor o igual a 10', 'error')

    return render_template('consulta2.html', form=form, horarios=horarios)

# Renderiza la página para hacer la consulta 3
@consultas_blueprint.route('/consulta3', methods=['GET','POST'])
def consulta3():
    prolog = PrologMT()
    form = Consulta3Form()

    formatted_res = []
    horarios = []

    if form.validate_on_submit and form.semestre.data != None:
        cursos = db.session.query(Curso).all()
        profes = db.session.query(Profesor).all()
        requestProvider = AulaDaoImpl()
        aulas = requestProvider.getAulas()
        prolog.consult('consultas.pl')

        assertCursos(prolog, cursos)
        assertDias(prolog)
        assertHoras(prolog)
        assertLecciones(prolog)
        assertSemestres(prolog)
        assertAulas(prolog, aulas)
        assertProfesores(prolog, profes)

        count = 0

        if form.todos.data:
            for valor in prolog.query("consulta3(X)"):
                if count <= 1000:
                    res = valor['X']
                    formatted_functor = format_functor(res)
                    formatted_res.append(formatFunctorRes(formatted_functor))
                    count = count+1
                else:
                    break
        else: 
            semestre = form.semestre.data

            for valor in prolog.query("consulta3_semestre("+str(semestre)+",X)"):
                if count <= 1000:
                    res = valor['X']
                    formatted_functor = format_functor(res)
                    formatted_res.append(formatFunctorRes(formatted_functor))
                    count = count+1
                else:
                    break
                
        horarios = getResults(formatted_res)

        prolog.retractall("curso(_,_,_,_,_,_)")
        prolog.retractall("dia(_,_)")
        prolog.retractall("hora(_,_,_)")
        prolog.retractall("leccion(_,_)")
        prolog.retractall("profesor(_,_,_,_)")
        prolog.retractall("semestre(_,_)")
        prolog.retractall("aula(_,_,_,_)")

        flash(u'Consulta realizada correctamente')

    return render_template('consulta3.html', form=form, horarios=horarios)

# Toma una lista y la transforma en un string con forma de lista
def stringThis(choices):
    strng = "["

    for i in range(len(choices)):
        if i == len(choices)-1:
            strng = strng + str(choices[i]) + "]"
        else:
            strng = strng + str(choices[i]) + ","

    return strng

# Toma una lista y la transforma en un string de las opciones sin corchetes
def tupleThis(lst):
    strng = ""
    for i in range(len(lst)):
        if i == len(lst)-1:
            strng = strng + str(lst[i])
        else:
            strng = strng + str(lst[i]) + ","

    return strng

# Hace el assert en prolog de todos los cursos que hay en la base de datos   
def assertCursos(pl, cursos):
    total_length = len(cursos)

    for curso in cursos:
        id = curso.getId()
        nombre = curso.getNombre().lower()
        tipo = curso.getTipo().lower()
        creditos = curso.getCreditos()
        semestre = curso.getSemestre()
        lecciones = curso.getLecciones()

        pl.assertz("curso("+str(id)+","+nombre+","+tipo+","+str(creditos)+","+str(semestre)+","+str(lecciones)+")")

        if (lecciones == 2):
            total_length = total_length + 1
            new_id = total_length
            pl.assertz("curso("+str(new_id)+","+nombre+","+tipo+","+str(creditos)+","+str(semestre)+","+str(lecciones)+")")
        
# Hace el assert en prolog de todos los días
def assertDias(pl):
    dias = ["lunes","martes","miercoles","jueves","viernes"]
    dias_id = [1,2,3,4,5]

    for i in range(len(dias)):
        dia = dias[i]
        dia_id = dias_id[i]

        pl.assertz("dia("+str(dia_id)+","+dia+")")

# Hace el assert en prolog de todas las horas
def assertHoras(pl):
    hours = ['7:55-8:45','8:50-9:40','9:45-10:35','10:40-11:30','12:30-1:20','1:25-2:15','2:20-3:10','3:15-4:05']
    hours_id = [1,2,3,4,5,6,7,8]

    for i in range(len(hours)):
        splt = hours[i].split('-')
        hour1 = splt[0]
        hour2 = splt[1]
        hour_id = hours_id[i]

        pl.assertz("hora("+str(hour_id)+","+hour1+","+hour2+")")

# Hace el assert en prolog de todas las lecciones
def assertLecciones(pl):
    lecciones = [4,4,2,2,2,2]
    hours = [1,5,1,3,5,7]

    for i in range(len(lecciones)):
        leccion = lecciones[i]
        hour = hours[i]

        pl.assertz("leccion("+str(leccion)+","+str(hour)+")")

# Hace el assert en prolog de todos los semestres
def assertSemestres(pl):
    semestres = [1,2,3,4,5,6,7]

    for semestre in semestres:
        cursos = Curso.query.filter_by(_semestre=semestre).all()
        cursos_id = [i.getId() for i in cursos]
        pl.assertz("semestre("+str(semestre)+",cursos("+tupleThis(cursos_id)+"))")

# Hace el assert en prolog de todas las aulas que hay en la base de datos   
def assertAulas(pl, aulas):
    for aula in aulas:
        id = aula.getId()
        nombre = aula.getNombre().lower()
        capacidad = aula.getCapacidad()
        tipo = aula.getTipo().lower()

        pl.assertz("aula("+str(id)+","+nombre+","+str(capacidad)+","+tipo+")")

# Hace el assert en prolog de todos los profesores que hay en la base de datos   
def assertProfesores(pl, profes):
    for profe in profes:
        assertProfesor(pl, profe)

# Hace el assert en prolog de un solo profesor 
def assertProfesor(pl, profe):
    profe_id = profe.getId()
    disponibilidad = Disponibilidad.query.filter_by(_profesor_id=profe_id).first()
    d_id = disponibilidad.getId()
    dias = Dia.query.filter_by(_disponibilidad_id=d_id).all()
    dias_id = [i.getId() for i in dias]
    
    hours = []

    for dia_id in dias_id:
        dia = Hora.query.filter_by(_dia_id=dia_id).all()
        hours.append(dia)
    
    nombre_completo = profe.getNombre().split()
    nombre = nombre_completo[0].lower()
    apellido = nombre_completo[1].lower()
    cedula = profe.getCedula()
    cursos = Curso.query.join(profesores_cursos).join(Profesor).filter(profesores_cursos.c._profesor_id == profe_id).all()
    cursos_id = [i.getId() for i in cursos]

    dias_disp = []

    for i in range(len(hours)):
        dia = []
        dia.append(i+1)
        hora = hours[i]
        for j in range(len(hora)):
            hora_id = 0
            inicio = hora[j].getHora().split("-")[0]
            if inicio == '7:55':
                hora_id = 1
            elif inicio == '8:50': 
                hora_id = 2
            elif inicio == '9:45':
                hora_id = 3
            elif inicio == '10:40': 
                hora_id = 4
            elif inicio == '12:30':
                hora_id = 5
            elif inicio == '1:25': 
                hora_id = 6
            elif inicio == '2:20':
                hora_id = 7
            elif inicio == '3:15': 
                hora_id = 8
            dia.append(hora_id)
        dias_disp.append(dia)

    profe_cursos = tupleThis(cursos_id)
    lunes = tupleThis(dias_disp[0])
    martes = tupleThis(dias_disp[1])
    miercoles = tupleThis(dias_disp[2])
    jueves = tupleThis(dias_disp[3])
    viernes = tupleThis(dias_disp[4])
            
    pl.assertz("profesor(nombre("+nombre+","+apellido+"),"+str(cedula)+",cursos("+profe_cursos+"),disponibilidad("+
                "dia_disp("+lunes+"),dia_disp("+martes+"),dia_disp("+miercoles+"),dia_disp("+jueves+"),dia_disp("+viernes+")))")

# Desarma el valor retornado por prolog en algo legible, sirve para Functor y Atom          
def format_value(answer):
    output = ""
    if isinstance(answer, list):
        output = "[ " + ", ".join([format_value(val) for val in answer]) + " ]"
    elif isinstance(answer, Functor) and answer.arity == 2:
        output = "{0}{1}{2}".format(answer.args[0], answer.name, answer.args[1])
    elif isinstance(answer, Atom):
        output = answer.value
    else:
        output = "{}".format(answer)

    return output

# Le da formato a un Atom con la función format_value
def format_atom(result):
    if len(result) == 0:
        return "false."

    if len(result) == 1 and len(result[0]) == 0:
        return "true."

    output = ""
    for res in result:
        tmpOutput = []
        for i in range(len(res)):
            tmpOutput.append(format_value(res[i]))
        output += ", ".join(tmpOutput) + ", "
    output = output[:-2] + " "

    return output

# Le da formato a un Functor con la función format_value
def format_functor(result):
    if len(result) == 0:
        return "false."

    if len(result) == 1 and len(result[0]) == 0:
        return "true."

    output = []
    for res in result:
        output.append(format_value(res))

    return output

# Le da formato a un string de resultados dados por un Atom
def formatRes(resultados):
    formatted_res = []
    for res in resultados:
        splitted = res.split(",")
        stripped = [s.strip() for s in splitted]
        capitalized = [s.capitalize() for s in stripped]
        formatted_res.append(capitalized)

    return formatted_res

# Le da formato a un string de resultados dados por un Functor
def formatFunctorRes(resultados):
    formatted_res = []
    words = ['horario',')','(',':']
    for res in resultados:
        txt = replaceWords(words, res)
        splitted = txt.split(",")
        stripped = [s.strip() for s in splitted]
        capitalized = [s.capitalize() for s in stripped]
        capitalized[-4] = ":".join([capitalized[-4],capitalized[-3]])
        capitalized[-2] = ":".join([capitalized[-2],capitalized[-1]])
        formatted_res.append(capitalized)

    return formatted_res

# Le quita las palabras dadas en la lista words a un txt dado
def replaceWords(words, txt):
    for word in words:
        txt = txt.replace(word,"")
    
    return txt
    
# Retorna los elementos en las posiciones de mask de la lista formatted_res para hacer un 
# de datos para mostrar
def getResults(formatted_res):
    res = []
    mask = [0,66,132,198,264,330,396,462,528,594,660,726,792,858,924,990]
    for element in mask:
        res.append(formatted_res[element])

    return res