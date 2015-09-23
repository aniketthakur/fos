import datetime
from esthenos import db
from blinker import signal
from flask.ext.mongorest.resources import Resource


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
    document = EsthenosOrgNotification


class EsthenosOrgState(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    state_name = db.StringField(max_length=60,required=True)


class EsthenosOrgStateResource(Resource):
    document = EsthenosOrgState


class EsthenosOrgRegion(db.Document):
    state = db.ReferenceField('EsthenosOrgState')
    organisation = db.ReferenceField('EsthenosOrg')
    region_name = db.StringField(max_length=60,required=True)


class EsthenosOrgRegionResource(Resource):
    document = EsthenosOrgRegion


class EsthenosOrgArea(db.Document):
    state = db.ReferenceField('EsthenosOrgState')
    region = db.ReferenceField('EsthenosOrgRegion')
    organisation = db.ReferenceField('EsthenosOrg')
    area_name = db.StringField(max_length=60,required=True)


class EsthenosOrgAreaResource(Resource):
    document = EsthenosOrgArea


class EsthenosOrgBranch(db.Document):
    state = db.ReferenceField('EsthenosOrgState')
    region = db.ReferenceField('EsthenosOrgRegion')
    area = db.ReferenceField('EsthenosOrgArea')
    organisation = db.ReferenceField('EsthenosOrg')
    branch_name = db.StringField(max_length=60,required=True)


class EsthenosOrgBranchResource(Resource):
    document = EsthenosOrgBranch


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
    organisation = db.ReferenceField('EsthenosOrg')
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
    stat_type = db.StringField(max_length=20, required=False) #2015JAN10,2015JANW1,2015JAN,2015,


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


class EsthenosOrgCenter(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    center_id = db.StringField(max_length=10,required=False)
    center_name = db.StringField(max_length=60,required=True)
    size = db.IntField(default=0)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)
    cgt_grt_pdf_link = db.StringField(max_length=512,required=False)
    disbursement_pdf_link = db.StringField(max_length=512,required=False)

    def __unicode__(self):
      return "%s, %s, %s" % (self.center_id, self.center_name, self.organisation)


class EsthenosOrgCenterResource(Resource):
    document= EsthenosOrgRegion


class EsthenosOrgGroup(db.Document):
    organisation = db.ReferenceField('EsthenosOrg')
    center = db.ReferenceField('EsthenosOrgCenter',required=False)
    branch = db.ReferenceField('EsthenosOrgBranch',required=False)
    group_id = db.StringField(max_length=20,required=False)
    group_name = db.StringField(max_length=120,required=True)
    leader_name = db.StringField(max_length=120,required=False)
    leader_number = db.StringField(max_length=120,required=False)
    size = db.IntField(default=0)
    location_name = db.StringField(max_length=120,required=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)
    cgt_grt_pdf_link = db.StringField(max_length=512,required=False)
    disbursement_pdf_link = db.StringField(max_length=512,required=False,default="#")

    def __unicode__(self):
        return "%s, %s, %s, %s" % (self.organisation, self.group_name, self.location_name, self.size)


class EsthenosOrgGroupResource(Resource):
    document= EsthenosOrgGroup


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


class EsthenosOrgGroupGRTSession(db.Document):
    organisation = db.ReferenceField('EsthenosOrg',required=True)
    group = db.ReferenceField('EsthenosOrgGroup',required=True)
    questions=db.DictField(required=False)
    score = db.FloatField(default=0,required=False)
    state = db.StringField(max_length=128, required=True, default="none")


class EsthenosOrgGroupCGT1Session(db.Document):
    organisation = db.ReferenceField('EsthenosOrg',required=True)
    group = db.ReferenceField('EsthenosOrgGroup',required=True)
    questions = db.DictField(required=False)
    score = db.FloatField(default=0,required=False)
    state = db.StringField(max_length=128, required=True, default="none")


class EsthenosOrgGroupCGT2Session(db.Document):
    organisation = db.ReferenceField('EsthenosOrg',required=True)
    group = db.ReferenceField('EsthenosOrgGroup',required=True)
    questions=db.DictField(required=False)
    score = db.FloatField(default=0,required=False)
    state = db.StringField(max_length=128, required=True, default="none")


class EsthenosOrgGRTTemplateQuestion(db.Document):
    question=db.StringField(max_length=1024,required=True)
    question_regional = db.StringField(max_length=1024,required=True)
    language_type=db.StringField(max_length=128,required=True,default="Hindi")
    organisation = db.ReferenceField('EsthenosOrg')


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


class EsthenosOrgCGT1TemplateQuestion(db.Document):
    question = db.StringField(max_length=1024,required=True)
    question_regional = db.StringField(max_length=1024,required=True)
    language_type = db.StringField(max_length=128,required=True,default="Hindi")
    organisation = db.ReferenceField('EsthenosOrg')


class EsthenosOrgCGT2TemplateQuestion(db.Document):
    question=db.StringField(max_length=1024,required=True)
    question_regional = db.StringField(max_length=1024,required=True)
    language_type=db.StringField(max_length=128,required=True,default="Hindi")
    organisation = db.ReferenceField('EsthenosOrg')


class EsthenosOrgTeleCallingTemplateQuestion(db.Document):
    question=db.StringField(max_length=1024,required=True)
    question_regional = db.StringField(max_length=1024,required=True)
    language_type=db.StringField(max_length=128,required=True,default="Hindi")
    organisation = db.ReferenceField('EsthenosOrg')


class EsthenosOrgIndivijualTeleCallingSession(db.Document):
    application = db.ReferenceField('EsthenosOrgApplication',required=True)
    organisation = db.ReferenceField('EsthenosOrg',required=True)
    group = db.ReferenceField('EsthenosOrgGroup',required=True)
    questions=db.DictField(required=False)
    score = db.FloatField(default=0,required=False)


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


class EsthenosOrgApplicationStatusType(db.Document):
    status = db.StringField(max_length=100, required=True,default="")
    status_message = db.StringField(max_length=512, required=True,default="")
    status_code = db.IntField(default=0)
    sub_status_code = db.IntField(default=0)
    sub_status_message = db.StringField(max_length=512, required=True,default="")

    def __unicode__(self):
        return self.status


class EsthenosOrgApplicationStatus(db.Document):
    status = db.ReferenceField('EsthenosOrgApplicationStatusType')
    status_message = db.StringField(max_length=512, required=True,default="")
    updated_on = db.DateTimeField(default=datetime.datetime.now)


class EsthenosOrgApplication(db.Document):
    owner = db.ReferenceField('EsthenosUser')
    group = db.ReferenceField('EsthenosOrgGroup')
    center = db.ReferenceField('EsthenosOrgCenter')
    branch = db.ReferenceField('EsthenosOrgBranch')
    product = db.ReferenceField('EsthenosOrgProduct', required=False)
    organisation = db.ReferenceField('EsthenosOrg')

    applicant_kyc = db.EmbeddedDocumentField(EsthenosOrgApplicationKYC)
    guarantor1_kyc = db.EmbeddedDocumentField(EsthenosOrgApplicationKYC)
    guarantor2_kyc = db.EmbeddedDocumentField(EsthenosOrgApplicationKYC)
    other_documents = db.ListField(db.EmbeddedDocumentField(EsthenosOrgApplicationKYC))

    business_lat = db.StringField(max_length=512, required=False, default="")
    business_lng = db.StringField(max_length=512, required=False, default="")

    tag = db.EmbeddedDocumentField(EsthenosOrgApplicationMap,required=False)
    timeline = db.ListField(db.ReferenceField('EsthenosOrgApplicationStatus'))

    updated_on = db.DateTimeField(default=datetime.datetime.now)
    date_created = db.DateTimeField(default=datetime.datetime.now)

    status = db.IntField(default=0)
    current_status = db.ReferenceField(EsthenosOrgApplicationStatusType)
    current_status_updated = db.DateTimeField(default=datetime.datetime.now)

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

    male_count = db.IntField(default=0.0)
    female_count = db.IntField(default=0.0)
    members_above18 =  db.IntField(default=0)
    members_less_than_18 =  db.IntField(default=0)
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

    family_assets_land_acres = db.FloatField(default=0)
    family_assets_orchard_acres = db.FloatField(default=0)
    family_assets_number_of_rented_houses_or_flats = db.FloatField(default=0)
    family_assets_number_of_rented_shops_or_godowns = db.FloatField(default=0)

    bank_name = db.StringField(max_length=200, required=False,default="")
    bank_ifsc_code = db.StringField(max_length=20, required=False,default="")
    bank_account_number = db.StringField(max_length=200, required=False,default="")
    bank_account_holder_name = db.StringField(max_length=200, required=False,default="")
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

    loan_eligibility_based_on_net_income = db.FloatField(default=0.0)
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
