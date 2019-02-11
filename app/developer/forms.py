from flask import request
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.developer.model import Application, Service
from flask import request


class ApplicationForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    description = TextAreaField(_l('Description'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    
    def source(self, **kw):
        if kw.get('application'):
            app = kw.get('application')
            self.name.data = app.name
            self.description.data = app.description

class ServiceForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    description = TextAreaField(_l('Description'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    
    def source(self, **kw):
        if kw.get('service'):
            service = kw.get('service')
            self.name.data = service.name
            self.description.data = service.description

class AppServiceForm(FlaskForm):
    application = SelectField(_l('Application'), 
                              coerce=int)
    service = SelectField(_l('Service'), 
                          coerce=int)
    submit = SubmitField(_l('Submit'))
    delete = SubmitField(_l('Delete'))
    
    def validate_application(self, application):
        return True
    
    def validate_service(self, service):
        return True
    
    def __init__(self,*args, **kw):
        FlaskForm.__init__(self, *args, **kw)
        self.application.choices = [(a.id, a.name) for a in Application.query.order_by('name')]
        self.service.choices = [(a.id, a.name) for a in Service.query.order_by('name')]
    
    def source(self, **kw):
        self.application.disabled=False
        self.service.disabled=False
        if kw.get('app_service'):
            app_service = kw.get('app_service')
            self.application.data = app_service.application_id
            self.application.disabled=True
            self.service.data = app_service.service_id
            self.app_service_id = app_service.id
        if kw.get('application'):
            application = kw.get('application')
            self.application.data = application.id
            self.application.disabled=True
        if kw.get('service'):
            service = kw.get('service')
            self.service.data = service.id
            self.service.diabled=True

#        self.application.choices = [(a.id, a.name) for a in Application.query.order_by('name')]
#        self.service.choices = [(a.id, a.name) for a in Service.query.order_by('name')]


