
# Creating  Routes
from pipes import Template
from unittest import result
from flask import current_app
from sqlalchemy import func, cast, String, Integer
from sqlalchemy.orm import aliased
from sqlalchemy.orm import joinedload
import bcrypt
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies
    
)
import requests
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from models.instrumento import Instrumento
from utils.db import db
import routes.api_externa_conexion.get_login as get
import jwt
from datetime import datetime, timedelta
import random
from models.usuario import Usuario
from models.cuentas import Cuenta
from models.ficha import Ficha
from models.trazaFicha import TrazaFicha
import hashlib
from tokens.token import generar_token

fichas = Blueprint('fichas',__name__)


def refrescoValorActualCuentaFichas(user_id):    
      try:
            repuesta_cuenta = get.pyRofexInicializada.get_account_report()
            if repuesta_cuenta and 'accountData' in repuesta_cuenta:
                reporte = repuesta_cuenta['accountData']
                available_to_collateral = reporte['availableToCollateral']
                fichas_usuario = db.session.query(Ficha).filter(Ficha.user_id == user_id).all()

                for ficha in fichas_usuario:
                    ficha.valor_cuenta_actual = available_to_collateral
                    db.session.commit()
            else:
                # Aquí puedes agregar código adicional si deseas realizar alguna acción específica cuando no hay datos.
                pass

      except Exception as e:
            db.session.rollback()
    # Aquí puedes agregar código adicional si deseas manejar la excepción de alguna manera.
        

@fichas.route('/fichas-asignar', methods = ['POST'])
def fichas_asignar():
    try:  
        access_token = request.form.get('access_token_forma')
        llave_ficha = request.form.get('tokenInput')  
        layouts = request.form.get('layoutOrigen') 
    
        try:
            user_id = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token de acceso expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token de acceso no válido'}), 401

        if not llave_ficha:
            return jsonify({'error': 'Falta el valor de la llave de ficha'}), 400

        if not layouts:
            return jsonify({'error': 'Falta el valor de layout'}), 400
        
 
      
      
      
             # Obtener todas las TrazaFichas con sus Fichas relacionadas
        traza_fichas_con_fichas = db.session.query(TrazaFicha).join(Ficha).options(joinedload(TrazaFicha.ficha)).all()

            # Puedes acceder a las fichas relacionadas de cada TrazaFicha en el bucle
            
      
      
        try:
            for traza_ficha in traza_fichas_con_fichas:
                    ficha_relacionada = traza_ficha.ficha
                
                    llave_bytes = ficha_relacionada.llave
                    llave_hex = llave_bytes.hex()  # Convertimos los bytes a representación hexadecimal

                    # Luego, si necesitas obtener la llave original como bytes nuevamente
                    llave_original_bytes = bytes.fromhex(llave_hex)
                    #obtenemos el valor
                    decoded_token = jwt.decode(ficha_relacionada.token, llave_original_bytes, algorithms=['HS256'])
                        
                    #obtenemos el numero
                    random_number = decoded_token.get('random_number')
                   
                        
                         
                        
                            
                    
            print("Llave ")
        except Exception as e:
               db.session.rollback()      
       
       
       
            
        return render_template("notificaciones/noPoseeDatos.htmll")
    except:  
        print("retorno incorrecto")  
        flash('no posee fichas aún')   
        return render_template("notificaciones/noPoseeDatos.html")
    

@fichas.route('/fichas-tomar', methods=['POST'])
def fichas_tomar():
    try:  
        access_token = request.form.get('access_token_forma')
        llave_ficha = request.form.get('tokenInput')  
        layouts = request.form.get('layoutOrigen') 
    
        try:
            user_id = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token de acceso expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token de acceso no válido'}), 401

        if not llave_ficha:
            return jsonify({'error': 'Falta el valor de la llave de ficha'}), 400

        if not layouts:
            return jsonify({'error': 'Falta el valor de layout'}), 400
        
 
      
      
      
        fichas = Ficha.query.filter_by().all()
      
      
        try:
            
            print("Llave ")
        except Exception as e:
               db.session.rollback()      
       
       
        #consultas de las neuvas fichas aceptadas
        ficha_aceptadas =  db.session.query(TrazaFicha).filter(TrazaFicha.user_id_traspaso == user_id).all()
       
            
        return render_template("notificaciones/noPoseeDatos.html")
    except:  
        print("retorno incorrecto")  
        flash('no posee fichas aún')   
        return render_template("notificaciones/noPoseeDatos.html")

    
    
@fichas.route('/crearFicha', methods=['POST'])
def crear_ficha():
    try:
        data = request.json
        valor = data.get('valor')
        access_token = data.get('accessToken')
        cuenta = data.get('cuenta')
        correoElectronico = data.get('correoElectronico')
        total_cuenta = data.get('total_cuenta')
        layouts = data.get('layoutOrigen')
       
   
        
        
        # obtener los valores del accesToken
        if access_token:
            app = current_app._get_current_object()                    
            userid = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
            exp_timestamp = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['exp']
            # Llamada a la función para generar el token
            token_con_llave = generar_token(userid, valor, cuenta)

            # Separa el token de la llave secreta
            token_generado = token_con_llave[:-64]
            llave_generada = token_con_llave[-64:]
            llave_bytes = llave_generada.encode('utf-8')
            #cuenta_id = Cuenta.query.filter_by(accountCuenta=cuenta).first()
            cuenta_id = db.session.query(Cuenta).filter_by(accountCuenta=cuenta).first()
            # almacenar el valor en el token
            # Ahora puedes crear una nueva ficha
            valorPorCien = valor * 100
            porcentajeCreacion = valorPorCien / total_cuenta  
            nueva_ficha = Ficha(
                user_id=userid,
                cuenta_broker_id=cuenta_id.id,  
                activo=True,  
                token=token_generado, 
                llave = llave_bytes,
                monto_efectivo=valor,
                porcentaje_creacion=porcentajeCreacion, 
                valor_cuenta_creacion=total_cuenta, 
                valor_cuenta_actual=total_cuenta,  
                estado="PENDIENTE",  
                fecha_generacion=datetime.now(), 
                interes=0.0 
            )

            # Almacenar el token en la base de datos
            db.session.add(nueva_ficha)
            db.session.commit()
            
                     # Consulta todas las fichas del usuario dado
            #fichas_usuario = Ficha.query.filter_by(user_id=userid).all()
            #total_cuenta = available_to_collateral + portfolio
            total_para_fichas =  total_cuenta * 0.6
            print(total_para_fichas)
        
           # fichas_usuario = Ficha.query.filter_by(user_id=userid).all()
            fichas_usuario = db.session.query(Ficha).filter(Ficha.user_id == userid).all()
           
            return render_template("notificaciones/noPoseeDatos.html")

            #return jsonify({'fichas_usuario': fichas_json})
                
          
        
          
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@fichas.route("/fichasToken_fichas_generar/", methods=['POST'])   
def fichasToken_fichas_generar():
   try:  
        total_cuenta = 0.0
        access_token = request.form['access_token_form_GenerarFicha'] 
        layouts = request.form['layoutOrigen']
        repuesta_cuenta = get.pyRofexInicializada.get_account_report()
        reporte = repuesta_cuenta['accountData']
        if reporte!=None:
            available_to_collateral = reporte['availableToCollateral']
            portfolio = reporte['portfolio']
           # layouts = 'layout'
        # print("detalle  ",available_to_collateral)
        # print("detalle ",portfolio)
        
            
            if access_token:
                    user_id = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
            # Consulta todas las fichas del usuario dado
            #fichas_usuario = Ficha.query.filter_by(user_id=user_id).all()
            total_cuenta = available_to_collateral + portfolio
            total_para_fichas =  total_cuenta * 0.6
            fichas_usuario = db.session.query(Ficha).filter(Ficha.user_id == user_id).all()
      
           
            try:
                for ficha in fichas_usuario:
                    #print(ficha.monto_efectivo)
                    total_para_fichas=total_para_fichas - ficha.monto_efectivo
                    diferencia = available_to_collateral - ficha.valor_cuenta_creacion
                    porcien= diferencia*100
                    interes = porcien/available_to_collateral
                    interes = int(interes)
                    ficha.interes = interes
                    
                # print(interes)  
                    llave_bytes = ficha.llave
                    llave_hex = llave_bytes.hex()  # Convertimos los bytes a representación hexadecimal

                    # Luego, si necesitas obtener la llave original como bytes nuevamente
                    llave_original_bytes = bytes.fromhex(llave_hex)
                    #obtenemos el valor
                    decoded_token = jwt.decode(ficha.token, llave_original_bytes, algorithms=['HS256'])
                    
                    #obtenemos el numero
                    random_number = decoded_token.get('random_number')
                    # Agregamos random_number a la ficha
                    ficha.random_number = random_number
                    ficha.interes = interes
                    db.session.commit()
            except Exception as e:
                db.session.rollback()   
            
        
            print(total_para_fichas)    
           
            return render_template("notificaciones/noPoseeDatos.html")  
        else:
             flash('no posee datos') 
             return render_template("notificaciones/noPoseeDatos.html")   
   except:  
        print("no llama correctamente")  
        flash('no hay fichas creadas aún')   
        if total_cuenta < 1:
              return render_template("notificaciones/noPoseeDatosFichas.html",layout = layouts)  
        return render_template("fichas/fichasGenerar.html", datos=[],total_para_fichas=total_para_fichas,total_cuenta=total_cuenta, layout = layouts)
        
          
  # return render_template("login.html" )
    
 

@fichas.route("/fichasToken-fichas-listar/", methods=["POST"])   
def fichasToken_fichas_listar():
    try:  
        access_token = request.form['access_token_form_ListarFicha'] 
        layouts = request.form['layoutOrigen']
        repuesta_cuenta = get.pyRofexInicializada.get_account_report()
        reporte = repuesta_cuenta['accountData']
        available_to_collateral = reporte['availableToCollateral']
        portfolio = reporte['portfolio']
       # print("detalle  ",available_to_collateral)
       # print("detalle ",portfolio)
        #layouts = 'layout'
        
        if access_token:
            user_id = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
            fichas_usuario = db.session.query(Ficha).filter(Ficha.user_id == user_id).all()
            traza_fichas = db.session.query(TrazaFicha).filter(TrazaFicha.user_id_traspaso == user_id).all()
            try:
                for ficha in fichas_usuario:
                    #print(ficha.monto_efectivo)
                
                    diferencia = available_to_collateral - ficha.valor_cuenta_creacion
                    porcien= diferencia*100
                    interes = porcien/available_to_collateral
                    interes = int(interes)
                    ficha.interes = interes
                # print(interes)  
                    llave_bytes = ficha.llave
                    llave_hex = llave_bytes.hex()  # Convertimos los bytes a representación hexadecimal

                    # Luego, si necesitas obtener la llave original como bytes nuevamente
                    llave_original_bytes = bytes.fromhex(llave_hex)
                    #obtenemos el valor
                    decoded_token = jwt.decode(ficha.token, llave_original_bytes, algorithms=['HS256'])
                    
                    #obtenemos el numero
                    random_number = decoded_token.get('random_number')
                    # Agregamos random_number a la ficha
                    ficha.random_number = random_number
                    db.session.commit()
            except Exception as e:
                db.session.rollback()   
                
             # Obtener todas las TrazaFichas con sus Fichas relacionadas
            traza_fichas_con_fichas = db.session.query(TrazaFicha).join(Ficha).options(joinedload(TrazaFicha.ficha)).all()

            # Puedes acceder a las fichas relacionadas de cada TrazaFicha en el bucle
            for traza_ficha in traza_fichas_con_fichas:
                ficha_relacionada = traza_ficha.ficha
                print(f"Ficha relacionada - ID: {ficha_relacionada.id}, Token: {ficha_relacionada.token}")
            
          
                
            return render_template("fichas/fichasListado.html", datos=fichas_usuario, layout = layouts)
    except:  
        print("no llama correctamente")  
        flash('fichasListado Incorrect')   
        return render_template("fichas/fichasListado.html", datos=[], layout=layouts)  
    
@fichas.route("/fichasToken-fichas-listar-sin-cuenta/", methods=["POST"])   
def fichasToken_fichas_listar_sin_cuenta():
    try:  
        access_token = request.form['access_token_form_ListarFicha'] 
        layouts = request.form['layoutOrigen']
      
       # print("detalle  ",available_to_collateral)
       # print("detalle ",portfolio)
       
        
        if access_token:
                user_id = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
        # Consulta todas las fichas del usuario dado
        #fichas_usuario = Ficha.query.filter_by(user_id=user_id).all()
        fichas_usuario = db.session.query(Ficha).filter(Ficha.user_id == user_id).all()
         
        try:
            for ficha in fichas_usuario:
                #print(ficha.monto_efectivo)
               
                diferencia =  ficha.valor_cuenta_actual - ficha.valor_cuenta_creacion
                porcien= diferencia*100
                interes = porcien/ficha.valor_cuenta_actual
                interes = int(interes)
                ficha.interes = interes
            # print(interes)  
                llave_bytes = ficha.llave
                llave_hex = llave_bytes.hex()  # Convertimos los bytes a representación hexadecimal

                # Luego, si necesitas obtener la llave original como bytes nuevamente
                llave_original_bytes = bytes.fromhex(llave_hex)
                #obtenemos el valor
                decoded_token = jwt.decode(ficha.token, llave_original_bytes, algorithms=['HS256'])
                
                #obtenemos el numero
                random_number = decoded_token.get('random_number')
                valorInicial = decoded_token.get('valor')
                # Agregamos random_number a la ficha
                ficha.random_number = random_number
                db.session.commit()
        except Exception as e:
               db.session.rollback()   
        traza_fichas_con_fichas = []  # o asigna la lista que corresponda
           # Obtener todas las TrazaFichas con sus Fichas relacionadas
        traza_fichas_con_fichas = db.session.query(TrazaFicha).join(Ficha).options(joinedload(TrazaFicha.ficha)).all()

        for traza_ficha in traza_fichas_con_fichas:
            ficha_relacionada = traza_ficha.ficha
            llave_bytes = ficha_relacionada.llave
            llave_hex = llave_bytes.hex()  # Convertimos los bytes a representación hexadecimal

            # Luego, si necesitas obtener la llave original como bytes nuevamente
            llave_original_bytes = bytes.fromhex(llave_hex)
            #obtenemos el valor
            decoded_token = jwt.decode(ficha_relacionada.token, llave_original_bytes, algorithms=['HS256'])
                
            #obtenemos el numero
            random_number = decoded_token.get('random_number')
            valorInicial = decoded_token.get('valor')
            # Agregamos random_number a la ficha
            ficha_relacionada.random_number = random_number

            # Imprimir todos los campos de Ficha
            print("Campos de Ficha:")
            print(f"  ID: {ficha_relacionada.id}")
            print(f"  User ID: {ficha_relacionada.user_id}")
            print(f"  Cuenta Broker ID: {ficha_relacionada.cuenta_broker_id}")
            print(f"  Activo: {ficha_relacionada.activo}")
            print(f"  monto_efectivo: {ficha_relacionada.monto_efectivo}")
            print(f" interes: {ficha_relacionada.interes}")
            print(f"  estado: {ficha_relacionada.estado}")
            print(f" user_id_traspaso: {traza_ficha.user_id_traspaso}")
            # ... Agrega más campos según sea necesario

            print("\n")  
          
                
            
            
        return render_template("fichas/fichasListado.html", datos=traza_fichas_con_fichas,usuario_id= user_id,layout = layouts)
    except:  
        print("retorno incorrecto")  
        flash('no posee fichas aún')   
        return render_template("fichas/fichasListado.html", datos=[], layout=layouts)

       # return render_template("notificaciones/errorOperacionSinCuenta.html", layout = layouts) 
    
@fichas.route("/fichasToken_fichas_all/", methods=["POST"])   
def fichasToken_fichas_all():
    if request.method == 'POST':
        
        access_token = request.json.get('accessToken')

        todasLasCuentas = []

        if access_token:
            app = current_app._get_current_object()
            
            try:
                user_id = jwt.decode(access_token.encode(), app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
                usuario = Usuario.query.get(user_id)         
                cuentas = db.session.query(Cuenta).join(Usuario).filter(Cuenta.user_id == user_id).all()

                if cuentas:
                    data = []  # Lista para almacenar los datos de las cuentas
                    
                    for cuenta in cuentas:
                        password_cuenta = cuenta.passwordCuenta.decode('utf-8')
                        data.append({
                            'id': cuenta.id,
                            'user_id': cuenta.user_id,
                            'accountCuenta': cuenta.accountCuenta,
                            'userCuenta': cuenta.userCuenta,
                            'passwordCuenta': password_cuenta,
                            'selector': cuenta.selector
                        })
                    
                    return jsonify({'cuentas': data})  # Devolver los datos en formato JSON
                
                else:
                    return jsonify({'message': 'No se encontraron cuentas asociadas a este usuario.'}), 404
                  
            except Exception as e:
                print("Error:", str(e))
                print("No se pudo registrar la cuenta.")
                db.session.rollback()  # Hacer rollback de la sesión
                return jsonify({'error': 'Hubo un error en la solicitud.'}), 500
    
    return jsonify({'message': 'Solicitud no válida.'}), 400

@fichas.route("/fichasToken_fichas_usuarios_get",  methods=["GET"])
def fichasToken_fichas_usuarios_get():
   try:
      if request.method == 'GET': 
           cuentasBroker = db.session.query(Cuenta).all()
           db.session.close()
           return render_template("/cuentas/cuntasUsuariosBrokers.html",datos = cuentasBroker)
   except:
       print('no hay usuarios') 
   return 'problemas con la base de datos'

@fichas.route("/eliminar-ficha/",  methods=["POST"])
def eliminar_ficha():
  if request.method == 'POST':
    access_token = request.form['access_token']
    layouts = request.form['layoutOrigen']
    if access_token:
        app = current_app._get_current_object()
            
        ficha_id = request.form['eliminarFichaId']
       
        user_id = jwt.decode(access_token.encode(), app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
               
        # Buscar y eliminar la ficha
        ficha = Ficha.query.filter_by(id=ficha_id, user_id=user_id).first()
        
        if ficha:
          if ficha.estado == 'PENDIENTE' or ficha.estado == 'ENTREGADO':
                    db.session.delete(ficha)
                    db.session.commit()
                    db.session.close()

                    flash('Ficha eliminada correctamente.')
                    mensaje = "La ficha ha sido eliminada correctamente."
        else:
            mensaje = "No se encontró la ficha o no tienes permisos para eliminarla."
        fichas_usuario = []  # o asigna la lista que corresponda

        fichas_usuario = Ficha.query.filter_by(user_id=user_id).all()
        
        repuesta_cuenta = get.pyRofexInicializada.get_account_report()
        reporte = repuesta_cuenta['accountData']
        available_to_collateral = reporte['availableToCollateral']
        portfolio = reporte['portfolio']
        
        total_cuenta = available_to_collateral + portfolio
        total_para_fichas =  total_cuenta * 0.6
        
        for ficha in fichas_usuario:
           # print(ficha.token)
            llave_bytes = ficha.llave
            llave_hex = llave_bytes.hex()  # Convertimos los bytes a representación hexadecimal

            # Luego, si necesitas obtener la llave original como bytes nuevamente
            llave_original_bytes = bytes.fromhex(llave_hex)
            #obtenemos el valor
            decoded_token = jwt.decode(ficha.token, llave_original_bytes, algorithms=['HS256'])
            
            #obtenemos el numero
            random_number = decoded_token.get('random_number')
            # Agregamos random_number a la ficha
            ficha.random_number = random_number
            
     
        if not fichas_usuario:
            fichas_usuario = []
       

        return render_template("fichas/fichasGenerar.html", datos=fichas_usuario, total_para_fichas=total_para_fichas, total_cuenta=total_cuenta, layout=layouts)


@fichas.route("/reportar-ficha/",  methods=["POST"])
def reportar_ficha():
  if request.method == 'POST':
    access_token = request.form['access_token']
    layouts = request.form['layoutOrigen']
    if access_token:
        app = current_app._get_current_object()
            
        ficha_id = request.form['reportarFichaId']
        id_ficha = request.form['reportaridFicha']
       
        user_id = jwt.decode(access_token.encode(), app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
               
        # Buscar y eliminar la ficha
        ficha = Ficha.query.filter_by(id=id_ficha).first()
        trazaficha = TrazaFicha.query.filter_by(id=ficha_id).first()
        
        if ficha:
            if ficha.estado != 'ENTREGADO':
                ficha.estado = 'REPORTADO'
                trazaficha.estado_traza = 'REPORTADO'
                db.session.commit()
               
                flash('Ficha reportada correctamente.')
                mensaje = "La ficha ha sido reportada correctamente."
        else:
            mensaje = "No se encontró la ficha o no tienes permisos para reportar."
        fichas_usuario = []  # o asigna la lista que corresponda

        fichas_usuario = db.session.query(Ficha).filter(Ficha.user_id == user_id).all()
         
        try:
            for ficha in fichas_usuario:
                #print(ficha.monto_efectivo)
               
                diferencia =  ficha.valor_cuenta_actual - ficha.valor_cuenta_creacion
                porcien= diferencia*100
                interes = porcien/ficha.valor_cuenta_actual
                interes = int(interes)
                ficha.interes = interes
            # print(interes)  
                llave_bytes = ficha.llave
                llave_hex = llave_bytes.hex()  # Convertimos los bytes a representación hexadecimal

                # Luego, si necesitas obtener la llave original como bytes nuevamente
                llave_original_bytes = bytes.fromhex(llave_hex)
                #obtenemos el valor
                decoded_token = jwt.decode(ficha.token, llave_original_bytes, algorithms=['HS256'])
                
                #obtenemos el numero
                random_number = decoded_token.get('random_number')
                valorInicial = decoded_token.get('valor')
                # Agregamos random_number a la ficha
                ficha.random_number = random_number
                db.session.commit()
        except Exception as e:
               db.session.rollback()   
        
           # Obtener todas las TrazaFichas con sus Fichas relacionadas
        traza_fichas_con_fichas = db.session.query(TrazaFicha).join(Ficha).options(joinedload(TrazaFicha.ficha)).all()

        for traza_ficha in traza_fichas_con_fichas:
            ficha_relacionada = traza_ficha.ficha
     

            # Imprimir todos los campos de Ficha
            print("Campos de Ficha:")
            print(f"  ID: {ficha_relacionada.id}")
            print(f"  User ID: {ficha_relacionada.user_id}")
            print(f"  Cuenta Broker ID: {ficha_relacionada.cuenta_broker_id}")
            print(f"  Activo: {ficha_relacionada.activo}")
            print(f"  monto_efectivo: {ficha_relacionada.monto_efectivo}")
            print(f" interes: {ficha_relacionada.interes}")
            print(f"  estado: {ficha_relacionada.estado}")
            print(f" user_id_traspaso: {traza_ficha.user_id_traspaso}")
            # ... Agrega más campos según sea necesario

            print("\n")  
          
                
            
            
        return render_template("fichas/fichasListado.html", datos=traza_fichas_con_fichas,usuario_id= user_id,layout = layouts)
   
   
@fichas.route("/recibir-ficha/",  methods=["POST"])
def recibir_ficha():
  if request.method == 'POST':
    access_token = request.form['recibir_access_token']
    layouts = request.form['layoutOrigen']
    if access_token:
        app = current_app._get_current_object()
            
        ficha_id = request.form['recibirFichaId']
        id_ficha = request.form['recibiridFicha']
       
        user_id = jwt.decode(access_token.encode(), app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
               
        # Buscar y eliminar la ficha
          # Buscar y eliminar la ficha
        ficha = Ficha.query.filter_by(id=id_ficha).first()
       
        
        traza_ficha = TrazaFicha.query.filter_by(id=ficha_id, user_id_traspaso=user_id).first()
        
        if traza_ficha:
            if traza_ficha.estado_traza == 'ACEPTADO':
                db.session.delete(traza_ficha)              
                ficha.estado = 'ENTREGADO'
                db.session.add(ficha)
                db.session.commit()
                flash('Ficha recibida correctamente.')
                mensaje = "La trazaficha ha sido eliminada correctamente."
        else:
            mensaje = "No se encontró la ficha o no tienes permisos para acpetarla."
        traza_fichas_con_fichas = []  # o asigna la lista que corresponda

       
        
       
              # Obtener todas las TrazaFichas con sus Fichas relacionadas
        traza_fichas_con_fichas = db.session.query(TrazaFicha).join(Ficha).options(joinedload(TrazaFicha.ficha)).all()

        for traza_ficha in traza_fichas_con_fichas:
            ficha_relacionada = traza_ficha.ficha
     

            # Imprimir todos los campos de Ficha
            print("Campos de Ficha:")
            print(f"  ID: {ficha_relacionada.id}")
            print(f"  User ID: {ficha_relacionada.user_id}")
            print(f"  Cuenta Broker ID: {ficha_relacionada.cuenta_broker_id}")
            print(f"  Activo: {ficha_relacionada.activo}")
            print(f"  monto_efectivo: {ficha_relacionada.monto_efectivo}")
            print(f" interes: {ficha_relacionada.interes}")
            print(f"  estado: {ficha_relacionada.estado}")
            print(f" user_id_traspaso: {traza_ficha.user_id_traspaso}")
            # ... Agrega más campos según sea necesario

            print("\n")  
          
                
            
            
        return render_template("fichas/fichasListado.html", datos=traza_fichas_con_fichas,usuario_id= user_id,layout = layouts)
   