% -------------------------------------------------------------------------------

% Anade un elemento al final de una lista.
%
add_tail(X,[],[X]).
add_tail(X,[H|T],[H|L]):-add_tail(X,T,L).

% Devuelve una lista de profesores que dan un curso dado o los cursos
% que da un profesor dado.
%
curso_profesor(P,C):- profesor(_,P,X,_), X =.. [_|T], member(C,T).

% -------------------------------------------------------------------------------
% Asocia al profesor dado con los cursos a partir de la disponibilidad
% de horario de este y los cursos que imparte.
consulta1_profe(P,R):-
    curso(C,Curso,_,_,_,_),
    curso_profesor(P,C),
    consulta_disp(P,C,Res),
    profesor(nombre(PName,_),P,_,_),
    append([PName],[Curso],X),
    append([X],[Res],R).

% Asocia los profesores con los cursos a partir de disponibilidad de
% horario de los profesores y los cursos que imparten.
%
consulta1(R):-
    curso(C,Curso,_,_,_,_),
    curso_profesor(P,C),
    consulta_disp(P,C,Res),
    profesor(nombre(PName,_),P,_,_),
    append([PName],[Curso],X),
    append([X],[Res],R).

% Toma el id del curso dado y saca el bloque de este, luego dependiendo
% del tamano del bloque llama a find_in_day con el Profesor, Bloque y R
% para el resultado.
%
consulta_disp(P,C,R):-
    curso(C,_,_,_,_,L),
    (   L is 4 -> find_in_day4(P,L,R)
    ;   L is 2 -> find_in_day2(P,L,R)).

% Toma el dia correspondiente y luego llama a find_in_hour con el
% Profesor, Bloque, Hora y el Dia.
%
find_in_day2(P,L,R):-
    dia(D,Dia),
    find_in_hour2(P,L,H,D),
    append([Dia],[H],X),
    hora(ID,H,_), NewID is ID+1,
    hora(NewID,_,F),
    append(X,[F],R).

% Toma el dia correspondiente y luego llama a find_in_hour con el
% Profesor, Bloque, Hora y el Dia.
%
find_in_day4(P,L,R):-
    dia(D,Dia),
    find_in_hour4(P,L,H,D),
    append([Dia],[H],X),
    hora(ID,H,_), NewID is ID+3,
    hora(NewID,_,F),
    append(X,[F],R).

% Toma la hora del bloque correspondiente, llama a verify_curso_bloque
% luego a hour_disp.
%
find_in_hour2(P,L,R,D):-
    leccion(L,H),
    verify_curso_leccion2(P,D,H),
    hour_disp2(H,R).

% Toma la hora del bloque correspondiente, llama a verify_curso_bloque
% luego a hour_disp.
%
find_in_hour4(P,L,R,D):-
    leccion(L,H),
    verify_curso_leccion4(P,D,H),
    hour_disp4(H,R).

% Dependiendo del id de la hora devuelve la hora correspondiente.
%
hour_disp4(H,R):-
    H==1, hora(1,R,_);
    H==5, hora(5,R,_).

% Dependiendo del id de la hora devuelve la hora correspondiente.
%
hour_disp2(H,R):-
    H==1, hora(1,R,_);
    H==3, hora(3,R,_);
    H==5, hora(5,R,_);
    H==7, hora(7,R,_).

% Verifica que la hora dada se encuentre dentro de la disponibilidad del
% profesor.
%
verify_curso_leccion2(P,D,H):-
    profesor(_,P,_,Disp), Disp =.. [_|X],
    (   member(dia_disp(D,H,_,_,_),X);
    member(dia_disp(D,_,_,H,_),X);
    member(dia_disp(D,H,_,_,_,_,_,_,_),X);
    member(dia_disp(D,_,_,H,_,_,_,_,_),X);
    member(dia_disp(D,_,_,_,_,H,_,_,_),X);
    member(dia_disp(D,_,_,_,_,_,_,H,_),X)).

% Verifica que la hora dada se encuentre dentro de la disponibilidad del
% profesor.
%
verify_curso_leccion4(P,D,H):-
    profesor(_,P,_,Disp), Disp =.. [_|X],
    (   member(dia_disp(D,H,_,_,_),X) ;
    member(dia_disp(D,H,_,_,_,_,_,_,_),X);
    member(dia_disp(D,_,_,_,_,H,_,_,_),X)).

% -------------------------------------------------------------------------------

% Consulta todos los horarios posibles sin choques, dada una lista de
% cursos.
%
consulta2(Cursos,R):-
    length(Cursos,L),
    (   L < 11 -> Fin is L+1,
    week(1,Fin,Cursos,[],[],R,_,_)
    ;   write('Ha ingresado muchos cursos...')).

% Condicion de parada para dar una respuesta, cuando llega al final de
% todos los cursos que se deben insertar.
%
week(Fin,Fin,_,_,List,R,_,_):- reverse(List,R).

% Busca todas las condiciones posibles si la hora es la correcta para el
% curso y la hora aun no esta registrada, guarda las respuestas en list
% y aumenta el inicio para que avance.
%
week(Ini,Fin,[Curso|Cursos],Lecciones,List,R,NLess,NL):-
    dia(Dia,_),
    hora(Hora,_,_),
    dia_hora(Curso,Hora),
    not(verify_dia_hora(Dia,Hora,Lecciones)),
    curso(Curso,_,_,_,_,L),
    add_to_list(Curso,Dia,Hora,L,List,NL),
    (L is 4 ->
    add_to_lecciones(Dia,Hora,Lecciones,NewL), add_another_lecciones(Dia,Hora,NewL,NLess);
    add_to_lecciones(Dia,Hora,Lecciones,NLess)),
    NewIni is Ini+1,
    (   add_rest(Curso,Cursos,NC) ->
    NewFin is Fin+1, week(NewIni,NewFin,NC,NLess,NL,R,_,_)

    ;  week(NewIni,Fin,Cursos,NLess,NL,R,_,_)).

% Busca los cursos restantes de 2 lecciones
%
add_rest(Curso,Cursos,NC):-
    (   Curso is 1 -> add_tail(23,Cursos,NC)
    ;   Curso is 2 -> add_tail(24,Cursos,NC)
    ;   Curso is 3 -> add_tail(25,Cursos,NC)
    ;   Curso is 5 -> add_tail(26,Cursos,NC)
    ;   Curso is 11 -> add_tail(27,Cursos,NC)
    ;   Curso is 12 -> add_tail(28,Cursos,NC)
    ;   Curso is 14 -> add_tail(29,Cursos,NC)
    ;   Curso is 16 -> add_tail(30,Cursos,NC)
    ;   Curso is 21 -> add_tail(31,Cursos,NC)).


% Anade un curso, dia, hora a la lista de respuestas.
%
add_to_list(Curso,Dia,Hora,Leccion,List,NL):-
    dia(Dia,DName),
    curso(Curso,CName,_,_,_,B),
    hora(Hora,HIni,_),
    (   Leccion is 4 -> NewH is Hora+3, hora(NewH,_,HFin)
    ;   NewH is Hora+1, hora(NewH,_,HFin)),
    append([horario(CName,B,DName,HIni,HFin)],List,NL).

% Anade un nuevo bloque a la lista de bloques, los cuales contienen un
% dia y una hora registrados.
%
add_to_lecciones(Dia,Hora,Lecciones,NLess):-
    append([lesson(Dia,Hora)],Lecciones,NLess).

% Cuando B es 4 anade un segundo bloque para que los cursos que se
% imparten en 2 lecciones no se metan en medio.
%
add_another_lecciones(Dia,Hora,Lecciones,NLess):-
    Hora is 1 ->
    append([lesson(Dia,3)],Lecciones,NLess)
    ;
    append([lesson(Dia,7)],Lecciones,NLess).

% Verifica que una hora dada se encuentre incluido en las horas
% posibles de un Curso.
%
dia_hora(Curso, Hora):-
    curso(Curso,_,_,_,_,L),
    findall(H, leccion(L,H),Horas),
    member(Hora, Horas).

% Verifica que el dia y la hora aun no esten en la lista de bloques
% implementados.
%
verify_dia_hora(Dia,Hora,Lecciones):-
    member(lesson(Dia,Hora),Lecciones).

% -------------------------------------------------------------------------------

% Consulta todos los horarios posibles de todos los semestres juntos sin
% choques tomando en cuenta cursos, aulas y profesores
%
consulta3(R):-
    findall(S, semestre(S,_), Semestres),
    length(Semestres,L),
    Fin is L+1,
    find_semestre_comb(1,Fin,Semestres,[],[],[],R,_,_,_).

% Retorna la lista de respuestas de los horarios cuando la lista de
% semestres llega a su fin.
%
find_semestre_comb(Fin,Fin,_,List,_,_,R,_,_,_):- reverse(List,R).

% Combina los semestres con sus respectivos resultados individuales
% tomando en cuenta que Aulas y Profesores esten libres en la hora y dia
% que se les va a asignar.
%
find_semestre_comb(Ini,Fin,[Semestre|Semestres],List,Aulas,Profes,R,NL,NA,NP):-
    get_semestre(Semestre,Horario,Aulas,Profes,A,P),
    append(Horario,List,NL),
    append(A,Aulas,NA),
    append(P,Profes,NP),
    NewIni is Ini+1,
    find_semestre_comb(NewIni,Fin,Semestres,NL,NA,NP,R,_,_,_).

% Obtiene los resultados de un semestre en especifico tomando los
% cursos de ese semestre.
%
get_semestre(Semestre,R,Aulas,Profes,RA,RP):-
    semestre(Semestre,CursosEst),
    CursosEst =.. [_|Cursos],
    length(Cursos,L),
    Fin is L+1,
    find_combination(1,Fin,Cursos,[],Aulas,Profes,R,_,_,_,RA,RP).

% Consulta las combinaciones de los cursos, aulas y profesores sin
% choques del semestre dado.
%
consulta3_semestre(Semestre,R):-
    semestre(Semestre,CursosEst),
    CursosEst =.. [_|Cursos],
    length(Cursos,L),
    Fin is L+1,
    find_combination(1,Fin,Cursos,[],[],[],R,_,_,_,_,_).

% Devuelve las lista de tanto de los horarios de ese
% semestre como de la disponibilidad de aulas y profesores cuando la
% lista de cursos de ese semestre llega a su fin.
%
find_combination(Fin,Fin,_,List,Aulas,Profes,R,_,_,_,RA,RP):-
    reverse(List,R),
    reverse(Aulas,RA),
    reverse(Profes,RP).

% Encuentra las combinaciones de cursos de un semestre en especifico
% tomando en cuenta la disponibilidad de aulas y profesores ya
% insertados en la respuesta.
%
find_combination(Ini,Fin,[Curso|Cursos],List,Aulas,Profes,R,NL,NA,NP,RA,RP):-
    curso(Curso,_,TipoAula,_,_,_),
    aula(Aula,_,_,TipoAula),
    curso_profesor(Profesor,Curso),
    consulta_disp(Profesor,Curso,Horario),
    get_dia_hora(Horario,Dia,Hora),
    not(verify_profe_hora(Profesor,Dia,Hora,Profes)),
    add_to_profes(Profesor,Dia,Hora,Profes,NP),
    not(verify_aula_hora(Aula,Dia,Hora,Aulas)),
    add_to_aulas(Aula,Dia,Hora,Aulas,NA),
    add_to_res(Curso,Profesor,Aula,Horario,List,NL),
    NewIni is Ini+1,
    find_combination(NewIni,Fin,Cursos,NL,NA,NP,R,_,_,_,RA,RP).

% Anade un nuevo elemento a la respuesta de la consulta.
%
add_to_res(Curso,Profesor,Aula,Horario,List,NL):-
    curso(Curso,CName,_,_,_,_),
    profesor(nombre(PName,_),Profesor,_,_),
    aula(Aula,AName,_,_),
    nth0(0,Horario,Dia),nth0(1,Horario,Hora),nth0(2,Horario,Fin),
    append([horario(CName,PName,AName,Dia,Hora,Fin)],List,NL).

% Anade un nuevo elemento a la lista de aulas ocupadas.
%
add_to_aulas(Aula,Dia,Hora,Aulas,NA):-
    append([aula_hora(Aula,Dia,Hora)],Aulas,NA).

% Verifica que un aula tenga disponibilidad de la hora y dia que se le
% solicitan.
%
verify_aula_hora(Aula,Dia,Hora,Aulas):-
    member(aula_hora(Aula,Dia,Hora),Aulas).

% Anade un nuevo elemento a la lista de profesores ocupados.
add_to_profes(Profesor,Dia,Hora,Profes,NP):-
    append([profe_hora(Profesor,Dia,Hora)],Profes,NP).

% Verifica que un profesor tenga disponibilidad a la hora y dia que se
% le solicitan.
%
verify_profe_hora(Profesor,Dia,Hora,Profes):-
    member(profe_hora(Profesor,Dia,Hora),Profes).

% Obtiene el dia y la hora de inicio de un horario dado.
%
get_dia_hora(Horario,Dia,Hora):-
    nth0(0,Horario,Dia), nth0(1,Horario,Hora).
