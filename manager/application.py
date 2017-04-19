# -*- coding: utf-8 -*-

from flask import Flask

from .models import configure_db
from .web import configure_web
from .assets import configure_assets


DEFAULT_APPNAME = 'manager-server'


def create_app(config=None, app_name=None):

    if app_name is None:
        app_name = DEFAULT_APPNAME

    app = Flask(app_name, static_folder='manager/web/static')

    configure_app(app, config)
    configure_db(app)
    configure_web(app)
    configure_assets(app)

    return app


def configure_app(app, config=None):

    if config is not None:
        app.config.from_object(config)
    else:
        try:
            app.config.from_object('localconfig.LocalConfig')
        except ImportError:
            app.config.from_object('manager.config.DevelopmentConfig')
