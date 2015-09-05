SERVER_SETTINGS = {
    "name" : "fos",
    "host" : ["fos.prod.esthenos.com"],
    "user-deploy" : "ubuntu",
    "user-provision" : "root"    
}

MONGODB_SETTINGS = {
    'DB': 'fos',
    'PORT': 61228,
    'HOST': 'ds061228.mongolab.com',
    'USERNAME':'saggraha-user',
    'PASSWORD':'saggraha-password'
}

CELERY_SETTINGS = {
    'CELERY_BROKER_URL' : 'amqp://esthenos-tasks:esthenos@127.0.0.1:5672//esthenos-tasks',
    'CELERY_RESULT_BACKEND' : 'amqp://esthenos-tasks:esthenos@127.0.0.1:5672//esthenos-tasks'
}

AWS_SETTINGS = {
    'AWS_ACCESS_KEY_ID' : 'AKIAITWBEHC2SAGDFQSA',
    'AWS_SECRET_ACCESS_KEY' : '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'
}

FEATURES = {
    "disbursement": True,
    "hignmark_equifax": True,
    
    "questions_grt": True,
    "questions_cgt1": True,
    "questions_cgt2": True,
    "questions_telecalling": True,
    "questions_psychometric": False,
    
    "accounts_reports": True,
    "accounts_scrutiny": True,
    "accounts_sanctions": True,
    "accounts_applications": True,
    "accounts_enroll_customers": False,
}
