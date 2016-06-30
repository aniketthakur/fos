from celery import Celery
from esthenos import mainapp as app

def make_celery(task_name, broker, resultbackend):
    celery = Celery(task_name, broker=broker)
    celery.conf.update(app.config)
    celery.conf.update({
        "CELERY_MAX_CACHED_RESULTS": 20,
        "CELERY_TASK_RESULT_EXPIRES": 10,
    })

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
