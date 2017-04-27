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


class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_order'

    STATUS_CANCELLED = 'CANCELLED'
    STATUS_QUOTING = 'QUOTING'
    STATUS_PENDING = 'PENDING'
    STATUS_PARTIAL = 'PARTIAL'
    STATUS_CONFIRMED = 'CONFIRMED'
    STATUS_CLOSED = 'CLOSED'
    STATUS_DRAFT = 'DRAFT'

    STATUSES = [
        (STATUS_CANCELLED, 'Cancelada'),
        (STATUS_QUOTING, 'Presupuestando'),
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_PARTIAL, 'Parcial'),
        (STATUS_CONFIRMED, 'Confirmada'),
        (STATUS_CLOSED, 'Cerrada'),
        (STATUS_DRAFT, 'Borrador'),
    ]

    METHOD_EMAIL = 'EMAIL'
    METHOD_FAX = 'FAX'
    METHOD_PERSONALLY = 'PERSONALLY'

    METHODS = [
        (METHOD_MAIL, 'Correo Electrónico'),
        (METHOD_FAX, 'Fax'),
        (METHOD_PHONE, 'Telefónico'),
        (METHOD_PERSONALLY, 'Personalmente'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    status = db.Column(ChoiceType(STATUSES))
    notes = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)
    method = db.Column(ChoiceType(METHODS))

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    supplier = db.relationship(Supplier, backref=db.backref('orders', lazy='dynamic'))


class PurchaseOrderItem(db.Model):
    __tablename__ = 'purchase_order_item'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(20))
    description = db.Column(db.String(60))
    quantity = db.Column(db.Integer)
    received_quantity = db.Column(db.Integer, default=0)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship(PurchaseOrder, backref='items')
