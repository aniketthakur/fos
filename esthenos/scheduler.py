#!/usr/bin/python

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
from tasks import  *
@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')

@sched.scheduled_job('interval', minutes=3)
def timed_job2():
    print('This job is run every three minutes.')


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