from flask_marshmallow import Marshmallow
from flask import Blueprint
from utils.db import db
from sqlalchemy import inspect,Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship

ma = Marshmallow()

orden = Blueprint('orden',__name__) 



class Orden(db.Model):
    __tablename__ = 'orden'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('usuarios.id'))  
    userCuenta = db.Column(db.String(120)) 
    accountCuenta = db.Column(db.String(120))    
    clOrdId_alta = db.Column(db.String(120))
    clOrdId_baja = db.Column(db.String(120))
    clientId = db.Column(db.Integer)    
    wsClOrdId_timestamp = db.Column(db.DateTime)
    clOrdId_alta_timestamp = db.Column(db.DateTime)
    clOrdId_baja_timestamp =  db.Column(db.DateTime)
    proprietary =  db.Column(db.Boolean)
    marketId = db.Column(db.String(120)) 
    symbol = db.Column(db.String(120))     
    tipo = db.Column(db.String(120))
    tradeEnCurso = db.Column(db.String(120))
    ut = db.Column(db.Integer)   
    senial = db.Column(db.String(120))
    status = db.Column(db.String(500))
    
    
    usuarios = relationship("Usuario", back_populates="orden")
    #usuario = relationship("Usuario", back_populates="orden")
   

    
 # constructor
    def __init__(self, user_id,userCuenta,accountCuenta,
                 clOrdId_alta,
                 clOrdId_baja,
                 clientId,
                 wsClOrdId_timestamp,
                 clOrdId_alta_timestamp ,
                 clOrdId_baja_timestamp ,
                 proprietary,
                 marketId,
                 symbol,   
                 tipo,
                 tradeEnCurso,
                 ut,   
                 senial,
                 status):
       
        self.user_id = user_id
        self.userCuenta = userCuenta        
        self.accountCuenta = accountCuenta
        self.clOrdId_alta  = clOrdId_alta
        self.clOrdId_baja   = clOrdId_baja
        self.clientId  = clientId
        self.wsClOrdId_timestamp   = wsClOrdId_timestamp
        self.clOrdId_alta_timestamp  = clOrdId_alta_timestamp
        self.clOrdId_baja_timestamp  = clOrdId_baja_timestamp
        self.proprietary = proprietary
        self.marketId  = marketId
        self.symbol = symbol
        self.tipo = tipo
        self.tradeEnCurso = tradeEnCurso
        self.ut = ut   
        self.senial = senial
        self.status = status
        

   

    @classmethod
    def crear_tabla_orden(_self):
         insp = inspect(db.engine)
         if not insp.has_table("orden"):
              db.create_all()
             
    
        
class MerShema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "userCuenta","accountCuenta",
                 "clOrdId_alta",
                 "clOrdId_baja",
                 "clientId",
                 "wsClOrdId_timestamp",
                 "clOrdId_alta_timestamp" ,
                 "clOrdId_baja_timestamp" ,
                 "proprietary",
                 "marketId",
                 "symbol",   
                 "tipo",
                 "tradeEnCurso",
                 "ut",   
                 "senial",
                 "status")

mer_schema = MerShema()
mer_shema = MerShema(many=True)