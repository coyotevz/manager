# -*- coding: utf-8 -*-

from flask_assets import Environment, Bundle


assets = Environment()

def configure_assets(app):
    assets.init_app(app)


scss = Bundle(
    'web/scss/main.scss',
    filters='libsass',
    depends='web/scss/*.scss',
)

style = Bundle(
    scss,
    'web/css/main.css',
    output='style.css',
    filters='cssmin',
)

script = Bundle(
    # jQuery first, then Tether, then Bootstrap JS.
    'web/js/jquery-3.1.1.slim.js',
    'web/js/tether.js',
    'web/js/bootstrap.js',
    filters='jsmin',
    output='script.js',
)

assets.register('style', style)
assets.register('script', script)
