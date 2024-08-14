from flask_marshmallow import Marshmallow
from flask import Blueprint
from utils.db import db
from sqlalchemy import inspect,Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

ma = Marshmallow()

cuentas = Blueprint('cuentas',__name__) 



class Cuenta(db.Model):
    __tablename__ = 'cuentas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('usuarios.id'))  
    userCuenta = db.Column(db.String(120), unique=True, nullable=False)
    passwordCuenta = db.Column(db.LargeBinary(128), nullable=False)
    accountCuenta = db.Column(db.String(500), nullable=True)
    selector = db.Column(db.String(500), nullable=True)
    ficha = relationship("Ficha", back_populates="cuentas")
    trazaFichas = relationship('TrazaFicha', backref='cuenta')    
    usuarios = relationship("Usuario", back_populates="cuentas")

    
 # constructor
    def __init__(self, id,user_id,userCuenta,passwordCuenta,accountCuenta,selector):
        self.id = id
        self.user_id = user_id
        self.userCuenta = userCuenta
        self.passwordCuenta = passwordCuenta
        self.accountCuenta = accountCuenta
        self.selector = selector

   
    def __repr__(self):
        return f"Cuenta(id={self.id}, user_id={self.user_id}, userCuenta={self.userCuenta}, passwordCuenta={self.passwordCuenta}, accountCuenta={self.accountCuenta}, selector={self.selector})"
    @classmethod
    def crear_tabla_cuentas(self):
         insp = inspect(db.engine)
         if not insp.has_table("cuentas"):
              db.create_all()
             
    
        
class MerShema(ma.Schema):
    class Meta:
        fields = ("id", "user_id" ,"userCuenta","passwordCuenta","accountCuenta","selector")

mer_schema = MerShema()
mer_shema = MerShema(many=True)

