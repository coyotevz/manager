# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, request

from ..models import db, Account, Supplier
from ..forms import SupplierForm


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

@buz.route('/suppliers')
def suppliers():
    suppliers = Supplier.query
    return render_template('business/suppliers.html', suppliers=suppliers)

@buz.route('/suppliers/new', methods=['GET', 'POST'])
def supplier_new():
    form = SupplierForm()
    if form.validate_on_submit():
        clean_data = {k: v for k, v in form.data.items() if (k != 'csrf_token' and v not in ('', None))}
        new_supplier = Supplier(**clean_data)
        db.session.add(new_supplier)
        db.session.commit()
        return redirect(url_for('.suppliers'))
    return render_template('business/supplier-form.html', new=True, form=form)

@buz.route('/suppliers/<int:id>')
def supplier_view(id):
    supplier = Supplier.query.get_or_404(id)
    return render_template('business/supplier-view.html', supplier=supplier)

@buz.route('/suppliers/<int:id>/edit', methods=['GET', 'POST'])
def supplier_edit(id):
    supplier = Supplier.query.get_or_404(id)
    return render_template('business/supplier-form.html', new=False)

@buz.route('/purchase-documents')
def purchase_documents():
    return render_template('business/purchase-documents.html', documents=None)
