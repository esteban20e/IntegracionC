# Creating  Routes
from pipes import Template
from unittest import result
from flask import current_app

import requests
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify,abort    
from models.instrumento import Instrumento
from utils.db import db
import routes.api_externa_conexion.get_login as get
import jwt
from models.usuario import Usuario




usuario = Blueprint('usuario',__name__)

@usuario.route("/usuariosModal/", methods=['GET'])
def obtener_usuarios_modal():
    try:
        usuarios = db.session.query(Usuario).all()
        db.session.close()
        # Crear una lista de diccionarios para cada usuario
        usuarios_json = [{'id': usuario.id, 'nombre': usuario.correo_electronico} for usuario in usuarios]
        return jsonify(usuarios=usuarios_json)
    except Exception as e:
        print('Error al obtener usuarios:', str(e))
        abort(500)  # Devuelve un código de estado de error 500 si hay problemas con la base de datos

@usuario.route("/usuarios/",  methods=["GET"])
def usuarios():
   try:
      if request.method == 'GET': 
           usuarios = db.session.query(Usuario).all()
           db.session.close()
           return render_template("/usuarios/usuarios.html",datos = usuarios)
   except:
       print('no hay usuarios') 
   return 'problemas con la base de datos'

@usuario.route("/eliminar-usuario/",  methods=["POST"])
def eliminar_usuario():
    usuario_id = request.form['usuario_id']
    usuario = Usuario.query.get(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente.')
    usuarios = db.session.query(Usuario).all()
    db.session.close()
    return render_template("/usuarios/usuarios.html",datos = usuarios)

@usuario.route("/editar-usuario",  methods=["POST"])
def editar_usuario():
    usuario_id = request.form['id']
    usuario = Usuario.query.get(usuario_id)
    usuario.email = request.form['email']
    usuario.roll = request.form['rol']
    db.session.commit()
    flash('Usuario editado correctamente.')
    usuarios = db.session.query(Usuario).all()
    db.session.close()
    return render_template("/usuarios/usuarios.html",datos = usuarios)

