#!/usr/bin/python

from tasks import  *
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')

@sched.scheduled_job('interval', minutes=3)
def timed_job2():
    print('This job is run every three minutes.')
    send_organisation_notification_today.apply_async()


@sched.scheduled_job('cron', day_of_week='mon-sat', hour=4,minute=25)
def notification_1():
    send_organisation_notification_today.apply_async()
    print('This job is running at 9hrs 55 min.')


@sched.scheduled_job('cron', day_of_week='mon-sat', hour=12,minute=25)
def notification_2():
    send_organisation_notification_today.apply_async()
    print('This job is running at 17hrs 55 min.')


@sched.scheduled_job('cron', day_of_week='mon-sat', hour=14,minute=45)
def notification_3():
    send_organisation_notification_as_on.apply_async()
    print('This job is running at 18hrs 0 min.')


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()


def send_organisation_notification_as_on():
    orgs = EsthenosOrg.objects.all()
    for org in orgs:
        app_submitted_total = 1000
        app_submitted_success = 800
        app_submitted_fail = 200
        data_entry_total = 00
        data_entry_success = 00
        data_entry_fail = 00
        kyc_entry_total = 00
        kyc_entry_success = 00
        kyc_entry_fail = 00
        kyc_validation_total = 2000
        kyc_validation_success = 1980
        kyc_validation_fail = 20
        cb_check_total = 1980
        cb_check_success = 1800
        cb_check_fail = 180
        cb_check_total = 1980
        cf_analysis_total  = 1800
        cf_analysis_success  = 1600
        cf_analysis_fail  = 200
        cgt_ready_total  = 1800
        cgt_ready_success  = 1600
        cgt_ready_fail  = 200
        cgt1_done_total  = 1000
        cgt1_done_success  = 900
        cgt1_done_fail  = 100
        cgt2_done_total  = 900
        cgt2_done_success  = 800
        cgt2_done_fail  = 100
        grt_ready_total  = 800
        grt_ready_success  = 700
        grt_ready_fail  = 100
        grt_done_total  = 700
        grt_done_success  = 600
        grt_done_fail  = 100
        dd_done_total = 500
        disbursed_total = 400
        users = EsthenosUser.objects.filter(organisation=org)
        for user in users:
            kwargs = locals()
            html_data = render_template("email/notification_today.html", **kwargs)
            conn.send_email(mainapp.config["SERVER_EMAIL"], "Collections Stats",None,[user.email],format="html" ,html_body=html_data)


def send_organisation_notification_today():
    orgs = EsthenosOrg.objects.all()
    for org in orgs:
        app_submitted_total = 100
        app_submitted_success = 80
        app_submitted_fail = 20
        data_entry_total = 0
        data_entry_success = 0
        data_entry_fail = 0
        kyc_entry_total = 0
        kyc_entry_success = 0
        kyc_entry_fail = 0
        kyc_validation_total = 200
        kyc_validation_success = 198
        kyc_validation_fail = 2
        cb_check_total = 198
        cb_check_success = 180
        cb_check_fail = 18
        cb_check_total = 198
        cf_analysis_total  = 180
        cf_analysis_success  = 160
        cf_analysis_fail  = 20
        cgt_ready_total  = 180
        cgt_ready_success  = 160
        cgt_ready_fail  = 20
        cgt1_done_total  = 100
        cgt1_done_success  = 90
        cgt1_done_fail  = 10
        cgt2_done_total  = 90
        cgt2_done_success  = 80
        cgt2_done_fail  = 10
        grt_ready_total  = 80
        grt_ready_success  = 70
        grt_ready_fail  = 10
        grt_done_total  = 70
        grt_done_success  = 60
        grt_done_fail  = 10
        dd_done_total = 50
        disbursed_total = 40
        users = EsthenosUser.objects.filter(organisation=org)
        for user in users:
            kwargs = locals()
            html_data = render_template("email/notification_today.html", **kwargs)
            conn.send_email(mainapp.config["SERVER_EMAIL"], "Collections Stats",None,[user.email],format="html" ,html_body=html_data)
