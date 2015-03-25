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


@periodic_task(run_every=datetime.timedelta(minutes=5))
def queue_processor():
    print "queue processor"
    today = datetime.datetime.now()
    Year,WeekNum,DOW = today.isocalendar()
    # connect to another MongoDB server altogether


if __name__ == '__main__':
    celery.start()
