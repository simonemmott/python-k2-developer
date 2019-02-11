from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _
from app import db
from app.developer.forms import ApplicationForm, ServiceForm, AppServiceForm
from app.developer.model import Application, Service, AppService
from app.developer import bp
from k2_util import numUtil
   
    
@bp.route('/apps', methods=['GET'])
@login_required
def apps():
    page = request.args.get('page', 1, type=int)
    applications = Application.query.order_by(Application.name.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('developer.apps', page=applications.next_num) if applications.has_next else None
    prev_url = url_for('developer.apps', page=applications.prev_num) if applications.has_prev else None
    return render_template('developer/application/apps.html', title=_('Applications'),
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
    return render_template('developer/application/app.html', title=_('New Application'), form=form)
    

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
        page = request.args.get('page', 1, type=int)
        services = application.services.paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('app', id=application.id, page=servcies.next_num) if services.has_next else None
        prev_url = url_for('app', id=application.id, page=services.prev_num) if services.has_prev else None
    return render_template('developer/application/app.html', title=_('Application'), form=form, application=application, services=services.items)

@bp.route('/services', methods=['GET'])
@login_required
def services():
    page = request.args.get('page', 1, type=int)
    services = Service.query.order_by(Service.name.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('dev.services', page=servcies.next_num) if services.has_next else None
    prev_url = url_for('dev.services', page=services.prev_num) if services.has_prev else None
    return render_template('developer/service/services.html', title=_('Services'),
                           services=services.items, next_url=next_url,
                           prev_url=prev_url)
    

@bp.route('/services/new', methods=['GET', 'POST'])
@login_required
def new_service():
    service = Service()
    form = ServiceForm()
    if form.validate_on_submit():
        service.name = form.name.data
        service.description = form.description.data
        db.session.add(service)
        db.session.commit()
        flash(_('Your new service has been saved.'))
        return redirect(url_for('dev.services'))
    return render_template('developer/service/service.html', title=_('New Service'), form=form)
    

@bp.route('/service/<id>', methods=['GET', 'POST'])
@login_required
def service(id):
    if numUtil.is_int(id):
        service = Service.query.filter_by(id=id).first_or_404()
    else:
        service = Service.query.filter_by(name=id).first_or_404()

    form = ServiceForm()
    if form.validate_on_submit():
        service.name = form.name.data
        service.description = form.description.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('dev.services'))
    elif request.method == 'GET':
        form.source(service=service)
    return render_template('developer/service/service.html', title=_('Service'), form=form)

@bp.route('/app/<id>/services/new', methods=['GET', 'POST'])
@login_required
def new_app_service(id):
    if numUtil.is_int(id):
        application = Application.query.filter_by(id=id).first_or_404()
    else:
        application = Application.query.filter_by(name=id).first_or_404()
        
    app_service = AppService()
    form = AppServiceForm()
    form.source(application=application)
    if form.validate_on_submit():
        app_service.application = application
        app_service.service = Service.query.get(form.service.data)
        db.session.add(app_service)
        db.session.commit()
        flash(_('Your new service {srv} has added to your application.'.format(srv=app_service.service.name)))
        return redirect(url_for('dev.app', id=app_service.application.id))
    return render_template('developer/app_service/app_service.html', title=_('New Application Service'), form=form)
    

@bp.route('/app_service/<id>', methods=['GET', 'POST'])
@login_required
def app_service(id):
    app_service = AppService.query.filter_by(id=id).first_or_404()

    form = AppServiceForm()
    form.validate_on_submit()
#    print(form.application.data)
#    print(form.service.data)
    if request.method == 'POST':
        app_service.service = Service.query.get(form.service.data)
        app_service.application = app_service.application
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('dev.app', id=app_service.application.id))
    elif request.method == 'GET':
        form.source(app_service=app_service)
    return render_template('developer/app_service/app_service.html', title=_('Application Service'), form=form)

@bp.route('/app_service/<id>/delete', methods=['GET','POST'])
@login_required
def app_service_delete(id):
    app_service = AppService.query.filter_by(id=id).first_or_404()
    application_id = app_service.application_id
    db.session.delete(app_service)
    db.session.commit()
    return redirect(url_for('dev.app', id=application_id))


