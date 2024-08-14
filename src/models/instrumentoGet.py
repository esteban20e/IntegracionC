from utils.db import db
from flask_marshmallow import Marshmallow
from flask import Blueprint
from sqlalchemy import inspect,Column, Integer, String, ForeignKey

ma = Marshmallow()

instrumentoGet = Blueprint('instrumentoGet',__name__)


class InstrumentoGet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(100))   
    lowLimitPrice = db.Column(db.Float)
    highLimitPrice = db.Column(db.Float)
    minPriceIncrement = db.Column(db.Float)
    minTradeVol = db.Column(db.Float)
    maxTradeVol = db.Column(db.Float)
    tickSize = db.Column(db.Float)
    contractMultiplier = db.Column(db.Float)
    roundLot = db.Column(db.Float)
    priceConvertionFactor = db.Column(db.Float) 
    maturityDate = db.Column(db.Float) 
    currency = db.Column(db.Float)
    orderTypes = db.Column(db.Float)
    timesInForce = db.Column(db.Float)
    securityType = db.Column(db.Float)
    settlType = db.Column(db.Float)
    instrumentPricePrecision = db.Column(db.Float)
    instrumentSizePrecision = db.Column(db.Float)
    securityId = db.Column(db.Float) 
    securityIdSource = db.Column(db.Float) 
    securityDescription = db.Column(db.Float)
    tickPriceRanges = db.Column(db.Float)
    tickPriceRanges1 = db.Column(db.Float)
    tickPriceRanges2 = db.Column(db.Float)
    cficode = db.Column(db.Float)
    marketId = db.Column(db.Float) 
    
    # constructor
    def __init__( self,symbol, lowLimitPrice, highLimitPrice, minPriceIncrement, minTradeVol, maxTradeVol, tickSize, contractMultiplier, roundLot, priceConvertionFactor, maturityDate, currency, orderTypes, timesInForce, securityType, settlType, instrumentPricePrecision, instrumentSizePrecision, securityId, securityIdSource, securityDescription, tickPriceRanges, tickPriceRanges1, tickPriceRanges2, cficode, marketId):   
        self.symbol = symbol
        self.lowLimitPrice = lowLimitPrice
        self.highLimitPrice = highLimitPrice
        self.minPriceIncrement = minPriceIncrement
        self.minTradeVol = minTradeVol
        self.maxTradeVol = maxTradeVol
        self.tickSize = tickSize
        self.contractMultiplier = contractMultiplier
        self.roundLot = roundLot
        self.priceConvertionFactor = priceConvertionFactor 
        self.maturityDate = maturityDate
        self.currency = currency
        self.orderTypes = orderTypes
        self.timesInForce = timesInForce
        self.securityType = securityType
        self.settlType = settlType 
        self.instrumentPricePrecision = instrumentPricePrecision
        self.instrumentSizePrecision = instrumentSizePrecision
        self.securityId = securityId
        self.securityIdSource = securityIdSource
        self.securityDescription = securityDescription
        self.tickPriceRanges = tickPriceRanges
        self.tickPriceRanges1 = tickPriceRanges1
        self.tickPriceRanges2 = tickPriceRanges2
        self.cficode = cficode
        self.marketId = marketId
        
    @classmethod
    def crear_tabla_instrumentoGet(self):
        insp = inspect(db.engine)
        if not insp.has_table("instrumentoGet"):
            db.create_all()
        
class MerShema(ma.Schema):
    class Meta:
        fields = ("id","symbol", "lowLimitPrice", "highLimitPrice", "minPriceIncrement", "minTradeVol", "maxTradeVol", "tickSize", "contractMultiplier", "roundLot", "priceConvertionFactor", "maturityDate", "currency", "orderTypes", "timesInForce", "securityType", "settlType", "instrumentPricePrecision", "instrumentSizePrecision", "securityId", "securityIdSource", "securityDescription", "tickPriceRanges", "tickPriceRanges1", "tickPriceRanges2", "cficode", "marketId")

        
mer_schema = MerShema()
mer_shema = MerShema(many=True)

