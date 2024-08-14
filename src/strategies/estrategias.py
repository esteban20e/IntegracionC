from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify,current_app
import routes.instrumentosGet as instrumentosGet
from utils.db import db
import routes.api_externa_conexion.get_login as get
import routes.api_externa_conexion.validaInstrumentos as val
import routes.instrumentos as inst
from datetime import datetime
import enum
from models.instrumentoEstrategiaUno import InstrumentoEstrategiaUno
import socket
from models.triggerEstrategia import TriggerEstrategia
from models.usuario import Usuario
from models.cuentas import Cuenta
import jwt

estrategias = Blueprint('estrategias',__name__)

       
class States(enum.Enum):
    WAITING_MARKET_DATA = 0
    WAITING_CANCEL = 1
    WAITING_ORDERS = 2


@estrategias.route("/estrategias-usuario-general/",  methods=["GET"])
def estrategias_usuario_general():
    try:
      if request.method == 'GET': 
           triggerEstrategia = db.session.query(TriggerEstrategia).all()
           db.session.close()
           return render_template("/estrategias/panelControEstrategiaUser.html",datos = [0,triggerEstrategia])
    except:
       print('no hay usuarios') 
    return 'problemas con la base de datos'

@estrategias.route("/estrategias-usuario-nadmin",  methods=["POST"])
def estrategias_usuario_nadmin():
    try:
      if request.method == 'POST': 
          access_token = request.form.get('access_token_est') 
          if access_token:
            app = current_app._get_current_object()  
            
            usuario_id = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']                    
            estrategias = db.session.query(TriggerEstrategia).join(Usuario).filter(TriggerEstrategia.user_id == usuario_id).all()
            db.session.close()
            for estrategia in estrategias:
                print("ID:", estrategia.id)
                print("Name:", estrategia.userCuenta)
                # Print other attributes as needed
                print()
            return render_template("/estrategias/panelControEstrategiaUser.html",datos = [usuario_id,estrategias])
    
    except:
       print('no hay estrategias en strategies/estrategias.py') 
    return  render_template("/notificaciones/errorEstrategiaVacia.html")

@estrategias.route("/estrategias-usuario",  methods=["POST"])
def estrategias_usuario():
    try:
      if request.method == 'POST': 
            usuario_id = request.form['usuario_id']                      
            estrategias = db.session.query(TriggerEstrategia).join(Usuario).filter(TriggerEstrategia.user_id == usuario_id).all()
            db.session.close()
            for estrategia in estrategias:
                print("ID:", estrategia.id)
                print("Name:", estrategia.userCuenta)
                # Print other attributes as needed
                print()
            return render_template("/estrategias/panelControEstrategiaUser.html",datos = [usuario_id,estrategias])
    
    except:
       print('no hay estrategias') 
    return  render_template("/notificaciones/errorEstrategiaVacia.html")

@estrategias.route("/eliminar-trigger/",  methods=["POST"])
def eliminar_trigger():
    IdTrigger = request.form['IdTrigger']
   
    usuario_id = request.form['user_id']
    Trigger = TriggerEstrategia.query.get(IdTrigger)
    db.session.delete(Trigger)
    db.session.commit()
    
    
    flash('Trigger eliminado correctamente.')
    estrategias = db.session.query(TriggerEstrategia).all()
    db.session.close()   
    return render_template("/estrategias/panelControEstrategiaUser.html",datos = [usuario_id,estrategias])
@estrategias.route("/editar-trigger-nombre", methods=["POST"])
def editar_trigger_nombre():
    IdTrigger = request.form['IdTrigger']
    usuario_id = request.form['usuario_id']  
    
    Trigger = TriggerEstrategia.query.get(IdTrigger)
    Trigger.nombreEstrategia = request.form['TriggerNombre']
   
    db.session.commit()
   
    flash('Estrategia editado correctamente.')
    estrategias = db.session.query(TriggerEstrategia).all()
    db.session.close()
    return render_template("/estrategias/panelControEstrategiaUser.html",datos = [usuario_id,estrategias])
    
@estrategias.route("/editar-Trigger/", methods = ["POST"] )
def editar_Trigger():
    try:
        if request.method == 'POST':
            usuario_id = request.form['user_id']
            IdTrigger = request.form['IdTrigger']
            horaInicio = request.form['horaInicio']  
            horaFin = request.form['horaFin']  
            ManualAutomatico = request.form['ManualAutomatico'] 
            
            horaInicioSalvar, minutosInicioSalvar = horaInicio.split(':')
            horaFinSalvar, minutosFinSalvar = horaFin.split(':')
            hora_inicio = datetime(year=2023, month=7, day=3, hour=int(horaInicioSalvar), minute=int(minutosInicioSalvar))
            hora_fin = datetime(year=2023, month=7, day=3, hour=int(horaFinSalvar), minute=int(minutosFinSalvar))
            
            
            Trigger = TriggerEstrategia.query.get(IdTrigger)            
            Trigger.ManualAutomatico = ManualAutomatico
            Trigger.horaInicio = hora_inicio
            Trigger.horaFin = hora_fin
            
            db.session.commit()
            
            flash('Estrategia editada correctamente.')
            estrategias = db.session.query(TriggerEstrategia).all()
            db.session.close()
            return render_template("/estrategias/panelControEstrategiaUser.html",datos = [usuario_id,estrategias])
                    
    except:
                print('no hay estrategias')
    return render_template("/notificaciones/errorEstrategiaVacia.html")

@estrategias.route("/alta-estrategias-trig", methods=["POST"])
def alta_estrategias_trig():
    try:
        if request.method == 'POST':
            user_id = request.form['usuario_id']          
            correo_electronico = request.form['correo_electronico']
            cuenta = request.form['cuentaBroker']
            nombreEstrategia = request.form['nombreEstrategia']
           
            nombre = db.session.query(TriggerEstrategia).filter(TriggerEstrategia.nombreEstrategia == nombreEstrategia).first()

            if nombre is None:
                cuenta = Cuenta.query.filter_by(user_id=user_id, accountCuenta=cuenta).first()
                if cuenta:
                    print("Datos de la cuenta:")
                    print("ID:", cuenta.id)
                    print("User ID:", cuenta.user_id)
                    print("User Cuenta:", cuenta.userCuenta)
                    print("Password Cuenta:", cuenta.passwordCuenta)
                    print("Account Cuenta:", cuenta.accountCuenta)                
                    
                    hora_inicio = datetime(year=2023, month=7, day=3, hour=int(15), minute=int(00))
                    hora_fin = datetime(year=2023, month=7, day=3, hour=int(17), minute=int(00))
                    triggerEstrategia = TriggerEstrategia( 
                            id=None,   
                            user_id=user_id,
                            userCuenta=cuenta.userCuenta,
                            passwordCuenta=cuenta.passwordCuenta,
                            accountCuenta=cuenta.accountCuenta, 
                            horaInicio=hora_inicio,  # Ejemplo de hora de inicio (15:00)
                            horaFin=hora_fin,  # Ejemplo de hora de fin (17:00)     
                            ManualAutomatico = 'AUTOMATICO',
                            nombreEstrategia = nombreEstrategia    
                            )
                    
                
                    db.session.add(triggerEstrategia)  # Agregar la instancia de Cuenta a la sesión
                    db.session.commit()  # Confirmar los cambios
                    db.session.refresh(triggerEstrategia)  # Actualizar la instancia desde la base de datos para obtener el ID generado
                    triggerEstrategia_id = triggerEstrategia.id  # Obtener el ID generado
                    estrategias = db.session.query(TriggerEstrategia).join(Usuario).filter(TriggerEstrategia.user_id == user_id).all()
                    db.session.close()
                    
                    return render_template("/estrategias/panelControEstrategiaUser.html", datos=[user_id, estrategias])

    except:
        print('no hay estrategias')

    return render_template("/notificaciones/errorEstrategiaVacia.html")

@estrategias.route('/inicioEstrategias/')
def inicioEstrategias():
 try:
   get.pyRofexInicializada.get_account_position()
   return render_template('/estrategias.html')
 except:  
     print("contraseña o usuario incorrecto")  
     flash('Loggin Incorrect')    
     return render_template("login.html" )    
   
@estrategias.route('/detenerWS/', methods=["GET", "POST"])
def detenerWS():
    try:
        get.pyRofexInicializada.close_websocket_connection()

        # Obtener los datos por POST (cambia 'nombre_del_campo' al nombre correcto)
        usuario_id = request.form['usuario_id']

        # Llamar a la función estrategias_usuario_nadmin y pasar los datos por POST
        resultado_estrategias = estrategias_usuario_nadmin()

        # Hacer algo con el resultado de la función si es necesario

        
    except Exception as e:
        print('Error al detener WS:', str(e))
        return render_template("errorOperacion.html")  # Puedes renderizar una plantilla de error específica
 
@estrategias.route('/cargaDatosEstrategyUno/', methods = ['POST'])
def cargaDatosEstrategyUno():   
    if request.method == 'POST':         
        Ticker = request.form["Ticker"]   
        cantidad = request.form["cantidad"] 
        spread = request.form["spread"] 
        mensaje = Ticker+','+cantidad+','+spread
        
        inst = InstrumentoEstrategiaUno(Ticker, cantidad, spread)
       #00
        get.pyRofexInicializada.init_websocket_connection (market_data_handler,order_report_handler,error_handler,exception_error)
        tickers=[inst.instrument]
        print("tickers",tickers)
        entries = [get.pyRofexInicializada.MarketDataEntry.BIDS,
                    get.pyRofexInicializada.MarketDataEntry.OFFERS
                    ]   
        print("entries",entries)     
        instrumento_suscriptio = get.pyRofexInicializada.market_data_subscription(tickers,entries)
        print(instrumento_suscriptio)
        print(inst.instrument)
        # Subscribes to receive order report for the default account
        get.pyRofexInicializada.order_report_subscription(snapshot=True)
        return render_template('/estrategiaOperando.html')
    
    
@estrategias.route('/estrategyUno/')
def estrategyUno():     
    
    try:
        print()
        print()
        print("<<<--------EstrategyUno-------->>>>>")
        inst = InstrumentoEstrategiaUno("WTI/MAY23", 12, 0.05) 
        get.pyRofexInicializada.init_websocket_connection (market_data_handler,order_report_handler,error_handler,exception_error)
        tickers=[inst.instrument]
        print("_EstrategyUno_tickers_",tickers)
        entries = [get.pyRofexInicializada.MarketDataEntry.BIDS,
                    get.pyRofexInicializada.MarketDataEntry.OFFERS
                    ]   
        print("_EstrategyUno_entries_",entries)     
        print()
        instrumento_suscription = get.pyRofexInicializada.market_data_subscription(tickers,entries)
        print()
        print("_EstrategyUno_instrumento_suscriptio_",instrumento_suscription)
        print("_EstrategyUno_inst.instrument_",inst.instrument)
        # Subscribes to receive order report for the default account
        get.pyRofexInicializada.order_report_subscription(snapshot=True)
        return render_template('/estrategiaOperando.html')
    except:  
        print("_EstrategyUno_contraseña o usuario incorrecto")  
        flash('Loggin Incorrect')    
        return render_template("errorLogueo.html" ) 
    
       
@estrategias.route('/estrategyDos/')
def estrategyDos():     
    
    
    try:
        inst = InstrumentoEstrategiaUno("WTI/MAY23", 12, 0.05) 
        print("<<<--------estrategyDoooooooooooooooooooosssssss-------->>>>>")
        get.pyRofexInicializada.init_websocket_connection (handler_estrategyDos,o_r_handler_estrategyDos,error_handler,exception_error)
        tickers=[inst.instrument]
        print("tickers",tickers)
        entries = [get.pyRofexInicializada.MarketDataEntry.BIDS,
                    get.pyRofexInicializada.MarketDataEntry.OFFERS
                    ]   
        print("entries",entries)     
        instrumento_suscriptio = get.pyRofexInicializada.market_data_subscription(tickers,entries)
        print(instrumento_suscriptio)
        print(inst.instrument)
        # Subscribes to receive order report for the default account
        get.pyRofexInicializada.order_report_subscription(snapshot=True)
        return render_template('/estrategiaOperando.html')
    except:  
        print("contraseña o usuario incorrecto")  
        flash('Loggin Incorrect')    
        return render_template("errorLogueo.html" ) 
 
 
@estrategias.route('/estrategyPcDaniel/')
def estrategyPcDaniel():
    print("<<<<<<--------estrategyPcDaniel----->>>>>>>")
    variable1=123
    variable2=456
    variable3=789
    variable4=12458.21444
    return render_template('/estrategiaOperando.html')
 
    # Defines the handlers that will process the messages.
#<<<<<<<<<<<<<<<<<<-------------------AQUI SE DEFINE LA COMPRA Y VENTA AUTOMATICA DIRECTA -------------------->>>>>>>>>>>>>


@estrategias.route('/Estrategia_001/')
def Estrategia_001():
    try:
        inst = InstrumentoEstrategiaUno("WTI/MAY23", 12, 0.05) 
        print("_____________________Estrategia_001:...")
        get.pyRofexInicializada.init_websocket_connection (handler_Estrategia_001,o_r_handler_Estrategia_001,error_handler,exception_error)
        tickers=[inst.instrument]
        print("tickers",tickers)
        entries = [get.pyRofexInicializada.MarketDataEntry.BIDS,
                    get.pyRofexInicializada.MarketDataEntry.OFFERS
                    ]   
        print("entries",entries)     
        instrumento_suscriptio = get.pyRofexInicializada.market_data_subscription(tickers,entries)
        print(instrumento_suscriptio)
        print(inst.instrument)
        
        # Subscribes to receive order report for the default account
        get.pyRofexInicializada.order_report_subscription(snapshot=True)
        return render_template('/estrategiaOperando.html')
    except:  
        print("contraseña o usuario incorrecto")  
        flash('Loggin Incorrect')    
        return render_template("errorLogueo.html" ) 

    

def handler_Estrategia_001(message):
    # mensaje = Ticker+','+cantidad+','+spread
        print("_____________________Estrategia_001:...")
        print("Processing ddddddddddddddddddMarket Data Message Received: ",message)
        
                
        last_md = None
        bid = message["marketData"]["BI"]
        offer = message["marketData"]["OF"]
        symbol =  message["instrumentId"]["symbol"]
        price = message["marketData"]["BI"][0]["price"]
        orderQty = "3"
        if bid and offer:
           bid_px = bid[0]["price"]
           offer_px = offer[0]["price"]
           print("bid_px: ",bid_px," offer_px ",offer_px," symbol ",symbol," orderQty ",orderQty," price ",price)
           #datos = saaoperacionGral(bid,offer)
           #datos = saaoperacionGral(bid,offer)
           #datos = saaoperacionGral(bid,offer)
           get.pyRofexInicializada.send_order_via_websocket(ticker=symbol, side=get.pyRofexInicializada.Side.BUY, size=orderQty, order_type=get.pyRofexInicializada.OrderType.LIMIT,price=price)  
        
        else:
          InstrumentoEstrategiaUno._cancel_if_orders()
      


def o_r_handler_Estrategia_001(message):
  print("_____________________Estrategia_001:...")
  #print("Mensaje de OrderRouting: {0}".format(message))
  get.reporte_de_ordenes.append(message)



def handler_estrategyDos(message):
    # mensaje = Ticker+','+cantidad+','+spread
        print("Processing ddddddddddddddddddMarket Data Message Received: ",message)
        
                   
        last_md = None
        bid = message["marketData"]["BI"]
        offer = message["marketData"]["OF"]
        symbol =  message["instrumentId"]["symbol"]
        price = message["marketData"]["BI"][0]["price"]
        orderQty = "3"
        if bid and offer:
           bid_px = bid[0]["price"]
           offer_px = offer[0]["price"]
           print("bid_px: ",bid_px," offer_px ",offer_px," symbol ",symbol," orderQty ",orderQty," price ",price)
           get.pyRofexInicializada.send_order_via_websocket(ticker=symbol, side=get.pyRofexInicializada.Side.BUY, size=orderQty, order_type=get.pyRofexInicializada.OrderType.LIMIT,price=price)  
         
        else:
          InstrumentoEstrategiaUno._cancel_if_orders()




def o_r_handler_estrategyDos(message):
  
  #print("Mensaje de OrderRouting: {0}".format(message))
  get.reporte_de_ordenes.append(message)
      

  
    
def market_data_handler( message):
    
       # mensaje = Ticker+','+cantidad+','+spread
        print("Processing Market Data Message Received: {0}".format(message))
       # clientesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #clientesocket.connect(('localhost',8089))
        #clientesocket.send(format(message).encode())
       
        if InstrumentoEstrategiaUno.state is States.WAITING_MARKET_DATA:
            print("Processing Market Data Message Received: {0}".format(message))
            last_md = None
            bid = message["marketData"]["BI"]
            offer = message["marketData"]["OF"]
            if bid and offer:
                bid_px = bid[0]["price"]
                offer_px = offer[0]["price"]
                bid_offer_spread = round(offer_px - bid_px, 6) - 0.002
                if bid_offer_spread >= InstrumentoEstrategiaUno.spread:
                    if InstrumentoEstrategiaUno.my_order:
                        for order in InstrumentoEstrategiaUno.my_order.values():
                            if order["orderReport"]["side"] == "BUY" and \
                                    order["orderReport"]["price"] < bid_px:
                                InstrumentoEstrategiaUno._send_order(get.pyRofexInicializada.Side.BUY, bid_px + InstrumentoEstrategiaUno.tick, InstrumentoEstrategiaUno.buy_size)
                            elif order["orderReport"]["side"] == "SELL" and \
                                    order["orderReport"]["price"] > offer_px:
                                InstrumentoEstrategiaUno._send_order(get.pyRofexInicializada.Side.SELL, offer_px - InstrumentoEstrategiaUno.tick, InstrumentoEstrategiaUno.sell_size)
                    else:
                        if InstrumentoEstrategiaUno.buy_size > 0:
                            InstrumentoEstrategiaUno._send_order(get.pyRofexInicializada.Side.BUY, bid_px + InstrumentoEstrategiaUno.tick, InstrumentoEstrategiaUno.buy_size)
                        if InstrumentoEstrategiaUno.sell_size > 0:
                            InstrumentoEstrategiaUno._send_order(get.pyRofexInicializada.Side.SELL, offer_px - InstrumentoEstrategiaUno.tick, InstrumentoEstrategiaUno.sell_size)
                else:  # Lower spread
                    InstrumentoEstrategiaUno._cancel_if_orders()
            else:
                InstrumentoEstrategiaUno._cancel_if_orders()
        else:
            InstrumentoEstrategiaUno.last_md = message








    # Defines the handlers that will process the Order Reports.
def order_report_handler( order_report):
        print("Order Report Message Received: {0}".format(order_report))
        if order_report["orderReport"]["clOrdId"] in InstrumentoEstrategiaUno.my_order.keys():
            InstrumentoEstrategiaUno._update_size(order_report)
            if order_report["orderReport"]["status"] in ("NEW", "PARTIALLY_FILLED"):
                print("processing new order")
                InstrumentoEstrategiaUno.my_order[order_report["orderReport"]["clOrdId"]] = order_report
            elif order_report["orderReport"]["status"] == "FILLED":
                print("processing filled")
                del InstrumentoEstrategiaUno.my_order[order_report["orderReport"]["clOrdId"]]
            elif order_report["orderReport"]["status"] == "CANCELLED":
                print("processing cancelled")
                del InstrumentoEstrategiaUno.my_order[order_report["orderReport"]["clOrdId"]]

            if InstrumentoEstrategiaUno.state is States.WAITING_CANCEL:
                if not InstrumentoEstrategiaUno.my_order:
                    InstrumentoEstrategiaUno.state = States.WAITING_MARKET_DATA
                    if InstrumentoEstrategiaUno.last_md:
                        InstrumentoEstrategiaUno.market_data_handler(InstrumentoEstrategiaUno.last_md)
            elif InstrumentoEstrategiaUno.state is States.WAITING_ORDERS:
                for order in InstrumentoEstrategiaUno.my_order.values():
                    if not order:
                        return
                InstrumentoEstrategiaUno.state = States.WAITING_MARKET_DATA
                if InstrumentoEstrategiaUno.last_md:
                    InstrumentoEstrategiaUno.market_data_handler(InstrumentoEstrategiaUno.last_md)
                    
                    
                    
                    

def _update_size(order):
        if order["orderReport"]["status"] in ("PARTIALLY_FILLED", "FILLED"):
            if order["orderReport"]["side"] == "BUY":
                InstrumentoEstrategiaUno.buy_size -= round(order["orderReport"]["lastQty"])
            if order["orderReport"]["side"] == "SELL":
                InstrumentoEstrategiaUno.sell_size -= round(order["orderReport"]["lastQty"])
            if InstrumentoEstrategiaUno.sell_size == InstrumentoEstrategiaUno.buy_size == 0:
                InstrumentoEstrategiaUno.sell_size = InstrumentoEstrategiaUno.buy_size = InstrumentoEstrategiaUno.initial_size

def _cancel_if_orders():
        if InstrumentoEstrategiaUno.my_order:
            InstrumentoEstrategiaUno.state = States.WAITING_CANCEL
            for order in InstrumentoEstrategiaUno.my_order.values():
                get.pyRofexInicializada.cancel_order(order["orderReport"]["clOrdId"])
                print("canceling order %s" % order["orderReport"]["clOrdId"])

def _send_order( side, px, size):
        InstrumentoEstrategiaUno.state = States.WAITING_ORDERS
        order = get.pyRofexInicializada.send_order(
            ticker=InstrumentoEstrategiaUno.instrument,
            side=side,
            size=size,
            price=round(px, 6),
            order_type=get.pyRofexInicializada.OrderType.LIMIT,
            cancel_previous=True
        )
        InstrumentoEstrategiaUno.my_order[order["order"]["clientId"]] = None
        print("sending %s order %s@%s - id: %s" % (side, size, px, order["order"]["clientId"]))
        
        
        
##########################esto es para ws#############################
#Mensaje de MarketData: {'type': 'Md', 'timestamp': 1632505852267, 'instrumentId': {'marketId': 'ROFX', 'symbol': 'DLR/DIC21'}, 'marketData': {'BI': [{'price': 108.25, 'size': 100}], 'LA': {'price': 108.35, 'size': 3, 'date': 1632505612941}, 'OF': [{'price': 108.45, 'size': 500}]}}
def error_handler(message):
  print("Mensaje de error: {0}".format(message))
  
def exception_error(message):
  print("Mensaje de excepción: {0}".format(message))  
  {"type":"or","orderReport":{"orderId":"1128056","clOrdId":"user14545967430231","proprietary":"api","execId":"160127155448-fix1-1368","accountId":{"id":"30"},"instrumentId":{"marketId":"ROFX","symbol":"DODic21"},"price":18.000,"orderQty":10,"ordType":"LIMIT","side":"BUY","timeInForce":"DAY","transactTime":"20160204-11:41:54","avgPx":0,"lastPx":0,"lastQty":0,"cumQty":0,"leavesQty":10,"status":"CANCELLED","text":"Reemplazada"}}


  
  


   

