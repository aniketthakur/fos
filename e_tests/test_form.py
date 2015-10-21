import json
import requests

url = "http://localhost:8080/api/organisation/applications"

querystring = {
    "instance_token":"ChADpwltz-mp-WkS0VIVyt8dP0Xtvac8Ee8ZY1lsPIg"
}

payload = {
    "applicant_other_card_land_details": {
        "estimated_resale_value_of_property": "88",
        "loan_outstanding_against_such_property": "8",
        "land_description": "h"
    },
    "assets_id": "acbd29e4-c21f-49ad-8417-239e5d180154",
    "group": "",
    "applicant_other_card_home_image": {},
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
    "applicant_family_details_details3": {
        "name": "",
        "education": "",
        "occupations_details": "",
        "age": "",
        "annual_income": "",
        "relation": ""
    },
    "applicant_kyc_details": {
        "address": "4/166, . near bus stand  ",
        "dob_yob": "1992",
        "pan_card_father_s_husband_s_name": "",
        "pincode": "516257",
        "pan_card_name": "",
        "occupation": "g",
        "state": "Andhra Pradesh",
        "taluk": "Lakkireddipalle",
        "voter_id_father_s_husband_s_name": "",
        "voter_id": "",
        "email_id": "b",
        "permanent_address": "",
        "pan_card_id": "",
        "phone_number": "6",
        "father_s_husband_s_name": "S/O Fyroz Basha",
        "age": "23",
        "country": "India",
        "district": "Cuddapah",
        "name": "Pattan Saddam Hussain",
        "uid": "565061987998",
        "voter_id_name": "",
        "type": "AADHAAR",
        "mobile_number": "9"
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
    "timeslot": {
        "time": "",
        "day": ""
    },
    "guarantor1_other_card_details2": {
        "bank_credit_co_perative_society": "",
        "name_of_borrower": "h",
        "loan_amount": ""
    },
    "applicant_other_card_electricity_details": {
        "name": ""
    },
    "applicant_other_card_bank_details2": {
        "bank_name": "hs",
        "account_holder_name": "hx",
        "bank_branch": "",
        "branch_ifsc_code": "a",
        "account_operational_since": "7",
        "bank_account_type": "Saving",
        "account_number": "4"
    },
    "guarantor1_kyc_details": {
        "address": ", .   Singhasan",
        "dob_yob": "1988",
        "pan_card_father_s_husband_s_name": "",
        "pincode": "332027",
        "pan_card_name": "",
        "occupation": "b",
        "state": "Rajasthan",
        "taluk": "Singhasan",
        "voter_id_father_s_husband_s_name": "",
        "voter_id": "",
        "email_id": "b",
        "permanent_address": "h",
        "pan_card_id": "",
        "phone_number": "7",
        "father_s_husband_s_name": "S/O Ganpat Singh",
        "age": "27",
        "country": "India",
        "district": "Sikar",
        "name": "Vijender Singh",
        "uid": "337972036560",
        "voter_id_name": "",
        "type": "AADHAAR",
        "mobile_number": "0"
    },
    "locations_map": {
        "home": {
            "lat": 0,
            "lng": 0
        },
        "center": {
            "lat": 0,
            "lng": 0
        },
        "business": {
            "lat": 23.00227111,
            "lng": 72.53280684
        }
    },
    "applicant_other_card_id_details": {
        "pan_card": "",
        "driving_license": "",
        "passport": "",
        "voter_id": "",
        "ration_card": ""
    },
    "applicant_other_card_nominee_details": {
        "nominee_relation": "Father",
        "nominee_phone": "97",
        "nominee_age": "97",
        "nominee_name": "bz",
        "nominee_gender": "Male"
    },
    "center": "",
    "applicant_business_docs_info": {
        "pancard_no": "",
        "details_of_principal_raw_materials": "",
        "business_name": "hz",
        "area_market_value": "",
        "vat_service_tax_regn_no": "",
        "description_business": "bz",
        "address_of_place_of_business": "",
        "shops__establishment_no": "",
        "details_of_finished_goods": "zh",
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
    "applicant_other_card_bank_details1": {
        "bank_name": "q",
        "account_holder_name": "z",
        "bank_branch": "",
        "branch_ifsc_code": "v",
        "account_operational_since": "6",
        "bank_account_type": "Saving",
        "account_number": "6"
    },
    "applicant_family_details_details1": {
        "name": "",
        "education": "",
        "occupations_details": "",
        "age": "",
        "annual_income": "",
        "relation": ""
    },
    "applicant_page_branch": {
        "tertiary_asset_for_hypothecation": "None"
    },
    "applicant_other_card_credit_card_details": {
        "issue_bank": "hz",
        "card_no": "67"
    },
    "applicant_other_card_liabilities": {
        "liabilities_chits": "",
        "liabilities_friends__family_hand_loans": "",
        "liabilities_insurance": "",
        "liabilities_bank_loans": ""
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
    "applicant_other_form_hypo_goods_image": {},
    "applicant_personal_docs": {
        "marital_status": "Married",
        "religion": "Hindu",
        "physical_disability": "Partial",
        "education": "Upto Primary",
        "gender": "Male",
        "category": "General"
    },
    "applicant_other_form_other_info": {
        "primary_asset_for_hypothecation___current_market_value": "5"
    },
    "applicant_family_details": {
        "family_festival_expenditure__monthly": "",
        "family_entertainment_expenditure__monthly": "",
        "family_travel_expenditure__monthly": "",
        "family_medical_expenditure__monthly": "",
        "family_other_expenditure__monthly": "",
        "family_food_expenditure__monthly": "",
        "family_education_expenditure__monthly": ""
    },
    "applicant_loan_details_applied_loan": {
        "repayment_option": "Weekly",
        "required_loan_amount": "N",
        "purpose_of_the_loan": "N"
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
    "applicant_family_details_members": {
        "members_above_18": "4",
        "members_less_than_18": "3",
        "total_number_of_family_members": "1",
        "female_count": "2",
        "total_earning_members": "4",
        "male_count": "14"
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
    "guarantor1_other_card_details1": {
        "bank_credit_co_perative_society": "",
        "name_of_borrower": "b",
        "loan_amount": ""
    },
    "guarantor2_kyc_details": {
        "address": "E-387, GALI N0-8.   Patparganj",
        "dob_yob": "1981",
        "pan_card_father_s_husband_s_name": "",
        "pincode": "110091",
        "pan_card_name": "",
        "occupation": "h",
        "state": "Delhi",
        "taluk": "East Vinod Nagar",
        "voter_id_father_s_husband_s_name": "",
        "voter_id": "",
        "email_id": "b",
        "permanent_address": "",
        "pan_card_id": "",
        "phone_number": "6",
        "father_s_husband_s_name": "S/O Shri Asharfi Lal Mehto",
        "age": "34",
        "country": "India",
        "district": "East Delhi",
        "name": "Pramod Kumar",
        "uid": "729348086056",
        "voter_id_name": "",
        "type": "AADHAAR",
        "mobile_number": "9"
    },
    "applicant_other_form_hypo_docs_image": {},
    "product": ""
}

headers = {
  'content-type': "application/json"
}

response = requests.post(url, json=payload, params=querystring)
print(response.text)