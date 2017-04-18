# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal

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

    _code = db.Column("code", db.String)
    _balance = db.Column("balance", db.Numeric(10, 2), default=None)
    _type = db.Column("type", db.Enum(*_type_str.keys(), name='account_type'),
                      default=None)

    parent_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    parent = db.relationship("Account", remote_side=[id], backref="children")

    def get_path(self):
        parent = self
        path = []
        while parent:
            path.append(parent)
            parent = parent.parent
        return reversed(path)

    def get_children_recursively(self):
        children = set(self.children)
        if not len(children):
            return set()
        for child in self.children:
            children |= child.get_children_recursively()
        return children

    @property
    def code(self):
        return ".".join([a._code for a in self.get_path()])

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def type(self):
        if self._type is not None:
            return self._type
        return self.parent.type

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
        return self._balance or Decimal('0')

    @balance.setter
    def balance(self, value):
        assert value in self._type_str.keys()
        if self.children:
            raise ValueError("Can only set type attribute to to level accounts")
        self._type = value

    def __repr__(self):
        return "<Account({}, name={}, code={}, balance={})>".format(
                self.type, self.name, self.code, self.balance)


class AccountTransaction(db.Model):
    __tablename__ = 'account_transaction'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)


class AccountTransactionEntry(db.Model):
    __tablename__ = 'account_transaction_entry'

    TYPE_SOURCE = 'SOURCE'
    TYPE_DEST = 'DEST'

    _types = {
        TYPE_SOURCE: 'Origen',
        TYPE_DEST: 'Destino',
    }

    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    target = db.relationship(Account, backref="transaction_entries")
    transaction_id = db.Column(db.Integer, db.ForeignKey('account_transaction.id'),
                               nullable=False)
    transaction = db.relationship(AccountTransaction, backref="entries")
    type = db.Column(db.Enum(*_types.keys(), name='entry_type'),
                     nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return "<AccountTransactionEntry(type={})>".format(self.type)


def model_instances(iter_, model):
    for obj in iter_:
        if isinstance(obj, model):
            yield obj


@db.event.listens_for(db.session, 'before_commit')
def _entry_before_commit(session):
    changed = list(session.new)
    for entry in model_instances(changed, AccountTransactionEntry):
        etype = entry.type
        target = entry.target
        amount = entry.amount
        if etype == AccountTransactionEntry.TYPE_SOURCE:
            target.decrement(amount)
        elif etype == AccountTransactionEntry.TYPE_DEST:
            target.increment(amount)
        else:
            raise TypeError("Unknown transaction type")


@db.event.listens_for(db.session, 'before_commit')
def _verify_transaction(session):
    changed = list(session.new) + list(session.dirty)
    for transaction in model_instances(changed, AccountTransaction):
        transaction.verify()
