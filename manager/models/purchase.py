# -*- coding: utf-8 -*-

"""Simple purchase documents model"""

from decimal import Decimal
from sqlalchemy_utils import ChoiceType

from . import db
from .supplier import Supplier


class PurchaseDocument(db.Model):
    __tablename__ = 'purchase_document'

    TYPE_FACTURA_A = 'FACTURA_A'
    TYPE_PRESUPUESTO = 'PRESUPUESTO'

    TYPES = [
        (TYPE_FACTURA_A, 'Factura A'),
        (TYPE_PRESUPUESTO, 'Presupuesto'),
    ]

    _short_type = {
        TYPE_FACTURA_A: 'FAA',
        TYPE_PRESUPUESTO: 'PRE',
    }

    STATUS_PENDING = 'PENDING'
    STATUS_EXPIRED = 'EXPIRED'
    STATUS_PAID = 'PAID'

    STATUSES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_EXPIRED, 'Vencida'),
        (STATUS_PAID, 'Pagada'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(ChoiceType(TYPES))
    pos = db.Column(db.Integer) # document point of sale part number
    number = db.Column(db.Integer)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    notes = db.Column(db.String)
    creation_date = db.Column(db.DateTime)
    issue_data = db.Column(db.Date)
    receipt_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    status = db.Column(ChoiceType(STATUSES))

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    supplier = db.relationship(Supplier, backref=db.backref('documents', lazy='dynamic'))

    @property
    def number_display(self):
        retval = "%08d" % self.number
        if self.pos:
            retval = "%04s-%s" % (self.pos, retval)
        return " ".join(self._sort_type.get(self.type), retval)
