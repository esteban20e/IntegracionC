from flask_marshmallow import Marshmallow
from flask import Blueprint
from utils.db import db
from sqlalchemy import inspect,Column, Integer, String, ForeignKey,Time
from sqlalchemy.orm import relationship

ma = Marshmallow()

triggerEstrategia = Blueprint('triggerEstrategia',__name__) 

class TriggerEstrategia(db.Model):
    __tablename__ = 'triggerEstrategia'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('usuarios.id'))  
    userCuenta = db.Column(db.String(120), nullable=False)
    passwordCuenta = db.Column(db.LargeBinary(128), nullable=False)
    accountCuenta = db.Column(db.String(500), nullable=True)
    horaInicio = db.Column(db.Time)  # Nuevo atributo de tiempo
    horaFin = db.Column(db.Time)  # Nuevo atributo de tiempo
    ManualAutomatico = db.Column(db.String(500), nullable=False)
    nombreEstrategia = db.Column(db.String(500), nullable=False)
    
    
    usuarios = relationship("Usuario", back_populates="triggerEstrategia")
    
 # constructor
    def __init__(self, id,user_id,userCuenta,passwordCuenta,accountCuenta,horaInicio,horaFin,ManualAutomatico,nombreEstrategia):
        self.id = id
        self.user_id = user_id
        self.userCuenta = userCuenta
        self.passwordCuenta = passwordCuenta
        self.accountCuenta = accountCuenta
        self.horaInicio = horaInicio
        self.horaFin = horaFin
        self.ManualAutomatico = ManualAutomatico
        self.nombreEstrategia = nombreEstrategia
   

    @classmethod
    def crear_tabla_triggerEstrategia(self):
         insp = inspect(db.engine)
         if not insp.has_table("triggerEstrategia"):
              db.create_all()
             
    
        
class MerShema(ma.Schema):
    class Meta:
        fields = ("id", "user_id" ,"userCuenta","passwordCuenta","accountCuenta","horaInicio","horaFin" ,"ManualAutomatico","nombreEstrategia")

mer_schema = MerShema()
mer_shema = MerShema(many=True)