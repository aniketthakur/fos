__author__ = 'prathvi'
# Flask and Flask-SQLAlchemy initialization here
from flask import render_template, request,Response
from flask_login import current_user, login_required
from e_tokens.utils import login_or_key_required
import json,hashlib
from e_admin.models import EsthenosUser
from e_organisation.models import EsthenosOrgApplicationHighMark,EsthenosOrgApplicationHighMarkRequest
from flask import  Blueprint
import os,tempfile
from esthenos.crossdomain import *
from esthenos.utils import random_with_N_digits
#import flickr_api
#flickr_api.set_keys(api_key = "8766ced6ec90eb38a32778e847a83233", api_secret = "cda7061fdbd608fd")
storage_path =  os.path.join(os.curdir,'pitaya/uploads')
reports_views = Blueprint('reports_views', __name__,
                        template_folder='templates')

from flask.ext import excel
from flask import Flask, make_response

def get_application_headers():
    headers = list()
    headers.append("Application ID")
    headers.append("Upload Type")
    headers.append("Status")
    headers.append("Applicant Name")
    headers.append("Gender")
    headers.append("Age")
    headers.append("DOB")
    headers.append("Address")
    headers.append("Member Telephone")
    headers.append("Member Tele Code")
    headers.append("Member Country")
    headers.append("Member State")
    headers.append("Member City")
    headers.append("Member Taluk")
    headers.append("Member Village")
    headers.append("Member Relationship Status")
    headers.append("Telephone Number")
    headers.append("Mobile Number")
    headers.append("Applied Loan")
    headers.append("Religion")
    headers.append("Category")
    headers.append("Caste")
    headers.append("Education")
    headers.append("Type Of Residence")
    headers.append("Quality Of House")
    headers.append("Drinking Water")
    headers.append("Purpose Of Loan")
    headers.append("Family Size")
    headers.append("Adult Count")
    headers.append("Children Below18")
    headers.append("Children Below12")
    headers.append("Primary Business Category")
    headers.append("Primary Business")
    headers.append("Secondary Business Category")
    headers.append("Secondary Business")
    headers.append("Tertiary Business Category")
    headers.append("Tertiary Business")
    headers.append("Family Assets")
    headers.append("Money Lenders Loan")
    headers.append("Money Lenders Loan Roi")
    headers.append("Bank Loan")
    headers.append("Bank Loan Roi")
    headers.append("Branch Name")
    headers.append("Branch Id")
    headers.append("State Name")
    headers.append("State Id")
    headers.append("Region Name")
    headers.append("Region Id")
    headers.append("Cm Id")
    headers.append("Cm Cell No")
    headers.append("Repeat Application Id")
    headers.append("Repayment Method")
    headers.append("Primary Income")
    headers.append("Secondary Income")
    headers.append("Tertiary Income")
    headers.append("Other Income")
    headers.append("Total Income")
    headers.append("Business Expense")
    headers.append("Food Expense")
    headers.append("Travel Expense")
    headers.append("Entertainment Expense")
    headers.append("Educational Expense")
    headers.append("Medical Expense")
    headers.append("Other Expense")
    headers.append("Total Expenditure")
    headers.append("Total Liability")
    headers.append("Outstanding1")
    headers.append("Outstanding2")
    headers.append("Outstanding3")
    headers.append("Outstanding4")
    headers.append("Total Outstanding")
    headers.append("Other Outstanding Chit")
    headers.append("Other Outstanding Insurance")
    headers.append("Other Outstanding Emi")
    headers.append("Total Other Outstanding")
    headers.append("Net Income")
    headers.append("Total Running Loans")
    headers.append("Total Existing Outstanding From")
    headers.append("Total Running Loans From Mfi")
    headers.append("Total Existing Outstanding From Mfi")
    headers.append("Existing Loan Cycle")
    headers.append("Eligible Loan Cycle")
    headers.append("Defaults With No Mfis")
    headers.append("Attendence Percentage")
    headers.append("Loan Eligibility Based On Net Income")
    headers.append("Loan Eligibility Based On Company Policy")
    headers.append("Village Electricity")
    headers.append("Interested In Other Fp")
    headers.append("Radio Member Disability")
    headers.append("Village Water")
    headers.append("Festival Expenditure")
    headers.append("Village Medical Facilities")
    headers.append("Micropension Inclusion")
    headers.append("Self Owned Land")
    headers.append("Center Leader Cell")
    headers.append("Center Size")
    headers.append("Applicationtype")
    headers.append("Bankaccount Inclusion")
    headers.append("Fl Loans")
    headers.append("Village Hospital Category")
    headers.append("Group Leader Cell")
    headers.append("Bankfi Amount")
    headers.append("Patta Land")
    headers.append("Group Size")
    headers.append("Select House Type")
    headers.append("Village Road")
    headers.append("Fnf Inclusion")
    headers.append("Member F Or H Name")
    headers.append("Member Pincode")
    headers.append("Repayment Mode")
    headers.append("Moneylenders Amount")
    headers.append("House Rent Expenditure")
    headers.append("Village Public Transport")
    headers.append("House Hold Expenditure")
    headers.append("Village")
    headers.append("JLG")
    headers.append("SHG")
    headers.append("Borroers Cell")
    headers.append("Leader Cell")
    headers.append("Leader Cell1")
    headers.append("Guarantor Borrowers Are Nominee")
    headers.append("Borrower S")
    headers.append("Guranteer S")
    headers.append("Member F Or H Age")
    headers.append("Select Education")
    headers.append("Girl")
    headers.append("Boy")
    headers.append("P Expense")
    headers.append("S Expense")
    headers.append("T Expense")
    headers.append("I Total")
    headers.append("E Total")
    headers.append("Member Id Proof Number")
    headers.append("Current Status Updated")
    headers.append("Date Created")
    headers.append("Date Updated")
    headers.append("Excepted Disbursment Date")
    return headers

def get_application_rowdata(app):
    row_data = list()
    row_data.append(app["application_id"])
    row_data.append(app["upload_type"])
    row_data.append(app["status"])
    row_data.append(app["applicant_name"])
    row_data.append(app["gender"])
    row_data.append(app["age"])
    row_data.append(app["dob"])
    row_data.append(app["address"])
    row_data.append(app["member_telephone"])
    row_data.append(app["member_tele_code"])
    row_data.append(app["member_country"])
    row_data.append(app["member_state"])
    row_data.append(app["member_city"])
    row_data.append(app["member_taluk"])
    row_data.append(app["member_village"])
    row_data.append(app["member_relationship_status"])
    row_data.append(app["telephone_number"])
    row_data.append(app["mobile_number"])
    row_data.append(app["applied_loan"])
    row_data.append(app["religion"])
    row_data.append(app["category"])
    row_data.append(app["caste"])
    row_data.append(app["education"])
    row_data.append(app["type_of_residence"])
    row_data.append(app["quality_of_house"])
    row_data.append(app["drinking_water"])
    row_data.append(app["purpose_of_loan"])
    row_data.append(app["family_size"])
    row_data.append(app["adult_count"])
    row_data.append(app["children_below18"])
    row_data.append(app["children_below12"])
    row_data.append(app["primary_business_category"])
    row_data.append(app["primary_business"])
    row_data.append(app["secondary_business_category"])
    row_data.append(app["secondary_business"])
    row_data.append(app["tertiary_business_category"])
    row_data.append(app["tertiary_business"])
    row_data.append(app["family_assets"])
    row_data.append(app["money_lenders_loan"])
    row_data.append(app["money_lenders_loan_roi"])
    row_data.append(app["bank_loan"])
    row_data.append(app["bank_loan_roi"])
    row_data.append(app["branch_name"])
    row_data.append(app["branch_id"])
    row_data.append(app["state_name"])
    row_data.append(app["state_id"])
    row_data.append(app["region_name"])
    row_data.append(app["region_id"])
    row_data.append(app["cm_id"])
    row_data.append(app["cm_cell_no"])
    row_data.append(app["repeat_application_id"])
    row_data.append(app["repayment_method"])
    row_data.append(app["primary_income"])
    row_data.append(app["secondary_income"])
    row_data.append(app["tertiary_income"])
    row_data.append(app["other_income"])
    row_data.append(app["total_income"])
    row_data.append(app["business_expense"])
    row_data.append(app["food_expense"])
    row_data.append(app["travel_expense"])
    row_data.append(app["entertainment_expense"])
    row_data.append(app["educational_expense"])
    row_data.append(app["medical_expense"])
    row_data.append(app["other_expense"])
    row_data.append(app["total_expenditure"])
    row_data.append(app["total_liability"])
    row_data.append(app["outstanding_1"])
    row_data.append(app["outstanding_2"])
    row_data.append(app["outstanding_3"])
    row_data.append(app["outstanding_4"])
    row_data.append(app["total_outstanding"])
    row_data.append(app["other_outstanding_chit"])
    row_data.append(app["other_outstanding_insurance"])
    row_data.append(app["other_outstanding_emi"])
    row_data.append(app["total_other_outstanding"])
    row_data.append(app["net_income"])
    row_data.append(app["total_running_loans"])
    row_data.append(app["total_existing_outstanding_from"])
    row_data.append(app["total_running_loans_from_mfi"])
    row_data.append(app["total_existing_outstanding_from_mfi"])
    row_data.append(app["existing_loan_cycle"])
    row_data.append(app["eligible_loan_cycle"])
    row_data.append(app["defaults_with_no_mfis"])
    row_data.append(app["attendence_percentage"])
    row_data.append(app["loan_eligibility_based_on_net_income"])
    row_data.append(app["loan_eligibility_based_on_company_policy"])
    row_data.append(app["village_electricity"])
    row_data.append(app["interested_in_other_fp"])
    row_data.append(app["radio_member_disability"])
    row_data.append(app["village_water"])
    row_data.append(app["festival_expenditure"])
    row_data.append(app["village_medical_facilities"])
    row_data.append(app["micropension_inclusion"])
    row_data.append(app["self_owned_land"])
    row_data.append(app["center_leader_cell"])
    row_data.append(app["center_size"])
    row_data.append(app["applicationtype"])
    row_data.append(app["bankaccount_inclusion"])
    row_data.append(app["fl_loans"])
    row_data.append(app["village_hospital_category"])
    row_data.append(app["group_leader_cell"])
    row_data.append(app["bankfi_amount"])
    row_data.append(app["patta_land"])
    row_data.append(app["group_size"])
    row_data.append(app["select_house_type"])
    row_data.append(app["village_road"])
    row_data.append(app["fnf_inclusion"])
    row_data.append(app["member_f_or_h_name"])
    row_data.append(app["member_pincode"])
    row_data.append(app["repayment_mode"])
    row_data.append(app["moneylenders_amount"])
    row_data.append(app["house_rent_expenditure"])
    row_data.append(app["village_public_transport"])
    row_data.append(app["house_hold_expenditure"])
    row_data.append(app["village"])
    row_data.append(app["JLG"])
    row_data.append(app["SHG"])
    row_data.append(app["borroers_cell"])
    row_data.append(app["leader_cell"])
    row_data.append(app["leader_cell1"])
    row_data.append(app["guarantor_borrowers_are_nominee"])
    row_data.append(app["borrower_s"])
    row_data.append(app["guranteer_s"])
    row_data.append(app["member_f_or_h_age"])
    row_data.append(app["select_education"])
    row_data.append(app["girl"])
    row_data.append(app["boy"])
    row_data.append(app["p_expense"])
    row_data.append(app["s_expense"])
    row_data.append(app["t_expense"])
    row_data.append(app["i_total"])
    row_data.append(app["e_total"])
    row_data.append(app["member_id_proof_number"])
    row_data.append(app["current_status_updated"])
    row_data.append(app["date_created"])
    row_data.append(app["date_updated"])
    row_data.append(app["excepted_disbursment_date"])
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
            hmresp = EsthenosOrgApplicationHighMark.objects.get(application_id=app.application_id)
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
        user  = EsthenosUser.objects.get(id=c_user.id)
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
    from e_organisation.models import EsthenosOrgApplication
    if request.method == 'GET':
        user  = EsthenosUser.objects.get(id=c_user.id)

        applications = EsthenosOrgApplication.objects.filter(organisation=user.organisation)

        application_data = list()

        hm_request_headers = list()
        hm_request_headers.append("APPLICANT ID TYPE 1")

        headers =  hm_request_headers
        application_data.append(headers)
        for app in applications:
            hm_request = EsthenosOrgApplicationHighMarkRequest.objects.get(applications.application_id)
            row_data = list()
            row_data.append(hm_request["application_id"])

            app_row_data = row_data
            application_data.append(app_row_data)

        output = excel.make_response_from_array(application_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=himark_request_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output