from pipes import Template
from unittest import result
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from models.usuario import Usuario
from models.cuentas import Cuenta
from models.triggerEstrategia import TriggerEstrategia
from datetime import datetime, timedelta, time
import smtplib
import schedule
import time
import strategies.estrategias as estrategias
from utils.common import Marshmallow, db
from datetime import datetime
import jwt

programar_trigger = Blueprint('programar_trigger', __name__)

# Crear la tabla cuenta si no existe
def crea_tabla_triggerEstrategia():
    hora_inicio = datetime(year=2023, month=7, day=3, hour=15, minute=0)
    hora_fin = datetime(year=2023, month=7, day=3, hour=17, minute=0)
    triggerEstrategia = TriggerEstrategia(    
        id=1,
        user_id = "1",
        userCuenta="mauriciodioli6603",
        passwordCuenta="zbwitW5#",
        accountCuenta="REM6603",  
        horaInicio=hora_inicio,  # Ejemplo de hora de inicio (15:00)
        horaFin=hora_fin,  # Ejemplo de hora de fin (17:00) 
        ManualAutomatico = "MANUAL",  
        nombreEstrategia = "sheet"     
    )
    triggerEstrategia.crear_tabla_triggerEstrategia()
    print("Tabla creada!")




@programar_trigger.route('/trigger/')
def trigger():
    
    return render_template("/automatizacion/trigger.html")

@programar_trigger.route('/programador_trigger/', methods=['POST'])
def programador_trigger():
    
    crea_tabla_triggerEstrategia()
    # Obtener las horas ingresadas por el usuario desde los datos enviados en el cuerpo de la solicitud
    horaInicio = request.json["horaInicio"]
    horaFin = request.json["horaFin"]
    cuenta =  request.json["cuenta"]    
    usuario =  request.json["usuario"]
    correoElectronico =  request.json["correoElectronico"]
    access_token = request.json["tokenAcceso"]
    accesoManualAutomatico =request.json["accesoManualAutomatico"]
    ##passwordCuenta=passwordCuenta_encoded,
    if access_token:
        app = current_app._get_current_object()
        try:
            user_id = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
            usuario_objeto = Usuario.query.get(user_id)  # Obtener el objeto Usuario correspondiente al user_id
            
            cuenta = Cuenta.query.filter_by(user_id=user_id).first()
            if cuenta:
                print("Datos de la cuenta:")
                print("ID:", cuenta.id)
                print("User ID:", cuenta.user_id)
                print("User Cuenta:", cuenta.userCuenta)
                print("Password Cuenta:", cuenta.passwordCuenta)
                print("Account Cuenta:", cuenta.accountCuenta)
                horaInicioSalvar, minutosInicioSalvar = horaInicio.split(':')
                horaFinSalvar, minutosFinSalvar = horaFin.split(':')
               
            hora_inicio = datetime(year=2023, month=7, day=3, hour=int(horaInicioSalvar), minute=int(minutosInicioSalvar))
            hora_fin = datetime(year=2023, month=7, day=3, hour=int(horaFinSalvar), minute=int(minutosFinSalvar))
            triggerEstrategia = TriggerEstrategia( 
                     id=None,   
                     user_id=user_id,
                     userCuenta=cuenta.userCuenta,
                     passwordCuenta=cuenta.passwordCuenta,
                     accountCuenta=cuenta.accountCuenta, 
                     horaInicio=hora_inicio,  # Ejemplo de hora de inicio (15:00)
                     horaFin=hora_fin,  # Ejemplo de hora de fin (17:00)     
                     ManualAutomatico = accesoManualAutomatico         
                            
                     )
            
           
            db.session.add(triggerEstrategia)  # Agregar la instancia de Cuenta a la sesión
            db.session.commit()  # Confirmar los cambios
            db.session.refresh(triggerEstrategia)  # Actualizar la instancia desde la base de datos para obtener el ID generado
            triggerEstrategia_id = triggerEstrategia.id  # Obtener el ID generado
           
            print("Auomatico registrada exitosamente!")
            print("automatico registrada usuario id !",triggerEstrategia_id)
         #   todasLasCuentas = get_cuentas_de_broker(user_id)
            triggerEstrategia1 = TriggerEstrategia.query.filter_by(id=triggerEstrategia_id).first() 
            db.session.close()
            render_template("/")
              
          #  for cuenta in todasLasCuentas:
           #       print(cuenta['accountCuenta'])

        except Exception as e:
            # Manejo específico de la excepción
            print("Error:", str(e))
            db.session.rollback()  # Hacer rollback de la sesión
            db.session.close()
            print("No se pudo registrar la hora a automatizar.")
        # Llamar a la función del trigger y pasarle las horas ingresadas
    programar_tareas(horaInicio, horaFin)

    return "Triggers programados"

def programar_tareas(horaInicio, horaFin):
    # Convertir las horas ingresadas en formato de cadena a objetos de fecha y hora
    horaInicio_deseada = datetime.strptime(horaInicio, "%H:%M")
    horaFin_deseada = datetime.strptime(horaFin, "%H:%M")

    # Obtener la hora actual
    hora_actual = datetime.now()

    # Calcular las diferencias de tiempo hasta las horas deseadas
    diferencia_tiempo_inicio = horaInicio_deseada - hora_actual
    diferencia_tiempo_fin = horaFin_deseada - hora_actual

    # Si las horas deseadas ya han pasado hoy, se ajustan para que sean las del próximo día
    if diferencia_tiempo_inicio.total_seconds() < 0:
        diferencia_tiempo_inicio += timedelta(days=1)
    if diferencia_tiempo_fin.total_seconds() < 0:
        diferencia_tiempo_fin += timedelta(days=1)

    # Programar las tareas de inicio y finalización a las horas deseadas
    schedule.every().day.at(horaInicio_deseada.strftime("%H:%M")).do(tarea_inicio)
    schedule.every().day.at(horaFin_deseada.strftime("%H:%M")).do(tarea_fin)

def tarea_inicio():
    print("Tarea de inicio ejecutada")
    # Programar la próxima ejecución después de 24 horas
    schedule.every(24).hours.do(tarea_inicio)

    # Aquí puedes enviar los datos a otra ruta en otro archivo Python
    # utilizando la librería requests o similar
    datos_usuario = {
        "nombre": "Usuario",
        "email": "usuario@example.com"
    }
    response = requests.post(url_for('estrategia_sheet_WS.estrategia_sheet_WS'), data=datos_usuario)

    if response.status_code == 200:
        print("Datos de usuario enviados con éxito")
    else:
        print("Error al enviar los datos de usuario")

def tarea_fin():
    print("Tarea de finalización ejecutada")
    # Programar la próxima ejecución después de 24 horas
    schedule.every(24).hours.do(tarea_fin)

    
    response = requests.get(url_for('estrategias.detenerWS'))

    if response.status_code == 200:
        print("Detener WS exitoso")
    else:
        print("Error al detener WS")
        



