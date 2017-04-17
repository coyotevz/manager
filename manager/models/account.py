# -*- coding: utf-8 -*-

from datetime import datetime

from . import db


class Account(db.Model):
    __tablename__ = 'account'

    TYPE_ASSET = 'ASSET'
    TYPE_LIABILITY = 'LIABILITY'
    TYPE_EQUITY = 'EQUITY'
    TYPE_INCOME = 'INCOME'
    TYPE_EXPENSE = 'EXPENSE'

    _type_str = {
        TYPE_ASSET: 'Activo',
        TYPE_LIABILITY: 'Pasivo',
        TYPE_EQUITY: 'Patrimonio',
        TYPE_INCOME: 'Ingreso',
        TYPE_EXPENSE: 'Egreso',
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    _balance = db.Column("balance", db.Numeric(10, 2), default=None)
    _type = db.Column("type", db.Enum(*_type_str.keys(), name='account_type'),
                      default=None)

    parent_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    parent = db.relationship("Account", remote_side=[id], backref="children")

    @property
    def type(self):
        if self._type is not None:
            return self._type
        return self.parent._type

    @type.setter
    def type(self, value):
        if self.parent:
            raise InvalidArgumentError("Can only set type attribute on top "
                                       "level accounts")
        self._type = value

    @property
    def balance(self):
        if self.children:
            return sum([c.balance for c in self.children])
        return self._balance or Decimla('0')

    def __repr__(self):
        return "<Account({}, name={}, balance={})>".format(
                self.type, self.name, self.balance)


class AccountTransactoin(db.Model):
    __tablename__ = 'account_transaction'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
