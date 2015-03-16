#!/usr/bin/env python

from wtforms import Form, TextField, PasswordField, HiddenField, ValidationError, DateField
from wtforms import validators as v
from flask_login import current_user
from flask.ext.sauth.models import User, authenticate
from .models import EsthenosUser
from p_organisation.models import EsthenosOrg, EsthenosOrgProduct
from p_admin.models import EsthenosUser
from p_organisation.models import EsthenosOrg
from p_admin.models import EsthenosUser
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


class AddEmployeeForm( Form):
    FirstName = TextField( validators=[v.DataRequired(), v.Length(max=255)])
    LastName = TextField( validators=[v.DataRequired(), v.Length(max=512)])
    role = TextField( validators=[v.DataRequired(), v.Length(max=512)])
    DateOfBirth= TextField( validators=[v.DataRequired(), v.Length(max=512)])
    gender = TextField( validators=[v.DataRequired(), v.Length(max=12)])
    Address = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    TeleNo = TextField( validators=[v.DataRequired(), v.Length(max=20)])
    TeleCode = TextField( validators=[v.DataRequired(), v.Length(max=5)])
    Country = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    State = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    City = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    Email = TextField( validators=[v.DataRequired(), v.Email(), v.Length(max=256)])
    PostalCode=TextField(validators=[v.DataRequired(),v.Length(max=6)])

    def save( self):
        emp = EsthenosUser.create_user(self.FirstName.data,self.Email.data,"Pass123",True)
        emp.save()
        #set fields
        emp.first_name = self.FirstName.data
        emp.last_name = self.LastName.data
        emp.roles= list()
        emp.roles.append(self.role.data)
        emp.active = True
        emp.date_of_birth = self.DateOfBirth.data
        emp.postal_address = self.Address.data
        emp.postal_telephone = self.TeleNo.data
        emp.postal_tele_code = self.TeleCode.data
        emp.postal_country = self.Country.data
        emp.postal_state = self.State.data
        emp.postal_city = self.City.data
        emp.sex=self.gender.data
        emp.owner =  EsthenosUser.objects.get(id=current_user.id)
        emp.email = self.Email.data
        emp.save()

        return emp



class RegistrationFormAdmin( Form):
    name = TextField( validators=[v.DataRequired(), v.Length(max=256)])
    email = TextField( validators=[v.DataRequired(), v.Email(), v.Length(max=256), v.Email()])
    password = PasswordField( validators=[v.DataRequired(), v.Length(max=256)])
    type = HiddenField()

    def validate_email( form, field):
        email = field.data.lower().strip()
        if( EsthenosUser.objects(email=email).count()):
            raise ValidationError( "Hey! This email is already registered with us. Did you forget your password?")

    def save( self):
        user = EsthenosUser.create_user( self.name.data, self.email.data, self.password.data, email_verified=True)
        user.save()
        return user

class AddOrganizationEmployeeForm(Form):
    first_name_add_organisation=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    last_name_add_organisation=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    role=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    date_of_birth_add_organisation=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    gender=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    email_add_organisation= TextField( validators=[v.DataRequired(), v.Email(), v.Length(max=256), v.Email()])
    address_add_org_emp=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    city_add_organisation=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    state_add_organisation=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    country_add_organisation=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    postal_code_add_organisation=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    tele_code_add_organisation=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    teleno_add_organisation=TextField( validators=[v.DataRequired(), v.Length(max=255)])

    def validate_email_add_organisation( form,field):
        email_add_organisation = field.data.lower().strip()
        if( EsthenosUser.objects(email=email_add_organisation).count()):
            raise ValidationError( "Hey! This email is already registered with us. Did you forget your password?")
    def save( self,org_id):
        emp=EsthenosUser.create_user(self.first_name_add_organisation.data,self.email_add_organisation.data,"Esthenos",True)
        emp.organisation = EsthenosOrg.objects.get(id=org_id)
        emp.postal_address = self.address_add_org_emp.data
        emp.roles= list()
        emp.roles.append(self.role.data)
        emp.active = True
        emp.first_name = self.first_name_add_organisation.data
        emp.last_name = self.last_name_add_organisation.data
        emp.add_role(self.role.data)
        emp.date_of_birth = self.date_of_birth_add_organisation.data
        emp.postal_address = self.address_add_org_emp.data
        emp.postal_telephone = self.teleno_add_organisation.data
        emp.postal_tele_code = self.tele_code_add_organisation.data
        emp.postal_country = self.country_add_organisation.data
        emp.postal_state = self.state_add_organisation.data
        emp.postal_city = self.city_add_organisation.data
        emp.owner = EsthenosUser.objects.get(id=current_user.id)
        emp.name=self.first_name_add_organisation.data
        emp.email=self.email_add_organisation.data
        emp.save()
        return emp



class AddOrganisationProductForm(Form):

    product_name=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    loan_amount=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    life_insurance=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    eligible_cycle=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    number_installments=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    emi=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    last_emi=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    processing_fee=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    total_processing_fees=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    interest_rate=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    insurance_period=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    insurance_free_borrowers_only=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    insurance_free_borrowers_n_guarnteer=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    total_processing_fees_borrowers_n_guarnteer=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    emi_collection_period_weekly=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    emi_collection_period_monthly=TextField( validators=[v.DataRequired(), v.Length(max=255)])
    emi_collection_period_fortnightly=TextField( validators=[v.DataRequired(), v.Length(max=255)])


    def save(self,org_id):
        prod=EsthenosOrgProduct(name=self.product_name)
        prod.loan_amount=self.loan_amount.data
        prod.life_insurance=self.life_insurance.data
        prod.eligible_cycle=self.eligible_cycle.data
        prod.emi=self.emi.data
        prod.last_emi=self.last_emi.data
        prod.processing_fee=self.processing_fee.data
        prod.total_processing_fees=self.total_processing_fees.data
        prod.interest_rate=self.interest_rate.data
        prod.insurance_period=self.insurance_period.data
        prod.insurance_free_borrowers_only=self.insurance_free_borrowers_only.data
        prod.insurance_free_borrowers_n_guarnteer=self.insurance_free_borrowers_n_guarnteer.data
        prod.total_processing_fees_borrowers_n_guarnteer=self.total_processing_fees_borrowers_n_guarnteer.data
        prod.emi_collection_period_weekly=self.emi_collection_period_weekly.data
        prod.emi_collection_period_monthly=self.emi_collection_period_monthly.data
        prod.emi_collection_period_fortnightly=self.emi_collection_period_fortnightly.data
        prod.organisation=EsthenosOrg.objects.get(id=org_id)
        prod.save()
        return prod



