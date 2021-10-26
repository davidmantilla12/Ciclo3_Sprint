from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField, IntegerField, SubmitField, DateField,BooleanField,TimeField
from wtforms.validators import DataRequired

class comentario(FlaskForm):
    '''id_comentario=IntegerField('id_comentario',render_kw={"placeholder": "id_comentario"})'''
    usuario=StringField('usuario',render_kw={"placeholder": "usuario"})
    id_vuelo=IntegerField("id_vuelo",render_kw={"placeholder": "id_vuelo"})
    puntuacion=IntegerField('puntuacion', render_kw={"placeholder": "puntuacion"})
    comentario=StringField('comentario',render_kw={"placeholder": "comentario"})
    enviar=SubmitField("Agregar comentario")