#!/usr/bin/python

from e_admin.models import  EsthenosSettings,EsthenosUser
from e_organisation.models import *

organisation = EsthenosOrg.objects.all()
for org in organisation:
    org.delete()


prods = EsthenosOrgProduct.objects.all()
for prod in prods:
    prod.delete()


apps = EsthenosUser.objects.all()
for app in apps:
    app.delete()


user = EsthenosUser.create_user("admin","admin@esthenos.com","Admin312",True)
user.add_role("ADMIN")
user.first_name = "Admin"
user.last_name = ""
user.username = "Admin"
user.active = True
user.save()

if len(EsthenosSettings.objects.all()) ==1:
    EsthenosSettings.objects.all()[0].delete()

settings = EsthenosSettings()
print settings
settings.save()

apps = EsthenosOrgApplication.objects.all()
for app in apps:
    app.delete()

groups = EsthenosOrgGroup.objects.all()
for grp in groups:
    grp.delete()

groups = EsthenosOrgGroupGRTSession.objects.all()
for grp in groups:
    grp.delete()

groups = EsthenosOrgGroupCGT1Session.objects.all()
for grp in groups:
    grp.delete()

groups = EsthenosOrgGroupCGT2Session.objects.all()
for grp in groups:
    grp.delete()

groups = EsthenosOrgIndivijualTeleCallingSession.objects.all()
for grp in groups:
    grp.delete()

status = EsthenosOrgApplicationStatusType.objects.all()
for sta in status:
    sta.delete()



#if len(EsthenosOrgApplicationStatusType.objects.all()) == 0:


status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CHECK_FAILED"
status_type.status_message = "Quality Check Failed"
status_type.status_code = 10
status_type.sub_status_code = 5
status_type.sub_status = "CRITERIA_FAILED_BAD_DOCUMENT"
status_type.save()


status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CHECK_FAILED"
status_type.status_message = "Quality Check Failed"
status_type.status_code = 10
status_type.sub_status_code = 11
status_type.sub_status = "CRITERIA_FAILED_MISSING_DOCUMENTS"
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_KYC_CRITERIA_FAILED"
status_type.status_message = "Invalid/Fake Pancard"
status_type.status_code = 15
status_type.sub_status_code = 1
status_type.sub_status = "CRITERIA_FAILED_KYC_PAN_INVALID"
status_type.save()


status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_KYC_CRITERIA_FAILED"
status_type.status_message = "Invalid/Fake Aadhaar card"
status_type.status_code = 15
status_type.sub_status_code = 2
status_type.sub_status = "CRITERIA_FAILED_KYC_AADHAAR_INVALID"
status_type.save()


status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_KYC_CRITERIA_FAILED"
status_type.status_message = "Invalid/Fake Voter's Id"
status_type.status_code = 15
status_type.sub_status_code = 3
status_type.sub_status = "CRITERIA_FAILED_KYC_VOTERSID_INVALID"
status_type.save()


status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CF_CRITERIA_FAILED"
status_type.status_message = "Borrower defaulted in 1 or more previous MFI's"
status_type.status_code = 20
status_type.sub_status_code = 1
status_type.sub_status = "CRITERIA_FAILED_CF_DEFAULTS"
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CF_CRITERIA_FAILED"
status_type.status_message = "Borrower's AADHAAR is submitted previously"
status_type.status_code = 25
status_type.sub_status_code = 2
status_type.sub_status = "CRITERIA_FAILED_DUPLICATE_AADHAAR"
status_type.save()


status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_UPLOADED"
status_type.status_message = "Your application is uploaded to system"
status_type.status_code = 100
status_type.save()


status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_TAGGED"
status_type.status_message = "Application is tagged and ready of data entry"
status_type.status_code = 110
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_PREFILLED"
status_type.status_message = "Application is prefilled first round of checking"
status_type.status_code = 120
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_KYC_VALIDATION_PASSED"
status_type.status_message = "Application KYC has completed, validation successful"
status_type.status_code = 125
status_type.save()


status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CBCHECK_READY"
status_type.status_message = "Application data entry done and ready for CB Check"
status_type.status_code = 130
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CBCHECK_SUBMITED"
status_type.status_message = "Application CB Check has completed, waiting for results"
status_type.status_code = 140
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CBCHECK_RETURNED"
status_type.status_message = "Application CB Check results arrived"
status_type.status_code = 145
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CBCHECK_SUCCESS"
status_type.status_message = "Application CB Check has completed, validation cashflow analysis"
status_type.status_code = 150
status_type.save()


status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CASH_FLOW_READY"
status_type.status_message = "Application is Cash Flow Ready"
status_type.status_code = 160
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CASH_FLOW_PASSED"
status_type.status_message = "Application Cash Flow has Passed"
status_type.status_code = 170
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CASH_FLOW_FAILED"
status_type.status_message = "Application  Cash Flow has Failed, failed in one or multiple criteria match"
status_type.status_code = 180
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CGT1_READY"
status_type.status_message = "Application is CGT1 Ready"
status_type.status_code = 190
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CGT1_PENDING"
status_type.status_message = "Application is CGT1 Pending"
status_type.status_code = 200
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CGT1_FAILED"
status_type.status_message = "Application has failed CGT1"
status_type.status_code = 210
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CGT2_READY"
status_type.status_message = "Application is CGT2 Ready"
status_type.status_code = 220
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CGT2_PENDING"
status_type.status_message = "Application is CGT2 Pending"
status_type.status_code = 230
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CGT2_FAILED"
status_type.status_message = "Application has failed CGT2"
status_type.status_code = 240
status_type.save()


status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_GRT_READY"
status_type.status_message = "Application is GRT Ready"
status_type.status_code = 250
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_GRT_PENDING"
status_type.status_message = "Application is GRT Pending"
status_type.status_code = 260
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_GRT_FAILED"
status_type.status_message = "Application has failed GRT"
status_type.status_code = 270
status_type.save()


status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_GRT_DONE"
status_type.status_message = "Application GRT Done"
status_type.status_code = 272
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_TELECALLING_PASSED"
status_type.status_message = "Application tele calling has passed."
status_type.status_code = 276
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_TELECALLING_FAILED"
status_type.status_message = "Application tele calling has failed."
status_type.status_code = 278
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_UNDERWRITING_READY"
status_type.status_message = "Application is under-writing ready."
status_type.status_code = 280
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_UNDERWRITING_DONE"
status_type.status_message = "Application Under-writing done."
status_type.status_code = 290
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_DISBURSEMENT_READY"
status_type.status_message = "Application Disbursement ready"
status_type.status_code = 300
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_DISBURSEMENT_CANCELLED"
status_type.status_message = "Application Disbursement has been cancelled,possibly due to CGT-GRT failure"
status_type.status_code = 310
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_DISBURSEMENT_PENDING"
status_type.status_message = "Application Disbursement ready, waiting for disbursement over a week"
status_type.status_code = 320
status_type.save()




#Added By Deepak


#added by prathvi
