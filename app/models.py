from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), nullable=False)

    citas_creadas = db.relationship('Cita', foreign_keys='Cita.usuario_id', backref='creador', lazy=True)
    citas_asignadas = db.relationship('Cita', foreign_keys='Cita.agente_id', backref='asignado', lazy=True)


class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    proyecto = db.Column(db.String(100), nullable=False)
    consulta = db.Column(db.String(200), nullable=False)
    estado = db.Column(db.String(50), default='pendiente')
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime, nullable=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    agente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    usuario = db.relationship('Usuario', foreign_keys=[usuario_id])
    agente = db.relationship('Usuario', foreign_keys=[agente_id])
