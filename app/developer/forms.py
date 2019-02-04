from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from flask import request


class ApplicationForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    description = TextAreaField(_l('Description'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


