from utils.common import Marshmallow, db
from ast import Return
from http.client import UnimplementedFileMode

import json
from datetime import datetime
from re import template
from socket import socket
import pyRofex
# datetime.date.today()
import websocket
import requests
import jwt
import re
import os
import routes.api_externa_conexion.validaInstrumentos as valida

from routes.api_externa_conexion.wsocket import wsocketConexion as conexion
from fichasTokens.fichas import refrescoValorActualCuentaFichas
import routes.instrumentos as inst
from models.instrumento import Instrumento
import routes.api_externa_conexion.cuenta as cuenta
import ssl
from models.usuario import Usuario
from models.cuentas import Cuenta

from utils.db import db
from datetime import datetime
import time
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies
    
)
from flask import (
    Flask,
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    current_app,
    g,
    make_response
)


get_login = Blueprint('get_login',__name__)

 
user = "{{usuario}}" 
password = "{{contraseña}}" 
account = "{{cuenta}}"  
market_data_recibida = []
reporte_de_ordenes = []


SPREADSHEET_ID_PRUEBA='1yQeBg8AWinDLaErqjIy6OFn2lp2UM8SRFIcVYyLH4Tg'#drpiBot3 de pruba
SPREADSHEET_ID_PRODUCCION='1GMv6fwa1-4iwhPBZqY6ZNEVppPeyZY0R4JB39Xmkc5s'#drpiBot de produccion
SPREADSHEET_ID_USA='1sxbKe5pjF3BsGgUCUzBDGmI-zV5hWbd6nzJwRFw3yyU'#de produccion USA

VariableParaTiemposMDHandler = 0
accountLocalStorage = ""
VariableParaBotonPanico = 0
VariableParaSaldoCta = 0
pyRofexInicializada = pyRofex
pyConectionWebSocketInicializada = pyRofex
pyWsSuscriptionInicializada = pyRofex
diccionario_global_operaciones = {}
diccionario_operaciones_enviadas = {}
diccionario_global_sheet = {}
diccionario_global_sheet_intercambio = {}
hilo_iniciado_panel_control = {}  # Un diccionario para mantener los hilos por país
ultima_entrada = time.time()
# Configurar las URLs de la instancia de BMB
api_url = "https://api.bull.xoms.com.ar/"
ws_url = "wss://api.bull.xoms.com.ar/"





# Creating  Routes
#@get_login.route("/index")
#def index(): 
  
#   all_mer = Instrumento.query.all()
#   print("all_mer",all_mer)  
#   return render_template('index.html', datos = all_mer)


# Creating simple Routes
@get_login.route("/loginApi")
def loginApi():  
 return render_template("login.html")

@get_login.route('/home')
def home():
    return render_template('home.html')

@get_login.route("/panel_control_broker", methods=['GET'])
def panel_control_broker():
     if request.method == 'GET':       
       
        cuenta = []#si va cero entonces no cargar localstorage
        return render_template("/paneles/panelDeControlBroker.html", datos = cuenta)

@get_login.route("/loginExtAutomatico", methods=['POST'])
def loginExtAutomatico():
    print('get_login.loginExtAutomatico ')
    if request.method == 'POST':
        try:
            #selector = request.form.get('environment')
            selector = request.json.get('simuladoOproduccion')
            access_token = request.json.get('access_token')
            rutaDeLogeo =  request.json.get('origin_page')
            refresh_token = request.json.get('refresh_token')
            correo_electronico = request.json.get('correo_electronico')
            user = request.json.get('usuario')
            account = request.json.get('cuenta')
            simuladoOproduccion = request.json.get('simuladoOproduccion')
           # print('access_token ',access_token)
           # print('refresh_token ',refresh_token)
           # print('correo_electronico ',correo_electronico)
           
            if access_token:
                app = current_app._get_current_object()                    
                user_id = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
                exp_timestamp = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['exp']
                environment = pyRofexInicializada.Environment.REMARKET if selector == 'simulado' else pyRofexInicializada.Environment.LIVE
                print(f"Está enviando a {environment}")
                if account is not None and account != '':   
                   cuentas = db.session.query(Cuenta).filter(Cuenta.accountCuenta == account).first()
                   db.session.close()
                   passwordCuenta = cuentas.passwordCuenta
                   passwordCuenta = passwordCuenta.decode('utf-8')
                    
                   if  simuladoOproduccion !='':
                        if simuladoOproduccion =='simulado':
                            try:
                                            environment =pyRofexInicializada.Environment.REMARKET
                                            
                                          #  WsEndPoint ='wss://api.remarkets.primary.com.ar/'
                                          #  urlEndPoint= 'https://api.remarkets.primary.com.ar/'
                                          #  pyRofexInicializada._set_environment_parameter("url", urlEndPoint,environment)
                                          #  pyRofexInicializada._set_environment_parameter("ws",WsEndPoint,environment) 
                                          #  pyRofexInicializada._set_environment_parameter("proprietary", "PBCP", environment)
                                         
                                            pyRofexInicializada.initialize(user=cuentas.userCuenta,password=passwordCuenta,account=cuentas.accountCuenta,environment=environment )
                                            conexion() 
                                            refrescoValorActualCuentaFichas(user_id)                                    
                                            print("está logueado en simulado en REMARKET")
                                            if rutaDeLogeo == 'Home':  
                                                resp = make_response(jsonify({'redirect': 'home', 'cuenta': account, 'userCuenta': cuentas.userCuenta, 'selector': selector}))
                                                resp.headers['Content-Type'] = 'application/json'
                                                set_access_cookies(resp, access_token)
                                                set_refresh_cookies(resp, refresh_token)
                                                return resp
                                            else:                                          
                                                resp = make_response(jsonify({'redirect': 'panel_control_broker'}))
                                                resp.headers['Content-Type'] = 'application/json'
                                                set_access_cookies(resp, access_token)
                                                set_refresh_cookies(resp, refresh_token)
                                                return resp
                            except:
                                #  print("contraseña o usuario incorrecto")
                              flash('Loggin Incorrect')
                              return render_template("errorLogueo.html")
                        else:
                            exp_date = datetime.utcfromtimestamp(exp_timestamp)
                            fecha_actual =   datetime.utcnow()
                            if fecha_actual > exp_date:
                                environment = pyRofexInicializada.Environment.LIVE
                
                                pyRofexInicializada._set_environment_parameter("url", api_url,environment)
                                pyRofexInicializada._set_environment_parameter("ws", ws_url,environment) 
                                pyRofexInicializada._set_environment_parameter("proprietary", "PBCP", environment)
                                pyRofexInicializada.initialize(user=cuentas.userCuenta,password=passwordCuenta,account=cuentas.accountCuenta,environment=environment )
                                conexion()
                                refrescoValorActualCuentaFichas(user_id)
                                print("está logueado en produccion en LIVE")
                                if rutaDeLogeo != 'Home':      
                                 return render_template("/paneles/panelDeControlBroker.html")   
                                else:
                                    resp = make_response(jsonify({'redirect': 'panel_control_broker'}))
                                    resp.headers['Content-Type'] = 'application/json'
                                    set_access_cookies(resp, access_token)
                                    set_refresh_cookies(resp, refresh_token)
                                    return resp 
                            else:
                                 
                                  # return render_template('paneles/panelDeControlBroker.html', cuenta=[accountCuenta, user, selector])
                                  resp = make_response(jsonify({'redirect': 'panel_control_broker'}))
                                  resp.headers['Content-Type'] = 'application/json'
                                  set_access_cookies(resp, access_token)
                                  set_refresh_cookies(resp, refresh_token)
                                  return resp 
                else: 
                    return render_template('home.html', cuenta=[account,user,simuladoOproduccion]) 
            else:
                  return jsonify({'redirect': url_for('panelControl.panel_control')}) 
                    
        except jwt.InvalidTokenError:
            print("El token es inválido")
        except jwt.ExpiredSignatureError:
            print("El token ha expirado")
        except Exception as e:
            print("Otro error:", str(e))
        return render_template("cuentas/registrarCuentaBroker.html")





@get_login.route("/loginExtCuentaSeleccionadaBroker", methods=['POST'])
def loginExtCuentaSeleccionadaBroker():
     if request.method == 'POST':
        origin_page = request.form.get('origin_page')
        user = request.form.get('usuario')
        password = request.form.get('contraseña')
        accountCuenta = request.form.get('cuenta')
        access_token = request.form.get('access_token')
        
        if origin_page == 'login':
            selector = request.form.get('environment')
        else: 
            selector = request.form.get('selectorEnvironment')
        
        
       
        if not selector or not user or not password or not account:
            flash('Falta información requerida')
            return redirect(url_for('autenticacion.index'))

        try:
            inicializar_variables_globales()
            #creaJsonParaConextarseSheetGoogle()
            if selector == 'simulado':
                # Configurar para el entorno de simulación
                environments = pyRofexInicializada.Environment.REMARKET
              #  WsEndPoint ='wss://api.remarkets.primary.com.ar/'
              #  urlEndPoint= 'https://api.remarkets.primary.com.ar/'
              #  pyRofexInicializada._set_environment_parameter("url", urlEndPoint,environments)
              #  pyRofexInicializada._set_environment_parameter("ws",WsEndPoint,environments) 
              #  pyRofexInicializada._set_environment_parameter("proprietary", "PBCP", environments)
                                         
            else:
                # Configurar para el entorno LIVE
                environments = pyRofexInicializada.Environment.LIVE
                
                pyRofexInicializada._set_environment_parameter("url", api_url,environments)
                pyRofexInicializada._set_environment_parameter("ws", ws_url,environments) 
                pyRofexInicializada._set_environment_parameter("proprietary", "PBCP", environments)
               

                    
            print(f"Está enviando a {environments}")
            if access_token:
                user_id = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
                # Aquí puedes realizar operaciones relacionadas con el usuario si es necesario.
            
            pyRofexInicializada.initialize(user=user,password=password,account=accountCuenta,environment=environments )
            conexion()
            refrescoValorActualCuentaFichas(user_id)
           
           
            print(f"Está logueado en {selector} en {environments}")
            
            
        except jwt.ExpiredSignatureError:
            flash("El token ha expirado")
        except jwt.InvalidTokenError:
            flash("El token es inválido")
        except Exception as e:
            print('Error inesperado:', e)
            flash('No se pudo iniciar sesión')
            return render_template('errorLogueo.html')
            
 # Redirige a la página de origen según el valor de origin_page
        if origin_page == 'login':
            return render_template('home.html', cuenta=[accountCuenta, user, selector])
        elif origin_page == 'cuentasDeUsusario':
            return render_template('paneles/panelDeControlBroker.html', cuenta=[accountCuenta, user, selector])
        else:
            # Si origin_page no coincide con ninguna ruta conocida, redirige a una página por defecto.
            return render_template('registrarCuentaBroker.html')



def inicializar_variables_globales():
    global pyRofexInicializada, pyConectionWebSocketInicializada, pyWsSuscriptionInicializada
    
    
   

    pyRofexInicializada = pyRofex
    pyConectionWebSocketInicializada = pyRofex
    pyWsSuscriptionInicializada = pyRofex
    
    



  

#  reporte_de_ordenes.append(message)

   
def error_handler(message):
  print("Mensaje de error: {0}".format(message))

def exception_handler(e):
    print("Exception Occurred: {0}".format(e.msg))


       #ws.webSocket() ### AQUI FALTA HACER LA PANTALLA EN DONDE ELIJO LOS INSTRUMENTOS PARA SUSCRIBIRME 
       # repuesta_listado_instrumento = pyRofexInicializada.get_detailed_instruments()
       # listado_instrumentos = repuesta_listado_instrumento['instruments']
       # tickers_existentes = obtener_array_tickers(listado_instrumentos)
        #print(tickers_existentes)
       # mis_instrumentos = ["DLR/NOV22", "SOJ.ROS/MAY22","DLR/JUN22", "MERV - XMEV - TSLA - 48hs"]
       # instrumentos_existentes = valida.validar_existencia_instrumentos(mis_instrumentos,tickers_existentes)
        #print(instrumentos_existentes)
        
        ##aqui se conecta al ws
       # pyRofexInicializada.init_websocket_connection(market_data_handler,order_report_handler,error_handler,exception_error)
        #### aqui define el MarketDataEntry
       # entries = [pyRofexInicializada.MarketDataEntry.BIDS,
       #    pyRofexInicializada.MarketDataEntry.OFFERS,
       #    pyRofexInicializada.MarketDataEntry.LAST]        
        #instrumento_suscriptio =  pyRofexInicializada.market_data_subscription(instrumentos_existentes,entries)
        #print(instrumento_suscriptio)
       # pyRofexInicializada.order_report_subscription(snapshot=True)
       # saldo=obtenerSaldoCuenta()
        #print(saldo)
        ####aqui compro        
       # comprar('DLR/NOV22',25,108.25,pyRofex.OrderType.LIMIT)
        #vender('DLR/NOV22',25,108.25,pyRofex.OrderType.LIMIT)
      # actualizarTablaMD()
        
        





 

  
  

  
 
    




