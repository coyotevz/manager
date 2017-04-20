# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for

from ..models import Account, Supplier

buz = Blueprint('business', __name__, url_prefix='/business')


@buz.route('')
def index():
    return redirect(url_for('.summary'))

@buz.route('/summary')
def summary():
    return render_template('business/summary.html')

@buz.route('/accounts')
def accounts():
    accounts = Account.query.filter(Account.parent==None)\
                            .order_by(Account._code.asc())
    return render_template('business/accounts.html', accounts=accounts)

@buz.route('/customers')
def customers():
    return render_template('business/customers.html')

@buz.route('/suppliers')
def suppliers():
    suppliers = Supplier.query
    return render_template('business/suppliers.html', suppliers=suppliers)
