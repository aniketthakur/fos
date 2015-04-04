__author__ = 'prathvi'
import datetime
from esthenos  import db
from flask.ext.mongorest.resources import Resource
from blinker import signal
from flask_sauth.models import BaseUser
# Create your models here.


class EsthenosSettings(db.Document):
    loan_cycle_1_rbi = db.FloatField(default=35000)
    loan_cycle_1_plus_rbi = db.FloatField(default=50000)
    one_year_tenure_limit_rbi = db.FloatField(default=15000)
    hh_annual_income_limit_rural_rbi = db.FloatField(default=60000)
    hh_annual_income_limit_urban_rbi = db.FloatField(default=120000)
    total_indebtness_rbi = db.FloatField(default=50000)
    max_existing_loan_count_rbi = db.IntField(default=2)
    sales_tax = db.FloatField(default=12.36)
    organisations_count = db.IntField(default=0)

    def __unicode__(self):
        return "EsthenosSetings"


class EsthenosUser(BaseUser):
    first_name = db.StringField(max_length=255, required=False,default="")
    last_name = db.StringField(max_length=255, required=False,default="")
    profile_pic = db.StringField(max_length=255, required=False)
    unique_id = db.StringField(max_length=20, required=True,default = "NOTSET")
    status = db.IntField(default=0)
    activation_code = db.StringField(max_length=50, required=False)
    active = db.BooleanField(default=False)
    staff = db.BooleanField(default=False)
    permissions = db.DictField()
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)
    about = db.StringField(max_length=255, required=False)
    email = db.StringField(max_length=255, required=False)
    designation=db.StringField(max_length=255,required=False)
    date_of_birth=db.StringField(max_length=20, required=False)
    postal_address = db.StringField(max_length=255, required=False)
    postal_country = db.StringField(max_length=100, required=False)
    postal_state = db.StringField(max_length=100, required=False)
    postal_telephone = db.StringField(max_length=20, required=False)
    postal_tele_code = db.StringField(max_length=20, required=False)
    postal_city = db.StringField(max_length=100, required=False)
    organisation = db.ReferenceField('EsthenosOrg',required=False)
    org_state = db.ReferenceField('EsthenosOrgState')
    org_area =   db.ReferenceField('EsthenosOrgArea')
    org_region = db.ReferenceField('EsthenosOrgRegion')
    org_branch = db.ReferenceField('EsthenosOrgBranch')
    permissions=db.DictField()
    owner = db.ReferenceField('EsthenosUser',required=False)


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