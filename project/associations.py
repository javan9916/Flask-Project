from project import db

# Tabla de asociación profesores_cursos que mantiene la relación many-to-many
profesores_cursos = db.Table('profesores_cursos', db.metadata,
    db.Column('_profesor_id', db.Integer, db.ForeignKey('profesores._id')),
    db.Column('_curso_id', db.Integer, db.ForeignKey('cursos._id'))
)
