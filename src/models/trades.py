from flask_marshmallow import Marshmallow
from flask import Blueprint
from utils.db import db
from sqlalchemy import inspect,Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship

ma = Marshmallow()

trades = Blueprint('trades',__name__) 



class Trade(db.Model):
    __tablename__ = 'trades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('usuarios.id'))  
    userCuenta = db.Column(db.String(120)) 
    accountCuenta = db.Column(db.String(120))    
    clOrdId_alta = db.Column(db.String(120))
    clOrdId_baja = db.Column(db.String(120))   
    wsClOrdId = db.Column(db.DateTime)
    alta_timestamp = db.Column(db.DateTime)
    baja_timestamp =  db.Column(db.DateTime)
    proprietary =  db.Column(db.Boolean)
    marketId = db.Column(db.String(120)) 
    symbol = db.Column(db.String(120))     
    tipo = db.Column(db.String(120))
    tradeEnCurso = db.Column(db.String(120))
    ut = db.Column(db.Integer)      
    status = db.Column(db.String(500))
    
    usuario = relationship("Usuario", back_populates="trades")


    
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
    def crear_tabla_trades(self):
         insp = inspect(db.engine)
         if not insp.has_table("trades"):
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