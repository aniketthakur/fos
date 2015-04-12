__author__ = 'prathvi'
#!/usr/bin/env python
import datetime
from wtforms import Form, TextField, PasswordField, HiddenField, ValidationError, DateField
from wtforms import validators as v
from flask_login import current_user
from flask.ext.sauth.models import User, authenticate
from .models import EsthenosUser, EsthenosOrgApplication,EsthenosOrgCenter,EsthenosOrgGroup,EsthenosOrgApplicationStatusType,EsthenosOrgApplicationStatus
from e_organisation.models import EsthenosOrg, EsthenosOrgProduct
from e_admin.models import EsthenosUser
from e_organisation.models import EsthenosOrg
from e_admin.models import EsthenosUser,EsthenosSettings

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
('kyc1_member_code', u''), ('group_leader_cell', u''), ('bankfi_amount', u''), ('kyc1_address', u'4/166'), ('patta_land', u'2Acare'),
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
 ('kyc3_member_code', u''), ('selec_p_business', u'ORCHARD'), ('select_member_religion', u'HINDU'),
('select_member_caste_category', u'GENERAL'), ('moneylenders_amount', u'1000'), ('guarantor_id_proof', u''),
('house_rent_expenditure', u''), ('s_income', u'1500'), ('village_public_transport', u'BUS'), ('kyc1_tele_code', u''),
 ('house_hold_expenditure', u'1000'), ('kyc2_address', u''), ('village_electricity', u'12HR'), ('kyc2_tele_code', u''),
('product_id', u'5513c64957ab391b2fb50191'), ('kyc1_city', u'Cuddapah'), ('region', u'R1'), ('kyc3_teleno', u''),
('kyc3_kycid', u'ZMQ2471183'), ('fl_insurance', u'2000'), ('select_drinking_water', u'PIPED'), ('kyc2_member_code', u''),
('select_s_business_category', u'TRADING'), ('kyc3_state', u''), ('select_t_business_category', u'TRADING')])
    """
class AddApplicationManual(Form):
    application_id = TextField( validators=[v.DataRequired(), v.Length(max=40)])
    center_name = TextField( validators=[v.DataRequired(), v.Length(max=40)])
    group_name = TextField( validators=[v.DataRequired(), v.Length(max=40)])
    medical_expenditure= TextField( validators=[ v.Length(max=10)])
    interested_in_nps= TextField( validators=[v.DataRequired(), v.Length(max=40)])
    centre_leader=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    member_fullname=TextField( validators=[ v.Length(max=100)])
    state=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    interested_in_other_fp=TextField( validators=[v.DataRequired(), v.Length(max=40)])

    select_t_business=TextField( validators=[v.DataRequired(), v.Length(max=30)])
    select_s_business=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    select_p_business=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    select_p_business_category=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    select_s_business_category=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    select_t_business_category=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    p_income=TextField( validators=[v.DataRequired(), v.Length(max=7)])
    s_income=TextField( validators=[ v.Length(max=7)])
    t_income=TextField( validators=[ v.Length(max=7)])

    radio_member_disability=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    village_water=TextField( validators=[v.DataRequired(), v.Length(max=30)])
    festival_expenditure=TextField( validators=[ v.Length(max=10)])
    cm_cell_no=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    excepted_disbursment_date=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    village_medical_facilities=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    micropension_inclusion=TextField( validators=[v.DataRequired(), v.Length(max=40)])

    self_owned_land=TextField( validators=[ v.Length(max=10)])
    member_address_proof=TextField( validators=[ v.Length(max=400)])
    center_leader_cell=TextField( validators=[ v.Length(max=10)])
    center_size=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    select_type_of_residence=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    application_type=TextField( validators=[ v.Length(max=40)])
    application_type2=TextField( validators=[ v.Length(max=40)])
    application_type3=TextField( validators=[ v.Length(max=40)])
    shared_land=TextField( validators=[ v.Length(max=10)])
    child=TextField( validators=[ v.Length(max=10)])
    bankaccount_inclusion=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    fl_loans=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    guarantor_id_proof_number=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    fl_chits=TextField( validators=[v.DataRequired(), v.Length(max=40)])

    village_hospital_category=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    chit_amount=TextField( validators=[ v.Length(max=10)])
    cm_id=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    member_telephone=TextField( validators=[ v.Length(max=40)])
    group_leader_cell=TextField( validators=[ v.Length(max=10)])
    bankfi_amount=TextField( validators=[ v.Length(max=10)])
    patta_land=TextField( validators=[ v.Length(max=10)])
    chits_inclusion=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    moneylenders_roi=TextField( validators=[ v.Length(max=10)])
    current_cycle=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    member_age=TextField( validators=[ v.Length(max=40)])
    select_family_asset=TextField( validators=[ v.Length(max=40)])
    guarantor_fullname=TextField( validators=[v.DataRequired(), v.Length(max=100)])
    purpose_of_loan=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    group_size=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    member_husband_age=TextField( validators=[v.DataRequired(), v.Length(max=3)])
    member_id_proof_number=TextField( validators=[ v.Length(max=40)])
    select_house_type=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    village_road=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    chit_roi=TextField( validators=[ v.Length(max=10)])
    family_size=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    member_address2=TextField( validators=[ v.Length(max=40)])

    member_address1=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    food_expenditure=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    repeat_client_id=TextField( validators=[ v.Length(max=40)])
    entertainment_expenditure=TextField( validators=[ v.Length(max=10)])

    fnf_inclusion=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    education_expenditure=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    branch=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    applied_loan_amount=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    member_f_or_h_name=TextField( validators=[ v.Length(max=40)])
    travel_expenditure=TextField( validators=[ v.Length(max=10)])

    member_pincode=TextField( validators=[ v.Length(max=40)])
    repayment_mode=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    taluk=TextField( validators=[ v.Length(max=40)])
    group_leader=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    bankfi_roi=TextField( validators=[ v.Length(max=10)])
    member_husband_telephone=TextField( validators=[ v.Length(max=40)])

    select_member_religion=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    select_member_caste_category=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    moneylenders_amount=TextField( validators=[ v.Length(max=10)])
    house_rent_expenditure=TextField( validators=[ v.Length(max=10)])
    s_income=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    village_public_transport=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    house_hold_expenditure=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    village_electricity=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    product_id=TextField( validators=[v.DataRequired(), v.Length(max=64)])
    region=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    fl_insurance=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    select_drinking_water=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    select_t_business_category=TextField( validators=[v.DataRequired(), v.Length(max=40)])
    village=TextField( validators=[ v.Length(max=40)])
    JLG=TextField( validators=[ v.Length(max=10)])
    SHG=TextField( validators=[ v.Length(max=10)])
    borroers_cell=TextField( validators=[ v.Length(max=40)])
    leader_cell=TextField( validators=[ v.Length(max=40)])
    leader_cell1=TextField( validators=[ v.Length(max=40)])
    guarantor_borrowers_are_nominee=TextField( validators=[ v.Length(max=40)])
    borrower_s=TextField( validators=[ v.Length(max=40)])
    guranteer_s=TextField( validators=[ v.Length(max=40)])
    select_education=TextField( validators=[ v.Length(max=40)])
    girl=TextField( validators=[ v.Length(max=10)])
    boy=TextField( validators=[ v.Length(max=10)])
    p_expense=TextField( validators=[ v.Length(max=40)])
    s_expense=TextField( validators=[ v.Length(max=40)])
    t_expense=TextField( validators=[ v.Length(max=40)])



    def save( self):
        app = EsthenosOrgApplication.objects.filter(application_id=self.application_id.data)[0]
        app.applicant_name=self.member_fullname.data
        app.member_telephone = self.member_telephone.data
#       app.member_tele_code = self.postal_tele_code.data
#       app.member_country = self.kyc1_country.data
        app.member_state = self.state.data
#       app.member_city = self.member_city.data
        app.member_taluk = self.taluk.data
#        app.member_village = self.member_village.data
#        app.member_relationship_status = self.member_relationship_status.data
        app.telephone_number = self.member_husband_telephone.data
#        app.mobile_number = self.mobile_number.data
        app.member_applied_loan = self.applied_loan_amount.data
        app.religion = self.select_member_religion.data
        # app.category = self.select_member_caste_category.data
        app.caste = self.select_member_caste_category.data
        app.education = self.education_expenditure.data
        app.type_of_residence = self.select_type_of_residence.data
#        app.quality_of_house = self.quality_of_house.data
        app.drinking_water = self.select_drinking_water.data
        app.purpose_of_loan = self.purpose_of_loan.data
        app.family_size  = self.family_size.data
#        app.adult_count  = self.adult_count.data
        app.children_below18 = self.child.data
#        app.children_below12 = self.children_below12.data
        app.primary_business = self.select_p_business.data
        app.secondary_business = self.select_s_business.data
        app.tertiary_business=self.select_t_business.data

        app.primary_business_category = self.select_p_business_category.data
        app.secondary_business_category = self.select_s_business_category.data
        app.tertiary_business_category=self.select_s_business_category.data
        if self.p_income.data == "":
            self.p_income.data = "0"
        if self.s_income.data == "":
            self.s_income.data = "0"
        if self.t_income.data == "":
            self.t_income.data = "0"
        app.primary_income =float(self.p_income.data)
        app.secondary_income = float(self.s_income.data)
        app.tertiary_income =float(self.t_income.data)

        app.family_asset = self.select_family_asset.data
#        app.money_lenders_loan = self.money_lenders_loan.data
        app.money_lenders_loan_roi = float(self.moneylenders_roi.data)
        if self.bankfi_roi.data == "":
            self.bankfi_roi.data = "0"
        app.bank_loan_roi =  float(self.bankfi_roi.data)
        app.branch_name = self.branch.data
#        app.branch_id  = self.applciation_branch_id.data
#        app.state_id = self.state_id.data
#        app.region_id = self.region_id.data
        app.cm_id = self.cm_id.data
        app.cm_cell_no = self.cm_cell_no.data
#        app.repeat_client_id = self.repeat_client_id.data
#        app.repayment_method = self.repayment_method.data
        app.applicant_name = self.member_fullname.data
#        app.dob = self.member_dob.data
        app.address = self.member_address1.data + self.member_address2.data
#        app.gender =
        app.age =int(self.member_age.data)
        app.member_f_or_h_age = int(self.member_husband_age.data)
#        app.other_income = 0
        app.total_income = app.primary_income+app.secondary_income+app.tertiary_income+app.other_income
#        app.business_expense =
        app.food_expense = float(self.food_expenditure.data)
        app.travel_expense =float(self.travel_expenditure.data)
        app.entertainment_expense =float(self.entertainment_expenditure.data)
        # app.educational_expense = float(self.education_expenditure.data)
        # app.medical_expense =float(self.medical_expenditure.data)

#        app.other_expense = float(self.house_hold_expenditure.data)
#        app.total_expenditure = app.food_expense+app.travel_expense+app.entertainment_expense+app.educational_expense+app.medical_expense+app.other_expense
#        app.total_liability =
#        app.outstanding_1 =
#        app.outstanding_2 =
#        app.outstanding_3 =
#        app.outstanding_4 =
#        app.total_outstanding =
        if self.fl_chits.data == "":
            self.fl_chits.data = "0"
        if self.chit_amount.data == "":
            self.chit_amount.data = "0"
        if self.chits_inclusion.data == "":
            self.chits_inclusion.data = "0"

        app.other_outstanding_chit = float(self.fl_chits.data)+float(self.chit_amount.data)
        app.other_outstanding_insurance = float(self. fl_insurance.data)
#        app.other_outstanding_emi =
#        app.total_other_outstanding = app.other_outstanding_chit+app.other_outstanding_insurance
        app.net_income = float(self.p_income.data)+float(self.s_income.data)+float(self.t_income.data)

#        app.loan_eligibility_based_on_net_income =
#        app.loan_eligibility_based_on_company_policy =

        app.village_electricity=self.village_electricity.data
        app.interested_in_other_fp=self.interested_in_other_fp.data
        app.radio_member_disability=self.radio_member_disability.data
        app.village_water=self.village_water.data
        app.festival_expenditure=self.festival_expenditure.data
        app.village_medical_facilities=self.village_medical_facilities.data
        app.micropension_inclusion=self.micropension_inclusion.data
        app.self_owned_land=self.self_owned_land.data
        app.center_leader_cell=self.center_leader_cell.data
        app.center_size=self.center_size.data
        app.applicationtype=self.application_type.data
        app.shared_land=self.shared_land.data
        app.bankaccount_inclusion=self.bankaccount_inclusion.data
        app.fl_loans=self.fl_loans.data
        app.village_hospital_category=self.village_hospital_category.data
        app.group_leader_cell=self.group_leader_cell.data
        if self.bankfi_amount.data == "":
            self.bankfi_amount.data = "0"
        app.bank_loan=float(self.bankfi_amount.data)
        app.patta_land=self.patta_land.data
        app.group_size=self.group_size.data
        app.select_house_type=self.select_house_type.data
        app.village_road=self.village_road.data
        app.fnf_inclusion=self.fnf_inclusion.data
        app.member_f_or_h_name=self.member_f_or_h_name.data
        app.member_pincode=self.member_pincode.data
        app.repayment_mode=self.repayment_mode.data

        app.moneylenders_amount=self.moneylenders_amount.data
        if self.house_rent_expenditure.data == "":
            self.house_rent_expenditure.data = "0"
        app.house_rent_expenditure= float(self.house_rent_expenditure.data)
        app.village_public_transport=self.village_public_transport.data
        app.house_hold_expenditure=self.house_hold_expenditure.data
        app.village=self.village.data
        app.JLG=self.JLG.data
        app.SHG=self.SHG.data
        app.borroers_cell=self.borroers_cell.data
        app.leader_cell=self.leader_cell.data
        app.leader_cell1=self.leader_cell1.data
        app.guarantor_borrowers_are_nominee=self.guarantor_borrowers_are_nominee.data
        app.borrower_s=self.borrower_s.data
        app.guranteer_s=self.guranteer_s.data
        app.select_education=self.select_education.data
        app.girl=self.girl.data
        app.boy=self.boy.data
        if self.p_expense.data == "":
            self.p_expense.data = "0"
        if self.s_expense.data == "":
            self.s_expense.data = "0"
        if self.t_expense.data == "":
            self.t_expense.data = "0"
        app.p_expense=float(self.p_expense.data)
        app.s_expense=float(self.s_expense.data)
        app.t_expense= float(self.t_expense.data)
        app.i_total=app.primary_income+app.secondary_income+app.tertiary_income
        app.e_total=app.p_expense+app.s_expense+app.t_expense
        app.member_id_proof_number=self.member_id_proof_number.data

        status = EsthenosOrgApplicationStatus(status = app.current_status,updated_on=app.current_status_updated)
        status.save()
        app.timeline.append(status)

        app.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=4)
        app.current_status_updated = datetime.datetime.now()
        app.status = 4
        app.save()

        return None



"""
{'application_member_village': [u'This field is required.'], 'application_cast': [u'This field is required.'],
 'application_cm_id': [u'This field is required.'], 'application_category': [u'This field is required.'],
 'application_self_owned': [u'This field is required.'], 'applciation_branch_id': [u'This field is required.'],
 'application_bank_loan_roi': [u'This field is required.'], 'application_region_id': [u'This field is required.'],
 'application_monthly_income': [u'This field is required.'], 'application_member_country': [u'This field is required.'],
 'application_family_asset': [u'This field is required.'], 'application_cm_cell_no': [u'This field is required.'],
 'application_family_size': [u'This field is required.'], 'application_education_expenditure': [u'This field is required.'],
 'application_money_lenders_loan': [u'This field is required.'], 'application_food_expenditure': [u'This field is required.'],
 'application_money_lenders_loan_roi': [u'This field is required.'], 'application_entertainment_expenditure': [u'This field is required.'],
 'application_cycle': [u'This field is required.'], 'application_branch_name': [u'This field is required.'],
 'application_friends_family_loan_roi': [u'This field is required.'], 'application_state_id': [u'This field is required.']}

"""
class AddApplicationMobile(Form):

    application_id=TextField( validators=[ v.Length(max=40)])
    application_member_telephone = TextField( validators=[ v.Length(max=40)])
    application_member_country = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    group_name = TextField( validators=[v.DataRequired(), v.Length(max=40)])
    center_name = TextField( validators=[v.DataRequired(), v.Length(max=40)])
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
    application_self_owned= TextField( validators=[ v.Length(max=100)])
    application_patta= TextField( validators=[v.Length(max=100)])
    application_shared= TextField( validators=[ v.Length(max=100)])
    application_chits= TextField( validators=[ v.Length(max=100)])
    application_insurance= TextField( validators=[ v.Length(max=100)])
    application_quality_of_house= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_medical_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_education_expenditure= TextField( validators=[ v.Length(max=100)])
    application_travel_expenditure= TextField( validators=[ v.Length(max=100)])
    application_friends_family_loan_roi= TextField( validators=[ v.Length(max=100)])
    application_bank_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_repeat_client_id= TextField( validators=[ v.Length(max=100)])
    application_cycle= TextField( validators=[ v.Length(max=100)])

    application_branch_name= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_member_address = TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_member_tele_code = TextField( validators=[ v.Length(max=9)])
    application_member_state = TextField( validators=[v.Length(max=100)])
    application_member_city = TextField( validators=[ v.Length(max=100)])
    application_member_taluk= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_member_village= TextField( validators=[ v.Length(max=100)])
    application_member_dob= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_member_co_name= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_telephone_number= TextField( validators=[ v.Length(max=100)])
    application_mobile_number= TextField( validators=[ v.Length(max=100)])
    application_education= TextField( validators=[ v.Length(max=100)])
    application_category= TextField( validators=[ v.Length(max=100)])
    application_cast= TextField( validators=[ v.Length(max=100)])
    application_type_of_residence= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_drinking_water= TextField( validators=[ v.Length(max=100)])
    application_purpose_of_loan= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_monthly_income= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_business_category= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_family_asset= TextField( validators=[ v.Length(max=100)])
    application_agricultural_land= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_loans= TextField( validators=[ v.Length(max=100)])
    application_house_hold_expenditure= TextField( validators=[ v.Length(max=100)])
    application_food_expenditure= TextField( validators=[ v.Length(max=100)])
    application_entertainment_expenditure= TextField( validators=[ v.Length(max=100)])
    application_festival_expenditure= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_friends_family_loans= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_money_lenders_loan= TextField( validators=[ v.Length(max=100)])
    application_money_lenders_loan_roi= TextField( validators=[ v.Length(max=100)])
    application_bank_loan_roi= TextField( validators=[ v.Length(max=100)])
    applciation_branch_id= TextField( validators=[ v.Length(max=100)])
    application_state_id= TextField( validators=[ v.Length(max=100)])
    application_region_id= TextField( validators=[ v.Length(max=100)])
    application_cm_id= TextField( validators=[ v.Length(max=100)])
    application_cm_cell_no= TextField( validators=[v.DataRequired(), v.Length(max=100)])

    application_repayment_method= TextField( validators=[v.DataRequired(), v.Length(max=100)])
    application_tertiary_income= TextField( validators=[v.DataRequired(), v.Length(max=100)])

    def save( self):
        c_user = current_user
        user = EsthenosUser.objects.get(id=c_user.id)
        app=EsthenosOrgApplication(applicant_name=self.application_member_name.data)
        center,status = EsthenosOrgCenter.objects.get_or_create(center_name=self.center_name.data,organisation=user.organisation)
        group,status = EsthenosOrgGroup.objects.get_or_create(center=center,organisation=user.organisation,group_name=self.group_name.data)
        app.organisation = user.organisation
        app.center = center
        app.group = group
        app.owner = user
        app.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=5)
        app.current_status_updated = datetime.datetime.now()
        settings = EsthenosSettings.objects.all()[0]
        inc_count = EsthenosOrg.objects.get(id = user.organisation.id).application_count+1
        app.application_id = user.organisation.name.upper()[0:2]+str(settings.organisations_count)+"{0:06d}".format(inc_count)
        app.upload_type = "AUTOMATIC_UPLOAD"
        EsthenosOrg.objects.get(id = user.organisation.id).update(inc__application_count=1)
        app.status = 0
        app.member_telephone = self.application_member_telephone.data
        app.member_tele_code = self.application_member_tele_code.data
        app.member_country = self.application_member_country.data
        app.member_state = self.application_member_state.data
        app.member_city = self.application_member_city.data
        app.member_taluk = self.application_member_taluk.data
        app.member_village = self.application_member_village.data
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
        app.adult_count  = int(self.application_adult_count.data)
#        app.children_below18 = int(self.application_children_below18.data)
#        app.children_below12 = int(self.application_children_below12.data)
        app.business_category = self.application_business_category.data
        app.business = self.application_business.data
        app.family_asset = self.application_family_asset.data
#        app.money_lenders_loan = float(self.application_money_lenders_loan.data)
#        app.money_lenders_loan_roi = float(self.application_money_lenders_loan_roi.data)
        app.bank_loan = float(self.application_bank_loan.data)
#        app.bank_loan_roi = float(self.application_bank_loan_roi.data)
#        app.branch_name = self.application_branch_name.data
#        app.branch_id  = self.applciation_branch_id.data
#        app.state_id = self.application_state_id.data
#        app.region_id = self.application_region_id.data
#        app.cm_id = self.application_cm_id.data
#        app.cm_cell_no = self.application_cm_cell_no.data
#        app.repeat_client_id = self.application_repeat_client_id.data
        app.repayment_method = self.application_repayment_method.data
        app.applicant_name = self.application_member_name.data
        app.dob = self.application_member_dob.data
        app.address = self.application_member_address.data
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
#        app.other_outstanding_insurance = float(self.application_insurance.data)
#       app.other_outstanding_emi =
        app.total_other_outstanding = app.other_outstanding_chit+app.other_outstanding_insurance
        app.net_income = app.total_income - app.total_expenditure
#       app.total_running_loans =
#       app.total_existing_outstanding_from =
#       app.total_running_loans_from_mfi =
#       app.total_existing_outstanding_from_mfi =
#       app.existing_loan_cycle =
#        app.eligible_loan_cycle =self.application_cycle.data
#       app.defaults_with_no_mfis =
#       app.attendence_percentage =
#       app.loan_eligibility_based_on_net_income =
#       app.loan_eligibility_based_on_company_policy =

        status = EsthenosOrgApplicationStatus(status = app.current_status,updated_on=app.current_status_updated)
        status.save()
        app.timeline.append(status)

        app.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=4)
        app.current_status_updated = datetime.datetime.now()
        app.status = 4
        app.save()

        return None



        #fields present in form and not in models



