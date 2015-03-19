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
    application_member_name= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_member_dob= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_member_co_name= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_member_relationship_status= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_telephone_number= TextField( validators=[ v.Length(max=100)])
    application_mobile_number= TextField( validators=[ v.Length(max=100)])
    application_member_applied_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_religion= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_category= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_cast= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_education= TextField( validators=[ v.Length(max=100)])
    application_type_of_residence= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_quality_of_house= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_drinking_water= TextField( validators=[ v.Length(max=100)])
    application_purpose_of_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_family_size= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_adult_count= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_children_below18= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_children_below12= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_monthly_income= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_business_category= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_business= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_secondary_business_income= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_family_asset= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_agricultural_land= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_self_owned= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_patta= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_shared= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_loans= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_chits= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_insurance= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_house_hold_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_food_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_medical_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_education_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_entertainment_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_festival_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_travel_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_friends_family_loans= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_friends_family_loan_roi= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_money_lenders_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_money_lenders_loan_roi= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_bank_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_bank_loan_roi= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_branch_name= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    applciation_branch_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_state_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_region_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_cm_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_cm_cell_no= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_repeat_client_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_cycle= TextField( validators=[v.DataRequired(), v.Length(max=100)])

    def save( self):
        return None