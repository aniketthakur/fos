__author__ = 'prathvi'
from esthenos import mainapp
import sys
import os,tempfile
import datetime
from bson import  ObjectId
import hashlib
import traceback
import  urllib2
import pymongo
import json
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from esthenos import mainapp
conn = None
dirname,file_name = os.path.split(os.path.abspath(__file__))
root_dir = os.path.join(dirname,"data")+"/"
from celery.task import periodic_task
from pixuate_storage_digikyc import get_url_with_id
from pixuate import get_aadhaar_details_url,get_pan_details_url,get_vid_details_url
from job import make_celery
from e_organisation.models import EsthenosOrg
from e_admin.models import EsthenosUser
celery = make_celery('esthenos.tasks',mainapp.config['CELERY_BROKER_URL'],mainapp.config['CELERY_RESULT_BACKEND'])

import boto
conn = boto.connect_ses(
    aws_access_key_id=mainapp.config.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=mainapp.config.get("AWS_SECRET_ACCESS_KEY"))


conn_s3 = boto.connect_s3(
    aws_access_key_id=mainapp.config.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=mainapp.config.get("AWS_SECRET_ACCESS_KEY"))
from esthenos import render_template,mainapp

from e_organisation.models import EsthenosOrgApplication,EsthenosOrgApplicationStatusType,EsthenosOrgApplicationStatus,EsthenosOrgApplicationKYC,EsthenosOrgStats
#from e_admin.models import EsthenosOrgApplication
from datetime import date

def calculate_age(born):
    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year, month=born.month+1, day=1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year



@periodic_task(run_every=datetime.timedelta(seconds=60))
@celery.task
def org_applications_stats_update():
    organisations = EsthenosOrg.objects.all()
    for org in organisations:
        date_obj =  datetime.datetime.now()
        date_obj.day
        stat = EsthenosOrgStats.objects.get_or_create(organisation=org)

        stat.stat_type = ""

    pass


@periodic_task(run_every=datetime.timedelta(seconds=60))
@celery.task
def tagged_applications():
    with mainapp.app_context():
        print "in prefill applications"
        uploaded_applications = EsthenosOrgApplication.objects.filter(status=110)
        """
    {'query_url': u'http://api.pixuate.com/objects/55041d942a76201b0bf035ff/b48eead256efd179e211c141e82ede0a_p.jpg'}
    {"scan_result": [{"DOB": "31/03/1989", "Father's/Organisation Name": "ASHOK SHARMA  ", "Name": "HARSH SHARMA  ", "PAN": "CTZPS1166F", "raw": " \n\n\nINCOME TAX DEPARTMENT\n\n\nHARSH SHARMA\n\n\nASHOK SHARMA\n\n\n31/03/1989\n\n\nEer11'1anenfAccount Number\n\n\nCTZPS1166F\n\n\n"}], "validation_result": "PENDING"}
    127.0.0.1 - - [28/Mar/2015 01:24:00] "GET /admin/read_pan/5515a5682a762065ac21c974 HTTP/1.1" 200 -
    {"scan_result": [{"VID": "XKP/0560292", "DOB": "09/11/1987", "Gender": "Female", "raw": " is-1:\n33 3.1\n'.. .'.S\"u-1\nWfiirasan\n\nIDENTITY\n. qn4 Hi...\nCOMMISSION\nELECTION\n\n./J\nU31\nW3-T1171\n1'eFcTTTFf\nOF\nINDIA\nCARD\namfm\nXKP/0560292\nHE\nIEEIET\n71TH\n09/11/1987\nDate of Birth\nElectors Name\nTrFHa'v1aTiITG\nWIHI/WEI '\nEm .\nWW\nF ather's/Husband's\n/ Female\nSex\n1511\n3111\nIE-3131\nDINESH BATARANA\nDIPIKA BATARANA\nWWFIT\nEWIYFIT\n", "Elector's Name": " DIPIKA BATARANA", "Father's/Mother's/Husband's Name": " DINESH BATARANA"}], "validation_result": "PENDING"}
    127.0.0.1 - - [28/Mar/2015 01:24:25] "GET /admin/read_vid/5515a56f2a762065ac21c975 HTTP/1.1" 200 -
    {"scan_result": {"vtc": "Lakkireddipalle", "co": "S/O Fyroz Basha", "name": "Pattan Saddam Hussain", "gender": "M", "state": "Andhra Pradesh", "raw": "\n\nv. V1V   1 .V .'r \n  :   1 ,  ,/J4... 4.u.n..L\nFun\ni 26515 26rgv'75a 7.'Ixi'fo 35\nPattan Saddam Hussain\n", "year_of_birth": "1992", "house": "4/166", "aadhaar_id": "565061987998", "dist": "Cuddapah"}, "validation_result": "PENDING"}
        """
        print "processing "+ str(len(uploaded_applications))+" applications"
        for application in uploaded_applications:
            cur_index = 1
            for kyc_id_key in application.tag.kyc_file_pixuate_id.keys():
                kyc_id = application.tag.kyc_file_pixuate_id[kyc_id_key]
                url = get_url_with_id(kyc_id)
                if str(kyc_id_key) == "p":
                    rawdata = get_pan_details_url(url)
                    data = json.loads(rawdata)["scan_result"][0]
                    #{"scan_result": [{"DOB": "31/03/1989", "Father's/Organisation Name": "ASHOK SHARMA  ", "Name": "HARSH SHARMA  ", "PAN": "CTZPS1166F", "raw": " \n\n\nINCOME TAX DEPARTMENT\n\n\nHARSH SHARMA\n\n\nASHOK SHARMA\n\n\n31/03/1989\n\n\nEer11'1anenfAccount Number\n\n\nCTZPS1166F\n\n\n"}], "validation_result": "PENDING"}
                    kyc = EsthenosOrgApplicationKYC()
                    if "Name" in data.keys():
                        kyc.name =  data["Name"].strip()
                        application.applicant_name = kyc.name
                    if "Father's/Organisation Name" in data.keys():
                        kyc.father_or_husband_name =  data["Father's/Organisation Name"].strip()
                        application.member_f_or_h_name = kyc.father_or_husband_name
                    if "PAN" in data.keys():
                        kyc.kyc_number = data["PAN"].strip()
                    if "DOB" in data.keys():
                        kyc.dob = data["DOB"].strip()
                    kyc.raw = data["raw"]
                    kyc.validation = json.loads(rawdata)["validation_result"]
                    if cur_index == 1:
                        application.kyc_1 = kyc
                    else:
                        application.kyc_2 = kyc

                if str(kyc_id_key) == "v":
                    rawdata = get_vid_details_url(url)
                    data = json.loads(rawdata)["scan_result"][0]
                    #{"scan_result": [{"VID": "XKP/0560292", "DOB": "09/11/1987", "Gender": "Female", "raw": " is-1:\n33 3.1\n'.. .'.S\"u-1\nWfiirasan\n\nIDENTITY\n. qn4 Hi...\nCOMMISSION\nELECTION\n\n./J\nU31\nW3-T1171\n1'eFcTTTFf\nOF\nINDIA\nCARD\namfm\nXKP/0560292\nHE\nIEEIET\n71TH\n09/11/1987\nDate of Birth\nElectors Name\nTrFHa'v1aTiITG\nWIHI/WEI '\nEm .\nWW\nF ather's/Husband's\n/ Female\nSex\n1511\n3111\nIE-3131\nDINESH BATARANA\nDIPIKA BATARANA\nWWFIT\nEWIYFIT\n", "Elector's Name": " DIPIKA BATARANA", "Father's/Mother's/Husband's Name": " DINESH BATARANA"}], "validation_result": "PENDING"}
                    kyc = EsthenosOrgApplicationKYC()
                    if "Elector's Name" in data.keys():
                        kyc.name =  data["Elector's Name"].strip()
                    if "Father's/Mother's/Husband's Name" in data.keys():
                        kyc.father_or_husband_name =  data["Father's/Mother's/Husband's Name"].strip()
                    if "VID" in data.keys():
                        kyc.kyc_number = data["VID"].strip()
                    if "Gender" in data.keys():
                        kyc.gender = data["Gender"].strip()
                    if "DOB" in data.keys():
                        kyc.dob = data["DOB"].strip()

                    if "Address" in data.keys():
                        kyc.address1 = data["Address"].strip()
                    if "Pincode" in data.keys():
                        kyc.pincode = data["Pincode"].strip()
                    kyc.raw = data["raw"]
                    kyc.validation = json.loads(rawdata)["validation_result"]
                    if cur_index == 1:
                        application.kyc_1 = kyc
                    else:
                        application.kyc_2 = kyc

                if str(kyc_id_key) == "a":
                    rawdata = get_aadhaar_details_url(url)
                    data = json.loads(rawdata)["scan_result"]
                    #{"scan_result": {"vtc": "Lakkireddipalle", "co": "S/O Fyroz Basha", "name": "Pattan Saddam Hussain", "gender": "M", "state": "Andhra Pradesh", "raw": "\n\nv. V1V   1 .V .'r \n  :   1 ,  ,/J4... 4.u.n..L\nFun\ni 26515 26rgv'75a 7.'Ixi'fo 35\nPattan Saddam Hussain\n", "year_of_birth": "1992", "house": "4/166", "aadhaar_id": "565061987998", "dist": "Cuddapah"}, "validation_result": "PENDING"}
                    kyc = EsthenosOrgApplicationKYC()
                    kyc.name =  data["name"].strip()
                    kyc.father_or_husband_name =  data["co"].strip()
                    kyc.kyc_number = data["aadhaar_id"].strip()
                    kyc.gender = data["gender"].strip()
                    if "state" in data.keys():
                        kyc.state = data["state"].strip()
                    if "pincode" in data.keys():
                        kyc.pincode = data["pincode"].strip()
                    if "house" in data.keys() and "vtc" in data.keys() and "dist" in data.keys():
                        kyc.address1 = data["house"]+ ", " +data["vtc"] + ", " +data["dist"]
                        application.address = kyc.address1
                    if "vtc" in data.keys() and "dist" in data.keys():
                        kyc.address1 = data["vtc"] + ", " +data["dist"]
                    if "year_of_birth" in data.keys():
                        kyc.dob = data["year_of_birth"]
                        application.age = calculate_age(datetime.datetime(year=int(kyc.dob), month=1, day=1).date())
                    kyc.raw = data["raw"]
                    kyc.validation = json.loads(rawdata)["validation_result"]
                    if cur_index == 1:
                        application.kyc_1 = kyc
                    else:
                        application.kyc_2 = kyc
                cur_index = cur_index+1

            for gkyc_id_key in application.tag.gkyc_file_pixuate_id.keys():
                gkyc_id = application.tag.gkyc_file_pixuate_id[gkyc_id_key]
                url = get_url_with_id(gkyc_id)
                if str(gkyc_id_key) == "p":
                    rawdata = get_pan_details_url(url)
                    data = json.loads(rawdata)["scan_result"][0]
                    #{"scan_result": [{"DOB": "31/03/1989", "Father's/Organisation Name": "ASHOK SHARMA  ", "Name": "HARSH SHARMA  ", "PAN": "CTZPS1166F", "raw": " \n\n\nINCOME TAX DEPARTMENT\n\n\nHARSH SHARMA\n\n\nASHOK SHARMA\n\n\n31/03/1989\n\n\nEer11'1anenfAccount Number\n\n\nCTZPS1166F\n\n\n"}], "validation_result": "PENDING"}
                    kyc = EsthenosOrgApplicationKYC()
                    if "Name" in data.keys():
                        kyc.name =  data["Name"].strip()
                    if "Father's/Organisation Name" in data.keys():
                        kyc.father_or_husband_name =  data["Father's/Organisation Name"].strip()
                    if "PAN" in data.keys():
                        kyc.kyc_number = data["PAN"].strip()
                    if "DOB" in data.keys():
                        kyc.dob = data["DOB"].strip()
                    kyc.raw = data["raw"]
                    kyc.validation = json.loads(rawdata)["validation_result"]
                    application.gkyc_1 = kyc
                if str(gkyc_id_key) == "v":
                    rawdata = get_vid_details_url(url)
                    data = json.loads(rawdata)["scan_result"][0]
                    #{"scan_result": [{"VID": "XKP/0560292", "DOB": "09/11/1987", "Gender": "Female", "raw": " is-1:\n33 3.1\n'.. .'.S\"u-1\nWfiirasan\n\nIDENTITY\n. qn4 Hi...\nCOMMISSION\nELECTION\n\n./J\nU31\nW3-T1171\n1'eFcTTTFf\nOF\nINDIA\nCARD\namfm\nXKP/0560292\nHE\nIEEIET\n71TH\n09/11/1987\nDate of Birth\nElectors Name\nTrFHa'v1aTiITG\nWIHI/WEI '\nEm .\nWW\nF ather's/Husband's\n/ Female\nSex\n1511\n3111\nIE-3131\nDINESH BATARANA\nDIPIKA BATARANA\nWWFIT\nEWIYFIT\n", "Elector's Name": " DIPIKA BATARANA", "Father's/Mother's/Husband's Name": " DINESH BATARANA"}], "validation_result": "PENDING"}
                    kyc = EsthenosOrgApplicationKYC()
                    if "Elector's Name" in data.keys():
                        kyc.name =  data["Elector's Name"].strip()
                    if "Father's/Mother's/Husband's Name" in data.keys():
                        kyc.father_or_husband_name =  data["Father's/Mother's/Husband's Name"].strip()
                    if "VID" in data.keys():
                        kyc.kyc_number = data["VID"].strip()
                    if "Gender" in data.keys():
                        kyc.gender = data["Gender"].strip()
                    if "DOB" in data.keys():
                        kyc.dob = data["DOB"].strip()
                    if "Address" in data.keys():
                        kyc.address1 = data["Address"].strip()
                    if "Pincode" in data.keys():
                        kyc.pincode = data["Pincode"].strip()
                    kyc.raw = data["raw"]
                    kyc.validation = json.loads(rawdata)["validation_result"]
                    application.gkyc_1 = kyc
                if str(gkyc_id_key) == "a":
                    rawdata = get_aadhaar_details_url(url)
                    data = json.loads(rawdata)["scan_result"]
                    #{"scan_result": {"vtc": "Lakkireddipalle", "co": "S/O Fyroz Basha", "name": "Pattan Saddam Hussain", "gender": "M", "state": "Andhra Pradesh", "raw": "\n\nv. V1V   1 .V .'r \n  :   1 ,  ,/J4... 4.u.n..L\nFun\ni 26515 26rgv'75a 7.'Ixi'fo 35\nPattan Saddam Hussain\n", "year_of_birth": "1992", "house": "4/166", "aadhaar_id": "565061987998", "dist": "Cuddapah"}, "validation_result": "PENDING"}
                    kyc = EsthenosOrgApplicationKYC()
                    kyc.name =  data["name"].strip()
                    kyc.father_or_husband_name =  data["co"].strip()
                    kyc.kyc_number = data["aadhaar_id"].strip()
                    kyc.gender = data["gender"].strip()
                    if "state" in data.keys():
                        kyc.state = data["state"].strip()
                    if "pincode" in data.keys():
                        kyc.pincode = data["pincode"].strip()
                    if "house" in data.keys() and "vtc" in data.keys() and "dist" in data.keys():
                        kyc.address1 = data["house"]+ ", " +data["vtc"] + ", " +data["dist"]
                    if "vtc" in data.keys() and "dist" in data.keys():
                        kyc.address1 = data["vtc"] + ", " +data["dist"]
                    if "year_of_birth" in data.keys():
                        kyc.dob = data["year_of_birth"]
                    kyc.raw = data["raw"]
                    kyc.validation = json.loads(rawdata)["validation_result"]
                    application.gkyc_1 = kyc

            application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=120)[0]
            application.current_status_updated  = datetime.datetime.now()
            application.status = 120
            application.save()

@celery.task
@periodic_task(run_every=datetime.timedelta(seconds=20))
def all_prefilled_applications():
    with mainapp.app_context():
        print "queue processor"
        today = datetime.datetime.now()
        Year,WeekNum,DOW = today.isocalendar()
        # connect to another MongoDB server altogether
        all_tagged_applications = EsthenosOrgApplication.objects.filter(status=120)

        for application in all_tagged_applications:
            if application.kyc_1 != None:
                #check for validation status and accordingly set the status
                pass
            if application.kyc_2 != None:
                #check for validation status and accordingly set the status
                pass
            if application.gkyc_1 != None:
                #check for validation status and accordingly set the status
                pass

            status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=application.current_status_updated)
            status.save()
            application.timeline.append(status)

            status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=125)[0],updated_on=datetime.datetime.now())
            status.save()
            application.timeline.append(status)

            application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=130)[0]
            application.current_status_updated  = datetime.datetime.now()
            application.status = 130

            application.save()

from utils import make_equifax_request_entry_application_id,make_highmark_request_for_application_id
@celery.task
@periodic_task(run_every=datetime.timedelta(seconds=120))
def cb_checkready_applications():
    print "queue processor"
    today = datetime.datetime.now()
    Year,WeekNum,DOW = today.isocalendar()
    # connect to another MongoDB server altogether
    all_cbcheckready_applications = EsthenosOrgApplication.objects.filter(status=130)

    for application in all_cbcheckready_applications:
        make_equifax_request_entry_application_id(application.application_id)
        make_highmark_request_for_application_id(application.application_id)
        status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=application.current_status_updated)
        status.save()
        application.timeline.append(status)

        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=140)[0]
        application.current_status_updated  = datetime.datetime.now()
        application.status = 140
        application.save()

from e_organisation.models import EsthenosOrgApplicationEqifaxResponse
@periodic_task(run_every=datetime.timedelta(seconds=20))
def cbcheck_statuscheck_applications():
    print "queue processor"
    today = datetime.datetime.now()
    Year,WeekNum,DOW = today.isocalendar()
    # connect to another MongoDB server altogether
    cbcheck_statuscheck_applications = EsthenosOrgApplication.objects.filter(status=145)

    for application in cbcheck_statuscheck_applications:
        status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=application.current_status_updated)
        status.save()
        application.timeline.append(status)
        resp = EsthenosOrgApplicationEqifaxResponse.objects.filter(kendra_or_centre_id=application.application_id)[0]
        apps_with_same_aadhaar =  EsthenosOrgApplication.objects.filter(kyc_1__kyc_number=resp.national_id_card)
        is_failed = False
        if len(apps_with_same_aadhaar)>1:
            is_failed = True
            print "duplicate aadhaar found"
            for app in apps_with_same_aadhaar:
                if app.application_id != application.application_id:
                    print "duplicate aadhaar found in "+app.application_id
                    status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=25)[0],updated_on=datetime.datetime.now())
                    status.status_message = "duplicate aadhaar found in "+app.application_id
                    status.save()
                    application.timeline.append(status)
                    break
        if resp.num_active_account > 2:
            is_failed = True
            print "number of active loans 2+"+application.application_id
            status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=25)[0],updated_on=datetime.datetime.now())
            status.status_message = "number of active loans 2+"
            status.save()
            application.timeline.append(status)
            break
        if resp.sum_overdue_amount > 0:
            is_failed = True
            print "number of defaults 1+"+application.application_id
            status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=20)[0],updated_on=datetime.datetime.now())
            status.status_message = "number of defaults 1+"
            status.save()
            application.timeline.append(status)
            break
        if not is_failed:
            status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=150)[0],updated_on=datetime.datetime.now())
            status.save()
            application.timeline.append(status)

            #below line will change according to status and validation done for highmark
            application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=160)[0]
            application.current_status_updated  = datetime.datetime.now()
            application.status = 160
            application.save()

@periodic_task(run_every=datetime.timedelta(minutes=1))
def cashflow_ready_applications():
    print "queue processor"
    today = datetime.datetime.now()
    Year,WeekNum,DOW = today.isocalendar()
    # connect to another MongoDB server altogether
    cashflow_ready_applications = EsthenosOrgApplication.objects.filter(status=160)

    for application in cashflow_ready_applications:
        status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=application.current_status_updated)
        status.save()
        application.timeline.append(status)


        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=170)[0],updated_on=datetime.datetime.now())
        status.save()
        application.timeline.append(status)

        #update cgt_grt links
        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=190)[0]
        application.current_status_updated  = datetime.datetime.now()
        application.status = 190
        application.save()

import os
import zipfile
import StringIO
from dateutil.relativedelta import relativedelta
import pdfkit
import tempfile
from e_organisation.models import EsthenosOrgGroup
@celery.task
def generate_post_grt_applications(org_id,group_id,disbursement_date,first_collection_after_indays):
    print "generate_post_grt_applications"
    group = EsthenosOrgGroup.objects.get(group_id=group_id)
    #org = EsthenosOrg.objects.get(id=org_id)
    apps = EsthenosOrgApplication.objects.filter(group=group)
    product = apps[0].product
    tmp_files = list()
    dir = tempfile.mkdtemp( prefix='pdf_')
    dir = dir+"/"
    tf = dir+ "dpn.pdf"
    print tf
    #generate dpn here
    kwargs = locals()
    body = render_template( "pdf_HMPL_DPN_HINDI.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.50in',
            'margin-right': '0.50in',
            'margin-bottom': '0.50in',
            'margin-left': '0.50in',
            'encoding': "UTF-8",
            'orientation' : 'Portrait'
        }
        open(tf, 'w').close()
        pdfkit.from_string(body, tf,options=options)
        tmp_files.append(tf)

    except Exception as e:
        print e.message

    #generate agreement here
    tf = dir+ "agreement.pdf"
    kwargs = locals()
    body = render_template( "pdf_HMPL_LA_Hindi.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.25in',
            'margin-bottom': '0.75in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'orientation' : 'Portrait'
        }
        open(tf, 'w').close()
        pdfkit.from_string(body, tf,options=options)
        tmp_files.append(tf)
    except Exception as e:
        print e.message

    loan_amount = 20000.0

    second_collection_after_indays = 30
    first_emi = 1100
    rate_of_interest= .260/12.0
    current_principal = loan_amount
    passbook_rows = list()
    for i in range(1,25):
        row= dict()
        interest = 0.0
        if(i==1):
            interest = first_collection_after_indays/30.0 * rate_of_interest  * current_principal
        else:
            interest = second_collection_after_indays/30.0 * rate_of_interest * current_principal
        date_after_month = disbursement_date.today()+ relativedelta(months=i)
        import math
        interest = math.ceil(interest * 1000)/1000.0
        frac, whole = math.modf(interest)
        if frac>0.5:
            interest = whole+1
        else:
            interest = whole

        row["date"] = str(disbursement_date.day)+"/"+date_after_month.strftime("%b")+"/"+str(date_after_month.year)
        row["interest"] = interest
        row["prev_os"] = current_principal
        current_principal = current_principal-(first_emi - interest)
        row["principal"] = (first_emi - interest)

        if i==24:
            row["emi"] = first_emi+current_principal
            current_principal= 0
        else:
            row["emi"] = first_emi
        row["next_os"] = current_principal

        passbook_rows.append(row)

    #generate passbook here
    for app in apps:


        tf = dir+ app.application_id+"passbook.pdf"
        kwargs = locals()
        body = render_template( "pdf_HindustanPassbook.html", **kwargs)
        try:
            options = {
                'page-size': 'A4',
                'margin-top': '0.15in',
                'margin-right': '0.0in',
                'margin-bottom': '0.15in',
                'margin-left': '0.0in',
                'encoding': "UTF-8",
                'orientation' : 'Landscape'
            }
            open(tf, 'w').close()
            pdfkit.from_string(body, tf,options=options)
            tmp_files.append(tf)
        except Exception as e:
            print "in exception"
            print e.message


    #generate sanction letter
    tf = dir+"sanction_letter.pdf"
    org_name = "Hindustan Microfinance"
    kwargs = locals()
    body = render_template( "pdf_Sanction_Letter.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.35in',
            'margin-right': '0.25in',
            'margin-bottom': '0.35in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'orientation' : 'Landscape'
        }
        open(tf, 'w').close()
        pdfkit.from_string(body, tf,options=options)
        tmp_files.append(tf)
    except Exception as e:
        print e.message

    #generate processing fees
    tf = dir+"processing_fees.pdf"
    org_name = "Hindustan Microfinance"
    kwargs = locals()
    body = render_template( "pdf_Processing_Fees.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.35in',
            'margin-right': '0.25in',
            'margin-bottom': '0.35in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'orientation' : 'Landscape'
        }
        open(tf, 'w').close()
        pdfkit.from_string(body, tf,options=options)
        tmp_files.append(tf)
    except Exception as e:
        print e.message


    #generate insurance fees
    tf = dir+"insurance_fees.pdf"
    org_name = "Hindustan Microfinance"
    kwargs = locals()
    body = render_template( "pdf_InsuranceFees.html", **kwargs)
    try:
        options = {
            'page-size': 'A4',
            'margin-top': '0.35in',
            'margin-right': '0.25in',
            'margin-bottom': '0.35in',
            'margin-left': '0.25in',
            'encoding': "UTF-8",
            'orientation' : 'Landscape'
        }
        open(tf, 'w').close()
        pdfkit.from_string(body, tf,options=options)
        tmp_files.append(tf)
    except Exception as e:
        print e.message

    print tmp_files
    filenames = tmp_files

    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better

    zdir = tempfile.mkdtemp( prefix='zip_')
    zdir = zdir+"/"
    # The zip compressor
    tf = zdir+group_id
    zip(dir, tf)
    from boto.s3.key import Key
    bucket = conn_s3.get_bucket("hindusthanarchives")
    k = Key(bucket)
    k.key = tf+".zip"
    k.set_contents_from_filename(tf+".zip")
    k.make_public()
    os.remove(tf+".zip")
    group.disbursement_pdf_link = k.key
    group.save()


import os
import zipfile

def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
    zf.close()

@periodic_task(run_every=datetime.timedelta(minutes=1))
def cgt_grt_success_applications():
    print "queue processor"
    today = datetime.datetime.now()
    Year,WeekNum,DOW = today.isocalendar()
    # connect to another MongoDB server altogether
    cgt_grt_success_applications = EsthenosOrgApplication.objects.filter(status=280)

    for application in cgt_grt_success_applications:
        status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=application.current_status_updated)
        status.save()
        application.timeline.append(status)
        #here we generate pdf for disbursement

        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=300)[0]
        application.current_status_updated  = datetime.datetime.now()
        application.status = 300
        application.save()

if __name__ == '__main__':
    celery.start()
