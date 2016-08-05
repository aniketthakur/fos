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
    assets_id = TextField(validators=[v.Length(max=10000)])
    assets_map = TextField(validators=[v.Length(max=10000)])
    locations_map = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_cbcheck = TextField(validators=[v.Length(max=10000)])

    #newly added fields
    guarantor1_other_card_co_applicant = TextField(validators=[v.Length(max=10000)])
    guarantor1_kyc_details = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_ile_conformation= TextField(validators=[v.Length(max=10000)])
    applicant_family_details_ce_conformation= TextField(validators=[v.Length(max=10000)])
    applicant_other_card_assets_liabilities = TextField(validators=[v.Length(max=10000)])


    guarantor1_other_card_details1 = TextField(validators=[v.Length(max=10000)])
    guarantor1_other_card_details2 = TextField(validators=[v.Length(max=10000)])
    guarantor1_other_card_details3 = TextField(validators=[v.Length(max=10000)])
    guarantor2_kyc_details = TextField(validators=[v.Length(max=10000)])

    applicant_kyc_details = TextField(validators=[v.Length(max=10000)])

    applicant_loan_details_applied_loan = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_personal_detail = TextField(validators=[v.Length(max=10000)])
    applicant_nominee_details = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_liabilities = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_phone_details = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_electricity_details = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_credit_card_details = TextField(validators=[v.Length(max=10000)])

    applicant_hypothecation_goods_hypothecation1 = TextField(validators=[v.Length(max=10000)])
    applicant_hypothecation_goods_hypothecation2 = TextField(validators=[v.Length(max=10000)])
    applicant_hypothecation_goods_hypothecation3 = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_bank_details1 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_bank_details2 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_bank_details3 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_bank_details4 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_bank_details5 = TextField(validators=[v.Length(max=10000)])

    applicant_family_details_avg_monthly_exp = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_other_assets = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_members = TextField(validators=[v.Length(max=10000)])
    applicant_business_docs_detail4  = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_special_profile = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_type_of_equipment1 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_type_of_equipment2 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_type_of_equipment3 = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_assets = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_banking1 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_banking2 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_banking3 = TextField(validators=[v.Length(max=10000)])

    #added new fields
    applicant_family_details_family_members1 = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_family_members2 = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_family_members3 = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_family_members4 = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_family_members5 = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_family_members6 = TextField(validators=[v.Length(max=10000)])
    applicant_family_details_family_members7 = TextField(validators=[v.Length(max=10000)])


    applicant_loan_details_close_details1 = TextField(validators=[v.Length(max=10000)])
    applicant_loan_details_close_details2 = TextField(validators=[v.Length(max=10000)])
    applicant_loan_details_close_details3 = TextField(validators=[v.Length(max=10000)])
    applicant_loan_details_close_details4 = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_land_details1 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_land_details2 = TextField(validators=[v.Length(max=10000)])
    applicant_other_card_land_details3 = TextField(validators=[v.Length(max=10000)])

    applicant_business_docs_info = TextField(validators=[v.Length(max=10000)])

    applicant_business_docs_details4 = TextField(validators=[v.Length(max=10000)])

    applicant_personal_docs_vehicle1 = TextField(validators=[v.Length(max=10000)])
    applicant_personal_docs_vehicle2 = TextField(validators=[v.Length(max=10000)])
    applicant_personal_docs_vehicle3 = TextField(validators=[v.Length(max=10000)])

    applicant_business_docs_sale_info = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_family_assets = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_purchase_info = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_bus_monthly_exp = TextField(validators=[v.Length(max=10000)])

    applicant_business_docs_customer1 = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_cust_supplier = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_id_details = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_emp_business_info = TextField(validators=[v.Length(max=10000)])

    applicant_other_card_borrower_furnished = TextField(validators=[v.Length(max=10000)])

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
            age = data.get("age", ""),
            name = data.get("name", ""),
            sex = data.get("sex", ""),
            relation = data.get("relationship", ""),
            education = data.get("education", ""),
            years_of_involvement = data.get("years_of_involvement", ""),
            monthly_income = data.get("monthly_income", ""),
            occupations_details = data.get("occupations_details", ""),
        )


    def load_land_details(self, data):
        return EsthenosOrgApplicationLandDetails(
            area_in_sqft = toFloat(data.get("area_in_sqft", "")),
            land_location = data.get("land_location", ""),
            ownership = data.get("ownership", ""),
            loan_outstanding = toFloat(data.get("loan_outstanding", "")),
            estimated_resale_value = toFloat(data.get("estimated_resale_value", ""))
        )

    def load_loan_details(self, data):
        return EsthenosOrgApplicationLoanDetails(
            interest= data.get("interest", ""),
            type_of_loan = data.get("type_of_loan", ""),
            name_of_bank = data.get("name_of_bank", ""),
            loan_detail = data.get("loan_detail", ""),
            emi_repayments = data.get("emi_repayments", ""),
            loan_amount_key = data.get("loan_amount_key", ""),
            tenure_in_months = data.get("tenure_in_months", ""),
            collateral_details = data.get("collateral_details", ""),
        )

    def load_cardbanking_details(self,data):
        return  EstthenosOrgCardBankingDetails(
            bank_name = data.get("bank_name", ""),
            month_5_10th = data.get("month_5_10th", ""),
            month_2_30th = data.get("month_2_30th", ""),
            month_1_20th = data.get("month_1_20th", ""),
            month_5_30th = data.get("month_5_30th",""),
            month_4_credit = data.get("month_4_credit", ""),
            month_5_20th = data.get("month_5_20th",""),
            account_no = data.get("account_no",""),
            month_1_credit = data.get("month_1_credit",""),
            month_3_10th = data.get("month_3_10th",""),
            month_5_credit = data.get("month_5_credit",""),
            month_2_20th = data.get("month_2_20th",""),
            month_5_inward_bounce = data.get("month_5_inward_bounce",""),
            month_3_credit = data.get("month_3_credit",""),
            month_2_10th = data.get("month_2_10th",""),
            month_1_10th = data.get("month_1_10th",""),
            month_6_inward_bounce = data.get("month_6_inward_bounce",""),
            month_1_inward_bounce = data.get("month_1_inward_bounce",""),
            month_4_30th = data.get("month_4_30th",""),
            month_2_credit = data.get("month_2_credit",""),
            month_4_inward_bounce = data.get("month_4_inward_bounce",""),
            month_1_30th = data.get("month_1_30th",""),
            month_3_inward_bounce = data.get("month_3_inward_bounce",""),
            month_6_credit = data.get("month_6_credit",""),
            month_4_10th = data.get("month_4_10th",""),
            month_3_30th = data.get("month_3_30th",""),
            month_4_20th = data.get("month_4_20th",""),
            month_6_20th = data.get("month_6_20th",""),
            month_2_inward_bounce = data.get("month_2_inward_bounce",""),
            month_3_20th = data.get("month_3_20th",""),
            month_6_30th = data.get("month_6_30th",""),
            month_6_10th = data.get("month_6_10th",""),
        )

    def load_bank_details(self,data):
        return EsthenosOrgApplicationBankDetails(
            bank_name = data.get("bank_name", ""),
            bank_ifsc_code = data.get("branch_ifsc_code", ""),
            bank_account_number = data.get("account_number", ""),
            bank_account_holder_name = data.get("account_holder_name", ""),
            bank_bank_branch = data.get("bank_branch", ""),
            bank_bank_account_type = data.get("bank_account_type", ""),
            bank_account_operational_since = data.get("account_operational_since", ""),
            micr_code = data.get("micr_code", "")
        )

    def load_guarantor_card_details(self,data):
        return EsthenosOrgGuarantorCardDetails(
            bank_credit_society = data.get("bank_credit_co_perative_society",""),
            name_of_borrower = data.get("name_of_borrower",""),
            loan_amount = toFloat(data.get("loan_amount",""))
        )

    def load_type_equipment(self, data):
        return EsthenosOrgApplicationTypeEquipment(
            estimated_value = toFloat(data.get("estimated_value","")),
            details_of_equipment_supplier = data.get("details_of_equipment_supplier",""),
            date_of_manufacturing_equipment = data.get("date_of_manufacturing_equipment",""),
        )

    def load_docs_vehicle(self, data):
        return EsthenosOrgApplicationDocsVehicle(
            year_of_registration = toInt(data.get("year_of_registration","")),
            estimated_resale_value = toFloat(data.get("estimated_resale_value","")),
            type_of_vehicle_manufacturer = data.get("type_of_vehicle_manufacturer","")
        )

    def save(self,app):
        user = EsthenosUser.objects.get(id=current_user.id)
        is_app = True if app else False

        applicant_kyc = self.load(self.applicant_other_card_cbcheck)
        if not is_app:
            user.organisation.update(inc__application_count=1)
            app = EsthenosOrgApplication(
                name = applicant_kyc["name"],
                owner = user,
                assets_id = str(self.assets_id.data),
                organisation = user.organisation
            )
        else:
            previous_state = app.status
            app.assets_id = str(self.assets_id.data)
            app.name = applicant_kyc['name']
            app.update_status(185)

        # app.name = applicant_kyc["name"]
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

        # data = self.load(self.applicant_other_card_phone_details)
        # app.internet_data_uses = data.get("internet_data_uses", "")
        # app.mobile_services_provider = data.get("mobile_services_provider", "")
        # app.billing_type = data.get("billing_type", "")
        # app.handset_type = data.get("handset_type", "")
        # app.average_monthly_bill = toFloat(data.get("average_monthly_bill", ""))
        #
        # data = self.load(self.applicant_other_card_electricity_details)
        # app.electricity_monthly_bill = toFloat(data.get("electricity_monthly_bill", ""))
        # app.power_supplier = data.get("Tata Power", "")
        #
        # applicant_personal = self.load(self.applicant_other_card_personal_detail)
        # app.religion = applicant_personal.get("religion", "")
        # app.category = applicant_personal.get("category", "")
        # app.education = applicant_personal.get("education", "")
        # app.disability = applicant_personal.get("physical_disability", "")
        #
        # data = self.load(self.applicant_family_details_members)
        # app.male_count = toInt(data.get("male_count", ""))
        # app.female_count = toInt(data.get("female_count", ""))
        # app.members_above18 = toInt(data.get("members_above_18", ""))
        # app.members_less_than_18 = toInt(data.get("members_less_than_18", ""))
        # app.total_earning_members = toInt(data.get("total_earning_members", ""))
        # app.total_number_of_family_members = toInt(data.get("total_number_of_family_members", ""))
        #
        # data = self.load(self.applicant_nominee_details)
        # app.nominee_age = data.get("nominee_age", "")
        # app.nominee_name = data.get("nominee_name", "")
        # app.nominee_phone = data.get("nominee_phone", "")
        # app.nominee_gender = data.get("nominee_gender", "")
        # app.nominee_relation = data.get("nominee_relation", "")

        data = self.load(self.applicant_family_details_assets)
        app.quality_of_house = data.get("quality_of_house")
        app.house_stay_duration = data.get("how_long_are_you_staying_in_house__in_years", "")
        app.rent_agreement = data.get("rent_agreement", "")
        app.house_monthly_rent = data.get("monthly_rent", "")
        app.type_of_house = data.get("type_of_house", "")

        data = self.load(self.applicant_loan_details_applied_loan)
        app.applied_loan = toFloat(data.get("required_loan_amount", ""))
        app.purpose_of_loan = data.get("purpose_of_loan", "")
        app.repayment_method = data.get("repayment_option", "")

        data = self.load(self.applicant_business_docs_details4)
        app.details_of_finished_goods = data.get("details_of_finished_goods","")
        app.business_outreach_methods = data.get("method_of_reaching_out_to_customers_to_increase_business","")
        app.place_of_storage_for_material = data.get("place_of_storage_for_material","")
        app.details_of_principal_raw_materials = data.get("details_of_principal_raw_materials","")
        app.nature_of_keeping_business_accounts = data.get("nature_of_keeping_business_accounts","")
        app.place_agency_of_purchase_of_materials = data.get("place_agency_of_purchase_of_materials","")
        app.business_assets_average_value_of_inventory = toFloat(data.get("business_assets_average_value_of_inventory",""))
        app.business_assets_average_value_of_receivables = toFloat(data.get("business_assets_average_value_of_receivables",""))

        data = self.load(self.applicant_family_details_avg_monthly_exp)
        app.education_expenses = data.get("education_expenses", "")
        app.medical_expenses = data.get("medical_expenses", "")
        app.grocery_expenses = data.get("grocery_expenses", "")
        app.family_other_expenses = data.get("other_expenses", "")
        app.conveyance_expenses = data.get("conveyance_expenses", "")

        data = self.load(self.applicant_family_details_other_assets)
        app.family_other_assets = data.get("2 family_other_assets", "")

        data = self.load(self.applicant_business_docs_detail4)
        app.family_other_assets = data.get("place_of_storage_for_material", "")
        app.current_receivables = data.get("current_receivables", "")
        app.details_of_principal_raw_materials = data.get("details_of_principal_raw_materials", "")
        app.method_to_increase_business = data.get("method_of_reaching_out_to_customers_to_increase_business", "")
        app.nature_of_keeping_business_accounts = data.get("nature_of_keeping_business_accounts", "")
        app.place_agency_of_purchase_of_materials = data.get("place_agency_of_purchase_of_materials", "")
        app.stock_value_as_seen = data.get("stock_value_as_seen", "")

        data = self.load(applicant_other_card_special_profile)
        app.purchase_detail1 = data.get("purchase_details_1", "")
        app.purchase_cycle = data.get("purchase_cycle", "")
        app.purchase_details2 = data.get("purchase_details_2", "")
        app.cash_credit_percentage = data.get("cash_credit_percentage", "")
        app.details_of_key_purchaser = data.get("details_of_key_purchaser", "")
        app.is_business_socially_desirable = data.get("is_the_business_socially_desirable", "")
        app.purchase_details3 = data.get("purchase_details_3", "")
        app.payment_cycle_days = data.get("payment_cycle_days", "")

        data = self.load(self.applicant_business_docs_customer1)
        app.address = data.get("address", "")
        # app.name_4 = data.get("name_4", "")
        # app.name_3 = data.get("name_3", "")
        # app.address_4 = data.get("address_4", "")
        # app.name_2 = data.get("name_2", "")
        # app.name_5 = data.get("name_5", "")
        # app.telephone_no_4 = toInt(data.get("telephone_no_4", ""))
        # app.address_5 = data.get("address_5", "")
        # app.address_2 = data.get("address_2", "")
        # app.institution_credit= data.get("address_2", "")
        # app.telephone_no_3 = toInt(data.get("telephone_no_3", ""))
        # app.address_3 = data.get("address_3", "")
        # app.telephone_no_2 = toInt(data.get("telephone_no_2", ""))
        app.name= data.get("name", "")
        # app.individual_credit= data.get("individual_credit", "")
        # app.telephone_no_5 = toInt(data.get("telephone_no_5", ""))
        app.telephone_no = toInt(data.get("telephone_no", ""))
        app.telephoneno = toInt(data.get("telephoneno", ""))

        data = self.load(self.applicant_other_card_cust_supplier)
        app.sup_address = data.get("address","")
        app.sup_telephoneno_4 = toInt(data.get("telephoneno_4",""))
        app.sup_name_4 = data.get("name_4","")
        app.sup_name_3 = data.get("name_3","")
        app.sup_telephoneno_2= toInt(data.get("telephoneno_2",""))
        app.sup_address_5 = data.get("address_5","")
        app.sup_telephoneno_5 = toInt(data.get("telephoneno_5",""))
        app.sup_telephoneno_3 = toInt(data.get("telephoneno_3",""))
        app.sup_name_2 = data.get("name_2","")
        app.sup_name_5 = data.get("name_5","")
        app.sup_address_4 = data.get("address_4","")
        app.sup_address_2 = data.get("address_2","")
        app.sup_address_3 = data.get("address_3","")
        app.sup_name = data.get("name","")
        app.sup_telephoneno = toInt(data.get("telephoneno",""))

        data = self.load(self.applicant_loan_details_applied_loan)
        app.loan_type = data.get("loan_type","")
        app.required_loan_amount = data.get("required_loan_amount","")
        app.repayment_option = data.get("repayment_option","")
        app.emi_capacity = data.get("emi_capacity_as_per_the_customer","")
        app.type_of_repayment = data.get("type_of_repayment","")
        app.emi = data.get("emi","")
        app.tenure = data.get("tenure","")
        app.amount_allocated_for_assets = data.get("if_assets_purchaged_,_amount_allocated_for_assets","")
        app.purpose_of_loan = data.get("purpose_of_loan","")

        data = self.load(self.applicant_other_card_id_details)
        app.id_pancard = data.get("pan_card","")
        app.id_driving_license = data.get("driving_license","")
        app.id_passport = data.get("passport","")
        app.id_voter = data.get("voter_id","")
        app.id_ration_card = data.get("ration_card","")

        data = self.load(self.applicant_hypothecation_goods_hypothecation1)
        app.primary_asset_for_hypothecation_purchase_year = data.get("purchase_year", "")
        app.primary_asset_for_hypothecation_purchase_price = toFloat(data.get("purchase_price", ""))
        app.primary_asset_for_hypothecation_purchase_purpose = data.get("purchase_purpose", "")
        app.primary_asset_for_hypothecation_current_market_value = toFloat(data.get("market_value", ""))
        app.primary_asset_for_hypothecation_details_of_hypothecated_goods = data.get("goods_details", "")

        data = self.load(self.applicant_hypothecation_goods_hypothecation2)
        app.secondary_asset_for_hypothecation_purchase_year  = data.get("purchase_year", "")
        app.secondary_asset_for_hypothecation_purchase_price = toFloat(data.get("purchase_price", ""))
        app.secondary_asset_for_hypothecation_purchase_purpose = data.get("purchase_purpose", "")
        app.secondary_asset_for_hypothecation_current_market_value = toFloat(data.get("market_value", ""))
        app.secondary_asset_for_hypothecation_details_of_hypothecated_goods = data.get("goods_details", "")

        data = self.load(self.applicant_hypothecation_goods_hypothecation3)
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

        data = self.load(self.applicant_business_docs_sale_info)
        app.sales_revenue_in_1_month = data.get("sales_revenue_in_1_month", "")
        app.sales_revenue_in_5_month = data.get("sales_revenue_in_5_month", "")
        app.sales_revenue_in_4_month = data.get("sales_revenue_in_4_month", "")
        app.sales_revenue_in_3_month = data.get("sales_revenue_in_3_month", "")
        app.sales_revenue_in_10_month = data.get("sales_revenue_in_10_month", "")
        app.sales_revenue_in_12_month = data.get("sales_revenue_in_12_month", "")
        app.sales_revenue_in_8_month = data.get("sales_revenue_in_8_month", "")
        app.total_annual_revenue_credit = data.get("total_monthly_revenue__credit", "")
        app.peak_monthly_sale = data.get("peak_monthly_sale","")
        app.avg_lean_period_sale = data.get("avg_lean_period_sale","")
        app.avg_monthly_sale = data.get("avg_monthly_sale","")
        app.sales_revenue_in_7_month = data.get("sales_revenue_in_7_month", "")
        app.sales_revenue_in_6_month = data.get("sales_revenue_in_6_month", "")
        app.sales_revenue_in_9_month = data.get("sales_revenue_in_9_month", "")
        app.total_annual_revenue_cash = data.get("total_monthly_revenue__cash", "")
        app.sales_revenue_in_2_month = data.get("sales_revenue_in_2_month", "")
        app.sales_revenue_in_11_month = data.get("sales_revenue_in_11_month", "")

        data = self.load(self.applicant_other_card_purchase_info)
        app.raw_material_purchase_in_5_month = toFloat(data.get("raw_material_purchase_in_5_month", ""))
        app.raw_material_purchase_in_7_month = toFloat(data.get("raw_material_purchase_in_7_month", ""))
        app.raw_material_purchase_in_4_month = toFloat(data.get("raw_material_purchase_in_4_month", ""))
        app.raw_material_purchase_in_3_month = toFloat(data.get("raw_material_purchase_in_3_month", ""))
        app.raw_material_purchase_in_8_month = toFloat(data.get("raw_material_purchase_in_8_month", ""))
        app.raw_material_purchase_in_10_month = toFloat(data.get("raw_material_purchase_in_10_month", ""))
        app.total_annual_purchase_cash = toFloat(data.get("total_monthly_purchase__cash", ""))
        app.raw_material_purchase_in_11_month = toFloat(data.get("raw_material_purchase_in_11_month", ""))
        app.total_annual_purchase_credit = toFloat(data.get("total_monthly_purchase__credit", ""))
        app.raw_material_purchase_in_2_month = toFloat(data.get("raw_material_purchase_in_2_month", ""))
        app.raw_material_purchase_in_12_month = toFloat(data.get("raw_material_purchase_in_12_month", ""))
        app.raw_material_purchase_in_9_month = toFloat(data.get("raw_material_purchase_in_9_month", ""))
        app.raw_material_purchase_in_1_month = toFloat(data.get("raw_material_purchase_in_1_month", ""))
        app.raw_material_purchase_in_6_month = toFloat(data.get("raw_material_purchase_in_6_month", ""))

        data = self.load(self.applicant_other_card_family_assets)
        app.computer = data.get("computer", "")
        app.ref_y_n = data.get("ref_y_n", "")
        app.television = data.get("television", "")
        app.wm_y_n = data.get("wm_y_n", "")
        app.two_wheeler = data.get("2_wheeler", "")
        app.refrigerator = data.get("refrigerator", "")
        app.other_y_n = data.get("other_y_n", "")
        app.television_y_n = data.get("televsn_y_n", "")
        app.comp_y_n = data.get("comp_y_n", "")
        app.two_wheeler_y_n = data.get("2wheeler_y_n", "")
        app.washing_machine = data.get("washing_machine", "")

        data = self.load(self.applicant_other_card_emp_business_info)
        app.permanent_employees = toInt(data.get("permanent_employees", ""))
        app.average_monthly_wage_for_relatives = toFloat(data.get("monthly_wage_for_relatives", ""))
        app.relatives_in_business = toInt(data.get("relatives_in_business", ""))
        app.wages_paid = data.get("wages_paid", "")
        app.average_monthly_wage_for_contract_employees = toFloat(data.get("monthly_wage_for_contract_employees", ""))
        app.contract_employees = toInt(data.get("contract_employees", ""))
        app.average_monthly_wage_for_permanent_employees = toFloat(data.get("monthly_wage_for_permanent_employees", ""))

        data = self.load(self.applicant_other_card_bus_monthly_exp)
        app.utility_expenses = data.get("utility_expenses", "")
        app.fuel_expenses = data.get("fuel_expenses", "")
        app.selling_expenses = data.get("selling_expenses", "")
        app.transport_expenses = data.get("transport_expenses", "")

        data = self.load(self.applicant_business_docs_info)
        app.business_name = data.get("business_name", "")
        app.workplace_details = data.get("workplace_details", "")
        app.area_market_value = toFloat(data.get("area_market_value", ""))
        app.registered_rent_agreement = data.get("registered_rent_agreement", "")
        app.address_of_place_of_business = data.get("address_of_place_of_business", "")
        app.no_of_years_in_business = toInt(data.get("no_of_years_in_business", ""))
        app.shops__establishment_no = data.get("shops__establishment_no", "")
        app.monthly_rent = toFloat(data.get("monthly_rent", ""))
        app.type_of_business_entity = data.get("type_of_business_entity", "")
        app.area_occupied = toFloat(data.get("area_occupied", ""))
        app.outstanding_loan = toFloat(data.get("outstanding_loan", ""))
        app.description_business = data.get("description_business", "")
        app.activity = data.get("activity", "")

        data = self.load(self.applicant_other_card_credit_card_details)
        app.issue_bank_2 = data.get("issue_bank_2", "")
        app.issue_bank_1 = data.get("issue_bank_1", "")
        app.issue_bank_3 = data.get("issue_bank_3", "")

        data = self.load(self.applicant_other_card_borrower_furnished)
        app.no_borrowers_you_furnished_guarantees__ = data.get("for_how_many_borrowers_have_you_furnished_guarantees__", "")

        data = self.load(self.applicant_other_card_assets_liabilities)
        app.cash_balance = data.get("cash_balance", "")
        app.payable_supp = data.get("payable_to_suppliers", "")
        app.fixed_deposit_ppf = data.get("fixed_deposit_and_ppf", "")
        app.immovable_property_commercial = data.get("immovable_property_estimated_value___commercial", "")
        app.others_long_term = data.get("others_long_term_loans", "")
        app.loan_amount_payable_1 = data.get("loan__amount_payable_1_year_onwards", "")
        app.immovable_property_agriculture = data.get("immovable_property_estimated_value___agriculture", "")
        app.receivables_from_customer = data.get("receivables_from_customer", "")
        app.vehicles_current_estimate = data.get("vehicles_current_estimate_of_resale_value", "")
        app.short_term_loans = data.get("other_short_term_loans", "")
        app.bank_balance = data.get("bank_balance", "")
        app.immovable_property_residential = data.get("immovable_property_estimated_value___residential", "")
        app.gold_and_jewellery = data.get("gold_and_jewellery", "")
        app.raw_material_in_han = data.get("raw_material_in_han", "")
        app.insurance_policies = data.get("insurance_policies", "")
        app.loan_emis_payable_1 = data.get("loan__emis_payable_in_the_next_1_year", "")

        data = self.load(self.applicant_family_details_ce_conformation)
        app.confirmation_for_originl_doc_ce = data.get("i_confirm_that_i_have_seen_the_original_documents","")

        data = self.load(self.applicant_other_card_ref)
        app.ref_mobile_no_2 = data.get("ref_mobile_no_2","")
        app.ref_mobile_no_1 = data.get("ref_mobile_no_1","")
        app.ref_name_1 = data.get("ref_name_1","")
        app.ref_remarks_1 = data.get("ref_remarks_1","")
        app.ref_name_2 = data.get("ref_name_2","")
        app.ref_remarks_2 = data.get("ref_remarks_2","")

        data = self.load(self.applicant_other_card_product)
        app.product_details_1 = data.get("product_details_1", "")
        app.product_details_2 = data.get("product_details_2", "")
        app.product_details_3 = data.get("product_details_3", "")
        app.product_details_4 = data.get("product_details_4", "")
        app.product_details_10 = data.get("product_details_10", "")
        app.product_details_5 = data.get("product_details_5","")
        app.product_details_6 = data.get("product_details_6", "")
        app.product_details_7 = data.get("product_details_7", "")
        app.product_details_8 = data.get("product_details_8", "")

        data = self.load(applicant_business_docs_info_doc)
        app.tds_no = data.get("tds_no","")
        app.current_account_no = data.get("current_account_no","")
        app.electric_bil = data.get("comercial_indus_electric_bill_consumer_no","")
        app.ssi_registration_ref_no = data.get("ssi_registration_entrepeneur_memorandum_ref_no","")
        app.business_pancard_no = data.get("pancard_no","")
        app.permissions_licenses_reqd = data.get("permissions_licenses_reqd","")
        app.vat_service_tax_regn_no = data.get("vat_service_tax_regn_no","")

        locations_map = self.load(self.locations_map)
        # app.home_loc = EsthenosOrgLocation(lat=toFloat(locations_map.get("home",{}).get("lat","")), lng=toFloat(locations_map.get("home",{}).get("lng","")))
        app.business_loc = EsthenosOrgLocation(lat=toFloat(locations_map.get("business",{}).get("lat","")), lng=toFloat(locations_map.get("business",{}).get("lng","")))

        data = self.load(self.applicant_family_details_ile_conformation)
        app.confirmation_for_originl_doc_ile = data.get("i_confirm_that_i_have_seen_the_original_documents","")

        applicant = self.load(self.applicant_other_card_cbcheck)
        app.applicant_kyc = EsthenosOrgApplicationKYC(
            kyc_type = applicant.get("type",""),
            kyc_number = applicant.get("aadhar_card_number",""),
            age = applicant.get("age",""),
            dob = applicant.get("date_of_birth",""),
            name = applicant.get("name",""),
            taluk = applicant.get("taluk",""),
            state = applicant.get("state",""),
            gender = applicant.get("gender", ""),
            pincode = applicant.get("pin_code",""),
            address = applicant.get("address",""),
            country = applicant.get("country",""),
            district = applicant.get("district",""),
            phone_number = applicant.get("phone_number",""),
            mobile_number = applicant.get("mobile_number",""),
            mothers_name = applicant.get("mother_s_name",""),
            father_or_husband_name = applicant.get("father_s_name",""),
            spouse_aadhar_card_number = applicant.get("spouse_aadhar_card_number",""),
            spouse_name = applicant.get("spouse_name",""),
            occupation = applicant.get("occupation",""),
            emailid = applicant.get("email_id",""),
            voterid = applicant.get("voter_id",""),
            voterid_name = applicant.get("voter_id_name",""),
            voter_id_father_s_husband_s_name = applicant.get("voter_id_father_s_husband_s_name",""),
            pancard_id = applicant.get("pan_card",""),
            pancard_name = applicant.get("pan_card_name",""),
            pan_card_father_s_husband_s_name = applicant.get("pan_card_father_s_husband_s_name",""),
            ration_id = applicant.get("ration_card",""),
        )


        # add family details.
        data = self.load(self.applicant_family_details_family_members1)
        app.family_details1 = self.load_family_details(data)

        data = self.load(self.applicant_family_details_family_members2)
        app.family_details2 = self.load_family_details(data)

        data = self.load(self.applicant_family_details_family_members3)
        app.family_details3 = self.load_family_details(data)

        data = self.load(self.applicant_family_details_family_members4)
        app.family_details4 = self.load_family_details(data)

        data = self.load(self.applicant_family_details_family_members5)
        app.family_details5 = self.load_family_details(data)

        data = self.load(self.applicant_family_details_family_members6)
        app.family_details6 = self.load_family_details(data)

        data = self.load(self.applicant_family_details_family_members7)
        app.family_details7 = self.load_family_details(data)


        # add land details.
        data = self.load(self.applicant_other_card_residence)
        app.land_details1 = self.load_land_details(data)

        # data = self.load(self.applicant_other_card_land_details2)
        # app.land_details2 = self.load_land_details(data)
        #
        # data = self.load(self.applicant_other_card_land_details3)
        # app.land_details3 = self.load_land_details(data)
        #

        # add loan details.
        data = self.load(self.applicant_loan_details_close_details1)
        app.loan_details1 = self.load_loan_details(data)

        data = self.load(self.applicant_loan_details_close_details2)
        app.loan_details2 = self.load_loan_details(data)

        data = self.load(self.applicant_loan_details_close_details3)
        app.loan_details3 = self.load_loan_details(data)

        data = self.load(self.applicant_loan_details_close_details4)
        app.loan_details4 = self.load_loan_details(data)

        data = self.load(self.applicant_other_card_banking1)
        app.cardbank1 = self.load_cardbanking_details(data)

        data = self.load(self.applicant_other_card_banking2)
        app.cardbank2 = self.load_cardbanking_details(data)

        data = self.load(self.applicant_other_card_banking3)
        app.cardbank3 = self.load_cardbanking_details(data)

        #add bank details.
        data = self.load(self.applicant_other_card_bank_details1)
        app.bank_details1 = self.load_bank_details(data)

        data = self.load(self.applicant_other_card_bank_details2)
        app.bank_details2 = self.load_bank_details(data)

        data = self.load(self.applicant_other_card_bank_details3)
        app.bank_details3 = self.load_bank_details(data)

        data = self.load(self.applicant_other_card_bank_details4)
        app.bank_details4 = self.load_bank_details(data)

        data = self.load(self.applicant_other_card_bank_details5)
        app.bank_details5 = self.load_bank_details(data)

        #guarantor1 card details
        data = self.load(self.guarantor1_other_card_details1)
        app.guarantor_carddetails1 = self.load_guarantor_card_details(data)

        data = self.load(self.guarantor1_other_card_details2)
        app.guarantor_carddetails2 = self.load_guarantor_card_details(data)

        data = self.load(self.guarantor1_other_card_details3)
        app.guarantor_carddetails3 = self.load_guarantor_card_details(data)

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

        #newly_added _ field
        # data = self.load(self.applicant_other_card_cbcheck)
        # app.cbcheck_aadhar_card_number = data.get("aadhar_card_number","")
        # app.cbcheck_father_s_name = data.get("father_s_name","")
        # app.cbcheck_date_of_birth = data.get("date_of_birth","")
        # app.cbcheck_state = data.get("state","")
        # app.cbcheck_pin_code = data.get("pin_code","")
        # app.cbcheck_pan_card = data.get("pan_card","")
        # app.cbcheck_ration_card = data.get("ration_card","")
        # app.cbcheck_voter_id_number = data.get("voter_id_number","")
        # app.cbcheck_mobile_number = data.get("mobile_number","")
        # app.cbcheck_address = data.get("address","")
        # app.cbcheck_name = data.get("name","")
        # app.cbcheck_age = data.get("age","")
        # app.cbcheck_spouse_name = data.get("spouse_name","")
        # app.cbcheck_mother_s_name = data.get("mother_s_name","")
        # app.cbcheck_gender = data.get("gender","")
        # app.cbcheck_district = data.get("district","")
        #
        # data = self.load(self.guarantor1_other_card_co_applicant)
        # app.guarantor1_aadhar_card_number = data.get("aadhar_card_number","")
        # app.guarantor1_father_s_name = data.get("father_s_name","")
        # app.guarantor1_date_of_birth = data.get("date_of_birth","")
        # app.guarantor1_state = data.get("state","")
        # app.guarantor1_pin_code = data.get("pin_code","")
        # app.guarantor1_pan_card = data.get("pan_card","")
        # app.guarantor1_ration_card = data.get("ration_card","")
        # app.guarantor1_voter_id_number = data.get("voter_id_number","")
        # app.guarantor1_mobile_number = data.get("mobile_number","")
        # app.guarantor1_address = data.get("address","")
        # app.guarantor1_name = data.get("name","")
        # app.guarantor1_age = data.get("age","")
        # app.guarantor1_spouse_name = data.get("spouse_name","")
        # app.guarantor1_mother_s_name = data.get("mother_s_name","")
        # app.guarantor1_relation_with_the_applicant = data.get("relation_with_the_applicant","")
        # app.guarantor1_gender = data.get("gender","")
        # app.guarantor1_district = data.get("district","")

        # add guarantor details.
        guarantor1 = self.load(self.guarantor1_other_card_co_applicant)
        app.guarantor1_kyc = EsthenosOrgApplicationKYC(
            kyc_type = guarantor1.get("type", []),
            kyc_number = guarantor1.get("aadhar_card_number", []),
            age = guarantor1.get("age", []),
            dob = guarantor1.get("date_of_birth", []),
            name = guarantor1.get("name", []),
            taluk = guarantor1.get("taluk", []),
            state = guarantor1.get("state", []),
            gender = guarantor1.get("gender",[]),
            pincode = guarantor1.get("pin_code", []),
            address = guarantor1.get("address", []),
            country = guarantor1.get("country", []),
            district = guarantor1.get("district", []),
            phone_number = guarantor1.get("phone_number", []),
            mobile_number = guarantor1.get("mobile_number", []),
            father_or_husband_name = guarantor1.get("father_s_name", []),
            mothers_name = guarantor1.get("mother_s_name",[]),
            spouse_aadhar_card_number = guarantor1.get("spouse_aadhar_card_number", []),
            spouse_name = guarantor1.get("spouse_name", []),
            occupation = guarantor1.get("occupation", []),
            emailid = guarantor1.get("email_id",[]),
            voterid = guarantor1.get("voter_id_number",[]),
            voterid_name = guarantor1.get("voter_id_name",[]),
            voter_id_father_s_husband_s_name = guarantor1.get("voter_id_father_s_husband_s_name",[]),
            pancard_id = guarantor1.get("pan_card",[]),
            pancard_name = guarantor1.get("pan_card_name",[]),
            pan_card_father_s_husband_s_name = guarantor1.get("pan_card_father_s_husband_s_name",[]),
            ration_id = guarantor1.get("ration_card",[])
        )

        guarantor2 = self.load(self.guarantor2_kyc_details)
        app.guarantor2_kyc = EsthenosOrgApplicationKYC(
            kyc_type = guarantor2.get("type", []),
            kyc_number = guarantor2.get("uid", []),
            age = guarantor2.get("age", []),
            dob = guarantor2.get("dob_yob", []),
            name = guarantor2.get("name", []),
            taluk = guarantor2.get("taluk", []),
            state = guarantor2.get("state", []),
            pincode = guarantor2.get("pincode", []),
            address = guarantor2.get("address", []),
            country = guarantor2.get("country", []),
            district = guarantor2.get("district", []),
            phone_number = guarantor2.get("phone_number", []),
            mobile_number = guarantor2.get("mobile_number", []),
            father_or_husband_name = guarantor2.get("father_s_husband_s_name", []),
            spouse_aadhar_card_number = guarantor2.get("spouse_aadhar_card_number", []),
            spouse_name = guarantor2.get("spouse_name", []),
            occupation = guarantor1.get("occupation", []),
            emailid = guarantor1.get("email_id",[]),
            voterid = guarantor1.get("voter_id",[]),
            voterid_name = guarantor1.get("voter_id_name",[]),
            voter_id_father_s_husband_s_name = guarantor1.get("voter_id_father_s_husband_s_name",[]),
            pancard_id = guarantor1.get("pan_card_id",[]),
            pancard_name = guarantor1.get("pan_card_name",[]),
            pan_card_father_s_husband_s_name = guarantor1.get("pan_card_father_s_husband_s_name",[])
        )

        assets_map = self.load(self.assets_map)
        applicant_docs = assets_map.get("applicant", {})
        app.applicant_docs = EsthenosOrgApplicationDocs(
            pan_docs = applicant_docs.get("pan_card", []),
            aadhar_docs = applicant_docs.get("aadhar_card", []),
            voterid_docs = applicant_docs.get("voter_card", []),
            personal_docs = applicant_docs.get("personal_docs", []),
            business_docs = applicant_docs.get("business_docs", []),
            hypothecation_goods = applicant_docs.get("hypothecation_goods",[]),
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

        if not is_app:
            # group = EsthenosOrgGroup.objects.get(organisation=user.organisation, id=self.branch.data)
            app_count = EsthenosOrg.objects.get(id=user.organisation.id).application_count + 1
            app.application_id = user.organisation.name.upper()[0:2] + user.organisation.code + "{0:07d}".format(app_count)
            app.update_status(110)
            app.save()

        else:
            app.update_status(186)
            app.is_registered = True
            app.save()
            if 170 == previous_state:
                app.verified(True)
                app.update_status(187)
            else:
                if previous_state < 140 and previous_state not in [20, 25, 26]:
                    app.update_status(130)
                elif (previous_state >= 140 and previous_state in [180, 188]) or (previous_state in [20, 25, 26]):
                    app.update_status(188)

            app.save()


        return None
