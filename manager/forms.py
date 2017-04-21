# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SupplierForm(FlaskForm):

    rz = StringField('Razón Social', validators=[DataRequired()])
    name = StringField('Nombre', description="Marca o nombre de fantasía utlizado por el proveedor")
