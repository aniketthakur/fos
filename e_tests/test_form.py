import json
import requests,sys

# url = "http://%s/api/app_token/generate" % ("localhost:8080")
# payload = {"email": "demo@fos-test.esthenos.com", "password":"demodemo"}
# response = requests.post(url, data=payload)
# print response.text
# sys.exit(0)

url = "http://localhost:8080/api/organisation/applications"

querystring = {
    "instance_token":"0MXwdcivD_QfawQ6vFbj_djYMVzb_CpzTtLH0P5mRbY"
}

payload = {
    "group": "",
    "applicant_business_docs_customer1":{   
        "address": "hdhddhh", #[All other are Customer Details from 1 to 5]
        "name_4": "hdhdhr",
        "name_3": "hdhdhdhdj",
        "address_5": "hdhdhr",
        "name_2": "ndndnhdh",
        "name_5": "hdhdhd",
        "telephone_no_4": "84848488454",
        "address_4": "hdhdhrh",
        "address_2": "hdhdhdh",
        "institution_credit": "30 days",#(This Field is from page "Business info:Details of Key Customers")
        "telephone_no_3": "84848484884",
        "address_3": "hdhdhrh",
        "telephone_no_2": "87878787878",
        "name": "ududuru",
        "individual_credit_": "15 days",#(This Field is from page "Business info:Details of Key Customers")
        "telephone_no_5": "84848488484",
        "telephone_no": "87878789797"
    },
    "applicant_other_card_sales_info": {             #  [NEW PAGE]
        "sales_revenue_in_1_month": "100000",
        "sales_revenue_in_5_month": "1000",
        "sales_revenue_in_4_month": "10000",
        "sales_revenue_in_3_month": "10000",
        "sales_revenue_in_10_month": "10000",
        "sales_revenue_in_12_month": "10000",
        "sales_revenue_in_8_month": "1000",
       "total_annual_revenue_credit": "250000",
       "sales_revenue_in_7_month": "10000",
       "sales_revenue_in_6_month": "1000",
        "sales_revenue_in_9_month": "10000",
       "total_annual_revenue_cash": "250000",
       "sales_revenue_in_2_month": "10000",
        "sales_revenue_in_11_month": "10000"
    },
    "applicant_other_card_type_equipment3":{           # [NEW PAGE]
        "estimated_value": "55000",
        "is_equipment_given_as_collateral__dropdown_with_values": "No",
        "date_of_manufacturing_equipment": "duurur",
        "details_of_equipment_supplier": "hfuru"
    },
     "applicant_family_details_details3": {   #[NEW PAGE]
         "aadhar_number": "245454564646",
         "name": "dhhdj",
         "education": "Jdjdj",
         "occupations_details": "Hdjdjj",
         "age": "27",
         "annual_income": "57548",
         "relation": "Udhdjd"
     },
    "applicant_nominee_details": {
        "nominee_relation": "Father",
        "nominee_phone": "7887548454",
        "nominee_age": "27",
        "nominee_name": "hdhdh",
        "nominee_gender": "Male"
    },
    "timeslot": {     
        "time": "",
        "day": ""
    },
    "guarantor1_other_card_details2": {  
        "bank_credit_co_perative_society": "uruur",
        "name_of_borrower": "hduru",
        "loan_amount": "5454"
    },
    "applicant_other_card_electricity_details": {
        "electricity_monthly_bill": "2000",
        "power_supplier": "Tata Power"
    },
    "applicant_other_card_emp_business_info": {   #  [EXCEPT NEW FIELDS ALL OTHER ARE FROM "BUSINESS INFO:OTHER DETAILS" PAGE]
        "permanent_employees": "5454",
        "average_monthly_wage_for_relatives": "5455", #	[ ADD ]
        "relatives_in_business": "5548",
        "wages_paid": "Monthly",                                  
        "average_monthly_wage_for_contract_employees": "5454",	 #[ ADD ]
        "contract_employees": "5155",
        "average_monthly_wage_for_permanent_employees": "54545"	#[ ADD ]
    },
    "applicant_other_card_bank_details2": {
        "bank_name": "hdjrj",
        "account_holder_name": "ururuu",
        "bank_branch": "hrjruu",
        "branch_ifsc_code": "hdhrhjrj",
        "account_operational_since": "12-3-2014",
        "bank_account_type": "Saving",
        "account_number": "54545545"
    },
     "applicant_other_card_land_details1": {  #[NEW PAGE]
         "land_location": "unjhdhd",	#[ ADD ]
         "type_of_property": "Residential", #[ ADD ]
         "area_in_sqft": "2800",		#[ ADD ]
         "estimated_resale_value": "58180",
         "loan_outstanding": "200000"
     },
    "guarantor1_other_card_details3": {
        "bank_credit_co_perative_society": "his",
        "name_of_borrower": "uruurur",
        "loan_amount": "585"
    },
    "applicant_other_card_bank_details1": {
        "bank_name": "hdhfh",
        "account_holder_name": "udhrhj",
        "bank_branch": "hdudu",
        "branch_ifsc_code": "hdjdjdjdj",
        "account_operational_since": "12-3-2014",
        "bank_account_type": "Saving",
        "account_number": "5784848848"
    },
     "applicant_family_details_details1":  {   #[NEW PAGE]
         "aadhar_number": "845464664646",
         "name": "Reshma",
         "education": "HSC",
         "occupations_details": "Housewife",
         "age": "24",
         "annual_income": "0",
         "relation": "WIFE"
     },
    "applicant_hypothecation_goods_details3": {
        "purchase_purpose": "Uh",
        "market_value": "54545",
        "goods_details": "Dhfh",
        "purchase_year": "85",
        "purchase_price": "588",
        "goods_image": "",
        "goods_docs_image": ""
    },
     "applicant_other_card_land_details3": {     #[NEW PAGE]
         "land_location": "uuueu",		#[ ADD ]
         "type_of_property": "Residential",	#[ ADD ]
         "area_in_sqft": "548",			#[ ADD ]
         "estimated_resale_value": "2000",
         "loan_outstanding": "5500"
     },
    "applicant_other_card_bank_details4": {
        "bank_name": "udurjj",
        "account_holder_name": "jdhrhhrj",
        "bank_branch": "udurhu",
        "branch_ifsc_code": "jdjrjrj",
        "account_operational_since": "12-3-2014",
        "bank_account_type": "Saving",
        "account_number": "8784848845"
    },
     "applicant_family_expenditure": {		#[NEW PAGE]
         "education_expenses": "500",
         "medical_expenses": "500",
         "grocery_expenses": "5000",
         "other_expenses": "3000",
         "conveyance_expenses": "5000"
     },
     "applicant_loan_details_details1": { #[NEW PAGE]
         "type_of_loan": "rjururu",
         "interest": "946",
         "name_of_bank": "rjururu",
         "emi_repayments": "54554",
         "outstanding_loan_amount": "5555",
         "collateral_details": "ueueuu",
         "loan_detail": "Bank",
         "tenure_in_months": "545",
         "loan_amount_key": "545545"
     },
     "applicant_loan_details_details4": {
         "type_of_loan": "udjj",
         "interest": "99",
         "name_of_bank": "jdj",
         "emi_repayments": "888",
         "outstanding_loan_amount": "58",
         "collateral_details": "nnj",
         "loan_detail": "Bank",
         "tenure_in_months": "888",
         "loan_amount_key": "888"
     },
    "applicant_loan_details_applied_loan": {
        "repayment_option": "Monthly",
        "required_loan_amount": "500000",
        "purpose_of_the_loan": "Buy Machine"
    },
     "applicant_loan_details_details3": { #[NEW PAGE]
         "type_of_loan": "udu",
         "interest": "6",
         "name_of_bank": "hdh",
         "emi_repayments": "5",
         "outstanding_loan_amount": "85",
         "collateral_details": "uu",
         "loan_detail": "Bank",
         "tenure_in_months": "55",
         "loan_amount_key": "54"
     },
    "applicant_family_details_assets": {
        "how_long_are_you_staying_in_house__in_years": "3-5 years",
        "residence_details": "Family Owned",
        "rent_agreement": "No",
        "monthly_rent": "20000"
    },
     "applicant_other_card_family_assets": {  # [NEW PAGE]
         "computer": "OwnFund",
         "ref_y_n": "Yes",
         "television": "OwnFund",
         "other": "Loan",
         "wm_y_n": "Yes",
         "2_wheeler": "OwnFund",
         "refrigerator": "Loan",
         "other_y_n": "Yes",
         "televsn_y_n": "Yes",
         "comp_y_n": "Yes",
         "2wheeler_y_n": "Yes",
         "washing_machine": "OwnFund"
     },
    "guarantor1_other_card_details1": {
        "bank_credit_co_perative_society": "Jenn",
        "name_of_borrower": "hdh",
        "loan_amount": "8455"
    },
   "applicant_other_card_type_equipment2": {	#[NEW PAGE]
       "estimated_value": "5151",
       "is_equipment_given_as_collateral__dropdown_with_values": "No",
       "date_of_manufacturing_equipment": "uru",
       "details_of_equipment_supplier": "yeururu"
   },
    "product": "",
    "assets_id": "6126ae3a-c7e1-4f06-bc38-63f42c016873",
    "applicant_other_card_purchase_info": {		#[NEW PAGE]
       "raw_material_purchase_in_5_month": "40000",
       "raw_material_purchase_in_7_month": "40000",
        "raw_material_purchase_in_4_month": "40000",
       "raw_material_purchase_in_3_month": "40000",
       "raw_material_purchase_in_8_month": "40000",
        "raw_material_purchase_in_10_month": "40000",
        "total_annual_purchase_cash": "250000",
        "raw_material_purchase_in_11_month": "40000",
       "total_annual_purchase_credit": "250000",
        "raw_material_purchase_in_2_month": "40000",
        "raw_material_purchase_in_12_month": "40000",
        "raw_material_purchase_in_9_month": "40000",
        "raw_material_purchase_in_1_month": "40000",
        "raw_material_purchase_in_6_month": "40000"
    },
   "applicant_business_docs_detail4": {		#[NEW PAGE]
       "place_agency_of_purchase_of_materials": "uruuru",
       "business_assets_average_value_of_inventory": "54554",
       "nature_of_keeping_business_accounts": "Sale/Purchase Note Book",
       "details_of_principal_raw_materials": "uruurur",
       "place_of_storage_for_material": "Godown",
       "method_of_reaching_out_to_customers_to_increase_business": "uruu",
       "details_of_finished_goods": "urhr",
       "business_assets_average_value_of_receivables": "54554"
   },
   "applicant_personal_docs_vehicle1": {		#[NEW PAGE]
       "estimated_resale_value": "250000",
       "year_of_registration": "2010",
       "type_of_vehicle_manufacturer": "hr"
   },
    "applicant_kyc_details": {
        "address": "E-387, GALI N0-8.   Patparganj",
        "spouse_aadhar_card_number": "546764944949",	#[ADD]
        "dob_yob": "1981",
        "pan_card_father_s_husband_s_name": "Saddam Hussain",
        "pincode": "110091",
        "pan_card_name": "Pattan Saddam Hussain",
        "occupation": "Railway",
        "state": "Delhi",
        "taluk": "East Vinod Nagar",
        "voter_id_father_s_husband_s_name": "Saddam Hussain",
        "voter_id": "RT000788999",
        "email_id": "nitin.gk@hotmail.com",
        "spouse_name": "Reshma",			#[ADD]
        "permanent_address": "Graham apt",
        "pan_card_id": "AWEPG9YY78",
        "phone_number": "04917557879",
        "father_s_husband_s_name": "S/O Shri Asharfi Lal Mehto",
        "age": "34",
        "country": "India",
        "district": "East Delhi",
        "name": "Pramod Kumar",
        "uid": "729348086056",
        "voter_id_name": "Pattan Saddam Hussain",
        "type": "AADHAAR",
        "mobile_number": "8797994949"
    },
    "assets_map": {
        "guarantor1": {
            "aadhar_card": [
                "6126ae3a-c7e1-4f06-bc38-63f42c016873/guarantor1_aadhar_card__aadhaar card_0.jpg",
                "6126ae3a-c7e1-4f06-bc38-63f42c016873/guarantor1_aadhar_card__aadhaar card_1.jpg"
            ]
        },
        "guarantor2": {
            "aadhar_card": [
                "6126ae3a-c7e1-4f06-bc38-63f42c016873/guarantor2_aadhar_card__aadhaar card_0.jpg",
                "6126ae3a-c7e1-4f06-bc38-63f42c016873/guarantor2_aadhar_card__aadhaar card_1.jpg"
            ]
        },
        "applicant": {
            "photo": [
                "6126ae3a-c7e1-4f06-bc38-63f42c016873/applicant_photo_borrower_1.jpg"
            ],
            "aadhar_card": [
                "6126ae3a-c7e1-4f06-bc38-63f42c016873/applicant_aadhar_card__aadhaar card_0.jpg",
                "6126ae3a-c7e1-4f06-bc38-63f42c016873/applicant_aadhar_card__aadhaar card_1.jpg"
            ]
        }
    },
    "applicant_other_card_phone_details": {
        "internet_data_uses": "Yes",
        "mobile_services_provider": "Vodafone",
        "billing_type": "Prepaid",
        "handset_type": "Smart Phone",
        "average_monthly_bill": "2000"
    },
    "applicant_other_card_bank_details5": {
        "bank_name": "hdjfjrj",
        "account_holder_name": "ururuuru",
        "bank_branch": "ururuur",
        "branch_ifsc_code": "urudjrj",
        "account_operational_since": "12-3-2014",
        "bank_account_type": "Saving",
        "account_number": "848454664645"
    },
    "applicant_hypothecation_goods_details1": {
        "purchase_purpose": "Ujn",
        "market_value": "54554",
        "goods_details": "Ururu",
        "purchase_year": "8845",
        "purchase_price": "5888",
        "goods_image": "",
        "goods_docs_image": ""
    },
    "guarantor1_kyc_details": {
        "address": ", . zakariya house,zakariya colony,3/103 dargha mohalla Asind",
        "spouse_aadhar_card_number": "878757878784",	#[ ADD ]
        "dob_yob": "1984",
        "pan_card_father_s_husband_s_name": "jjdjdjd",
        "pincode": "311301",
        "pan_card_name": "jjjjd",
        "occupation": "hchfnj",
        "state": "Rajasthan",
        "taluk": "Asind",
        "voter_id_father_s_husband_s_name": "ndndnnfn",
        "voter_id": "jfjfj",
        "email_id": "ururuu",
        "spouse_name": "hdhdjdjjdj",			#[ ADD ]
        "permanent_address": "udrj",
        "pan_card_id": "jjdjdj",
        "phone_number": "80787876797",
        "father_s_husband_s_name": "S/O Shabbir Mohammad Chhipa",
        "age": "31",
        "country": "India",
        "district": "Bhilwara",
        "name": "Arif Mohammad Chhipa",
        "uid": "968354673454",
        "voter_id_name": "ncjfjfjj",
        "type": "AADHAAR",
        "mobile_number": "8787884848"
    },
   "applicant_personal_docs_vehicle3": {	#[NEW PAGE]
       "estimated_resale_value": "57546",
       "year_of_registration": "2010",
       "type_of_vehicle_manufacturer": "ueuuur"
   },
    "locations_map": {
        "home": {
            "lat": 12.9721252,
            "lng": 77.6530464
        },
        "business": {
            "lat": 12.971891350075795,
            "lng": 77.65289271561521
        }
    },
    "applicant_other_card_type_equipment1": {	#[NEW PAGE]
       "estimated_value": "5515",
        "is_equipment_given_as_collateral__dropdown_with_values": "No",
        "date_of_manufacturing_equipment": "hruru",
        "details_of_equipment_supplier": "ururu"
    },
    "applicant_other_card_id_details": {
        "pan_card": "AWEPG9YY78",
        "driving_license": "HJDJKDMD88999",
        "passport": "hdjjjd8889",
        "voter_id": "YUGDHKD8999",
        "ration_card": "RT08877788"
    },
    "center": "",
    "applicant_hypothecation_goods_details2": {
        "purchase_purpose": "Hh",
        "market_value": "58858",
        "goods_details": "Hhdh",
        "purchase_year": "58",
        "purchase_price": "5888",
        "goods_image": "",
        "goods_docs_image": ""
    },
    "applicant_business_docs_info": {
        "permissions_licenses_reqd": "hdhrhrh",		#[ ADD ]
        "business_name": "hjdjj",
        "type_of_business_entity": "Proprietor",	#[ADD]
        "area_market_value": "54555",
        "vat_service_tax_regn_no": "hdhrhh",
        "monthly_rent": "57548",			#[ADD]
        "ssi_registration_entrepeneur_memorandum_ref_no": "hdhhrhr",	#[ADD]
        "description_business": "hdhdhhdh",
        "registered_rent_agreement": "Yes",		#[ADD]
        "shops__establishment_no": "hdhrhrh",
        "no_of_years_in_business": "2",			#[ADD]
        "workplace_details": "Owned",			#[ADD]
        "pancard_no": "hdhdhhdhd",
        "area_occupied": "8787",
        "outstanding_loan": "500",
        "address_of_place_of_business": "hdhrhrh"
    },
     "applicant_family_details_details2": {   #[NEW PAGE]
         "aadhar_number": "548484846565",
         "name": "Saddam Hussain",
         "education": "SSC",
         "occupations_details": "Hjdj",
         "age": "50",
         "annual_income": "150000",
         "relation": "Father"
     },
     "applicant_other_card_assets_liability": {		#[NEW PAGE]
         "insurance_policies": "5588",
         "loans_from_relatives,money_lender_etc": "588",
         "creditors_for_raw_material": "888",
         "raw_material_in_han": "588",
        "loan_outstanding_against__property_value___agriculture": "588",
         "loan_outstanding_against__property_value___residential": "888",
         "vehicle_loans": "888",
         "loan_outstanding_against__property_value___commercial_": "558",
         "cash_and_bank_balance": "588",
         "vehicles_current_estimate_of_resale_value": "588",
         "immovable_property_estimated_value___agriculture": "8888",
         "immovable_property_estimated_value___residential": "555",
         "immovable_property_estimated_value___commercial": "558888",
         "fixed_deposit_and_ppf": "555",
         "receivables_from_customer": "888",
         "gold_and_jewellery": "888"
     },
    "applicant_other_card_credit_card_details": {
        "issue_bank_2": "hrhjru",
        "issue_bank_1": "hdururu",	#[ADD]
        "issue_bank_3": "ururuu"	#[ADD]
    },
    "applicant_business_docs_home_image": {},
    "applicant_business_docs_home_loc": {},
    "applicant_other_card_cust_supplier": {
        "address": "udurhruu",
        "telephoneno_4": "884845",
        "name_4": "jrhruru",
        "name_3": "hdhrhh",
        "telephoneno_2": "84848",
        "address_5": "jejrj",
        "telephoneno_5": "88454548845",
        "telephoneno_3": "454554",
        "credit": "15 days",
        "name_2": "hdhhdhrhrh",
        "name_5": "hdhhdhrh",
        "address_4": "jhdhd",
        "address_2": "hdhrh",
        "address_3": "hrhrhh",
        "name": "uduruur",
        "telephoneno": "55555555555"
    },
     "applicant_other_card_land_details2": {  #[New Page]
         "land_location": "ueueuuj",		#[ADD]
         "type_of_property": "Residential",	#[ADD]
         "area_in_sqft": "548",			#[ADD]
         "estimated_resale_value": "54555",
         "loan_outstanding": "28800"
     },
    "applicant_other_card_bank_details3": {
        "bank_name": "ururu",
        "account_holder_name": "jrhhrhrh",
        "bank_branch": "jduruur",
        "branch_ifsc_code": "hdjdjd",
        "account_operational_since": "13-3-2013",
        "bank_account_type": "Saving",
        "account_number": "54554545"
    },
    "applicant_personal_docs": {
        "marital_status": "Married",
        "religion": "Hindu",
        "physical_disability": "None",
        "education": "SSC",
        "gender": "Male",
        "category": "General"
    },
    "applicant_other_card_borrower_furnished": {
        "for_how_many_borrowers_have_you_furnished_guarantees__": "One"		#[ADD]
    },
     "applicant_loan_details_details2": {  #[NEW PAGE]
        "type_of_loan": "ueuruur",
        "interest": "66",
         "name_of_bank": "urjruu",
         "emi_repayments": "55",
         "outstanding_loan_amount": "55",
         "collateral_details": "uu",
         "loan_detail": "Bank",
         "tenure_in_months": "545",
         "loan_amount_key": "545545"
     },
    "guarantor2_kyc_details": {
        "address": "10/2, KHALASHI LINE. THANA GWALTOLI  ",
        "spouse_aadhar_card_number": "455448484554",		#[ADD]
        "dob_yob": "1990",
        "pan_card_father_s_husband_s_name": "jjjdjdj",
        "pincode": "208002",
        "pan_card_name": "udhdhfh",
        "occupation": "udururjr",
        "state": "Uttar Pradesh",
        "taluk": "Kanpur",
        "voter_id_father_s_husband_s_name": "ududjudj",
        "voter_id": "jdjjdjfj",
        "email_id": "jdjdjj",
        "spouse_name": "hdhdhj",				#[ADD]
        "permanent_address": "hhdhdh",
        "pan_card_id": "ududuru",
        "phone_number": "875485",
        "father_s_husband_s_name": "S/O ASHOK SHARMA",
        "age": "25",
        "country": "India",
        "district": "Kanpur Nagar",
        "name": "Ashutosh Sharma",
        "uid": "335482230048",
        "voter_id_name": "iruruuru",
        "type": "AADHAAR",
        "mobile_number": "5454545"
    },
    "applicant_other_card_bus_monthly_exp": {		#[NEW PAGE]
     "electricity_charges": "5000",
     "freight_charges": "500",
         "petrol_expenses": "500",
         "other_expenses": "5000",
         "salaries_and_wages": "500000"
     },
    "applicant_personal_docs_vehicle2": {		#[NEW PAGE]
        "estimated_resale_value": "245458",
        "year_of_registration": "2010",
        "type_of_vehicle_manufacturer": "uduru"
    }
}

headers = {
  'content-type': "application/json"
}

response = requests.post(url, json=payload, params=querystring)
print(response.text)
