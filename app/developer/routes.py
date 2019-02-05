from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _
from app import db
from app.developer.forms import ApplicationForm
from app.developer.models import Application
from app.developer import bp
from k2_util import numUtil
   
    
@bp.route('/apps', methods=['GET'])
@login_required
def apps():
    page = request.args.get('page', 1, type=int)
    applications = Application.query.order_by(Application.name.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('developer.apps', page=applications.next_num) if applications.has_next else None
    prev_url = url_for('developer.apps', page=applications.prev_num) if applications.has_prev else None
    return render_template('developer/apps.html', title=_('Applications'),
                           applications=applications.items, next_url=next_url,
                           prev_url=prev_url)
    

@bp.route('/apps/new', methods=['GET', 'POST'])
@login_required
def new_app():
    application = Application()
    form = ApplicationForm()
    if form.validate_on_submit():
        application.name = form.name.data
        application.description = form.description.data
        db.session.add(application)
        db.session.commit()
        flash(_('Your new application has been saved.'))
        return redirect(url_for('dev.apps'))
    return render_template('developer/app.html', title=_('Application'), form=form)
    

@bp.route('/app/<id>', methods=['GET', 'POST'])
@login_required
def app(id):
    if numUtil.is_int(id):
        application = Application.query.filter_by(id=id).first_or_404()
    else:
        application = Application.query.filter_by(name=id).first_or_404()

    form = ApplicationForm()
    if form.validate_on_submit():
        application.name = form.name.data
        application.description = form.description.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('dev.apps'))
    elif request.method == 'GET':
        form.source(application=application)
    return render_template('developer/app.html', title=_('Application'), form=form)


