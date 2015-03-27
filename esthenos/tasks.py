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

conn = None
dirname,file_name = os.path.split(os.path.abspath(__file__))
root_dir = os.path.join(dirname,"data")+"/"
from celery.task import periodic_task

from job import make_celery
celery = make_celery('esthenos.tasks',mainapp.config['CELERY_BROKER_URL'],mainapp.config['CELERY_RESULT_BACKEND'])

from e_organisation.models import EsthenosOrgApplication,EsthenosOrgApplicationStatusType
#from e_admin.models import EsthenosOrgApplication

@periodic_task(run_every=datetime.timedelta(minutes=1))
def all_tagged_applications():
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
        application.timeline.append(application.current_status)
        application.timeline.append(EsthenosOrgApplicationStatusType.objects.filter(status_code=5)[0])
        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=7)[0]
        application.save()
from initdb import make_sample_highmark_request_for_application_id,add_sample_highmark_response
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
        application.timeline.append(application.current_status)
        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=8)[0]
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
        application.timeline.append(application.current_status)
        application.timeline.append(EsthenosOrgApplicationStatusType.objects.filter(status_code=9)[0])
        #below line will change according to status and validation done for highmark
        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=11)[0]
        application.save()

@periodic_task(run_every=datetime.timedelta(minutes=1))
def cashflow_ready_applications():
    print "queue processor"
    today = datetime.datetime.now()
    Year,WeekNum,DOW = today.isocalendar()
    # connect to another MongoDB server altogether
    status_cashflow_ready = EsthenosOrgApplicationStatusType.objects.filter(status_code=11)[0]
    cashflow_ready_applications = EsthenosOrgApplication.objects.filter(current_status=status_cashflow_ready)

    for application in cashflow_ready_applications:
        application.timeline.append(application.current_status)
        #below line will change according to status and validation done for highmark
        application.current_status = EsthenosOrgApplicationStatusType.objects.filter(status_code=9)[0]
        application.save()


if __name__ == '__main__':
    celery.start()
