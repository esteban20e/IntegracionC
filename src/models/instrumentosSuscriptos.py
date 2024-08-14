from utils.db import db
from flask_marshmallow import Marshmallow
from flask import Blueprint
from sqlalchemy import inspect,Column, Integer, String, ForeignKey


ma = Marshmallow()

instrumentoSuscriptos = Blueprint('instrumentoSuscriptos',__name__)


class InstrumentoSuscriptos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(100))   
    timestamp =  db.Column(db.Integer) 
    
    # constructor
    def __init__(self,symbol,timestamp):   
        self.symbol = symbol       
        self.timestamp = timestamp

    @classmethod
    def crear_tabla_instrumentoSuscriptos(self):
        insp = inspect(db.engine)
        if not insp.has_table("instrumentoSuscriptos"):
            db.create_all()
                
class MerShema(ma.Schema):
    class Meta:
        fields = ("id","symbol","timestamp")
        
mer_schema = MerShema()
mer_shema = MerShema(many=True)

