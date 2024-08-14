from utils.db import db
from flask_marshmallow import Marshmallow
from flask import Blueprint
from sqlalchemy import inspect,Column, Integer, String, ForeignKey
ma = Marshmallow()
instrumento = Blueprint('instrumento',__name__) 
class Instrumento(db.Model):
    __tablename__ = 'instrumento'
    id = db.Column(db.Integer, primary_key=True)
    especie = db.Column(db.String(100))
    c_compra = db.Column(db.Float)
    p_compra = db.Column(db.Float)
    p_venta = db.Column(db.Float)
    c_venta = db.Column(db.Float)
    ultimo = db.Column(db.Float)
    var = db.Column(db.Float)
    apertura = db.Column(db.Float)
    minimo = db.Column(db.Float)
    maximo = db.Column(db.Float)
    cierre_anterior = db.Column(db.Float)
    volumen = db.Column(db.Float)
    vol_monto = db.Column(db.Float)
    vwap = db.Column(db.Float)
    idsegmento = db.Column(db.Float)
    idmarket = db.Column(db.Float)
   

    # constructor
    def __init__(self, especie,c_compra,p_compra,p_venta,c_venta,ultimo,var,apertura,minimo,maximo,cierre_anterior,volumen,vol_monto,vwap,idsegmento,idmarket):
        self.especie = especie
        self.c_compra = c_compra
        self.p_compra = p_compra
        self.p_venta = p_venta
        self.c_venta = c_venta
        self.ultimo = ultimo
        self.var = var
        self.apertura = apertura
        self.minimo = minimo
        self.maximo = maximo
        self.cierre_anterior = cierre_anterior
        self.volumen = volumen
        self.vol_monto = vol_monto
        self.vwap = vwap
        self.idsegmento = idsegmento
        self.idmarket = idmarket

    @classmethod        
    def crear_tabla_instrumento(self):
        insp = inspect(db.engine)
        if not insp.has_table("instrumento"):
            db.create_all()
                  
class MerShema(ma.Schema):
    class Meta:
        fields = ("id",  "especie","c_compra","p_compra","p_venta","c_venta","ultimo","var","apertura","minimo","maximo","cierre_anterior","volumen","vol_monto","vwap","idsegmento","idmarket")

mer_schema = MerShema()
mer_shema = MerShema(many=True)

