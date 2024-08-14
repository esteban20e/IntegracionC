import jwt
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from datetime import datetime, timedelta
import random
import secrets


token = Blueprint('token',__name__)

def generar_token(user_id, valor, cuenta):
    llave = secrets.token_hex(32)
    print(llave)
    # Generar un número aleatorio utilizando el ID de usuario y el valor proporcionado
   
    random_number = random.randint(1, 10000)

    # Obtener la fecha de generación actual
    fecha_generacion = datetime.utcnow()

    # Agregar los datos al token como claims personalizados
    token_data = {
        'user_id': user_id,
        'random_number': random_number,
        'fecha_generacion': fecha_generacion.isoformat(),
        'valor': valor,
        'cuenta': cuenta
    }

  
    # Crear el token
    token_generado = jwt.encode(token_data, llave , algorithm='HS256')
    dato = token_generado + llave
    return dato
