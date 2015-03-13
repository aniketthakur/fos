__author__ = 'prathvi'
import datetime
from esthenos  import db
from flask.ext.mongorest.resources import Resource
from blinker import signal
from flask_sauth.models import BaseUser
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


class OrgState(db.Document):
    name = db.StringField(max_length=60,required=True)

class OrgStateResource(Resource):
    document= OrgState


class OrgRegion(db.Document):
    district = db.ReferenceField('OrgState')
    name = db.StringField(max_length=60,required=True)

class OrgRegiontResource(Resource):
    document= OrgRegion

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



class EsthenosOrg(db.Document):
    states = db.ListField(db.StringField())
    regions = db.ListField(db.StringField())
    areas = db.ListField(db.StringField())
    branches = db.ListField(db.StringField())
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

class EsthenosOrgUser(BaseUser):
    state = db.ReferenceField('OrgState')
    district = db.ReferenceField('OrgDistrict')
    name = db.StringField(max_length=512, required=False,default="")
    profile_pic = db.StringField(max_length=255, required=False)
    type = db.ReferenceField('EsthenosOrgUserType', required=True)
    unique_id = db.IntField(default=0)
    status = db.IntField(default=0)
    activation_code = db.StringField(max_length=50, required=False)
    active = db.BooleanField(default=False)
    staff = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)
    about = db.StringField(max_length=255, required=False)
    organisation = db.ReferenceField('EsthenosOrg')
    owner = db.ReferenceField('EsthenosUser')
    #user_tokens = db.ListField(db.EmbeddedDocumentField(PUserToken))
    notifications = db.ListField(db.ReferenceField('EsthenosOrgNotification'))


    def __unicode__(self):
        return self.name + "<" + self.email + ">"

    def is_active(self):
        return self.active

    def is_staff(self):
        return self.staff

    def get_fullname(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_shortname(self):
        return self.first_name

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class EsthenosOrgAgentUser(BaseUser):
    first_name = db.StringField(max_length=255, required=False,default="")
    last_name = db.StringField(max_length=255, required=False,default="")
    profile_pic = db.StringField(max_length=255, required=False)
    type = db.ReferenceField('EsthenosOrgUserType', required=True)
    unique_id = db.IntField(default=0)
    status = db.IntField(default=0)
    activation_code = db.StringField(max_length=50, required=False)
    active = db.BooleanField(default=False)
    staff = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)
    about = db.StringField(max_length=255, required=False)
    owner = db.ReferenceField('EsthenosOrgUser')
    #user_tokens = db.ListField(db.EmbeddedDocumentField(PUserToken))
    notifications = db.ListField(db.ReferenceField('EsthenosOrgNotification'))


    def __unicode__(self):
        return self.name + "<" + self.email + ">"

    def is_active(self):
        return self.active

    def is_staff(self):
        return self.staff

    def get_fullname(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_shortname(self):
        return self.first_name

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class EsthenosOrgCenter(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    center_name = db.StringField(max_length=60,required=True)

class EsthenosOrgCenterResource(Resource):
    document= EsthenosOrgRegion


class EsthenosOrgGroup(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    group_name = db.StringField(max_length=60,required=True)

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

    def __unicode__(self):
        return self.elector_name + "<" + self.father_or_husband_name + ">"


class EsthenosOrgProduct(db.Document):
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
    emi_collection_period_weekly =  db.BooleanField(default=False)
    emi_collection_period_monthly =  db.BooleanField(default=False)
    emi_collection_period_fortnightly =  db.BooleanField(default=False)

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

    def __unicode__(self):
        return "EsthenosOrgSetings"

class EsthenosOrgApplication(db.Document):
    center = db.ReferenceField('EsthenosOrgCenter')
    group = db.ReferenceField('EsthenosOrgGroup')
    application_id = db.StringField(max_length=255, required=False,default="")
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
    pan_card = db.EmbeddedDocumentField(EsthenosOrgApplicationPanCard)
    vid_card = db.EmbeddedDocumentField(EsthenosOrgApplicationVID)
    aadhaar_card = db.EmbeddedDocumentField(EsthenosOrgApplicationAadhaar)


    def __unicode__(self):
        return self.application_id + "<" + self.applicant_name + ">"






sauth_user_registered = signal('user-registered')

@sauth_user_registered.connect
def user_registered(action,user,plan_name):
    if action == "flask-satuh":
        print "User registered"

sauth_user_registered.connect(user_registered)