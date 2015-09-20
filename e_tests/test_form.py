import json
import requests

url = "http://localhost:8080/mobile/application/json"

querystring = {
  "instance_token":"8SxMXsnLgRzgeIpufwdBPPrD6lm_awBFzA7kd51-zxs"
}

payload = {
    "appId": "02973f8d-3c85-44a3-826e-821506475014",
    "applicant_other_info": {
        "psychometric_test_q2": "Answer 3.",
        "2nd_asset_for_hypothecation": "None",
        "asset_for_hypothecation___current_market_value": "698",
        "nominee_name": "Ahvz",
        "nominee_gender": "Male",
        "psychometric_test_q4": "Answer 1.",
        "psychometric_test_q9": "Answer 4.",
        "family_travel_expenditure__monthly": "6",
        "primary_business_activities": "Sc",
        "financial_liabilities_chits": "25",
        "asset_for_hypothecation___details_of_hypothecated_goods": "Ggh",
        "account_number": "55555555555555555",
        "total_earning_members": "15",
        "repayment_option": "Fortnightly",
        "account_holder_name": "Gh",
        "family_festival_expenditure_monthly": "58",
        "nominee_age": "6797",
        "female_count": "12",
        "secondary_business_category": "None",
        "asset_for_hypothecation___purchase_purpose": "Thf",
        "financial_liabilities_bank_loans": "41",
        "nominee_phone": "9797797997",
        "marital_status": "Married",
        "asset_for_hypothecation___purchase_price": "365",
        "nominee_relationship_with_borrower": "Spouse",
        "male_count": "15",
        "financial_liabilities_insurance": "98",
        "psychometric_test_q7": "Answer 3.",
        "primary_business_expenditure___employee_salary": "23",
        "family_education_expenditure_monthly": "48",
        "members_less_than_18": "13",
        "primary_business___premise": "Own Premise",
        "psychometric_test_q6": "Answer 2.",
        "required_loan_amount": "25",
        "primary_business_expenditure___admin": "59",
        "primary_business___number_of_employees": "5",
        "other_family_asset_s": "Flat/ House on rent, Car, Tractor, Van",
        "psychometric_test_q1": "Answer 4.",
        "tertiary_business_category": "None",
        "primary_business_income_monthly": "45",
        "family_assets_orchard__acres": "58",
        "psychometric_test_q5": "Answer 1.",
        "family_entertainment_expenditure__monthly": "25",
        "asset_for_hypothecation___purchase_year": "36",
        "primary_business_seasonality": "Yearly",
        "family_assets_number_of_rented_shops_or_godowns": "5",
        "family_assets_number_of_rented_houses_or_flats": "4",
        "gender": "Male",
        "quality_of_house": "Kaccha/Mud",
        "family_other_expenditure_monthly": "33",
        "members_above_18": "14",
        "category": "OBC",
        "family_food_expenditure__monthly": "2",
        "3rd_asset_for_hypothecation": "None",
        "education": "Post Graduate",
        "psychometric_test_q10": "Answer 3.",
        "primary_business_expenditure___working_capital": "41",
        "primary_business_category": "Trading",
        "financial_liabilities_friends__family_hand_loans": "32",
        "primary_business___number_of_years_in_business": "58",
        "psychometric_test_q3": "Answer 2.",
        "family_assets_land_acres": "5",
        "bank_name": "Gf",
        "ifsc_code": "gfvhuhcdd",
        "family_medical_expenditure_monthly": "66",
        "primary_business_expenditure___other_expenses": "44",
        "how_long_are_you_staying_in_house__in_years": "4",
        "purpose_of_the_loan": "Rg",
        "total_number_of_family_members": "1",
        "physical_disability_member": "None",
        "primary_business_expenditure___rent": "59",
        "religion": "Jain",
        "type_of_house": "Self Owned",
        "psychometric_test_q8": "Answer 4."
    },
    "applicant_other_form_hypo_docs_image": {},
    "guarantor1_aadhar_card": {
        "address": "  sh",
        "father_s_husband_s_name": "S/O Shri Asharfi Lal Mehto",
        "age": "34",
        "country": "India",
        "dob_yob": "1981",
        "pincode": "110091",
        "district": "East Delhi",
        "name": "Pramod Kumar",
        "state": "Delhi",
        "taluk": "East Vinod Nagar",
        "mobile_number": "",
        "phone_number": ""
    },
    "applicant_aadhar_card": {
        "address": "near bus stand  ",
        "father_s_husband_s_name": "S/O Fyroz Basha",
        "age": "23",
        "country": "India",
        "dob_yob": "1992",
        "pincode": "516257",
        "district": "Cuddapah",
        "name": "Pattan Saddam Hussain",
        "state": "Andhra Pradesh",
        "taluk": "Lakkireddipalle",
        "mobile_number": "",
        "phone_number": "14"
    },
    "applicant_other_form_hypo_goods_image": {},
    "guarantor2_aadhar_card": {
        "address": "  sh",
        "father_s_husband_s_name": "S/O Ganpat Singh",
        "age": "27",
        "country": "India",
        "dob_yob": "1988",
        "pincode": "332027",
        "district": "Sikar",
        "name": "Vijender Singh",
        "state": "Rajasthan",
        "taluk": "Singhasan",
        "mobile_number": "",
        "phone_number": ""
    }
}

headers = {
  'content-type': "application/json"
}

response = requests.post(url, json=payload, params=querystring)
print(response.text)