from flask_marshmallow import Marshmallow
from flask import Blueprint
from utils.db import db
from sqlalchemy import inspect,Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship

ma = Marshmallow()

ficha = Blueprint('ficha', __name__)

class Ficha(db.Model):
    __tablename__ = 'ficha'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, ForeignKey('usuarios.id'))  
    cuenta_broker_id = db.Column(Integer, ForeignKey('cuentas.id'))  
    activo = db.Column(Boolean, nullable=False, default=False)   
    token = db.Column(String(500), nullable=True)
    llave = db.Column(db.LargeBinary(128), nullable=False)
    monto_efectivo = db.Column(Float)
    porcentaje_creacion = db.Column(Integer)   
    valor_cuenta_creacion = db.Column(Float)
    valor_cuenta_actual = db.Column(Float)
    estado = db.Column(String(500), nullable=True)
    fecha_generacion = db.Column(DateTime)
    interes = db.Column(Float)
   
    cuentas = relationship("Cuenta", back_populates="ficha")   
    usuarios = relationship("Usuario", back_populates="ficha")
    trazaFichas = relationship('TrazaFicha', back_populates='ficha')
    
    def __init__(self, user_id, cuenta_broker_id, activo=False, token=None,llave=None, monto_efectivo=0.0, 
                 porcentaje_creacion=0, valor_cuenta_creacion=0.0, valor_cuenta_actual=0.0, 
                 estado=None, fecha_generacion=None, interes=0.0):
        self.user_id = user_id
        self.cuenta_broker_id = cuenta_broker_id
        self.activo = activo
        self.token = token
        self.llave = llave
        self.monto_efectivo = monto_efectivo
        self.porcentaje_creacion = porcentaje_creacion
        self.valor_cuenta_creacion = valor_cuenta_creacion
        self.valor_cuenta_actual = valor_cuenta_actual
        self.estado = estado
        self.fecha_generacion = fecha_generacion
        self.interes = interes

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.activo

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @classmethod
    def crear_tabla_ficha(cls):
        insp = inspect(db.engine)
        if not insp.has_table(cls.__tablename__):
            db.create_all()

class MerSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "cuenta_broker_id", "activo", "token","llave", "monto_efectivo",
                  "porcentaje_creacion", "valor_cuenta_creacion", "valor_cuenta_actual", 
                  "estado", "fecha_generacion", "interes")

mer_schema = MerSchema()
mer_schemas = MerSchema(many=True)
