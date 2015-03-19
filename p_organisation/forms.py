__author__ = 'prathvi'
#!/usr/bin/env python

from wtforms import Form, TextField, PasswordField, HiddenField, ValidationError, DateField
from wtforms import validators as v
from flask_login import current_user
from flask.ext.sauth.models import User, authenticate
from .models import EsthenosUser
from p_organisation.models import EsthenosOrg, EsthenosOrgProduct
from p_admin.models import EsthenosUser
from p_organisation.models import EsthenosOrg
from p_admin.models import EsthenosUser,EsthenosSettings
class UpdateApplicationForm( Form):
    application_postal_address =TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_telephone =TextField( validators=[v.DataRequired(), v.Length(max=20)])
    application_postal_tele_code =TextField( validators=[v.DataRequired(), v.Length(max=5)])
    application_postal_country =TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_state =TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_city =TextField( validators=[v.DataRequired(), v.Length(max=100)])

    def save( self):
        return None


class AddApplicationMobile(Form):
    application_postal_address = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_telephone = TextField( validators=[v.DataRequired(), v.Length(max=20)])
    application_postal_tele_code = TextField( validators=[v.DataRequired(), v.Length(max=5)])
    application_postal_country = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_state = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_city = TextField( validators=[v.DataRequired(), v.Length(max=100)])

    def save( self):
        return None