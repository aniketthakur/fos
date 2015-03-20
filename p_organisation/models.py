from wtforms.validators import required

__author__ = 'prathvi'
import datetime
from esthenos  import db
from flask.ext.mongorest.resources import Resource
from blinker import signal
from flask_sauth.models import BaseUser
from p_admin.models import EsthenosUser
# Create your models here.

class EsthenosOrgNotification(db.Document):
    to_user = db.ReferenceField('EsthenosOrg')
    from_user = db.ReferenceField('EsthenosOrg', required=False)
    sender_name = db.StringField(max_length=255, required=True)
    sender_extra_data = db.StringField(max_length=255, required=False)
    notification_type = db.StringField(max_length=255, required=True) #BILLING ,COLLABORATION
    message = db.StringField(max_length=255, required=True)
    read_state = db.BooleanField(default=False)
    notification_date = db.DateTimeField(default=datetime.datetime.now)

class EsthenosOrgNotificationResource(Resource):
    document= EsthenosOrgNotification


class EsthenosOrgState(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    state_name = db.StringField(max_length=60,required=True)

class EsthenosOrgStateResource(Resource):
    document= EsthenosOrgState


class EsthenosOrgArea(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    area_name = db.StringField(max_length=60,required=True)

class EsthenosOrgAreaResource(Resource):
    document= EsthenosOrgArea

class EsthenosOrgRegion(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    region_name = db.StringField(max_length=60,required=True)

class EsthenosOrgRegionResource(Resource):
    document= EsthenosOrgRegion


class EsthenosOrgBranch(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    branch_name = db.StringField(max_length=60,required=True)

class EsthenosOrgBranchResource(Resource):
    document= EsthenosOrgBranch



class EsthenosOrgToken(db.EmbeddedDocument):
    auth_token = db.StringField(max_length=255, required=True)
    client_id = db.StringField(max_length=255, required=True)
    expires_in = db.IntField(default=0)
    token_state = db.StringField(max_length=255, required=True)
    unique_user_id = db.StringField(max_length=255, required=True)
    client_name = db.StringField(max_length=255, required=True)
    api_version = db.StringField(max_length=255, required=True)

class EsthenosOrgTokenResource(Resource):
    document= EsthenosOrgToken

class PixuateObjectUrlMap(db.Document):
    pixuate_id = db.StringField(max_length=255)
    pixuate_url = db.StringField(max_length=512)
    pixuate_original_url = db.StringField(max_length=512)


class EsthenosOrgApplicationMap(db.EmbeddedDocument):
    file_id = db.IntField(required=True)
    app_file_pixuate_id = db.ListField(db.StringField(max_length=255))
    kyc_file_pixuate_id = db.ListField(db.StringField())
    gkyc_file_pixuate_id = db.ListField(db.StringField())

class EsthenosOrgUserUploadSession(db.Document):
    unique_session_key = db.StringField(max_length=255, required=True)
    owner = db.ReferenceField('EsthenosUser')
    session_group = db.ReferenceField('EsthenosOrgGroup', required=False)
    session_center = db.ReferenceField('EsthenosOrgCenter', required=False)
    number_of_applications = db.IntField(default=0, required=False)
    number_of_kycs = db.IntField(default=0, required=False)
    date_created = db.DateTimeField(default=datetime.datetime.now)
    date_updated = db.DateTimeField(default=datetime.datetime.now)
    applications = db.ListField(db.EmbeddedDocumentField(EsthenosOrgApplicationMap), required=False)
    tagged = db.BooleanField(default=False)

class EsthenosOrg(db.Document):
    code = db.StringField(max_length=5, required=False)
    logo_url = db.StringField(max_length=255, required=False)
    domain = db.StringField(max_length=128, required=False)
    states = db.ListField(db.ReferenceField('EsthenosOrgState'), required=False)
    areas = db.ListField(db.ReferenceField('EsthenosOrgArea'), required=False)
    regions = db.ListField(db.ReferenceField('EsthenosOrgRegion'), required=False)
    branches = db.ListField(db.ReferenceField('EsthenosOrgBranch'), required=False)
    name = db.StringField(max_length=512, required=True)
    profile_pic = db.StringField(max_length=255, required=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)
    about = db.StringField(max_length=255, required=False)
    owner = db.ReferenceField('EsthenosUser')
    postal_address = db.StringField(max_length=255, required=False)
    postal_country = db.StringField(max_length=100, required=False)
    postal_state = db.StringField(max_length=100, required=False)
    postal_telephone = db.StringField(max_length=20, required=False)
    postal_tele_code = db.StringField(max_length=20, required=False)
    postal_city = db.StringField(max_length=100, required=False)
    postal_code = db.StringField(max_length=10, required=False)
    email = db.StringField( unique=True)
    application_count = db.IntField(default=1)


class EsthenosOrgCenter(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    center_name = db.StringField(max_length=60,required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

class EsthenosOrgCenterResource(Resource):
    document= EsthenosOrgRegion


class EsthenosOrgGroup(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    center = db.ReferenceField('EsthenosOrgCenter',required=False)
    group_name = db.StringField(max_length=60,required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

class EsthenosOrgBranchResource(Resource):
    document= EsthenosOrgGroup


class EsthenosOrgApplicationPanCard(db.EmbeddedDocument):
    name_or_org_name = db.StringField(max_length=255, required=False,default="")
    father_or_org_name = db.StringField(max_length=255, required=False,default="")
    dob = db.StringField(max_length=20, required=False,default="")
    pan_number = db.StringField(max_length=20, required=False,default="")

    def __unicode__(self):
        return self.name_or_org_name + "<" + self.father_or_org_name + ">"


class EsthenosOrgApplicationVID(db.EmbeddedDocument):
    vid_number = db.StringField(max_length=20, required=False,default="")
    dob = db.StringField(max_length=20, required=False,default="")
    elector_name = db.StringField(max_length=255, required=False,default="")
    father_or_husband_name = db.StringField(max_length=255, required=False,default="")
    gender = db.StringField(max_length=20, required=False,default="")
    address1 = db.StringField(max_length=512, required=False,default="")
    address2 = db.StringField(max_length=512, required=False,default="")
    state = db.StringField(max_length=128, required=False,default="")
    dist = db.StringField(max_length=128, required=False,default="")
    taluk = db.StringField(max_length=128, required=False,default="")
    pincode = db.StringField(max_length=20, required=False,default="")
    date_created = db.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.elector_name + "<" + self.father_or_husband_name + ">"

class EsthenosOrgApplicationAadhaar(db.EmbeddedDocument):
    aadhaar_number = db.StringField(max_length=20, required=False,default="")
    dob = db.StringField(max_length=20, required=False,default="")
    name = db.StringField(max_length=255, required=False,default="")
    care_of_name = db.StringField(max_length=255, required=False,default="")
    gender = db.StringField(max_length=20, required=False,default="")
    address1 = db.StringField(max_length=512, required=False,default="")
    address2 = db.StringField(max_length=512, required=False,default="")
    state = db.StringField(max_length=128, required=False,default="")
    dist = db.StringField(max_length=128, required=False,default="")
    taluk = db.StringField(max_length=128, required=False,default="")
    pincode = db.StringField(max_length=20, required=False,default="")
    date_created = db.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.elector_name + "<" + self.father_or_husband_name + ">"


class EsthenosOrgProduct(db.Document):
    product_name=db.StringField(max_length=128,required=True)
    organisation = db.ReferenceField('EsthenosOrg')
    loan_amount = db.FloatField(default=0.0)
    life_insurance = db.FloatField(default=0.0)
    eligible_cycle = db.IntField(default=0)
    number_installments = db.IntField(default=0)
    emi = db.FloatField(default=0)
    last_emi = db.FloatField(default=0)
    processing_fee = db.FloatField(default=0)
    total_processing_fees = db.FloatField(default=0)
    interest_rate = db.FloatField(default=0)
    insurance_period = db.FloatField(default=0)
    insurance_free_borrowers_only = db.FloatField(default=0.0)
    total_processing_fees_borrowers_only = db.FloatField(default=0)
    insurance_free_borrowers_n_guarnteer = db.FloatField(default=0.0)
    total_processing_fees_borrowers_n_guarnteer = db.FloatField(default=0)
    emi_repayment=db.StringField(max_length=128,required=False)

    def __unicode__(self):
        return "EsthenosOrgProduct"


class EsthenosOrgSettings(db.Document):
    loan_cycle_1_org = db.FloatField(default=35000)
    loan_cycle_1_plus_org = db.FloatField(default=50000)
    one_year_tenure_limit_org = db.FloatField(default=15000)
    hh_annual_income_limit_rural_org = db.FloatField(default=60000)
    hh_annual_income_limit_annual_org = db.FloatField(default=120000)
    total_indebtness_org = db.FloatField(default=50000)
    max_existing_loan_count_org = db.IntField(default=2)
    applicatant_min_attendence_percentage = db.FloatField(default=0.0)

    def __unicode__(self):
        return "EsthenosOrgSetings"

class EsthenosOrgApplicationStatusTypes(db.Document):
    staus =  db.StringField(max_length=20, required=True,default="")
    staus_message =  db.StringField(max_length=512, required=True,default="")
    status_code = db.IntField(default=0)
    def __unicode__(self):
        return "EsthenosOrgApplicationStatusTypes"

class EsthenosOrgApplicationStatus(db.EmbeddedDocument):
    status = db.ReferenceField('EsthenosOrgApplicationStatusTypes')
    message = db.StringField(max_length=512, required=False,default="")

    def __unicode__(self):
        return "EsthenosOrgApplicationStatus"

class EsthenosOrgApplication(db.Document):
    center = db.ReferenceField('EsthenosOrgCenter')
    group = db.ReferenceField('EsthenosOrgGroup')
    organisation = db.ReferenceField('EsthenosOrg')
    tag = db.EmbeddedDocumentField(EsthenosOrgApplicationMap)
    application_id = db.StringField(max_length=255, required=False,default="")
    upload_type = db.StringField(max_length=20, required=False,default="")
    status = db.StringField(max_length=45, required=False,default="")
    applicant_name = db.StringField(max_length=45, required=False,default="")
    gender = db.StringField(max_length=20, required=False,default="")
    age = db.IntField(default=0)
    dob = db.StringField(max_length=20, required=False,default="")
    address = db.StringField(max_length=512, required=False,default="")
    primary_income = db.FloatField(default=0.0)
    secondary_income = db.FloatField(default=0.0)
    tertiary_income = db.FloatField(default=0.0)
    other_income = db.FloatField(default=0.0)
    total_income = db.FloatField(default=0.0)
    business_expense = db.FloatField(default=0.0)
    food_expense = db.FloatField(default=0.0)
    travel_expense = db.FloatField(default=0.0)
    entertainment_expense = db.FloatField(default=0.0)
    educational_expense = db.FloatField(default=0.0)
    medical_expense = db.FloatField(default=0.0)
    other_expense = db.FloatField(default=0.0)
    total_expenditure = db.FloatField(default=0.0)
    total_liability = db.FloatField(default=0.0)
    outstanding_1 = db.FloatField(default=0.0)
    outstanding_2 = db.FloatField(default=0.0)
    outstanding_3 = db.FloatField(default=0.0)
    outstanding_4 = db.FloatField(default=0.0)

    total_outstanding = db.FloatField(default=0.0)
    other_outstanding_chit = db.FloatField(default=0.0)
    other_outstanding_insurance = db.FloatField(default=0.0)
    other_outstanding_emi = db.FloatField(default=0.0)
    total_other_outstanding = db.FloatField(default=0.0)
    net_income = db.FloatField(default=0.0)
    total_running_loans = db.IntField(default=0.0)
    total_existing_outstanding_from = db.FloatField(default=0.0)
    total_running_loans_from_mfi = db.IntField(default=0)
    total_existing_outstanding_from_mfi = db.FloatField(default=0.0)
    existing_loan_cycle = db.IntField(default=0)
    eligible_loan_cycle = db.IntField(default=0)
    defaults_with_no_mfis = db.IntField(default=0)
    attendence_percentage = db.FloatField(default=0.0)
    loan_eligibility_based_on_net_income = db.FloatField(default=0.0)
    loan_eligibility_based_on_company_policy = db.FloatField(default=0.0)
    pan_card = db.EmbeddedDocumentField(EsthenosOrgApplicationPanCard)
    vid_card = db.EmbeddedDocumentField(EsthenosOrgApplicationVID)
    aadhaar_card = db.EmbeddedDocumentField(EsthenosOrgApplicationAadhaar)
    current_status = db.ReferenceField('EsthenosOrgApplicationStatusTypes')
    timeline =  db.ListField(db.EmbeddedDocumentField(EsthenosOrgApplicationStatus))
    date_created = db.DateTimeField(default=datetime.datetime.now)
    date_updated = db.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.application_id + "<" + self.applicant_name + ">"



class EsthenosOrgApplicationHighMark(db.Document):
    application_id = db.StringField(max_length=255, required=True,default="")
    member_id=db.StringField(max_length=128, required=True,default="")
    member_name=db.StringField(max_length=128, required=True,default="")
    spouse_name=db.StringField(max_length=128, required=True,default="")
    status=db.StringField(max_length=128, required=True,default="")
    own=db.StringField(max_length=128, required=True,default="")
    oth_all=db.IntField( required=True,default="")
    oth_active=db.IntField( required=True,default="")
    pri=db.IntField( required=True,default="")
    sec=db.IntField( required=True,default="")
    closed_account=db.IntField( required=True,default="")
    active_account=db.IntField( required=True,default="")
    default_account=db.IntField( required=True,default="")
    own_disb_atm=db.IntField( required=True,default="")
    other_disb_atm=db.IntField( required=True,default="")
    value=db.StringField(max_length=128, required=True,default="")
    remark=db.StringField(max_length=128, required=True,default="")
    error_descripton=db.StringField(max_length=128, required=True,default="")
    address=db.StringField(max_length=512, required=True,default="")
    dob_age=db.StringField(max_length=128, required=True,default="")
    age_as_on_dt=db.IntField( required=True,default="")
    father_name=db.StringField(max_length=128, required=True,default="")
    ration_card=db.StringField(max_length=128, required=True,default="")
    voter_id=db.StringField(max_length=128, required=True,default="")
    phone=db.IntField( required=True,default="")
    rel_type1=db.StringField(max_length=128, required=True,default="")
    mbr_rel_name1=db.StringField(max_length=128, required=True,default="")
    rel_type2=db.StringField(max_length=128, required=True,default="")
    mbr_rel_name2=db.StringField(max_length=128, required=True,default="")
    driving_lic=db.StringField(max_length=128, required=False,default="")
    other_id_type1=db.StringField(max_length=128, required=False,default="")
    other_id_val1=db.StringField(max_length=128, required=False,default="")
    branch=db.StringField(max_length=128, required=True,default="")
    kendra=db.StringField(max_length=128, required=True,default="")
    report_id=db.StringField(max_length=128, required=True,default="")

    raw = db.StringField(max_length=4096, required=True,default="")
    def __unicode__(self):
        return "EsthenosOrgApplicationStatus"

class EsthenosOrgApplicationHighMarkRequest(db.Document):
    application_id = db.StringField(max_length=255, required=True,default="")
    sent_status = db.BooleanField(default=False)
    segment_identifier = db.StringField(max_length=255, required=False,default="")
    credit_request_type=db.StringField(max_length=255,required=False,default="")
    credit_report_transaction_id=db.StringField(max_length=255,required=False,default="")
    credit_inquiry_purpose_type=db.StringField(max_length=255,required=False,default="")
    credit_inquiry_purpose_type_description=db.StringField(max_length=255,required=False,default="")
    credit_inquiry_stage=db.StringField(max_length=255,required=False,default="")
    credit_report_transaction_date_time=db.StringField(max_length=255,required=False,default="")
    applicant_name1=db.StringField(max_length=255,required=True,default="")
    applicant_name2=db.StringField(max_length=255,required=False,default="")
    applicant_name3=db.StringField(max_length=255,required=False,default="")
    applicant_name4=db.StringField(max_length=255,required=False,default="")
    applicant_name5=db.StringField(max_length=255,required=False,default="")
    member_father_name=db.StringField(max_length=255,required=True,default="")
    member_mother_name=db.StringField(max_length=255,required=False,default="")
    member_spouse_name=db.StringField(max_length=255,required=True,default="")
    member_relationship_type1=db.StringField(max_length=255,required=False,default="")
    member_relationship_name1=db.StringField(max_length=255,required=True,default="")
    member_relationship_type2=db.StringField(max_length=255,required=False,default="")
    member_relationship_name2=db.StringField(max_length=255,required=False,default="")
    member_relationship_type3=db.StringField(max_length=255,required=False,default="")
    member_relationship_name3=db.StringField(max_length=255,required=False,default="")
    member_relationship_type4=db.StringField(max_length=255,required=False,default="")
    member_relationship_name4=db.StringField(max_length=255,required=False,default="")
    applicant_birth_date=db.StringField(max_length=255,required=False,default="")
    applicant_age=db.IntField(required=True,default="")
    applicant_age_as_on_date=db.StringField(max_length=255,required=False,default="")
    applicant_id_type1=db.StringField(max_length=255,required=False,default="")
    applicant_id1=db.StringField(max_length=255,required=True,default="")
    applicant_id_type2=db.StringField(max_length=255,required=False,default="")
    applicant_id1=db.StringField(max_length=255,required=True,default="")
    acct_open_date=db.StringField(max_length=255,required=False,default="")
    applicant_id__account_no=db.StringField(max_length=255,required=False,default="")
    branch_id=db.StringField(max_length=255,required=False,default="")
    member_id=db.StringField(max_length=255,required=True,default="")
    kendra_id=db.StringField(max_length=255,required=True,default="")
    applied_for_amount__current_balance=db.IntField(required=True,default="")
    key_person_name=db.StringField(max_length=255,required=False,default="")
    key_person_relation=db.StringField(max_length=255,required=False,default="")
    nominee_name=db.StringField(max_length=255,required=False,default="")
    applicant_telephone_number_type1=db.IntField(required=False,default="")
    applicant_telephone_number1=db.IntField(required=True,default="")
    applicant_telephone_number_type2=db.IntField(required=False,default="")
    applicant_telephone_number2=db.IntField(required=False,default="")
    applicant_address_type1=db.StringField(max_length=255,required=False,default="")
    applicant_address1=db.StringField(max_length=255,required=True,default="")
    applicant_address1_city=db.StringField(max_length=255,required=True,default="")
    applicant_address1_state=db.StringField(max_length=255,required=True,default="")
    applicant_address1_pincode=db.StringField(max_length=255,required=True,default="")
    applicant_address_type2=db.StringField(max_length=255,required=False,default="")
    applicant_address2=db.StringField(max_length=255,required=False,default="")
    applicant_address2_city=db.StringField(max_length=255,required=False,default="")
    applicant_address2_state=db.StringField(max_length=255,required=False,default="")
    applicant_address2_pincode=db.StringField(max_length=255,required=False,default="")

    def __unicode__(self):
        return "EsthenosOrgApplicationStatus"

sauth_user_registered = signal('user-registered')

@sauth_user_registered.connect
def user_registered(action,user,plan_name):
    if action == "flask-satuh":
        print "User registered"

sauth_user_registered.connect(user_registered)