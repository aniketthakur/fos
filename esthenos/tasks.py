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

from e_organisation.models import EsthenosOrgApplication,EsthenosOrgApplicationStatusType,EsthenosOrgApplicationStatus
#from e_admin.models import EsthenosOrgApplication

def prefill_applications():

    status_tagged = EsthenosOrgApplicationStatusType.objects.filter(status_code=0)[0]
    uploaded_applications = EsthenosOrgApplication.objects.filter(current_status=status_tagged)

    for application in uploaded_applications:
        kyc_urls = list()
        kyc_ids = application.tag.kyc_file_pixuate_id
        for kyc_id_key in application.tag.kyc_file_pixuate_id.keys():
            kyc_id = application.tag.kyc_file_pixuate_id[kyc_id_key]
            url = get_url_with_id(kyc_id)
            if kyc_id == "p":
                data = get_pan_details_url(url)
            if kyc_id == "a":
                data = get_aadhaar_details_url(url)
            if kyc_id == "v":
                data = get_vid_details_url(url)

        gkyc_urls = list()
        gkyc_ids = application.tag.gkyc_file_pixuate_id
        for gkyc_id_key in application.tag.gkyc_file_pixuate_id.keys():
            gkyc_id = application.tag.gkyc_file_pixuate_id[gkyc_id_key]
            url = get_url_with_id(gkyc_id)
            if kyc_id == "p":
                data = get_pan_details_url(url)
            if kyc_id == "a":
                data = get_aadhaar_details_url(url)
            if kyc_id == "v":
                data = get_vid_details_url(url)


@periodic_task(run_every=datetime.timedelta(minutes=1))
def all_tagged_applications():
    with mainapp.app_context():
        print "queue processor"
        today = datetime.datetime.now()
        Year,WeekNum,DOW = today.isocalendar()
        # connect to another MongoDB server altogether
        status_tagged = EsthenosOrgApplicationStatusType.objects.filter(status_code=4)[0]
        all_tagged_applications = EsthenosOrgApplication.objects.filter(current_status=status_tagged)

        for application in all_tagged_applications:
            if application.kyc_1_pan_card != None:
                pass
            if application.kyc_1_aadhaar_card != None:
                pass
            if application.kyc_1_vid_card != None:
                pass
            if application.kyc_2_aadhaar_card != None:
                pass
            if application.kyc_2_vid_card != None:
                pass
            if application.gkyc_1_pan_card != None:
                pass
            if application.gkyc_1_aadhaar_card != None:
                pass
            if application.gkyc_1_vid_card != None:
                pass
            status = EsthenosOrgApplicationStatus(status = application.current_status,updated_on=application.current_status_updated)
            status.save()
            application.timeline.append(status)

            status = EsthenosOrgApplicationStatus(status = EsthenosOrgApplicationStatusType.objects.filter(status_code=5)[0],updated_on=datetime.datetime.now())
            status.save()
            application.timeline.append(status)

            application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=7)[0]
            application.current_status_updated  = datetime.datetime.now()
            application.save()

from utils import make_sample_highmark_request_for_application_id,add_sample_highmark_response
@periodic_task(run_every=datetime.timedelta(minutes=1))
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
        application.save()

@periodic_task(run_every=datetime.timedelta(minutes=1))
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
        application.save()

@periodic_task(run_every=datetime.timedelta(minutes=1))
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
        application.save()



@periodic_task(run_every=datetime.timedelta(minutes=1))
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
        application.save()

if __name__ == '__main__':
    celery.start()
