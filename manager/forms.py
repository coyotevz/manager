# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

from .models import db, Supplier


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):

    @classmethod
    def get_session(self):
        return db.session


class SupplierForm(ModelForm):

    class Meta:
        model = Supplier
        only = ('rz', 'name', 'type', 'delivery_included')
