__author__ = 'prathvi'
#!/usr/bin/env python

from wtforms import Form, TextField, PasswordField, HiddenField, ValidationError, DateField
from wtforms import validators as v
from flask_login import current_user
from flask.ext.sauth.models import User, authenticate
from .models import EsthenosUser, EsthenosOrgApplication
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


    application_postal_telephone = TextField( validators=[ v.Length(max=20)])
    application_postal_country = TextField( validators=[v.DataRequired(), v.Length(max=100)])

    application_member_name= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_family_size= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_adult_count= TextField( validators=[ v.Length(max=100)])
    application_children_below18= TextField( validators=[ v.Length(max=100)])
    application_children_below12= TextField( validators=[v.Length(max=100)])
    application_member_relationship_status= TextField( validators=[v.Length(max=100)])
    application_business= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_secondary_business_income= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_member_applied_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_religion= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_self_owned= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_patta= TextField( validators=[v.Length(max=100)])
    application_shared= TextField( validators=[ v.Length(max=100)])
    application_chits= TextField( validators=[ v.Length(max=100)])
    application_insurance= TextField( validators=[ v.Length(max=100)])
    application_quality_of_house= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_medical_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_education_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_travel_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_friends_family_loan_roi= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_bank_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_repeat_client_id= TextField( validators=[ v.Length(max=100)])
    application_cycle= TextField( validators=[v.DataRequired(), v.Length(max=100)])

    application_branch_name= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_address = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_tele_code = TextField( validators=[v.DataRequired(), v.Length(max=9)])
    application_postal_state = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_city = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_taluk= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_village= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_member_dob= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_member_co_name= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_telephone_number= TextField( validators=[ v.Length(max=100)])
    application_mobile_number= TextField( validators=[ v.Length(max=100)])
    application_education= TextField( validators=[ v.Length(max=100)])
    application_category= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_cast= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_type_of_residence= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_drinking_water= TextField( validators=[ v.Length(max=100)])
    application_purpose_of_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_monthly_income= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_business_category= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_family_asset= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_agricultural_land= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_loans= TextField( validators=[ v.Length(max=100)])
    application_house_hold_expenditure= TextField( validators=[ v.Length(max=100)])
    application_food_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_entertainment_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_festival_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_friends_family_loans= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_money_lenders_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_money_lenders_loan_roi= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_bank_loan_roi= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    applciation_branch_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_state_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_region_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_cm_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_cm_cell_no= TextField( validators=[v.DataRequired(), v.Length(max=100)])

    application_repayment_method= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_tertiary_income= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    def save( self):
        app=EsthenosOrgApplication(applicant_name=self.application_member_name.data)
#       app.center = self.application_
#       app.organisation =
#       app.application_id =
#       app.upload_type =
#       app.status =
        app.postal_telephone = self.application_postal_telephone.data
        app.postal_tele_code = self.application_postal_tele_code.data
        app.postal_country = self.application_postal_country.data
        app.postal_state = self.application_postal_state.data
        app.postal_city = self.application_postal_city.data
        app.postal_taluk = self.application_postal_taluk.data
        app.postal_village = self.application_postal_village.data
        app.member_relationship_status = self.application_member_relationship_status.data
        app.telephone_number = self.application_telephone_number.data
        app.mobile_number = self.application_mobile_number.data
        app.member_applied_loan = self.application_member_applied_loan.data
        app.religion = self.application_religion.data
        app.category = self.application_category.data
        app.cast = self.application_cast.data
        app.education = self.application_education.data
        app.type_of_residence = self.application_type_of_residence.data
        app.quality_of_house = self.application_quality_of_house.data
        app.drinking_water = self.application_drinking_water.data
        app.purpose_of_loan = self.application_purpose_of_loan.data
        app.family_size  = self.application_family_size.data
        app.adult_count  = self.application_adult_count.data
        app.children_below18 = self.application_children_below18.data
        app.children_below12 = self.application_children_below12.data
        app.business_category = self.application_business_category.data
        app.business = self.application_business.data
        app.family_asset = self.application_family_asset.data
        app.money_lenders_loan = self.application_money_lenders_loan.data
        app.money_lenders_loan_roi = self.application_money_lenders_loan_roi.data
        app.bank_loan = self.application_bank_loan.data
        app.bank_loan_roi = float(self.application_bank_loan_roi.data)
        app.branch_name = self.application_branch_name.data
        app.branch_id  = self.applciation_branch_id.data
        app.state_id = self.application_state_id.data
        app.region_id = self.application_region_id.data
        app.cm_id = self.application_cm_id.data
        app.cm_cell_no = self.application_cm_cell_no.data
        app.repeat_client_id = self.application_repeat_client_id.data
        app.repayment_method = self.application_repayment_method.data
        app.applicant_name = self.application_member_name.data
        app.dob = self.application_member_dob.data
        app.address = self.application_postal_address.data
        app.primary_income =float(self.application_monthly_income.data)
        app.secondary_income = float(self.application_secondary_business_income.data)
        app.tertiary_income =float(self.application_tertiary_income.data)

#       app.gender =
#       app.age =
        app.other_income = 0
        app.total_income = app.primary_income+app.secondary_income+app.tertiary_income+app.other_income
#       app.business_expense =
        app.food_expense = float(self.application_food_expenditure.data)
        app.travel_expense =float(self.application_travel_expenditure.data)
        app.entertainment_expense =float(self.application_entertainment_expenditure.data)
        app.educational_expense = float(self.application_education_expenditure.data)
        app.medical_expense =float(self.application_medical_expenditure.data)
        app.other_expense = float(self.application_house_hold_expenditure.data)
        app.total_expenditure = app.food_expense+app.travel_expense+app.entertainment_expense+app.educational_expense+app.medical_expense+app.other_expense
#       app.total_liability =
#       app.outstanding_1 =
#       app.outstanding_2 =
#       app.outstanding_3 =
#       app.outstanding_4 =
#       app.total_outstanding =
        app.other_outstanding_chit = float(self.application_chits.data)
        app.other_outstanding_insurance = float(self.application_insurance.data)
#       app.other_outstanding_emi =
        app.total_other_outstanding = app.other_outstanding_chit+app.other_outstanding_insurance
        app.net_income = app.total_income - app.total_expenditure
#       app.total_running_loans =
#       app.total_existing_outstanding_from =
#       app.total_running_loans_from_mfi =
#       app.total_existing_outstanding_from_mfi =
#       app.existing_loan_cycle =
        app.eligible_loan_cycle =self.application_cycle.data
#       app.defaults_with_no_mfis =
#       app.attendence_percentage =
#       app.loan_eligibility_based_on_net_income =
#       app.loan_eligibility_based_on_company_policy =
#       app.pan_card =
#       app.vid_card =
        app.save()

        return None



        #fields present in form and not in models



