from flask_marshmallow import Marshmallow
from flask import Blueprint
from utils.db import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import inspect

ma = Marshmallow()

image = Blueprint('image', __name__)

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('usuarios.id'))  
    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)   
    colorDescription = db.Column(db.String(255), nullable=False) 
    filepath = db.Column(db.String(500), nullable=True)
    randomNumber = db.Column(db.Integer) 
    
    usuarios = relationship("Usuario", back_populates="imagenes")

    def __init__(self, user_id, title, description, filepath, randomNumber,colorDescription):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.filepath = filepath
        self.randomNumber = randomNumber
        self.colorDescription = colorDescription

    def __repr__(self):
        return f"Image(id={self.id}, user_id={self.user_id}, title={self.title}, description={self.description}, filepath={self.filepath}, randomNumber={self.randomNumber},colorDescription={self.colorDescription})"

    @classmethod
    def crear_tabla_image(cls):
        insp = inspect(db.engine)
        if not insp.has_table("image"):
            db.create_all()

class MerShema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "title", "description", "filepath", "randomNumber","colorDescription")

mer_schema = MerShema()
mer_shema = MerShema(many=True)
