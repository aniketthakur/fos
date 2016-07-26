import json
import requests,sys

# url = "http://%s/api/app_token/generate" % ("localhost:8080")
# payload = {"email": "ramv@fos-test.esthenos.com", "password":"123"}
# response = requests.post(url, data=payload)
# print response.text
# sys.exit(0)
#
# url = "http://%s/api/token/sourcing" % ("localhost:8080")
# payload = {"email": "testce@fos-arohan-test.esthenos.com", "password":"123"}
# response = requests.post(url, data=payload)
# print response.text

querystring = {
    "instance_token":"f9rf973BejLpZQgbOmc5V3U7wDG2GLsTR7y1R86ITJQ"
}
url1 = "http://%s/api/organisation/branches" % ("localhost:8080")
print url1
response = requests.get(url1, params=querystring)
print response.text
# url = "http://localhost:8080/api/organisation/applications"

payload1 = {

    "group": "G-NA",
    "applicant_business_docs_customer1": {
        "address": "",
        "name_4": "",
        "name_3": "",
        "address_5": "",
        "name_2": "",
        "name_5": "",
        "telephone_no_4": "",
        "address_4": "",
        "address_2": "",
        "institution_credit": "7 days",
        "telephone_no_3": "",
        "address_3": "",
        "telephone_no_2": "",
        "name": "",
        "individual_credit_": "7 days",
        "telephone_no_5": "",
        "telephone_no": ""
    },
    "applicant_other_card_sales_info": {
        "sales_revenue_in_1_month": "",
        "sales_revenue_in_5_month": "",
        "sales_revenue_in_4_month": "",
        "sales_revenue_in_3_month": "",
        "sales_revenue_in_10_month": "",
        "sales_revenue_in_12_month": "",
        "sales_revenue_in_8_month": "",
        "total_annual_revenue_credit": "",
        "sales_revenue_in_7_month": "",
        "sales_revenue_in_6_month": "",
        "sales_revenue_in_9_month": "",
        "total_annual_revenue_cash": "",
        "sales_revenue_in_2_month": "",
        "sales_revenue_in_11_month": ""
    },
    "applicant_other_card_type_equipment3": {
        "estimated_value": "",
        "is_equipment_given_as_collateral__dropdown_with_values": "Yes",
        "date_of_manufacturing_equipment": "",
        "details_of_equipment_supplier": ""
    },
    "applicant_family_details_details3": {
        "aadhar_number": "",
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
    "guarantor1_other_card_details2": {
        "bank_credit_co_perative_society": "",
        "name_of_borrower": "",
        "loan_amount": ""
    },
    "applicant_other_card_electricity_details": {
        "electricity_monthly_bill": "",
        "power_supplier": ""
    },
    "applicant_other_card_emp_business_info": {
        "permanent_employees": "",
        "average_monthly_wage_for_relatives": "",
        "relatives_in_business": "",
        "wages_paid": "Daily",
        "average_monthly_wage_for_contract_employees": "",
        "contract_employees": "",
        "average_monthly_wage_for_permanent_employees": ""
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
    "applicant_other_card_land_details1": {
        "land_location": "",
        "type_of_property": "Residential",
        "area_in_sqft": "",
        "estimated_resale_value": "",
        "loan_outstanding": ""
    },
    "applicant_family_details_details5": {
        "aadhar_number": "",
        "name": "",
        "education": "",
        "occupations_details": "",
        "age": "",
        "annual_income": "",
        "relation": ""
    },
    "guarantor1_other_card_details3": {
        "bank_credit_co_perative_society": "",
        "name_of_borrower": "",
        "loan_amount": ""
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
        "aadhar_number": "",
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
        "purchase_price": ""
    },
    "applicant_other_card_land_details3": {
        "land_location": "",
        "type_of_property": "Residential",
        "area_in_sqft": "",
        "estimated_resale_value": "",
        "loan_outstanding": ""
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
    "applicant_family_expenditure": {
        "education_expenses": "",
        "medical_expenses": "",
        "grocery_expenses": "",
        "other_expenses": "",
        "conveyance_expenses": ""
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
        "purpose_of_loan": "",
        "repayment_option": "Monthly",
        "required_loan_amount": ""
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
        "how_long_are_you_staying_in_house__in_years": "1 year",
        "residence_details": "Family Owned",
        "rent_agreement": "Yes",
        "monthly_rent": ""
    },
    "applicant_other_card_family_assets": {
        "computer": "N/A",
        "ref_y_n": "No",
        "television": "N/A",
        "other": "N/A",
        "wm_y_n": "No",
        "2_wheeler": "N/A",
        "refrigerator": "N/A",
        "other_y_n": "No",
        "televsn_y_n": "No",
        "comp_y_n": "No",
        "2wheeler_y_n": "No",
        "washing_machine": "N/A"
    },
    "guarantor1_other_card_details1": {
        "bank_credit_co_perative_society": "",
        "name_of_borrower": "",
        "loan_amount": ""
    },
    "applicant_other_card_type_equipment2": {
        "estimated_value": "",
        "is_equipment_given_as_collateral__dropdown_with_values": "Yes",
        "date_of_manufacturing_equipment": "",
        "details_of_equipment_supplier": ""
    },
    "product": "",
    "assets_id": "637a1c02-aeaf-4376-a0b3-83bcef4011a5",
    "applicant_family_details_details4": {
        "aadhar_number": "",
        "name": "",
        "education": "",
        "occupations_details": "",
        "age": "",
        "annual_income": "",
        "relation": ""
    },
    "applicant_other_card_bank_details6": {
        "bank_name": "",
        "account_holder_name": "",
        "bank_branch": "",
        "branch_ifsc_code": "",
        "account_operational_since": "",
        "bank_account_type": "Saving",
        "account_number": ""
    },
    "applicant_other_card_purchase_info": {
        "raw_material_purchase_in_5_month": "",
        "raw_material_purchase_in_7_month": "",
        "raw_material_purchase_in_4_month": "",
        "raw_material_purchase_in_3_month": "",
        "raw_material_purchase_in_8_month": "",
        "raw_material_purchase_in_10_month": "",
        "total_annual_purchase_cash": "",
        "raw_material_purchase_in_11_month": "",
        "total_annual_purchase_credit": "",
        "raw_material_purchase_in_2_month": "",
        "raw_material_purchase_in_12_month": "",
        "raw_material_purchase_in_9_month": "",
        "raw_material_purchase_in_1_month": "",
        "raw_material_purchase_in_6_month": ""
    },
    "applicant_business_docs_detail4": {
        "place_agency_of_purchase_of_materials": "",
        "business_assets_average_value_of_inventory": "",
        "nature_of_keeping_business_accounts": "Sale/Purchase Note Book",
        "details_of_principal_raw_materials": "",
        "place_of_storage_for_material": "Godown",
        "method_of_reaching_out_to_customers_to_increase_business": "",
        "details_of_finished_goods": "",
        "business_assets_average_value_of_receivables": ""
    },
    "applicant_personal_docs_vehicle1": {
        "estimated_resale_value": "",
        "year_of_registration": "",
        "type_of_vehicle_manufacturer": ""
    },
    "applicant_kyc_details": {
        "spouse_aadhar_card_number": "",
        "pan_card_father_s_husband_s_name": "",
        "pan_card_name": "",
        "gender": "Male",
        "voter_id_father_s_husband_s_name": "",
        "email_id": "",
        "phone_number": "",
        "father_s_husband_s_name": "Nmkhhb",
        "age": "40",
        "type": "AADHAAR",
        "mobile_number": "",
        "address": "Bjkjv",
        "dob_yob": "13/06/1976",
        "pincode": "",
        "occupation": "",
        "state": "",
        "taluk": "",
        "voter_id": "",
        "spouse_name": "",
        "permanent_address": "",
        "pan_card_id": "",
        "country": "India",
        "district": "",
        "name": "Jithin",
        "uid": "756588637785",
        "voter_id_name": ""
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
    "applicant_other_card_bank_details5": {
        "bank_name": "",
        "account_holder_name": "",
        "bank_branch": "",
        "branch_ifsc_code": "",
        "account_operational_since": "",
        "bank_account_type": "Saving",
        "account_number": ""
    },
    "applicant_hypothecation_goods_details1": {
        "purchase_purpose": "",
        "market_value": "",
        "goods_details": "",
        "purchase_year": "",
        "purchase_price": ""
    },
    "guarantor1_kyc_details": {
        "spouse_aadhar_card_number": "",
        "pan_card_father_s_husband_s_name": "",
        "pan_card_name": "",
        "gender": "Male",
        "voter_id_father_s_husband_s_name": "",
        "email_id": "",
        "phone_number": "",
        "father_s_husband_s_name": "",
        "age": "-1",
        "type": "AADHAAR",
        "mobile_number": "",
        "address": "",
        "dob_yob": "-1",
        "pincode": "",
        "occupation": "",
        "state": "",
        "taluk": "",
        "voter_id": "",
        "spouse_name": "",
        "permanent_address": "",
        "pan_card_id": "",
        "country": "India",
        "district": "",
        "name": "ramesh",
        "uid": "",
        "voter_id_name": ""
    },
    "applicant_personal_docs_vehicle3": {
        "estimated_resale_value": "",
        "year_of_registration": "",
        "type_of_vehicle_manufacturer": ""
    },
    "locations_map": {
        "business": {
            "lat": 12.9720551,
            "lng": 77.6530023
        }
    },
    "applicant_other_card_type_equipment1": {
        "estimated_value": "",
        "is_equipment_given_as_collateral__dropdown_with_values": "Yes",
        "date_of_manufacturing_equipment": "",
        "details_of_equipment_supplier": ""
    },
    "applicant_other_card_id_details": {
        "pan_card": "",
        "driving_license": "",
        "passport": "",
        "voter_id": "",
        "ration_card": ""
    },
    "center": "C-NA",
    "applicant_hypothecation_goods_details2": {
        "purchase_purpose": "",
        "market_value": "",
        "goods_details": "",
        "purchase_year": "",
        "purchase_price": ""
    },
    "applicant_business_docs_info": {
        "permissions_licenses_reqd": "",
        "business_name": "",
        "type_of_business_entity": "Proprietor",
        "area_market_value": "",
        "vat_service_tax_regn_no": "",
        "monthly_rent": "",
        "ssi_registration_entrepeneur_memorandum_ref_no": "",
        "description_business": "",
        "registered_rent_agreement": "Yes",
        "shops__establishment_no": "",
        "no_of_years_in_business": "",
        "workplace_details": "Owned",
        "pancard_no": "",
        "area_occupied": "",
        "outstanding_loan": "",
        "address_of_place_of_business": ""
    },
    "applicant_family_details_details2": {
        "aadhar_number": "",
        "name": "",
        "education": "",
        "occupations_details": "",
        "age": "",
        "annual_income": "",
        "relation": ""
    },
    "applicant_other_card_assets_liability": {
        "insurance_policies": "",
        "loans_from_relatives,money_lender_etc": "",
        "creditors_for_raw_material": "",
        "raw_material_in_han": "",
        "loan_outstanding_against__property_value___agriculture": "",
        "loan_outstanding_against__property_value___residential": "",
        "vehicle_loans": "",
        "loan_outstanding_against__property_value___commercial_": "",
        "cash_and_bank_balance": "",
        "vehicles_current_estimate_of_resale_value": "",
        "immovable_property_estimated_value___agriculture": "",
        "immovable_property_estimated_value___residential": "",
        "immovable_property_estimated_value___commercial": "",
        "fixed_deposit_and_ppf": "",
        "receivables_from_customer": "",
        "gold_and_jewellery": ""
    },
    "applicant_other_card_credit_card_details": {
        "issue_bank_2": "",
        "issue_bank_1": "",
        "issue_bank_3": ""
    },
    "applicant_business_docs_home_image": {},
    "applicant_business_docs_home_loc": {},
    "applicant_other_card_cust_supplier": {
        "address": "",
        "telephoneno_4": "",
        "name_4": "",
        "name_3": "",
        "telephoneno_2": "",
        "address_5": "",
        "telephoneno_5": "",
        "telephoneno_3": "",
        "credit": "7 days",
        "name_2": "",
        "name_5": "",
        "address_4": "",
        "address_2": "",
        "address_3": "",
        "name": "",
        "telephoneno": ""
    },
    "applicant_other_card_land_details2": {
        "land_location": "",
        "type_of_property": "Residential",
        "area_in_sqft": "",
        "estimated_resale_value": "",
        "loan_outstanding": ""
    },
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
        "education": "SSC",
        "category": "General"
    },
    "applicant_other_card_borrower_furnished": {
        "for_how_many_borrowers_have_you_furnished_guarantees__": "Three"
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
        "spouse_aadhar_card_number": "",
        "pan_card_father_s_husband_s_name": "",
        "pan_card_name": "",
        "gender": "Male",
        "voter_id_father_s_husband_s_name": "",
        "email_id": "",
        "phone_number": "",
        "father_s_husband_s_name": "",
        "age": "-1",
        "type": "AADHAAR",
        "mobile_number": "",
        "address": "",
        "dob_yob": "-1",
        "pincode": "",
        "occupation": "",
        "state": "",
        "taluk": "",
        "voter_id": "",
        "spouse_name": "",
        "permanent_address": "",
        "pan_card_id": "",
        "country": "India",
        "district": "",
        "name": "suresh",
        "uid": "",
        "voter_id_name": ""
    },
    "applicant_other_card_bus_monthly_exp": {
        "electricity_charges": "",
        "freight_charges": "",
        "petrol_expenses": "",
        "other_expenses": "",
        "salaries_and_wages": ""
    },
    "applicant_personal_docs_vehicle2": {
        "estimated_resale_value": "",
        "year_of_registration": "",
        "type_of_vehicle_manufacturer": ""
    }
}

# for i in range(0, 1):
#     response = requests.post(url, json=payload, params=querystring)
#     print(response.text)
