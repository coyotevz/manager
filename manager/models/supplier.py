# -*- coding: utf-8 -*-

"""Simple suppliers model"""

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
    rz = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True)
    type = db.Column(ChoiceType(TYPES))
    delivery_included = db.Column(db.Boolean)

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
