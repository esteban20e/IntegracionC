from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from utils.common import Marshmallow, db, get
import routes.instrumentosGet as instrumentosGet
import routes.api_externa_conexion.validaInstrumentos as val

import routes.instrumentos as inst
from datetime import datetime

import pandas as pd
import pyRofex #lo utilizo para test
import time    #lo utilizo para test
import asyncio
import websockets
import websocket
import json


wsocket = Blueprint('wsocket',__name__)



reporte_de_instrumentos = []


def wsocketConexion():
   
   
  # get.pyRofexInicializada.order_report_subscription()
  # get.pyRofexInicializada.add_websocket_market_data_handler(market_data_handler_arbitraje_001)
   
   pyRofexWebSocket = get.pyRofexInicializada.init_websocket_connection(market_data_handler=market_data_handler_0,order_report_handler=order_report_handler_0,error_handler=error_handler,exception_handler=exception_handler)
   get.pyRofexInicializada.remove_websocket_market_data_handler(market_data_handler_0)
   get.pyRofexInicializada.remove_websocket_order_report_handler(order_report_handler_0)
 

def market_data_handler_0(message):
    print(message)

def order_report_handler_0(message):
  print(message)



@wsocket.route('/detenerWSSuscripcionInstrumentos/')   
def detenerWSSuscripcionInstrumentos():
     get.pyRofexInicializada.close_websocket_connection()
     return render_template("home.html" )
   


@wsocket.route('/suscriptos/')
def suscriptos():
      try:
        #traigo los instrumentos para suscribirme
        mis_instrumentos = instrumentosGet.get_instrumento_para_suscripcion_ws()
        longitudLista = len(mis_instrumentos)
        print(len(mis_instrumentos),"<<<<<---------------------mis_instrumentos --------------------------->>>>>> ",mis_instrumentos)
        repuesta_listado_instrumento = get.pyRofexInicializada.get_detailed_instruments()
      # print("repuesta_listado_instrumento repuesta_listado_instrumento ",repuesta_listado_instrumento)
        listado_instrumentos = repuesta_listado_instrumento['instruments']   
        tickers_existentes = inst.obtener_array_tickers(listado_instrumentos) 
        instrumentos_existentes = val.validar_existencia_instrumentos(mis_instrumentos,tickers_existentes)
      
      ##aqui se conecta al ws
        
        get.pyRofexInicializada.init_websocket_connection(market_data_handler,order_report_handler,error_handler,exception_error)
        print("<<<-----------pasoooo conexiooooonnnn wsocket.py--------->>>>>")
      
        #### aqui define el MarketDataEntry
        entries = [get.pyRofexInicializada.MarketDataEntry.BIDS,
                    get.pyRofexInicializada.MarketDataEntry.OFFERS,
                    get.pyRofexInicializada.MarketDataEntry.LAST]
       # while True: 

          ###asi puedo llamar otra funcion para manejar los datos del ws#####      
          #get.pyRofexInicializada.add_websocket_market_data_handler(mostrar)
          #### aqui se subscribe   
        print("<<<-----------entries instrumento_suscriptio--------->>>>> ",entries)              
        print("<<<-----------instrumentos_existentes a suscribir en wsocket.py--------->>>>>",instrumentos_existentes)       
        mensaje =get.pyRofexInicializada.market_data_subscription(tickers=instrumentos_existentes,entries=entries)
        
        print("instrumento_suscriptio",mensaje)
          # Subscribes to an Invalid Instrument (Error Message Handler should be call)
        # get.pyRofexInicializada.market_data_subscription(tickers=["InvalidInstrument"],entries=entries)
       
        #print("report encontrado ",report) 
       # time.sleep(100)
       # time.sleep(1)  
     # except KeyboardInterrupt:
      #  pass
       # get.pyRofexInicializad ºa.close_websocket_connection()
       
       
        return render_template('suscripcion.html', datos =  [get.market_data_recibida,longitudLista])
      except:  
           print("contraseña o usuario incorrecto")  
           flash('Loggin Incorrect')    
           return render_template("errorLogueo.html" ) 

@wsocket.route('/SuscripcionWs/', methods = ['POST'])
def SuscripcionWs():
  
     if request.method == "POST":     
     
        Ticker = request.form["symbol"]                 
        Ticker = Ticker.replace("*", " ")
       # print("websoooooooooooooooooketttt en wsocket.py ",Ticker)
        #almaceno los symbol a suscribirme
        instrumentosGet.guarda_instrumento_para_suscripcion_ws(Ticker)
        #traigo los instrumentos para suscribirme
        #mis_instrumentos = instrumentosGet.get_instrumento_para_suscripcion_ws()
       
        #print("llega aquiiiiiiiiiiiiiiiiiiiiiiiiiiiiii mis_instrumentos ",mis_instrumentos)
        #repuesta_listado_instrumento = get.pyConectionWebSocketInicializada.get_detailed_instruments()
        #listado_instrumentos = repuesta_listado_instrumento['instruments']   
        #tickers_existentes = inst.obtener_array_tickers(listado_instrumentos) 
        #longitudLista = len(mis_instrumentos)
        #instrumentos_existentes = val.validar_existencia_instrumentos(mis_instrumentos,tickers_existentes)
        #print("instrumentos_existentes ",instrumentos_existentes)    
    ##aqui se conecta al ws
       
        
        
        #### aqui define el MarketDataEntry
      #  print("siiiiiiiiiiiiiiiiiiiiii paaaaaaaaaaaaaaaaaasaaaaaaaaaaaaaaaaa conexion")
        #entries = [get.pyConectionWebSocketInicializada.MarketDataEntry.BIDS,
        #            get.pyConectionWebSocketInicializada.MarketDataEntry.OFFERS,
        #            get.pyConectionWebSocketInicializada.MarketDataEntry.LAST]
         
        ###asi puedo llamar otra funcion para manejar los datos del ws#####      
        #get.pyRofexInicializada.add_websocket_market_data_handler(mostrar)
         #### aqui se subscribe
       
        #get.pyConectionWebSocketInicializada.market_data_subscription(tickers=instrumentos_existentes,entries=entries)
        #print("instrumento_suscriptio",instrumento_suscriptio)
        #get.pyConectionWebSocketInicializada.order_report_subscription(snapshot=True)
        diccionario ={}
        #actualizarTablaMD()
        #diccionario.update(get.market_data_recibida)
        repuesta_listado_instrumento = get.pyRofexInicializada.get_detailed_instruments()
        #repuesta_listado_instrumento = get.pyRofexInicializada.get_market_data()
        listado_instrumentos = repuesta_listado_instrumento['instruments']
        #for listado_instrumentos in listado_instrumentos:
       # print("listado_instrumentos en instrumentos_detalles en intrumentos.py",listado_instrumentos)#aqui muestro los instrumentos por pantalla
        print("listado_instrumentos en instrumentos_detalles en intrumentos.py")
        return render_template("instrumentos.html", datos = listado_instrumentos   )
        #return render_template('suscripcion.html', datos =  [get.market_data_recibida,longitudLista])


##########################esto es para ws#############################
#Mensaje de MarketData: {'type': 'Md', 'timestamp': 1632505852267, 'instrumentId': {'marketId': 'ROFX', 'symbol': 'DLR/DIC21'}, 'marketData': {'BI': [{'price': 108.25, 'size': 100}], 'LA': {'price': 108.35, 'size': 3, 'date': 1632505612941}, 'OF': [{'price': 108.45, 'size': 500}]}}

def error_handler(message):
  print("Mensaje de error: {0}".format(message))

def exception_handler(e):
    print("Exception Occurred: {0}".format(e.msg))
  
def exception_error(message):
  print("Mensaje de excepción: {0}".format(message))  
  {"type":"or","orderReport":{"orderId":"1128056","clOrdId":"user14545967430231","proprietary":"api","execId":"160127155448-fix1-1368","accountId":{"id":"30"},"instrumentId":{"marketId":"ROFX","symbol":"DODic23"},"price":18.000,"orderQty":10,"ordType":"LIMIT","side":"BUY","timeInForce":"DAY","transactTime":"20160204-11:41:54","avgPx":0,"lastPx":0,"lastQty":0,"cumQty":0,"leavesQty":10,"status":"CANCELLED","text":"Reemplazada"}}

def order_report_handler(message):
  
  
  #print("Mensaje de OrderRouting: {0}".format(message))
  get.reporte_de_ordenes.append(message)
  
 # 2-Defines the handlers that will process the messages and exceptions.
def order_report_handler_cancel(message):
    print("Order Report Message Received: {0}".format(message))
    # 6-Handler will validate if the order is in the correct state (pending_new)
    if message["orderReport"]["status"] == "NEW":
        # 6.1-We cancel the order using the websocket connection
        print("Send to Cancel Order with clOrdID: {0}".format(message["orderReport"]["clOrdId"]))
        pyRofex.cancel_order_via_websocket(message["orderReport"]["clOrdId"])

    # 7-Handler will receive an Order Report indicating that the order is cancelled (will print it)
    if message["orderReport"]["status"] == "CANCELLED":
        print("Order with ClOrdID '{0}' is Cancelled.".format(message["orderReport"]["clOrdId"])) 
   
  ###########tabla de market data
  #Mensaje de MarketData: {'type': 'Md', 'timestamp': 1632505852267, 'instrumentId': {'marketId': 'ROFX', 'symbol': 'DLR/DIC21'}, 'marketData': {'BI': [{'price': 108.25, 'size': 100}], 'LA': {'price': 108.35, 'size': 3, 'date': 1632505612941}, 'OF': [{'price': 108.45, 'size': 500}]}}

def market_data_handler(message):
  
  
 # print("message",message)
  ticker = message["instrumentId"]["symbol"]
  bid = message["marketData"]["BI"] if len(message["marketData"]["BI"]) != 0 else [{'price': "-", 'size': "-"}]
  offer = message["marketData"]["OF"] if len(message["marketData"]["OF"]) != 0 else [{'price': "-", 'size': "-"}]
  last = message["marketData"]["LA"]["price"] if message["marketData"]["LA"] != None else 0
  dateLA = message['marketData']['LA']['date'] if message["marketData"]["LA"] != None else 0

  timestamp = message['timestamp']
  objeto_md = {'symbol':ticker,'bid':bid,'offer':offer,'last':last,'dateLA':dateLA,'timestamp':timestamp}
  get.market_data_recibida.append(objeto_md)
 
  #print("Mensaje de MarketData en market_data_handler: {0}".format(message))
  
  
  #{"type":"or","orderReport":{"orderId":"1128056","clOrdId":"user14545967430231","proprietary":"api","execId":"160127155448-fix1-1368","accountId":{"id":"30"},"instrumentId":{"marketId":"ROFX","symbol":"DODic21"},"price":18.000,"orderQty":10,"ordType":"LIMIT","side":"BUY","timeInForce":"DAY","transactTime":"20160204-11:41:54","avgPx":0,"lastPx":0,"lastQty":0,"cumQty":0,"leavesQty":10,"status":"CANCELLED","text":"Reemplazada"}}
def order_report_handler(message):
  #print("Mensaje de OrderRouting: {0}".format(message))
  get.reporte_de_ordenes.append(message)
  
  
def actualizarTablaMD():
  print("actualizarTablaMD")
  
  df = pd.DataFrame(columns=pd.Index(['Ticker','Timestamp','Vol. Compra','Precio Compra', 'Precio Venta', 'Vol. Venta', 'Ult. Precio Operado']))
  for md in get.market_data_recibida: 
    reporte_de_instrumentos.append({
          'Ticker': md['ticker'],
          'Timestamp':datetime.fromtimestamp(int(md['timestamp'])/1000),
          'Vol. Compra':md['bid'][0]['size'],
          'Precio Compra':md['bid'][0]['price'],
          'Precio Venta': md['offer'][0]['price'],
          'Vol. Venta': md['offer'][0]['size'],
          'Ult. Precio Operado': md['last']})
    df = df.append(
        {
          'Ticker': md['ticker'],
          'Timestamp':datetime.fromtimestamp(int(md['timestamp'])/1000),
          'Vol. Compra':md['bid'][0]['size'],
          'Precio Compra':md['bid'][0]['price'],
          'Precio Venta': md['offer'][0]['price'],
          'Vol. Venta': md['offer'][0]['size'],
          'Ult. Precio Operado': md['last']}, 
          ignore_index=True)
 
  return df.style.set_table_styles(
      [{'selector': 'tr:hover',
        'props': [('background-color', 'yellow'),('color', 'black')]},
      {'selector': 'thead',
        'props': [('font-size', '16px'),('padding', '8px'),('background-color','brown')]}]
      )
   #return  render_template("suscripcion.html")

async def muestraTabla(webSocket,path):
  name = await webSocket.recv()
  print(f"< {name}")
  
  greeting = f"hello {name}!"
  
  await webSocket.send(greeting)
  print(f"< {greeting}")
        
  start_server = websockets.serve(muestraTabla,"localhost",8765)
  asyncio.get_event_loop().run_untill_complete(start_server)
  asyncio.get_event_loop().run_forever()


def on_message(message):
  # Se conecta al servidor local WebSocket
    local_websocket = websocket.WebSocket()
    local_websocket.connect("ws://localhost:8765/")
    # Convierte el mensaje de cadena JSON a un objeto Python
    market_data = json.loads(message)

    # Envía el mensaje al servidor local WebSocket
    print(json.dumps(market_data))
    local_websocket.send(json.dumps(market_data))
    
    
