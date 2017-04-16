# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from .preferences import prefs
from .business import buz

web = Blueprint('web', __name__, template_folder='templates', static_folder='static')

def configure_web(app):
    app.register_blueprint(web)
    app.register_blueprint(prefs)
    app.register_blueprint(buz)


@web.route('/')
def index():
    return render_template('index.html')

@web.route('/about')
def about():
    return render_template('about.html')
