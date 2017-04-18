# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def configure_db(app):
    db.init_app(app)


from .account import Account, AccountTransaction, AccountTransactionEntry
