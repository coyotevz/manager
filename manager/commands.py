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


@app.cli.command('import')
@click.argument('filename')
def import_xml(filename):
    """Import data from XML file."""
    from xml.etree import ElementTree as ET
    from manager.models.account import import_account_data
    from manager.models.supplier import import_supplier_data

    click.echo("Importing data from: {}".format(filename))
    tree = ET.parse(filename)

    db.create_all()

    for accounts_data in tree.findall('accounts'):
        import_account_data(accounts_data)

    for suppliers_data in tree.findall('suppliers'):
        import_supplier_data(suppliers_data)

    db.session.commit()
