import datetime
from esthenos import db
from blinker import signal
from flask_sauth.models import BaseUser
from flask.ext.mongorest.resources import Resource


class EsthenosUser(BaseUser):
    first_name = db.StringField(max_length=255, required=False,default="")
    last_name = db.StringField(max_length=255, required=False,default="")
    user_name = db.StringField(max_length=100,required=False)
    email = db.StringField(max_length=255, required=False)
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
    designation = db.StringField(max_length=255,required=False)
    date_of_birth = db.StringField(max_length=20, required=False)

    postal_address = db.StringField(max_length=255, required=False)
    postal_city = db.StringField(max_length=100, required=False)
    postal_state = db.StringField(max_length=100, required=False)
    postal_country = db.StringField(max_length=100, required=False)
    postal_telephone = db.StringField(max_length=20, required=False)
    postal_tele_code = db.StringField(max_length=20, required=False)

    owner = db.ReferenceField('EsthenosUser',required=False)
    org_area = db.ReferenceField('EsthenosOrgArea',required=False)
    org_state = db.ReferenceField('EsthenosOrgState',required=False)
    org_region = db.ReferenceField('EsthenosOrgRegion',required=False)
    org_branch = db.ReferenceField('EsthenosOrgBranch',required=False)
    organisation = db.ReferenceField('EsthenosOrg',required=False)

    def __unicode__(self):
        return "%s, %s, %s" % (self.name, self.email, self.organisation)

    def is_active(self):
        return self.active

    def is_staff(self):
        return self.staff

    def get_fullname(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_shortname(self):
        return self.first_name

    def get_organization(self):
        return self.organisation

    def get_phone_number(self):
        return "%s %s" % (self.postal_tele_code, self.postal_telephone)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class EsthenosOrg(db.Document):
    code = db.StringField(max_length=5, required=False)
    logo_url = db.StringField(max_length=255, required=False)
    domain = db.StringField(max_length=128, required=False)
    states = db.ListField(db.ReferenceField('EsthenosOrgState'), required=False)
    monthly_target = db.IntField(default=0)
    monthly_disbursed = db.IntField(default=0)
    monthly_amount_disbursed = db.IntField(default=0)
    name = db.StringField(max_length=512, required=True)
    profile_pic = db.StringField(max_length=255, required=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)
    about = db.StringField(max_length=255, required=False)
    owner = db.ReferenceField('EsthenosUser')
    postal_address = db.StringField(max_length=255, required=False)
    postal_country = db.StringField(max_length=100, required=False)
    postal_state = db.StringField(max_length=100, required=False)
    postal_telephone = db.StringField(max_length=512, required=False)
    postal_tele_code = db.StringField(max_length=512, required=False)
    postal_city = db.StringField(max_length=100, required=False)
    postal_code = db.StringField(max_length=10, required=False)
    email = db.StringField( unique=True)
    application_count = db.IntField(default=0)
    group_count = db.IntField(default=1)
    center_count = db.IntField(default=1)
    employee_count = db.IntField(default=1)
    user_count = db.IntField(default=1)

    def __unicode__(self):
      return "%s, %s, %s, %s" % (self.name, self.email, self.group_count, self.center_count)


class EsthenosSettings(db.Document):
    loan_cycle_1_rbi = db.FloatField(default=35000)
    loan_cycle_1_plus_rbi = db.FloatField(default=100000)
    one_year_tenure_limit_rbi = db.FloatField(default=15000)
    hh_annual_income_limit_rural_rbi = db.FloatField(default=60000)
    hh_annual_income_limit_urban_rbi = db.FloatField(default=120000)
    total_indebtness_rbi = db.FloatField(default=100000)
    max_existing_loan_count_rbi = db.IntField(default=2)
    sales_tax = db.FloatField(default=12.36)
    organisations_count = db.IntField(default=0)


class EsthenosOrgNotification(db.Document):
    to_user = db.ReferenceField('EsthenosOrg')
    from_user = db.ReferenceField('EsthenosOrg', required=False)
    sender_name = db.StringField(max_length=255, required=True)
    sender_extra_data = db.StringField(max_length=255, required=False)
    notification_type = db.StringField(max_length=255, required=True) #BILLING ,COLLABORATION
    message = db.StringField(max_length=255, required=True)
    read_state = db.BooleanField(default=False)
    notification_date = db.DateTimeField(default=datetime.datetime.now)


class EsthenosOrgApplicationStatusType(db.Document):
    status = db.StringField(max_length=100, required=True,default="")
    status_message = db.StringField(max_length=512, required=True,default="")
    group_status = db.StringField(max_length=512, required=True,default="")
    status_code = db.IntField(default=0)
    sub_status_code = db.IntField(default=0)
    sub_status_message = db.StringField(max_length=512, required=True,default="")

    def __unicode__(self):
        return self.status


class EsthenosOrgApplicationStatus(db.Document):
    status = db.ReferenceField(EsthenosOrgApplicationStatusType)
    status_message = db.StringField(max_length=512, required=True, default="")
    updated_on = db.DateTimeField(default=datetime.datetime.now)


class EsthenosOrgState(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    name = db.StringField(max_length=60, required=True)


class EsthenosOrgRegion(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgState)
    name = db.StringField(max_length=60, required=True)


class EsthenosOrgArea(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgRegion)
    name = db.StringField(max_length=60, required=True)


class EsthenosOrgBranch(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgArea)
    name = db.StringField(max_length=60, required=True)


class EsthenosOrgCenter(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgBranch)
    name = db.StringField(max_length=60, required=True)

    center_id = db.StringField(max_length=10, required=False)
    center_timeslot = db.DateTimeField(required = False)

    @staticmethod
    def unique_id(org):
        return org.name.upper()[0:2]+"C"+"{0:06d}".format(org.center_count)


class EsthenosOrgGroup(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgCenter, required=False)
    name = db.StringField(max_length=120, required=True)

    group_id = db.StringField(max_length=20,required=False)
    leader_name = db.StringField(max_length=120,required=False)
    leader_number = db.StringField(max_length=120,required=False)

    size = db.IntField(default=0)
    size_override = db.BooleanField(default=False)
    members = db.IntField(default=0)

    status = db.IntField(default=0)
    current_status = db.ReferenceField(EsthenosOrgApplicationStatusType)
    current_status_updated = db.DateTimeField(default=datetime.datetime.now)

    timeline = db.ListField(db.ReferenceField(EsthenosOrgApplicationStatus))

    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    cgt_grt_pdf_link = db.StringField(max_length=512,required=False)
    disbursement_pdf_link = db.StringField(max_length=512,required=False,default="#")

    def applications(self):
        return EsthenosOrgApplication.objects.filter(group=self)

    def full(self):
        return (self.size != 0 and self.members >= self.size) or self.size_override

    def verified(self):
        return EsthenosOrgApplication.objects.filter(group=self, status=170).count() == self.members

    def update_status(self, status_code):
        self.status = status_code
        self.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=status_code)
        self.current_status_updated = datetime.datetime.now()

        status = EsthenosOrgApplicationStatus(
          status=self.current_status,
          updated_on=self.current_status_updated
        )
        status.save()
        self.timeline.append(status)

        for app in self.applications():
            app.update_status(status_code)
            app.save()

        self.save()

    def tojson(self):
        return {
          'group_id': str(self.group_id),
          'group_size': str(self.size),
          'group_name': str(self.name),
          'group_members': str(self.members),
          'current_status' : str(self.current_status.group_status),
          'current_status_updated' : str(self.current_status_updated)
        }

    @staticmethod
    def unique_id(org):
        return org.name.upper()[0:2]+"G"+"{0:06d}".format(org.group_count)


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
    kyc_file_pixuate_id = db.DictField()
    gkyc_file_pixuate_id = db.DictField()


class EsthenosOrgApplicationDocs(db.EmbeddedDocument):
    pan_docs = db.ListField(db.StringField(max_length=255))
    aadhar_docs = db.ListField(db.StringField(max_length=255))
    voterid_docs = db.ListField(db.StringField(max_length=255))
    personal_docs = db.ListField(db.StringField(max_length=255))
    business_docs = db.ListField(db.StringField(max_length=255))
    other_docs = db.ListField(db.StringField(max_length=255))

    def has_kyc(self):
        return self.pan_docs + self.aadhar_docs + self.voterid_docs

    def kyc_docs(self):
        return self.pan_docs + self.aadhar_docs + self.voterid_docs

    def all_docs(self):
        return self.pan_docs + self.aadhar_docs + self.voterid_docs + self.personal_docs + self.business_docs + self.other_docs


class EsthenosOrgUserUploadSession(db.DynamicDocument):
    unique_session_key = db.StringField(max_length=255, required=True)
    owner = db.ReferenceField('EsthenosUser')
    session_group = db.ReferenceField('EsthenosOrgGroup', required=False)
    session_center = db.ReferenceField('EsthenosOrgCenter', required=False)
    number_of_applications = db.IntField(default=0, required=False)
    number_of_kycs = db.IntField(default=0, required=False)
    number_of_gkycs = db.IntField(default=0, required=False)
    date_created = db.DateTimeField(default=datetime.datetime.now)
    date_updated = db.DateTimeField(default=datetime.datetime.now)
    applications = db.DictField()
    tagged = db.BooleanField(default=False)


class EsthenosOrgHierarchy(db.Document):
    level = db.IntField(required=True)
    role = db.StringField(max_length=10, required=True)
    title = db.StringField(max_length=10, required=True)
    title_full = db.StringField(max_length=50, required=True)


class EsthenosOrgRole(db.Document):
    role = db.StringField(max_length=25, required=True)
    features = db.ListField(db.StringField(max_length=255))


class EsthenosOrgRoleSettings(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    role = db.StringField(max_length=25, required=True)
    access_dash = db.StringField(max_length=10, required=True,default="no")
    access_enroll_customer = db.StringField(max_length=10, required=True,default="no")
    access_cgt = db.StringField(max_length=10, required=True,default="no")
    access_grt = db.StringField(max_length=10, required=True,default="no")
    access_disburse = db.StringField(max_length=10, required=True,default="no")
    access_reports = db.StringField(max_length=10, required=True,default="no")
    access_maker = db.StringField(max_length=10, required=True,default="no")
    access_checker = db.StringField(max_length=10, required=True,default="no")
    noti_de_done = db.StringField(max_length=10, required=True,default="no")
    noti_cbc_done = db.StringField(max_length=10, required=True,default="no")
    noti_cfa_done = db.StringField(max_length=10, required=True,default="no")
    noti_dd_done = db.StringField(max_length=10, required=True,default="no")
    noti_db_done = db.StringField(max_length=10, required=True,default="no")
    reports_all_data = db.StringField(max_length=10, required=True,default="no")
    reports_de_done = db.StringField(max_length=10, required=True,default="no")
    reports_cbc_done = db.StringField(max_length=10, required=True,default="no")
    reports_cfa_done = db.StringField(max_length=10, required=True,default="no")
    reports_dd_done = db.StringField(max_length=10, required=True,default="no")
    reports_db_done = db.StringField(max_length=10, required=True,default="no")


class EsthenosOrgStats(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    stat_type = db.StringField(max_length=20, required=False)
    datetime = db.DateTimeField(default=datetime.datetime.now)

    application_submitted = db.IntField(default=0)
    application_kyc_ready = db.IntField(default=0)
    application_kyc_done = db.IntField(default=0)
    application_kyc_passed = db.IntField(default=0)
    application_kyc_failed = db.IntField(default=0)
    application_cbcheck_ready = db.IntField(default=0)
    application_cbcheck_done = db.IntField(default=0)
    application_cbcheck_passed = db.IntField(default=0)
    application_cbcheck_failed = db.IntField(default=0)
    application_cf_ready = db.IntField(default=0)
    application_cf_done = db.IntField(default=0)
    application_cf_passed = db.IntField(default=0)
    application_cf_failed = db.IntField(default=0)
    application_cgt1_ready = db.IntField(default=0)
    application_cgt1_done = db.IntField(default=0)
    application_cgt1_passed = db.IntField(default=0)
    application_cgt1_failed = db.IntField(default=0)
    application_cgt2_ready = db.IntField(default=0)
    application_cgt2_done = db.IntField(default=0)
    application_cgt2_passed = db.IntField(default=0)
    application_cgt2_failed = db.IntField(default=0)
    application_grt_ready = db.IntField(default=0)
    application_grt_done = db.IntField(default=0)
    application_grt_passed = db.IntField(default=0)
    application_grt_failed = db.IntField(default=0)
    application_underwriting_ready = db.IntField(default=0)
    application_underwriting_done = db.IntField(default=0)
    application_disbursement_ready = db.IntField(default=0)
    application_disbursement_pending = db.IntField(default=0)
    application_disbursement_done = db.IntField(default=0)


class EsthenosOrgApplicationKYC(db.EmbeddedDocument):
    kyc_type = db.StringField(max_length=512, required=False,default="")
    kyc_number = db.StringField(max_length=512, required=False,default="")
    age = db.StringField(max_length=512, required=False,default="")
    dob = db.StringField(max_length=512, required=False,default="")
    name = db.StringField(max_length=255, required=False,default="")
    taluk = db.StringField(max_length=128, required=False,default="")
    state = db.StringField(max_length=128, required=False,default="")
    gender = db.StringField(max_length=512, required=False,default="")
    pincode = db.StringField(max_length=512, required=False,default="")
    address = db.StringField(max_length=512, required=False,default="")
    country = db.StringField(max_length=512, required=False,default="")
    district = db.StringField(max_length=512, required=False,default="")
    phone_number = db.StringField(max_length=512, required=False,default="")
    mobile_number = db.StringField(max_length=512, required=False,default="")
    father_or_husband_name = db.StringField(max_length=255, required=False,default="")
    date_created = db.DateTimeField(default=datetime.datetime.now)
    validation = db.StringField(max_length=512, required=True,default="PENDING")

    def __unicode__(self):
        return self.kyc_number + "<" + self.name + ">"


class EsthenosOrgApplicationScrutiny(db.EmbeddedDocument):
    total_income = db.FloatField(required=False, default=0)
    total_expense = db.FloatField(required=False, default=0)

    foir_ratio = db.FloatField(required=False, default=0)
    total_ltv = db.FloatField(required=False, default=0)
    total_amount = db.FloatField(required=False, default=0)

    memo_business_type = db.StringField(max_length=512, required=True, default="")
    memo_business_name = db.StringField(max_length=512, required=True, default="")
    memo_applicant_address = db.StringField(max_length=512, required=True, default="")

    memo_loan_emi = db.FloatField(required=False, default=0)
    memo_loan_amount = db.FloatField(required=False, default=0)
    memo_loan_period = db.FloatField(required=False, default=0)
    memo_loan_interest = db.FloatField(required=False, default=0)
    memo_loan_processing_fee = db.FloatField(required=False, default=0)

    date = db.DateTimeField(default=datetime.datetime.now)
    owner = db.ReferenceField(EsthenosUser)
    status = db.StringField(max_length=512, required=True, default="")


class EsthenosOrgApplicationSanction(db.EmbeddedDocument):
    total_income = db.FloatField(required=False, default=0)
    total_expense = db.FloatField(required=False, default=0)

    foir_ratio = db.FloatField(required=False, default=0)
    total_ltv = db.FloatField(required=False, default=0)
    total_amount = db.FloatField(required=False, default=0)

    memo_business_type = db.StringField(max_length=512, required=True, default="")
    memo_business_name = db.StringField(max_length=512, required=True, default="")
    memo_applicant_address = db.StringField(max_length=512, required=True, default="")

    memo_loan_emi = db.FloatField(required=False, default=0)
    memo_loan_amount = db.FloatField(required=False, default=0)
    memo_loan_period = db.FloatField(required=False, default=0)
    memo_loan_interest = db.FloatField(required=False, default=0)
    memo_loan_processing_fee = db.FloatField(required=False, default=0)

    date = db.DateTimeField(default=datetime.datetime.now)
    owner = db.ReferenceField(EsthenosUser)
    status = db.StringField(max_length=512, required=True, default="")


class EsthenosOrgPsychometricTemplateQuestionSession(db.Document):
      organisation = db.ReferenceField('EsthenosOrg',required=True)
      group = db.ReferenceField('EsthenosOrgGroup',required=True)
      questions=db.DictField(required=False)
      score=db.FloatField(default=0,required=False)


class EsthenosOrgPsychometricTemplateQuestion(db.Document):
    question = db.StringField(max_length=1024,required=True)
    question_regional = db.StringField(max_length=1024,required=True)

    answer1 = db.StringField(max_length=1024,required=True)
    answer_regional1 = db.StringField(max_length=1024,required=True)

    answer2 = db.StringField(max_length=1024,required=True)
    answer_regional2 = db.StringField(max_length=1024,required=True)

    answer3 = db.StringField(max_length=1024,required=True)
    answer_regional3 = db.StringField(max_length=1024,required=True)

    answer4 = db.StringField(max_length=1024,required=True)
    answer_regional4 = db.StringField(max_length=1024,required=True)

    language_type = db.StringField(max_length=128,required=True,default="Hindi")
    organisation = db.ReferenceField('EsthenosOrg')


class EsthenosOrgProduct(db.Document):
    product_name=db.StringField(max_length=128,required=True)
    loan_type=db.StringField(max_length=128,required=False)
    organisation = db.ReferenceField('EsthenosOrg')
    loan_amount = db.FloatField(default=25000)
    life_insurance = db.FloatField(default=0.0)
    eligible_cycle = db.IntField(default=0)
    number_installments = db.IntField(default=0)
    emi = db.FloatField(default=0)
    service_tax = db.FloatField(default=0)
    insurance_service_tax = db.FloatField(default=0)
    last_emi = db.FloatField(default=0)
    processing_fee = db.FloatField(default=0)
    total_processing_fees = db.FloatField(default=0)
    interest_rate = db.FloatField(default=0)
    insurance_period = db.FloatField(default=0)
    insurance_free = db.FloatField(default=0.0)
    total_insurance_fees = db.FloatField(default=0)
    rd_free = db.FloatField(default=0)
    emi_repayment=db.StringField(max_length=128,required=False)


class EsthenosOrgSettings(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    loan_cycle_1_org = db.FloatField(default=35000)
    loan_cycle_1_plus_org = db.FloatField(default=100000)
    one_year_tenure_limit_org = db.FloatField(default=15000)
    hh_annual_income_limit_rural_org = db.FloatField(default=60000)
    hh_annual_income_limit_urban_org = db.FloatField(default=120000)
    total_indebtness_org = db.FloatField(default=100000)
    max_existing_loan_count_org = db.IntField(default=2)
    applicatant_min_attendence_percentage = db.FloatField(default=0.0)
    product_cycle_1_group_min = db.IntField(default=5)
    product_cycle_1_group_max = db.IntField(default=20)
    product_cycle_2_group_min = db.IntField(default=5)
    product_cycle_2_group_max = db.IntField(default=20)
    product_cycle_3_group_min = db.IntField(default=5)
    product_cycle_3_group_max = db.IntField(default=20)
    product_cycle_4_group_min = db.IntField(default=5)
    product_cycle_4_group_max = db.IntField(default=20)
    highmark_username = db.StringField(max_length=100, required=True,default="")
    highmark_password = db.StringField(max_length=100, required=True,default="")


class EsthenosOrgLocation(db.EmbeddedDocument):
    lat = db.FloatField(default=0.0)
    lng = db.FloatField(default=0.0)

    def __unicode__(self):
      return {"lat": self.lat, "lng": self.lng}


class EsthenosOrgApplication(db.Document):
    owner = db.ReferenceField(EsthenosUser)
    group = db.ReferenceField(EsthenosOrgGroup)
    center = db.ReferenceField(EsthenosOrgCenter)
    branch = db.ReferenceField(EsthenosOrgBranch)
    product = db.ReferenceField(EsthenosOrgProduct)
    organisation = db.ReferenceField(EsthenosOrg)

    applicant_kyc = db.EmbeddedDocumentField(EsthenosOrgApplicationKYC, default=EsthenosOrgApplicationKYC)
    applicant_docs = db.EmbeddedDocumentField(EsthenosOrgApplicationDocs, default=EsthenosOrgApplicationDocs)

    guarantor1_kyc = db.EmbeddedDocumentField(EsthenosOrgApplicationKYC, default=EsthenosOrgApplicationKYC)
    guarantor1_docs = db.EmbeddedDocumentField(EsthenosOrgApplicationDocs, default=EsthenosOrgApplicationDocs)

    guarantor2_kyc = db.EmbeddedDocumentField(EsthenosOrgApplicationKYC, default=EsthenosOrgApplicationKYC)
    guarantor2_docs = db.EmbeddedDocumentField(EsthenosOrgApplicationDocs, default=EsthenosOrgApplicationDocs)

    other_documents = db.ListField(db.EmbeddedDocumentField(EsthenosOrgApplicationKYC))

    home_loc = db.EmbeddedDocumentField(EsthenosOrgLocation, default=EsthenosOrgLocation)
    business_loc = db.EmbeddedDocumentField(EsthenosOrgLocation, default=EsthenosOrgLocation)

    tag = db.EmbeddedDocumentField(EsthenosOrgApplicationMap,required=False)
    timeline = db.ListField(db.ReferenceField(EsthenosOrgApplicationStatus))

    updated_on = db.DateTimeField(default=datetime.datetime.now)
    date_created = db.DateTimeField(default=datetime.datetime.now)

    status = db.IntField(default=0)
    current_status = db.ReferenceField(EsthenosOrgApplicationStatusType)
    current_status_updated = db.DateTimeField(default=datetime.datetime.now)

    scrutiny = db.EmbeddedDocumentField(EsthenosOrgApplicationScrutiny, default=EsthenosOrgApplicationScrutiny)
    sanction = db.EmbeddedDocumentField(EsthenosOrgApplicationSanction, default=EsthenosOrgApplicationSanction)

    assets_id = db.StringField(max_length=255, required=False,default="")
    application_id = db.StringField(max_length=255, required=False,default="")

    age = db.IntField(default=0)
    dob = db.StringField(max_length=512, required=False,default="")
    yob = db.StringField(max_length=512, required=False,default="")
    applicant_name = db.StringField(max_length=45, required=False,default="")
    city = db.StringField(max_length=128, required=False,default="")
    taluk = db.StringField(max_length=128, required=False,default="")
    state = db.StringField(max_length=128, required=False,default="")
    district = db.StringField(max_length=128, required=False,default="")
    address = db.StringField(max_length=512, required=False,default="")
    country = db.StringField(max_length=128, required=False,default="")
    pincode = db.StringField(max_length=10, required=False,default="")
    mobile = db.StringField(max_length=10, required=False,default="")
    tele_code = db.StringField(max_length=128, required=False,default="")
    tele_phone = db.StringField(max_length=128, required=False,default="")
    father_or_husband_name = db.StringField(max_length=512, required=False,default="")

    caste = db.StringField(max_length=512, required=False,default="")
    gender = db.StringField(max_length=512, required=False,default="")
    religion = db.StringField(max_length=512, required=False,default="")
    category = db.StringField(max_length=512, required=False,default="")
    education = db.StringField(max_length=512, required=False,default="")
    disability = db.StringField(max_length=512, required=False,default="")
    marital_status = db.StringField(max_length=512, required=False,default="")

    male_count = db.IntField(default=0.0)
    female_count = db.IntField(default=0.0)
    members_above18 =  db.IntField(default=0)
    members_less_than_18 = db.IntField(default=0)
    total_earning_members = db.IntField(default=0)
    total_number_of_family_members = db.IntField(default=0)

    nominee_age = db.StringField(max_length=512, required=False,default="")
    nominee_name = db.StringField(max_length=512, required=False,default="")
    nominee_phone = db.StringField(max_length=512, required=False,default="")
    nominee_gender = db.StringField(max_length=512, required=False,default="")
    nominee_relationship_with_borrower = db.StringField(max_length=512, required=False,default="")

    type_of_house = db.StringField(max_length=512, required=False,default="")
    quality_of_house = db.StringField(max_length=512, required=False,default="")
    house_stay_duration = db.FloatField(default=0.0)

    applied_loan = db.FloatField(default=0.0)
    purpose_of_loan = db.StringField(max_length=512, required=False,default="")

    family_assets_other = db.StringField(max_length=512, required=False,default="")
    family_assets_land_acres = db.FloatField(default=0)
    family_assets_orchard_acres = db.FloatField(default=0)
    family_assets_number_of_rented_houses_or_flats = db.FloatField(default=0)
    family_assets_number_of_rented_shops_or_godowns = db.FloatField(default=0)

    bank_name = db.StringField(max_length=200, required=False,default="")
    bank_ifsc_code = db.StringField(max_length=20, required=False,default="")
    bank_account_number = db.StringField(max_length=200, required=False,default="")
    bank_account_holder_name = db.StringField(max_length=200, required=False,default="")
    bank_bank_branch = db.StringField(max_length=200, required=False,default="")
    bank_bank_account_type = db.StringField(max_length=200, required=False,default="")
    bank_account_operational_since = db.StringField(max_length=200, required=False,default="")

    bank2_name = db.StringField(max_length=200, required=False,default="")
    bank2_ifsc_code = db.StringField(max_length=20, required=False,default="")
    bank2_account_number = db.StringField(max_length=200, required=False,default="")
    bank2_account_holder_name = db.StringField(max_length=200, required=False,default="")
    bank2_bank_branch = db.StringField(max_length=200, required=False,default="")
    bank2_bank_account_type = db.StringField(max_length=200, required=False,default="")
    bank2_account_operational_since = db.StringField(max_length=200, required=False,default="")

    cheque_no = db.StringField(max_length=512, required=False,default="")
    cheque_bank_name = db.StringField(max_length=512, required=False,default="")
    repayment_mode = db.StringField(max_length=512, required=False,default="")
    repayment_method = db.StringField(max_length=512, required=False,default="")

    primary_business_premise = db.StringField(max_length=512, required=False,default="")
    primary_business_category = db.StringField(max_length=512, required=False,default="")
    primary_business_activities = db.StringField(max_length=512, required=False,default="")
    primary_business_seasonality = db.StringField(max_length=512, required=False,default="")
    primary_business_income_monthly = db.FloatField(default=0.0)
    primary_business_number_of_employees = db.FloatField(default=0.0)
    primary_business_expense_rent = db.FloatField(default=0.0)
    primary_business_expense_admin = db.FloatField(default=0.0)
    primary_business_expense_other = db.FloatField(default=0.0)
    primary_business_expense_working_capital = db.FloatField(default=0.0)
    primary_business_expense_employee_salary = db.FloatField(default=0.0)
    primary_business_number_of_years_in_business = db.FloatField(default=0.0)

    secondary_business = db.StringField(max_length=512, required=False,default="")
    secondary_business_category = db.StringField(max_length=512, required=False,default="")
    secondary_business_income_monthly = db.FloatField(default=0.0)
    secondary_business_expenses_monthly = db.FloatField(default=0.0)

    tertiary_business = db.StringField(max_length=512, required=False,default="")
    tertiary_business_category = db.StringField(max_length=512, required=False,default="")
    tertiary_business_income_monthly = db.FloatField(default=0.0)
    tertiary_business_expenses_monthly = db.FloatField(default=0.0)

    other_income = db.FloatField(default=0.0)

    food_expense = db.FloatField(default=0.0)
    other_expense = db.FloatField(default=0.0)
    travel_expense = db.FloatField(default=0.0)
    medical_expense = db.FloatField(default=0.0)
    festival_expense = db.FloatField(default=0)
    educational_expense = db.FloatField(default=0.0)
    entertainment_expense = db.FloatField(default=0.0)

    primary_asset_for_hypothecation_purchase_year = db.StringField(max_length=512, required=False, default="")
    primary_asset_for_hypothecation_purchase_price = db.FloatField(default=0.0)
    primary_asset_for_hypothecation_purchase_purpose = db.StringField(max_length=512, required=False, default="")
    primary_asset_for_hypothecation_current_market_value = db.FloatField(default = 0.0)
    primary_asset_for_hypothecation_details_of_hypothecated_goods = db.StringField(max_length=512, required=False, default="")

    secondary_asset_for_hypothecation_purchase_year = db.StringField(max_length=512, required=False, default="")
    secondary_asset_for_hypothecation_purchase_price = db.FloatField(default=0.0)
    secondary_asset_for_hypothecation_purchase_purpose = db.StringField(max_length=512, required=False, default="")
    secondary_asset_for_hypothecation_current_market_value = db.FloatField(default=0.0)
    secondary_asset_for_hypothecation_details_of_hypothecated_goods = db.StringField(max_length=512, required=False, default="")

    tertiary_asset_for_hypothecation_purchase_year = db.StringField(max_length=512, required=False, default="")
    tertiary_asset_for_hypothecation_purchase_price = db.FloatField(default=0.0)
    tertiary_asset_for_hypothecation_purchase_purpose = db.StringField(max_length=512, required=False, default="")
    tertiary_asset_for_hypothecation_current_market_value = db.FloatField(default = 0.0)
    tertiary_asset_for_hypothecation_details_of_hypothecated_goods = db.StringField(max_length=512, required=False, default="")

    total_liability = db.FloatField(default=0.0)
    outstanding_1 = db.FloatField(default=0.0)
    outstanding_2 = db.FloatField(default=0.0)
    outstanding_3 = db.FloatField(default=0.0)
    outstanding_4 = db.FloatField(default=0.0)
    total_outstanding = db.FloatField(default=0.0)

    other_outstanding_emi = db.FloatField(default=0.0)
    other_outstanding_chit = db.FloatField(default=0.0)
    other_outstanding_insurance = db.FloatField(default=0.0)
    other_outstanding_familynfriends = db.FloatField(default=0.0)

    total_running_loans = db.IntField(default=0.0)
    total_running_loans_from_mfi = db.IntField(default=0)
    total_existing_outstanding_from = db.FloatField(default=0.0)
    total_existing_outstanding_from_mfi = db.FloatField(default=0.0)

    loan_eligibility_based_on_company_policy = db.FloatField(default=0.0)

    existing_loan_cycle = db.IntField(default=0)
    eligible_loan_cycle = db.IntField(default=0)
    defaults_with_no_mfis = db.IntField(default=0)
    attendence_percentage = db.FloatField(default=0.0)

    equifax_submitted = db.BooleanField(default=False)
    highmark_submitted = db.BooleanField(default=False)
    generate_disbursement = db.BooleanField(default=False)
    generate_disbursement_done = db.BooleanField(default=False)

    expected_tenure_in_months = db.IntField(default=0)
    expected_emi_amount_served = db.FloatField(default=0.0)

    def total_income(self):
        return self.primary_business_income_monthly \
              + self.secondary_business_income_monthly \
              + self.tertiary_business_income_monthly \
              + self.other_income

    def total_expenditure(self):
        return self.food_expense\
              + self.travel_expense\
              + self.entertainment_expense \
              + self.educational_expense \
              + self.medical_expense \
              + self.business_expense() \
              + self.other_expense

    def total_other_outstanding(self):
        return self.other_outstanding_emi \
              + self.other_outstanding_chit \
              + self.other_outstanding_insurance \
              + self.other_outstanding_familynfriends

    def net_income(self):
        return self.total_income() \
              - self.total_expenditure() \
              - self.total_other_outstanding()

    def business_expense(self):
        return self.secondary_business_expenses_monthly \
              + self.tertiary_business_expenses_monthly \
              + self.primary_business_expense_rent \
              + self.primary_business_expense_admin \
              + self.primary_business_expense_other \
              + self.primary_business_expense_working_capital \
              + self.primary_business_expense_employee_salary

    def loan_eligibility_based_on_net_income(self):
        return self.net_income() / 2 * self.product.number_installments

    def update_status(self, status_code):
        self.status = status_code
        self.current_status = EsthenosOrgApplicationStatusType.objects.get(status_code=status_code)
        self.current_status_updated = datetime.datetime.now()

        status = EsthenosOrgApplicationStatus(
          status=self.current_status,
          updated_on=self.current_status_updated
        )
        status.save()
        self.timeline.append(status)

    def __unicode__(self):
        return self.application_id + "<" + self.applicant_name + ">"


class EsthenosOrgApplicationHighMarkRequest(db.Document):
    application_id = db.StringField(max_length=255, required=True,default="")
    member_id=db.StringField(max_length=128, required=True,default="")
    member_name=db.StringField(max_length=128, required=True,default="")
    spouse_name=db.StringField(max_length=128, required=True,default="")
    status=db.StringField(max_length=128, required=True,default="")
    own=db.StringField(max_length=128, required=True,default="")
    oth_all=db.IntField( required=True,default=0)
    oth_active=db.IntField( required=True,default=0)
    pri=db.IntField( required=True,default=0)
    sec=db.IntField( required=True,default=0)
    closed_account=db.IntField( required=True,default=0)
    active_account=db.IntField( required=True,default=0)
    default_account=db.IntField( required=True,default=0)
    own_disb_amt=db.IntField( required=True,default=0)
    other_disb_amt=db.IntField( default=0)
    own_curr_amt=db.IntField(default=0)
    other_curr_amt=db.IntField(default=0)
    own_inst_amt=db.IntField(default=0)
    other_inst_amt=db.IntField(default=0)
    value=db.StringField(max_length=128, required=True,default="")
    remark=db.StringField(max_length=128, required=True,default="")
    error_descripton=db.StringField(max_length=128, required=True,default="")
    address=db.StringField(max_length=512, required=True,default="")
    dob_age=db.StringField(max_length=128, required=True,default="")
    age_as_on_dt=db.IntField( required=True,default=0)
    father_name=db.StringField(max_length=128, required=True,default="")
    ration_card=db.StringField(max_length=128, required=True,default="")
    voter_id=db.StringField(max_length=128, required=True,default="")
    phone=db.StringField(max_length=512, required=True,default="")
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
    raw = db.StringField(max_length=8096, required=True,default="")


class EsthenosOrgApplicationHighMarkResponse(db.Document):
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
    applicant_age=db.IntField(default=0)
    applicant_age_as_on_date=db.StringField(max_length=255,required=False,default="")
    applicant_id_type1=db.StringField(max_length=255,required=False,default="")
    applicant_id1=db.StringField(max_length=255,required=True,default="")
    applicant_id_type2=db.StringField(max_length=255,required=False,default="")
    applicant_id2=db.StringField(max_length=255,required=True,default="")
    acct_open_date=db.StringField(max_length=255,required=False,default="")
    applicant_id__account_no=db.StringField(max_length=255,required=False,default="")
    branch_id=db.StringField(max_length=255,required=False,default="")
    member_id=db.StringField(max_length=255,required=True,default="")
    kendra_id=db.StringField(max_length=255,required=True,default="")
    applied_for_amount__current_balance=db.IntField(required=True,default="")
    key_person_name=db.StringField(max_length=255,required=False,default="")
    key_person_relation=db.StringField(max_length=255,required=False,default="")
    nominee_name=db.StringField(max_length=255,required=False,default="")
    applicant_telephone_number_type1=db.StringField(required=False,default="")
    applicant_telephone_number1=db.StringField(required=False,default="")
    applicant_telephone_number_type2=db.StringField(required=False,default="")
    applicant_telephone_number2=db.StringField(required=False,default="")
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
    nominee_relationship_type=db.StringField(max_length=255,required=False,default="")


class EsthenosOrgApplicationEqifaxResponse(db.Document):
    report_id=db.IntField(default=0)
    reference_number=db.StringField(max_length=255,required=False,default="")
    unique_account_number=db.StringField(max_length=255,required=False,default="")
    date_of_issue=db.StringField(max_length=255,required=False,default="")
    member_name=db.StringField(max_length=255,required=False,default="")
    date_of_birth=db.StringField(max_length=255,required=False,default="")
    addl_name_type1=db.StringField(max_length=255,required=False,default="")
    addl_name1=db.StringField(max_length=255,required=False,default="")
    addl_name_type2=db.StringField(max_length=255,required=False,default="")
    addl_name2=db.StringField(max_length=255,required=False,default="")
    national_id_card=db.StringField(max_length=255,required=False,default="")
    passport=db.StringField(max_length=255,required=False,default="")
    ration_card=db.StringField(max_length=255,required=False,default="")
    voter_id=db.StringField(max_length=255,required=False,default="")
    pan_card=db.StringField(max_length=255,required=False,default="")
    additional_id1=db.StringField(max_length=255,required=False,default="")
    additional_id2=db.StringField(max_length=255,required=False,default="")
    address=db.StringField(max_length=255,required=False,default="")
    state=db.StringField(max_length=255,required=False,default="")
    postal=db.StringField(max_length=255,required=False,default="")
    branch_id=db.StringField(max_length=255,required=False,default="")
    kendra_or_centre_id=db.StringField(max_length=255,required=False,default="")
    own_mfi_indicator=db.IntField(default=0)
    total_responses=db.IntField(default=0)
    total_responses_own=db.IntField(default=0)
    total_responses_others=db.IntField(default=0)
    num_of_other_mfis=db.IntField(default=0)
    num_active_account=db.IntField(default=0)
    num_active_account_own=db.IntField(default=0)
    num_active_account_other=db.IntField(default=0)
    num_closed_account=db.IntField(default=0)
    num_closed_account_own=db.IntField(default=0)
    num_closed_account_other=db.IntField(default=0)
    num_past_due_account=db.IntField(default=0)
    num_past_due_account_own=db.IntField(default=0)
    num_past_due_account_other=db.IntField(default=0)
    sum_current_balance=db.FloatField(default=0)
    sum_current_balance_own=db.FloatField(default=0)
    sum_current_balance_other=db.FloatField(default=0)
    sum_disbursed=db.FloatField(default=0)
    sum_disbursed_own=db.FloatField(default=0)
    sum_disbursed_other=db.FloatField(default=0)
    sum_installment_amount=db.FloatField(default=0)
    sum_installment_amount_own=db.FloatField(default=0)
    sum_installment_amount_other=db.FloatField(default=0)
    sum_overdue_amount=db.FloatField(default=0)
    sum_overdue_amount_own=db.FloatField(default=0)
    sum_overdue_amount_other=db.FloatField(default=0)
    sum_writtenoff_amount=db.FloatField(default=0)
    sum_writtenoff_amount_own=db.FloatField(default=0)
    sum_writtenoff_amount_other=db.FloatField(default=0)
    num_writtenoff_account=db.IntField(default=0)
    num_writtenoff_account_own=db.IntField(default=0)
    num_writtenoff_accountnon_own=db.IntField(default=0)


class EsthenosOrgApplicationEqifax(db.Document):
    reference_number=db.StringField(required=True)
    member_id_unique_accountnumber=db.StringField(default="", required=False)
    inquiry_purpose=db.StringField(max_length=255, required=False,default="")
    transaction_amount=db.FloatField(default=0, required=False)
    consumer_name=db.StringField(max_length=255, required=False,default="")
    additional_type1=db.StringField(max_length=255, required=False,default="")
    additional_name1=db.StringField(max_length=255, required=False,default="")
    additional_type2=db.StringField(max_length=255, required=False,default="")
    additional_name2=db.StringField(max_length=255, required=False,default="")
    address_city=db.StringField(max_length=255, required=False,default="")
    state_union_territory=db.StringField(max_length=255, required=False,default="")
    postal_pin=db.StringField(default=0)
    ration_card=db.StringField(max_length=255, required=False,default="")
    voter_id=db.StringField(max_length=255, required=False,default="")
    additional_id1=db.StringField(max_length=255, required=False,default="")
    additional_id2=db.StringField(max_length=255, required=False,default="")
    national_id_card=db.StringField(max_length=255, required=False,default="")
    tax_id_pan=db.StringField(max_length=255, required=False,default="")
    phone_home=db.StringField(max_length=20, required=False,default="")
    phone_mobile=db.StringField(max_length=20, required=False,default="")
    dob=db.StringField(max_length=255, required=False,default="")
    gender=db.StringField(max_length=255, required=False,default="")
    branch_id=db.StringField(max_length=255, required=False,default="")
    kendra_id=db.StringField(max_length=255, required=False,default="")


sauth_user_registered = signal('user-registered')

@sauth_user_registered.connect
def user_registered(action,user,plan_name):
    if action == "flask-satuh":
        print "User registered"

sauth_user_registered.connect(user_registered)
