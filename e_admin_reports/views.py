import os, tempfile
import json, hashlib, pyexcel
from flask.ext import excel
from flask import Flask, make_response
from flask import  Blueprint
from flask import render_template, request,Response
from flask_login import current_user, login_required

from esthenos.crossdomain import *
from esthenos.utils import random_with_N_digits
from e_tokens.utils import login_or_key_required
from e_admin.models import EsthenosUser
from e_organisation.models import EsthenosOrgApplicationHighMarkRequest,EsthenosOrgApplicationHighMarkResponse,EsthenosOrgApplicationEqifaxResponse
from e_reports.views import get_application_headers,get_application_rowdata

storage_path =  os.path.join(os.curdir,'pitaya/uploads')
admin_reports_views = Blueprint('admin_reports_views', __name__, template_folder='templates')

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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



@admin_reports_views.route('/admin/cbcheck/highmark/', methods=["POST"])
@login_or_key_required
def himark_request_reports_import():
    c_user = current_user
    kwargs = locals()
    print request.files
    if request.method == 'POST' and 'file' in request.files:
        # handle file upload
        filename = request.files['file'].filename
        extension = filename.split(".")[1]
        # Obtain the file extension and content
        # pass a tuple instead of a file name
        sheet = pyexcel.load_from_memory(extension, request.files['file'].read())
        # then use it as usual
        data = pyexcel.to_dict(sheet)
        for k,v in data.items():
            if k != "Series_1":
                print k,v[0]
                hm_resp=EsthenosOrgApplicationHighMarkResponse()
                hm_resp.application_id=v[0]
                hm_resp.sent_status=v[1]
                hm_resp.segment_identifier=v[2]
                hm_resp.credit_request_type=v[3]
                hm_resp.credit_report_transaction_id=v[4]
                hm_resp.credit_inquiry_purpose_type=v[5]
                hm_resp.credit_inquiry_purpose_type_description=v[6]
                hm_resp.credit_inquiry_stage=v[7]
                hm_resp.credit_report_transaction_date_time=v[8]
                hm_resp.applicant_name1=v[9]
                hm_resp.applicant_name2=v[10]
                hm_resp.applicant_name3=v[11]
                hm_resp.applicant_name4=v[12]
                hm_resp.applicant_name5=v[13]
                hm_resp.member_father_name=v[14]
                hm_resp.member_mother_name=v[15]
                hm_resp.member_spouse_name=v[16]
                hm_resp.member_relationship_type1=v[17]
                hm_resp.member_relationship_name1=v[18]
                hm_resp.member_relationship_type2=v[19]
                hm_resp.member_relationship_name2=v[20]
                hm_resp.member_relationship_type3=v[21]
                hm_resp.member_relationship_name3=v[22]
                hm_resp.member_relationship_type4=v[23]
                hm_resp.member_relationship_name4=v[24]
                hm_resp.applicant_birth_date=v[25]
                if not is_number(v[26]):
                    v[26] = 0
                hm_resp.applicant_age=v[26]
                hm_resp.applicant_age_as_on_date=v[27]
                hm_resp.applicant_id_type1=v[28]
                hm_resp.applicant_id1=v[29]
                hm_resp.applicant_id_type2=v[30]
                hm_resp.applicant_id2=v[31]
                hm_resp.acct_open_date=v[32]
                hm_resp.applicant_id__account_no=v[33]
                hm_resp.branch_id=v[34]
                hm_resp.member_id=v[35]
                hm_resp.kendra_id=v[36]
                if not is_number(v[37]):
                    v[37] = 0
                hm_resp.applied_for_amount__current_balance=v[37]
                hm_resp.key_person_name=v[38]
                hm_resp.key_person_relation=v[39]
                hm_resp.nominee_name=v[40]
                hm_resp.applicant_telephone_number_type1=v[41]
                hm_resp.applicant_telephone_number1=v[42]
                hm_resp.applicant_telephone_number_type2=v[43]
                hm_resp.applicant_telephone_number2=v[44]
                hm_resp.applicant_address_type1=v[45]
                hm_resp.applicant_address1=v[46]
                hm_resp.applicant_address1_city=v[47]
                hm_resp.applicant_address1_state=v[48]
                hm_resp.applicant_address1_pincode=v[49]
                hm_resp.applicant_address_type2=v[50]
                hm_resp.applicant_address2=v[51]
                hm_resp.applicant_address2_city=v[52]
                hm_resp.applicant_address2_state=v[53]
                hm_resp.applicant_address2_pincode=v[54]
                hm_resp.nominee_relationship_type=v[55]


    return Response(json.dumps({'status':'sucess'}), content_type="application/json", mimetype='application/json')

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
        #application_data.append(headers)
        for org in organisations:
            applications = EsthenosOrgApplication.objects.filter(organisation=org,status__gte=100,status__lte=150)
            for app in applications:
                try:
                    hm_request = EsthenosOrgApplicationHighMarkResponse.objects.filter(application_id=app.application_id)[0]
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

from e_organisation.models import EsthenosOrgApplicationStatus,EsthenosOrgApplicationStatusType
import datetime
@admin_reports_views.route('/admin/cbcheck/equifax/', methods=["POST"])
@login_or_key_required
def equifax_request_reports_import():
    c_user = current_user
    kwargs = locals()
    print request.files
    if request.method == 'POST' and 'file' in request.files:
        # handle file upload
        filename = request.files['file'].filename
        extension = filename.split(".")[1]
        # Obtain the file extension and content
        # pass a tuple instead of a file name
        sheet = pyexcel.load_from_memory(extension, request.files['file'].read())
        # then use it as usual
        data = pyexcel.to_dict(sheet)
        for k,v in data.items():
            if k != "Series_1":
                print k,v[0]

                applications = EsthenosOrgApplication.objects.filter(application_id=v[21])
                if len(applications)>0:
                    application = applications[0]
                    print application
                    status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=application.current_status_updated)
                    status.save()
                    application.timeline.append(status)

                    application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=145)[0]
                    application.current_status_updated  = datetime.datetime.now()
                    application.status = 145
                    application.save()

                    eq_resp = EsthenosOrgApplicationEqifaxResponse()
                    eq_resp.report_id=v[0]   #IntField(default=0)
                    eq_resp.reference_number=v[1]   #IntField(default=0)
                    eq_resp.unique_account_number=str(v[2])   #IntField(default=0)
                    eq_resp.date_of_issue=v[3]   #StringField(max_length=255,required=False,default="")
                    eq_resp.member_name=v[4]   #StringField(max_length=255,required=False,default="")
                    eq_resp.date_of_birth=v[5]   #StringField(max_length=255,required=False,default="")
                    eq_resp.addl_name_type1=v[6]   #StringField(max_length=255,required=False,default="")
                    eq_resp.addl_name1=v[7]   #StringField(max_length=255,required=False,default="")
                    eq_resp.addl_name_type2=v[8]   #StringField(max_length=255,required=False,default="")
                    eq_resp.addl_name2=v[9]   #StringField(max_length=255,required=False,default="")
                    eq_resp.national_id_card=str(v[10])   #StringField(max_length=255,required=False,default="")
                    eq_resp.passport=v[11]   #StringField(max_length=255,required=False,default="")
                    eq_resp.ration_card=v[12]   #StringField(max_length=255,required=False,default="")
                    eq_resp.voter_id=v[13]   #StringField(max_length=255,required=False,default="")
                    eq_resp.pan_card=v[14]   #StringField(max_length=255,required=False,default="")
                    eq_resp.additional_id1=v[15]   #StringField(max_length=255,required=False,default="")
                    eq_resp.additional_id2=v[16]   #StringField(max_length=255,required=False,default="")
                    eq_resp.address=v[17]   #StringField(max_length=255,required=False,default="")
                    eq_resp.state=v[18]   #StringField(max_length=255,required=False,default="")
                    eq_resp.postal=v[19]   #StringField(max_length=255,required=False,default="")
                    eq_resp.branch_id=v[20]   #StringField(max_length=255,required=False,default="")
                    eq_resp.kendra_or_centre_id=v[21]   #StringField(max_length=255,required=False,default="")
                    if not is_number(v[22]):
                        v[22] = 0
                    eq_resp.own_mfi_indicator=v[22]   #IntField(default=0)
                    if not is_number(v[23]):
                        v[23] = 0
                    eq_resp.total_responses=v[23]   #IntField(default=0)
                    if not is_number(v[24] ):
                        v[24] = 0
                    eq_resp.total_responses_own=v[24]   #IntField(default=0)
                    if not is_number(v[25] ):
                        v[25] = 0
                    eq_resp.total_responses_others=v[25]   #IntField(default=0)
                    if not is_number(v[26] ):
                        v[26] = 0
                    eq_resp.num_of_other_mfis=v[26]   #IntField(default=0)
                    if not is_number(v[27] ):
                        v[27] = 0
                    eq_resp.num_active_account=v[27]   #IntField(default=0)
                    application.total_running_loans = eq_resp.num_active_account
                    if not is_number(v[28] ):
                        v[28] = 0
                    eq_resp.num_active_account_own=v[28]   #IntField(default=0)
                    if not is_number(v[29] ):
                        v[29] = 0
                    eq_resp.num_active_account_other=v[29]   #IntField(default=0)
                    application.total_running_loans_from_mfi = eq_resp.num_active_account_other
                    if not is_number(v[30] ):
                        v[30] = 0
                    eq_resp.num_closed_account=v[30]   #IntField(default=0)
                    if not is_number(v[31] ):
                        v[31] = 0
                    eq_resp.num_closed_account_own=v[31]   #IntField(default=0)
                    if not is_number(v[32] ):
                        v[32] = 0
                    eq_resp.num_closed_account_other=v[32]   #IntField(default=0)
                    if not is_number(v[33] ):
                        v[33] = 0
                    eq_resp.num_past_due_account=v[33]   #IntField(default=0)
                    application.defaults_with_no_mfis=int(v[33])   #IntField(default=0)
                    if not is_number(v[34] ):
                        v[34] = 0
                    eq_resp.num_past_due_account_own=v[34]   #IntField(default=0)
                    if not is_number(v[35] ):
                        v[35] = 0
                    eq_resp.num_past_due_account_other=v[35]   #IntField(default=0)
                    if not is_number(v[36] ):
                        v[36] = 0
                    eq_resp.sum_current_balance=float(v[36])   #IntField(default=0)
                    application.total_existing_outstanding_from = eq_resp.sum_current_balance
                    application.loan_eligibility_based_on_company_policy= 50000-application.total_existing_outstanding_from
                    if not is_number(v[37] ):
                        v[37] = 0
                    eq_resp.sum_current_balance_own=float(v[37])   #IntField(default=0)
                    if not is_number(v[38] ):
                        v[38] = 0
                    eq_resp.sum_current_balance_other=float(v[38])   #IntField(default=0)
                    application.total_existing_outstanding_from_mfi = eq_resp.sum_current_balance_other
                    if not is_number(v[39] ):
                        v[39] = 0
                    eq_resp.sum_disbursed=float(v[39])   #IntField(default=0)
                    if not is_number(v[40] ):
                        v[40] = 0
                    eq_resp.sum_disbursed_own=float(v[40])   #IntField(default=0)
                    if not is_number(v[41] ):
                        v[41] = 0
                    eq_resp.sum_disbursed_other=float(v[41])   #IntField(default=0)
                    if not is_number(v[42] ):
                        v[42] = 0
                    eq_resp.sum_installment_amount=float(v[42])   #IntField(default=0)
                    if not is_number(v[43] ):
                        v[43] = 0
                    eq_resp.sum_installment_amount_own=float(v[43])   #IntField(default=0)
                    if not is_number(v[44] ):
                        v[44] = 0
                    eq_resp.sum_installment_amount_other=float(v[44])   #IntField(default=0)
                    if not is_number(v[45] ):
                        v[45] = 0
                    eq_resp.sum_overdue_amount=float(v[45])   #IntField(default=0)
                    if not is_number(v[46] ):
                        v[46] = 0
                    eq_resp.sum_overdue_amount_own=float(v[46])   #IntField(default=0)
                    if not is_number(v[47] ):
                        v[47] = 0
                    eq_resp.sum_overdue_amount_other=float(v[47])   #IntField(default=0)
                    if not is_number(v[48] ):
                        v[48] = 0
                    eq_resp.sum_writtenoff_amount=float(v[48])   #IntField(default=0)
                    if not is_number(v[49] ):
                        v[49] = 0
                    eq_resp.sum_writtenoff_amount_own=float(v[49])   #IntField(default=0)
                    if not is_number(v[50] ):
                        v[50] = 0
                    eq_resp.sum_writtenoff_amount_other=float(v[50])   #IntField(default=0)
                    if not is_number(v[51] ):
                        v[51] = 0
                    eq_resp.num_writtenoff_account=float(v[51])   #IntField(default=0)

                    if not is_number(v[52] ):
                        v[52] = 0
                    eq_resp.num_writtenoff_account_own=float(v[52])   #IntField(default=0)
                    if not is_number(v[53] ):
                        v[53] = 0
                    eq_resp.num_writtenoff_accountnon_own=float(v[53])   #IntField(default=0)
                    eq_resp.save()
                    application.save()


    return Response(json.dumps({'status':'sucess'}), content_type="application/json", mimetype='application/json')

@admin_reports_views.route('/admin/cbcheck/equifax/download', methods=["GET"])
@login_or_key_required
def eqifax_request_reports():
    c_user = current_user
    kwargs = locals()
    from e_organisation.models import EsthenosOrgApplicationEqifax,EsthenosOrg
    if request.method == 'GET':
        organisations = EsthenosOrg.objects.all()
        application_data = list()
        application_data.append(list())
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
        print organisations
        for org in organisations:

            applications = EsthenosOrgApplication.objects.filter(organisation=org,status__gte=100,status__lte=150)

            for app in applications:
                print app.applicant_name
                try:
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
                    row_data.append("MH") #eq_request["state_union_territory"]
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
