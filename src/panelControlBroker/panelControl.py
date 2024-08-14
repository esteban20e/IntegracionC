# Creating  Routes
from pipes import Template
from unittest import result
from flask import current_app

import requests
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from models.instrumento import Instrumento
from utils.db import db
import routes.api_externa_conexion.get_login as get
import jwt
from models.usuario import Usuario
from models.cuentas import Cuenta
from models.orden import Orden
import threading
import strategies.datoSheet as datoSheet
import time
from flask import abort

panelControl = Blueprint('panelControl',__name__)

def obtener_pais():
    ip = request.remote_addr
    response = requests.get(f'http://ipinfo.io/{ip}')
    data = response.json()
    pais = data.get('country')
    return f'El país de la conexión es: {pais}'


@panelControl.route('/panel_control_sin_cuenta')
def panel_control_sin_cuenta():
   
    pais = request.args.get('country')
    layout = request.args.get('layoutOrigen')
    usuario_id = request.args.get('usuario_id')
    
    respuesta =  llenar_diccionario_cada_15_segundos_sheet(pais)
    
    if determinar_pais(pais)  is not None:
     
     datos_desempaquetados = forma_datos_para_envio_paneles(get.diccionario_global_sheet[pais],usuario_id)
     if len(datos_desempaquetados) != 0:
       get.diccionario_global_sheet_intercambio = datos_desempaquetados
     else:
       datos_desempaquetados = forma_datos_para_envio_paneles(get.diccionario_global_sheet[pais],usuario_id)
    else:
      enviar_leer_sheet(pais)
      datos_desempaquetados = forma_datos_para_envio_paneles(get.diccionario_global_sheet[pais],usuario_id)
    
    if layout == 'layout_signal':
        return render_template("/paneles/panelSheetCompleto.html", datos = datos_desempaquetados)
    if layout == 'layout': 
        return render_template("/paneles/panelSheetCompleto.html", datos = datos_desempaquetados)
    if layout == 'layout' or layout == 'layoutConexBroker':        
        return render_template("/paneles/panelDeControlBroker.html", datos = datos_desempaquetados)
    return "Página no encontrada"  # Cambia el mensaje según sea necesario

@panelControl.route("/panel_control")
def panel_control():
     pais = request.args.get('country')
     layout = request.args.get('layoutOrigen')
     usuario_id = request.args.get('usuario_id')
     
     
     respuesta =  llenar_diccionario_cada_15_segundos_sheet(pais)
     if  determinar_pais(pais) is not None:
        datos_desempaquetados = forma_datos_para_envio_paneles(get.diccionario_global_sheet[pais],usuario_id)
     else:
        enviar_leer_sheet(pais)
        datos_desempaquetados = forma_datos_para_envio_paneles(get.diccionario_global_sheet[pais],usuario_id)
 
         
     if layout == 'layout_signal':
        return render_template("/paneles/panelSignalSinCuentas.html", datos = datos_desempaquetados)
     if layout == 'layout' or layout == 'layoutConexBroker':      
        return render_template("/paneles/panelSignalConCuentas.html", datos = datos_desempaquetados)
     return "Página no encontrada"  # Cambia el mensaje según sea necesario

@panelControl.route("/panel_control_atomatico/<pais>/<usuario_id>")
def panel_control_atomatico(pais,usuario_id):
     
     if  determinar_pais(pais) is not None:
       datos_desempaquetados = forma_datos_para_envio_paneles(get.diccionario_global_sheet[pais],usuario_id)
     else:
        enviar_leer_sheet(pais)
        datos_desempaquetados = forma_datos_para_envio_paneles(get.diccionario_global_sheet[pais],usuario_id)
 
     if datos_desempaquetados:
     # print(datos_desempaquetados)
      return jsonify(datos=datos_desempaquetados)


def forma_datos_para_envio_paneles(ContenidoSheet, usuario_id):
    if not ContenidoSheet:
        return False

    datos_desempaquetados = list(ContenidoSheet)[2:]  # Desempaqueta los datos y omite las dos primeras filas
    datos_procesados = []

    for i, tupla_exterior in enumerate(datos_desempaquetados):
        dato = list(tupla_exterior)  # Convierte la tupla interior a una lista

        with db.session.begin(subtransactions=True):
            orden_existente = db.session.query(Orden).filter_by(symbol=dato[0], user_id=usuario_id).first()

            if orden_existente:
                dato_extra = (orden_existente.clOrdId_alta_timestamp, orden_existente.senial)
                dato += dato_extra
            else:
                dato += (None, None)

            dato.append(i+1)
            datos_procesados.append(tuple(dato))

    return datos_procesados

def llenar_diccionario_cada_15_segundos_sheet(pais):
    get.hilo_iniciado_panel_control

    # Verifica si ya hay un hilo iniciado para este país
    if pais in get.hilo_iniciado_panel_control and get.hilo_iniciado_panel_control[pais].is_alive():
        return f"Hilo para {pais} ya está en funcionamiento"

    # Si no hay un hilo iniciado para este país, lo inicia
    hilo = threading.Thread(target=ejecutar_en_hilo, args=(pais,))
    get.hilo_iniciado_panel_control[pais] = hilo
    hilo.start()

    return f"Hilo iniciado para {pais}"

def ejecutar_en_hilo(pais):
    while True:
        time.sleep(120)
        print("ENTRA A THREAD Y LEE EL SHEET")
        enviar_leer_sheet(pais)
        

def enviar_leer_sheet(pais):
      
     if pais not in ["argentina", "usa"]:
        # Si el país no es válido, retorna un código de estado HTTP 404 y un mensaje de error
        abort(404, description="País no válido")
        
     if pais == "argentina":
         ContenidoSheet =  datoSheet.leerSheet(get.SPREADSHEET_ID_PRUEBA,'bot')
     elif pais == "usa":
          ContenidoSheet =  datoSheet.leerSheet(get.SPREADSHEET_ID_PRODUCCION,'drpibotUSA')
     else:
         return "País no válido"
     get.diccionario_global_sheet[pais] ={}
     get.diccionario_global_sheet[pais] =list(ContenidoSheet)

def determinar_pais(pais):
    if hasattr(get, 'diccionario_global_sheet') and isinstance(get.diccionario_global_sheet, dict):
        # Asegúrate de que 'get.diccionario_global_sheet' exista y sea un diccionario

        lista_asociada = get.diccionario_global_sheet.get(pais, None)
        if lista_asociada is not None:
           # print(f"La lista asociada a {pais} es: {lista_asociada}")
            return lista_asociada
        else:
            #print(f"No se encontró una lista asociada a {pais}")
            return None
    else:
        print(f"'get.diccionario_global_sheet' no está disponible o no es un diccionario con las listas asociadas a los países.")
        return None

    
     