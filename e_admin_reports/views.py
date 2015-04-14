__author__ = 'prathvi'
# Flask and Flask-SQLAlchemy initialization here
from flask import render_template, request,Response
from flask_login import current_user, login_required
from e_tokens.utils import login_or_key_required
import json,hashlib
from e_admin.models import EsthenosUser
from e_organisation.models import EsthenosOrgApplicationHighMarkRequest,EsthenosOrgApplicationHighMarkResponse
from flask import  Blueprint
import os,tempfile
from esthenos.crossdomain import *
from esthenos.utils import random_with_N_digits
#import flickr_api
#flickr_api.set_keys(api_key = "8766ced6ec90eb38a32778e847a83233", api_secret = "cda7061fdbd608fd")
storage_path =  os.path.join(os.curdir,'pitaya/uploads')
admin_reports_views = Blueprint('admin_reports_views', __name__,
    template_folder='templates')

from flask.ext import excel
from flask import Flask, make_response
from reports.views import get_application_headers,get_application_rowdata
@admin_reports_views.route('/admin/reports/internal_main/download', methods=["GET"])
@login_or_key_required
def admin_internal_main_reports():
    c_user = current_user
    kwargs = locals()
    from e_organisation.models import EsthenosOrgApplication
    if request.method == 'GET':
        user  = EsthenosUser.objects.get(id=c_user.id)

        app_headers = get_application_headers()
        app_headers.append("Organisation Name")

        applications = EsthenosOrgApplication.objects.all()

        application_data = list()


        headers = app_headers
        application_data.append(headers)
        for app in applications:
            app_row_data= get_application_rowdata(app)
            app_row_data.append(app.organisation.name)
            app_row_data = app_row_data
            application_data.append(app_row_data)

        output = excel.make_response_from_array(application_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=internal_main_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output

from e_organisation.models import EsthenosOrgApplication,EsthenosOrg

@admin_reports_views.route('/admin/cbcheck/highmark/download', methods=["GET"])
@login_or_key_required
def himark_request_reports():
    c_user = current_user
    kwargs = locals()

    if request.method == 'GET':
        organisations = EsthenosOrg.objects.all()
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
        for org in organisations:
            applications = EsthenosOrgApplication.objects.filter(organisation=org,status_code=7)
            for app in applications:
                try:
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
                except Exception as e:
                    print e.message

        output = excel.make_response_from_array(application_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=himark_request_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output

@admin_reports_views.route('/admin/cbcheck/equifax/download', methods=["GET"])
@login_or_key_required
def eqifax_request_reports():
    c_user = current_user
    kwargs = locals()
    from e_organisation.models import EsthenosOrgApplicationEqifax,EsthenosOrg
    if request.method == 'GET':
        organisations = EsthenosOrg.objects.all()
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

        for org in organisations:

            applications = EsthenosOrgApplication.objects.filter(organisation=org,status_code=7)

            for app in applications:
                try:
                    eq_request = EsthenosOrgApplicationEqifax.objects.get(application_id=app.application_id)
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
                except Exception as e:
                    print e.message

        output = excel.make_response_from_array(application_data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=eqifax_request_reports.csv"
        output.headers["Content-type"] = "text/csv"
        return output