# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for

prefs = Blueprint('preferences', __name__,
                  url_prefix='/preferences')

@prefs.route('')
def index():
    return render_template('preferences/index.html')

@prefs.route('/select-language', methods=['GET', 'POST'])
def select_language():
    if request.method == 'POST':
        return redirect(url_for('.index'))
    return render_template('preferences/select-language.html')

@prefs.route('/select-date-format', methods=['GET', 'POST'])
def select_date_format():
    if request.method == 'POST':
        return redirect(url_for('.index'))
    return render_template('preferences/select-date-format.html')

@prefs.route('/select-number-format', methods=['GET', 'POST'])
def select_number_format():
    if request.method == 'POST':
        return redirect(url_for('.index'))
    return render_template('preferences/select-number-format.html')

@prefs.route('/select-timezone', methods=['GET', 'POST'])
def select_timezone():
    if request.method == 'POST':
        return redirect(url_for('.index'))
    return render_template('preferences/select-timezone.html')
