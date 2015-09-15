import os, tempfile
import json, hashlib
from flask.ext import excel
from flask import Blueprint, request
from flask import render_template,session,request,Response,abort
from flask_login import current_user, login_required
from e_admin.models import EsthenosUser
from e_tokens.utils import login_or_key_required
from e_organisation.models import EsthenosOrg, EsthenosOrgApplicationHighMarkRequest, EsthenosOrgApplicationHighMarkResponse, EsthenosOrgApplication

storage_path =  os.path.join(os.curdir,'pitaya/uploads')
reports_views = Blueprint('reports_views', __name__, template_folder='templates')


def get_application_headers():
    headers = list()

    headers.append("Organisation Name")

    headers.append("Date Updated")
    headers.append("Date Created")

    headers.append("Status")
    headers.append("Current Status")
    headers.append("Current Status Updated")

    headers.append("Repeat Application ID")
    headers.append("Application ID")
    headers.append("Upload Type")
    headers.append("Applicant Name")
    headers.append("Age")
    headers.append("DOB")
    headers.append("Gender")
    headers.append("Education")

    headers.append("Address")
    headers.append("Member Mobile Phone")
    headers.append("Member Tele Code")
    headers.append("Member Country")
    headers.append("Member State")
    headers.append("Member City")
    headers.append("Member Taluk")
    headers.append("Member Village")
    headers.append("Member PinCode")
    headers.append("Member Disability")
    headers.append("Member F Or H Age")
    headers.append("Member F Or H Name")
    headers.append("Member Id Proof Number")
    headers.append("Member Relationship Status")

    headers.append("Purpose Of Loan")
    headers.append("Applied Loan")
    headers.append("Religion")
    headers.append("Category")
    headers.append("Caste")

    headers.append("Drinking Water")
    headers.append("Quality Of House")
    headers.append("Type Of Residence")
    headers.append("House Type")
    headers.append("House Stay Duration")

    headers.append("Family Size")
    headers.append("Adult Count")
    headers.append("Male Count")
    headers.append("Female Count")
    headers.append("Children Above18")
    headers.append("Children Below18")
    headers.append("Total Earning Members")

    headers.append("Primary Business Category")
    headers.append("Primary Business")

    headers.append("Secondary Business Category")
    headers.append("Secondary Business")

    headers.append("Tertiary Business Category")
    headers.append("Tertiary Business")

    headers.append("Family Assets")
    headers.append("Family assets: No of Cows")
    headers.append("Family assets: No of Sheeps")
    headers.append("Family assets: Patta Land")
    headers.append("Family assets: Shared Land")
    headers.append("Family assets: Orchard(Acres)")
    headers.append("Family assets: Self Owned Land(Acres)")

    headers.append("Primary Income")
    headers.append("Secondary Income")
    headers.append("Tertiary Income")
    headers.append("Other Income")
    headers.append("Total Income")

    headers.append("Primary Expense")
    headers.append("Secondary Expense")
    headers.append("Tertiary Expense")
    headers.append("Food Expense")
    headers.append("Travel Expense")
    headers.append("Medical Expense")
    headers.append("Educational Expense")
    headers.append("Festival Expense")
    headers.append("Entertainment Expense")
    headers.append("House Rent Expense")
    headers.append("Household Expense")
    headers.append("Business Expense")
    headers.append("Business Expense - Working Capital")
    headers.append("Business Expense - Employee Salary")
    headers.append("Business Expense - Rent")
    headers.append("Business Expense - Admin")
    headers.append("Business Expense - Other")
    headers.append("Other Expense")
    headers.append("Total Expenditure")

    headers.append("Total Liability")
    headers.append("Outstanding1")
    headers.append("Outstanding2")
    headers.append("Outstanding3")
    headers.append("Outstanding4")
    headers.append("Total Outstanding")

    headers.append("Other Outstanding Emi")
    headers.append("Other Outstanding Chit")
    headers.append("Other Outstanding Insurance")
    headers.append("Other Outstanding Friends & Family")
    headers.append("Total Other Outstanding")

    headers.append("Net Income")
    headers.append("Total Running Loans")

    headers.append("Total Running Loans From Mfi")
    headers.append("Total Existing Outstanding From")
    headers.append("Total Existing Outstanding From Mfi")

    headers.append("Loan Eligibility Based On Net Income")
    headers.append("Loan Eligibility Based On Company Policy")

    headers.append("Existing Loan Cycle")
    headers.append("Eligible Loan Cycle")
    headers.append("Defaults With No Mfis")
    headers.append("Attendence Percentage")

    headers.append("Interested In Other Fp")

    headers.append("Village")
    headers.append("Village Road")
    headers.append("Village Water")
    headers.append("Village Electricity")
    headers.append("Village Education Facilities")
    headers.append("Village Public Transport")
    headers.append("Village Hospital Category")
    headers.append("Village Medical Facilities")
    headers.append("Village Financial Institution")
    headers.append("Village Sanitation")

    headers.append("Bank Name")
    headers.append("Bank Ifsc Code")
    headers.append("Bank Account Number")
    headers.append("Bank Account Holder name")
    headers.append("Bank Cheque #")
    headers.append("Bank Cheque # Name")
    headers.append("Repayment Mode")
    headers.append("Repayment Method")

    headers.append("Guarantor S")
    headers.append("Guarantor Name")
    headers.append("Guarantor Age")
    headers.append("Guarantor Sex")

    headers.append("Guarantor Nominee Age")
    headers.append("Guarantor Nominee name")
    headers.append("Guarantor Nominee gender")
    headers.append("Guarantor borrowers_are_nominee")
    headers.append("Guarantor's Relationship With Borrower")
    headers.append("Guarantor Borrower Are Nominee For Each Other")

    headers.append("Borrower S")
    headers.append("Borrower's Nominee Age")
    headers.append("Borrower's Nominee Name")
    headers.append("Borrower's Nominee Gender")

    headers.append("Equifax Submitted")
    headers.append("Highmark Submitted")
    headers.append("Generate Disbursement")
    headers.append("Generate Disbursement Done")

    headers.append("Expected Tenure In Months")
    headers.append("Expected EMI Amount Served")

    return headers


def get_application_rowdata(app):
    row_data = list()

    row_data.append(app.organisation.name)

    row_data.append(app["updated_on"])
    row_data.append(app["date_created"])

    row_data.append(app["status"])
    row_data.append(app["current_status"])
    row_data.append(app["current_status_updated"])

    row_data.append(app["repeat_application_id"])
    row_data.append(app["application_id"])
    row_data.append(app["upload_type"])
    row_data.append(app["applicant_name"])
    row_data.append(app["age"])
    row_data.append(app["dob"])
    row_data.append(app["gender"])
    row_data.append(app["education"])

    row_data.append(app["address"])
    row_data.append(app["member_telephone"])
    row_data.append(app["member_tele_code"])
    row_data.append(app["member_country"])
    row_data.append(app["member_state"])
    row_data.append(app["member_city"])
    row_data.append(app["member_taluk"])
    row_data.append(app["member_village"])
    row_data.append(app["member_pincode"])
    row_data.append(app["member_disability"])
    row_data.append(app["member_f_or_h_age"])
    row_data.append(app["member_f_or_h_name"])
    row_data.append(app["member_id_proof_number"])
    row_data.append(app["member_relationship_status"])

    row_data.append(app["purpose_of_loan"])
    row_data.append(app["applied_loan"])
    row_data.append(app["religion"])
    row_data.append(app["category"])
    row_data.append(app["caste"])

    row_data.append(app["drinking_water"])
    row_data.append(app["quality_of_house"])
    row_data.append(app["type_of_residence"])
    row_data.append(app["select_house_type"])
    row_data.append(app["house_stay_duration"])

    row_data.append(app["family_size"])
    row_data.append(app["adult_count"])
    row_data.append(app["male_count"])
    row_data.append(app["female_count"])
    row_data.append(app["children_above18"])
    row_data.append(app["children_below18"])
    row_data.append(app["total_earning_members"])

    row_data.append(app["primary_business_category"])
    row_data.append(app["primary_business"])

    row_data.append(app["secondary_business_category"])
    row_data.append(app["secondary_business"])

    row_data.append(app["tertiary_business_category"])
    row_data.append(app["tertiary_business"])

    row_data.append(app["family_assets"])
    row_data.append(app["num_cows"])
    row_data.append(app["num_sheeps"])
    row_data.append(app["patta_land"])
    row_data.append(app["shared_land"])
    row_data.append(app["orchard_acre"])
    row_data.append(app["self_owned_land"])

    row_data.append(app["primary_income"])
    row_data.append(app["secondary_income"])
    row_data.append(app["tertiary_income"])
    row_data.append(app["other_income"])
    row_data.append(app["total_income"])

    row_data.append(app["primary_expenses"])
    row_data.append(app["secondary_expenses"])
    row_data.append(app["tertiary_expenses"])
    row_data.append(app["food_expense"])
    row_data.append(app["travel_expense"])
    row_data.append(app["medical_expense"])
    row_data.append(app["educational_expense"])
    row_data.append(app["festival_expenditure"])
    row_data.append(app["entertainment_expense"])
    row_data.append(app["house_rent_expenditure"])
    row_data.append(app["house_hold_expenditure"])
    row_data.append(app["business_expense"])
    row_data.append(app["business_expense_working_capital"])
    row_data.append(app["business_expense_employee_salary"])
    row_data.append(app["business_expense_rent"])
    row_data.append(app["business_expense_admin"])
    row_data.append(app["business_expense_other"])
    row_data.append(app["other_expense"])
    row_data.append(app["total_expenditure"])

    row_data.append(app["total_liability"])
    row_data.append(app["outstanding_1"])
    row_data.append(app["outstanding_2"])
    row_data.append(app["outstanding_3"])
    row_data.append(app["outstanding_4"])
    row_data.append(app["total_outstanding"])

    row_data.append(app["other_outstanding_emi"])
    row_data.append(app["other_outstanding_chit"])
    row_data.append(app["other_outstanding_insurance"])
    row_data.append(app["other_outstanding_familynfriends"])
    row_data.append(app["total_other_outstanding"])

    row_data.append(app["net_income"])
    row_data.append(app["total_running_loans"])

    row_data.append(app["total_running_loans_from_mfi"])
    row_data.append(app["total_existing_outstanding_from"])
    row_data.append(app["total_existing_outstanding_from_mfi"])

    row_data.append(app["loan_eligibility_based_on_net_income"])
    row_data.append(app["loan_eligibility_based_on_company_policy"])

    row_data.append(app["existing_loan_cycle"])
    row_data.append(app["eligible_loan_cycle"])
    row_data.append(app["defaults_with_no_mfis"])
    row_data.append(app["attendence_percentage"])

    row_data.append(app["interested_in_other_fp"])

    row_data.append(app["village"])
    row_data.append(app["village_road"])
    row_data.append(app["village_water"])
    row_data.append(app["village_electricity"])
    row_data.append(app["village_edu_facilities"])
    row_data.append(app["village_public_transport"])
    row_data.append(app["village_hospital_category"])
    row_data.append(app["village_medical_facilities"])
    row_data.append(app["village_financial_institution"])
    row_data.append(app["village_information_sanitation"])

    row_data.append(app["bank_name"])
    row_data.append(app["bank_ifsc_code"])
    row_data.append(app["bank_account_number"])
    row_data.append(app["bank_account_holder_name"])
    row_data.append(app["cheque_no"])
    row_data.append(app["cheque_bank_name"])
    row_data.append(app["repayment_mode"])
    row_data.append(app["repayment_method"])

    row_data.append(app["guranteer_s"])
    row_data.append(app["gurranter_s_sex"])
    row_data.append(app["gurranter_s_age"])
    row_data.append(app["gurranter_s_name"])

    row_data.append(app["gurantors_nominee_age"])
    row_data.append(app["gurantors_nominee_name"])
    row_data.append(app["gurantors_nominee_gender"])
    row_data.append(app["guarantor_borrowers_are_nominee"])
    row_data.append(app["gurantor_s_relationship_with_borrower"])
    row_data.append(app["gurantors_borrowers_are_nominee_for_each_other_"])

    row_data.append(app["borrower_s"])
    row_data.append(app["borrowers_nominee_age"])
    row_data.append(app["borrowers_nominee_name"])
    row_data.append(app["borrowers_nominee_gender"])

    row_data.append(app["equifax_submitted"])
    row_data.append(app["highmark_submitted"])
    row_data.append(app["generate_disbursement"])
    row_data.append(app["generate_disbursement_done"])

    row_data.append(app["expected_tenure_in_months"])
    row_data.append(app["expected_emi_amount_served"])

    return row_data


@reports_views.route('/reports/internal_main/download', methods=["GET"])
@login_or_key_required
def internal_main_reports():
    c_user = current_user
    kwargs = locals()
    from e_organisation.models import EsthenosOrgApplication
    if request.method == 'GET':
        user  = EsthenosUser.objects.get(id=c_user.id)
        applications = EsthenosOrgApplication.objects(organisation=user.organisation)
        application_data = list()

        app_headers = get_application_headers()
        hm_response_headers = list()
        hm_response_headers.append("Application Id")
        hm_response_headers.append("Member Id")
        hm_response_headers.append("Member Name")
        hm_response_headers.append("Spouse Name")
        hm_response_headers.append("Status")
        hm_response_headers.append("Own")
        hm_response_headers.append("Oth All")
        hm_response_headers.append("Oth Active")
        hm_response_headers.append("Pri")
        hm_response_headers.append("Sec")
        hm_response_headers.append("Closed Account")
        hm_response_headers.append("Active Account")
        hm_response_headers.append("Default Account")
        hm_response_headers.append("Own Disb Amt")
        hm_response_headers.append("Other Disb Amt")
        hm_response_headers.append("Own Curr Amt")
        hm_response_headers.append("Other Curr Amt")
        hm_response_headers.append("Own Inst Amt")
        hm_response_headers.append("Other Inst Amt")
        hm_response_headers.append("Value")
        hm_response_headers.append("Remark")
        hm_response_headers.append("Error Descripton")
        hm_response_headers.append("Address")
        hm_response_headers.append("Dob Age")
        hm_response_headers.append("Age As On Dt")
        hm_response_headers.append("Father Name")
        hm_response_headers.append("Ration Card")
        hm_response_headers.append("Voter Id")
        hm_response_headers.append("Phone")
        hm_response_headers.append("Rel Type1")
        hm_response_headers.append("Mbr Rel Name1")
        hm_response_headers.append("Rel Type2")
        hm_response_headers.append("Mbr Rel Name2")
        hm_response_headers.append("Driving Lic")
        hm_response_headers.append("Other Id Type1")
        hm_response_headers.append("Other Id Val1")
        hm_response_headers.append("Branch")
        hm_response_headers.append("Kendra")
        hm_response_headers.append("Report Id")
        headers = app_headers + hm_response_headers
        application_data.append(headers)
        for app in applications:
            app_row_data= get_application_rowdata(app)
            hmresp = EsthenosOrgApplicationHighMarkRequest.objects.get(application_id=app.application_id)
            row_data = list()
            row_data.append(hmresp["application_id"])
            row_data.append(hmresp["member_id"])
            row_data.append(hmresp["member_name"])
            row_data.append(hmresp["spouse_name"])
            row_data.append(hmresp["status"])
            row_data.append(hmresp["own"])
            row_data.append(hmresp["oth_all"])
            row_data.append(hmresp["oth_active"])
            row_data.append(hmresp["pri"])
            row_data.append(hmresp["sec"])
            row_data.append(hmresp["closed_account"])
            row_data.append(hmresp["active_account"])
            row_data.append(hmresp["default_account"])
            row_data.append(hmresp["own_disb_amt"])
            row_data.append(hmresp["other_disb_amt"])
            row_data.append(hmresp["own_curr_amt"])
            row_data.append(hmresp["other_curr_amt"])
            row_data.append(hmresp["own_inst_amt"])
            row_data.append(hmresp["other_inst_amt"])
            row_data.append(hmresp["value"])
            row_data.append(hmresp["remark"])
            row_data.append(hmresp["error_descripton"])
            row_data.append(hmresp["address"])
            row_data.append(hmresp["dob_age"])
            row_data.append(hmresp["age_as_on_dt"])
            row_data.append(hmresp["father_name"])
            row_data.append(hmresp["ration_card"])
            row_data.append(hmresp["voter_id"])
            row_data.append(hmresp["phone"])
            row_data.append(hmresp["rel_type1"])
            row_data.append(hmresp["mbr_rel_name1"])
            row_data.append(hmresp["rel_type2"])
            row_data.append(hmresp["mbr_rel_name2"])
            row_data.append(hmresp["driving_lic"])
            row_data.append(hmresp["other_id_type1"])
            row_data.append(hmresp["other_id_val1"])
            row_data.append(hmresp["branch"])
            row_data.append(hmresp["kendra"])
            row_data.append(hmresp["report_id"])
            app_row_data = app_row_data+row_data
            application_data.append(app_row_data)

        output = excel.make_response_from_array(application_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=internal_main_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output


@reports_views.route('/reports/external_main/download', methods=["GET"])
@login_or_key_required
def external_main_reports():
    c_user = current_user
    kwargs = locals()
    from e_organisation.models import EsthenosOrgApplication
    if request.method == 'GET':
        user = EsthenosUser.objects.get(id=c_user.id)
        applications = EsthenosOrgApplication.objects(organisation=user.organisation)
        application_data = list()
        headers = get_application_headers()
        application_data.append(headers)
        for app in applications:
            row_data = get_application_rowdata(app)
            application_data.append(row_data)

        output = excel.make_response_from_array(application_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=external_main_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output


@reports_views.route('/reports/highmark_request/download', methods=["GET"])
@login_or_key_required
def himark_request_reports():
    c_user = current_user
    kwargs = locals()

    if request.method == 'GET':
        user  = EsthenosUser.objects.get(id=c_user.id)

        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation)

        application_data = list()

        hm_request_headers = list()
        hm_request_headers.append("APPLICANT ID TYPE 1")
        hm_request_headers.append("SEGMENT IDENTIFIER")
        hm_request_headers.append("CREDIT REQUEST TYPE")
        hm_request_headers.append("CREDIT REPORT TRANSACTION ID")
        hm_request_headers.append("CREDIT INQUIRY PURPOSE TYPE")
        hm_request_headers.append("CREDIT INQUIRY PURPOSE TYPE DESCRIPTION")
        hm_request_headers.append("CREDIT INQUIRY STAGE")
        hm_request_headers.append("CREDIT REPORT TRANSACTION DATE TIME")
        hm_request_headers.append("APPLICANT NAME1")
        hm_request_headers.append("APPLICANT NAME2")
        hm_request_headers.append("APPLICANT NAME3")
        hm_request_headers.append("APPLICANT NAME4")
        hm_request_headers.append("APPLICANT NAME5")
        hm_request_headers.append("MEMBER FATHER NAME")
        hm_request_headers.append("MEMBER MOTHER NAME")
        hm_request_headers.append("MEMBER SPOUSE NAME")
        hm_request_headers.append("MEMBER RELATIONSHIP TYPE 1")
        hm_request_headers.append("MEMBER RELATIONSHIP NAME 1")
        hm_request_headers.append("MEMBER RELATIONSHIP TYPE 2")
        hm_request_headers.append("MEMBER RELATIONSHIP NAME 2")
        hm_request_headers.append("MEMBER RELATIONSHIP TYPE 3")
        hm_request_headers.append("MEMBER RELATIONSHIP NAME 3")
        hm_request_headers.append("MEMBER RELATIONSHIP TYPE 4")
        hm_request_headers.append("MEMBER RELATIONSHIP NAME 4")
        hm_request_headers.append("APPLICANT BIRTH DATE")
        hm_request_headers.append("APPLICANT AGE")
        hm_request_headers.append("APPLICANT AGE AS ON DATE")
        hm_request_headers.append("APPLICANT ID  1")
        hm_request_headers.append("APPLICANT ID TYPE 2")
        hm_request_headers.append("APPLICANT ID 2")
        hm_request_headers.append("ACCT OPEN DATE")
        hm_request_headers.append("APPLICATION-ID/ ACCOUNT-NO")
        hm_request_headers.append("BRANCH ID")
        hm_request_headers.append("MEMBER ID")
        hm_request_headers.append("KENDRA ID")
        hm_request_headers.append("APPLIED FOR AMOUNT/ CURRENT BALANCE")
        hm_request_headers.append("KEY PERSON NAME")
        hm_request_headers.append("KEY PERSON  RELATION")
        hm_request_headers.append("NOMINEE NAME")
        hm_request_headers.append("NOMINEE RELATIONSHIP TYPE")
        hm_request_headers.append("APPLICANT TELEPHONE NUMBER TYPE 1")
        hm_request_headers.append("APPLICANT TELEPHONE NUMBER 1")
        hm_request_headers.append("APPLICANT TELEPHONE NUMBER TYPE 2")
        hm_request_headers.append("APPLICANT TELEPHONE NUMBER 2")
        hm_request_headers.append("APPLICANT ADDRESS TYPE 1")
        hm_request_headers.append("APPLICANT ADDRESS 1")
        hm_request_headers.append("APPLICANT ADDRESS 1 CITY")
        hm_request_headers.append("APPLICANT ADDRESS 1 STATE")
        hm_request_headers.append("APPLICANT ADDRESS 1 PIN CODE")
        hm_request_headers.append("APPLICANT ADDRESS TYPE 2")
        hm_request_headers.append("APPLICANT ADDRESS 2")
        hm_request_headers.append("APPLICANT ADDRESS 2 CITY")
        hm_request_headers.append("APPLICANT ADDRESS 2 STATE")
        hm_request_headers.append("APPLICANT ADDRESS 2 PIN CODE")
        headers =  hm_request_headers
        application_data.append(headers)
        for app in applications:
            hm_request = EsthenosOrgApplicationHighMarkResponse.objects.get(application_id=app.application_id)
            row_data = list()
            row_data.append(hm_request["application_id"])
            row_data.append(hm_request["segment_identifier"])
            row_data.append(hm_request["credit_request_type"])
            row_data.append(hm_request["credit_report_transaction_id"])
            row_data.append(hm_request["credit_inquiry_purpose_type"])
            row_data.append(hm_request["credit_inquiry_purpose_type_description"])
            row_data.append(hm_request["credit_inquiry_stage"])
            row_data.append(hm_request["credit_report_transaction_date_time"])
            row_data.append(hm_request["applicant_name1"])
            row_data.append(hm_request["applicant_name2"])
            row_data.append(hm_request["applicant_name3"])
            row_data.append(hm_request["applicant_name4"])
            row_data.append(hm_request["applicant_name5"])
            row_data.append(hm_request["member_father_name"])
            row_data.append(hm_request["member_mother_name"])
            row_data.append(hm_request["member_spouse_name"])
            row_data.append(hm_request["member_relationship_type1"])
            row_data.append(hm_request["member_relationship_name1"])
            row_data.append(hm_request["member_relationship_type2"])
            row_data.append(hm_request["member_relationship_name2"])
            row_data.append(hm_request["member_relationship_type3"])
            row_data.append(hm_request["member_relationship_name3"])
            row_data.append(hm_request["member_relationship_type4"])
            row_data.append(hm_request["member_relationship_name4"])
            row_data.append(hm_request["applicant_birth_date"])
            row_data.append(hm_request["applicant_age"])
            row_data.append(hm_request["applicant_age_as_on_date"])
            row_data.append(hm_request["applicant_id_type1"])
            row_data.append(hm_request["applicant_id1"])
            row_data.append(hm_request["applicant_id_type2"])
            row_data.append(hm_request["applicant_id2"])
            row_data.append(hm_request["acct_open_date"])
            row_data.append(hm_request["applicant_id__account_no"])
            row_data.append(hm_request["branch_id"])
            row_data.append(hm_request["member_id"])
            row_data.append(hm_request["kendra_id"])
            row_data.append(hm_request["applied_for_amount__current_balance"])
            row_data.append(hm_request["key_person_name"])
            row_data.append(hm_request["key_person_relation"])
            row_data.append(hm_request["nominee_name"])
            row_data.append(hm_request["applicant_telephone_number_type1"])
            row_data.append(hm_request["applicant_telephone_number1"])
            row_data.append(hm_request["applicant_telephone_number_type2"])
            row_data.append(hm_request["applicant_telephone_number2"])
            row_data.append(hm_request["applicant_address_type1"])
            row_data.append(hm_request["applicant_address1"])
            row_data.append(hm_request["applicant_address1_city"])
            row_data.append(hm_request["applicant_address1_state"])
            row_data.append(hm_request["applicant_address1_pincode"])
            row_data.append(hm_request["applicant_address_type2"])
            row_data.append(hm_request["applicant_address2"])
            row_data.append(hm_request["applicant_address2_city"])
            row_data.append(hm_request["applicant_address2_state"])
            row_data.append(hm_request["applicant_address2_pincode"])
            row_data.append(hm_request["nominee_relationship_type"])

            app_row_data = row_data
            application_data.append(app_row_data)

        output = excel.make_response_from_array(application_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=himark_request_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output


@reports_views.route('/reports/eqifax_request/download', methods=["GET"])
@login_or_key_required
def eqifax_request_reports():
    c_user = current_user
    kwargs = locals()
    from e_organisation.models import EsthenosOrgApplicationEqifax
    if request.method == 'GET':
        user  = EsthenosUser.objects.get(id=c_user.id)

        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation)

        application_data = list()

        eq_request_headers = list()
        eq_request_headers.append("Reference Number")
        eq_request_headers.append("Member ID/ Unique Account Number")
        eq_request_headers.append("Inquiry Purpose (Required)")
        eq_request_headers.append("Transaction Amount")
        eq_request_headers.append("ConsumerName (Required)")
        eq_request_headers.append("Additional Type1 (Relationship)")
        eq_request_headers.append("Additional Name1")
        eq_request_headers.append("Additional Type2")
        eq_request_headers.append("Additional Name2")
        eq_request_headers.append("Address & City (Required)")
        eq_request_headers.append("State/Union Territory (Required)")
        eq_request_headers.append("Postal Pin (Required)")
        eq_request_headers.append("Ration Card")
        eq_request_headers.append("Voter ID")
        eq_request_headers.append("Additional Id 1")
        eq_request_headers.append("Additional Id 2")
        eq_request_headers.append("National ID Card (UIN)")
        eq_request_headers.append("Tax ID / PAN ")
        eq_request_headers.append("Phone (Home)")
        eq_request_headers.append("Phone (Mobile)")
        eq_request_headers.append("DOB(Required)")
        eq_request_headers.append("Gender")
        eq_request_headers.append("Branch ID")
        eq_request_headers.append("Kendra ID")

        headers =  eq_request_headers
        application_data.append(headers)
        for app in applications:
            print app.application_id
            eq_request = EsthenosOrgApplicationEqifax.objects.filter(kendra_id=app.application_id)[0]
            row_data = list()
            row_data.append(eq_request["reference_number"])
            row_data.append(eq_request["member_id_unique_accountnumber"])
            row_data.append(eq_request["inquiry_purpose"])
            row_data.append(eq_request["transaction_amount"])
            row_data.append(eq_request["consumer_name"])
            row_data.append(eq_request["additional_type1"])
            row_data.append(eq_request["additional_name1"])
            row_data.append(eq_request["additional_type2"])
            row_data.append(eq_request["additional_name2"])
            row_data.append(eq_request["address_city"])
            row_data.append(eq_request["state_union_territory"])
            row_data.append(eq_request["postal_pin"])
            row_data.append(eq_request["ration_card"])
            row_data.append(eq_request["voter_id"])
            row_data.append(eq_request["additional_id1"])
            row_data.append(eq_request["additional_id2"])
            row_data.append(eq_request["national_id_card"])
            row_data.append(eq_request["tax_id_pan"])
            row_data.append(eq_request["phone_home"])
            row_data.append(eq_request["phone_mobile"])
            row_data.append(eq_request["dob"])
            row_data.append(eq_request["gender"])
            row_data.append(eq_request["branch_id"])
            row_data.append(eq_request["kendra_id"])

            app_row_data = row_data
            application_data.append(app_row_data)

        output = excel.make_response_from_array(application_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=eqifax_request_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output
