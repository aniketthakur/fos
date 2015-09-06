ORGS_SETTINGS = [
    {
        "org" : "fos.esthenos.com",
        "name" : "FOS1 Demo MicroFinance Pvt. Ltd.",
        "email": "admin-org@fos.esthenos.com",
        "phone": "9876543210",
        "phone-code": "91",
        "postal-city": "Kolaba",
        "postal-code": "123321",
        "postal-state": "Bolaka",
        "postal-address": "12, Bolak New Kada",
        "postal-country": "India",
        "users" : [
            {
                "role" : "executive",
                "fname" : "demo",
                "lname" : "users",
                "email" : "demo",
                "passwd" : "demodemo",
                "mobile" : "+91-9876543210"
            }
        ]
    }
]

SERVER_SETTINGS = {
    "org" : "fos.esthenos.com",
    "host" : ["fos.prod.esthenos.com"],
    "user-deploy" : "ubuntu",
    "user-provision" : "root",    
    "user-details" : [
        {
            "role" : "admin",
            "fname" : "admin",
            "lname" : "users",
            "email" : "admin",
            "passwd" : "adminadmin",
            "mobile" : "+91-9876543210"
        }
    ]
}

MONGODB_SETTINGS = {
    'DB': 'testdb1',
    'PORT': 41583,
    'HOST': 'ds041583.mongolab.com',
    'USERNAME': 'test-user',
    'PASSWORD': 'test-password'
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
    "hignmark_equifax": False,
    
    "questions_grt": False,
    "questions_cgt1": False,
    "questions_cgt2": False,
    "questions_telecalling": False,
    "questions_psychometric": True,
    
    "accounts_reports": True,
    "accounts_scrutiny": True,
    "accounts_sanctions": True,
    "accounts_applications": True,
    "accounts_enroll_customers": False,
}


APP_STATUS = [
    {
        'status' : 'APPLICATION_CHECK_FAILED',
        'status_code' : 10,
        'status_message' : 'Quality Checked Failed',
        'sub_status' : 'CRITERIA_FAILED_BAD_DOCUMENT',
        'sub_status_code' : 5
    },
    {
        'status' : 'APPLICATION_CHECK_FAILED',
        'status_message' : 'Quality Check Failed',
        'status_code' : 10,
        'sub_status_code' : 11,
        'sub_status' : 'CRITERIA_FAILED_MISSING_DOCUMENTS'
    },
    {
        'status' : 'APPLICATION_KYC_CRITERIA_FAILED',
        'status_message' : 'Invalid/Fake Pancard',
        'status_code' : 15,
        'sub_status_code' : 1,
        'sub_status' : 'CRITERIA_FAILED_KYC_PAN_INVALID'
    },
    {
        'status' : 'APPLICATION_KYC_CRITERIA_FAILED',
        'status_message' : 'Invalid/Fake Aadhaar card',
        'status_code' : 15,
        'sub_status_code' : 2,
        'sub_status' : 'CRITERIA_FAILED_KYC_AADHAAR_INVALID'
    },
    {
        'status' : 'APPLICATION_KYC_CRITERIA_FAILED',
        'status_message' : "Invalid/Fake Voter's Id",
        'status_code' : 15,
        'sub_status_code' : 3,
        'sub_status' : 'CRITERIA_FAILED_KYC_VOTERSID_INVALID'
    },
    {
        'status' : 'APPLICATION_CF_CRITERIA_FAILED',
        'status_message' : 'Borrower defaulted in 1 or more MFIs',
        'status_code' : 20,
        'sub_status_code' : 1,
        'sub_status' : 'CRITERIA_FAILED_CF_DEFAULTS'
    },
    {
        'status' : 'APPLICATION_CF_CRITERIA_FAILED',
        'status_message' : "Borrower's AADHAAR is submitted previously",
        'status_code' : 25,
        'sub_status_code' : 2,
        'sub_status' : 'CRITERIA_FAILED_DUPLICATE_AADHAAR'
    },
    {
        'status' : 'APPLICATION_UPLOADED',
        'status_message' : 'Your application is uploaded to system',
        'status_code' : 100
    },
    {
        'status' : 'APPLICATION_TAGGED',
        'status_message' : 'Application is tagged and ready of data entry',
        'status_code' : 110
    },
    {
        'status' : 'APPLICATION_PREFILLED',
        'status_message' : 'Application is prefilled first round of checking',
        'status_code' : 120
    },
    {
        'status' : 'APPLICATION_KYC_VALIDATION_PASSED',
        'status_message' : 'Application KYC has completed, validation successful',
        'status_code' : 125
    },
    {
        'status' : 'APPLICATION_CBCHECK_READY',
        'status_message' : 'Application data entry done and ready for CB Check',
        'status_code' : 130
    },
    {
        'status' : 'APPLICATION_CBCHECK_SUBMITED',
        'status_message' : 'Application CB Check has completed, waiting for results',
        'status_code' : 140
    },
    {
        'status' : 'APPLICATION_CBCHECK_RETURNED',
        'status_message' : 'Application CB Check results arrived',
        'status_code' : 145
    },
    {
        'status' : 'APPLICATION_CBCHECK_SUCCESS',
        'status_message' : 'Application CB Check has completed, validation cashflow analysis',
        'status_code' : 150
    },
    {
        'status' : 'APPLICATION_CASH_FLOW_READY',
        'status_message' : 'Application is Cash Flow Ready',
        'status_code' : 160
    },
    {
        'status' : 'APPLICATION_CASH_FLOW_PASSED',
        'status_message' : 'Application Cash Flow has Passed',
        'status_code' : 170
    },
    {
        'status' : 'APPLICATION_CASH_FLOW_FAILED',
        'status_message' : 'Application  Cash Flow has Failed, failed in one or multiple criteria match',
        'status_code' : 180
    },
    {
        'status' : 'APPLICATION_CGT1_READY',
        'status_message' : 'Application is CGT1 Ready',
        'status_code' : 190
    },
    {
        'status' : 'APPLICATION_CGT1_PENDING',
        'status_message' : 'Application is CGT1 Pending',
        'status_code' : 200
    },
    {
        'status' : 'APPLICATION_CGT1_FAILED',
        'status_message' : 'Application has failed CGT1',
        'status_code' : 210
    },
    {
        'status' : 'APPLICATION_CGT2_READY',
        'status_message' : 'Application is CGT2 Ready',
        'status_code' : 220
    },
    {
        'status' : 'APPLICATION_CGT2_PENDING',
        'status_message' : 'Application is CGT2 Pending',
        'status_code' : 230
    },
    {
        'status' : 'APPLICATION_CGT2_FAILED',
        'status_message' : 'Application has failed CGT2',
        'status_code' : 240
    },
    {
        'status' : 'APPLICATION_GRT_READY',
        'status_message' : 'Application is GRT Ready',
        'status_code' : 250
    },
    {
        'status' : 'APPLICATION_GRT_PENDING',
        'status_message' : 'Application is GRT Pending',
        'status_code' : 260
    },
    {
        'status' : 'APPLICATION_GRT_FAILED',
        'status_message' : 'Application has failed GRT',
        'status_code' : 270
    },
    {
        'status' : 'APPLICATION_GRT_DONE',
        'status_message' : 'Application GRT Done',
        'status_code' : 272
    },
    {
        'status' : 'APPLICATION_TELECALLING_PASSED',
        'status_message' : 'Application tele calling has passed.',
        'status_code' : 276
    },
    {
        'status' : 'APPLICATION_TELECALLING_FAILED',
        'status_message' : 'Application tele calling has failed.',
        'status_code' : 278
    },
    {
        'status' : 'APPLICATION_UNDERWRITING_READY',
        'status_message' : 'Application is under-writing ready.',
        'status_code' : 280
    },
    {
        'status' : 'APPLICATION_UNDERWRITING_DONE',
        'status_message' : 'Application Under-writing done.',
        'status_code' : 290
    },
    {
        'status' : 'APPLICATION_DISBURSEMENT_READY',
        'status_message' : 'Application Disbursement ready',
        'status_code' : 300
    },
    {
        'status' : 'APPLICATION_DISBURSEMENT_CANCELLED',
        'status_message' : 'Application Disbursement has been cancelled,possibly due to CGT-GRT failure',
        'status_code' : 310
    },
    {
        'status' : 'APPLICATION_DISBURSEMENT_PENDING',
        'status_message' : 'Application Disbursement ready, waiting for disbursement over a week',
        'status_code' : 320
    }
]
