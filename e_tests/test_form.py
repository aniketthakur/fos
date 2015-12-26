import json
import requests


# url = "http://%s/api/token/sourcing" % ("localhost:8085")
# payload = {"email": "demo@fos-test.esthenos.com", "password":"demodemo"}
# response = requests.post(url, data=payload)
# print response.text

querystring = {
    "instance_token":"kLU_SA8ocKgvDSbhdgp-JTIsNTIzTvaMFwP6cyE2MDc"
}
url = "http://localhost:8085/api/organisation/applications"

payload = {
    "group": "",
    "applicant_business_docs_customer1": {
        "address": "",
        "name": "",
        "telephoneno": "",
        "telephone_no": ""
    },
    "applicant_family_details_details3": {
        "name": "",
        "education": "",
        "occupations_details": "",
        "age": "",
        "annual_income": "",
        "relation": ""
    },
    "applicant_nominee_details": {
        "nominee_relation": "Father",
        "nominee_phone": "",
        "nominee_age": "",
        "nominee_name": "",
        "nominee_gender": "Male"
    },
    "timeslot": {
        "time": "",
        "day": ""
    },
    "guarantor1_other_card_details2": {
        "bank_credit_co_perative_society": "",
        "name_of_borrower": "",
        "loan_amount": ""
    },
    "applicant_other_card_electricity_details": {
        "electricity_monthly_bill": "",
        "power_supplier": ""
    },
    "applicant_other_card_bank_details2": {
        "bank_name": "",
        "account_holder_name": "",
        "bank_branch": "",
        "branch_ifsc_code": "",
        "account_operational_since": "",
        "bank_account_type": "Saving",
        "account_number": ""
    },
    "applicant_other_card_bank_details1": {
        "bank_name": "",
        "account_holder_name": "",
        "bank_branch": "",
        "branch_ifsc_code": "",
        "account_operational_since": "",
        "bank_account_type": "Saving",
        "account_number": ""
    },
    "applicant_family_details_details1": {
        "name": "",
        "education": "",
        "occupations_details": "",
        "age": "",
        "annual_income": "",
        "relation": ""
    },
    "applicant_hypothecation_goods_details3": {
        "purchase_purpose": "",
        "market_value": "",
        "goods_details": "",
        "purchase_year": "",
        "purchase_price": "",
        "goods_image": "",
        "goods_docs_image": ""
    },
    "applicant_other_card_bank_details4": {
        "bank_name": "",
        "account_holder_name": "",
        "bank_branch": "",
        "branch_ifsc_code": "",
        "account_operational_since": "",
        "bank_account_type": "Saving",
        "account_number": ""
    },
    "applicant_business_docs_customer2": {
        "address": "",
        "name": "",
        "telephoneno": "",
        "telephone_no": ""
    },
    "applicant_family_expenditure": {
        "family_festival_expenditure__monthly": "",
        "family_entertainment_expenditure__monthly": "",
        "family_travel_expenditure__monthly": "",
        "family_medical_expenditure__monthly": "",
        "family_other_expenditure__monthly": "",
        "family_food_expenditure__monthly": "",
        "family_education_expenditure__monthly": ""
    },
    "applicant_loan_details_details1": {
        "type_of_loan": "",
        "interest": "",
        "name_of_bank": "",
        "emi_repayments": "",
        "outstanding_loan_amount": "",
        "collateral_details": "",
        "loan_detail": "Bank",
        "tenure_in_months": "",
        "loan_amount_key": ""
    },
    "applicant_loan_details_details4": {
        "type_of_loan": "",
        "interest": "",
        "name_of_bank": "",
        "emi_repayments": "",
        "outstanding_loan_amount": "",
        "collateral_details": "",
        "loan_detail": "Bank",
        "tenure_in_months": "",
        "loan_amount_key": ""
    },
    "applicant_loan_details_applied_loan": {
        "repayment_option": "Monthly",
        "required_loan_amount": "",
        "purpose_of_the_loan": ""
    },
    "applicant_business_docs_details3": {
        "biz_premise": "Own Premise",
        "biz_expense_rent": "",
        "biz_num_years": "",
        "biz_expense_salary": "",
        "biz_seasonality": "Yearly",
        "biz_category": "Trading",
        "biz_expense_other": "",
        "biz_expense_admin": "",
        "biz_expense_working_capital": "",
        "biz_num_employees": "",
        "biz_income_monthly": "",
        "biz_activity": ""
    },
    "applicant_loan_details_details3": {
        "type_of_loan": "",
        "interest": "",
        "name_of_bank": "",
        "emi_repayments": "",
        "outstanding_loan_amount": "",
        "collateral_details": "",
        "loan_detail": "Bank",
        "tenure_in_months": "",
        "loan_amount_key": ""
    },
    "applicant_family_details_assets": {
        "monthly_rent": "",
        "family_assets_land_acres": "",
        "family_assets_number_of_rented_shops_or_godowns": "",
        "family_assets_number_of_rented_houses_or_flats": "",
        "how_long_are_you_staying_in_house__in_years": "",
        "rent_agreement": "Yes",
        "quality_of_house": "Pakka/Concrete",
        "family_assets_orchard__acres": "",
        "type_of_house": "Family Owned"
    },
    "guarantor1_other_card_details1": {
        "bank_credit_co_perative_society": "",
        "name_of_borrower": "",
        "loan_amount": ""
    },
    "applicant_business_docs_customer4": {
        "address": "",
        "name": "",
        "telephoneno": "",
        "telephone_no": ""
    },
    "applicant_family_details_other_assets": {
        "family_other_assets": "Bike, Truck, Tractor, TV"
    },
    "product": "",
    "applicant_business_docs_customer5": {
        "address": "",
        "name": "",
        "telephoneno": "",
        "telephone_no": ""
    },
    "applicant_other_card_land_details": {
        "estimated_resale_value_of_property": "",
        "loan_outstanding_against_such_property": "",
        "land_description": ""
    },
    "assets_id": "698dd0ba-bfcd-4261-a591-3bd0d09d736d",
    "applicant_business_docs_billing": {
        "credit_period_in_days_to_individuals": "7",
        "chartered_accountant": "Yes",
        "sale_and_purchase_book": "Yes",
        "bank_account": "Yes",
        "place_of_storage_for_production_of_raw_material": "Place of Business",
        "formal_books_of_account": "Yes",
        "source_of_funding_for_purchase_of_material": "Own Funds",
        "credit_period_in_days_to_institutions": "7",
        "number_of_days_credit_for_raw_material_purchase": "7"
    },
    "applicant_business_docs_detail4": {
        "estimated_value": "",
        "number_of_relatives_helping_in_business": "",
        "permanent": "",
        "wage_payment_to_employees": "Daily",
        "type_of_equipment_machinery_used_in_business": "",
        "age_of_machinery": "",
        "contract_no": "",
        "average_wage_paid": "",
        "number_of_employees_already_present_in_mobile": "",
        "collateral_created_or_security_given_of_equipment": "",
        "method_of_reaching_out_to_customers_to_increase_business": "",
        "details_of_manufacturer": ""
    },
    "applicant_business_docs_details2": {
        "biz_premise": "Own Premise",
        "biz_expense_rent": "",
        "biz_num_years": "",
        "biz_expense_salary": "",
        "biz_seasonality": "Yearly",
        "biz_category": "Trading",
        "biz_expense_other": "",
        "biz_expense_admin": "",
        "biz_expense_working_capital": "",
        "biz_num_employees": "",
        "biz_income_monthly": "",
        "biz_activity": ""
    },
    "applicant_business_docs_details1": {
        "biz_premise": "Own Premise",
        "biz_expense_rent": "",
        "biz_num_years": "",
        "biz_expense_salary": "",
        "biz_seasonality": "Yearly",
        "biz_category": "Trading",
        "biz_expense_other": "",
        "biz_expense_admin": "",
        "biz_expense_working_capital": "",
        "biz_num_employees": "",
        "biz_income_monthly": "",
        "biz_activity": ""
    },
    "applicant_kyc_details": {
        "name": "Gsh",
        "address": ", .   ",
        "dob_yob": "-1",
        "pan_card_father_s_husband_s_name": "",
        "pincode": "",
        "pan_card_name": "",
        "occupation": "",
        "state": "",
        "taluk": "",
        "voter_id_father_s_husband_s_name": "",
        "voter_id": "",
        "email_id": "",
        "permanent_address": "",
        "pan_card_id": "",
        "phone_number": "",
        "father_s_husband_s_name": "",
        "age": "-1",
        "country": "India",
        "district": "",
        "uid": "",
        "voter_id_name": "",
        "type": "AADHAAR",
        "mobile_number": ""
    },
    "assets_map": {
        "guarantor1": {},
        "guarantor2": {},
        "applicant": {}
    },
    "applicant_other_card_phone_details": {
        "internet_data_uses": "",
        "mobile_services_provider": "",
        "billing_type": "",
        "handset_type": "",
        "average_monthly_bill": ""
    },
    "applicant_hypothecation_goods_details1": {
        "purchase_purpose": "",
        "market_value": "",
        "goods_details": "",
        "purchase_year": "",
        "purchase_price": "",
        "goods_image": "",
        "goods_docs_image": ""
    },
    "guarantor1_kyc_details": {
        "address": ", .   ",
        "dob_yob": "-1",
        "pan_card_father_s_husband_s_name": "",
        "pincode": "",
        "pan_card_name": "",
        "occupation": "",
        "state": "",
        "taluk": "",
        "voter_id_father_s_husband_s_name": "",
        "voter_id": "",
        "email_id": "",
        "permanent_address": "",
        "pan_card_id": "",
        "phone_number": "",
        "father_s_husband_s_name": "",
        "age": "-1",
        "country": "India",
        "district": "",
        "name": "",
        "uid": "",
        "voter_id_name": "",
        "type": "AADHAAR",
        "mobile_number": ""
    },
    "locations_map": {
        "home": {
            "lat": 12.97205203,
            "lng": 77.65267892
        },
        "business": {
            "lat": 12.97205203,
            "lng": 77.65267892
        }
    },
    "applicant_other_card_id_details": {
        "pan_card": "",
        "driving_license": "",
        "passport": "",
        "voter_id": "",
        "ration_card": ""
    },
    "center": "",
    "applicant_hypothecation_goods_details2": {
        "purchase_purpose": "",
        "market_value": "",
        "goods_details": "",
        "purchase_year": "",
        "purchase_price": "",
        "goods_image": "",
        "goods_docs_image": ""
    },
    "applicant_business_docs_info": {
        "pancard_no": "",
        "details_of_principal_raw_materials": "",
        "business_name": "",
        "area_market_value": "",
        "vat_service_tax_regn_no": "",
        "description_business": "",
        "address_of_place_of_business": "",
        "shops__establishment_no": "",
        "details_of_finished_goods": "",
        "area_occupied_of_business_sq_ft": ""
    },
    "applicant_family_details_details2": {
        "name": "",
        "education": "",
        "occupations_details": "",
        "age": "",
        "annual_income": "",
        "relation": ""
    },
    "applicant_other_card_credit_card_details": {
        "issue_bank": "",
        "card_no": ""
    },
    "applicant_business_docs_home_image": {},
    "applicant_other_card_liabilities": {
        "liabilities_chits": "",
        "liabilities_friends__family_hand_loans": "",
        "liabilities_insurance": "",
        "liabilities_bank_loans": ""
    },
    "applicant_business_docs_customer3": {
        "address": "",
        "name": "",
        "telephoneno": "",
        "telephone_no": ""
    },
    "applicant_business_docs_home_loc": {},
    "applicant_other_card_bank_details3": {
        "bank_name": "",
        "account_holder_name": "",
        "bank_branch": "",
        "branch_ifsc_code": "",
        "account_operational_since": "",
        "bank_account_type": "Saving",
        "account_number": ""
    },
    "applicant_personal_docs": {
        "marital_status": "Married",
        "religion": "Hindu",
        "physical_disability": "None",
        "education": "Upto Primary",
        "gender": "Male",
        "category": "General"
    },
    "applicant_family_details_members": {
        "members_above_18": "",
        "members_less_than_18": "",
        "total_number_of_family_members": "",
        "female_count": "",
        "total_earning_members": "",
        "male_count": ""
    },
    "applicant_loan_details_details2": {
        "type_of_loan": "",
        "interest": "",
        "name_of_bank": "",
        "emi_repayments": "",
        "outstanding_loan_amount": "",
        "collateral_details": "",
        "loan_detail": "Bank",
        "tenure_in_months": "",
        "loan_amount_key": ""
    },
    "guarantor2_kyc_details": {
        "address": ", .   ",
        "dob_yob": "-1",
        "pan_card_father_s_husband_s_name": "",
        "pincode": "",
        "pan_card_name": "",
        "occupation": "",
        "state": "",
        "taluk": "",
        "voter_id_father_s_husband_s_name": "",
        "voter_id": "",
        "email_id": "",
        "permanent_address": "",
        "pan_card_id": "",
        "phone_number": "",
        "father_s_husband_s_name": "",
        "age": "-1",
        "country": "India",
        "district": "",
        "name": "",
        "uid": "",
        "voter_id_name": "",
        "type": "AADHAAR",
        "mobile_number": ""
    }
}

for i in range(0, 10):
    response = requests.post(url, json=payload, params=querystring)
    print(response.text)
