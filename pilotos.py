from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField, IntegerField, SubmitField, DateField,BooleanField,TimeField
from wtforms.validators import DataRequired

class piloto(FlaskForm): 
    id_piloto=IntegerField('id_piloto',render_kw={"placeholder": "id piloto"})
    nombre=StringField('nombre',render_kw={"placeholder": "Nombre"})
    cedula=StringField('cedula', render_kw={"placeholder": "Cedula"})
    vuelos=StringField('vuelos',render_kw={"placeholder": "Trama de vuelos asignados"})
    puntuacion=IntegerField("Puntuacion",render_kw={"placeholder": "Puntuacion promedio"})
    numPuntuado=IntegerField("numero de veces puntuado",render_kw={"placeholder": "Numero de veces que ha sido puntuado"})
    enviar=SubmitField("Agregar piloto")
    completar=SubmitField("Completar datos")