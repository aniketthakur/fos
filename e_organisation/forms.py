__author__ = 'prathvi'
#!/usr/bin/env python

from wtforms import Form, TextField, PasswordField, HiddenField, ValidationError, DateField
from wtforms import validators as v
from flask_login import current_user
from flask.ext.sauth.models import User, authenticate
from .models import EsthenosUser, EsthenosOrgApplication
from e_organisation.models import EsthenosOrg, EsthenosOrgProduct
from e_admin.models import EsthenosUser
from e_organisation.models import EsthenosOrg
from e_admin.models import EsthenosUser,EsthenosSettings
class UpdateApplicationForm( Form):
    application_postal_address =TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_telephone =TextField( validators=[v.DataRequired(), v.Length(max=20)])
    application_postal_tele_code =TextField( validators=[v.DataRequired(), v.Length(max=5)])
    application_postal_country =TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_state =TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_postal_city =TextField( validators=[v.DataRequired(), v.Length(max=100)])

    def save( self):
        return None

"""
ImmutableMultiDict([('kyc1_teleno', u''), ('center_name', u'MUDDANAHALLI'), ('kyc2_kycid', u'VB/05/041/336769'),
('group_name', u'DHANALAKSHMI'), ('kyc1_state', u'Andhra Pradesh'), ('kyc2_f_or_h_name', u'Name  Jovdeb'),
('postofficeaccount_inclusion', u'yes'), ('kyc2_country', u''), ('interested_in_health_indurance', u'yes'), ('kyc3_f_or_h_name', u' Mahesh Palekar'),
('kyc3_tele_code', u''), ('kyc2_city', u''), ('kyc1_country', u''),
('medical_expenditure', u'200'), ('interested_in_nps', u'yes'), ('centre_leader', u'Rajamma'), ('gkycid1', u'5513eb792a762065ac21c88b'),
 ('member_fullname', u'Pattan Saddam Hussain'), ('state', u'Karnataka'), ('interested_in_other_fp', u'yes'),
('select_t_business', u'ORCHARD'), ('radio_member_disability', u''), ('village_water', u'POND'), ('festival_expenditure', u'100'),
 ('cm_cell_no', u'8197998833'), ('kyc2_name', u' Mishra Suiit'), ('excepted_disbursment_date', u'27/03/2015'),
('kycid2', u'5513ebb22a762065ac21c88f'), ('village_medical_facilities', u'PHC'), ('micropension_inclusion', u'yes'), ('kyc2_state', u''),
 ('kyc3_name', u' Prathwirai Palekar'), ('p_income', u'3500'), ('self_owned_land', u'1 Acare'), ('member_address_proof', u''),
('center_leader_cell', u''), ('center_size', u'8'), ('select_type_of_residence', u'FAMILY_OWNED'), ('applicationtype', u'VID'),
('shared_land', u''), ('child', u'1'), ('child', u'1'), ('bankaccount_inclusion', u'yes'), ('kyc1_f_or_h_name', u'S/O Fyroz Basha'),
('fl_loans', u'2000'), ('guarantor_id_proof_number', u'ZMQ2471183'), ('fl_chits', u'2000'), ('kyc1_kycid', u'565061987998'),
('selec_p_business_category', u'TRADING'), ('village_hospital_category', u'ALLOPATHY'), ('chit_amount', u''),
('cm_id', u'0'), ('member_id_proof_number', u'565061987998'), ('member_telephone', u'8197998833'), ('kyc2_dob', u'20'),
('kyc1_postal_code', u''), ('group_leader_cell', u''), ('bankfi_amount', u''), ('kyc1_address', u'4/166'), ('patta_land', u'2Acare'),
('chits_inclusion', u'yes'), ('moneylenders_roi', u'15'), ('kyc3_dob', u'27/08/1988'), ('current_cycle', u'1'),
('kyc3_address', u''), ('member_age', u'25'), ('select_family_asset', u'MIXER'), ('select_family_asset', u'BULLOCK_CART'),
('select_family_asset', u'BYCYCLE'), ('guarantor_fullname', u' Prathwirai Palekar'), ('purpose_of_loan', u'farming'),
 ('group_size', u'100'), ('member_husband_age', u'45'), ('member_address_proof_number', u'VB/05/041/336769'),
 ('select_house_type', u'PAKKA'), ('village_road', u'CONCRETE'), ('kyc2_teleno', u''), ('kycid1', u'5513ebad2a762065ac21c88e'),
('chit_roi', u''), ('kyc1_dob', u'1992'), ('family_size', u'5'), ('member_address2', u'ABC'), ('select_s_business', u'ORCHARD'),
 ('member_address1', u'HAL'), ('food_expenditure', u'300'), ('repeat_client_id', u''), ('entertainment_expenditure', u'50'),
('kyc3_country', u''), ('kyc3_city', u''), ('member_id_proof', u''), ('kyc1_name', u'Pattan Saddam Hussain'), ('fnf_inclusion', u'2000'),
('education_expenditure', u'50'), ('branch', u'Branch1'), ('applied_loan_amount', u'10000'), ('member_f_or_h_name', u'S/O Fyroz Basha'),
('travel_expenditure', u'20'), ('t_income', u'1500'), ('member_pincode', u'580003'), ('repayment_mode', u'monthly'),
('taluk', u'Honavar'), ('group_leader', u'Ganga'), ('bankfi_roi', u''), ('member_husband_telephone', u'982929029'),
 ('kyc3_postal_code', u''), ('selec_p_business', u'ORCHARD'), ('select_member_religion', u'HINDU'),
('select_member_caste_category', u'GENERAL'), ('moneylenders_amount', u'1000'), ('guarantor_id_proof', u''),
('house_rent_expenditure', u''), ('s_income', u'1500'), ('village_public_transport', u'BUS'), ('kyc1_tele_code', u''),
 ('house_hold_expenditure', u'1000'), ('kyc2_address', u''), ('village_electricity', u'12HR'), ('kyc2_tele_code', u''),
('product_id', u'5513c64957ab391b2fb50191'), ('kyc1_city', u'Cuddapah'), ('region', u'R1'), ('kyc3_teleno', u''),
('kyc3_kycid', u'ZMQ2471183'), ('fl_insurance', u'2000'), ('select_drinking_water', u'PIPED'), ('kyc2_postal_code', u''),
('select_s_business_category', u'TRADING'), ('kyc3_state', u''), ('select_t_business_category', u'TRADING')])
    """
class AddApplicationManual(Form):
    member_telephone = TextField( validators=[ v.Length(max=20)])
    kyc1_country = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    member_fullname= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    family_size= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    adult_count= TextField( validators=[ v.Length(max=100)])
    children_below18= TextField( validators=[ v.Length(max=100)])
    children_below12= TextField( validators=[v.Length(max=100)])
    member_relationship_status= TextField( validators=[v.Length(max=100)])
    business= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    secondary_business_income= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    member_applied_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    religion= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    self_owned= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    patta= TextField( validators=[v.Length(max=100)])
    shared= TextField( validators=[ v.Length(max=100)])
    chits= TextField( validators=[ v.Length(max=100)])
    insurance= TextField( validators=[ v.Length(max=100)])
    quality_of_house= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    medical_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    education_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    travel_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    friends_family_loan_roi= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    bank_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    repeat_client_id= TextField( validators=[ v.Length(max=100)])
    cycle= TextField( validators=[v.DataRequired(), v.Length(max=100)])

    branch_name= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    postal_address = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    postal_tele_code = TextField( validators=[v.DataRequired(), v.Length(max=9)])
    postal_state = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    postal_city = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    postal_taluk= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    postal_village= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    member_dob= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    member_co_name= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    telephone_number= TextField( validators=[ v.Length(max=100)])
    mobile_number= TextField( validators=[ v.Length(max=100)])
    education= TextField( validators=[ v.Length(max=100)])
    category= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    cast= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    type_of_residence= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    drinking_water= TextField( validators=[ v.Length(max=100)])
    purpose_of_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    monthly_income= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    business_category= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    family_asset= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    agricultural_land= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    loans= TextField( validators=[ v.Length(max=100)])
    house_hold_expenditure= TextField( validators=[ v.Length(max=100)])
    food_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    entertainment_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    festival_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    friends_family_loans= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    money_lenders_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    money_lenders_loan_roi= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    bank_loan_roi= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    applciation_branch_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    state_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    region_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    cm_id= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    cm_cell_no= TextField( validators=[v.DataRequired(), v.Length(max=100)])

    repayment_method= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    tertiary_income= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    def save( self):
        app=EsthenosOrgApplication(applicant_name=self.member_fullname.data)
#        app.center =
#        app.organisation =
#        app.application_id =
#        app.upload_type =
#        app.status =
#        app.postal_telephone = self.member_telephone.data
#        app.postal_tele_code = self.postal_tele_code.data
#        app.postal_country = self.kyc1_country.data
#        app.postal_state = self.postal_state.data
#        app.postal_city = self.postal_city.data
#        app.postal_taluk = self.postal_taluk.data
#        app.postal_village = self.postal_village.data
#        app.member_relationship_status = self.member_relationship_status.data
#        app.telephone_number = self.telephone_number.data
#        app.mobile_number = self.mobile_number.data
#        app.member_applied_loan = self.member_applied_loan.data
#        app.religion = self.religion.data
#        app.category = self.category.data
#        app.cast = self.cast.data
#        app.education = self.education.data
#        app.type_of_residence = self.type_of_residence.data
#        app.quality_of_house = self.quality_of_house.data
#        app.drinking_water = self.drinking_water.data
#        app.purpose_of_loan = self.purpose_of_loan.data
#        app.family_size  = self.family_size.data
#        app.adult_count  = self.adult_count.data
#        app.children_below18 = self.children_below18.data
#        app.children_below12 = self.children_below12.data
#        app.business_category = self.business_category.data
#        app.business = self.business.data
#        app.family_asset = self.family_asset.data
#        app.money_lenders_loan = self.money_lenders_loan.data
#        app.money_lenders_loan_roi = self.money_lenders_loan_roi.data
#        app.bank_loan = self.bank_loan.data
#        app.bank_loan_roi = float(self.bank_loan_roi.data)
#        app.branch_name = self.branch_name.data
#        app.branch_id  = self.applciation_branch_id.data
#        app.state_id = self.state_id.data
#        app.region_id = self.region_id.data
#        app.cm_id = self.cm_id.data
#        app.cm_cell_no = self.cm_cell_no.data
#        app.repeat_client_id = self.repeat_client_id.data
#        app.repayment_method = self.repayment_method.data
#        app.applicant_name = self.member_name.data
#        app.dob = self.member_dob.data
#        app.address = self.postal_address.data
#        app.primary_income =float(self.monthly_income.data)
#        app.secondary_income = float(self.secondary_business_income.data)
#        app.tertiary_income =float(self.tertiary_income.data)
#
#        app.gender =
#        app.age =
#        app.other_income = 0
#        app.total_income = app.primary_income+app.secondary_income+app.tertiary_income+app.other_income
#        app.business_expense =
#        app.food_expense = float(self.food_expenditure.data)
#        app.travel_expense =float(self.travel_expenditure.data)
#        app.entertainment_expense =float(self.entertainment_expenditure.data)
#        app.educational_expense = float(self.education_expenditure.data)
#        app.medical_expense =float(self.medical_expenditure.data)
#        app.other_expense = float(self.house_hold_expenditure.data)
#        app.total_expenditure = app.food_expense+app.travel_expense+app.entertainment_expense+app.educational_expense+app.medical_expense+app.other_expense
#        app.total_liability =
#        app.outstanding_1 =
#        app.outstanding_2 =
#        app.outstanding_3 =
#        app.outstanding_4 =
#        app.total_outstanding =
#        app.other_outstanding_chit = float(self.chits.data)
#        app.other_outstanding_insurance = float(self.insurance.data)
#        app.other_outstanding_emi =
#        app.total_other_outstanding = app.other_outstanding_chit+app.other_outstanding_insurance
#        app.net_income = app.total_income - app.total_expenditure
#        app.total_running_loans =
#        app.total_existing_outstanding_from =
#        app.total_running_loans_from_mfi =
#        app.total_existing_outstanding_from_mfi =
#        app.existing_loan_cycle =
#        app.eligible_loan_cycle =self.cycle.data
#        app.defaults_with_no_mfis =
#        app.attendence_percentage =
#        app.loan_eligibility_based_on_net_income =
#        app.loan_eligibility_based_on_company_policy =
#        app.pan_card =
#        app.vid_card =
#        app.save()

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



