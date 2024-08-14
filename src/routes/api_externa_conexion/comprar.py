# Creating  Routes
from pipes import Template
from unittest import result
import requests
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from models.instrumento import Instrumento
from utils.db import db



comprar = Blueprint('comprar',__name__)

@comprar.route("/compraInstrumento",  methods=["GET"])
def compraInstrumento():
   if request.method == 'GET': 
 ####   AQUI TENGO QUE COMPARA LA FECHA ####     
  
   
    #return render_template('comprar.html', datos = r.json())
    return "salida"
