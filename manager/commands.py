# -*- coding: utf-8 -*-

import click

from manager.application import create_app
from manager.models import db


app = create_app()

@app.cli.command()
def initdb():
    """Creates database tables."""
    db.create_all()


@app.cli.command()
def dropdb():
    """Drop all database tables."""
    if click.confirm("Are you sure?  You will lose all your data!"):
        db.drop_all()
