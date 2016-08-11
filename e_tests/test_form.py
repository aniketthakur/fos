import json
import requests,sys

# url = "http://%s/api/app_token/generate" % ("localhost:8080")
# payload = {"email": "ramv@fos-test.esthenos.com", "password":"123"}
# response = requests.post(url, data=payload)
# print response.text
# sys.exit(0)

# url = "http://%s/api/organisation/branches/57a18d0985cfef7e6ce0f769/applications/pre_registration" % ("fos-arohan-test.esthenos.com")
url = "http://%s/api/organisation/applications"  % ("localhost:8080")
# url = "http://%s/api/organisation/branches" % ("fos-arohan-test.esthenos.com")
# url = "http://%s/api/token/sourcing" % ("fos-arohan-test.esthenos.com")
# url = "http://%s/api/token/sourcing" % ("localhost:8080")
# url = "http://%s/api/organisation/applications"  % ("localhost:8080")
# url = "http://%s/api/organisation/applications/pre_register" % ("localhost:8080")
# payload = {"email": "ileagent@fos-arohan-test.esthenos.com", "password":"123"}
# payload = {"email": "testce1@fos-arohan-test.esthenos.com", "password":"123"}
# response = requests.post(url, data=payload)
# print response.text

querystring = {
    # "instance_token":"VAu9IbgAU2HlXH5dua21IwmgLPVkup4oHIQGLs8-gjs"
    # "instance_token":"Y7Pxzm2zQZIvcRrrni_nPjyYMzdE7GNryu9tZfexR_I"
    # "instance_token":"_jwjjLLl6yBmsXYF9nqwgtSwRpFsdkNe8V23x1X9sQU"
    "instance_token":"M-u5wznPyaAsHy5aWlgnJ0Xw1cocfQq9Qcic8eJMvu8"
}

payload3 = {
    "guarantor1_other_card_co_applicant": {
        "address": "Vhtdgjhvvhgg Hhvvvhh",
        "aadhar_card_number": "262425252525",
        "father_s_name": "Mr. Ghgffghhh Ghgffyuhh",
        "date_of_birth": "11/08/1987",
        "state": "Assam",
        "gender": "Male",
        "pin_code": "242415",
        "spouse_name": "Mrs. Vghgfcvvv Bjhggg",
        "age": "29",
        "ration_card": "32417777",
        "relation_with_the_applicant": "Brother",
        "pan_card": "ERTYU5463V",
        "district": "Fhhhfvhjhhhh",
        "name": "  Fghhvfguhb Jhxfhhgg",
        "mother_s_name": "Mrs. Ghhgghhhhg Hhggggh",
        "voter_id_number": "FJDCNJGCVHJ",
        "mobile_number": "9747456552"
    },
    "assets_id": "b953c236-fbe3-49c6-9295-25b0b62a9601",
    "applicant_family_details_family_members7": {
        "age": "",
        "occupations_details": " ",
        "relationship": "",
        "name": "",
        "education": "",
        "annual_income": "",
        "sex": "",
        "years_of_involvement": ""
    },
    "branch": "57a46939ebc8b20f2871b815",
    "applicant_family_details_family_members4": {
        "age": "",
        "occupations_details": " ",
        "relationship": "",
        "name": "",
        "education": "",
        "annual_income": "",
        "sex": "",
        "years_of_involvement": ""
    },
    "applicant_family_details_family_members2": {
        "age": "",
        "occupations_details": " ",
        "relationship": "",
        "name": "",
        "education": "",
        "annual_income": "",
        "sex": "",
        "years_of_involvement": ""
    },
    "assets_map": {
        "guarantor1": {},
        "guarantor2": {},
        "applicant": {}
    },
    "applicant_family_details_family_members1": {
        "age": "",
        "occupations_details": " ",
        "relationship": "",
        "name": "",
        "education": "",
        "annual_income": "",
        "sex": "",
        "years_of_involvement": ""
    },
    "locations_map": {
        "business": {
            "lat": 0,
            "lng": 0
        }
    },
    "applicant_other_card_personal_detail": {
        "religion": "Hindu",
        "physical_disability": "None",
        "education": "PG and Above",
        "category": "General"
    },
    "applicant_family_details_family_members6": {
        "age": "",
        "occupations_details": " ",
        "relationship": "",
        "name": "",
        "education": "",
        "annual_income": "",
        "sex": "",
        "years_of_involvement": ""
    },
    "applicant_family_details_ile_conformation": {
        "i_confirm_that_i_have_seen_the_original_documents": "Yes"
    },
    "applicant_family_details_family_members5": {
        "age": "",
        "occupations_details": " ",
        "relationship": "",
        "name": "",
        "education": "",
        "annual_income": "",
        "sex": "",
        "years_of_involvement": ""
    },
    "applicant_family_details_family_members3": {
        "age": "",
        "occupations_details": " ",
        "relationship": "",
        "name": "",
        "education": "",
        "annual_income": "",
        "sex": "",
        "years_of_involvement": ""
    },
    "applicant_other_card_cbcheck": {
        "address": "Stxhchjbbngg",
        "aadhar_card_number": "252525252524",
        "father_s_name": "Mr. Bvcxdfghjj Vhjjh",
        "date_of_birth": "22/08/1989",
        "state": "Assam",
        "gender": "Male",
        "pin_code": "782435",
        "spouse_name": "Mrs. Qwerty Asd",
        "age": "27",
        "ration_card": "12345",
        "pan_card": "QWERT4331V",
        "district": "Rfthhddchh",
        "name": "  Jithin Jithin",
        "mother_s_name": "Mrs. Vuvghhgghhhhh",
        "voter_id_number": "THJJJJJJJN",
        "mobile_number": "8745213690"
    }
}



# url1 = "http://%s/api/organisation/branches" % ("localhost:8080")
# url1 = "http://%s/api/organisation/branches/579867d2ebc8b2422fc9849f/applications/pre_registration" % ("localhost:8080")
# url1 = "http://%s/api/organisation/branches" % ("fos-arohan-test.esthenos.com")
# print url1
#
# print payload3
# response = requests.post(url, data = payload3, params=querystring)
# print response.text
# url = "http://localhost:8080/api/organisation/applications"

payload1 = {
    "assets_id": "fdc2d6b9-026c-4b55-a795-1bc953e0bb5f",
    "applicant_other_card_assets_liabilities": {
        "insurance_policies": "",
        "others_long_term_loans": "",
        "raw_material_in_han": "",
        "cash_balance": "",
        "payable_to_suppliers": "",
        "loan__emis_payable_in_the_next_1_year": "",
        "vehicles_current_estimate_of_resale_value": "",
        "immovable_property_estimated_value___agriculture": "",
        "immovable_property_estimated_value___residential": "",
        "other_short_term_loans": "",
        "immovable_property_estimated_value___commercial": "",
        "loan__amount_payable_1_year_onwards": "",
        "fixed_deposit_and_ppf": "",
        "bank_balance": "",
        "receivables_from_customer": "",
        "gold_and_jewellery": ""
    },
    "branch": "57a46939ebc8b20f2871b815",
    "applicant_hypothecation_goods_hypothecation1": {
        "purchase_purpose": "",
        "market_value": "",
        "goods_details": "",
        "purchase_year": "",
        "purchase_price": ""
    },
    "applicant_business_docs_customer1": {
        "address": "",
        "name": "",
        "telephoneno": "",
        "telephone_no": ""
    },
    "applicant_other_card_purchase_info": {
        "raw_material_purchase_in_5_month": "",
        "raw_material_purchase_in_7_month": "",
        "raw_material_purchase_in_4_month": "",
        "raw_material_purchase_in_3_month": "",
        "raw_material_purchase_in_8_month": "",
        "total_monthly_purchase__credit": "",
        "raw_material_purchase_in_10_month": "",
        "raw_material_purchase_in_11_month": "",
        "raw_material_purchase_in_2_month": "",
        "raw_material_purchase_in_12_month": "",
        "raw_material_purchase_in_9_month": "",
        "total_monthly_purchase__cash": "",
        "raw_material_purchase_in_1_month": "",
        "raw_material_purchase_in_6_month": ""
    },
    "applicant_loan_details_active_details2": {
        "type_of_loan": "",
        "interest": "",
        "name_of_bank": "",
        "emi_repayments": "",
        "collateral_details": "",
        "loan_detail": "",
        "tenure_in_months": "",
        "loan_amount_key": ""
    },
    "applicant_business_docs_detail4": {
        "place_agency_of_purchase_of_materials": "",
        "nature_of_keeping_business_accounts": "Sale/Purchase Note Book",
        "details_of_principal_raw_materials": "",
        "current_receivables": "",
        "stock_value_as_seen": "",
        "method_of_reaching_out_to_customers_to_increase_business": "",
        "place_of_storage_for_material": "Godown"
    },
    "applicant_loan_details_close_details3": {
        "type_of_loan": "",
        "interest": "",
        "name_of_bank": "",
        "emi_repayments": "",
        "collateral_details": "",
        "loan_detail": "",
        "tenure_in_months": "",
        "loan_amount_key": ""
    },
    "applicant_loan_details_close_details2": {
        "type_of_loan": "",
        "interest": "",
        "name_of_bank": "",
        "emi_repayments": "",
        "collateral_details": "",
        "loan_detail": "",
        "tenure_in_months": "",
        "loan_amount_key": ""
    },
    "applicant_other_card_type_of_equipment3": {
        "estimated_value": "",
        "date_of_manufacturing_equipment": "",
        "details_of_equipment_supplier": ""
    },
    "applicant_family_details_avg_monthly_exp": {
        "education_expenses": "21",
        "medical_expenses": "24",
        "grocery_expenses": "25",
        "other_expenses": "23",
        "conveyance_expenses": "26"
    },
    "assets_map": {
        "guarantor1": {},
        "guarantor2": {},
        "applicant": {}
    },
    "applicant_other_card_banking1": {
        "month_3_inward_bounce": "",
        "month_3_20th": "",
        "month_2_10th": "",
        "month_2_credit": "",
        "month_6_20th": "",
        "month_5_inward_bounce": "",
        "month_2_30th": "",
        "month_6_credit": "",
        "month_1_20th": "",
        "month_5_30th": "",
        "month_5_20th": "",
        "month_2_20th": "",
        "month_4_30th": "",
        "month_4_10th": "",
        "month_3_30th": "",
        "month_3_credit": "",
        "month_1_10th": "",
        "month_6_30th": "",
        "month_6_10th": "",
        "month_1_credit": "",
        "month_3_10th": "",
        "bank_name": "",
        "month_5_10th": "",
        "month_1_inward_bounce": "",
        "month_5_credit": "",
        "month_2_inward_bounce": "",
        "month_1_30th": "",
        "account_no": "",
        "month_4_inward_bounce": "",
        "month_4_credit": "",
        "month_6_inward_bounce": "",
        "month_4_20th": ""
    },
    "applicant_other_card_emp_business_info": {
        "monthly_wage_for_permanent_employees": "",
        "permanent_employees": "",
        "monthly_wage_for_contract_employees": "",
        "monthly_wage_for_relatives": "",
        "relatives_in_business": "",
        "wages_paid": '',
        "contract_employees": ""
    },
    "applicant_other_card_bank_details2": {
        "account_holder_name": '',
        "bank_branch": '',
        "branch_ifsc_code": '',
        "account_operational_since": "",
        "bank_account_type": "",
        "micr_code": "",
        "bank_name": " ",
        "account_number": ''
    },
    "locations_map": {},
    "applicant_business_docs_info": {
        "workplace_details": "",
        "business_name": "",
        "area_occupied": "",
        "type_of_business_entity": "",
        "activity": "",
        "area_market_value": "",
        "monthly_rent": "",
        "outstanding_loan": "",
        "description_business": "",
        "address_of_place_of_business": "",
        "registered_rent_agreement": "",
        "shops__establishment_no": "",
        "no_of_years_in_business": ""
    },
    "applicant_other_card_residence": {
        "land_location": "",
        "ownership": "",
        "area_in_sqft": "",
        "estimated_resale_value": "",
        "loan_outstanding": ""
    },
    "applicant_other_card_bank_details1": {
        "account_holder_name": '',
        "bank_branch": '',
        "branch_ifsc_code": '',
        "account_operational_since": "",
        "bank_account_type": "Saving",
        "micr_code": "",
        "bank_name": "Axis Bank",
        "account_number": ''
    },
    "applicant_business_docs_home_image": {},
    "applicant_loan_details_active_details3": {
        "type_of_loan": "",
        "interest": "",
        "name_of_bank": "",
        "emi_repayments": "",
        "collateral_details": "",
        "loan_detail": "",
        "tenure_in_months": "",
        "loan_amount_key": ""
    },
    "applicant_loan_details_close_details1": {
        "type_of_loan": "",
        "interest": "",
        "name_of_bank": "",
        "emi_repayments": "",
        "collateral_details": "",
        "loan_detail": "",
        "tenure_in_months": "",
        "loan_amount_key": ""
    },
    "applicant_other_card_type_of_equipment2": {
        "estimated_value": "",
        "date_of_manufacturing_equipment": "",
        "details_of_equipment_supplier": ""
    },
    "applicant_business_docs_info_doc": {
        "current_account_no": "",
        "permissions_licenses_reqd": "",
        "comercial_indus_electric_bill_consumer_no": "",
        "pancard_no": "",
        "ssi_registration_entrepeneur_memorandum_ref_no": "",
        "tds_no": "",
        "vat_service_tax_regn_no": ""
    },
    "applicant_hypothecation_goods_hypothecation3": {
        "purchase_purpose": "",
        "market_value": "",
        "goods_details": "",
        "purchase_year": "",
        "purchase_price": ""
    },
    "applicant_other_card_cust_supplier": {
        "address": "",
        "telephoneno_4": "",
        "name_4": "",
        "name_3": "",
        "telephoneno_2": "",
        "address_5": "",
        "telephoneno_5": "",
        "telephoneno_3": "",
        "name_2": "",
        "name_5": "",
        "address_4": "",
        "address_2": "",
        "address_3": "",
        "name": "",
        "telephoneno": ""
    },
    "applicant_other_card_type_of_equipment1": {
        "estimated_value": "",
        "date_of_manufacturing_equipment": "",
        "details_of_equipment_supplier": ""
    },
    "applicant_other_card_bank_details3": {
        "account_holder_name": '',
        "bank_branch": '',
        "branch_ifsc_code": '',
        "account_operational_since": "",
        "bank_account_type": "",
        "micr_code": "",
        "bank_name": " ",
        "account_number": ''
    },
    "applicant_other_card_banking2": {
        "month_3_inward_bounce": "",
        "month_3_20th": "",
        "month_2_10th": "",
        "month_2_credit": "",
        "month_6_20th": "",
        "month_5_inward_bounce": "",
        "month_2_30th": "",
        "month_6_credit": "",
        "month_1_20th": "",
        "month_5_30th": "",
        "month_5_20th": "",
        "month_2_20th": "",
        "month_4_30th": "",
        "month_4_10th": "",
        "month_3_30th": "",
        "month_3_credit": "",
        "month_1_10th": "",
        "month_6_30th": "",
        "month_6_10th": "",
        "month_1_credit": "",
        "month_3_10th": "",
        "bank_name": "",
        "month_5_10th": "",
        "month_1_inward_bounce": "",
        "month_5_credit": "",
        "month_2_inward_bounce": "",
        "month_1_30th": "",
        "account_no": "",
        "month_4_inward_bounce": "",
        "month_4_credit": "",
        "month_6_inward_bounce": "",
        "month_4_20th": ""
    },
    "applicant_other_card_special_profile": {
        "is_the_business_socially_desirable": "",
        "purchase_details_2": "",
        "cash_credit_percentage": "",
        "details_of_key_purchaser": "",
        "purchase_cycle": "",
        "purchase_details_3": "",
        "purchase_details_1": "",
        "payment_cycle_days": ""
    },
    "applicant_other_card_banking3": {
        "month_3_inward_bounce": "",
        "month_3_20th": "",
        "month_2_10th": "",
        "month_2_credit": "",
        "month_6_20th": "",
        "month_5_inward_bounce": "",
        "month_2_30th": "",
        "month_6_credit": "",
        "month_1_20th": "",
        "month_5_30th": "",
        "month_5_20th": "",
        "month_2_20th": "",
        "month_4_30th": "",
        "month_4_10th": "",
        "month_3_30th": "",
        "month_3_credit": "",
        "month_1_10th": "",
        "month_6_30th": "",
        "month_6_10th": "",
        "month_1_credit": "",
        "month_3_10th": "",
        "bank_name": "",
        "month_5_10th": "",
        "month_1_inward_bounce": "",
        "month_5_credit": "",
        "month_2_inward_bounce": "",
        "month_1_30th": "",
        "account_no": "",
        "month_4_inward_bounce": "",
        "month_4_credit": "",
        "month_6_inward_bounce": "",
        "month_4_20th": ""
    },
    "applicant_hypothecation_goods_hypothecation2": {
        "purchase_purpose": "",
        "market_value": "",
        "goods_details": "",
        "purchase_year": "",
        "purchase_price": ""
    },
    "applicant_loan_details_applied_loan": {
        "repayment_option": "",
        "required_loan_amount": "",
        "emi_capacity_as_per_the_customer": "",
        "tenure": "",
        "if_assets_purchaged_,_amount_allocated_for_assets": "",
        "purpose_of_loan": "",
        "type_of_repayment": "",
        "loan_type": "",
        "emi": ""
    },
    "applicant_other_card_product": {
        "product_details_10": "",
        "product_details_8": "",
        "product_details_1": "",
        "product_details_7": "",
        "product_details_6": "",
        "product_details_4": "",
        "product_details_5": "",
        "product_details_3": "",
        "product_details_2": ""
    },
    "applicant_other_card_borrower_furnished": {
        "for_how_many_borrowers_have_you_furnished_guarantees__": "None"
    },
    "applicant_business_docs_sale_info": {
        "peak_monthly_sale": "",
        "sales_revenue_in_1_month": "",
        "sales_revenue_in_5_month": "",
        "avg_monthly_sale": "",
        "sales_revenue_in_4_month": "",
        "sales_revenue_in_3_month": '',
        "sales_revenue_in_10_month": "",
        "sales_revenue_in_12_month": "",
        "sales_revenue_in_8_month": "",
        "sales_revenue_in_7_month": "",
        "sales_revenue_in_6_month": "",
        "avg_lean_period_sale": "",
        "total_monthly_revenue__credit": "",
        "sales_revenue_in_9_month": '',
        "sales_revenue_in_2_month": "",
        "total_monthly_revenue__cash": "",
        "sales_revenue_in_11_month": ""
    },
    "applicant_loan_details_active_details1": {
        "type_of_loan": "",
        "interest": "",
        "name_of_bank": "",
        "emi_repayments": "",
        "collateral_details": "",
        "loan_detail": "",
        "tenure_in_months": "",
        "loan_amount_key": ""
    },
    "applicant_other_card_ref": {
        "ref_remarks_1": "",
        "ref_name_1": "",
        "ref_mobile_no_2": "",
        "ref_name_2": "",
        "ref_mobile_no_1": "",
        "ref_remarks_2": ""
    },
    "applicant_family_details_assets": {
        "how_long_are_you_staying_in_house__in_years": "1",
        "rent_agreement": "N/A",
        "quality_of_house": "Pakka/Concrete",
        "type_of_house": "Family Owned",
        "monthly_rent": ""
    },
    "applicant_other_card_bus_monthly_exp": {
        "selling_expenses": "",
        "transport_expenses": "",
        "fuel_expenses": "",
        "utility_expenses": ""
    },
    "application_id": "FO10000022",
    "applicant_family_details_ce_conformation": {
        "i_confirm_that_i_have_seen_the_original_documents": "Yes"
    },
    "applicant_family_details_other_assets": {
        "family_other_assets": "2 wheeler, Television, Computer, Washing Machine, Others"
    }
}



# # for i in range(0, 1):
response = requests.post(url,json =payload1, params=querystring)
print(response.text)
