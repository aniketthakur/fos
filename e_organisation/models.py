import datetime
from esthenos import db
from blinker import signal
from flask_sauth.models import BaseUser
from flask.ext.mongorest.resources import Resource


class EsthenosOrg(db.Document):
    code = db.StringField(max_length=5, required=False)
    name = db.StringField(max_length=512, required=True)
    about = db.StringField(max_length=255, required=False)
    domain = db.StringField(max_length=128, required=False)

    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    postal_address = db.StringField(max_length=255, required=False)
    postal_country = db.StringField(max_length=100, required=False)
    postal_code = db.StringField(max_length=10, required=False)
    postal_city = db.StringField(max_length=100, required=False)
    postal_state = db.StringField(max_length=100, required=False)
    postal_telephone = db.StringField(max_length=512, required=False)
    postal_tele_code = db.StringField(max_length=512, required=False)

    email = db.StringField( unique=True)
    group_count = db.IntField(default=1)
    center_count = db.IntField(default=1)

    admins = db.ListField(db.ReferenceField('EsthenosUser'))

    user_count = db.IntField(default=1)
    employee_count = db.IntField(default=1)
    application_count = db.IntField(default=0)

    def is_admin(self, user):
        return user in self.admins

    def __unicode__(self):
        return "%s, %s, %s, %s" % (self.name, self.email, self.group_count, self.center_count)


class EsthenosOrgHierarchy(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)

    role = db.StringField(max_length=10, required=True)
    title = db.StringField(max_length=10, required=True)
    title_full = db.StringField(max_length=50, required=True)

    level = db.IntField(required=True)
    access = db.StringField(required=True)
    features = db.ListField(db.StringField(max_length=255))

    def is_admin(self):
        return (self.level == 0) and ("ADMIN" in self.role)

    def has_permission(self, feature):
        return feature in self.features

    def __unicode__(self):
        return "%s: %s" % (self.title, self.features)


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
    organisation = db.ReferenceField(EsthenosOrg)
    to_user = db.ReferenceField('EsthenosUser')
    from_user = db.ReferenceField('EsthenosUser')
    read_state = db.BooleanField(default=False)
    message = db.StringField(max_length=255, required=True)
    notification_type = db.StringField(max_length=255, required=True)
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
    updated_on = db.DateTimeField(default=datetime.datetime.now)


class EsthenosOrgState(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    name = db.StringField(max_length=60, required=True)
    regions = db.ListField(db.ReferenceField('EsthenosOrgRegion'))

    def add_region(self, name):
        region, status = EsthenosOrgRegion.objects.get_or_create(
            name=name, organisation=self.organisation, parent=self
        )
        self.regions.append(region)
        self.save()
        return region, status

    @property
    def json(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
        }

    @property
    def children(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "count": len(self.regions),
            "children": [region.json for region in self.regions],
        }

    @property
    def hierarchy(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "regions": [region.hierarchy for region in self.regions]
        }

    def __unicode__(self):
        return self.name


class EsthenosOrgRegion(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgState)
    name = db.StringField(max_length=60, required=True)
    areas = db.ListField(db.ReferenceField('EsthenosOrgArea'))

    @property
    def state(self):
        return self.parent

    @property
    def json(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
        }

    @property
    def parents(self):
        return {
            "state": str(self.state.id),
        }

    @property
    def children(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "count": len(self.areas),
            "parents": self.parents,
            "children": [area.json for area in self.areas],
        }

    @property
    def hierarchy(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "parents": self.parents,
            "children": [area.hierarchy for area in self.areas]
        }

    def add_area(self, name):
        area, status = EsthenosOrgArea.objects.get_or_create(
            name=name, organisation=self.organisation, parent=self
        )
        self.areas.append(area)
        self.save()
        return area, status

    def __unicode__(self):
        return self.name


class EsthenosOrgArea(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgRegion)
    name = db.StringField(max_length=60, required=True)
    branches = db.ListField(db.ReferenceField('EsthenosOrgBranch'))

    @property
    def region(self):
        return self.parent

    @property
    def state(self):
        return self.parent.parent

    @property
    def json(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
        }

    @property
    def parents(self):
        return {
            "state": str(self.state.id),
            "region": str(self.region.id),
        }

    @property
    def children(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "count": len(self.branches),
            "parents": self.parents,
            "children": [branch.json for branch in self.branches],
        }

    @property
    def hierarchy(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "parents": self.parents,
            "children": [branch.hierarchy for branch in self.branches]
        }

    def add_branch(self, name):
        branch, status = EsthenosOrgBranch.objects.get_or_create(
            name=name, organisation=self.organisation, parent=self
        )
        self.branches.append(branch)
        self.save()
        return branch, status

    def __unicode__(self):
        return self.name


class EsthenosOrgBranch(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgArea)
    name = db.StringField(max_length=60, required=True)
    centers = db.ListField(db.ReferenceField('EsthenosOrgCenter'))

    @property
    def area(self):
        return self.parent

    @property
    def region(self):
        return self.parent.parent

    @property
    def state(self):
        return self.parent.parent.parent

    @property
    def json(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
        }

    @property
    def parents(self):
        return {
            "state": str(self.state.id),
            "region": str(self.region.id),
            "area": str(self.area.id),
        }

    @property
    def children(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "count": len(self.centers),
            "parents": self.parents,
            "children": [center.json for center in self.centers],
        }

    @property
    def hierarchy(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "parents": self.parents,
            "children": [center.hierarchy for center in self.centers]
        }

    def add_center(self, name):
        center, status = EsthenosOrgCenter.objects.get_or_create(
            name=name, organisation=self.organisation, parent=self,
            center_id=EsthenosOrgCenter.unique_id(self.organisation)
        )
        self.centers.append(center)
        self.save()
        self.organisation.update(inc__center_count=1)
        return center, status

    def __unicode__(self):
        return self.name


class EsthenosOrgCenter(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgBranch)
    name = db.StringField(max_length=60, required=True)
    groups = db.ListField(db.ReferenceField('EsthenosOrgGroup'))

    officer = db.StringField(max_length=60, required=True, default="")
    officer_phone_number = db.StringField(max_length=60, required=True, default="")

    center_id = db.StringField(max_length=10, required=False)
    center_timeslot = db.DateTimeField(required = False)

    @property
    def branch(self):
        return self.parent

    @property
    def area(self):
        return self.parent.parent

    @property
    def region(self):
        return self.parent.parent.parent

    @property
    def state(self):
        return self.parent.parent.parent.parent

    @property
    def json(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "time": self.center_timeslot,
        }

    @property
    def parents(self):
        return {
            "state": str(self.state.id),
            "region": str(self.region.id),
            "area": str(self.area.id),
            "branch": str(self.branch.id),
        }

    @property
    def children(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "count": len(self.groups),
            "parents": self.parents,
            "children": [group.json for group in self.groups],
        }

    @property
    def hierarchy(self):
        return {
            "id": str(self.id),
            "name": str(self.name),
            "time": self.center_timeslot,
            "parents": self.parents,
            "children": [group.json for group in self.groups]
        }

    def add_group(self, name):
        group, status = EsthenosOrgGroup.objects.get_or_create(
            name=name, organisation=self.organisation, parent=self,
            group_id=EsthenosOrgGroup.unique_id(self.organisation)
        )
        group.update_status(110)
        self.groups.append(group)
        self.save()
        self.organisation.update(inc__group_count=1)
        return group, status

    def __unicode__(self):
        return self.name

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

    @property
    def group_name(self):
        return self.name

    @property
    def center(self):
        return self.parent

    @property
    def branch(self):
        return self.parent.parent

    @property
    def area(self):
        return self.parent.parent.parent

    @property
    def region(self):
        return self.parent.parent.parent.parent

    @property
    def state(self):
        return self.parent.parent.parent.parent.parent

    def __unicode__(self):
        return self.name

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

    @property
    def json(self):
        return {
          'id' : str(self.id),
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


class EsthenosUser(BaseUser):
    last_name = db.StringField(max_length=255, required=True)
    first_name = db.StringField(max_length=255, required=True)

    email = db.StringField(max_length=255, required=False)
    gender = db.StringField(max_length=255, required=False)
    active = db.BooleanField(default=False)

    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField(default=datetime.datetime.now)

    date_of_birth = db.StringField(max_length=20, required=False)
    postal_address = db.StringField(max_length=255, required=False)
    postal_code = db.StringField(max_length=100, required=False)
    postal_city = db.StringField(max_length=100, required=False)
    postal_state = db.StringField(max_length=100, required=False)
    postal_country = db.StringField(max_length=100, required=False)
    postal_telephone = db.StringField(max_length=20, required=False)
    postal_tele_code = db.StringField(max_length=20, required=False)

    states = db.ListField(db.ReferenceField(EsthenosOrgState))
    regions = db.ListField(db.ReferenceField(EsthenosOrgRegion))
    areas = db.ListField(db.ReferenceField(EsthenosOrgArea))
    branches = db.ListField(db.ReferenceField(EsthenosOrgBranch))

    hierarchy = db.ReferenceField(EsthenosOrgHierarchy, required=True)
    organisation = db.ReferenceField(EsthenosOrg, required=True)

    def is_admin(self):
        return self.hierarchy.is_admin()

    def is_allowed(self, feature):
        # delegating it to hierarchy,
        # so that this may later be fine tuned.
        return self.hierarchy.has_permission(feature)

    @property
    def name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def phone_number(self):
        return "%s %s" % (self.postal_tele_code, self.postal_telephone)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


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


class EsthenosOrgUserPerformanceItem(db.EmbeddedDocument):
    owner = db.ReferenceField(EsthenosUser)
    name = db.StringField(max_length=256, required=True)
    created = db.DateTimeField(default=datetime.datetime.now)
    updated = db.DateTimeField(default=datetime.datetime.now)

    target = db.IntField(default=0)
    achieved = db.IntField(default=0)

    @property
    def percentage(self):
        return (self.achieved / max(self.target, 1)) * 100

    @property
    def json(self):
        return {
            "target" : self.target,
            "achieved" : self.achieved,
            "percentage" : self.percentage,
        }

    def __unicode__(self):
        return "name: %s, achievement: %s" % (self.name, self.percentage)


class EsthenosOrgUserPerformance(db.Document):
    owner = db.ReferenceField(EsthenosUser)
    hour = db.IntField(default=0, required=True)
    created = db.DateTimeField(default=datetime.datetime.now)
    updated = db.DateTimeField(default=datetime.datetime.now)

    apps_sourced = db.EmbeddedDocumentField(EsthenosOrgUserPerformanceItem,
                                            default=EsthenosOrgUserPerformanceItem(name="apps-sourced"))

    apps_disbursed = db.EmbeddedDocumentField(EsthenosOrgUserPerformanceItem,
                                              default=EsthenosOrgUserPerformanceItem(name="apps-disbursed"))

    amount_disbursed = db.EmbeddedDocumentField(EsthenosOrgUserPerformanceItem,
                                                default=EsthenosOrgUserPerformanceItem(name="amount-disbursed"))

    groups_disbursed = db.EmbeddedDocumentField(EsthenosOrgUserPerformanceItem,
                                               default=EsthenosOrgUserPerformanceItem(name="groups-disbursed"))

    centers_disbursed = db.EmbeddedDocumentField(EsthenosOrgUserPerformanceItem,
                                                default=EsthenosOrgUserPerformanceItem(name="centers-disbursed"))

    pending_grt = db.IntField(default=0)
    pending_cgt1 = db.IntField(default=0)
    pending_cgt2 = db.IntField(default=0)

    @property
    def json(self):
        return {
            "apps_sourced" : self.apps_sourced.json,
            "apps_disbursed" : self.apps_disbursed.json,
            "amount_disbursed" : self.amount_disbursed.json,
            "groups_disbursed" : self.groups_disbursed.json,
            "centers_disbursed" : self.centers_disbursed.json,

            "pending_grt" : self.pending_grt,
            "pending_cgt1" : self.pending_cgt1,
            "pending_cgt2" : self.pending_cgt2,
        }


class EsthenosOrgUserPerformanceTarget(db.Document):
    owner = db.ReferenceField(EsthenosUser)
    organisation = db.ReferenceField(EsthenosOrg)

    name = db.StringField(max_length=512, required=True)
    role = db.ReferenceField(EsthenosOrgHierarchy, required=True)

    end_date = db.DateTimeField(default=datetime.datetime.now)
    start_date = db.DateTimeField(default=datetime.datetime.now)

    loan_target = db.FloatField(default=0)
    group_target = db.FloatField(default=0)
    center_target = db.FloatField(default=0)

    business_target = db.FloatField(default=0)
    applications_target = db.IntField(default=0)


    created = db.DateTimeField(default=datetime.datetime.now)


class EsthenosOrgStats(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    granularity = db.StringField(max_length=20, required=True)
    created = db.DateTimeField(default=datetime.datetime.now)

    hour = db.IntField(default=0, required=True)
    endtime = db.DateTimeField(default=datetime.datetime.now, required=True)
    starttime = db.DateTimeField(default=datetime.datetime.now, required=True)

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

    application_telecalling_ready = db.IntField(default=0)
    application_telecalling_done = db.IntField(default=0)
    application_telecalling_passed = db.IntField(default=0)
    application_telecalling_failed = db.IntField(default=0)

    application_underwriting_ready = db.IntField(default=0)
    application_underwriting_done = db.IntField(default=0)

    application_disbursement_ready = db.IntField(default=0)
    application_disbursement_pending = db.IntField(default=0)
    application_disbursement_done = db.IntField(default=0)

    total_groups_disbursed = db.FloatField(default=0)
    total_centers_disbursed = db.FloatField(default=0)

    total_loans_disbursed = db.FloatField(default=0)
    total_loans_amount_disbursed = db.FloatField(default=0)

    total_loans_leaked = db.FloatField(default=0)
    total_loans_applied = db.FloatField(default=0)

    def calculate(self):
        print "calculating daily stats for start-time:%s end-time:%s" % (self.starttime, self.endtime)
        applications = EsthenosOrgApplication.objects.filter(
            organisation = self.organisation,
            current_status_updated__lte = self.endtime,
        )

        self.application_submitted = self.calc_status(applications, 110)

        self.application_cbcheck_done = self.calc_status(applications, 150)
        self.application_cf_done = self.calc_status(applications, 170)

        self.application_grt_done = self.calc_status(applications, 204)
        self.application_cgt1_done = self.calc_status(applications, 190)
        self.application_cgt2_done = self.calc_status(applications, 194)
        self.application_telecalling_done = self.calc_status(applications, 223)

        self.application_underwriting_done = self.calc_status(applications, 231)
        self.application_disbursement_done = self.calc_status(applications, 240)

        self.total_groups_disbursed = 1
        self.total_centers_disbursed = 1

        self.total_loans_disbursed = self.calc_status(applications, 240)
        self.total_loans_amount_disbursed = self.calc_status(applications, 240)

        self.total_loans_leaked = 1
        self.total_loans_applied = self.calc_status(applications, 110)

        self.save()

    def calc_apps(self, applications, status_code):
        def filter_status(x):
            return x.status.status_code == status_code

        def filter_time(x):
            return (x.updated_on >= self.starttime) and (x.updated_on <= self.endtime)

        def filter_app(x):
            return filter_time(x) and filter_status(x)

        apps = []
        for application in applications:
            apps += filter(filter_app, application.timeline)

        return apps

    def calc_status(self, applications, status_code):
        apps = self.calc_apps(applications, status_code)
        return len(apps)

    def rollup_daily(self):
        print "calculating daily stats for start-time:%s end-time:%s" % (self.starttime, self.endtime)
        print "calculation"


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
    spouse_aadhar_card_number = db.IntField(required=False, default=0)
    spouse_name = db.StringField(max_length=512, required=False,default="")

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


class EsthenosOrgApplicationFamilyDetails(db.EmbeddedDocument):
    age = db.IntField(required=False, default=0)
    name = db.StringField(max_length=20, required=False,default="")
    education = db.StringField(max_length=512, required=False,default="")
    aadhar_number = db.StringField(max_length=20, required=False,default="")
    annual_income = db.FloatField(required=False, default=0)
    occupations_details = db.StringField(max_length=512, required=False,default="")
    relation = db.StringField(max_length=512, required=False,default="")


class EsthenosOrgApplicationLandDetails(db.EmbeddedDocument):
    land_location = db.StringField(max_length=512, default="")
    type_of_property = db.StringField(max_length=512, default="")
    area_in_sqft = db.FloatField(default=0)
    loan_outstanding = db.FloatField(default=0)
    estimated_resale_value = db.FloatField(default=0)


class EsthenosOrgApplicationLoanDetails(db.EmbeddedDocument):
    type_of_loan= db.StringField(max_length=512, default="")
    interest= db.FloatField(default=0)
    name_of_bank= db.StringField(max_length=512, default="")
    emi_repayments= db.FloatField(default=0)
    outstanding_loan_amount= db.FloatField(default=0)
    collateral_details= db.StringField(max_length=512, default="")
    loan_detail= db.StringField(max_length=512, default="")
    tenure_in_months= db.FloatField(default=0)
    loan_amount_key= db.FloatField(default=0)


class EsthenosOrgApplicationTypeEquipment(db.EmbeddedDocument):
    estimated_value = db.FloatField(default=0)
    is_equipment_given_as_collateral = db.StringField(max_length=512, default="")
    date_of_manufacturing_equipment = db.StringField(max_length=512, default="")
    details_of_equipment_supplier= db.StringField(max_length=512, default="")


class EsthenosOrgApplicationDocsVehicle(db.EmbeddedDocument):
    year_of_registration = db.FloatField(default=0)
    estimated_resale_value = db.FloatField(default=0)
    type_of_vehicle_manufacturer = db.StringField(max_length=512, default="")


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
    disbursement_pdf_link = db.StringField(max_length=512, required=False, default="#")

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

    # caste = db.StringField(max_length=512, required=False,default="")
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

    residence_details = db.StringField(max_length=512, required=False,default="")
    house_stay_duration = db.FloatField(default=0.0)
    rent_agreement = db.StringField(max_length=512, required=False,default="")
    house_monthly_rent = db.FloatField(default=0.0)

    applied_loan = db.FloatField(default=0.0)
    purpose_of_loan = db.StringField(max_length=512, required=False,default="")

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

    details_of_finished_goods = db.StringField(max_length=512, required=False,default="")
    business_outreach_methods = db.StringField(max_length=512, required=False,default="")
    place_of_storage_for_material = db.StringField(max_length=512, required=False,default="")
    details_of_principal_raw_materials = db.StringField(max_length=512, required=False,default="")
    nature_of_keeping_business_accounts = db.StringField(max_length=512, required=False,default="")
    place_agency_of_purchase_of_materials = db.StringField(max_length=512, required=False,default="")
    business_assets_average_value_of_inventory = db.FloatField(default=0.0)
    business_assets_average_value_of_receivables = db.FloatField(default=0.0)

    other_income = db.FloatField(default=0.0)

    education_expenses = db.FloatField(default=0.0)
    medical_expenses = db.FloatField(default=0.0)
    grocery_expenses = db.FloatField(default=0.0)
    family_other_expenses = db.FloatField(default=0.0)
    conveyance_expenses = db.FloatField(default=0)

    electricity_charges = db.FloatField(default=0.0)
    freight_charges = db.FloatField(default=0.0)
    petrol_expenses = db.FloatField(default=0.0)
    other_expenses = db.FloatField(default=0.0)
    salaries_and_wages = db.FloatField(default=0.0)

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

    internet_data_uses = db.StringField(max_length=512, required=False, default="")
    mobile_services_provider = db.StringField(max_length=512, required=False, default="")
    billing_type = db.StringField(max_length=512, required=False, default="")
    handset_type = db.StringField(max_length=512, required=False, default="")
    average_monthly_bill = db.FloatField(default=0.0)

    electricity_monthly_bill = db.FloatField(default=0.0)
    power_supplier = db.StringField(max_length=512, required=False, default="")

    family_details1 = db.EmbeddedDocumentField(EsthenosOrgApplicationFamilyDetails, default=EsthenosOrgApplicationFamilyDetails)
    family_details2 = db.EmbeddedDocumentField(EsthenosOrgApplicationFamilyDetails, default=EsthenosOrgApplicationFamilyDetails)
    family_details3 = db.EmbeddedDocumentField(EsthenosOrgApplicationFamilyDetails, default=EsthenosOrgApplicationFamilyDetails)
    family_details4 = db.EmbeddedDocumentField(EsthenosOrgApplicationFamilyDetails, default=EsthenosOrgApplicationFamilyDetails)
    family_details5 = db.EmbeddedDocumentField(EsthenosOrgApplicationFamilyDetails, default=EsthenosOrgApplicationFamilyDetails)

    loan_details1 = db.EmbeddedDocumentField(EsthenosOrgApplicationLoanDetails, default=EsthenosOrgApplicationLoanDetails)
    loan_details2 = db.EmbeddedDocumentField(EsthenosOrgApplicationLoanDetails, default=EsthenosOrgApplicationLoanDetails)
    loan_details3 = db.EmbeddedDocumentField(EsthenosOrgApplicationLoanDetails, default=EsthenosOrgApplicationLoanDetails)
    loan_details4 = db.EmbeddedDocumentField(EsthenosOrgApplicationLoanDetails, default=EsthenosOrgApplicationLoanDetails)

    land_details1 = db.EmbeddedDocumentField(EsthenosOrgApplicationLandDetails, default=EsthenosOrgApplicationLandDetails)
    land_details2 = db.EmbeddedDocumentField(EsthenosOrgApplicationLandDetails, default=EsthenosOrgApplicationLandDetails)
    land_details3 = db.EmbeddedDocumentField(EsthenosOrgApplicationLandDetails, default=EsthenosOrgApplicationLandDetails)

    docs_vehicle1 = db.EmbeddedDocumentField(EsthenosOrgApplicationDocsVehicle, default=EsthenosOrgApplicationDocsVehicle)
    docs_vehicle2 = db.EmbeddedDocumentField(EsthenosOrgApplicationDocsVehicle, default=EsthenosOrgApplicationDocsVehicle)
    docs_vehicle3 = db.EmbeddedDocumentField(EsthenosOrgApplicationDocsVehicle, default=EsthenosOrgApplicationDocsVehicle)

    type_equipment1 = db.EmbeddedDocumentField(EsthenosOrgApplicationTypeEquipment, default=EsthenosOrgApplicationTypeEquipment)
    type_equipment2 = db.EmbeddedDocumentField(EsthenosOrgApplicationTypeEquipment, default=EsthenosOrgApplicationTypeEquipment)
    type_equipment3 = db.EmbeddedDocumentField(EsthenosOrgApplicationTypeEquipment, default=EsthenosOrgApplicationTypeEquipment)

    sales_revenue_in_1_month = db.FloatField(default=0.0)
    sales_revenue_in_5_month = db.FloatField(default=0.0)
    sales_revenue_in_4_month = db.FloatField(default=0.0)
    sales_revenue_in_3_month = db.FloatField(default=0.0)
    sales_revenue_in_10_month = db.FloatField(default=0.0)
    sales_revenue_in_12_month = db.FloatField(default=0.0)
    sales_revenue_in_8_month = db.FloatField(default=0.0)
    total_annual_revenue_credit = db.FloatField(default=0.0)
    sales_revenue_in_7_month = db.FloatField(default=0.0)
    sales_revenue_in_6_month = db.FloatField(default=0.0)
    sales_revenue_in_19_month = db.FloatField(default=0.0)
    total_annual_revenue_cash = db.FloatField(default=0.0)
    sales_revenue_in_2_month = db.FloatField(default=0.0)
    sales_revenue_in_11_month = db.FloatField(default=0.0)

    raw_material_purchase_in_5_month = db.FloatField(default=0.0)
    raw_material_purchase_in_7_month = db.FloatField(default=0.0)
    raw_material_purchase_in_4_month = db.FloatField(default=0.0)
    raw_material_purchase_in_3_month = db.FloatField(default=0.0)
    raw_material_purchase_in_8_month = db.FloatField(default=0.0)
    raw_material_purchase_in_10_month = db.FloatField(default=0.0)
    total_annual_purchase_cash = db.FloatField(default=0.0)
    raw_material_purchase_in_11_month = db.FloatField(default=0.0)
    total_annual_purchase_credit = db.FloatField(default=0.0)
    raw_material_purchase_in_2_month = db.FloatField(default=0.0)
    raw_material_purchase_in_12_month = db.FloatField(default=0.0)
    raw_material_purchase_in_9_month = db.FloatField(default=0.0)
    raw_material_purchase_in_1_month = db.FloatField(default=0.0)
    raw_material_purchase_in_6_month = db.FloatField(default=0.0)

    computer = db.StringField(max_length=512, required=False,default="")
    ref_y_n = db.StringField(max_length=512, required=False,default="")
    television = db.StringField(max_length=512, required=False,default="")
    other = db.StringField(max_length=512, required=False,default="")
    wm_y_n = db.StringField(max_length=512, required=False,default="")
    two_wheeler = db.StringField(max_length=512, required=False,default="")
    refrigerator = db.StringField(max_length=512, required=False,default="")
    other_y_n = db.StringField(max_length=512, required=False,default="")
    television_y_n = db.StringField(max_length=512, required=False,default="")
    comp_y_n = db.StringField(max_length=512, required=False,default="")
    two_wheeler_y_n = db.StringField(max_length=512, required=False,default="")
    washing_machine = db.StringField(max_length=512, required=False,default="")

    address = db.StringField(max_length=512, required=False,default="") #[All other are Customer Details from 1 to 5]
    name_4 = db.StringField(max_length=512, required=False,default="")
    name_3 = db.StringField(max_length=512, required=False,default="")
    address_5 = db.StringField(max_length=512, required=False,default="")
    name_2 = db.StringField(max_length=512, required=False,default="")
    name_5 = db.StringField(max_length=512, required=False,default="")
    telephone_no_4 = db.FloatField(default=0.0)
    address_4 = db.StringField(max_length=512, required=False,default="")
    address_2 = db.StringField(max_length=512, required=False,default="")
    institution_credit = db.StringField(max_length=512, required=False,default="")#(This Field is from page "Business info:Details of Key Customers")
    telephone_no_3 = db.FloatField(default=0.0)
    address_3 = db.StringField(max_length=512, required=False,default="")
    telephone_no_2 = db.FloatField(default=0.0)
    name = db.StringField(max_length=512, required=False,default="")
    individual_credit =  db.StringField(max_length=512, required=False,default="")#(This Field is from page "Business info:Details of Key Customers")
    telephone_no_5 = db.FloatField(default=0.0)
    telephone_no = db.FloatField(default=0.0)

    permanent_employees = db.IntField(required=True,default=0)
    average_monthly_wage_for_relatives = db.FloatField(default=0.0)
    relatives_in_business = db.IntField(required=True,default=0)
    wages_paid = db.StringField(max_length=512, required=False,default="")
    average_monthly_wage_for_contract_employees = db.FloatField(default=0.0)
    contract_employees = db.IntField(required=True,default=0)
    average_monthly_wage_for_permanent_employees = db.FloatField(default=0.0)

    insurance_policies = db.IntField(required=True,default=0)
    loans_from_whom = db.StringField(max_length=512, required=False,default="")
    creditors_for_raw_material = db.FloatField(default=0.0)
    raw_material_in_han = db.FloatField(default=0.0)
    loan_outstanding_against_agriculture= db.FloatField(default=0.0)
    loan_outstanding_against_residential= db.FloatField(default=0.0)
    vehicle_loans =  db.IntField(required=True,default=0)
    loan_outstanding_against_commercial_= db.FloatField(default=0.0)
    cash_and_bank_balance= db.FloatField(default=0.0)
    vehicles_resale_value= db.FloatField(default=0.0)
    immovable_estimated_value_agriculture= db.FloatField(default=0.0)
    immovable_estimated_value_residential= db.FloatField(default=0.0)
    immovable_estimated_value_commercial= db.FloatField(default=0.0)
    fixed_deposit_and_ppf= db.FloatField(default=0.0)
    receivables_from_customer= db.FloatField(default=0.0)
    gold_and_jewellery= db.FloatField(default=0.0)

    permissions_licenses_reqd = db.StringField(max_length=512, required=False,default="")
    business_name = db.StringField(max_length=512, required=False,default="")
    type_of_business_entity = db.StringField(max_length=512, required=False,default="")
    area_market_value= db.FloatField(default=0.0)
    vat_service_tax_regn_no = db.StringField(max_length=512, required=False,default="")
    monthly_rent= db.FloatField(default=0.0)
    ssi_registration_entrepeneur_memorandum_ref_no = db.StringField(max_length=512, required=False,default="")
    description_business = db.StringField(max_length=512, required=False,default="")
    registered_rent_agreement = db.StringField(max_length=512, required=False,default="")
    shops__establishment_no = db.StringField(max_length=512, required=False,default="")
    no_of_years_in_business = db.IntField(required=True,default=0)
    workplace_details = db.StringField(max_length=512, required=False,default="")
    pancard_no = db.StringField(max_length=512, required=False,default="")
    area_occupied= db.FloatField(default=0.0)
    outstanding_loan= db.FloatField(default=0.0)
    address_of_place_of_business = db.StringField(max_length=512, required=False,default="")

    issue_bank_2 = db.StringField(max_length=512, required=False,default="")
    issue_bank_1 = db.StringField(max_length=512, required=False,default="")
    issue_bank_3 = db.StringField(max_length=512, required=False,default="")

    no_borrowers_you_furnished_guarantees__ = db.StringField(max_length=512, required=False,default="")

    @property
    def total_income(self):
        return self.total_annual_revenue_cash \
              + self.total_annual_revenue_credit

    @property
    def total_expenditure(self):
        return self.house_monthly_rent\
              + self.average_monthly_bill\
              + self.electricity_monthly_bill \
              + self.grocery_expenses \
              + self.conveyance_expenses \
              + self.medical_expenses \
              + self.education_expenses \
              + self.family_other_expenses \
              + self.monthly_rent \
              + self.electricity_charges \
              + self.petrol_expenses \
              + self.freight_charges \
              + self.salaries_and_wages \
              + self.other_expenses \
              + self.loan_details1.emi_repayments \
              + self.loan_details2.emi_repayments \
              + self.loan_details3.emi_repayments \
              + self.loan_details4.emi_repayments \
              + self.average_monthly_purchase

    @property
    def average_monthly_purchase(self):
        return round((self.total_annual_purchase_cash \
              + self.total_annual_purchase_credit)/12, 0)

    @property
    def average_monthly_income(self):
        return round((self.total_annual_revenue_cash \
              + self.total_annual_revenue_credit)/12, 0)

    def total_other_outstanding(self):
        return self.other_outstanding_emi \
              + self.other_outstanding_chit \
              + self.other_outstanding_insurance \
              + self.other_outstanding_familynfriends

    @property
    def net_income(self):
        return self.average_monthly_income \
              - self.total_expenditure

    def business_expense(self):
        return self.secondary_business_expenses_monthly \
              + self.tertiary_business_expenses_monthly \
              + self.primary_business_expense_rent \
              + self.primary_business_expense_admin \
              + self.primary_business_expense_other \
              + self.primary_business_expense_working_capital \
              + self.primary_business_expense_employee_salary

    @property
    def loan_eligibility_based_on_net_income(self):
        return self.net_income / 2 * 60

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