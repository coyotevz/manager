# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

buz = Blueprint('business', __name__, url_prefix='/business')


@buz.route('')
def index():
    return render_template('business/index.html')
