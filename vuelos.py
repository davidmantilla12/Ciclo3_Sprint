from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField, IntegerField, SubmitField, DateField,BooleanField
from wtforms.validators import DataRequired

class vuelo(FlaskForm): 
    id_vuelo=IntegerField('codigo', validators=[DataRequired("Llena este campo")],render_kw={"placeholder": "id vuelo"})
    origen=StringField('origen', validators=[DataRequired("Llena este campo")],render_kw={"placeholder": "Origen"})
    destino=StringField('destino', validators=[DataRequired("Llena este campo")],render_kw={"placeholder": "Destino"})
    hora_salida=DateField('hora de salida', validators=[DataRequired("Llena este campo")],render_kw={"placeholder": "Hora de Salida"})
    hora_llegada=DateField('hora de llegada', validators=[DataRequired("Llena este campo")],render_kw={"placeholder": "Hora de llegada"})
    fecha=DateField('fecha de ida', format="%Y-%m-%d",default=datetime.today, validators=[DataRequired("Llena este campo")])
    fecha_vuelta=DateField('fecha de vuelta', format="%Y-%m-%d",default=datetime.today, validators=[DataRequired("Llena este campo")])
    piloto=StringField('piloto',render_kw={"placeholder": "Id de Piloto"})
    asientos=StringField("asientos",validators=[DataRequired("Llena este campo")],render_kw={"placeholder": "string de asientos"})
    asientos_libres=StringField("asientos libres",render_kw={"placeholder": "string de asientos libres"})
    valor=IntegerField("Valor",render_kw={"placeholder": "Valor del vuelo"})
    puntuacion=IntegerField("Puntuacion",render_kw={"placeholder": "Puntuacion promedio"})
    numPuntuado=IntegerField("numero de veces puntuado",render_kw={"placeholder": "Numero de veces que ha sido puntuado"})
    enviar=SubmitField("Agregar Vuelo")
