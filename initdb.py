#!/usr/bin/python

from e_admin.models import  EsthenosSettings,EsthenosUser
from e_organisation.models import *

organisation = EsthenosOrg.objects.all()
for org in organisation:
    org.delete()

apps = EsthenosOrgApplication.objects.all()
for app in apps:
    app.delete()


prods = EsthenosOrgProduct.objects.all()
for prod in prods:
    prod.delete()


apps = EsthenosUser.objects.all()
for app in apps:
    app.delete()

status = EsthenosOrgApplicationStatusType.objects.all()
for sta in status:
    sta.delete()

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



#if len(EsthenosOrgApplicationStatusType.objects.all()) == 0:
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_UPLOADED"
status_type.status_message = "Your application is uploaded to system"
status_type.status_code = 0
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_PREFILLED"
status_type.status_message = "Application is prefilled first round of checking"
status_type.status_code = 1
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "BAD_DOCUMENT"
status_type.status_message = "Cannot process current document"
status_type.status_code = 2
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "DOCUMENT MISSING"
status_type.status_message = "Some documents required for the processing are missing"
status_type.status_code = 3
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_TAGGED"
status_type.status_message = "Application is tagged and ready of data entry"
status_type.status_code = 4
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CRITERIA_FAILED"
status_type.status_message = "Some organisation criteria failed required for the processing are missing"
status_type.status_code = -1
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_KYC_VALIDATION_PASSED"
status_type.status_message = "Application KYC has completed, validation successfulh"
status_type.status_code = 5
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_KYC_VALIDATION_FAILED"
status_type.status_message = "Application KYC has completed, failed in one or multiple criteria match"
status_type.status_code = 6
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CBCHECK_READY"
status_type.status_message = "Application data entry done and ready for CB Check"
status_type.status_code = 7
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CBCHECK_SUBMITED"
status_type.status_message = "Application CB Check has completed, waiting for results"
status_type.status_code = 8
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CBCHECK_SUCCESS"
status_type.status_message = "Application CB Check has completed, validation cashflow analysis"
status_type.status_code = 9
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CBCHECK_FAILED"
status_type.status_message = "Application CB Check has completed, failed in one or multiple criteria match"
status_type.status_code = 10
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CASH_FLOW_READY"
status_type.status_message = "Application is Cash Flow Ready"
status_type.status_code = 11
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CASH_FLOW_PASSED"
status_type.status_message = "Application  Cash Flow has Passed"
status_type.status_code = 12
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CASH_FLOW_FAILED"
status_type.status_message = "Application  Cash Flow has Failed, failed in one or multiple criteria match"
status_type.status_code = 13
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CGT1_READY"
status_type.status_message = "Application is CGT1 Ready"
status_type.status_code = 14
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CGT1_PENDING"
status_type.status_message = "Application is CGT1 Pending"
status_type.status_code = 15
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CGT1_FAILED"
status_type.status_message = "Application has failed CGT1"
status_type.status_code = 16
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CGT2_READY"
status_type.status_message = "Application is CGT2 Ready"
status_type.status_code = 17
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CGT2_PENDING"
status_type.status_message = "Application is CGT2 Pending"
status_type.status_code = 18
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_CGT2_FAILED"
status_type.status_message = "Application has failed CGT2"
status_type.status_code = 19
status_type.save()


status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_GRT_READY"
status_type.status_message = "Application is GRT Ready"
status_type.status_code = 20
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_GRT_PENDING"
status_type.status_message = "Application is GRT Pending"
status_type.status_code = 21
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_GRT_FAILED"
status_type.status_message = "Application has failed GRT"
status_type.status_code = 22
status_type.save()

status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_UNDERWRITING_READY"
status_type.status_message = "Application is under writing ready"
status_type.status_code = 23
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_UNDERWRITING_DONE"
status_type.status_message = "Application Under writing done"
status_type.status_code = 24
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_DISBURSEMENT_READY"
status_type.status_message = "Application Disbursement ready"
status_type.status_code = 25
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_DISBURSEMENT_CANCELLED"
status_type.status_message = "Application Disbursement has been cancelled,possibly due to CGT-GRT failure"
status_type.status_code = 26
status_type.save()
status_type = EsthenosOrgApplicationStatusType()
status_type.status = "APPLICATION_DISBURSEMENT_PENDING"
status_type.status_message = "Application Disbursement ready, waiting for disbursement over a week"
status_type.status_code = 27
status_type.save()




#Added By Deepak


#added by prathvi
