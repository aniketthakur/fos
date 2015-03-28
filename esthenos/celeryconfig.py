__author__ = 'prathvi'

from celery.schedules import crontab

CELERY_IMPORTS=("esthenos.tasks",)

CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'esthenos.tasks.prefill_applications',
        'schedule': crontab(minute='*/1'),
        'args': (),
    },
}