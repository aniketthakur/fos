__author__ = 'prathvi'
import mailchimp
from esthenos  import mainapp
@mainapp.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    native = date.replace(tzinfo=None)
    format='%b %d, %Y'
    return native.strftime(format)

def subscribe(name,email_ad, list_id= "93c1a74cac"):
    try:
        m = get_mailchimp_api()
        m.lists.subscribe(list_id, email = {'email':email_ad},merge_vars={'DNAME':name})
        print  "The email has been successfully subscribed"
    except mailchimp.ListAlreadySubscribedError:
        print  "That email is already subscribed to the list"
    except mailchimp.Error, e:
        print  'An error occurred: %s - %s' % (e.__class__, e)

class ordered_dict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self._order = self.keys()

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        if key in self._order:
            self._order.remove(key)
        self._order.append(key)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._order.remove(key)

    def order(self):
        return self._order[:]

    def ordered_items(self):
        return [(key,self[key]) for key in self._order]


from random import randint
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def get_mailchimp_api():
    return mailchimp.Mailchimp('6e73868dbf17cff787d3b9dab5a4f396-us5') #your api key here


from flask import request

def request_wants_json():
    best = request.accept_mimetypes\
    .best_match(['application/json', 'text/html'])
    return best == 'application/json' and\
           request.accept_mimetypes[best] >\
           request.accept_mimetypes['text/html']


from e_organisation.models import EsthenosOrgApplicationHighMarkRequest,EsthenosOrgApplicationHighMarkResponse,EsthenosOrgApplication,EsthenosOrgApplicationEqifax
#Added by Deepak
def make_highmark_request_for_application_id(app_id):
    app = EsthenosOrgApplication.objects.get(application_id = app_id)
    if app.highmark_submitted == True:
        return
    app.highmark_submitted = True
    hmrequest = EsthenosOrgApplicationHighMarkRequest()
    hmrequest.applicant_id1=app.application_id
    hmrequest.acct_open_date=app.created_on
    hmrequest.applicant_address1=app.address+" "
    hmrequest.applicant_address1_city=app.member_city
    hmrequest.applicant_address1_pincode=app.member_pincode
    hmrequest.applicant_address1_state=app.member_state
    hmrequest.applicant_address2=""
    hmrequest.applicant_address2_city=""
    hmrequest.applicant_address2_pincode=""
    hmrequest.applicant_address2_state=""
    hmrequest.applicant_address_type1="D12"
    hmrequest.applicant_address_type2=""
    hmrequest.applicant_age=app.age
    hmrequest.applicant_age_as_on_date=""
    hmrequest.applicant_birth_date=app.dob
    hmrequest.applicant_id__account_no=""
    hmrequest.applicant_id_type1=app.application_id
    hmrequest.applicant_id_type2=""
    hmrequest.applicant_name1=app.applicant_name
    hmrequest.applicant_name2=""
    hmrequest.applicant_name3=""
    hmrequest.applicant_name4=""
    hmrequest.applicant_name5=""
    hmrequest.applicant_telephone_number1=app.member_telephone
    hmrequest.applicant_telephone_number2=""
    hmrequest.applied_for_amount__current_balance=""
    hmrequest.branch_id=app.branch_id
    hmrequest.credit_inquiry_purpose_type=app.purpose_of_loan
    hmrequest.credit_inquiry_purpose_type_description=""
    hmrequest.credit_inquiry_stage="PRE-SCREEN"
    hmrequest.credit_report_transaction_date_time=app.excepted_disbursment_date
    hmrequest.credit_report_transaction_id=""
    hmrequest.credit_request_type="JOIN"
    hmrequest.kendra_id=app.center
    hmrequest.key_person_name=app.member_f_or_h_name
    hmrequest.key_person_relation=""
    hmrequest.member_father_name=app.member_f_or_h_name
    hmrequest.member_id=app.application_id
    hmrequest.member_mother_name=""
    hmrequest.member_relationship_name1=""
    hmrequest.member_relationship_name2=""
    hmrequest.member_relationship_name3=""
    hmrequest.member_relationship_name4=""
    hmrequest.member_relationship_type1=""
    hmrequest.member_relationship_type2=""
    hmrequest.member_relationship_type3=""
    hmrequest.member_relationship_type4=""
    hmrequest.member_mother_name=""
    hmrequest.member_spouse_name=""
    hmrequest.nominee_name=app.member_f_or_h_name
    hmrequest.segment_identifier=""
    hmrequest.sent_status=True
    hmrequest.save()
    app.save()

from e_organisation.models import EsthenosOrgApplicationEqifax

def make_equifax_request_entry_application_id(app_id):
    app = EsthenosOrgApplication.objects.get(application_id = app_id)
    if app.equifax_submitted == True:
        return
    app.equifax_submitted = True
    eqrequest = EsthenosOrgApplicationEqifax()
    eqrequest.reference_number=app_id
    eqrequest.member_id_unique_accountnumber=app_id
    eqrequest.inquiry_purpose=6
    eqrequest.transaction_amount=app.applied_loan
    eqrequest.consumer_name=app.applicant_name
    eqrequest.additional_type1="K02"
    eqrequest.additional_name1=""
    eqrequest.additional_type2=""
    eqrequest.additional_name2=""
    eqrequest.address_city=app.member_city
    eqrequest.state_union_territory=app.member_state
    eqrequest.postal_pin=app.member_pincode
    eqrequest.ration_card=""
    eqrequest.voter_id=""
    if app.kyc_1 != None:
        eqrequest.additional_id1=app.kyc_1.kyc_number
    
    eqrequest.additional_id2=""
    if app.kyc_1 != None:
        eqrequest.national_id_card=app.kyc_1.kyc_number
    eqrequest.tax_id_pan=""
    eqrequest.phone_home=""
    eqrequest.phone_mobile=app.member_telephone
    eqrequest.dob=app.dob
    eqrequest.gender=app.gender
    eqrequest.branch_id=""
    eqrequest.kendra_id=""
    eqrequest.save()
    app.save()


def add_sample_highmark_response(app_id):

#        app.total_running_loans =
#        app.total_existing_outstanding_from =
#        app.total_running_loans_from_mfi =
#        app.total_existing_outstanding_from_mfi =
#        app.existing_loan_cycle =
#        app.eligible_loan_cycle =self.cycle.data
#        app.defaults_with_no_mfis =
#        app.attendence_percentage =
    hmresponse = EsthenosOrgApplicationHighMarkResponse()
    hmresponse.active_account="0"
    hmresponse.address="#81 MARIMUDDANAHALLI HUNSURE TO MYSOURE KARIMUDDANAHALLI 571189 KA"
    hmresponse.age_as_on_dt=20
    hmresponse.application_id=app_id
    hmresponse.branch="MYSORE3"
    hmresponse.closed_account="0"
    hmresponse.default_account="0"
    hmresponse.dob_age="1-1-1959"
    hmresponse.driving_lic=""
    hmresponse.error_descripton=""
    hmresponse.father_name=""
    hmresponse.kendra="KARIMUDDANAHALLI"
    hmresponse.mbr_rel_name1="GOVINDEGOWDA"
    hmresponse.mbr_rel_name2="GARIGOWDA"
    hmresponse.member_id="KA1031411"
    hmresponse.member_name="LAXMAMMA"
    hmresponse.oth_active="0"
    hmresponse.oth_all="0"
    hmresponse.other_disb_atm="201442"
    hmresponse.other_id_type1=""
    hmresponse.other_id_val1=""
    hmresponse.own="false"
    hmresponse.own_disb_atm="0"
    hmresponse.phone="8693947846"
    hmresponse.pri="5"
    hmresponse.ration_card=""
    hmresponse.rel_type1="(Father)"
    hmresponse.rel_type2="=(Husband)"
    hmresponse.remark="Borrower has more than 2 Active loans"
    hmresponse.report_id="FFSL140909CR72163129"
    hmresponse.sec="1"
    hmresponse.spouse_name="SRINIVAS"
    hmresponse.status="SUCCESS"
    hmresponse.value="Over Exposure"
    hmresponse.voter_id="ACS35085"
    print hmresponse
    hmresponse.save()
