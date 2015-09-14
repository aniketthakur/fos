import json
import datetime
from wtforms import Form, TextField, PasswordField, HiddenField, ValidationError, DateField
from wtforms import validators as v
from flask_login import current_user

from e_admin.models import EsthenosUser, EsthenosSettings
from e_organisation.models import *

def toInt(value):
  try:
    return int(value)
  except:
    return 0

def toFloat(value):
  try:
    return float(value)
  except:
    return 0.0


class AddApplicationMobile(Form):
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
    address = TextField( validators=[ v.Length(max=512)]) #Tonka

    total_earning_members = TextField( validators=[ v.Length(max=512)]) #
    total_number_of_family_members = TextField( validators=[ v.Length(max=512)]) #12

    male_count = TextField( validators=[ v.Length(max=512)]) #6
    female_count = TextField( validators=[ v.Length(max=512)]) #6

    members_above_18 = TextField( validators=[ v.Length(max=512)]) #6
    members_less_than_18 = TextField( validators=[ v.Length(max=512)]) #6

    other_family_asset_s = TextField( validators=[ v.Length(max=512)]) #Bike, Gas

    gurranter_s_sex = TextField( validators=[ v.Length(max=512)]) #
    gurranter_s_age = TextField( validators=[ v.Length(max=512)]) #
    gurranter_s_name = TextField( validators=[ v.Length(max=512)]) #

    gurantors_nominee_age = TextField( validators=[ v.Length(max=512)]) #Habib
    gurantors_nominee_name = TextField( validators=[ v.Length(max=512)]) #Habib
    gurantors_nominee_gender = TextField( validators=[ v.Length(max=512)]) #Habib

    borrowers_nominee_age = TextField( validators=[ v.Length(max=512)]) #Habib
    borrowers_nominee_gender = TextField( validators=[ v.Length(max=512)]) #Habib
    borrowers_nominee_name = TextField( validators=[ v.Length(max=512)]) #Habib

    gurantors_borrowers_are_nominee_for_each_other_ = TextField( validators=[ v.Length(max=512)]) #Yes
    gurantor_s_relationship_with_borrower = TextField( validators=[ v.Length(max=512)]) #Father

    type_of_house = TextField( validators=[ v.Length(max=512)]) #Self Owned
    quality_of_house = TextField( validators=[ v.Length(max=512)]) #Kaccha/Mud
    source_of_drinking_water = TextField( validators=[ v.Length(max=512)]) #Borewell, Open Well
    how_long_are_you_staying_in_house__in_years = TextField( validators=[ v.Length(max=512)]) #25

    repayment_option = TextField( validators=[ v.Length(max=512)]) #Monthly
    purpose_of_the_loan = TextField( validators=[ v.Length(max=512)]) #cattle rearing
    required_loan_amount = TextField( validators=[ v.Length(max=512)]) #25000

    bank_name = TextField( validators=[ v.Length(max=512)]) #
    ifsc_code = TextField( validators=[ v.Length(max=512)]) #
    account_number = TextField( validators=[ v.Length(max=512)]) #')])
    account_holder_name = TextField( validators=[ v.Length(max=512)]) #')])

    interested_in_buying_other_products = TextField( validators=[ v.Length(max=512)]) #None

    financial_liabilities_friends__family_hand_loans = TextField( validators=[ v.Length(max=512)]) #
    financial_liabilities_chits = TextField( validators=[ v.Length(max=512)]) #
    financial_liabilities_insurance = TextField( validators=[ v.Length(max=512)]) #
    financial_liabilities_bank_loans = TextField( validators=[ v.Length(max=512)]) #

    secondary_business_category = TextField( validators=[ v.Length(max=512)]) #Services
    secondary_business_activities = TextField( validators=[ v.Length(max=512)]) #New something
    secondary_business_income_monthly = TextField( validators=[ v.Length(max=512)]) #3000
    secondary_business_expenses_monthly = TextField( validators=[ v.Length(max=512)]) #1000

    primary_business_category = TextField( validators=[ v.Length(max=512)]) #Services
    primary_business_activities = TextField( validators=[ v.Length(max=512)]) #something here
    primary_business_income_monthly = TextField( validators=[ v.Length(max=512)]) #8000
    primary_business_expenses_monthly = TextField( validators=[ v.Length(max=512)]) #2000

    tertiary_business_category = TextField( validators=[ v.Length(max=512)]) #
    tertiary_business_activities = TextField( validators=[ v.Length(max=512)]) #New something
    tertiary_business_income_monthly = TextField( validators=[ v.Length(max=512)]) #3000
    tertiary_business_expenses_monthly = TextField( validators=[ v.Length(max=512)]) #3000

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
    family_assets_number_of_sheeps = TextField( validators=[ v.Length(max=512)]) #10
    family_assets_number_of_cows = TextField( validators=[ v.Length(max=512)]) #20

    family_food_expenditure__monthly = TextField( validators=[ v.Length(max=512)]) #2000
    family_other_expenditure_monthly = TextField( validators=[ v.Length(max=512)]) #1000
    family_travel_expenditure__monthly = TextField( validators=[ v.Length(max=512)]) #1000
    family_medical_expenditure_monthly = TextField( validators=[ v.Length(max=512)]) #
    family_festival_expenditure_monthly = TextField( validators=[ v.Length(max=512)]) #1000
    family_education_expenditure_monthly = TextField( validators=[ v.Length(max=512)]) #
    family_entertainment_expenditure__monthly = TextField( validators=[ v.Length(max=512)]) #1000

    kyc = TextField( validators=[ v.Length(max=2048)]) #2000

    def save( self):
        user = EsthenosUser.objects.get(id=current_user.id)
        app = EsthenosOrgApplication(applicant_name=self.name.data)
        settings = EsthenosSettings.objects.all()[0]
        inc_count = EsthenosOrg.objects.get(id = user.organisation.id).application_count+1
        app.owner = user
        app.organisation = user.organisation
        app.application_id = user.organisation.name.upper()[0:2]+str(settings.organisations_count)+"{0:06d}".format(inc_count)
        user.organisation.update(inc__application_count=1)

        if self.gurantors_borrowers_are_nominee_for_each_other_.data == "No":
            app.guarantor_borrowers_are_nominee = "NO"
            app.gurantors_nominee_name = self.gurantors_nominee_name.data
            app.gurantors_nominee_gender = self.gurantors_nominee_gender.data
            app.gurantors_nominee_age = self.gurantors_nominee_age.data
            app.borrowers_nominee_age = self.borrowers_nominee_age.data
            app.borrowers_nominee_gender = self.borrowers_nominee_gender.data
            app.borrowers_nominee_name = self.borrowers_nominee_name.data
            app.gurantor_s_relationship_with_borrower = self.gurantor_s_relationship_with_borrower.data
        else:
            app.guarantor_borrowers_are_nominee = "YES"

        app.borrowers_nominee_name = self.borrowers_nominee_name.data
        app.gurantor_s_relationship_with_borrower = self.gurantor_s_relationship_with_borrower.data

        app.member_pincode = self.pincode.data
        app.male_count = toInt(self.male_count.data)
        app.female_count = toInt(self.female_count.data)
        app.house_stay_duration = toFloat(self.how_long_are_you_staying_in_house__in_years.data)

        app.bank_name = self.bank_name.data
        app.bank_ifsc_code = self.ifsc_code.data
        app.bank_account_number = self.account_number.data
        app.bank_account_holder_name = self.account_holder_name.data

        app.member_disability = self.physical_disability_member.data
        app.member_f_or_h_name = self.father_s__husband_s_name.data

        app.gurranter_s_age = toFloat(self.gurranter_s_age.data)
        app.gurranter_s_sex = self.gurranter_s_sex.data
        app.gurranter_s_name = self.gurranter_s_name.data

        app.village_electricity = self.village_information_electricity_hours.data
        app.village_hospital_category = self.village_information_medical_category.data
        app.village_medical_facilities = self.village_information_medical_facility.data
        app.village_public_transport = self.village_information_public_transportaion.data
        app.village_road = self.village_information_road_quality.data
        app.village_water = self.village_information_water_bodies.data
        app.village_edu_facilities = self.village_information_education_institutes.data
        app.village_financial_institution = self.village_information_financial_institutions.data
        app.village_information_sanitation = self.village_information_sanitation.data

        app.status = 0
        app.upload_type = "AUTOMATIC_UPLOAD"

        app.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=110)
        app.current_status_updated = datetime.datetime.now()

        app.member_telephone = self.phone_number.data
        app.member_tele_code = "+91"
        app.member_country = self.country.data
        app.member_state = self.state.data
        app.member_city = self.district.data
        app.member_taluk = self.taluk.data
        app.member_village = ""
        app.member_relationship_status = self.relationship_status.data

        app.cast = ""
        app.religion = self.religion.data
        app.category = self.category.data
        app.applied_loan = toFloat(self.required_loan_amount.data)

        app.education = self.education.data
        app.type_of_residence = self.type_of_house.data
        app.quality_of_house = self.quality_of_house.data
        app.drinking_water = self.source_of_drinking_water.data
        app.purpose_of_loan = self.purpose_of_the_loan.data
        app.family_size = toInt(self.total_number_of_family_members.data)
        app.total_earning_members = toInt(self.total_earning_members.data)
        app.children_above18 = toInt(self.members_above_18.data)
        app.children_below18 = toInt(self.members_less_than_18.data)
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
        app.gender = self.gender.data
        app.num_cows = toInt(self.family_assets_number_of_cows.data)
        app.num_sheeps = toInt(self.family_assets_number_of_sheeps.data)

        app.address = self.address.data
        app.primary_business = self.primary_business_activities.data
        app.secondary_business = self.secondary_business_activities.data
        app.tertiary_business=self.tertiary_business_activities.data

        app.primary_business_category = self.primary_business_category.data
        app.secondary_business_category = self.secondary_business_category.data
        app.tertiary_business_category=self.tertiary_business_category.data

        app.primary_income = toFloat(self.primary_business_income_monthly.data)
        app.secondary_income = toFloat(self.secondary_business_income_monthly.data)
        app.tertiary_income = toFloat(self.tertiary_business_income_monthly.data)
        app.other_income = 0
        app.total_income = app.primary_income\
                           + app.secondary_income\
                           + app.tertiary_income \
                           + app.other_income

        app.primary_expenses = toFloat(self.primary_business_expenses_monthly.data)
        app.secondary_expenses = toFloat(self.secondary_business_expenses_monthly.data)
        app.tertiary_expenses = toFloat(self.tertiary_business_expenses_monthly.data)
        app.food_expense = toFloat(self.family_food_expenditure__monthly.data)
        app.other_expense = toFloat(self.family_other_expenditure_monthly.data)
        app.travel_expense = toFloat(self.family_travel_expenditure__monthly.data)
        app.medical_expense = toFloat(self.family_medical_expenditure_monthly.data)
        app.educational_expense = toFloat(self.family_education_expenditure_monthly.data)
        app.entertainment_expense = toFloat(self.family_entertainment_expenditure__monthly.data)
        app.business_expense = app.primary_expenses\
                               + app.secondary_expenses \
                               + app.tertiary_expenses
        app.total_expenditure = app.food_expense\
                                + app.travel_expense\
                                + app.entertainment_expense \
                                + app.educational_expense \
                                + app.medical_expense \
                                + app.other_expense \
                                + app.primary_expenses \
                                + app.secondary_expenses \
                                + app.tertiary_expenses

        app.other_outstanding_emi = toFloat(self.financial_liabilities_bank_loans.data)
        app.other_outstanding_chit = toFloat(self.financial_liabilities_chits.data)
        app.other_outstanding_insurance = toFloat(self.financial_liabilities_insurance.data)
        app.other_outstanding_familynfriends = toFloat(self.financial_liabilities_friends__family_hand_loans.data)
        app.total_other_outstanding = + app.other_outstanding_emi \
                                      + app.other_outstanding_chit \
                                      + app.other_outstanding_insurance \
                                      + app.other_outstanding_familynfriends

        app.net_income = app.total_income - app.total_expenditure - app.total_other_outstanding
        status = EsthenosOrgApplicationStatus(status=app.current_status, updated_on=app.current_status_updated)
        status.save()

        app.timeline.append(status)
        data_kyc = self.kyc.data.replace("'", '"').replace('u"', '"')

        kyc_json = json.loads(data_kyc)
        if kyc_json.has_key("aadhaar"):
            kyc_obj = EsthenosOrgApplicationKYC()
            kyc_obj.kyc_type = "AADHAAR"

            if "aadhar_f" in kyc_json["aadhaar"]:
                kyc_obj.image_id_f = kyc_json["aadhaar"]["aadhar_f"]

            if "aadhar_b" in kyc_json["aadhaar"]:
                kyc_obj.image_id_b = kyc_json["aadhaar"]["aadhar_b"]

            if "uid" in kyc_json["aadhaar"]:
                kyc_obj.kyc_number = kyc_json["aadhaar"]["uid"]

            if "yob" in kyc_json["aadhaar"]:
                kyc_obj.dob = kyc_json["aadhaar"]["yob"]

            if "name" in kyc_json["aadhaar"]:
                kyc_obj.name = kyc_json["aadhaar"]["name"]

            if "gender" in kyc_json["aadhaar"]:
                kyc_obj.gender = kyc_json["aadhaar"]["gender"]

            if kyc_json["aadhaar"].has_key("house"):
                kyc_obj.address1 = kyc_json["aadhaar"]["house"]

            if kyc_json["aadhaar"].has_key("lm"):
                kyc_obj.address1 = kyc_json["aadhaar"]["lm"]

            if "state" in kyc_json["aadhaar"]:
                kyc_obj.state = kyc_json["aadhaar"]["state"]

            if "dist" in kyc_json["aadhaar"]:
                kyc_obj.dist = kyc_json["aadhaar"]["dist"]

            if kyc_json["aadhaar"].has_key("vtc"):
                kyc_obj.taluk = kyc_json["aadhaar"]["vtc"]

            if "pc" in kyc_json["aadhaar"]:
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

        app.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=120)
        app.current_status_updated = datetime.datetime.now()
        app.status = 120
        app.save()

        return None
