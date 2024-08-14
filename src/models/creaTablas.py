from models.usuario import Usuario
from models.cuentas import Cuenta
from models.ficha import Ficha
from models.logs import Logs
from models.orden import Orden
from models.modelMedia.image import Image
from models.instrumento import Instrumento
from models.instrumentoGet import InstrumentoGet
from models.instrumentosSuscriptos import InstrumentoSuscriptos
from models.instrumentoEstrategiaUno import InstrumentoEstrategiaUno
from models.trades import Trade
from models.trazaFicha import TrazaFicha
from models.triggerEstrategia import TriggerEstrategia

from datetime import datetime
from flask import Blueprint

creaTabla = Blueprint('creaTabla',__name__)

def crea_tablas_DB():
    Usuario.crear_tabla_usuarios()
    Cuenta.crear_tabla_cuentas()
    Ficha.crear_tabla_ficha()
    Logs.crear_tabla_logs()
    Image.crear_tabla_image()
    Trade.crear_tabla_trades()
    TrazaFicha.crear_tabla_trazaFichas()
    TriggerEstrategia.crear_tabla_triggerEstrategia()
    Orden.crear_tabla_orden()   
    Instrumento.crear_tabla_instrumento()
    InstrumentoGet.crear_tabla_instrumentoGet()
    InstrumentoSuscriptos.crear_tabla_instrumentoSuscriptos()
    InstrumentoEstrategiaUno.crear_tabla_instrumentoEstrategiaUno()
    
    
    
    
    
    
   
    