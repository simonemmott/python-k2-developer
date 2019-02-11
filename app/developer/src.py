from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app, Response
from flask_login import current_user, login_required
from flask_babel import _
from app import db
from app.developer.forms import ApplicationForm
from app.developer.model import Application
from app.developer import bp
from k2_util import numUtil
from k2_core.source import Directory
   
def _application(id):
    if numUtil.is_int(id):
        return Application.query.filter_by(id=id).first_or_404()
    else:
        return Application.query.filter_by(name=id).first_or_404()

@bp.route('/app/<id>/src')
def application_src(id):

    application = _application(id)
        
    directory = Directory(application.name)
    directory.set('babel.cfg', url_for('dev.babel_src', id=application.id))
    directory.set('config.py', url_for('dev.config_src', id=application.id))
    directory.set('{app}.py'.format(app=application.name), url_for('dev.app_src', id=application.id))
        
    return directory.response()

@bp.route('/app/<id>/src/babel')
def babel_src(id):
    application = _application(id)
    resp = Response(status=200, content_type='text/text')
    resp.set_data(render_template('developer/src/babel.cfg', application=application))
    return resp

    
@bp.route('/app/<id>/src/config')
def config_src(id):
    application = _application(id)
    resp = Response(status=200, content_type='text/python')
    resp.set_data(render_template('developer/src/config.py', application=application))
    return resp
    
@bp.route('/app/<id>/src/app')
def app_src(id):
    application = _application(id)
    resp = Response(status=200, content_type='text/python')
    resp.set_data(render_template('developer/src/app.py', application=application))
    return resp
    
    