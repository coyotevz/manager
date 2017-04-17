# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for

buz = Blueprint('business', __name__, url_prefix='/business')


@buz.route('')
def index():
    return redirect(url_for('.summary'))

@buz.route('/summary')
def summary():
    return render_template('business/summary.html')

@buz.route('/accounts')
def accounts():
    return render_template('business/accounts.html')

@buz.route('/customers')
def customers():
    return render_template('business/customers.html')

@buz.route('/suppliers')
def suppliers():
    return render_template('business/suppliers.html')
