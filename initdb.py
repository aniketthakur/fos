#!/usr/bin/python

from p_admin.models import  EsthenosSettings,EsthenosUser
from p_organisation.models import EsthenosOrgApplicationHighMark,EsthenosOrgApplicationHighMarkRequest

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
Highmarkrequest=EsthenosOrgApplicationHighMarkRequest()
Highmarkresponse=EsthenosOrgApplicationHighMark()

print settings
settings.save()
#Added by Deepak
if len(EsthenosOrgApplicationHighMarkRequest.objects.all()) ==1:
    EsthenosOrgApplicationHighMarkRequest.objects.all()[0].delete()

Highmarkrequest = EsthenosOrgApplicationHighMarkRequest()
Highmarkrequest.applicant_id1("GJ/19/137/370571")
Highmarkrequest.acct_open_date("")
Highmarkrequest.applicant_address1("44 MACHHLEL TA MATAR DIST KHEDA")
Highmarkrequest.applicant_address1_city("MACHEL")
Highmarkrequest.applicant_address1_pincode("387530")
Highmarkrequest.applicant_address1_state("GJ")
Highmarkrequest.applicant_address2("")
Highmarkrequest.applicant_address2_city("")
Highmarkrequest.applicant_address2_pincode("")
Highmarkrequest.applicant_address2_state("")
Highmarkrequest.applicant_address_type1("D12")
Highmarkrequest.applicant_address_type2("")
Highmarkrequest.applicant_age("40")
Highmarkrequest.applicant_age_as_on_date("05/03/2015 16:32:00")
Highmarkrequest.applicant_birth_date("05/03/2015 16:32:00")
Highmarkrequest.applicant_id__account_no("")
Highmarkrequest.applicant_id_type1("ID02")
Highmarkrequest.applicant_id_type2("ID05")
Highmarkrequest.applicant_name1("PARMAR BHEEKHEEBEN")
Highmarkrequest.applicant_name2("")
Highmarkrequest.applicant_name3("")
Highmarkrequest.applicant_name4("")
Highmarkrequest.applicant_name5("")
Highmarkrequest.applicant_telephone_number1("9574040983")
Highmarkrequest.applicant_telephone_number2("")
Highmarkrequest.applied_for_amount__current_balance("20000")
Highmarkrequest.branch_id("KHEDA")
Highmarkrequest.credit_inquiry_purpose_type("ACCT-ORIG")
Highmarkrequest.credit_inquiry_purpose_type_description("")
Highmarkrequest.credit_inquiry_stage("PRE-SCREEN")
Highmarkrequest.credit_report_transaction_date_time("0000-00-00 00:00:00")
Highmarkrequest.credit_report_transaction_id("")
Highmarkrequest.credit_request_type("JOIN")
Highmarkrequest.kendra_id("MACHHIYEL TALAVFALIYU")
Highmarkrequest.key_person_name("")
Highmarkrequest.key_person_relation("")
Highmarkrequest.member_father_name("UPGSINH")
Highmarkrequest.member_id("GJ8509005")
Highmarkrequest.member_mother_name("")
Highmarkrequest.member_relationship_name1("PARMAR DINESHBHAI")
Highmarkrequest.member_relationship_name2("PARMAR DINESHBHAI")
Highmarkrequest.member_relationship_name3("")
Highmarkrequest.member_relationship_name4("")
Highmarkrequest.member_relationship_type1("K02")
Highmarkrequest.member_relationship_type2("K01")
Highmarkrequest.member_relationship_type3("")
Highmarkrequest.member_relationship_type4("")
Highmarkrequest.member_mother_name("")
Highmarkrequest.member_spouse_name("DINESHBHAI")
Highmarkrequest.nominee_name("")
Highmarkrequest.segment_identifier("CRDRQINQR")
Highmarkrequest.sent_status("")
print Highmarkrequest
Highmarkrequest.save()
#Added By Deepak
if len(EsthenosOrgApplicationHighMark.objects.all()) ==1:
   EsthenosOrgApplicationHighMark.objects.all()[0].delete()

Highmarkresponse = EsthenosOrgApplicationHighMark()
print Highmarkresponse
Highmarkresponse.save()