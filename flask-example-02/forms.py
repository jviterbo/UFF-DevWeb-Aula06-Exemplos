from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RecadoForm(FlaskForm):
    texto = StringField("Novo recado", validators=[DataRequired(), Length(max=80)])
    descr = StringField("Descrição", validators=[DataRequired(), Length(max=280)])
    enviar = SubmitField("Adicionar")
