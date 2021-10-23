from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField, IntegerField, SubmitField, DateField,BooleanField,TimeField
from wtforms.validators import DataRequired

class vuelo(FlaskForm): 
    id_vuelo=IntegerField('codigo',render_kw={"placeholder": "id vuelo"})
    origen=StringField('origen',render_kw={"placeholder": "Origen"})
    destino=StringField('destino', render_kw={"placeholder": "Destino"})
    hora_salida=TimeField('hora de salida', format='%H:%M:%S',render_kw={"placeholder": "Hora de Salida"})
    hora_llegada=TimeField('hora de llegada', format='%H:%M:%S',render_kw={"placeholder": "Hora de llegada"})
    fecha=DateField('fecha de ida', format="%Y-%m-%d",default=datetime.today, render_kw={"placeholder":"Fecha de vuelo"})
    fecha_vuelta=DateField('fecha de vuelta', format="%Y-%m-%d",default=datetime.today)
    piloto=StringField('piloto',render_kw={"placeholder": "Id de Piloto"})
    asientos=StringField("asientos",render_kw={"placeholder": "Trama de asientos"})
    asientos_libres=StringField("asientos libres",render_kw={"placeholder": "Trama de asientos libres"})
    valor=IntegerField("Valor",render_kw={"placeholder": "Valor del vuelo"})
    puntuacion=IntegerField("Puntuacion",render_kw={"placeholder": "Puntuacion promedio"})
    numPuntuado=IntegerField("numero de veces puntuado",render_kw={"placeholder": "Numero de veces que ha sido puntuado"})
    enviar=SubmitField("Agregar Vuelo")
    completar=SubmitField("Completar datos",render_kw={'onmouseover':'consultarEst(),'})