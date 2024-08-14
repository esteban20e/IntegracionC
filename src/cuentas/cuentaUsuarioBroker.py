
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

cuentas = Blueprint('cuentas',__name__)

@cuentas.route("/cuentaUsuarioBroker_all_cuentas_post/", methods=["POST"])   
def cuentaUsuarioBroker_all_cuentas_post():
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

@cuentas.route("/cuentas-Usuario-Broker/",  methods=["GET"])
def cuentas_Usuario_Broker():
   try:
      if request.method == 'GET': 
           cuentasBroker = db.session.query(Cuenta).all()
           db.session.close()
           return render_template("/cuentas/cuntasUsuariosBrokers.html",datos = cuentasBroker)
   except:
       print('no hay usuarios') 
   return 'problemas con la base de datos'

@cuentas.route("/eliminar-Cuenta-broker-administracion/",  methods=["POST"])
def eliminar_cuenta_broker_administracion():

    cuenta_id = request.form['eliminarCuentaId']
    cuenta = Cuenta.query.get(cuenta_id)
    db.session.delete(cuenta)
    db.session.commit()
    flash('Cuenta eliminada correctamente.')
    cuentas = db.session.query(Cuenta).all()
    db.session.close()
    return render_template("/cuentas/cuntasUsuariosBrokers.html",datos = cuentas)

