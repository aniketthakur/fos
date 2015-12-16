import json
import datetime
from wtforms import Form, TextField, PasswordField, HiddenField, ValidationError, DateField
from wtforms import validators as v
from flask_login import current_user

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
    # group = TextField(validators=[v.Length(max=10000)])
    # center = TextField(validators=[v.Length(max=10000)])
    # product = TextField(validators=[v.Length(max=10000)])

    assets_id = TextField(validators=[v.Length(max=10000)])
    assets_map = TextField(validators=[v.Length(max=10000)])
    locations_map = TextField(validators=[v.Length(max=10000)])

    guarantor1_kyc_details = TextField(validators=[v.Length(max=10000)])
    # guarantor1_other_card_details1 = TextField(validators=[v.Length(max=10000)])

    guarantor2_kyc_details = TextField(validators=[v.Length(max=10000)])
    # guarantor1_other_card_details2 = TextField(validators=[v.Length(max=10000)])

    applicant_kyc_details = TextField(validators=[v.Length(max=10000)])
    # applicant_other_card_id_details = TextField(validators=[v.Length(max=10000)])
    applicant_loan_details_applied_loan = TextField(validators=[v.Length(max=10000)])

    applicant_personal_docs = TextField(validators=[v.Length(max=10000)])
    applicant_nominee_details = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_liabilities = TextField(validators=[v.Length(max=10000)])
    # applicant_other_card_land_details = TextField(validators=[v.Length(max=10000)])
    # applicant_other_card_phone_details = TextField(validators=[v.Length(max=10000)])
    # applicant_other_card_electricity_details = TextField(validators=[v.Length(max=10000)])
    # applicant_other_card_credit_card_details = TextField(validators=[v.Length(max=10000)])

    applicant_hypothecation_goods_details1 = TextField(validators=[v.Length(max=10000)])
    applicant_hypothecation_goods_details2 = TextField(validators=[v.Length(max=10000)])
    applicant_hypothecation_goods_details3 = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_bank_details1 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_bank_details2 = TextField(validators=[v.Length(max=10000)])

    applicant_family_expenditure = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_members = TextField(validators=[v.Length(max=10000)])

    applicant_family_details_assets = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_other_assets = TextField(validators=[v.Length(max=10000)])

    applicant_family_details_details1 = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_details2 = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_details3 = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_details4 = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_details5 = TextField(validators=[v.Length(max=10000)])
    
    applicant_loan_details_details1 = TextField(validators=[v.Length(max=10000)])
    applicant_loan_details_details2 = TextField(validators=[v.Length(max=10000)])
    applicant_loan_details_details3 = TextField(validators=[v.Length(max=10000)])
    applicant_loan_details_details4 = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_land_details1 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_land_details2 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_land_details3 = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_type_equipment1 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_type_equipment2 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_type_equipment3 = TextField(validators=[v.Length(max=10000)])

    # applicant_business_docs_info = TextField(validators=[v.Length(max=10000)])
    applicant_business_docs_details1 = TextField(validators=[v.Length(max=10000)])
    applicant_business_docs_details2 = TextField(validators=[v.Length(max=10000)])
    applicant_business_docs_details3 = TextField(validators=[v.Length(max=10000)])
    applicant_business_docs_details4 = TextField(validators=[v.Length(max=10000)])

    applicant_personal_docs_vehicle1 = TextField(validators=[v.Length(max=10000)])
    applicant_personal_docs_vehicle2 = TextField(validators=[v.Length(max=10000)])
    applicant_personal_docs_vehicle3 = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_sales_info = TextField(validators=[v.Length(max=10000)])

    def load(self, form):
        if (form.data is None) or (form.data == ""):
            return {}

        form = form.data\
                .replace("'", '"')\
                .replace('u"', '"')\
                .replace("\/", '/')\
                .replace(": None", ': "None"')
        return json.loads(form)
    
    def load_family_details(self, data):
        return EsthenosOrgApplicationFamilyDetails(
            age = toInt(data.get("age", "")),
            name = data.get("name", ""),
            relation = data.get("relation", ""),
            education = data.get("education", ""),
            aadhar_number = data.get("aadhar_number", ""),
            annual_income = toFloat(data.get("annual_income", "")),
            occupations_details = data.get("occupations_details", ""),
        )
    
    def load_land_details(self, data):
        return EsthenosOrgApplicationLandDetails(
            area_in_sqft = toFloat(data.get("area_in_sqft", "")),
            land_location = data.get("land_location", ""),
            type_of_property = data.get("type_of_property", ""),
            loan_outstanding = toFloat(data.get("loan_outstanding", "")),
            estimated_resale_value = toFloat(data.get("estimated_resale_value", ""))
        )
    
    def load_loan_details(self, data):
        return EsthenosOrgApplicationLoanDetails(
            interest= toFloat(data.get("interest", "")),
            type_of_loan = data.get("type_of_loan", ""),
            name_of_bank = data.get("name_of_bank", ""),
            loan_detail = data.get("loan_detail", ""),
            emi_repayments = toFloat(data.get("emi_repayments", "")),
            loan_amount_key = toFloat(data.get("loan_amount_key", "")),
            tenure_in_months = toFloat(data.get("tenure_in_months", "")),
            collateral_details = data.get("collateral_details", ""),
            outstanding_loan_amount = toFloat(data.get("outstanding_loan_amount", ""))
        )

    def load_type_equipment(self, data):
        return EsthenosOrgApplicationTypeEquipment(
            estimated_value = toFloat(data.get("estimated_value","")),
            details_of_equipment_supplier = data.get("details_of_equipment_supplier",""),
            date_of_manufacturing_equipment = data.get("date_of_manufacturing_equipment",""),
            is_equipment_given_as_collateral = data.get("is_equipment_given_as_collateral__dropdown_with_values","")
        )

    def load_docs_vehicle(self, data):
        return EsthenosOrgApplicationDocsVehicle(
            year_of_registration = toInt(data.get("year_of_registration","")),
            estimated_resale_value = toFloat(data.get("estimated_resale_value","")),
            type_of_vehicle_manufacturer = data.get("type_of_vehicle_manufacturer","")
        )

    def save(self):
        user = EsthenosUser.objects.get(id=current_user.id)
        user.organisation.update(inc__application_count=1)
        settings = EsthenosSettings.objects.all()[0]

        applicant_kyc = self.load(self.applicant_kyc_details)
        app = EsthenosOrgApplication(
            name = applicant_kyc["name"],
            owner = user,
            assets_id = str(self.assets_id.data),
            organisation = user.organisation
        )

        app.dob = applicant_kyc["dob_yob"]
        app.yob = applicant_kyc["dob_yob"]
        app.city = applicant_kyc["district"]
        app.taluk = applicant_kyc["taluk"]
        app.state = applicant_kyc["state"]
        app.district = applicant_kyc["district"]
        app.address = applicant_kyc["address"]
        app.country = applicant_kyc["country"]
        app.pincode = applicant_kyc["pincode"]
        app.mobile = applicant_kyc["mobile_number"]
        app.tele_code = "+91"
        app.tele_phone = applicant_kyc["phone_number"]
        app.applicant_name = applicant_kyc["name"]
        app.father_or_husband_name = applicant_kyc["father_s_husband_s_name"]

        applicant_personal = self.load(self.applicant_personal_docs)
        app.caste = applicant_personal.get("caste", "")
        app.gender = applicant_personal.get("gender", "")
        app.religion = applicant_personal.get("religion", "")
        app.category = applicant_personal.get("category", "") + applicant_personal.get("specify_category", "")
        app.education = applicant_personal.get("education", "")
        app.disability = applicant_personal.get("physical_disability", "")
        app.marital_status = applicant_personal.get("marital_status", "")

        data = self.load(self.applicant_family_details_members)
        app.male_count = toInt(data.get("male_count", ""))
        app.female_count = toInt(data.get("female_count", ""))
        app.members_above18 = toInt(data.get("members_above_18", ""))
        app.members_less_than_18 = toInt(data.get("members_less_than_18", ""))
        app.total_earning_members = toInt(data.get("total_earning_members", ""))
        app.total_number_of_family_members = toInt(data.get("total_number_of_family_members", ""))

        data = self.load(self.applicant_nominee_details)
        app.nominee_age = data.get("nominee_age", "")
        app.nominee_name = data.get("nominee_name", "")
        app.nominee_phone = data.get("nominee_phone", "")
        app.nominee_gender = data.get("nominee_gender", "")
        app.nominee_relation = data.get("nominee_relation", "")

        data = self.load(self.applicant_family_details_assets)
        app.type_of_house = data.get("type_of_house", "")
        app.quality_of_house = data.get("quality_of_house", "")
        app.house_stay_duration = toFloat(data.get("how_long_are_you_staying_in_house__in_years", ""))
        app.family_assets_land_acres = toFloat(data.get("family_assets_land_acres", ""))
        app.family_assets_orchard_acres = toFloat(data.get("family_assets_orchard__acres", ""))
        app.family_assets_number_of_rented_houses_or_flats = toFloat(data.get("family_assets_number_of_rented_houses_or_flats", ""))
        app.family_assets_number_of_rented_shops_or_godowns = toFloat(data.get("family_assets_number_of_rented_shops_or_godowns", ""))

        data = self.load(self.applicant_family_details_other_assets)
        app.family_assets_other = data.get("family_other_assets", "")

        data = self.load(self.applicant_loan_details_applied_loan)
        app.applied_loan = toFloat(data.get("required_loan_amount", ""))
        app.purpose_of_loan = data.get("purpose_of_the_loan", "")
        app.repayment_method = data.get("repayment_option", "")

        data = self.load(self.applicant_other_card_bank_details1)
        app.bank_name = data.get("bank_name", "")
        app.bank_ifsc_code = data.get("branch_ifsc_code", "")
        app.bank_account_number = data.get("account_number", "")
        app.bank_account_holder_name = data.get("account_holder_name", "")
        app.bank_bank_branch = data.get("bank_branch", "")
        app.bank_bank_account_type = data.get("bank_account_type", "")
        app.bank_account_operational_since = data.get("account_operational_since", "")

        data = self.load(self.applicant_other_card_bank_details2)
        app.bank2_name = data.get("bank_name", "")
        app.bank2_ifsc_code = data.get("branch_ifsc_code", "")
        app.bank2_account_number = data.get("account_number", "")
        app.bank2_account_holder_name = data.get("account_holder_name", "")
        app.bank2_bank_branch = data.get("bank_branch", "")
        app.bank2_bank_account_type = data.get("bank_account_type", "")
        app.bank2_account_operational_since = data.get("account_operational_since", "")

        data = self.load(self.applicant_business_docs_details1)
        app.primary_business_premise = data.get("biz_premise", "")
        app.primary_business_category = data.get("biz_category", "")
        app.primary_business_activities = data.get("biz_activity", "")
        app.primary_business_seasonality = data.get("biz_seasonality", "")
        app.primary_business_income_monthly = toFloat(data.get("biz_income_monthly", ""))
        app.primary_business_number_of_employees = toFloat(data.get("biz_num_employees", ""))
        app.primary_business_expense_rent = toFloat(data.get("biz_expense_rent", ""))
        app.primary_business_expense_admin = toFloat(data.get("biz_expense_admin", ""))
        app.primary_business_expense_other = toFloat(data.get("biz_expense_other", ""))
        app.primary_business_expense_working_capital = toFloat(data.get("biz_expense_working_capital", ""))
        app.primary_business_expense_employee_salary = toFloat(data.get("biz_expense_salary", ""))
        app.primary_business_number_of_years_in_business = toFloat(data.get("biz_num_years", ""))

        data = self.load(self.applicant_business_docs_details2)
        app.secondary_business = data.get("biz_activity", "")
        app.secondary_business_category = data.get("biz_category", "")
        app.secondary_business_income_monthly = toFloat(data.get("biz_income_monthly", ""))
        app.secondary_business_expenses_monthly = toFloat(data.get("biz_expenses_monthly", ""))

        data = self.load(self.applicant_business_docs_details3)
        app.tertiary_business = data.get("biz_activity", "")
        app.tertiary_business_category = data.get("biz_category", "")
        app.tertiary_business_income_monthly = toFloat(data.get("biz_income_monthly", ""))
        app.tertiary_business_expenses_monthly = toFloat(data.get("biz_expenses_monthly", ""))

        data = self.load(self.applicant_business_docs_details4)
        app.details_of_finished_goods = data.get("details_of_finished_goods","")
        app.business_outreach_methods = data.get("method_of_reaching_out_to_customers_to_increase_business","")
        app.place_of_storage_for_material = data.get("place_of_storage_for_material","")
        app.details_of_principal_raw_materials = data.get("details_of_principal_raw_materials","")
        app.nature_of_keeping_business_accounts = data.get("nature_of_keeping_business_accounts","")
        app.place_agency_of_purchase_of_materials = data.get("place_agency_of_purchase_of_materials","")
        app.business_assets_average_value_of_inventory = toFloat(data.get("business_assets_average_value_of_inventory",""))
        app.business_assets_average_value_of_receivables = toFloat(data.get("business_assets_average_value_of_receivables",""))

        data = self.load(self.applicant_family_expenditure)
        app.food_expense = toFloat(data.get("family_food_expenditure__monthly", ""))
        app.other_expense = toFloat(data.get("family_other_expenditure__monthly", ""))
        app.travel_expense = toFloat(data.get("family_travel_expenditure__monthly", ""))
        app.medical_expense = toFloat(data.get("family_medical_expenditure_monthly", ""))
        app.festival_expense = toFloat(data.get("family_festival_expenditure_monthly", ""))
        app.educational_expense = toFloat(data.get("family_education_expenditure_monthly", ""))
        app.entertainment_expense = toFloat(data.get("family_entertainment_expenditure__monthly", ""))

        data = self.load(self.applicant_hypothecation_goods_details1)
        app.primary_asset_for_hypothecation_purchase_year = data.get("purchase_year", "")
        app.primary_asset_for_hypothecation_purchase_price = toFloat(data.get("purchase_price", ""))
        app.primary_asset_for_hypothecation_purchase_purpose = data.get("purchase_purpose", "")
        app.primary_asset_for_hypothecation_current_market_value = toFloat(data.get("market_value", ""))
        app.primary_asset_for_hypothecation_details_of_hypothecated_goods = data.get("goods_details", "")

        data = self.load(self.applicant_hypothecation_goods_details2)
        app.secondary_asset_for_hypothecation_purchase_year  = data.get("purchase_year", "")
        app.secondary_asset_for_hypothecation_purchase_price = toFloat(data.get("purchase_price", ""))
        app.secondary_asset_for_hypothecation_purchase_purpose = data.get("purchase_purpose", "")
        app.secondary_asset_for_hypothecation_current_market_value = toFloat(data.get("market_value", ""))
        app.secondary_asset_for_hypothecation_details_of_hypothecated_goods = data.get("goods_details", "")

        data = self.load(self.applicant_hypothecation_goods_details3)
        app.tertiary_asset_for_hypothecation_purchase_year = data.get("purchase_year", "")
        app.tertiary_asset_for_hypothecation_purchase_price = toFloat(data.get("purchase_price", ""))
        app.tertiary_asset_for_hypothecation_purchase_purpose = data.get("purchase_purpose", "")
        app.tertiary_asset_for_hypothecation_current_market_value = toFloat(data.get("market_value", ""))
        app.tertiary_asset_for_hypothecation_details_of_hypothecated_goods = data.get("goods_details", "")

        data = self.load(self.applicant_other_card_liabilities)
        app.other_outstanding_emi = toFloat(data.get("liabilities_bank_loans", ""))
        app.other_outstanding_chit = toFloat(data.get("liabilities_chits", ""))
        app.other_outstanding_insurance = toFloat(data.get("liabilities_insurance", ""))
        app.other_outstanding_familynfriends = toFloat(data.get("liabilities_friends__family_hand_loans", ""))

        data = self.load(self.applicant_other_card_sales_info)
        app.sales_revenue_in_1_month = toFloat(data.get("sales_revenue_in_1_month", ""))
        app.sales_revenue_in_5_month = toFloat(data.get("sales_revenue_in_5_month", ""))
        app.sales_revenue_in_4_month = toFloat(data.get("sales_revenue_in_4_month", ""))
        app.sales_revenue_in_3_month = toFloat(data.get("sales_revenue_in_3_month", ""))
        app.sales_revenue_in_10_month = toFloat(data.get("sales_revenue_in_10_month", ""))
        app.sales_revenue_in_12_month = toFloat(data.get("sales_revenue_in_12_month", ""))
        app.sales_revenue_in_8_month = toFloat(data.get("sales_revenue_in_8_month", ""))
        app.total_annual_revenue_credit = toFloat(data.get("total_annual_revenue_credit", ""))
        app.sales_revenue_in_7_month = toFloat(data.get("sales_revenue_in_7_month", ""))
        app.sales_revenue_in_6_month = toFloat(data.get("sales_revenue_in_6_month", ""))
        app.sales_revenue_in_19_month = toFloat(data.get("sales_revenue_in_19_month", ""))
        app.total_annual_revenue_cash = toFloat(data.get("total_annual_revenue_cash", ""))
        app.sales_revenue_in_2_month = toFloat(data.get("sales_revenue_in_2_month", ""))
        app.sales_revenue_in_11_month = toFloat(data.get("sales_revenue_in_11_month", ""))

        locations_map = self.load(self.locations_map)
        app.home_loc = EsthenosOrgLocation(lat=locations_map["home"]["lat"], lng=locations_map["home"]["lng"])
        app.business_loc = EsthenosOrgLocation(lat=locations_map["business"]["lat"], lng=locations_map["business"]["lng"])

        applicant = self.load(self.guarantor1_kyc_details)
        app.applicant_kyc = EsthenosOrgApplicationKYC(
            kyc_type = applicant["type"],
            kyc_number = applicant["uid"],
            age = applicant["age"],
            dob = applicant["dob_yob"],
            name = applicant["name"],
            taluk = applicant["taluk"],
            state = applicant["state"],
            gender = applicant_personal.get("gender", ""),
            pincode = applicant["pincode"],
            address = applicant["address"],
            country = applicant["country"],
            district = applicant["district"],
            phone_number = applicant["phone_number"],
            mobile_number = applicant["mobile_number"],
            father_or_husband_name = applicant["father_s_husband_s_name"],
        )
        
        # add family details.
        data = self.load(self.applicant_family_details_details1)
        app.family_details1 = self.load_family_details(data)

        data = self.load(self.applicant_family_details_details2)
        app.family_details2 = self.load_family_details(data)

        data = self.load(self.applicant_family_details_details3)
        app.family_details3 = self.load_family_details(data)

        data = self.load(self.applicant_family_details_details4)
        app.family_details4 = self.load_family_details(data)

        data = self.load(self.applicant_family_details_details5)
        app.family_details5 = self.load_family_details(data)


        # add land details.
        data = self.load(self.applicant_other_card_land_details1)
        app.land_details1 = self.load_land_details(data)

        data = self.load(self.applicant_other_card_land_details2)
        app.land_details2 = self.load_land_details(data)

        data = self.load(self.applicant_other_card_land_details3)
        app.land_details3 = self.load_land_details(data)

        
        # add loan details.
        data = self.load(self.applicant_loan_details_details1)
        app.loan_details1 = self.load_loan_details(data)

        data = self.load(self.applicant_loan_details_details2)
        app.loan_details2 = self.load_loan_details(data)

        data = self.load(self.applicant_loan_details_details3)
        app.loan_details3 = self.load_loan_details(data)

        data = self.load(self.applicant_loan_details_details4)
        app.loan_details4 = self.load_loan_details(data)


        # add equipment type details.
        data = self.load(self.applicant_other_card_type_equipment1)
        app.type_equipment1 = self.load_type_equipment(data)

        data = self.load(self.applicant_other_card_type_equipment2)
        app.type_equipment2 = self.load_type_equipment(data)

        data = self.load(self.applicant_other_card_type_equipment3)
        app.type_equipment3 = self.load_type_equipment(data)


        # add vehicle docs
        data = self.load(self.applicant_personal_docs_vehicle1)
        app.docs_vehicle1 = self.load_docs_vehicle(data)

        data = self.load(self.applicant_personal_docs_vehicle2)
        app.docs_vehicle2 = self.load_docs_vehicle(data)

        data = self.load(self.applicant_personal_docs_vehicle3)
        app.docs_vehicle3 = self.load_docs_vehicle(data)


        # add guarantor details.
        guarantor1 = self.load(self.guarantor1_kyc_details)
        app.guarantor1_kyc = EsthenosOrgApplicationKYC(
            kyc_type = guarantor1["type"],
            kyc_number = guarantor1["uid"],
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

        guarantor2 = self.load(self.guarantor2_kyc_details)
        app.guarantor2_kyc = EsthenosOrgApplicationKYC(
            kyc_type = guarantor2["type"],
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

        assets_map = self.load(self.assets_map)
        applicant_docs = assets_map.get("applicant", {})
        app.applicant_docs = EsthenosOrgApplicationDocs(
            pan_docs = applicant_docs.get("pan_card", []),
            aadhar_docs = applicant_docs.get("aadhar_card", []),
            voterid_docs = applicant_docs.get("voter_card", []),
            personal_docs = applicant_docs.get("personal_docs", []),
            business_docs = applicant_docs.get("business_docs", []),
            other_docs = applicant_docs.get("other_card", []),
        )

        assets_map = self.load(self.assets_map)
        guarantor1_docs = assets_map.get("guarantor1", {})
        app.guarantor1_docs = EsthenosOrgApplicationDocs(
            pan_docs = guarantor1_docs.get("pan_card", []),
            aadhar_docs = guarantor1_docs.get("aadhar_card", []),
            voterid_docs = guarantor1_docs.get("voter_card", []),
            personal_docs = guarantor1_docs.get("personal_docs", []),
            business_docs = guarantor1_docs.get("business_docs", []),
            other_docs = guarantor1_docs.get("other_card", []),
        )

        assets_map = self.load(self.assets_map)
        guarantor2_docs = assets_map.get("guarantor2", {})
        app.guarantor2_docs = EsthenosOrgApplicationDocs(
            pan_docs = guarantor2_docs.get("pan_card", []),
            aadhar_docs = guarantor2_docs.get("aadhar_card", []),
            voterid_docs = guarantor2_docs.get("voter_card", []),
            personal_docs = guarantor2_docs.get("personal_docs", []),
            business_docs = guarantor2_docs.get("business_docs", []),
            other_docs = guarantor2_docs.get("other_card", []),
        )

        app_count = EsthenosOrg.objects.get(id=user.organisation.id).application_count + 1
        app.application_id = user.organisation.name.upper()[0:2] + str(settings.organisations_count) + "{0:06d}".format(app_count)

        app.update_status(110)
        app.save()

        return None
