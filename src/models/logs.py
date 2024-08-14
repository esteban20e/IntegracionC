from flask_marshmallow import Marshmallow
from flask import Blueprint
from utils.db import db
from sqlalchemy import inspect, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

ma = Marshmallow()

logs = Blueprint('logs', __name__) 

class Logs(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('usuarios.id'))
    userCuenta = db.Column(db.String(120)) 
    accountCuenta = db.Column(db.String(120))    
    fecha_log = db.Column(db.DateTime)  # Corregido a DateTime
    ip = db.Column(db.String(120))   
    funcion = db.Column(db.String(120))   
    archivo = db.Column(db.String(120))   
    linea = db.Column(db.Integer) 
    error = db.Column(db.String(120))   
    
    usuarios = relationship("Usuario", back_populates="logs")

    def __init__(self, user_id, userCuenta, accountCuenta, fecha_log, ip, funcion, archivo, linea, error):
        self.user_id = user_id
        self.userCuenta = userCuenta
        self.accountCuenta = accountCuenta
        self.fecha_log = fecha_log
        self.ip = ip
        self.funcion = funcion
        self.archivo = archivo
        self.linea = linea
        self.error = error
    @classmethod
    def crear_tabla_logs(self):
        insp = inspect(db.engine)
        if not insp.has_table("logs"):
            db.create_all()

class MerShema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "userCuenta", "accountCuenta", "fecha_log", "ip", "funcion", "archivo", "linea", "error")

mer_schema = MerShema()
mer_shema = MerShema(many=True)
