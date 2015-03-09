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


class OrgDistrict(db.Document):
    district = db.ReferenceField('OrgState')
    name = db.StringField(max_length=60,required=True)

class OrgDistrictResource(Resource):
    document= OrgDistrict


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


class EsthenosUser(BaseUser):
    first_name = db.StringField(max_length=255, required=False,default="")
    last_name = db.StringField(max_length=255, required=False,default="")
    profile_pic = db.StringField(max_length=255, required=False)
    unique_id = db.IntField(default=0)
    status = db.IntField(default=0)
    activation_code = db.StringField(max_length=50, required=False)
    active = db.BooleanField(default=False)
    staff = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)
    about = db.StringField(max_length=255, required=False)


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


class EsthenosUserResource(Resource):
    document = EsthenosUser



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
    pan_card = db.EmbeddedDocumentField(EsthenosOrgApplicationPanCard)
    vid_card = db.EmbeddedDocumentField(EsthenosOrgApplicationVID)
    aadhaar_card = db.EmbeddedDocumentField(EsthenosOrgApplicationAadhaar)


    def __unicode__(self):
        return self.application_id + "<" + self.application_name + ">"



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

class EsthenosOrgAgentUser(BaseUser):
    first_name = db.StringField(max_length=255, required=False,default="")
    last_name = db.StringField(max_length=255, required=False,default="")
    profile_pic = db.StringField(max_length=255, required=False)
    type = db.ReferenceField('EsthenosUserType', required=True)
    unique_id = db.IntField(default=0)
    status = db.IntField(default=0)
    activation_code = db.StringField(max_length=50, required=False)
    active = db.BooleanField(default=False)
    staff = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)
    about = db.StringField(max_length=255, required=False)
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


class Session(db.Document):
    sid = db.StringField(primary_key=True)
    data = db.DictField()
    expiration = db.DateTimeField()
    is_processed = db.BooleanField(default=False)


class EsthenosUserType(db.Document):
    type = db.StringField(max_length=20,required=True)



class EsthenosUserBiliing(db.Document):
    user = db.ReferenceField(EsthenosUser)
    total_applications = db.IntField(default=0)
    total_applications_manual = db.IntField(default=0)
    total_kyc = db.IntField(default=0)
    total_kyc_manual = db.IntField(default=0)
    billing_month = db.StringField(max_length=255, required=False,default="")
    billing_days = db.StringField(max_length=255, required=False,default="")

    def __unicode__(self):
        return self.user.name +" ---Requests"




sauth_user_registered = signal('user-registered')

@sauth_user_registered.connect
def user_registered(action,user,plan_name):
    if action == "flask-satuh":
        print "User registered"

sauth_user_registered.connect(user_registered)