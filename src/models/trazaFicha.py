from flask_marshmallow import Marshmallow
from flask import Blueprint
from utils.db import db
from sqlalchemy import inspect,Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

ma = Marshmallow()

trazaFicha = Blueprint('trazaFicha', __name__)

class TrazaFicha(db.Model):
    __tablename__ = 'trazaFichas'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    idFicha = db.Column(Integer, ForeignKey('ficha.id'))  
    user_id_traspaso = db.Column(Integer, ForeignKey('usuarios.id'))  
    
    cuenta_broker_id_traspaso = db.Column(Integer, ForeignKey('cuentas.id'))  
    fecha_traspaso = db.Column(DateTime)
    fecha_habilitacion = db.Column(DateTime)
    fecha_denuncia = db.Column(DateTime)
    fecha_baja = db.Column(DateTime)
    user_id_denuncia = db.Column(Integer)
    user_id_alta = db.Column(Integer)
    user_id_baja = db.Column(Integer)
    estado_traza = db.Column(String(500), nullable=True)
    token = db.Column(String(500), nullable=True)
    
    ficha = relationship('Ficha', back_populates='trazaFichas')    
    usuario = relationship('Usuario', back_populates='trazaFichas')  
    cuentas = relationship("Cuenta", back_populates="trazaFichas", overlaps="cuenta")

     
    def __init__(self, idFicha, user_id_traspaso, cuenta_broker_id_traspaso, fecha_traspaso, 
                 fecha_habilitacion, fecha_denuncia, fecha_baja, user_id_denuncia, user_id_alta, 
                 user_id_baja, estado_traza,token):
        self.idFicha = idFicha
        self.user_id_traspaso = user_id_traspaso
        self.cuenta_broker_id_traspaso = cuenta_broker_id_traspaso
        self.fecha_traspaso = fecha_traspaso
        self.fecha_habilitacion = fecha_habilitacion
        self.fecha_denuncia = fecha_denuncia
        self.fecha_baja = fecha_baja
        self.user_id_denuncia = user_id_denuncia
        self.user_id_alta = user_id_alta
        self.user_id_baja = user_id_baja
        self.estado_traza = estado_traza
        self.token = token

    @classmethod
    def crear_tabla_trazaFichas(cls):
        insp = inspect(db.engine)
        if not insp.has_table(cls.__tablename__):
            db.create_all()

class MerSchema(ma.Schema):
    class Meta:
        fields = ("id", "idFicha", "user_id_traspaso", "cuenta_broker_id_traspaso", 
                  "fecha_traspaso", "fecha_habilitacion", "fecha_denuncia", "fecha_baja", 
                  "user_id_denuncia", "user_id_alta", "user_id_baja", "estado_traza", "token")

mer_schema = MerSchema()
mer_schemas = MerSchema(many=True)
