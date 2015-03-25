#!/usr/bin/python

from p_admin.models import  EsthenosSettings,EsthenosUser
from p_organisation.models import EsthenosOrgApplicationHighMark,EsthenosOrgApplicationHighMarkRequest,EsthenosOrgApplication,EsthenosOrgApplicationStatusTypes

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
EsthenosSettings=EsthenosSettings()
EsthenosSettings=EsthenosSettings()

print settings
settings.save()

if EsthenosOrgApplicationStatusTypes.objects.all() == 0:
    status_type = EsthenosOrgApplicationStatusTypes()


#Added by Deepak
def make_sample_highmark_request_for_application_id(app_id):
    hmrequest = EsthenosOrgApplicationHighMarkRequest()
    hmrequest.applicant_id1(app_id)
    hmrequest.acct_open_date("")
    hmrequest.applicant_address1("44 MACHHLEL TA MATAR DIST KHEDA")
    hmrequest.applicant_address1_city("MACHEL")
    hmrequest.applicant_address1_pincode("387530")
    hmrequest.applicant_address1_state("GJ")
    hmrequest.applicant_address2("")
    hmrequest.applicant_address2_city("")
    hmrequest.applicant_address2_pincode("")
    hmrequest.applicant_address2_state("")
    hmrequest.applicant_address_type1("D12")
    hmrequest.applicant_address_type2("")
    hmrequest.applicant_age("40")
    hmrequest.applicant_age_as_on_date("05/03/2015 16:32:00")
    hmrequest.applicant_birth_date("05/03/2015 16:32:00")
    hmrequest.applicant_id__account_no("")
    hmrequest.applicant_id_type1("ID02")
    hmrequest.applicant_id_type2("ID05")
    hmrequest.applicant_name1("PARMAR BHEEKHEEBEN")
    hmrequest.applicant_name2("")
    hmrequest.applicant_name3("")
    hmrequest.applicant_name4("")
    hmrequest.applicant_name5("")
    hmrequest.applicant_telephone_number1("9574040983")
    hmrequest.applicant_telephone_number2("")
    hmrequest.applied_for_amount__current_balance("20000")
    hmrequest.branch_id("KHEDA")
    hmrequest.credit_inquiry_purpose_type("ACCT-ORIG")
    hmrequest.credit_inquiry_purpose_type_description("")
    hmrequest.credit_inquiry_stage("PRE-SCREEN")
    hmrequest.credit_report_transaction_date_time("0000-00-00 00:00:00")
    hmrequest.credit_report_transaction_id("")
    hmrequest.credit_request_type("JOIN")
    hmrequest.kendra_id("MACHHIYEL TALAVFALIYU")
    hmrequest.key_person_name("")
    hmrequest.key_person_relation("")
    hmrequest.member_father_name("UPGSINH")
    hmrequest.member_id("GJ8509005")
    hmrequest.member_mother_name("")
    hmrequest.member_relationship_name1("PARMAR DINESHBHAI")
    hmrequest.member_relationship_name2("PARMAR DINESHBHAI")
    hmrequest.member_relationship_name3("")
    hmrequest.member_relationship_name4("")
    hmrequest.member_relationship_type1("K02")
    hmrequest.member_relationship_type2("K01")
    hmrequest.member_relationship_type3("")
    hmrequest.member_relationship_type4("")
    hmrequest.member_mother_name("")
    hmrequest.member_spouse_name("DINESHBHAI")
    hmrequest.nominee_name("")
    hmrequest.segment_identifier("CRDRQINQR")
    hmrequest.sent_status("")
    print hmrequest
    hmrequest.save()
    add_sample_highmark_response(app_id)

def add_sample_highmark_response(app_id):
    hmresponse = EsthenosOrgApplicationHighMark()
    hmresponse.active_account("0")
    hmresponse.address("#81 MARIMUDDANAHALLI HUNSURE TO MYSOURE KARIMUDDANAHALLI 571189 KA")
    hmresponse.age_as_on_dt("")
    hmresponse.application_id(app_id)
    hmresponse.branch("MYSORE3")
    hmresponse.closed_account("0")
    hmresponse.default_account("0")
    hmresponse.dob_age("1-1-1959")
    hmresponse.driving_lic("")
    hmresponse.error_descripton("")
    hmresponse.father_name("")
    hmresponse.kendra("KARIMUDDANAHALLI")
    hmresponse.mbr_rel_name1("GOVINDEGOWDA")
    hmresponse.mbr_rel_name2("GARIGOWDA")
    hmresponse.member_id("KA1031411")
    hmresponse.member_name("LAXMAMMA")
    hmresponse.oth_active("0")
    hmresponse.oth_all("0")
    hmresponse.other_disb_atm("201442")
    hmresponse.other_id_type1("")
    hmresponse.other_id_val1("")
    hmresponse.own("false")
    hmresponse.own_disb_atm("0")
    hmresponse.phone("'8693947846")
    hmresponse.pri("5")
    hmresponse.ration_card("")
    hmresponse.rel_type1("(Father)")
    hmresponse.rel_type2("(Husband)")
    hmresponse.remark("Borrower has more than 2 Active loans")
    hmresponse.report_id("FFSL140909CR72163129")
    hmresponse.sec("1")
    hmresponse.spouse_name("SRINIVAS")
    hmresponse.status("SUCCESS")
    hmresponse.value("Over Exposure")
    hmresponse.voter_id("ACS35085")
    print hmresponse
    hmresponse.save()

#Added By Deepak


#added by prathvi
