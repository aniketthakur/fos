import json
import requests

url = "http://localhost:8080/mobile/application/json"

querystring = {
  "instance_token":"ChADpwltz-mp-WkS0VIVyt8dP0Xtvac8Ee8ZY1lsPIg"
}

payload = {
    "assets_id": "02973f8d-3c85-44a3-826e-821506475014",
    "applicant_other_info": {
        "2nd_asset_for_hypothecation": "None",
        "3rd_asset_for_hypothecation": "None",
        "asset_for_hypothecation___purchase_year": "36",
        "asset_for_hypothecation___purchase_price": "365",
        "asset_for_hypothecation___purchase_purpose": "Thf",
        "asset_for_hypothecation___current_market_value": "698",
        "asset_for_hypothecation___details_of_hypothecated_goods": "Ggh",
        "nominee_name": "Ahvz",
        "nominee_gender": "Male",
        "nominee_age": "6797",
        "nominee_phone": "9797797997",
        "nominee_relationship_with_borrower": "Spouse",
        "primary_business_category": "Trading",
        "primary_business_activities": "Sc",
        "primary_business_seasonality": "Yearly",
        "primary_business_income_monthly": "45",
        "primary_business___premise": "Own Premise",
        "primary_business___number_of_employees": "5",
        "primary_business_expenditure___admin": "59",
        "primary_business_expenditure___rent": "59",
        "primary_business_expenditure___other_expenses": "44",
        "primary_business_expenditure___employee_salary": "23",
        "primary_business_expenditure___working_capital": "41",
        "primary_business___number_of_years_in_business": "58",
        "family_travel_expenditure__monthly": "6",
        "family_festival_expenditure_monthly": "58",
        "family_education_expenditure_monthly": "48",
        "family_assets_land_acres": "5",
        "family_assets_orchard__acres": "58",
        "family_food_expenditure__monthly": "2",
        "family_other_expenditure_monthly": "33",
        "family_assets_number_of_rented_houses_or_flats": "4",
        "family_assets_number_of_rented_shops_or_godowns": "5",
        "family_entertainment_expenditure__monthly": "25",
        "financial_liabilities_chits": "25",
        "account_number": "55555555555555555",
        "total_earning_members": "15",
        "repayment_option": "Fortnightly",
        "account_holder_name": "Gh",
        "female_count": "12",
        "secondary_business_category": "None",
        "tertiary_business_category": "None",
        "marital_status": "Married",
        "male_count": "15",
        "required_loan_amount": "25",
        "other_family_asset_s": "Flat/ House on rent, Car, Tractor, Van",
        "gender": "Male",
        "quality_of_house": "Kaccha/Mud",
        "members_above_18": "14",
        "members_less_than_18": "13",
        "category": "OBC",
        "education": "Post Graduate",
        "financial_liabilities_insurance": "98",
        "financial_liabilities_bank_loans": "41",
        "financial_liabilities_friends__family_hand_loans": "32",
        "psychometric_test_q1": "Answer 4.",
        "psychometric_test_q2": "Answer 3.",
        "psychometric_test_q3": "Answer 2.",
        "psychometric_test_q4": "Answer 1.",
        "psychometric_test_q5": "Answer 1.",
        "psychometric_test_q6": "Answer 2.",
        "psychometric_test_q7": "Answer 3.",
        "psychometric_test_q8": "Answer 4.",
        "psychometric_test_q9": "Answer 4.",
        "psychometric_test_q10": "Answer 3.",
        "bank_name": "Gf",
        "ifsc_code": "gfvhuhcdd",
        "family_medical_expenditure_monthly": "66",
        "how_long_are_you_staying_in_house__in_years": "4",
        "purpose_of_the_loan": "Rg",
        "total_number_of_family_members": "1",
        "physical_disability_member": "None",
        "religion": "Jain",
        "type_of_house": "Self Owned",
    },
    "applicant_other_form_hypo_docs_image": {},
    "guarantor1_aadhar_card": {
        "uid" : "gid1",
        "type" : "aadhaar",
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
        "uid" : "uid1",
        "type" : "aadhaar",
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
        "uid" : "gid2",
        "type" : "aadhaar",
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

payload = {"appId":"02973f8d-3c85-44a3-826e-821506475014","applicant_other_info":{"psychometric_test_q2":"Answer 3.","2nd_asset_for_hypothecation":"None","asset_for_hypothecation___current_market_value":"698","nominee_name":"Ahvz","nominee_gender":"Male","psychometric_test_q4":"Answer 1.","psychometric_test_q9":"Answer 4.","family_travel_expenditure__monthly":"6","primary_business_activities":"Sc","financial_liabilities_chits":"25","asset_for_hypothecation___details_of_hypothecated_goods":"Ggh","account_number":"55555555555555555","total_earning_members":"15","repayment_option":"Fortnightly","account_holder_name":"Gh","family_festival_expenditure_monthly":"58","nominee_age":"6797","female_count":"12","secondary_business_category":"None","asset_for_hypothecation___purchase_purpose":"Thf","financial_liabilities_bank_loans":"41","nominee_phone":"9797797997","marital_status":"Married","asset_for_hypothecation___purchase_price":"365","nominee_relationship_with_borrower":"Spouse","male_count":"15","financial_liabilities_insurance":"98","psychometric_test_q7":"Answer 3.","primary_business_expenditure___employee_salary":"23","family_education_expenditure_monthly":"48","members_less_than_18":"13","primary_business___premise":"Own Premise","psychometric_test_q6":"Answer 2.","required_loan_amount":"25","primary_business_expenditure___admin":"59","primary_business___number_of_employees":"5","other_family_asset_s":"Flat\/ House on rent, Car, Tractor, Van","psychometric_test_q1":"Answer 4.","tertiary_business_category":"None","primary_business_income_monthly":"45","family_assets_orchard__acres":"58","psychometric_test_q5":"Answer 1.","family_entertainment_expenditure__monthly":"25","asset_for_hypothecation___purchase_year":"36","primary_business_seasonality":"Yearly","family_assets_number_of_rented_shops_or_godowns":"5","family_assets_number_of_rented_houses_or_flats":"4","gender":"Male","quality_of_house":"Kaccha\/Mud","family_other_expenditure_monthly":"33","members_above_18":"14","category":"OBC","family_food_expenditure__monthly":"2","3rd_asset_for_hypothecation":"None","education":"Post Graduate","psychometric_test_q10":"Answer 3.","primary_business_expenditure___working_capital":"41","primary_business_category":"Trading","financial_liabilities_friends__family_hand_loans":"32","primary_business___number_of_years_in_business":"58","psychometric_test_q3":"Answer 2.","family_assets_land_acres":"5","bank_name":"Gf","ifsc_code":"gfvhuhcdd","family_medical_expenditure_monthly":"66","primary_business_expenditure___other_expenses":"44","how_long_are_you_staying_in_house__in_years":"4","purpose_of_the_loan":"Rg","total_number_of_family_members":"1","physical_disability_member":"None","primary_business_expenditure___rent":"59","religion":"Jain","type_of_house":"Self Owned","psychometric_test_q8":"Answer 4."},"applicant_other_form_hypo_docs_image":{},"guarantor1_aadhar_card":{"address":"  sh","father_s_husband_s_name":"S\/O Shri Asharfi Lal Mehto","age":"34","country":"India","dob_yob":"1981","pincode":"110091","district":"East Delhi","name":"Pramod Kumar","state":"Delhi","taluk":"East Vinod Nagar","mobile_number":"","phone_number":""},"applicant_aadhar_card":{"address":"near bus stand  ","father_s_husband_s_name":"S\/O Fyroz Basha","age":"23","country":"India","dob_yob":"1992","pincode":"516257","district":"Cuddapah","name":"Pattan Saddam Hussain","state":"Andhra Pradesh","taluk":"Lakkireddipalle","mobile_number":"","phone_number":"14"},"applicant_other_form_hypo_goods_image":{},"guarantor2_aadhar_card":{"address":"  sh","father_s_husband_s_name":"S\/O Ganpat Singh","age":"27","country":"India","dob_yob":"1988","pincode":"332027","district":"Sikar","name":"Vijender Singh","state":"Rajasthan","taluk":"Singhasan","mobile_number":"","phone_number":""}}

payload = {"assets_id":"0d3e0500-0069-497a-a25a-6a2a882bc778","applicant_other_info":{"psychometric_test_q2":"Answer 3.","2nd_asset_for_hypothecation":"None","asset_for_hypothecation___current_market_value":"55744","nominee_name":"None","nominee_gender":"None","psychometric_test_q4":"Answer 1.","psychometric_test_q9":"Answer 4.","family_travel_expenditure__monthly":"8","primary_business_activities":"A","financial_liabilities_chits":"7","asset_for_hypothecation___details_of_hypothecated_goods":"Ggg","account_number":"555","total_earning_members":"None","repayment_option":"Fortnightly","account_holder_name":"Ggg","family_festival_expenditure_monthly":"3","nominee_age":"None","female_count":"None","secondary_business_category":"None","asset_for_hypothecation___purchase_purpose":"Ghh","financial_liabilities_bank_loans":"1","nominee_phone":"None","marital_status":"Widow","asset_for_hypothecation___purchase_price":"6669","nominee_relationship_with_borrower":"Son","male_count":"None","financial_liabilities_insurance":"9","psychometric_test_q7":"Answer 3.","primary_business_expenditure___employee_salary":"33","family_education_expenditure_monthly":"5","members_less_than_18":"None","primary_business___premise":"Own Premise","psychometric_test_q6":"Answer 2.","required_loan_amount":"5","primary_business_expenditure___admin":"69","primary_business___number_of_employees":"74","other_family_asset_s":"Investment Fix Deposit, Flat\/ House on rent, Car, Tractor, TV","psychometric_test_q1":"Answer 4.","tertiary_business_category":"None","primary_business_income_monthly":"8","family_assets_orchard__acres":"7","psychometric_test_q5":"Answer 1.","family_entertainment_expenditure__monthly":"66","asset_for_hypothecation___purchase_year":"255","primary_business_seasonality":"Yearly","family_assets_number_of_rented_shops_or_godowns":"3","family_assets_number_of_rented_houses_or_flats":"5","gender":"Female","quality_of_house":"Semi\/Pakka","family_other_expenditure_monthly":"6","members_above_18":"None","category":"SC\/ST","family_food_expenditure__monthly":"4","3rd_asset_for_hypothecation":"None","education":"Higher Secondary\/PU","psychometric_test_q10":"Answer 3.","primary_business_expenditure___working_capital":"58","primary_business_category":"Trading","financial_liabilities_friends__family_hand_loans":"2","primary_business___number_of_years_in_business":"85","psychometric_test_q3":"Answer 2.","family_assets_land_acres":"58","bank_name":"Fff","ifsc_code":"fggb","family_medical_expenditure_monthly":"2","primary_business_expenditure___other_expenses":"4","how_long_are_you_staying_in_house__in_years":"4","purpose_of_the_loan":"F","total_number_of_family_members":"None","physical_disability_member":"Partial","primary_business_expenditure___rent":"48","religion":"Hindu","type_of_house":"Rented\/Leased","psychometric_test_q8":"Answer 4."},"applicant_other_form_hypo_docs_image":{},"guarantor1_aadhar_card":{"address":"E-387, GALI N0-8.   Patparganj","dob_yob":"19815","pincode":"110091","state":"Delhi","taluk":"East Vinod Nagar","phone_number":"","father_s_husband_s_name":"S\/O Shri Asharfi Lal Mehto","age":"34","country":"India","district":"East Delhi","name":"Pramod Kumar","uid":"729348086056","type":"None","mobile_number":""},"applicant_aadhar_card":{"address":"E-387, GALI N0-8.   Patparganjg","dob_yob":"1981","pincode":"110091","state":"Delhi","taluk":"East Vinod Nagar","phone_number":"","father_s_husband_s_name":"S\/O Shri Asharfi Lal Mehto","age":"34","country":"India","district":"East Delhi","name":"Pramod Kumar","uid":"729348086056","type":"None","mobile_number":""},"applicant_other_form_hypo_goods_image":{},"guarantor2_aadhar_card":{"address":", .   Singhasan","dob_yob":"1988","pincode":"332027","state":"Rajasthan","taluk":"Singhasan","phone_number":"","father_s_husband_s_name":"S\/O Ganpat Singh","age":"27","country":"India","district":"Sikar","name":"Vijender Singh","uid":"337972036560","type":"None","mobile_number":"58888"}}

payload = {"assets_id":"0d3e0500-0069-497a-a25a-6a2a882bc778","applicant_other_info":{"psychometric_test_q2":"Answer 3.","2nd_asset_for_hypothecation":"None","asset_for_hypothecation___current_market_value":"55744","nominee_name":"None","nominee_gender":"None","psychometric_test_q4":"Answer 1.","psychometric_test_q9":"Answer 4.","family_travel_expenditure__monthly":"8","primary_business_activities":"A","financial_liabilities_chits":"7","asset_for_hypothecation___details_of_hypothecated_goods":"Ggg","account_number":"555","total_earning_members":"None","repayment_option":"Fortnightly","account_holder_name":"Ggg","family_festival_expenditure_monthly":"3","nominee_age":"None","female_count":"None","secondary_business_category":"None","asset_for_hypothecation___purchase_purpose":"Ghh","financial_liabilities_bank_loans":"1","nominee_phone":"None","marital_status":"Widow","asset_for_hypothecation___purchase_price":"6669","nominee_relationship_with_borrower":"Son","male_count":"None","financial_liabilities_insurance":"9","psychometric_test_q7":"Answer 3.","primary_business_expenditure___employee_salary":"33","family_education_expenditure_monthly":"5","members_less_than_18":"None","primary_business___premise":"Own Premise","psychometric_test_q6":"Answer 2.","required_loan_amount":"5","primary_business_expenditure___admin":"69","primary_business___number_of_employees":"74","other_family_asset_s":"Investment Fix Deposit, Flat\/ House on rent, Car, Tractor, TV","psychometric_test_q1":"Answer 4.","tertiary_business_category":"None","primary_business_income_monthly":"8","family_assets_orchard__acres":"7","psychometric_test_q5":"Answer 1.","family_entertainment_expenditure__monthly":"66","asset_for_hypothecation___purchase_year":"255","primary_business_seasonality":"Yearly","family_assets_number_of_rented_shops_or_godowns":"3","family_assets_number_of_rented_houses_or_flats":"5","gender":"Female","quality_of_house":"Semi\/Pakka","family_other_expenditure_monthly":"6","members_above_18":"None","category":"SC\/ST","family_food_expenditure__monthly":"4","3rd_asset_for_hypothecation":"None","education":"Higher Secondary\/PU","psychometric_test_q10":"Answer 3.","primary_business_expenditure___working_capital":"58","primary_business_category":"Trading","financial_liabilities_friends__family_hand_loans":"2","primary_business___number_of_years_in_business":"85","psychometric_test_q3":"Answer 2.","family_assets_land_acres":"58","bank_name":"Fff","ifsc_code":"fggb","family_medical_expenditure_monthly":"2","primary_business_expenditure___other_expenses":"4","how_long_are_you_staying_in_house__in_years":"4","purpose_of_the_loan":"F","total_number_of_family_members":"None","physical_disability_member":"Partial","primary_business_expenditure___rent":"48","religion":"Hindu","type_of_house":"Rented\/Leased","psychometric_test_q8":"Answer 4."},"applicant_other_form_hypo_docs_image":{},"guarantor1_aadhar_card":{"address":"E-387, GALI N0-8.   Patparganj","dob_yob":"19815","pincode":"110091","state":"Delhi","taluk":"East Vinod Nagar","phone_number":"","father_s_husband_s_name":"S\/O Shri Asharfi Lal Mehto","age":"34","country":"India","district":"East Delhi","name":"Pramod Kumar","uid":"729348086056","type":"None","mobile_number":""},"applicant_aadhar_card":{"address":"E-387, GALI N0-8.   Patparganjg","dob_yob":"1981","pincode":"110091","state":"Delhi","taluk":"East Vinod Nagar","phone_number":"","father_s_husband_s_name":"S\/O Shri Asharfi Lal Mehto","age":"34","country":"India","district":"East Delhi","name":"Pramod Kumar","uid":"729348086056","type":"None","mobile_number":""},"applicant_other_form_hypo_goods_image":{},"guarantor2_aadhar_card":{"address":", .   Singhasan","dob_yob":"1988","pincode":"332027","state":"Rajasthan","taluk":"Singhasan","phone_number":"","father_s_husband_s_name":"S\/O Ganpat Singh","age":"27","country":"India","district":"Sikar","name":"Vijender Singh","uid":"337972036560","type":"None","mobile_number":"58888"}}

payload = {"assets_id":"0d3e0500-0069-497a-a25a-6a2a882bc778","applicant_other_info":{"psychometric_test_q2":"Answer 3.","2nd_asset_for_hypothecation":"None","asset_for_hypothecation___current_market_value":"55744","nominee_name":"None","nominee_gender":"None","psychometric_test_q4":"Answer 1.","psychometric_test_q9":"Answer 4.","family_travel_expenditure__monthly":"8","primary_business_activities":"A","financial_liabilities_chits":"7","asset_for_hypothecation___details_of_hypothecated_goods":"Ggg","account_number":"555","total_earning_members":"None","repayment_option":"Fortnightly","account_holder_name":"Ggg","family_festival_expenditure_monthly":"3","nominee_age":"None","female_count":"None","secondary_business_category":"None","asset_for_hypothecation___purchase_purpose":"Ghh","financial_liabilities_bank_loans":"1","nominee_phone":"None","marital_status":"Widow","asset_for_hypothecation___purchase_price":"6669","nominee_relationship_with_borrower":"Son","male_count":"None","financial_liabilities_insurance":"9","psychometric_test_q7":"Answer 3.","primary_business_expenditure___employee_salary":"33","family_education_expenditure_monthly":"5","members_less_than_18":"None","primary_business___premise":"Own Premise","psychometric_test_q6":"Answer 2.","required_loan_amount":"5","primary_business_expenditure___admin":"69","primary_business___number_of_employees":"74","other_family_asset_s":"Investment Fix Deposit, Flat\/ House on rent, Car, Tractor, TV","psychometric_test_q1":"Answer 4.","tertiary_business_category":"None","primary_business_income_monthly":"8","family_assets_orchard__acres":"7","psychometric_test_q5":"Answer 1.","family_entertainment_expenditure__monthly":"66","asset_for_hypothecation___purchase_year":"255","primary_business_seasonality":"Yearly","family_assets_number_of_rented_shops_or_godowns":"3","family_assets_number_of_rented_houses_or_flats":"5","gender":"Female","quality_of_house":"Semi\/Pakka","family_other_expenditure_monthly":"6","members_above_18":"None","category":"SC\/ST","family_food_expenditure__monthly":"4","3rd_asset_for_hypothecation":"None","education":"Higher Secondary\/PU","psychometric_test_q10":"Answer 3.","primary_business_expenditure___working_capital":"58","primary_business_category":"Trading","financial_liabilities_friends__family_hand_loans":"2","primary_business___number_of_years_in_business":"85","psychometric_test_q3":"Answer 2.","family_assets_land_acres":"58","bank_name":"Fff","ifsc_code":"fggb","family_medical_expenditure_monthly":"2","primary_business_expenditure___other_expenses":"4","how_long_are_you_staying_in_house__in_years":"4","purpose_of_the_loan":"F","total_number_of_family_members":"None","physical_disability_member":"Partial","primary_business_expenditure___rent":"48","religion":"Hindu","type_of_house":"Rented\/Leased","psychometric_test_q8":"Answer 4."},"applicant_other_form_hypo_docs_image":{},"guarantor1_aadhar_card":{"address":"E-387, GALI N0-8.   Patparganj","dob_yob":"19815","pincode":"110091","state":"Delhi","taluk":"East Vinod Nagar","phone_number":"","father_s_husband_s_name":"S\/O Shri Asharfi Lal Mehto","age":"34","country":"India","district":"East Delhi","name":"Pramod Kumar","uid":"729348086056","type":"None","mobile_number":""},"applicant_aadhar_card":{"address":"E-387, GALI N0-8.   Patparganjg","dob_yob":"1981","pincode":"110091","state":"Delhi","taluk":"East Vinod Nagar","phone_number":"","father_s_husband_s_name":"S\/O Shri Asharfi Lal Mehto","age":"34","country":"India","district":"East Delhi","name":"Pramod Kumar","uid":"729348086056","type":"None","mobile_number":""},"applicant_other_form_hypo_goods_image":{},"guarantor2_aadhar_card":{"address":", .   Singhasan","dob_yob":"1988","pincode":"332027","state":"Rajasthan","taluk":"Singhasan","phone_number":"","father_s_husband_s_name":"S\/O Ganpat Singh","age":"27","country":"India","district":"Sikar","name":"Vijender Singh","uid":"337972036560","type":"None","mobile_number":"58888"}}

pay = {
    u'quality_of_house': u'None',
    u'how_long_are_you_staying_in_house__in_years': u'46795',
    u'primary_business_category': u'Labour',
    u'physical_disability_member': u'None',
    u'financial_liabilities_bank_loans': u'66',
    u'family_assets_land_acres': u'2154',
    u'specify_category': u'Njj',
    u'primary_business_activities': u'Ubx',
    u'total_earning_members': None,
    u'family_assets_number_of_rented_houses_or_flats': u'2225',
    u'family_entertainment_expenditure__monthly': u'9',
    u'required_loan_amount': u'3',
    u'family_travel_expenditure__monthly': u'64',
    u'primary_business_income_monthly': u'67',
    u'repayment_option': u'Fortnightly',
    u'education': u'UptoPrimary',
    u'tertiary_business_category': u'None',
    u'category': u'Others',
    u'primary_asset_for_hypothecation___purchase_price': u'1346',
    u'secondary_asset_for_hypothecation': u'None',
    u'financial_liabilities_insurance': u'697',
    u'nominee_name': None,
    u'financial_liabilities_friends__family_hand_loans': u'346',
    u'primary_asset_for_hypothecation___purchase_purpose': u'Jajaj',
    u'nominee_gender': None,
    u'family_medical_expenditure_monthly': u'364',
    u'family_other_expenditure_monthly': u'3164',
    u'ifsc_code': None,
    u'religion': u'Others',
    u'nominee_relationship_with_borrower': u'None',
    u'primary_business___premise': u'LeasedPremise',
    u'nominee_phone': None,
    u'bank_name': None,
    u'financial_liabilities_chits': u'6497',
    u'family_education_expenditure_monthly': u'364337',
    u'family_assets_orchard__acres': u'5487',
    u'nominee_age': None,
    u'primary_asset_for_hypothecation___details_of_hypothecated_goods': u'JajJ',
    u'primary_business_expenditure___employee_salary': u'164',
    u'account_holder_name': None,
    u'male_count': None,
    u'primary_asset_for_hypothecation___current_market_value': u'3134',
    u'primary_business_expenditure___other_expenses': u'964',
    u'primary_business_expenditure___working_capital': u'641',
    u'female_count': None,
    u'family_assets_number_of_rented_shops_or_godowns': u'6598',
    u'primary_business_expenditure___admin': u'497',
    u'secondary_business_category': u'None',
    u'primary_business_seasonality': u'Others',
    u'primary_business___number_of_employees': u'596',
    u'total_number_of_family_members': None,
    u'tertiary_asset_for_hypothecation': u'None',
    u'other_family_asset_s': u'Flat/Houseonrent, Bike, Car, Tractor, Van, TV',
    u'primary_asset_for_hypothecation___purchase_year': u'43676',
    u'members_less_than_18': None,
    u'marital_status': u'Married',
    u'family_festival_expenditure_monthly': u'6',
    u'members_above_18': None,
    u'primary_business_expenditure___rent': u'1479',
    u'type_of_house': u'None',
    u'account_number': None,
    u'gender': u'Other',
    u'family_food_expenditure__monthly': u'4764587',
    u'purpose_of_the_loan': u'Hb',
    u'primary_business___number_of_years_in_business': u'1346'
}

payload = {"assets_id":"ab22d3e5-3473-4b35-bbf0-16ce0da8e533","business_lng":77.4004362,"business_lat":28.5857611,"applicant_other_info":{},"guarantor1_aadhar_card":{"address":"4\/166, . near bus stand  ","dob_yob":"1992","pincode":"516257","state":"Andhra Pradesh","taluk":"Lakkireddipalle","phone_number":"","father_s_husband_s_name":"S\/O Fyroz Basha","age":"23","country":"India","district":"Cuddapah","name":"Pattan Saddam Hussain","uid":"565061987998","type":"AADHAAR","mobile_number":"8"},"applicant_aadhar_card":{"address":", . zakariya house,zakariya colony,3\/103 dargha mohalla Asind","dob_yob":"1984","pincode":"311301","state":"Rajasthan","taluk":"Asind","phone_number":"","father_s_husband_s_name":"S\/O Shabbir Mohammad Chhipa","age":"31","country":"India","district":"Bhilwara","name":"Arif Mohammad Chhipa","uid":"968354673454","type":"AADHAAR","mobile_number":"8"},"guarantor2_aadhar_card":{"address":"E-387, GALI N0-8.   Patparganj","dob_yob":"1981","pincode":"110091","state":"Delhi","taluk":"East Vinod Nagar","phone_number":"","father_s_husband_s_name":"S\/O Shri Asharfi Lal Mehto","age":"34","country":"India","district":"East Delhi","name":"Pramod Kumar","uid":"729348086056","type":"AADHAAR","mobile_number":"8"},"assets_map":{"guarantor1":{},"guarantor2":{},"applicant":{"pan_card":["ab22d3e5-3473-4b35-bbf0-16ce0da8e533\/applicant_pan_card_1.jpg"],"voter_card":["ab22d3e5-3473-4b35-bbf0-16ce0da8e533\/applicant_voter_card_0.jpg","ab22d3e5-3473-4b35-bbf0-16ce0da8e533\/applicant_voter_card_1.jpg"]}}}

headers = {
  'content-type': "application/json"
}

response = requests.post(url, json=payload, params=querystring)
print(response.text)