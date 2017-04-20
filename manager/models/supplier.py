# -*- coding: utf-8 -*-

"""Simple suppliers model"""

from decimal import Decimal

from . import db


class Supplier(db.Model):
    __tablename__ = 'supplier'

    TYPE_PRODUCTS = 'PRODUCTS'
    TYPE_SERVICES = 'SERVICES'
    TYPE_SUPPLIES = 'SUPPLIES'

    _sup_type = {
        TYPE_PRODUCTS: 'Productos',
        TYPE_SERVICES: 'Servicios',
        TYPE_SUPPLIES: 'Insumos',
    }

    id = db.Column(db.Integer, primary_key=True)
    rz = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True)

    sup_type = db.Column(db.Enum(*_sup_type.keys(), name='supplier_type'),
                         default=TYPE_PRODUCTS)

    delivery_included = db.Column(db.Boolean)

    debt = db.Column(db.Numeric(10, 2))
    expired = db.Column(db.Numeric(10, 2))
    expiration_date = db.Column(db.DateTime, default=None)

    @property
    def type(self):
        return self._sup_type.get(self.sup_type)


@db.event.listens_for(Supplier, "init")
def supplier_init(target, args, kargs):
    # Sets defaults to instance
    if 'delivery_included' not in kwargs:
        target.delivery_included = False
    if 'debt' not in kwargs:
        target.debt = Decimal(0)
    if 'expired' not in kwargs:
        target.expired = Decimal(0)
