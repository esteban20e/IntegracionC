
from utils.db import db
from flask_marshmallow import Marshmallow
from flask import Blueprint
import enum
from sqlalchemy import inspect,Column, Integer, String, ForeignKey


ma = Marshmallow()
instrumentoEstrategiaUno = Blueprint('instrumentoEstrategiaUno',__name__) 
class InstrumentoEstrategiaUno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instrument = db.Column(db.String(100))
    comision = db.Column(db.Float)
    initial_size = db.Column(db.Float)
    buy_size = db.Column(db.Float)
    sell_size = db.Column(db.Float)
    spread = db.Column(db.Float)
    tick = db.Column(db.Float)
    my_order = db.Column(db.Float)
    last_md = db.Column(db.Float)
    state = db.Column(db.Float)
    def __init__(self, instrument, size, spread):
        # Define variables
        self.instrument = instrument
        self.comision = 0
        self.initial_size = size
        self.buy_size = size
        self.sell_size = size
        self.spread = spread
        self.tick = 0.001
        self.my_order = dict()
        self.last_md = None
        self.state = States.WAITING_MARKET_DATA
 
    @classmethod
    def crear_tabla_instrumentoEstrategiaUno(self):
        insp = inspect(db.engine)
        if not insp.has_table("instrumentoEstrategiaUno"):
            db.create_all()
                    
class MerShema(ma.Schema):
    class Meta:
        fields = ("id","instrument","comision","initial_size","buy_size","sell_size","spread","tick","my_order","last_md","state")

mer_schema = MerShema()
mer_shema = MerShema(many=True)

class States(enum.Enum):
    WAITING_MARKET_DATA = 0
    WAITING_CANCEL = 1
    WAITING_ORDERS = 2