# -*- coding: utf-8 -*-

"""Simple suppliers model"""

from enum import Enum
from decimal import Decimal
from sqlalchemy_utils import ChoiceType

from . import db


class Supplier(db.Model):
    __tablename__ = 'supplier'

    TYPE_PRODUCTS = 'PRODUCTS'
    TYPE_SERVICES = 'SERVICES'
    TYPE_SUPPLIES = 'SUPPLIES'

    TYPES = [
        (TYPE_PRODUCTS, 'Productos'),
        (TYPE_SERVICES, 'Servicios'),
        (TYPE_SUPPLIES, 'Insumos'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    rz = db.Column(db.String, unique=True, nullable=False)#, info={'label': 'Razón Social'})
    name = db.Column(db.String, unique=True)#, info={
    #    'label': 'Nombre',
    #    'placeholder': 'Opcional',
    #    'description': "Marca o nombre de fantasía utlizado por el proveedor",
    #})

    type = db.Column(ChoiceType(TYPES))#, info={'label': 'Tipo de Proveedor'})

    delivery_included = db.Column(db.Boolean)#, info={'label': 'Incluye flete?'})

    debt = db.Column(db.Numeric(10, 2))
    expired = db.Column(db.Numeric(10, 2))
    expiration_date = db.Column(db.DateTime, default=None)


@db.event.listens_for(Supplier, "init")
def supplier_init(target, args, kwargs):
    # Sets defaults to instance
    if 'delivery_included' not in kwargs:
        target.delivery_included = False
    if 'debt' not in kwargs:
        target.debt = Decimal(0)
    if 'expired' not in kwargs:
        target.expired = Decimal(0)

# Import data from XML file (etree interface)

def import_supplier_data(element):
    for el in list(element):
        supplier = Supplier(**el.attrib)
        db.session.add(supplier)
