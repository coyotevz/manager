# -*- coding: utf-8 -*-

from os import path, pardir

basedir = path.abspath(path.join(path.dirname(__file__), pardir))

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '<must be secret>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ASSETS_OUTPUT_DIR = 'assets'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'data.db')
    ASSETS_DEBUG = True
