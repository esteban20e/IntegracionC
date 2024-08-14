import secrets
from functools import wraps
from flask import (
    Flask,
    Blueprint,
    request,
    redirect,
    jsonify,
    url_for,
    render_template,
    flash,
    make_response
)
from flask import request, make_response, jsonify

from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    set_access_cookies, 
    set_refresh_cookies,
    get_jwt_identity)


import bcrypt
from datetime import datetime, timedelta

from flask_login import LoginManager, login_required, login_user, UserMixin

import jwt
from flask_dance.consumer import oauth_authorized

from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from requests.exceptions import HTTPError
from models.usuario import Usuario
from datetime import datetime, timedelta
from utils.db import db
from usuarios.autenticacion import autenticacion

# Configuración del Blueprint para el registro de usuarios
registrarUsuario = Blueprint("registrarUsuario", __name__)

# Clave secreta para generar los tokens
SECRET_KEY = 'supersecreto'

# Duración de los tokens
TOKEN_DURATION = 30  # minutos
REFRESH_TOKEN_DURATION = 60  # minutos

@registrarUsuario.route('/logout', methods=['POST'])
def logout():
    token = request.cookies.get('token')

    # Decodificar el token
    username = decode_token(token)

    # Actualizar la base de datos para borrar los tokens del usuario
    with db.cursor() as cursor:
        cursor.execute('UPDATE usuarios SET token=NULL, refresh_token=NULL WHERE username=%s', (username,))
        db.commit()

    response = make_response(jsonify({'mensaje': 'Sesión cerrada'}))
    response.set_cookie('token', '', expires=0)
    response.set_cookie('refresh_token', '', expires=0)

    return response

@registrarUsuario.route("/registrar_usuario")
def registrar_usuario():
    return render_template("usuarios/registrarUsuario.html")

from flask import jsonify

@registrarUsuario.route('/registro-usuario', methods=['POST'])
def registro_usuario():
    correo_electronico = request.form['correo_electronico']   
    password = request.form['password']   
   
    print('password:', password)
    
    # Verificar si el usuario ya está registrado
    usuario_existente = Usuario.query.filter_by(correo_electronico=correo_electronico).first()

    if usuario_existente:
        flash('El correo electrónico ya está registrado.')
        return render_template("index.html")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Generar el token de acceso y el token de actualización
    access_token = create_access_token(identity=correo_electronico, expires_delta=timedelta(minutes=TOKEN_DURATION))
    refresh_token = create_refresh_token(identity=correo_electronico, expires_delta=timedelta(minutes=REFRESH_TOKEN_DURATION))

    usuario = Usuario(id=None, token=access_token, refresh_token=refresh_token, activo=True, correo_electronico=correo_electronico, password=hashed_password)

    db.session.add(usuario)
    db.session.commit()
    db.session.close()
    # Crear una respuesta
   


    flash('Registro como usuario exitoso.')
    # Crear una respuesta
    response = make_response(render_template("index.html"))
   # response = make_response(render_template("home.html", tokens=[access_token, refresh_token]))

    # Configurar las cookies HTTP con los tokens
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    # Devolver la respuesta con los tokens
    return response




def decode_token(token):
    try:
        # Decodificar el token con la clave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # Devolver el nombre de usuario almacenado en el token
        return payload['sub']

    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        # Si el token es inválido o ha expirado, devolver None
        return None
