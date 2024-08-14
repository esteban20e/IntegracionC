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




cuenta = Blueprint('cuenta',__name__)

# Crear la tabla cuenta si no existe
def crea_tabla_cuenta():
    cuenta = Cuenta(    
        id=1,
        user_id = "1",
        userCuenta="mauriciodioli6603",
        passwordCuenta="zbwitW5#",
        accountCuenta="REM6603",
        selector="simulado"                
    )
    cuenta.crear_tabla_cuentas()
    print("Tabla creada!")



@cuenta.route("/cuentas",  methods=["GET"])
def cuentas():
   
   
   try:
      if request.method == 'GET': 
   ####   AQUI TENGO QUE COMPARA LA FECHA ####     
      
         infoCuenta = obtenerCuenta()
         print(infoCuenta)
         
         return render_template("cuenta.html",datos = infoCuenta)
   except:  
        print("contraseña o usuario incorrecto")  
        flash('Loggin Incorrect')    
        return render_template("errorLogueo.html" ) 
     ##~######datos de la cuenta
def obtenerSaldoCuenta(cuenta):
  # print("_______________obtenerSaldoCuenta__________________")
   resumenCuenta = get.pyRofexInicializada.get_account_report(account=cuenta)
   return resumenCuenta["accountData"]["availableToCollateral"]

def obtenerCuenta(cuenta=None):
   resumenCuenta = get.pyRofexInicializada.get_account_report(account=cuenta)
   return resumenCuenta

@cuenta.route("/posicionCuenta")
def posicionCuenta():
     try:
        
        repuesta_cuenta = get.pyRofexInicializada.get_account_position()
        reporte = repuesta_cuenta['positions']
        if len(reporte)!=0:
          print("posicion cuentaaaaaaaaaaaaaaaaaaaaaa ",reporte)
          return render_template("cuentaPosicion.html",datos = reporte)
        else:
          return render_template("notificaciones/noPoseeDatos.html")
     except:  
        print("contraseña o usuario incorrecto")  
        flash('No registra posicion')    
          
     return render_template("login.html" )

@cuenta.route("/detalleCuenta")
def detalleCuenta():
   try:        
        repuesta_cuenta = get.pyRofexInicializada.get_detailed_position()
        reporte = repuesta_cuenta['detailedPosition']
        
        print("detalle cuentaaaaaaaaaaaaaaaaaaaaaa ",reporte)
        
        return render_template("cuentaDetalles.html",datos = reporte)
     
   except:  
        print("contraseña o usuario incorrecto")  
        flash('Loggin Incorrect')    
          
   return render_template("login.html" )

@cuenta.route("/reporteCuenta")
def reporteCuenta():
   try:        
        repuesta_cuenta = get.pyRofexInicializada.get_account_report()
        reporte = repuesta_cuenta['accountData']
        
        print("detalle cuentaaaaaaaaaaaaaaaaaaaaaa ",reporte)
        return render_template("cuenta.html",datos = reporte)
   except:  
      print("contraseña o usuario incorrecto")  
      flash('Loggin Incorrect')    
      return render_template("login.html" )
   
@cuenta.route("/registrar_cuenta_broker")
def registrar_cuenta_broker():
   
   return render_template("cuentas/registrarCuentaBroker.html")

@cuenta.route("/cuentas_de_broker_usuario_")
def cuentas_de_broker_usuario_():
     todasLasCuentas =  get_cuentas_de_broker_usuario()
     return render_template('cuentasDeUsuario.html', datos=todasLasCuentas)
    
@cuenta.route("/registrar_cuenta",  methods=["POST"])
def registrar_cuenta():
   if request.method == 'POST':
         todasLasCuentas = []
       
         access_token = request.form['access_token']
         correo_electronico  = request.form['correo_electronico']
         
         userCuenta = request.form['usuario']
         passwordCuenta = request.form['contraseña']
         accountCuenta = request.form['cuenta']
         selector = request.form['environment']
         print("___________cuentas___________userCuenta",userCuenta)
        
         print("___________cuentas___________accountCuenta",accountCuenta)
         print("___________cuentas___________correo_electronico",correo_electronico)
         # Codificar las cadenas usando UTF-8
         userCuenta_encoded = userCuenta.encode('utf-8')
         passwordCuenta_encoded = passwordCuenta.encode('utf-8')
         accountCuenta_encoded = accountCuenta.encode('utf-8')

         if access_token:
            app = current_app._get_current_object()
            
            try:
               user_id = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
               crea_tabla_cuenta()
               
               usuario = Usuario.query.get(user_id)  # Obtener el objeto Usuario correspondiente al user_id
               if selector == '1':
                  selectorStr = 'simulado'
               else: 
                  selectorStr = 'produccion'

               cuenta = Cuenta( 
                     id=None,   
                     user_id=user_id,
                     userCuenta=userCuenta_encoded,
                     passwordCuenta=passwordCuenta_encoded,
                     accountCuenta=accountCuenta_encoded,
                     selector=selectorStr              
                     )
               cuenta.user = usuario  # Asignar el objeto Usuario a la propiedad user de la instancia de Cuenta
               db.session.add(cuenta)  # Agregar la instancia de Cuenta a la sesión
               db.session.commit()  # Confirmar los cambios
               db.session.close()
              
               todasLasCuentas = get_cuentas_de_broker(user_id)
               print("Cuenta registrada exitosamente!")
               print("Cuenta registrada usuario id !",user_id)
               for cuenta in todasLasCuentas:
                  print(cuenta['accountCuenta'])
                  passwordCuenta = cuenta['passwordCuenta']
                  passwordCuenta_decoded = passwordCuenta.decode('utf-8')
                  print(passwordCuenta_decoded)

            except Exception as e:               
                db.session.rollback()  # Hacer rollback de la sesión
                db.session.close()
                flash('"No se pudo registrar la cuenta, la cuenta ya tiene usuario asignado.')
                print("No se pudo registrar la cuenta, la cuenta ya tiene usuario asignado.",e)
                
    
   return render_template('cuentas/registrarCuentaBroker.html')

@cuenta.route("/registro-Cuenta-administracion/",  methods=["POST"])
def registrar_cuenta_administracion():
   if request.method == 'POST':
         todasLasCuentas = []
         correo_electronico = request.form['userSistema']
         userCuenta = request.form['userCuentaBroker']
         passwordCuenta = request.form['passwordCuentaBroker']
         accountCuenta = request.form['accountCuentaBroker']
         print("___________cuentas___________userCuenta",userCuenta)
        
         print("___________cuentas___________accountCuenta",accountCuenta)
         print("___________cuentas___________correo_electronico",correo_electronico)
         # Codificar las cadenas usando UTF-8
         userCuenta_encoded = userCuenta.encode('utf-8')
         passwordCuenta_encoded = passwordCuenta.encode('utf-8')
         accountCuenta_encoded = accountCuenta.encode('utf-8')

         crea_tabla_cuenta()
         try:     
            usuario = Usuario.query.filter_by(correo_electronico=correo_electronico).first()  # Obtener el objeto Usuario correspondiente al user_id

            cuenta = Cuenta( 
                        id=None,   
                        user_id=usuario.id,
                        userCuenta=userCuenta_encoded,
                        passwordCuenta=passwordCuenta_encoded,
                        accountCuenta=accountCuenta_encoded                
                        )
          
            db.session.add(cuenta)  # Agregar la instancia de Cuenta a la sesión
            db.session.commit()  # Confirmar los cambios
            db.session.refresh(cuenta)  # Actualizar la instancia desde la base de datos para obtener el ID generado
            cuenta_id = cuenta.id  # Obtener el ID generado
           
            print("Auomatico registrada exitosamente!")
            print("automatico registrada usuario id !",cuenta_id)
         #   todasLasCuentas = get_cuentas_de_broker(user_id)
            
            cuentasBroker = db.session.query(Cuenta).all()
            
            db.session.close()
            print("Cuenta registrada exitosamente!")            

            return render_template("/cuentas/cuntasUsuariosBrokers.html",datos = cuentasBroker)
             
         except:               
                db.session.rollback()  # Hacer rollback de la sesión
                db.session.close()
                print("No se pudo registrar la cuenta.")
                return 'problemas con la base de datos'
  

def get_cuentas_de_broker(user_id):
    
    print("_______________________get_cuentas_de_broker_usuario",user_id)
    todasCuentas = []
    try:
        # Obtener el objeto Usuario correspondiente al user_id
        usuario = Usuario.query.get(user_id)         
        # Buscar todas las cuentas asociadas a ese usuario
        cuentas = db.session.query(Cuenta).filter(Cuenta.user_id == user_id).all()
        if cuentas:
            print("El usuario", usuario.correo_electronico, "tiene las siguientes cuentas asociadas:")
            for cuenta in cuentas:
                password_cuenta = cuenta.passwordCuenta.decode('utf-8')
                todasCuentas.append({'id': cuenta.id, 'accountCuenta': cuenta.accountCuenta,'userCuenta':cuenta.userCuenta,'passwordCuenta':password_cuenta, 'selector':cuenta.selector})
                print(cuenta.accountCuenta)    
        else:
            print("El usuario", usuario.nombre, "no tiene ninguna cuenta asociada.")
    except:
        print("No se pudo obtener las cuentas del usuario.")
    db.session.close()
    return todasCuentas




@cuenta.route("/get_cuentas_de_broker_usuario",  methods=["POST"])   
def get_cuentas_de_broker_usuario():
     if request.method == 'POST':
       
         access_token = request.form['access_token']
         todasLasCuentas = []
         if access_token:
            app = current_app._get_current_object()
            
            try:
               user_id = jwt.decode(access_token.encode(), app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']

              # user_id = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
                # Obtener el objeto Usuario correspondiente al user_id
               usuario = Usuario.query.get(user_id)         
              # Buscar todas las cuentas asociadas a ese usuario
               cuentas = db.session.query(Cuenta).join(Usuario).filter(Cuenta.user_id == user_id).all()

               if cuentas:
                  print("El usuario", usuario.correo_electronico, "tiene las siguientes cuentas asociadas:")
                  
                  for cuenta in cuentas:
                   todasLasCuentas.append(cuenta.accountCuenta)
                   password_cuenta = cuenta.passwordCuenta.decode('utf-8')
                   todasLasCuentas.append({'id': cuenta.id, 'accountCuenta': cuenta.accountCuenta,'userCuenta':cuenta.userCuenta,'passwordCuenta':password_cuenta,'selector':cuenta.selector})
     
                   print(cuenta.accountCuenta)	
                  
                
               else:
                  print("El usuario", usuario.nombre, "no tiene ninguna cuenta asociada.")
                  flash('No registra cuenta para el usuario: ',usuario.nombre)
                  return render_template("cuentas/registrarCuentaBroker.html")
                  
         
    
       
            except Exception as e:
                     print("Error:", str(e))
                     print("No se pudo registrar la cuenta.")
                     db.session.rollback()  # Hacer rollback de la sesión
                     return render_template("errorLogueo.html")
     db.session.close()
     return render_template('cuentas/cuentasDeUsuario.html', datos=todasLasCuentas)
  
@cuenta.route("/get_cuentas_de_broker_usuario_Abm",  methods=["POST"])   
def get_cuentas_de_broker_usuario_Abm():
     if request.method == 'POST':
       
         access_token = request.form['access_token_form_Abm']
         todasLasCuentas = []
         if access_token:
            app = current_app._get_current_object()
            
            try:
               user_id = jwt.decode(access_token.encode(), app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']

              # user_id = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
                # Obtener el objeto Usuario correspondiente al user_id
               usuario = Usuario.query.get(user_id)         
              # Buscar todas las cuentas asociadas a ese usuario
               cuentas = db.session.query(Cuenta).join(Usuario).filter(Cuenta.user_id == user_id).all()

               if cuentas:
                  print("El usuario", usuario.correo_electronico, "tiene las siguientes cuentas asociadas:")
                  
                  for cuenta in cuentas:
                   todasLasCuentas.append(cuenta.accountCuenta)
                   password_cuenta = cuenta.passwordCuenta.decode('utf-8')
                   todasLasCuentas.append({'id': cuenta.id, 'accountCuenta': cuenta.accountCuenta,'userCuenta':cuenta.userCuenta,'passwordCuenta':password_cuenta})
     
                   print(cuenta.accountCuenta)	
                  
                
               else:
                  print("El usuario", usuario.nombre, "no tiene ninguna cuenta asociada.")
                  flash('No registra cuenta para el usuario: ',usuario.nombre)
                  return render_template("cuentas/registrarCuentaBroker.html")
                  
         
    
       
            except:
                     print("No se pudo registrar la cuenta.")
                     db.session.rollback()  # Hacer rollback de la sesión
                     return render_template("errorLogueo.html")
     db.session.close()
     return render_template('cuentas/cuentasDeUsuarioAbm.html', datos=todasLasCuentas)
  
@cuenta.route("/delete_cuenta_usuario_broker",  methods=["POST"])   
def delete_cuenta_usuario_broker():
    try:
         if request.method == 'POST':
            id = request.form['id']            
            dato = Cuenta.query.get(id)
            print(dato)
            db.session.delete(dato)
            db.session.commit()
            flash('Operation Removed successfully')
            all_cuenta = db.session.query(Cuenta).all()
            db.session.close()
            return render_template("cuentas/cuentasDeUsuario.html", datos =  all_cuenta)
    except: 
            flash('Operation No Removed')       
            all_ins = db.session.query(Cuenta).all()
            db.session.close()
            
            return render_template('cuentas/cuentasDeUsuario.html', datos=all_cuenta) 
         
@cuenta.route("/logOutAccount")   
def logOutAccount():
   get.inicializar_variables_globales()
   get.diccionario_global_operaciones = {}
   get.diccionario_operaciones_enviadas = {}
   return render_template('cuentas/logOutAccount.html')

