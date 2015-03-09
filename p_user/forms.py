#!/usr/bin/env python

from wtforms import Form, TextField, PasswordField, HiddenField, ValidationError
from wtforms import validators as v
from flask_login import current_user
from flask.ext.sauth.models import User, authenticate
from .models import EsthenosOrg,EsthenosUser
class AddOrganisationForm( Form):
    org_name = TextField( validators=[v.DataRequired(), v.Length(max=255)])
    branches = TextField( validators=[v.DataRequired(), v.Length(max=512)])
    states = TextField( validators=[v.DataRequired(), v.Length(max=512)])
    areas = TextField( validators=[v.DataRequired(), v.Length(max=512)])
    regions = TextField( validators=[v.DataRequired(), v.Length(max=512)])
    postal_address = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    postal_telephone = TextField( validators=[v.DataRequired(), v.Length(max=20)])
    postal_tele_code = TextField( validators=[v.DataRequired(), v.Length(max=5)])
    postal_country = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    postal_state = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    postal_city = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    email = TextField( validators=[v.DataRequired(), v.Email(), v.Length(max=256), v.Email()])

    def validate_org_name( form, field):
        org_name = field.data.lower().strip()
        if( EsthenosOrg.objects(name=org_name).count()):
            raise ValidationError( "Hey! This organisation is already registered with us")

    def save( self):
        org = EsthenosOrg(name=self.org_name.data)
        #set fields
        org.branches = self.branches.data.split(",")
        org.states = self.states.data.split(",")
        org.areas = self.areas.data.split(",")
        org.regions = self.regions.data.split(",")
        org.postal_address = self.postal_address.data
        org.postal_telephone = self.postal_telephone.data
        org.postal_tele_code = self.postal_tele_code.data
        org.postal_country = self.postal_country.data
        org.postal_state = self.postal_state.data
        org.postal_city = self.postal_city.data
        org.owner =  EsthenosUser.objects.get(id=current_user.id)
        org.email = self.email.data
        org.save()
        return org