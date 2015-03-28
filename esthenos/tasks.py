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
from pixuate_storage import get_url_with_id
from pixuate import get_aadhaar_details_url,get_pan_details_url,get_vid_details_url
from job import make_celery
celery = make_celery('esthenos.tasks',mainapp.config['CELERY_BROKER_URL'],mainapp.config['CELERY_RESULT_BACKEND'])

from e_organisation.models import EsthenosOrgApplication,EsthenosOrgApplicationStatusType,EsthenosOrgApplicationStatus,EsthenosOrgApplicationKYC
#from e_admin.models import EsthenosOrgApplication


@periodic_task(run_every=datetime.timedelta(minutes=2))
def prefill_applications():
    with mainapp.app_context():
        print "in prefill applications"
        status_tagged = EsthenosOrgApplicationStatusType.objects.filter(status_code=0)[0]
        uploaded_applications = EsthenosOrgApplication.objects.filter(current_status=status_tagged)
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
                    if "Father's/Organisation Name" in data.keys():
                        kyc.father_or_husband_name =  data["Father's/Organisation Name"].strip()
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
                    if "vtc" in data.keys() and "dist" in data.keys():
                        kyc.address1 = data["vtc"] + ", " +data["dist"]
                    if "year_of_birth" in data.keys():
                        kyc.dob = data["year_of_birth"]
                    kyc.raw = data["raw"]
                    kyc.validation = json.loads(rawdata)["validation_result"]
                    if cur_index == 1:
                        application.kyc_1 = kyc
                    else:
                        application.kyc_2 = kyc

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

            application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=1)[0]
            application.current_status_updated  = datetime.datetime.now()
            application.status = 1
            application.save()

@periodic_task(run_every=datetime.timedelta(minutes=3))
def all_tagged_applications():
    with mainapp.app_context():
        print "queue processor"
        today = datetime.datetime.now()
        Year,WeekNum,DOW = today.isocalendar()
        # connect to another MongoDB server altogether
        status_tagged = EsthenosOrgApplicationStatusType.objects.filter(status_code=4)[0]
        all_tagged_applications = EsthenosOrgApplication.objects.filter(current_status=status_tagged)

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

            status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=5)[0],updated_on=datetime.datetime.now())
            status.save()
            application.timeline.append(status)

            application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=7)[0]
            application.current_status_updated  = datetime.datetime.now()
            application.status = 7
            application.save()

from utils import make_sample_highmark_request_for_application_id,add_sample_highmark_response
@celery.task
@periodic_task(run_every=datetime.timedelta(minutes=4))
def cb_checkready_applications():
    print "queue processor"
    today = datetime.datetime.now()
    Year,WeekNum,DOW = today.isocalendar()
    # connect to another MongoDB server altogether
    status_cbcheckready = EsthenosOrgApplicationStatusType.objects.filter(status_code=7)[0]
    all_cbcheckready_applications = EsthenosOrgApplication.objects.filter(current_status=status_cbcheckready)

    for application in all_cbcheckready_applications:
        make_sample_highmark_request_for_application_id(application.application_id)
        status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=application.current_status_updated)
        status.save()
        application.timeline.append(status)

        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=8)[0]
        application.current_status_updated  = datetime.datetime.now()
        application.status = 8
        application.save()

@periodic_task(run_every=datetime.timedelta(minutes=3))
def cbcheck_statuscheck_applications():
    print "queue processor"
    today = datetime.datetime.now()
    Year,WeekNum,DOW = today.isocalendar()
    # connect to another MongoDB server altogether
    status_cbchecksent = EsthenosOrgApplicationStatusType.objects.filter(status_code=8)[0]
    cbcheck_statuscheck_applications = EsthenosOrgApplication.objects.filter(current_status=status_cbchecksent)

    for application in cbcheck_statuscheck_applications:
        status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=application.current_status_updated)
        status.save()
        application.timeline.append(status)

        status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=9)[0],updated_on=datetime.datetime.now())
        status.save()
        application.timeline.append(status)

        #below line will change according to status and validation done for highmark
        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=11)[0]
        application.current_status_updated  = datetime.datetime.now()
        application.status = 11
        application.save()

@periodic_task(run_every=datetime.timedelta(minutes=3))
def cashflow_ready_applications():
    print "queue processor"
    today = datetime.datetime.now()
    Year,WeekNum,DOW = today.isocalendar()
    # connect to another MongoDB server altogether
    status_cashflow_ready = EsthenosOrgApplicationStatusType.objects.filter(status_code=12)[0]
    cashflow_ready_applications = EsthenosOrgApplication.objects.filter(current_status=status_cashflow_ready)

    for application in cashflow_ready_applications:
        status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=application.current_status_updated)
        status.save()
        application.timeline.append(status)
        #here we generate pdf
        #update cgt_grt links
        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=14)[0]
        application.current_status_updated  = datetime.datetime.now()
        application.status = 14
        application.save()



@periodic_task(run_every=datetime.timedelta(minutes=3))
@celery.task
def cgt_grt_success_applications():
    print "queue processor"
    today = datetime.datetime.now()
    Year,WeekNum,DOW = today.isocalendar()
    # connect to another MongoDB server altogether
    status_cgt_grt_success = EsthenosOrgApplicationStatusType.objects.filter(status_code=17)[0]
    cgt_grt_success_applications = EsthenosOrgApplication.objects.filter(current_status=status_cgt_grt_success)

    for application in cgt_grt_success_applications:
        status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=application.current_status_updated)
        status.save()
        application.timeline.append(status)
        #here we generate pdf for disbursement

        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=19)[0]
        application.current_status_updated  = datetime.datetime.now()
        application.status = 19
        application.save()

if __name__ == '__main__':
    celery.start()
