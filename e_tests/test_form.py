import json
import requests,sys

# url = "http://%s/api/app_token/generate" % ("localhost:8080")
# payload = {"email": "ramv@fos-test.esthenos.com", "password":"123"}
# response = requests.post(url, data=payload)
# print response.text
# sys.exit(0)

# url = "http://%s/api/organisation/branches/57a18d0985cfef7e6ce0f769/applications/pre_registration" % ("fos-arohan-test.esthenos.com")
url = "http://%s/api/organisation/applications"  % ("fos-arohan-test.esthenos.com")
# url = "http://%s/api/organisation/branches" % ("fos-arohan-test.esthenos.com")
# url = "http://%s/api/token/sourcing" % ("fos-arohan-test.esthenos.com")
# url = "http://%s/api/token/sourcing" % ("localhost:8080")
# url = "http://%s/api/organisation/applications/pre_register" % ("localhost:8080")
# payload = {"email": "nitin@fos-arohan-test.esthenos.com", "password":"1234"}
# response = requests.post(url, data=payload)
# print response.text

querystring = {
    "instance_token":"VAu9IbgAU2HlXH5dua21IwmgLPVkup4oHIQGLs8-gjs"
    # "instance_token":"d2ey5FgfSZckwjDV_OVMpF-Y7K_tmvk_zrKewGG4j9Y"
}

payload3 = {
    "applicant_other_card_cbcheck": {
       "aadhar_card_number": "768686764676",
       "father_s_name": "Mr. Hzhxhxjxxh",
       "date_of_birth": "08/08/1991",
       "state": "Jharkhand",
       "pin_code": "676856",
       "pan_card": "SJDJD7263H",
       "ration_card": "HZHJHJDH",
       "voter_id_number": "HZJXJXUDHHJ",
       "mobile_number": "776876",
       "address": "Jxuxuxzdj",
       "name": "  Hdxdsf",
       "age": "25",
       "spouse_name": "Mr. Hz Hxhxx",
       "mother_s_name": "Mrs. Jz Jx Hz Us Is J",
       "gender": "Male",
       "district": "Hxhxhxj"
   },
   "guarantor1_other_card_co_applicant": {
       "aadhar_card_number": "686868646776",
       "father_s_name": "Mr. Jxhxuzhzh",
       "date_of_birth": "08/08/1986",
       "state": "Jharkhand",
       "pin_code": "768686",
       "pan_card": "HDHDJ7263H",
       "ration_card": "HZHXHXXIDH",
       "voter_id_number": "JZJXJXZZDJDH",
       "mobile_number": "6768384759",
       "address": "Hx Hz Hxjdjdj",
       "name": "  Hz Hz Ghj",
       "age": "30",
       "spouse_name": "Mr. Hxhxhdfh",
       "mother_s_name": "Mrs. Hxhxhzh",
       "relation_with_the_applicant": "bzhxxfhhxhxh",
       "gender": "Male",
       "district": "Jz Uxudh"
   },
   "assets_id": "a3b5daf8-93e3-4c74-a3b5-a6ee89ab85bd",
   "locations_map": {
       "business": {
           "lat": 12.972055,
           "lng": 77.6529905
       }
   },
   "applicant_other_card_personal_detail": {
       "religion": "Hindu",
       "education": "Upto 5th class",
       "physical_disability": "None",
       "category": "Other Backward Class"
   },
   "applicant_family_details_family_members4": {
       "relationship": "",
       "sex": "",
       "name": "",
       "age": "",
       "occupations_details": " ",
       "years_of_involvement": "",
       "annual_income": "",
       "education": ""
   },
   "branch": "57a091d885cfef0b638ed29b",
   "applicant_family_details_family_members3": {
       "relationship": "",
       "sex": "",
       "name": "",
       "age": "",
       "occupations_details": " ",
       "years_of_involvement": "",
       "annual_income": "",
       "education": ""
   },
   "assets_map": {
       "applicant": {},
       "guarantor1": {},
       "guarantor2": {}
   },
   "applicant_family_details_family_members2": {
       "relationship": "",
       "sex": "",
       "name": "",
       "age": "",
       "occupations_details": " ",
       "years_of_involvement": "",
       "annual_income": "",
       "education": ""
   },
   "applicant_family_details_family_members1": {
       "relationship": "",
       "sex": "",
       "name": "",
       "age": "",
       "occupations_details": " ",
       "years_of_involvement": "",
       "annual_income": "",
       "education": ""
   },
   "applicant_family_details_family_members7": {
       "relationship": "",
       "sex": "",
       "name": "",
       "age": "",
       "occupations_details": " ",
       "years_of_involvement": "",
       "annual_income": "",
       "education": ""
   },
   "applicant_family_details_ile_conformation": {
       "i_confirm_that_i_have_seen_the_original_documents": "Yes"
   },
   "applicant_family_details_family_members6": {
       "relationship": "",
       "sex": "",
       "name": "",
       "age": "",
       "occupations_details": " ",
       "years_of_involvement": "",
       "annual_income": "",
       "education": ""
   },
   "applicant_family_details_family_members5": {
       "relationship": "",
       "sex": "",
       "name": "",
       "age": "",
       "occupations_details": " ",
       "years_of_involvement": "",
       "annual_income": "",
       "education": ""
   }
}

payload2 = {
    "guarantor1_other_card_co_applicant": {
        "address": "Hdhdu",
        "aadhar_card_number": "57575",
        "father_s_name": "  Jshgh",
        "date_of_birth": "01/08/1983",
        "state": "Assam",
        "gender": "Female",
        "pin_code": "757576",
        "spouse_name": "  Usudu",
        "age": "33",
        "ration_card": "HZUZUDUDU",
        "relation_with_the_applicant": "hzhxh",
        "pan_card": "JZJDU2837H",
        "district": "Usudu",
        "name": "  Hshdu",
        "mother_s_name": "  Hshdu",
        "voter_id_number": "ISUDIDIR",
        "mobile_number": "6767656567"
    },
    "assets_id": "d0a13d9d-aa28-4b03-882d-ea6705f09d61",
    "applicant_family_details_family_members7": {
        "age": "",
        "occupations_details": " ",
        "relationship": "",
        "name": "",
        "education": "",
        "sex": "",
        "years_of_involvement": "",
        "monthly_income": ""
    },
    "branch": "57a468e0ebc8b20f2871b80b",
    "applicant_family_details_family_members4": {
        "age": "",
        "occupations_details": " ",
        "relationship": "",
        "name": "",
        "education": "",
        "sex": "",
        "years_of_involvement": "",
        "monthly_income": ""
    },
    "applicant_family_details_family_members2": {
        "age": "",
        "occupations_details": " ",
        "relationship": "",
        "name": "",
        "education": "",
        "sex": "",
        "years_of_involvement": "",
        "monthly_income": ""
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
        "sex": "",
        "years_of_involvement": "",
        "monthly_income": ""
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
        "category": "Schedule Cast"
    },
    "applicant_family_details_family_members6": {
        "age": "",
        "occupations_details": " ",
        "relationship": "",
        "name": "",
        "education": "",
        "sex": "",
        "years_of_involvement": "",
        "monthly_income": ""
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
        "sex": "",
        "years_of_involvement": "",
        "monthly_income": ""
    },
    "applicant_family_details_family_members3": {
        "age": "",
        "occupations_details": " ",
        "relationship": "",
        "name": "",
        "education": "",
        "sex": "",
        "years_of_involvement": "",
        "monthly_income": ""
    },
    "applicant_other_card_cbcheck": {
        "address": "Ggggdxcg",
        "aadhar_card_number": "558555555555",
        "father_s_name": "Mr. Rtuugf",
        "date_of_birth": "02/08/1987",
        "state": "Jharkhand",
        "gender": "Male",
        "pin_code": "123654",
        "spouse_name": "  ",
        "age": "29",
        "ration_card": "",
        "pan_card": "WRYHG5677W",
        "district": "Fhjjbgggg",
        "name": "  Uurdyuu Ghii",
        "mother_s_name": "Mrs. Ghjhvvvb",
        "voter_id_number": "",
        "mobile_number": "8865555588"
    }
}

# url1 = "http://%s/api/organisation/branches" % ("localhost:8080")
# url1 = "http://%s/api/organisation/branches/579867d2ebc8b2422fc9849f/applications/pre_registration" % ("localhost:8080")
# url1 = "http://%s/api/organisation/branches" % ("fos-arohan-test.esthenos.com")
# print url1
# response = requests.get(url, params=querystring)
# print response.text
# url = "http://localhost:8080/api/organisation/applications"

payload1 = {
    "assets_id": "5845e64e-243e-43bd-b7e5-cdead9bc95b1",
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
    "branch": "57a18d0985cfef7e6ce0f769",
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
        "education_expenses": "2365",
        "medical_expenses": "256",
        "grocery_expenses": "235",
        "other_expenses": "2563",
        "conveyance_expenses": "258"
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
        "land_location": "Ghkccvv",
        "ownership": "Owned",
        "area_in_sqft": "2500",
        "estimated_resale_value": "250000",
        "loan_outstanding": "8668"
    },
    "applicant_other_card_bank_details1": {
        "account_holder_name": "Chigcvbh",
        "bank_branch": "Ghifcbjjji",
        "branch_ifsc_code": "GJFXVJJJJ",
        "account_operational_since": "03/08/2016",
        "bank_account_type": "Saving",
        "micr_code": "",
        "bank_name": "Axis Bank",
        "account_number": "9150100555856"
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
        "is_the_business_socially_desirable": "Yes",
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
    "application_id": "FO10000071",
    "applicant_family_details_ce_conformation": {
        "i_confirm_that_i_have_seen_the_original_documents": "Yes"
    },
    "applicant_family_details_other_assets": {
        "family_other_assets": "Refrigerator, 2 wheeler"
    }
}



# for i in range(0, 1):
response = requests.get(url,data = payload1, params=querystring)
print(response.text)
