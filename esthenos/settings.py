ORGS_SETTINGS = [
    {
        "org" : "fos-test.esthenos.com",
        "name" : "FOS Test MicroFinance Pvt. Ltd.",
        "email": "admin@fos-test.esthenos.com",
        "phone": "9876543210",
        "phone-code": "91",
        "postal-city": "Kolaba",
        "postal-code": "123321",
        "postal-state": "Bolaka",
        "postal-address": "12, Bolak New Kada",
        "postal-country": "India",
        "users" : [
            {
                "role" : "ORG_ADMIN",
                "active" : True,
                "dob" : "01/01/1970",
                "city" : "kabul",
                "state" : "kabula",
                "country" : "kabuland",
                "address" : "1st kabul, kaula, kabuland.",
                "telephone" : "9876543210",
                "tele_code" : "91",
                "fname" : "admin",
                "lname" : "users",
                "email" : "admin@fos-test.esthenos.com",
                "passwd" : "adminadmin",
            },
            {
                "role" : "ORG_CM",
                "active" : True,
                "dob" : "01/01/1970",
                "city" : "kabul",
                "state" : "kabula",
                "country" : "kabuland",
                "address" : "1st kabul, kaula, kabuland.",
                "telephone" : "9876543210",
                "tele_code" : "91",
                "fname" : "demo",
                "lname" : "users",
                "email" : "demo@fos-test.esthenos.com",
                "passwd" : "demodemo",
            }
        ],
        "hierarchy" : [
            {"level": 0, "access": "",          "role": "ORG_ADMIN",  "title": "admin",  "title_full": "organisation administrator"},
            {"level": 1, "access": "",          "role": "ORG_CXO",    "title": "cxo",    "title_full": "chief executive officer"},
            {"level": 2, "access": "",          "role": "ORG_VP",     "title": "vp",     "title_full": "vice president"},
            {"level": 3, "access": "states",    "role": "ORG_ZH",     "title": "sh",     "title_full": "state head"},
            {"level": 4, "access": "regions",   "role": "ORG_SH",     "title": "cm",     "title_full": "cluster manager"},
            {"level": 5, "access": "regions",   "role": "ORG_RM",     "title": "dm",     "title_full": "divisional manager"},
            {"level": 6, "access": "areas",     "role": "ORG_AM",     "title": "cm",     "title_full": "center area manager"},
            {"level": 7, "access": "branches",  "role": "ORG_BM",     "title": "com",    "title_full": "center branch manager"},
            {"level": 8, "access": "centers",   "role": "ORG_CM",     "title": "co",     "title_full": "center officer"}
        ],
        "geography" : {
            "states" : 1,
            "regions" : 1,
            "areas" : 1,
            "branches" : 2,
            "groups" : 0,
            "centers" : 0,
        }
    }
]

SERVER_SETTINGS = {
    "org" : "fos-test.esthenos.com",
    "host" : ["fos-test.prod.esthenos.com"],
    "git-branch" : "fos-test",
    "user-deploy" : "ubuntu"
}

MONGODB_SETTINGS = {
    'DB': 'fos-test',
    'PORT': 27017,
    'HOST': 'mongodb.prod.esthenos.com'
}

CELERY_SETTINGS = {
    'CELERY_BROKER_URL' : 'amqp://esthenos-tasks:esthenos@127.0.0.1:5672//esthenos-tasks',
    'CELERY_RESULT_BACKEND' : 'amqp://esthenos-tasks:esthenos@127.0.0.1:5672//esthenos-tasks'
}

AWS_SETTINGS = {
    'AWS_S3_BUCKET' : 'hindusthanarchives',
    'AWS_COGNITO_ID' : 'us-east-1:58e9693d-04b4-48a1-8820-b17c52514aaa',
    'AWS_ACCESS_KEY_ID' : 'AKIAITWBEHC2SAGDFQSA',
    'AWS_SECRET_ACCESS_KEY' : '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'
}

FEATURES = {
    "features_admin": {
        "title" : "Admin Features",
        "enabled": True,
    },
    "features_profile": {
        "title" : "Features For User Profile",
        "enabled": True,
    },
    "features_notifications": {
        "title" : "Features For Notifications",
        "enabled": True,
    },
    "features_api_products": {
        "title" : "Features For API Products",
        "enabled": True,
    },
    "features_api_applications_post": {
        "title" : "Features For API Application POST",
        "enabled": True,
    },
    "features_api_performance_target": {
        "title" : "Features For API Performance Target",
        "enabled": True,
    },
    "features_fos_branches": {
        "title" : "Features For FOS & Branches List",
        "enabled" : True,
    },
    "features_applications_track": {
        "title" : "Features For Applications Track",
        "enabled" : True,
    },
    "features_applications_cashflow": {
        "title" : "Features For Applications Cashflow",
        "enabled" : True,
    },
    "features_applications_scrutiny": {
        "title" : "Features For Application Scrutiny",
        "enabled" : True,
    },
    "features_applications_sanction": {
        "title" : "Features For Application Scrutiny",
        "enabled" : True,
    },
    "features_applications_scrutiny_stats": {
        "title" : "Stats For Application Scrutiny",
        "enabled" : False,
    },
    "features_applications_disbursement": {
        "title" : "Features For Disbursement",
        "enabled": True,
    },
    "features_psychometric_questions": {
        "title" : "Features For Notifications",
        "enabled": True,
    },
    "hignmark_equifax": {
        "title" : "HighMark / Equifax Verification",
        "enabled" : True,
    },
    "search_by_app_id": {
        "title" : "Search By Application ID",
        "enabled" : True,
    },
    "search_by_app_name": {
        "title" : "Search By Application Name",
        "enabled" : True,
    },
    "search_by_group_id": {
        "title" : "Search By Group ID",
        "enabled" : True,
    },
    "search_by_group_name": {
        "title" : "Search By Group Name",
        "enabled" : True,
    },
    "search_by_center_id": {
        "title" : "Search By Center ID",
        "enabled" : True,
    },
    "search_by_center_name": {
        "title" : "Search By Center Name",
        "enabled" : True,
    },
    "search_by_scrutiny_status": {
        "title" : "Search By Scrutiny Status",
        "enabled" : False,
    },
    "accounts_reports": {
        "title" : "Features For Reports",
        "enabled" : True,
    }
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
        'status' : 'APPLICATION_CF_CRITERIA_FAILED',
        'status_message' : "Borrower's has more than on active loans",
        'status_code' : 26,
        'sub_status_code' : 2,
        'sub_status' : 'CRITERIA_FAILED_MULTIPLE_ACTIVE_LOANS'
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
        'status' : 'APPLICATION_SCRUTINY_READY',
        'status_message' : 'Application is Ready for Scrutiny',
        'status_code' : 190
    },
    {
        'status' : 'APPLICATION_SCRUTINY_PENDING',
        'status_message' : 'Application Scrutiny Pending',
        'status_code' : 191
    },
    {
        'status' : 'APPLICATION_SCRUTINY_FAILED',
        'status_message' : 'Application Scrutiny failed',
        'status_code' : 192
    },
    {
        'status' : 'APPLICATION_SCRUTINY_PASSED',
        'status_message' : 'Application Scrutiny Passed',
        'status_code' : 193
    },
    {
        'status' : 'APPLICATION_SCRUTINY_ONHOLD',
        'status_message' : 'Application Scrutiny OnHold',
        'status_code' : 194
    },
    {
        'status' : 'APPLICATION_SANCTION_READY',
        'status_message' : 'Application is Ready for Sanction',
        'status_code' : 200
    },
    {
        'status' : 'APPLICATION_SANCTION_PENDING',
        'status_message' : 'Application Sanction Pending',
        'status_code' : 201
    },
    {
        'status' : 'APPLICATION_SANCTION_FAILED',
        'status_message' : 'Application Sanction failed',
        'status_code' : 202
    },
    {
        'status' : 'APPLICATION_SANCTION_PASSED',
        'status_message' : 'Application Sanction Passed',
        'status_code' : 203
    },
    {
        'status' : 'APPLICATION_SANCTION_ONHOLD',
        'status_message' : 'Application Sanction OnHold',
        'status_code' : 204
    },
    {
        'status' : 'APPLICATION_UNDERWRITING_READY',
        'status_message' : 'Application is under-writing ready.',
        'status_code' : 230
    },
    {
        'status' : 'APPLICATION_UNDERWRITING_DONE',
        'status_message' : 'Application under-writing done.',
        'status_code' : 231
    },
    {
        'status' : 'APPLICATION_DISBURSEMENT_READY',
        'status_message' : 'Application Disbursement ready',
        'status_code' : 240
    },
    {
        'status' : 'APPLICATION_DISBURSEMENT_CANCELLED',
        'status_message' : 'Application Disbursement has been cancelled,possibly due to CGT-GRT failure',
        'status_code' : 241
    },
    {
        'status' : 'APPLICATION_DISBURSEMENT_PENDING',
        'status_message' : 'Application Disbursement ready, waiting for disbursement over a week',
        'status_code' : 242
    },
    {
        'status' : 'APPLICATION_DISBURSEMENT_DONE',
        'status_message' : 'Application Disbursement Done',
        'status_code' : 243
    }
]
