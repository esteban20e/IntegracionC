from pipes import Template
from unittest import result
import requests
import json
import pyRofex
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from models.instrumento import Instrumento
import routes.instrumentos as inst
import routes.instrumentosGet as instrumentosGet
from utils.db import db
import routes.api_externa_conexion.get_login as get
import routes.api_externa_conexion.validaInstrumentos as val
from models.instrumentosSuscriptos import InstrumentoSuscriptos

import asyncio
import websockets
import websocket
import json
# Importar la clase base de la biblioteca de websockets
from websockets import WebSocketServerProtocol








# Crea la conexión WebSocket
ws = None
global datos


suscripciones = Blueprint('suscripciones',__name__)

reporte_de_instrumentos = []


@suscripciones.route("/suscripcion_instrumentos/" )
def suscripcion_instrumentos():
    try:
        
        return render_template("suscripcion.html" )

    except:        
        return render_template("login.html" )

@suscripciones.route("/suscripcionDb/" )
def suscripcionDb():
    try:
       
         all_ins = db.session.query(InstrumentoSuscriptos).all()
         db.session.close()
         return render_template("suscripciones_db.html", datos =  all_ins)
    except:        
        return render_template("errorLogueo.html" )
    
@suscripciones.route("/suscDelete/", methods = ['POST'] )
def suscDelete():
    try:
         if request.method == 'POST':
            id = request.form['id']            
            dato = InstrumentoSuscriptos.query.get(id)
            print(dato)
            db.session.delete(dato)
            db.session.commit()
            
            flash('Operation Removed successfully')
            all_ins = db.session.query(InstrumentoSuscriptos).all()
            db.session.close()
            return render_template("suscripciones_db.html", datos =  all_ins)
    except: 
            flash('Operation No Removed')       
            all_ins = db.session.query(InstrumentoSuscriptos).all()
            db.session.close()
            return render_template("suscripciones_db.html", datos =  all_ins)

@suscripciones.route('/ajax', methods=['POST'])
def ajax():

    if request.method == "POST":
        datos = request.get_json()['datos']  # Acc
       
        print(datos)
        return render_template("suscripcion.html", datos_modificados=datos)
    
# Función async para enviar datos al WebSocket
async def send_data_to_websocket(data):
    async with websockets.connect('ws://localhost:8765') as websocket:
        await websocket.send(data)

# Función para iniciar el servidor WebSocket
async def start_websocket_server():
    # Establecer la conexión WebSocket
    websocket = await websockets.connect("ws://localhost:8765")
    websocket.datos = [get.market_data_recibida,longitudLista]
    
    # Ejecutar el servidor WebSocket
    start_server = await websockets.serve(websocket_handler, "localhost", 8765)
    await start_server



async def websocket_handler(websocket, path):
   # Obtener los datos del contexto de la conexión
    datos = websocket.extra['datos']
    market_data_recibida = datos[0]
    longitudLista = datos[1]
    
    # Enviar los datos al cliente
    await websocket.send(json.dumps({'market_data': market_data_recibida, 'longitud_lista': longitudLista}))



@suscripciones.route("/SuscripcionPorWebSocket/")      
async def SuscripcionPorWebSocket():
    # Trae los instrumentos para suscribirte
    mis_instrumentos = instrumentosGet.get_instrumento_para_suscripcion_ws()
    longitudLista = len(mis_instrumentos)
    print(len(mis_instrumentos),"<<<<<---------------------mis_instrumentos --------------------------->>>>>> ",mis_instrumentos)
    repuesta_listado_instrumento = get.pyRofexInicializada.get_detailed_instruments()
    
    listado_instrumentos = repuesta_listado_instrumento['instruments']   
    
    tickers_existentes = inst.obtener_array_tickers(listado_instrumentos) 
    instrumentos_existentes = val.validar_existencia_instrumentos(mis_instrumentos,tickers_existentes)
    instrumentos_existentes_arbitrador1 = instrumentos_existentes.copy()

    ##aqui se conecta al ws
    #get.pyRofexInicializada.init_websocket_connection(market_data_handler2,order_report_handler,error_handler,exception_error)
    print("<<<-----------pasoooo conexiooooonnnn wsocket.py--------->>>>>")
      
    #### aqui define el MarketDataEntry
    entries = [get.pyRofexInicializada.MarketDataEntry.BIDS,
               get.pyRofexInicializada.MarketDataEntry.OFFERS,
               get.pyRofexInicializada.MarketDataEntry.LAST]
      
    #### aqui se subscribe   
    mensaje = get.pyWsSuscriptionInicializada(tickers=instrumentos_existentes,entries=entries)
    print("instrumento_suscriptio",mensaje)
    datos = [get.market_data_recibida,longitudLista]
    
   
    
    return render_template('suscripcion.html', datos=[get.market_data_recibida,longitudLista])


    
    
async def market_data_handler2(message):
  
  
  print("message",message)
  ticker = message["instrumentId"]["symbol"]
  bid = message["marketData"]["BI"] if len(message["marketData"]["BI"]) != 0 else [{'price': "-", 'size': "-"}]
  offer = message["marketData"]["OF"] if len(message["marketData"]["OF"]) != 0 else [{'price': "-", 'size': "-"}]
  last = message["marketData"]["LA"]["price"] if message["marketData"]["LA"] != None else 0
  dateLA = message['marketData']['LA']['date'] if message["marketData"]["LA"] != None else 0

  timestamp = message['timestamp']
  objeto_md = {'ticker':ticker,'bid':bid,'offer':offer,'last':last,'dateLA':dateLA,'timestamp':timestamp}
  get.market_data_recibida.append(objeto_md)
 
  print("Mensaje de MarketData en market_data_handler: {0}".format(message))
  data = {"bid": bid, "offer": offer, "last": last}
  await websocket.send(json.dumps(message))
  
  #{"type":"or","orderReport":{"orderId":"1128056","clOrdId":"user14545967430231","proprietary":"api","execId":"160127155448-fix1-1368","accountId":{"id":"30"},"instrumentId":{"marketId":"ROFX","symbol":"DODic21"},"price":18.000,"orderQty":10,"ordType":"LIMIT","side":"BUY","timeInForce":"DAY","transactTime":"20160204-11:41:54","avgPx":0,"lastPx":0,"lastQty":0,"cumQty":0,"leavesQty":10,"status":"CANCELLED","text":"Reemplazada"}}
def order_report_handler(message):
  print("Mensaje de OrderRouting: {0}".format(message))
  get.reporte_de_ordenes.append(message)
  

  
def error_handler(message):
  print("Mensaje de error: {0}".format(message))

def exception_handler(e):
    print("Exception Occurred: {0}".format(e.msg))
  
def exception_error(message):
  print("Mensaje de excepción: {0}".format(message))  
  {"type":"or","orderReport":{"orderId":"1128056","clOrdId":"user14545967430231","proprietary":"api","execId":"160127155448-fix1-1368","accountId":{"id":"30"},"instrumentId":{"marketId":"ROFX","symbol":"DODic23"},"price":18.000,"orderQty":10,"ordType":"LIMIT","side":"BUY","timeInForce":"DAY","transactTime":"20160204-11:41:54","avgPx":0,"lastPx":0,"lastQty":0,"cumQty":0,"leavesQty":10,"status":"CANCELLED","text":"Reemplazada"}}

    
    
    
#import websockets
#import json
#from pyRofex import *

# Crea la conexión WebSocket
#ws = None

# Define la función para enviar los datos a través del WebSocket
#async def send_data_to_websocket(data):
    # Convierte los datos a formato JSON
#    json_data = json.dumps(data)
    # Envía los datos al WebSocket
#    await ws.send(json_data)

# Define la función de callback para procesar los datos recibidos de PyRofex
#def process_market_data_message(message):
#    asyncio.ensure_future(send_data_to_websocket(message))

# Inicia la sesión en PyRofex
#initialize(user="mi_usuario", password="mi_contraseña", account="mi_cuenta", environment=Environment.REMARKET)

# Suscríbete al mercado de datos
#market_data_subscription(
#    tickers=["RFX20Mar22"],
#    entries=[MarketDataEntry.BIDS, MarketDataEntry.OFFERS],
#    depth=5
#)

# Registra la función de callback para el mercado de datos
#market_data_handler = MarketDataHandler()
#market_data_handler.add_subscription(market_data_subscription)
#market_data_handler.add_callback(MarketDataOperation.SUBSCRIBE, process_market_data_message)

# Inicia el servidor WebSocket
#async def start_websocket(websocket, path):
#    global ws
#    ws = websocket
#    print("WebSocket server started")

# Inicia el loop de PyRofex para procesar los mensajes entrantes
#start_server = websockets.serve(start_websocket, 'localhost', 8000)
#asyncio.get_event_loop().run_until_complete(start_server)
#asyncio.get_event_loop().run_forever()

