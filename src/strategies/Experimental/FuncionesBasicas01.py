from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify,  make_response
import routes.instrumentos as instrumentos
import routes.api_externa_conexion.get_login as get
import routes.api_externa_conexion.validaInstrumentos as val
import routes.instrumentos as inst
from datetime import datetime
import enum
from models.instrumentoEstrategiaUno import InstrumentoEstrategiaUno
import socket
import requests
import time
import json
from models.orden import Orden
import random
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#import routes.api_externa_conexion.cuenta as cuenta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import os #obtener el directorio de trabajo actual
#import drive
#drive.mount('/content/gdrive')

# la pagina que me trae para aca es esta:
# C:\Users\dpuntillovirtual01\Documents\bot421\src\templates\estrategias.html
# este archivo
# C:\Users\dpuntillovirtual01\Documents\bot421\src\strategies\Experimental\FuncionesBasicas01.py
# test WS:   src\strategies\utils\testWS.py
# esta rutina de test se lanza tambien desde estrategias.html

FuncionesBasicas01 = Blueprint('FuncionesBasicas01',__name__)
#estrategia004 = Blueprint('estrategia004',__name__)

@FuncionesBasicas01.route('/basicas/', methods = ['POST'])
def basicas():
 if request.method == 'POST':
        try:
            # Obtén los datos enviados en la solicitud AJAX
            data = request.get_json()

            # Accede a los datos individualmente
            userCuenta = data['userCuenta']
            idTrigger = data['idTrigger']
            access_token = data['access_token']
            idUser = data['idUser']
            correo_electronico = data['correo_electronico']
            cuenta = data['cuenta']
            tiempoInicio = data['tiempoInicio']
            tiempoFin = data['tiempoFin']
            automatico = data['automatico']
            nombre = data['nombre']

            # Ahora puedes procesar estos datos como desees
            # ...

            # Devuelve una respuesta (opcional)
           # resp = {'redirect': '/paginaDePrueba/'}
            #resp = make_response(jsonify({'redirect': 'test'}))
           # resp.headers['Content-Type'] = 'application/json'
            #return jsonify({'redirect': url_for('strategies.Experimental.paginaDePrueba')}) 
            return ''
        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir
            return str(e), 400  # Devuelve un código de estado 400 en caso de error


       # print('llegamos a basicas ')
@FuncionesBasicas01.route('/paginaDePrueba/')
def paginaDePrueba():  
  return render_template('test.html')  


@FuncionesBasicas01.route('/estrategia028/')
def estrategia028():
  print("<<<<<<--------<<<<<<--------estrategia028----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia027/')
def estrategia027():
  print("<<<<<<--------<<<<<<--------estrategia027----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia026/')
def estrategia026():
  print("<<<<<<--------<<<<<<--------estrategia026----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia025/')
def estrategia025():
  print("<<<<<<--------<<<<<<--------estrategia025----->>>>>>>----->>>>>>>")
  return ''



# la pagina que me trae para aca es esta:
# \bot421\src\templates\estrategias.html
# este archivo
# \bot421\src\strategies\Experimental\FuncionesBasicas01.py


@FuncionesBasicas01.route('/estrategia024/')
def estrategia024():
  print("<<<<<<--------<<<<<<--------estrategia024----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia023/')
def estrategia023():
  print("<<<<<<--------<<<<<<--------estrategia023----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia022/')
def estrategia022():
  print("<<<<<<--------<<<<<<--------estrategia022----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia021/')
def estrategia021():
  print("<<<<<<--------<<<<<<--------estrategia021----->>>>>>>----->>>>>>>")
  return ''

# la pagina que me trae para aca es esta:
# \bot421\src\templates\estrategias.html
# este archivo
# \bot421\src\strategies\Experimental\FuncionesBasicas01.py


@FuncionesBasicas01.route('/estrategia020/')
def estrategia020():
  print("<<<<<<--------<<<<<<--------estrategia020----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia019/')
def estrategia019():
  print("<<<<<<--------<<<<<<--------estrategia019----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia018/')
def estrategia018():
  print("<<<<<<--------<<<<<<--------estrategia018----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia017/')
def estrategia017():
  print("<<<<<<--------<<<<<<--------estrategia017----->>>>>>>----->>>>>>>")
  return ''

# la pagina que me trae para aca es esta:
# \bot421\src\templates\estrategias.html
# este archivo
# \bot421\src\strategies\Experimental\FuncionesBasicas01.py

@FuncionesBasicas01.route('/estrategia016/')
def estrategia016():
  print("<<<<<<--------<<<<<<--------estrategia016----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia015/')
def estrategia015():
  print("<<<<<<--------<<<<<<--------estrategia015----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia014/')
def estrategia014():
  print("<<<<<<--------<<<<<<--------estrategia014----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia013/')
def estrategia013():
  print("<<<<<<--------<<<<<<--------estrategia013----->>>>>>>----->>>>>>>")
  return ''





# la pagina que me trae para aca es esta:
# \bot421\src\templates\estrategias.html
# este archivo
# \bot421\src\strategies\Experimental\FuncionesBasicas01.py

@FuncionesBasicas01.route('/estrategia012/')
def estrategia012():
  print("<<<<<<--------<<<<<<--------estrategia012----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia011/')
def estrategia011():
  print("<<<<<<--------<<<<<<--------estrategia011----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia010/')
def estrategia010():
  print("<<<<<<--------<<<<<<--------estrategia010----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia009/')
def estrategia009():
  print("<<<<<<--------<<<<<<--------estrategia009----->>>>>>>----->>>>>>>")
  return ''



@FuncionesBasicas01.route('/estrategia008/')
def estrategia008():
  print("<<<<<<--------<<<<<<--------estrategia008----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia007/')
def estrategia007():
  print("<<<<<<--------<<<<<<--------estrategia007----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia006/')
def estrategia006():
  print("<<<<<<--------<<<<<<--------estrategia006----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia005/')
def estrategia005():
  print("<<<<<<--------<<<<<<--------estrategia005----->>>>>>>----->>>>>>>")
  return ''


@FuncionesBasicas01.route('/estrategia004/')
def estrategia004():
  print("<<<<<<--------<<<<<<--------estrategia004----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia003/')
def estrategia003():
  print("<<<<<<--------<<<<<<--------estrategia003----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia002/')
def estrategia002():
  print("<<<<<<--------<<<<<<--------estrategia002----->>>>>>>----->>>>>>>")
  return ''
@FuncionesBasicas01.route('/estrategia001/')#,methods=['POST'])
def estrategia001():
  print("<<<<<<--------<<<<<<--------estrategia001----->>>>>>>----->>>>>>>")
  
  #return render_template('/estrategiaOperando.html')
  return ''










# la pagina que me trae para aca es esta:
# \bot421\src\templates\estrategias.html
# este archivo
# \bot421\src\strategies\Experimental\FuncionesBasicas01.py



# calculo del mep AL30 con websoket
def MepAl30WS(message):
     
     
  #  resultado = instrument_by_symbol_para_CalculoMep(message)    
  #  resultado2 = instrument_by_symbol_para_CalculoMep(message) 
    
    
    #if isinstance(message["marketData"]["OF"][0]["price"],float):
    #precio = message["marketData"]["OF"][0]["price"]
    #if isinstance(message["marketData"]["OF"][0]["size"],int):
    #Liquidez_ahora_cedear = message["marketData"]["OF"][0]["size"]


    #if len( message['marketData']['OF']) == 0:
    #if not isinstance(message["marketData"]["OF"][0]["size"],int):# entra si el offer esta vacio
        # entra si el offer esta vacio
    #    print(" FUN calcularMepAl30WS: La clave 'OF' está vacía.")
    #else:

    #    al30_ci = message['marketData']['OF'][0]['price'] #vendedora OF
    #    al30D_ci =message['marketData']['BI'][0]['price'] #compradora BI
        #print("__________al30_ci____________",al30_ci)
        #print("__________al30D_ci____________",al30D_ci)
        
        # simulo compra de bono      
        #print("____simulo compra de bono ")  
        # al30ci_unitaria = al30_ci/100
        #cantidad_al30ci=int(10000/al30ci_unitaria)
        #print("__________cantidad_al30ci_________",cantidad_al30ci)
        
        # ahora simulo la venta de los bonos D
        #print("ahora simulo la venta de los bonos D")
        #al30D_ci_unitaria = al30D_ci/100
        #dolaresmep = al30D_ci_unitaria * cantidad_al30ci
        #mep = 10000 / dolaresmep
    mep = 380
    #print(" FUN calcularMepAl30WS: .")
    return mep
