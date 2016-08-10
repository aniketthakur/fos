import os, sys, time, json
import requests, boto
import tempfile, zipfile
from datetime import date
from mongoengine import Q
from e_highmark import parse_response as pr
from job import make_celery
from celery.task import periodic_task
from esthenos.settings import AWS_SETTINGS

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from esthenos import mainapp
from e_organisation.models import *
from utils import make_equifax_request_entry_application_id,make_highmark_request_for_application_id


conn = boto.connect_ses(
    aws_access_key_id=mainapp.config.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=mainapp.config.get("AWS_SECRET_ACCESS_KEY"))

conn_s3 = boto.connect_s3(
    aws_access_key_id=mainapp.config.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=mainapp.config.get("AWS_SECRET_ACCESS_KEY"))

celery = make_celery('esthenos.tasks',mainapp.config['CELERY_BROKER_URL'],mainapp.config['CELERY_RESULT_BACKEND'])


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


def downloadFile(url, outfile):
    start = time.clock()
    with open(outfile, 'wb') as f:
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')
        dl = 0
        if total_length is None: # no content length header
            f.write(r.content)
        else:
            for chunk in r.iter_content(1024):
                dl += len(chunk)
                f.write(chunk)

    return time.clock() - start


def zip_custom(src, dst):
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


@periodic_task(run_every=datetime.timedelta(minutes=15))
@celery.task
def calculate_stats():

    time = datetime.datetime.now()

    for branch in EsthenosOrgBranch.objects.all():
        stats = branch.stats_day(time)
        branch.stats.update(stats, time)

    for area in EsthenosOrgArea.objects.all():
        stats = [branch.stats.month(time).only(time) for branch in area.branches] + [EsthenosOrgStatsDay(created=time)]
        stats = reduce(lambda x, y: x + y, stats)
        area.stats.update(stats, time)

    for region in EsthenosOrgRegion.objects.all():
        stats = [area.stats.month(time).only(time) for area in region.areas] + [EsthenosOrgStatsDay(created=time)]
        stats = reduce(lambda x, y: x + y, stats)
        region.stats.update(stats, time)

    for state in EsthenosOrgState.objects.all():
        stats = [region.stats.month(time).only(time) for region in state.regions] + [EsthenosOrgStatsDay(created=time)]
        stats = reduce(lambda x, y: x + y, stats)
        state.stats.update(stats, time)


@periodic_task(run_every=datetime.timedelta(seconds=60))
@celery.task
def tagged_applications():

    with mainapp.app_context():
        uploaded_applications = EsthenosOrgApplication.objects.filter(status=110)
        for application in uploaded_applications:
            print "DEBUG"
            print application.save, application.house_stay_duration, type(application.house_stay_duration)
            application.update_status(120)
            application.save()


@celery.task
@periodic_task(run_every=datetime.timedelta(seconds=20))
def all_prefilled_applications():

    with mainapp.app_context():
        all_tagged_applications = EsthenosOrgApplication.objects.filter(status=120)
        for application in all_tagged_applications:
            application.update_status(125)
            application.update_status(130)
            application.save()


@celery.task
@periodic_task(run_every=datetime.timedelta(seconds=120))
def cb_checkready_applications():

    all_cbcheckready_applications = EsthenosOrgApplication.objects.filter(status=130)

    if len(all_cbcheckready_applications) > 0:
        mainapp.logger.debug("SENDNG APPLICAITONS :%s" % len(all_cbcheckready_applications))
        organisation = all_cbcheckready_applications[0].organisation
        responses_list = pr.get_highmark_response_applications(all_cbcheckready_applications)
        mainapp.logger.debug("applications for cb_checkready_highmark_applications :%s" % len(all_cbcheckready_applications))


@periodic_task(run_every=datetime.timedelta(seconds=20))
def cbcheck_statuscheck_applications():

    settings = EsthenosOrgSettings.objects.all()[0]
    cbcheck_applications = EsthenosOrgApplication.objects.filter(status=145)
    for application in cbcheck_applications:
        resp = EsthenosOrgApplicationEqifaxResponse.objects.filter(kendra_or_centre_id=application.application_id)
        if not len(resp): continue

        resp = resp[0]
        apps_with_same_aadhaar = EsthenosOrgApplication.objects.filter(applicant_kyc__kyc_number=resp.national_id_card).count()

        is_failed = False
        if apps_with_same_aadhaar > 1:
            is_failed = True
            for app in apps_with_same_aadhaar:
                if app.application_id != application.application_id:
                    application.update_status(25)
                    application.update_status(20)
                    break

        if not is_failed and resp.num_active_account > settings.max_existing_loan_count_org:
            is_failed = True
            application.update_status(26)
            application.update_status(20)

        if not is_failed and resp.sum_overdue_amount > 0:
            is_failed = True
            application.update_status(20)

        if not is_failed:
           application.update_status(160)

        application.save()


@periodic_task(run_every=datetime.timedelta(minutes=1))
def cashflow_ready_applications():
    applications = EsthenosOrgApplication.objects.filter(status=160)

    for application in applications:
        application.update_status(170)
        application.save()


@periodic_task(run_every=datetime.timedelta(minutes=1))
def scrutiny_ready_applications():
    applications = EsthenosOrgApplication.objects.filter(status=187)

    for application in applications:
        application.update_status(190)
        application.update_status(191)
        application.save()


@periodic_task(run_every=datetime.timedelta(minutes=1))
def sanction_ready_applications():
    applications = EsthenosOrgApplication.objects.filter(status=193)

    for application in applications:
        application.update_status(200)
        application.update_status(201)
        application.save()


@periodic_task(run_every=datetime.timedelta(minutes=1))
def underwriting_applications():
    applications = EsthenosOrgApplication.objects.filter(status=203)

    for application in applications:
        application.update_status(230)
        application.update_status(231)
        application.save()


@periodic_task(run_every=datetime.timedelta(minutes=1))
def disbursement_applications():
    applications = EsthenosOrgApplication.objects.filter(status=231)

    for application in applications:
        application.update_status(240)
        application.save()


@celery.task
def generate_post_grt_applications(org_id, applicant_id, disbursement_date, first_collection_after_indays):
    with mainapp.app_context():
        org = EsthenosOrg.objects.get(id=org_id)
        application = EsthenosOrgApplication.objects.get(organisation=org, application_id=applicant_id, status__gte=240)
        tmp_files = list()
        dir = tempfile.mkdtemp( prefix='pdf_')
        dir = dir+"/"
        tf = dir+ "dpn.pdf"

        #generate dpn here
        downloadFile("http://localhost:8080/internal/pdf_dpn/"+applicant_id,tf)
        tmp_files.append(tf)

        #generate agreement here
        tf = dir+ "agreement.pdf"
        downloadFile("http://localhost:8080/internal/pdf_la/"+applicant_id+"/"+disbursement_date,tf)
        tmp_files.append(tf)

        #generate sanction letter
        tf = dir+"sanction_letter.pdf"
        downloadFile("http://localhost:8080/internal/pdf_sl/"+applicant_id,tf)
        tmp_files.append(tf)

        #generate schedule 1
        tf = dir+"schedule_1.pdf"
        downloadFile("http://localhost:8080/internal/pdf_sd_1/"+applicant_id,tf)
        tmp_files.append(tf)

        #generate payment schedule
        tf = dir+"payment_schedule.pdf"
        downloadFile("http://localhost:8080/internal/pdf_ps/"+applicant_id,tf)
        tmp_files.append(tf)

        #generate continutiy letter
        tf = dir+"continuity_letter.pdf"
        downloadFile("http://localhost:8080/internal/pdf_cl/"+applicant_id,tf)
        tmp_files.append(tf)


        #generate processing fees
        tf = dir+"processing_fees.pdf"
        downloadFile("http://localhost:8080/internal/pdf_pf/"+applicant_id,tf)
        tmp_files.append(tf)

        #generate insurance fees
        tf = dir+"insurance_fees.pdf"
        downloadFile("http://localhost:8080/internal/pdf_if/"+applicant_id,tf)
        tmp_files.append(tf)

        #generate insurance fees
        tf = dir+"hccs_receipt.pdf"
        downloadFile("http://localhost:8080/internal/pdf_hccs_reciept/"+applicant_id,tf)
        tmp_files.append(tf)

        tf = dir+applicant_id+"passbook.pdf"
        downloadFile("http://localhost:8080/internal/pdf_hp/"+applicant_id+"/"+disbursement_date+"/"+str(1234)+"/"+str(1234)+"/"+str(first_collection_after_indays),tf)
        tmp_files.append(tf)

        tf = dir+applicant_id+"_application.pdf"
        downloadFile("http://localhost:8080/internal/pdf_application/"+applicant_id,tf)
        tmp_files.append(tf)

        zdir = tempfile.mkdtemp( prefix='zip_')
        zdir = zdir+"/"

        tf = zdir+applicant_id
        zip_custom(dir, tf)

        from boto.s3.key import Key
        bucket = conn_s3.get_bucket(AWS_SETTINGS['AWS_S3_BUCKET'])
        k = Key(bucket)
        k.key = tf+".zip"
        k.set_contents_from_filename(tf+".zip")
        os.remove(tf+".zip")

        application.disbursement_pdf_link = k.key
        application.save()


if __name__ == '__main__':
    celery.start()
