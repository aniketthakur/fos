import json
import datetime
from wtforms import Form, TextField, PasswordField, HiddenField, ValidationError, DateField
from wtforms import validators as v
from flask_login import current_user

from e_admin.models import EsthenosUser, EsthenosSettings
from e_organisation.models import *


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
        app = EsthenosOrgApplication.objects.get(application_id=self.application_id.data)
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
        app.applied_loan = float(self.applied_loan_amount.data)
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
        try:
            app.group_size=int(self.group_size.data)
        except Exception as e:
            print e.message
        app.village_road=self.village_road.data
        app.fnf_inclusion=self.fnf_inclusion.data
        app.member_f_or_h_name=self.member_f_or_h_name.data
        app.member_pincode=self.member_pincode.data
        app.repayment_method=self.repayment_mode.data

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


class AddApplicationMobile(Form):
    group_leader_cell = TextField( validators=[ v.Length(max=512)]) #8197997788
    group_size = TextField( validators=[ v.Length(max=512)]) #20
    group_leader_number = TextField( validators=[ v.Length(max=512)]) #20
    group_leader_name = TextField( validators=[ v.Length(max=512)]) #20
    center_name = TextField( validators=[ v.Length(max=512)]) #center1
    group_name = TextField( validators=[ v.Length(max=512)]) #group1
    product_name = TextField( validators=[ v.Length(max=512)]) #LP2000026
    name = TextField( validators=[ v.Length(max=512)]) #Swaraj Mahesh Palekar
    pincode = TextField( validators=[ v.Length(max=512)]) #581334
    district = TextField( validators=[ v.Length(max=512)]) #Uttara Kannada
    state = TextField( validators=[ v.Length(max=512)]) #Karnataka
    gender = TextField( validators=[ v.Length(max=512)]) #Male
    country = TextField( validators=[ v.Length(max=512)]) #India
    phone_number = TextField( validators=[ v.Length(max=512)]) #
    age = TextField( validators=[ v.Length(max=512)]) #
    physical_disability_member = TextField( validators=[ v.Length(max=512)]) #None
    relationship_status = TextField( validators=[ v.Length(max=512)]) #Unmarried
    education = TextField( validators=[ v.Length(max=512)]) #Secondary/Matric
    category = TextField( validators=[ v.Length(max=512)]) #General
    religion = TextField( validators=[ v.Length(max=512)]) #Hindu
    taluk = TextField( validators=[ v.Length(max=512)]) #Honavar
    father_s__husband_s_name = TextField( validators=[ v.Length(max=512)]) #S/O Mahesh Palekar
    dob_yob = TextField( validators=[ v.Length(max=512)]) #1991
    male_count = TextField( validators=[ v.Length(max=512)]) #6
    address = TextField( validators=[ v.Length(max=512)]) #Tonka
    female_count = TextField( validators=[ v.Length(max=512)]) #6
    total_earning_members = TextField( validators=[ v.Length(max=512)]) #
    total_number_of_family_members = TextField( validators=[ v.Length(max=512)]) #12
    members_less_than_18 = TextField( validators=[ v.Length(max=512)]) #6
    members_above_18 = TextField( validators=[ v.Length(max=512)]) #6
    other_family_asset_s = TextField( validators=[ v.Length(max=512)]) #Bike, Gas
    gurantors_nominee_name = TextField( validators=[ v.Length(max=512)]) #Habib
    gurantors_nominee_gender = TextField( validators=[ v.Length(max=512)]) #Habib
    gurantors_nominee_age = TextField( validators=[ v.Length(max=512)]) #Habib
    borrowers_nominee_age = TextField( validators=[ v.Length(max=512)]) #Habib
    borrowers_nominee_gender = TextField( validators=[ v.Length(max=512)]) #Habib
    borrowers_nominee_name = TextField( validators=[ v.Length(max=512)]) #Habib
    gurantor_s_relationship_with_borrower = TextField( validators=[ v.Length(max=512)]) #Father
    gurantors_borrowers_are_nominee_for_each_other_ = TextField( validators=[ v.Length(max=512)]) #Yes
    quality_of_house = TextField( validators=[ v.Length(max=512)]) #Kaccha/Mud
    type_of_house = TextField( validators=[ v.Length(max=512)]) #Self Owned
    how_long_are_you_staying_in_house__in_years = TextField( validators=[ v.Length(max=512)]) #25
    source_of_drinking_water = TextField( validators=[ v.Length(max=512)]) #Borewell, Open Well

    purpose_of_the_loan = TextField( validators=[ v.Length(max=512)]) #cattle rearing
    required_loan_amount = TextField( validators=[ v.Length(max=512)]) #25000
    repayment_option = TextField( validators=[ v.Length(max=512)]) #Monthly
    bank_name = TextField( validators=[ v.Length(max=512)]) #
    account_holder_name = TextField( validators=[ v.Length(max=512)]) #')])
    account_number = TextField( validators=[ v.Length(max=512)]) #')])
    ifsc_code = TextField( validators=[ v.Length(max=512)]) #


    interested_in_buying_other_products = TextField( validators=[ v.Length(max=512)]) #None

    financial_liabilities_friends__family_hand_loans = TextField( validators=[ v.Length(max=512)]) #
    financial_liabilities_chits = TextField( validators=[ v.Length(max=512)]) #
    financial_liabilities_insurance = TextField( validators=[ v.Length(max=512)]) #
    financial_liabilities_bank_loans = TextField( validators=[ v.Length(max=512)]) #
    gurranter_s_sex = TextField( validators=[ v.Length(max=512)]) #
    gurranter_s_name = TextField( validators=[ v.Length(max=512)]) #
    gurranter_s_age = TextField( validators=[ v.Length(max=512)]) #
    tertiary_business_category = TextField( validators=[ v.Length(max=512)]) #
    secondary_business_category = TextField( validators=[ v.Length(max=512)]) #Services
    tertiary_business_activities = TextField( validators=[ v.Length(max=512)]) #New something
    secondary_business_activities = TextField( validators=[ v.Length(max=512)]) #New something
    primary_business_activities = TextField( validators=[ v.Length(max=512)]) #something here
    primary_business_income_monthly = TextField( validators=[ v.Length(max=512)]) #8000
    primary_business_category = TextField( validators=[ v.Length(max=512)]) #Services
    secondary_business_expenses_monthly = TextField( validators=[ v.Length(max=512)]) #1000
    secondary_business_income_monthly = TextField( validators=[ v.Length(max=512)]) #3000
    tertiary_business_income_monthly = TextField( validators=[ v.Length(max=512)]) #3000
    tertiary_business_expenses_monthly = TextField( validators=[ v.Length(max=512)]) #3000
    primary_business_expenses_monthly = TextField( validators=[ v.Length(max=512)]) #2000
    village_information_water_bodies = TextField( validators=[ v.Length(max=512)]) #Sea, Pond
    village_information_medical_facility = TextField( validators=[ v.Length(max=512)]) #Public Hospital, None
    village_information_sanitation = TextField( validators=[ v.Length(max=512)]) #Public
    village_information_education_institutes = TextField( validators=[ v.Length(max=512)]) #Government School
    village_information_financial_institutions = TextField( validators=[ v.Length(max=512)]) #Post Office
    village_information_medical_category = TextField( validators=[ v.Length(max=512)]) #Allopathy, None
    village_information_road_quality = TextField( validators=[ v.Length(max=512)]) #Kaccha
    village_information_public_transportaion = TextField( validators=[ v.Length(max=512)]) #Train, Auto
    village_information_electricity_hours = TextField( validators=[ v.Length(max=512)]) #6_15
    family_assets_orchard__acres = TextField( validators=[ v.Length(max=512)]) #1
    family_assets_land_acres = TextField( validators=[ v.Length(max=512)]) #1
    family_education_expenditure_monthly = TextField( validators=[ v.Length(max=512)]) #
    family_assets_number_of_sheeps = TextField( validators=[ v.Length(max=512)]) #10
    family_assets_number_of_cows = TextField( validators=[ v.Length(max=512)]) #20
    family_entertainment_expenditure__monthly = TextField( validators=[ v.Length(max=512)]) #1000
    family_other_expenditure_monthly = TextField( validators=[ v.Length(max=512)]) #1000
    family_festival_expenditure_monthly = TextField( validators=[ v.Length(max=512)]) #1000
    family_travel_expenditure__monthly = TextField( validators=[ v.Length(max=512)]) #1000
    family_medical_expenditure_monthly = TextField( validators=[ v.Length(max=512)]) #
    family_food_expenditure__monthly = TextField( validators=[ v.Length(max=512)]) #2000
    kyc = TextField( validators=[ v.Length(max=2048)]) #2000

    def save( self):
        c_user = current_user
        user = EsthenosUser.objects.get(id=c_user.id)
        app = EsthenosOrgApplication(applicant_name=self.name.data)
        settings = EsthenosSettings.objects.all()[0]
        inc_count = EsthenosOrg.objects.get(id = user.organisation.id).application_count+1
        app.application_id = user.organisation.name.upper()[0:2]+str(settings.organisations_count)+"{0:06d}".format(inc_count)
        user.organisation.update(inc__application_count=1)

        #center = EsthenosOrgCenter.objects.get(center_name=self.center_name.data,organisation=user.organisation)
        group = EsthenosOrgGroup.objects.get(organisation=user.organisation,group_name=self.group_name.data)
        #products = EsthenosOrgProduct.objects.filter(product_name=self.product_name.data)
        products = EsthenosOrgProduct.objects.filter(product_name=self.product_name.data)
        app.organisation = user.organisation
        app.group_leader_cell=self.group_leader_number.data
        app.group_leader_cell=self.group_leader_name.data

        try:
            app.group_size=int(self.group_size.data)
        except Exception as e:
            print e.message

        if len(products) > 0:
            app.product = products[0]
        else:
            app.product = EsthenosOrgProduct.objects.all()[0]

        app.owner = user
        app.group = group

        if self.gurantors_borrowers_are_nominee_for_each_other_.data == "No":
            app.guarantor_borrowers_are_nominee = "NO"
            app.gurantors_nominee_age = self.gurantors_nominee_age.data
            app.gurantors_nominee_gender = self.gurantors_nominee_gender.data
            app.gurantors_nominee_age = self.gurantors_nominee_age.data
        else:
            app.guarantor_borrowers_are_nominee = "YES"

        app.borrowers_nominee_name = self.borrowers_nominee_name.data
        app.gurantor_s_relationship_with_borrower = self.gurantor_s_relationship_with_borrower.data
        app.member_pincode=self.pincode.data
        app.male_count= self.male_count.data
        app.female_count= self.female_count.data

        if self.how_long_are_you_staying_in_house__in_years.data == "":
            app.house_stay_duration = 0.0
        else:
            app.house_stay_duration  = int(self.how_long_are_you_staying_in_house__in_years.data)

        if self.financial_liabilities_chits.data == "":
            app.other_outstanding_chit = 0.0
        else:
            app.other_outstanding_chit = float(self.financial_liabilities_chits.data)

        if self.financial_liabilities_friends__family_hand_loans.data == "":
            app.financial_liabilities_chits = 0.0
        else:
            app.other_outstanding_familynfriends = float(self.financial_liabilities_friends__family_hand_loans.data)

        if self.financial_liabilities_insurance.data == "":
            app.other_outstanding_insurance = 0.0
        else:
            app.other_outstanding_insurance = float(self.financial_liabilities_insurance.data)

        if self.financial_liabilities_bank_loans.data == "":
            app.other_outstanding_emi = 0.0
        else:
            app.other_outstanding_emi = float(self.financial_liabilities_bank_loans.data)

        app.bank_name = self.bank_name.data
        app.bank_ifsc_code = self.ifsc_code.data
        app.bank_account_holder_name = self.account_holder_name.data
        app.bank_account_number = self.account_number.data
        app.member_f_or_h_name = self.father_s__husband_s_name.data
        app.gurranter_s_sex = self.gurranter_s_sex.data
        app.gurranter_s_name = self.gurranter_s_name.data

        if self.gurranter_s_age.data == "":
            self.gurranter_s_age.data = 0.0

        app.gurranter_s_age = float(self.gurranter_s_age.data)
        app.member_disability = self.physical_disability_member.data
        app.village_electricity = self.village_information_electricity_hours.data
        app.village_hospital_category = self.village_information_medical_category.data
        app.village_medical_facilities = self.village_information_medical_facility.data
        app.village_public_transport = self.village_information_public_transportaion.data
        app.village_water= self.village_information_water_bodies.data
        app.village_road = self.village_information_road_quality.data
        app.village_edu_facilities =self.village_information_education_institutes.data
        app.village_financial_institution = self.village_information_financial_institutions.data
        app.village_information_sanitation = self.village_information_sanitation.data

        #app.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=110)
        app.current_status_updated = datetime.datetime.now()
        app.upload_type = "AUTOMATIC_UPLOAD"
        app.status = 0
        app.member_telephone = self.phone_number.data
        app.member_tele_code = "+91"
        app.member_country = self.country.data
        app.member_state = self.state.data
        app.member_city = self.district.data
        app.member_taluk = self.taluk.data
        app.member_village = ""
        app.member_relationship_status = self.relationship_status.data
        app.applied_loan = float(self.required_loan_amount.data)
        app.religion = self.religion.data
        app.category = self.category.data
        app.cast = ""

        app.education = self.education.data
        app.type_of_residence = self.type_of_house.data
        app.quality_of_house = self.quality_of_house.data
        app.drinking_water = self.source_of_drinking_water.data
        app.purpose_of_loan = self.purpose_of_the_loan.data
        if self.total_number_of_family_members == '':
            self.total_number_of_family_members.data  = 0
        app.family_size  = int(self.total_number_of_family_members.data)
        if self.total_earning_members == '':
            app.total_earning_members  = 0
        app.total_earning_members  = int(self.total_earning_members.data)
        if self.members_above_18 == '':
            app.children_above18 = 0
        app.children_above18 = int(self.members_above_18.data)
        if self.members_less_than_18 == '':
            app.children_below18 = 0
        app.children_below18 = int(self.members_less_than_18.data)
        app.family_asset = self.other_family_asset_s.data
#        app.money_lenders_loan = float(self.application_money_lenders_loan.data)
#        app.money_lenders_loan_roi = float(self.application_money_lenders_loan_roi.data)
#        app.bank_loan = float(self.application_bank_loan.data)
#        app.bank_loan_roi = float(self.application_bank_loan_roi.data)
#        app.branch_name = self.application_branch_name.data
#        app.branch_id  = self.applciation_branch_id.data
#        app.state_id = self.application_state_id.data
#        app.region_id = self.application_region_id.data
#        app.cm_id = self.application_cm_id.data
#        app.cm_cell_no = self.application_cm_cell_no.data
#        app.repeat_client_id = self.application_repeat_client_id.data

        app.repayment_method = self.repayment_option.data
        app.applicant_name = self.name.data
        app.dob = self.dob_yob.data
        from esthenos.tasks import calculate_age

        if len(app.dob) == 4:
            app.age = calculate_age(datetime.datetime(year=int(app.dob), month=1, day=1).date())
        elif len(app.dob) >4:
            date_obj = datetime.datetime.strptime(app.dob, "%d/%m/%Y")
            app.age = calculate_age(date_obj)

        app.address = self.address.data
        app.primary_business = self.primary_business_activities.data
        app.secondary_business = self.secondary_business_activities.data
        app.tertiary_business=self.tertiary_business_activities.data

        app.primary_business_category = self.primary_business_category.data
        app.secondary_business_category = self.secondary_business_category.data
        app.tertiary_business_category=self.tertiary_business_category.data

        if self.primary_business_income_monthly.data == "":
            app.primary_income = 0.0
        else:
            app.primary_income =float(self.primary_business_income_monthly.data)
        if self.secondary_business_income_monthly.data == "":
            app.secondary_income = 0.0
        else:
            app.secondary_income = float(self.secondary_business_income_monthly.data)

        if self.tertiary_business_income_monthly.data == "":
            app.tertiary_income =0.0
        else:
            app.tertiary_income =float(self.tertiary_business_income_monthly.data)

        if self.primary_business_expenses_monthly.data == "":
            app.primary_expenses = 0.0
        else:
            app.primary_expenses =float(self.primary_business_expenses_monthly.data)

        if self.secondary_business_expenses_monthly.data == "":
            app.secondary_expenses = 0.0
        else:
            app.secondary_expenses = float(self.secondary_business_expenses_monthly.data)

        if self.tertiary_business_expenses_monthly.data == "":
            app.tertiary_expenses =0.0
        else:
            app.tertiary_expenses =float(self.tertiary_business_expenses_monthly.data)

        app.gender = self.gender.data
        app.other_income = 0
        app.total_income = app.primary_income+app.secondary_income+app.tertiary_income+app.other_income
#       app.business_expense =
        if self.family_food_expenditure__monthly.data == "":
            app.food_expense = 0.0
        else:
            app.food_expense = float(self.family_food_expenditure__monthly.data)
        if self.family_travel_expenditure__monthly.data == "":
            app.travel_expense = 0.0
        else:
            app.travel_expense =float(self.family_travel_expenditure__monthly.data)
        if self.family_entertainment_expenditure__monthly.data == "":
            app.entertainment_expense = 0.0
        else:
            app.entertainment_expense =float(self.family_entertainment_expenditure__monthly.data)
        if self.family_education_expenditure_monthly.data == "":
            app.educational_expense = 0.0
        else:
            app.educational_expense = float(self.family_education_expenditure_monthly.data)
        if self.family_medical_expenditure_monthly.data == "":
            app.medical_expense = 0.0
        else:
            app.medical_expense =float(self.family_medical_expenditure_monthly.data)
        if self.family_other_expenditure_monthly.data == "":
            app.other_expense = 0.0
        else:
            app.other_expense = float(self.family_other_expenditure_monthly.data)
        app.total_expenditure = app.food_expense+app.travel_expense+app.entertainment_expense+app.educational_expense+app.medical_expense+app.other_expense+app.tertiary_expenses+app.secondary_expenses+app.primary_expenses
#       app.total_liability =
#       app.outstanding_1 =
#       app.outstanding_2 =
#       app.outstanding_3 =
#       app.outstanding_4 =
#       app.total_outstanding =
        app.num_cows = self.family_assets_number_of_cows.data
        app.num_sheeps = self.family_assets_number_of_sheeps.data
        if self.financial_liabilities_chits.data == "":
            app.other_outstanding_chit = 0.0
        else:
            app.other_outstanding_chit = float(self.financial_liabilities_chits.data)
        if self.financial_liabilities_insurance.data == "":
            app.other_outstanding_insurance = 0.0
        else:
            app.other_outstanding_insurance = float(self.financial_liabilities_insurance.data.strip())
#       app.other_outstanding_emi =
        app.total_other_outstanding = app.other_outstanding_chit + app.other_outstanding_insurance + app.other_outstanding_emi
        app.net_income = app.total_income - app.total_expenditure - app.total_other_outstanding
        app.loan_eligibility_based_on_net_income = app.net_income * app.product.number_installments
        status = EsthenosOrgApplicationStatus(status = app.current_status,updated_on=app.current_status_updated)
        status.save()
        app.timeline.append(status)
        data_kyc=  self.kyc.data.replace("'", '"').replace('u"', '"')

        kyc_json = json.loads(data_kyc)
        if kyc_json.has_key("aadhaar"):
            kyc_obj = EsthenosOrgApplicationKYC()
            kyc_obj.kyc_type = "AADHAAR"

            try:
                kyc_obj.image_id_f = kyc_json["aadhaar"]["aadhar_f"]
                kyc_obj.image_id_b = kyc_json["aadhaar"]["aadhar_b"]
            except:
                print "no aadhaar images"

            kyc_obj.kyc_number = kyc_json["aadhaar"]["uid"]
            kyc_obj.dob = kyc_json["aadhaar"]["yob"]
            kyc_obj.name = kyc_json["aadhaar"]["name"]
            kyc_obj.gender = kyc_json["aadhaar"]["gender"]

            if kyc_json["aadhaar"].has_key("house"):
                kyc_obj.address1 = kyc_json["aadhaar"]["house"]

            if kyc_json["aadhaar"].has_key("lm"):
                kyc_obj.address1 = kyc_json["aadhaar"]["lm"]

            kyc_obj.state = kyc_json["aadhaar"]["state"]
            kyc_obj.dist = kyc_json["aadhaar"]["dist"]

            if kyc_json["aadhaar"].has_key("vtc"):
                kyc_obj.taluk = kyc_json["aadhaar"]["vtc"]

            kyc_obj.pincode = kyc_json["aadhaar"]["pc"]
            app.kyc_1 = kyc_obj


        kyc_obj = EsthenosOrgApplicationKYC()
        if kyc_json.has_key("pan") :
            kyc_obj.kyc_type = "PAN"
            kyc_obj.image_id_f = kyc_json["pan"]["pancard_f"]

        elif kyc_json.has_key("voters"):
            kyc_obj.kyc_type = "VOTERS"
            kyc_obj.image_id_f = kyc_json["voters"]["votercard_f"]
            kyc_obj.image_id_b = kyc_json["voters"]["votercard_b"]
        app.kyc_2 = kyc_obj

        if kyc_json.has_key("gurrantor") and kyc_json["gurrantor"].has_key("gurrantors_f")and kyc_json["gurrantor"].has_key("gurrantors_b"):
            kyc_obj = EsthenosOrgApplicationKYC()
            kyc_obj.type ="UNKNOWN"
            kyc_obj.image_id_f = kyc_json["gurrantor"]["gurrantors_f"]
            kyc_obj.image_id_b = kyc_json["gurrantor"]["gurrantors_b"]
            app.gkyc_1 = kyc_obj

        if kyc_json.has_key("other"):
            kyc_obj = EsthenosOrgApplicationKYC()
            kyc_obj.type ="OTHER"
            kyc_obj.image_id_f = kyc_json["other"]["other"]
            app.other_documents.append(kyc_obj)

        if kyc_json.has_key("bank"):
            kyc_obj = EsthenosOrgApplicationKYC()
            kyc_obj.type ="BANK_STATEMENT"
            kyc_obj.image_id_f = kyc_json["bank"]["bank_account_statement"]
            app.other_documents.append(kyc_obj)

        if kyc_json.has_key("ration"):
            kyc_obj = EsthenosOrgApplicationKYC()
            kyc_obj.type ="RATION"
            kyc_obj.image_id_f = kyc_json["ration"]["ration_f"]
            kyc_obj.image_id_b = kyc_json["ration"]["ration_b"]
            app.other_documents.append(kyc_obj)

        #app.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=120)
        app.current_status_updated = datetime.datetime.now()
        app.status = 120
        app.save()

        return None
