# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

from .models import db, Supplier, PurchaseDocument


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):

    @classmethod
    def get_session(self):
        return db.session


class SupplierForm(ModelForm):

    class Meta:
        model = Supplier
        only = ('rz', 'name', 'type', 'delivery_included')
        field_args = {
            'rz': {'label': 'Razón Social'},
            'name': {
                'label': 'Nombre',
                'description': "Marca o nombre de fantasía utilizado por el proveedor (Opcional)",
            },
            'type': {'label': 'Tipo de Proveedor'},
            'delivery_included': {'label': 'Incluye flete?'},
        }


class PurchaseDocumentForm(ModelForm):

    class Meta:
        model = PurchaseDocument
