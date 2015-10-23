import json
import requests

url = "http://localhost:8080/api/organisation/applications"

querystring = {
    "instance_token":"NFdTXRJvmrgCd4Zt5CLrWul9OrWhhunh62s2aS9Lf2A"
}

payload = {
    "applicant_other_card_land_details": {
        "estimated_resale_value_of_property": "",
        "loan_outstanding_against_such_property": "",
        "land_description": "d"
    },
    "applicant_family_details_other_assets": {
        "family_other_assets": "Flat/ House on rent, Bike, Tractor, Van"
    },
    "assets_id": "67bd3320-e690-48f8-b906-8cab82fb9636",
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
        "occupation": "",
        "state": "Andhra Pradesh",
        "taluk": "Lakkireddipalle",
        "voter_id_father_s_husband_s_name": "",
        "voter_id": "",
        "email_id": "",
        "permanent_address": "",
        "pan_card_id": "",
        "phone_number": "",
        "father_s_husband_s_name": "S/O Fyroz Basha",
        "age": "23",
        "country": "India",
        "district": "Cuddapah",
        "name": "Pattan Saddam Hussainu",
        "uid": "565061987998",
        "voter_id_name": "",
        "type": "AADHAAR",
        "mobile_number": ""
    },
    "assets_map": {
        "guarantor1": {
            "aadhar_card": [
                "67bd3320-e690-48f8-b906-8cab82fb9636/guarantor1_aadhar_card__aadhaar card_0.jpg",
                "67bd3320-e690-48f8-b906-8cab82fb9636/guarantor1_aadhar_card__aadhaar card_1.jpg",
                "67bd3320-e690-48f8-b906-8cab82fb9636/guarantor1_aadhar_card__aadhaar card_0.jpg",
                "67bd3320-e690-48f8-b906-8cab82fb9636/guarantor1_aadhar_card__aadhaar card_1.jpg"
            ]
        },
        "guarantor2": {
            "aadhar_card": [
                "67bd3320-e690-48f8-b906-8cab82fb9636/guarantor2_aadhar_card__aadhaar card_0.jpg",
                "67bd3320-e690-48f8-b906-8cab82fb9636/guarantor2_aadhar_card__aadhaar card_1.jpg"
            ]
        },
        "applicant": {
            "aadhar_card": [
                "67bd3320-e690-48f8-b906-8cab82fb9636/applicant_aadhar_card__aadhaar card_0.jpg",
                "67bd3320-e690-48f8-b906-8cab82fb9636/applicant_aadhar_card__aadhaar card_1.jpg"
            ]
        }
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
        "name_of_borrower": "s",
        "loan_amount": ""
    },
    "applicant_other_card_electricity_details": {
        "electricity_monthly_bill": "",
        "power_supplier": ""
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
    "applicant_other_card_bank_details2": {
        "bank_name": "",
        "branch_ifsc_code": "",
        "account_number": "",
        "account_holder_name": "",
        "bank_branch": "",
        "account_operational_since": "",
        "bank_account_type": "Saving",
    },
    "guarantor1_kyc_details": {
        "address": ", .   Singhasan",
        "dob_yob": "1988",
        "pan_card_father_s_husband_s_name": "",
        "pincode": "332027",
        "pan_card_name": "",
        "occupation": "",
        "state": "Rajasthan",
        "taluk": "Singhasan",
        "voter_id_father_s_husband_s_name": "",
        "voter_id": "",
        "email_id": "",
        "permanent_address": "",
        "pan_card_id": "",
        "phone_number": "",
        "father_s_husband_s_name": "S/O Ganpat Singh",
        "age": "27",
        "country": "India",
        "district": "Sikar",
        "name": "Vijender Singh",
        "uid": "337972036560",
        "voter_id_name": "",
        "type": "AADHAAR",
        "mobile_number": ""
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
            "lat": 23.00233934,
            "lng": 72.53279684
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
        "nominee_phone": "",
        "nominee_age": "",
        "nominee_name": "",
        "nominee_gender": "Male"
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
    "applicant_other_card_credit_card_details": {
        "issue_bank": "",
        "card_no": ""
    },
    "applicant_other_card_liabilities": {
        "liabilities_chits": "",
        "liabilities_friends__family_hand_loans": "",
        "liabilities_insurance": "",
        "liabilities_bank_loans": ""
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
    "applicant_personal_docs": {
        "marital_status": "Married",
        "religion": "Hindu",
        "physical_disability": "Partial",
        "education": "Upto Primary",
        "gender": "Male",
        "category": "General"
    },
    "applicant_loan_details_applied_loan": {
        "repayment_option": "Weekly",
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
    "applicant_family_details_assets": {
        "monthly_rent": "",
        "family_assets_land_acres": "",
        "family_assets_orchard__acres": "",
        "family_assets_number_of_rented_shops_or_godowns": "",
        "family_assets_number_of_rented_houses_or_flats": "",
        "how_long_are_you_staying_in_house__in_years": "",
        "quality_of_house": "Pakka/Concrete",
        "rent_agreement": "Yes",
        "type_of_house": ""
    },
    "guarantor1_other_card_details1": {
        "bank_credit_co_perative_society": "",
        "name_of_borrower": "d",
        "loan_amount": ""
    },
    "guarantor2_kyc_details": {
        "address": "E-387, GALI N0-8.   Patparganj",
        "dob_yob": "1981",
        "pan_card_father_s_husband_s_name": "",
        "pincode": "110091",
        "pan_card_name": "",
        "occupation": "",
        "state": "Delhi",
        "taluk": "East Vinod Nagar",
        "voter_id_father_s_husband_s_name": "",
        "voter_id": "",
        "email_id": "",
        "permanent_address": "",
        "pan_card_id": "",
        "phone_number": "",
        "father_s_husband_s_name": "S/O Shri Asharfi Lal Mehto",
        "age": "34",
        "country": "India",
        "district": "East Delhi",
        "name": "Pramod Kumar",
        "uid": "729348086056",
        "voter_id_name": "",
        "type": "AADHAAR",
        "mobile_number": ""
    },
    "product": ""
}

headers = {
  'content-type': "application/json"
}

response = requests.post(url, json=payload, params=querystring)
print(response.text)