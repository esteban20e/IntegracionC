# Creating  Routes
from pipes import Template
from unittest import result
import requests
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from models.instrumento import Instrumento
from utils.db import db
import routes.api_externa_conexion.get_login as get_login




validaInstrumentos = Blueprint('validaInstrumentos',__name__)


def validar_existencia_instrumentos(mi_listado,listado_instrumentos):
  listado_final = []
  for instrumento in mi_listado:
    if instrumento in listado_instrumentos:
      print(f'El instrumento {instrumento} existe en el mercado')
      listado_final.append(instrumento)
   # else:
   #   print(f'El instrumento {instrumento} NO existe en el mercado')
  return listado_final



def validar_existencia_instrumento_solo(symbol, listado_instrumentos):
    if symbol in listado_instrumentos:
        print(f'El instrumento {symbol} existe en el mercado')
        return symbol
    else:
        print(f'El instrumento {symbol} NO existe en el mercado')
        return None


