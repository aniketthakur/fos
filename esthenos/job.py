__author__ = 'prathvi'

from celery import Celery
from esthenos  import mainapp as app

def make_celery(task_name,broker=None,resultbackend=None):
    print app.import_name

    if broker is None:
        broker = app.config['CELERY_BROKER_URL']

    if resultbackend == None:
        resultbackend = app.config['CELERY_RESULT_BACKEND']

    celery = Celery(task_name,backend=resultbackend ,broker=broker)
    celery.conf.update(app.config)
    #from esthenos  import celeryconfig
    #celery.config_from_object(celeryconfig)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
