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

    assets_id = TextField(validators=[v.Length(max=512)])
    applicant_other_info = TextField(validators=[v.Length(max=4096)])
    applicant_aadhar_card = TextField(validators=[v.Length(max=2048)])
    guarantor1_aadhar_card = TextField(validators=[v.Length(max=2048)])
    guarantor2_aadhar_card = TextField(validators=[v.Length(max=2048)])

    def save(self):
        user = EsthenosUser.objects.get(id=current_user.id)
        user.organisation.update(inc__application_count=1)
        settings = EsthenosSettings.objects.all()[0]
        inc_count = EsthenosOrg.objects.get(id = user.organisation.id).application_count + 1

        applicant_misc = json.loads(self.applicant_other_info.data.replace("'", '"').replace('u"', '"'))
        applicant = json.loads(self.applicant_aadhar_card.data.replace("'", '"').replace('u"', '"'))
        guarantor1 = json.loads(self.guarantor1_aadhar_card.data.replace("'", '"').replace('u"', '"'))
        guarantor2 = json.loads(self.guarantor2_aadhar_card.data.replace("'", '"').replace('u"', '"'))

        app = EsthenosOrgApplication(
            name = applicant["name"],
            owner = user,
            appId = self.assets_id,
            organisation = user.organisation,
            application_id = user.organisation.name.upper()[0:2] + str(settings.organisations_count) + "{0:06d}".format(inc_count)
        )

        app.age = toInt(applicant["age"])
        app.dob = applicant["dob_yob"]
        app.yob = applicant["dob_yob"]
        app.city = applicant["district"]
        app.taluk = applicant["taluk"]
        app.state = applicant["state"]
        app.district = applicant["district"]
        app.address = applicant["address"]
        app.country = applicant["country"]
        app.pincode = applicant["pincode"]
        app.mobile = applicant["mobile_number"]
        app.tele_code = "+91"
        app.tele_phone = applicant["phone_number"]
        app.applicant_name = applicant["name"]
        app.father_or_husband_name = applicant["father_s_husband_s_name"]

        # app.caste = applicant_misc["caste"]
        app.gender = applicant_misc["gender"]
        app.religion = applicant_misc["religion"]
        app.category = applicant_misc["category"]
        app.education = applicant_misc["education"]
        app.disability = applicant_misc["physical_disability_member"]

        app.male_count = toInt(applicant_misc["male_count"])
        app.female_count = toInt(applicant_misc["female_count"])
        app.members_above18 = toInt(applicant_misc["members_above_18"])
        app.members_less_than_18 = toInt(applicant_misc["members_less_than_18"])
        app.total_earning_members = toInt(applicant_misc["total_earning_members"])
        app.total_number_of_family_members = toInt(applicant_misc["total_number_of_family_members"])

        app.nominee_age = applicant_misc["nominee_age"]
        app.nominee_name = applicant_misc["nominee_name"]
        app.nominee_phone = applicant_misc["nominee_phone"]
        app.nominee_gender = applicant_misc["nominee_gender"]
        app.nominee_relationship_with_borrower = applicant_misc["nominee_relationship_with_borrower"]

        app.type_of_house = applicant_misc["type_of_house"]
        app.quality_of_house = applicant_misc["quality_of_house"]
        app.house_stay_duration = toFloat(applicant_misc["how_long_are_you_staying_in_house__in_years"])

        app.applied_loan = toFloat(applicant_misc["required_loan_amount"])
        app.purpose_of_loan = applicant_misc["purpose_of_the_loan"]

        app.family_assets_land_acres = toFloat(applicant_misc["family_assets_land_acres"])
        app.family_assets_orchard_acres = toFloat(applicant_misc["family_assets_orchard__acres"])
        app.family_assets_number_of_rented_houses_or_flats = toFloat(applicant_misc["family_assets_number_of_rented_houses_or_flats"])
        app.family_assets_number_of_rented_shops_or_godowns = toFloat(applicant_misc["family_assets_number_of_rented_shops_or_godowns"])

        app.bank_name = applicant_misc["bank_name"]
        app.bank_ifsc_code = applicant_misc["ifsc_code"]
        app.bank_account_number = applicant_misc["account_number"]
        app.bank_account_holder_name = applicant_misc["account_holder_name"]
        app.repayment_method = applicant_misc["repayment_option"]

        app.primary_business_premise = applicant_misc["primary_business___premise"]
        app.primary_business_category = applicant_misc["primary_business_category"]
        app.primary_business_activities = applicant_misc["primary_business_activities"]
        app.primary_business_seasonality = applicant_misc["primary_business_seasonality"]
        app.primary_business_income_monthly = toFloat(applicant_misc["primary_business_income_monthly"])
        app.primary_business_number_of_employees = toFloat(applicant_misc["primary_business___number_of_employees"])
        app.primary_business_expense_rent = toFloat(applicant_misc["primary_business_expenditure___rent"])
        app.primary_business_expense_admin = toFloat(applicant_misc["primary_business_expenditure___admin"])
        app.primary_business_expense_other = toFloat(applicant_misc["primary_business_expenditure___other_expenses"])
        app.primary_business_expense_working_capital = toFloat(applicant_misc["primary_business_expenditure___working_capital"])
        app.primary_business_expense_employee_salary = toFloat(applicant_misc["primary_business_expenditure___employee_salary"])
        app.primary_business_number_of_years_in_business = toFloat(applicant_misc["primary_business___number_of_years_in_business"])

        app.secondary_business = applicant_misc.get("secondary_business_activities", "")
        app.secondary_business_category = applicant_misc.get("secondary_business_category", "")
        app.secondary_business_income_monthly = toFloat(applicant_misc.get("secondary_business_income_monthly", ""))
        app.secondary_business_expenses_monthly = toFloat(applicant_misc.get("secondary_business_expenses_monthly", ""))

        app.tertiary_business = applicant_misc.get("tertiary_business_activities", "")
        app.tertiary_business_category = applicant_misc.get("tertiary_business_category", "")
        app.tertiary_business_income_monthly = toFloat(applicant_misc.get("tertiary_business_income_monthly", ""))
        app.tertiary_business_expenses_monthly = toFloat(applicant_misc.get("tertiary_business_expenses_monthly", ""))

        app.food_expense = toFloat(applicant_misc["family_food_expenditure__monthly"])
        app.other_expense = toFloat(applicant_misc["family_other_expenditure_monthly"])
        app.travel_expense = toFloat(applicant_misc["family_travel_expenditure__monthly"])
        app.medical_expense = toFloat(applicant_misc["family_medical_expenditure_monthly"])
        app.festival_expense = toFloat(applicant_misc["family_festival_expenditure_monthly"])
        app.educational_expense = toFloat(applicant_misc["family_education_expenditure_monthly"])
        app.entertainment_expense = toFloat(applicant_misc["family_entertainment_expenditure__monthly"])

        app.other_outstanding_emi = toFloat(applicant_misc["financial_liabilities_bank_loans"])
        app.other_outstanding_chit = toFloat(applicant_misc["financial_liabilities_chits"])
        app.other_outstanding_insurance = toFloat(applicant_misc["financial_liabilities_insurance"])
        app.other_outstanding_familynfriends = toFloat(applicant_misc["financial_liabilities_friends__family_hand_loans"])

        app.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=110)
        app.current_status_updated = datetime.datetime.now()

        status = EsthenosOrgApplicationStatus(status=app.current_status, updated_on=app.current_status_updated)
        status.save()

        app.applicant_kyc = EsthenosOrgApplicationKYC(
            kyc_type = applicant["type"],
            kyc_number = applicant["uid"],
            age = applicant["age"],
            dob = applicant["dob_yob"],
            name = applicant["name"],
            taluk = applicant["taluk"],
            state = applicant["state"],
            gender = applicant_misc["gender"],
            pincode = applicant["pincode"],
            address = applicant["address"],
            country = applicant["country"],
            district = applicant["district"],
            phone_number = applicant["phone_number"],
            mobile_number = applicant["mobile_number"],
            father_or_husband_name = applicant["father_s_husband_s_name"],
        )

        app.guarantor1_kyc = EsthenosOrgApplicationKYC(
            kyc_type = applicant["type"],
            kyc_number = applicant["uid"],
            age = guarantor1["age"],
            dob = guarantor1["dob_yob"],
            name = guarantor1["name"],
            taluk = guarantor1["taluk"],
            state = guarantor1["state"],
            pincode = guarantor1["pincode"],
            address = guarantor1["address"],
            country = guarantor1["country"],
            district = guarantor1["district"],
            phone_number = guarantor1["phone_number"],
            mobile_number = guarantor1["mobile_number"],
            father_or_husband_name = guarantor1["father_s_husband_s_name"],
        )

        app.guarantor2_kyc = EsthenosOrgApplicationKYC(
            kyc_type = applicant["type"],
            kyc_number = guarantor2["uid"],
            age = guarantor2["age"],
            dob = guarantor2["dob_yob"],
            name = guarantor2["name"],
            taluk = guarantor2["taluk"],
            state = guarantor2["state"],
            pincode = guarantor2["pincode"],
            address = guarantor2["address"],
            country = guarantor2["country"],
            district = guarantor2["district"],
            phone_number = guarantor2["phone_number"],
            mobile_number = guarantor2["mobile_number"],
            father_or_husband_name = guarantor2["father_s_husband_s_name"],
        )

        app.timeline.append(status)

        app.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=120)
        app.current_status_updated = datetime.datetime.now()
        app.status = 120
        app.save()

        return None
