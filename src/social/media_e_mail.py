# Creating  Routes
from pipes import Template
from unittest import result
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from models.instrumento import Instrumento
from utils.db import db
import routes.api_externa_conexion.get_login as get
import jwt
from models.usuario import Usuario
from models.cuentas import Cuenta
from datetime import datetime
import smtplib



media_e_mail = Blueprint('media_e_mail',__name__)

@media_e_mail.route('/save-ip', methods=['POST'])
def save_ip():
    if request.method == 'POST':
        try:
            access_token = request.json.get('accesstoken')
            correo_electronico = request.json.get('correo_electronico')
            usuario = request.json.get('usuario1')
            ip = request.json.get('ip') 
            time = datetime.now()
            print('usario',usuario,'correo_electronico:', correo_electronico, 'ip:', ip, 'time:', time)

            # Configurar las variables para enviar el correo electrónico
            sender_email = 'mauriciodioli@gmail.com'
            receiver_email = 'mauriciodioli@gmail.com'
            password = 'bqsgnuufueyafsox'
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587

            # Crear el mensaje de correo electrónico
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = f'IP Address - {correo_electronico}'

            # Crear el cuerpo del mensaje con todos los parámetros
           
            body = f'Correo Electrónico: {correo_electronico}\n'
            body += f'Usuario: {usuario}\n'
            body += f'IP Address: {ip}\n'
            body += f'Time: {time}\n'
            
            message.attach(MIMEText(body, 'plain'))

            # Establecer una conexión con el servidor SMTP y enviar el correo electrónico
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())

            return 'OK'  # Devolver una respuesta exitosa al cliente
        except smtplib.SMTPException as e:
            # Manejar errores relacionados con el envío del correo electrónico
            print('Error al enviar el correo electrónico:', str(e))
            return 'Error al enviar el correo electrónico', 500  # Devolver una respuesta de error al cliente
        except Exception as e:
            # Manejar otros errores no esperados
            print('Error inesperado:', str(e))
            return 'Error inesperado', 500  # Devolver una respuesta de error al cliente
