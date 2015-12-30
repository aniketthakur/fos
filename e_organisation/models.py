import datetime
from datetime import timedelta
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


class EsthenosOrgStatsApplication(object):

    def __init__(self):
        self.cb_passed = 0
        self.cb_failed = 0

        self.cf_passed = 0
        self.cf_failed = 0

        self.kyc_passed = 0
        self.kyc_failed = 0

        self.loan_amount = 0
        self.loan_leaked = 0 # if cb, cf or kyc fail.
        self.loan_applied = 0 # application submitted.
        self.loan_disbursed = 0

        self.scrutiny_done = 0
        self.scrutiny_ready = 0
        self.scrutiny_failed = 0
        self.scrutiny_passed = 0
        self.scrutiny_onhold = 0

        self.sanction_done = 0
        self.sanction_ready = 0
        self.sanction_failed = 0
        self.sanction_passed = 0
        self.sanction_onhold = 0

    def __add__(self, other):
        """ sum up application stats to return group stats."""
        stats = EsthenosOrgStatsApplication()
        stats.cb_passed = self.cb_passed + other.cb_passed
        stats.cb_failed = self.cb_failed + other.cb_failed
        stats.cf_passed = self.cf_passed + other.cf_passed
        stats.cf_failed = self.cf_failed + other.cf_failed
        stats.kyc_passed = self.kyc_passed + other.kyc_passed
        stats.kyc_failed = self.kyc_failed + other.kyc_failed
        stats.loan_amount = self.loan_amount + other.loan_amount
        stats.loan_leaked = self.loan_leaked + other.loan_leaked
        stats.loan_applied = self.loan_applied + other.loan_applied
        stats.loan_disbursed = self.loan_disbursed + other.loan_disbursed
        stats.sanction_done = self.sanction_done + other.sanction_done
        stats.sanction_ready = self.sanction_ready + other.sanction_ready
        stats.sanction_failed = self.sanction_failed + other.sanction_failed
        stats.sanction_passed = self.sanction_passed + other.sanction_passed
        stats.sanction_onhold = self.sanction_onhold + other.sanction_onhold
        stats.scrutiny_done = self.scrutiny_done + other.scrutiny_done
        stats.sanction_ready = self.scrutiny_ready + other.scrutiny_ready
        stats.sanction_failed = self.scrutiny_failed + other.scrutiny_failed
        stats.sanction_passed = self.scrutiny_passed + other.scrutiny_passed
        stats.sanction_onhold = self.scrutiny_onhold + other.scrutiny_onhold
        return stats

    def __eq__(self, other):
        return self.cb_passed == other.cb_passed \
        and self.cb_failed == other.cb_failed \
        and self.cf_passed == other.cf_passed \
        and self.cf_failed == other.cf_failed \
        and self.kyc_passed == other.kyc_passed \
        and self.kyc_failed == other.kyc_failed \
        and self.loan_amount == other.loan_amount \
        and self.loan_leaked == other.loan_leaked \
        and self.loan_applied == other.loan_applied \
        and self.loan_disbursed == other.loan_disbursed \
        and self.sanction_done == other.sanction_done \
        and self.sanction_ready == other.sanction_ready \
        and self.sanction_failed == other.sanction_failed \
        and self.sanction_passed == other.sanction_passed \
        and self.sanction_onhold == other.sanction_onhold \
        and self.scrutiny_done == other.scrutiny_done \
        and self.scrutiny_ready == other.scrutiny_ready \
        and self.scrutiny_failed == other.scrutiny_failed \
        and self.scrutiny_passed == other.scrutiny_passed \
        and self.scrutiny_onhold == other.scrutiny_onhold


class EsthenosOrgLocation(db.EmbeddedDocument):
    lat = db.FloatField(default=0.0)
    lng = db.FloatField(default=0.0)

    @property
    def json(self):
        return {
            "lat" : self.lat,
            "lng" : self.lng
        }

    def __unicode__(self):
      return "{'lat': %s, 'lng': %s}" % (self.lat, self.lng)


class EsthenosOrgTimeSlot(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    day = db.StringField(max_length=512, required=True, default="")
    time = db.StringField(max_length=512, required=True, default="")

    @property
    def json(self):
        return {
            "id" : str(self.id),
            "day" : self.day,
            "time" : self.time
        }

    def __unicode__(self):
      return "%s, %s" % (self.time, self.day)


class EsthenosOrgStatsDay(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    created = db.DateTimeField(default=datetime.datetime.now())
    updated = db.DateTimeField(default=datetime.datetime.now())
    key = db.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d'))

    cb_passed = db.IntField(default=0)
    cb_failed = db.IntField(default=0)

    cf_passed = db.IntField(default=0)
    cf_failed = db.IntField(default=0)

    kyc_passed = db.IntField(default=0)
    kyc_failed = db.IntField(default=0)

    cgt1_ready  = db.IntField(default=0)
    cgt1_passed = db.IntField(default=0)
    cgt1_failed = db.IntField(default=0)

    cgt2_ready  = db.IntField(default=0)
    cgt2_passed = db.IntField(default=0)
    cgt2_failed = db.IntField(default=0)

    disbursement_tat = db.IntField(default=0)
    disbursement_done = db.IntField(default=0)
    disbursement_ready = db.IntField(default=0)

    loans_leaked = db.IntField(default=0)
    loans_applied = db.IntField(default=0)
    loans_disbursed = db.IntField(default=0)
    loans_disbursed_amount = db.FloatField(default=0)

    count_scrutiny_ready = db.IntField(default=0)
    count_scrutiny_passed = db.IntField(default=0)
    count_scrutiny_failed = db.IntField(default=0)
    count_scrutiny_onhold = db.IntField(default=0)

    count_sanctions_ready = db.IntField(default=0)
    count_sanctions_passed = db.IntField(default=0)
    count_sanctions_failed = db.IntField(default=0)
    count_sanctions_onhold = db.IntField(default=0)

    def describe(self):
        print "key                     :", self.key
        print "cb_passed               :", self.cb_passed
        print "cb_failed               :", self.cb_failed
        print "cf_passed               :", self.cf_passed
        print "cf_failed               :", self.cf_failed
        print "kyc_passed              :", self.kyc_passed
        print "kyc_failed              :", self.kyc_failed
        print "cgt1_ready              :", self.cgt1_ready
        print "cgt1_passed             :", self.cgt1_passed
        print "cgt1_failed             :", self.cgt1_failed
        print "cgt2_ready              :", self.cgt2_ready
        print "cgt2_passed             :", self.cgt2_passed
        print "cgt2_failed             :", self.cgt2_failed
        print "disbursement_tat        :", self.disbursement_tat
        print "disbursement_done       :", self.disbursement_done
        print "disbursement_ready      :", self.disbursement_ready
        print "loans_leaked            :", self.loans_leaked
        print "loans_applied           :", self.loans_applied
        print "loans_disbursed         :", self.loans_disbursed
        print "loans_disbursed_amount  :", self.loans_disbursed_amount
        print "count_scrutiny_ready    :", self.count_scrutiny_ready
        print "count_scrutiny_passed   :", self.count_scrutiny_passed
        print "count_scrutiny_failed   :", self.count_scrutiny_failed
        print "count_scrutiny_onhold   :", self.count_scrutiny_onhold
        print "count_sanctions_ready   :", self.count_sanctions_ready
        print "count_sanctions_passed  :", self.count_sanctions_passed
        print "count_sanctions_failed  :", self.count_sanctions_failed
        print "count_sanctions_onhold  :", self.count_sanctions_onhold

    def __add__(self, other):
        stats = EsthenosOrgStatsDay(organisation=self.organisation, key=self.key)
        stats.cb_passed = self.cb_passed + other.cb_passed
        stats.cb_failed = self.cb_failed + other.cb_failed

        stats.cf_passed = self.cf_passed + other.cf_passed
        stats.cf_failed = self.cf_failed + other.cf_failed

        stats.kyc_passed = self.kyc_passed + other.kyc_passed
        stats.kyc_failed = self.kyc_failed + other.kyc_failed

        stats.cgt1_ready  = self.cgt1_ready + other.cgt1_ready
        stats.cgt1_passed = self.cgt1_passed + other.cgt1_passed
        stats.cgt1_failed = self.cgt1_failed + other.cgt1_failed

        stats.cgt2_ready  = self.cgt2_ready + other.cgt2_ready
        stats.cgt2_passed = self.cgt2_passed + other.cgt2_passed
        stats.cgt2_failed = self.cgt2_failed + other.cgt2_failed

        stats.disbursement_tat = self.disbursement_tat + other.disbursement_tat
        stats.disbursement_done = self.disbursement_done + other.disbursement_done
        stats.disbursement_ready = self.disbursement_ready + other.disbursement_ready

        stats.loans_leaked = self.loans_leaked + other.loans_leaked
        stats.loans_applied = self.loans_applied + other.loans_applied
        stats.loans_disbursed = self.loans_disbursed + other.loans_disbursed
        stats.loans_disbursed_amount = self.loans_disbursed_amount + other.loans_disbursed_amount

        stats.count_sanctions_ready = self.count_sanctions_ready + other.count_sanctions_ready
        stats.count_sanctions_passed = self.count_sanctions_passed + other.count_sanctions_passed
        stats.count_sanctions_failed = self.count_sanctions_failed + other.count_sanctions_failed
        stats.count_sanctions_onhold = self.count_sanctions_onhold + other.count_sanctions_onhold

        stats.count_scrutiny_ready = self.count_scrutiny_ready + other.count_scrutiny_ready
        stats.count_scrutiny_passed = self.count_scrutiny_passed + other.count_scrutiny_passed
        stats.count_scrutiny_failed = self.count_scrutiny_failed + other.count_scrutiny_failed
        stats.count_scrutiny_onhold = self.count_scrutiny_onhold + other.count_scrutiny_onhold
        return stats

    def __sub__(self, other):
        stats = EsthenosOrgStatsDay(organisation=self.organisation, key=self.key)
        stats.cb_passed = self.cb_passed - other.cb_passed
        stats.cb_failed = self.cb_failed - other.cb_failed

        stats.cf_passed = self.cf_passed - other.cf_passed
        stats.cf_failed = self.cf_failed - other.cf_failed

        stats.kyc_passed = self.kyc_passed - other.kyc_passed
        stats.kyc_failed = self.kyc_failed - other.kyc_failed

        stats.cgt1_ready  = self.cgt1_ready - other.cgt1_ready
        stats.cgt1_passed = self.cgt1_passed - other.cgt1_passed
        stats.cgt1_failed = self.cgt1_failed - other.cgt1_failed

        stats.cgt2_ready  = self.cgt2_ready - other.cgt2_ready
        stats.cgt2_passed = self.cgt2_passed - other.cgt2_passed
        stats.cgt2_failed = self.cgt2_failed - other.cgt2_failed

        stats.disbursement_tat = self.disbursement_tat - other.disbursement_tat
        stats.disbursement_done = self.disbursement_done - other.disbursement_done
        stats.disbursement_ready = self.disbursement_ready - other.disbursement_ready

        stats.loans_leaked = self.loans_leaked - other.loans_leaked
        stats.loans_applied = self.loans_applied - other.loans_applied
        stats.loans_disbursed = self.loans_disbursed - other.loans_disbursed
        stats.loans_disbursed_amount = self.loans_disbursed_amount - other.loans_disbursed_amount

        stats.count_sanctions_ready = self.count_sanctions_ready - other.count_sanctions_ready
        stats.count_sanctions_passed = self.count_sanctions_passed - other.count_sanctions_passed
        stats.count_sanctions_failed = self.count_sanctions_failed - other.count_sanctions_failed
        stats.count_sanctions_onhold = self.count_sanctions_onhold - other.count_sanctions_onhold

        stats.count_scrutiny_ready = self.count_scrutiny_ready - other.count_scrutiny_ready
        stats.count_scrutiny_passed = self.count_scrutiny_passed - other.count_scrutiny_passed
        stats.count_scrutiny_failed = self.count_scrutiny_failed - other.count_scrutiny_failed
        stats.count_scrutiny_onhold = self.count_scrutiny_onhold - other.count_scrutiny_onhold
        return stats

    def __mul__(self, other):
        return reduce(lambda x, y: x + y, [self for index in range(other)])

    def __eq__(self, other):
        return self.key == other.key \
           and self.cb_passed == self.cb_passed \
           and self.cb_failed == other.cb_failed \
           and self.cf_passed == other.cf_passed \
           and self.cf_failed == other.cf_failed \
           and self.kyc_passed == other.kyc_passed \
           and self.kyc_failed == other.kyc_failed \
           and self.cgt1_ready  == other.cgt1_ready \
           and self.cgt1_passed == other.cgt1_passed \
           and self.cgt1_failed == other.cgt1_failed \
           and self.cgt2_ready  == other.cgt2_ready \
           and self.cgt2_passed == other.cgt2_passed \
           and self.cgt2_failed == other.cgt2_failed \
           and self.disbursement_tat == other.disbursement_tat \
           and self.disbursement_done == other.disbursement_done \
           and self.disbursement_ready == other.disbursement_ready \
           and self.loans_leaked == other.loans_leaked \
           and self.loans_applied == other.loans_applied \
           and self.loans_disbursed == other.loans_disbursed \
           and self.loans_disbursed_amount == other.loans_disbursed_amount \
           and self.count_sanctions_ready == other.count_sanctions_ready \
           and self.count_sanctions_passed == other.count_sanctions_passed \
           and self.count_sanctions_failed == other.count_sanctions_failed \
           and self.count_sanctions_onhold == other.count_sanctions_onhold \
           and self.count_scrutiny_ready == other.count_scrutiny_ready \
           and self.count_scrutiny_passed == other.count_scrutiny_passed \
           and self.count_scrutiny_failed == other.count_scrutiny_failed \
           and self.count_scrutiny_onhold == other.count_scrutiny_onhold \

    def __unicode__(self):
        return "day-stats: %s" % self.key

    @property
    def total_tat(self):
        return self.disbursement_tat / min(1, self.created.day)

    @property
    def total_conversion(self):
        fraction = (float(self.loans_disbursed) / max(1, self.loans_applied))
        return "%.2f" % (fraction * 100)


class EsthenosOrgStatsMonth(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    created = db.DateTimeField(default=datetime.datetime.now())
    updated = db.DateTimeField(default=datetime.datetime.now())
    key = db.StringField(default=datetime.datetime.now().strftime('%Y-%m'))

    # k, v = year-month-day, EsthenosOrgStatsDay
    stats_daily = db.DictField(required=False)
    stats_total = db.DictField(required=False)

    def day(self, time):
        """ return the latest stat as of for the given day. """
        key = time.strftime('%Y-%m-%d')
        return self.stats_total.get(key, EsthenosOrgStatsDay(organisation=self.organisation, key=key))

    def only(self, time, delta=timedelta(days=1)):
        """ return the latest stat as of for the given day. """
        key = time.strftime('%Y-%m-%d')
        return self.stats_daily.get(key, EsthenosOrgStatsDay(organisation=self.organisation, key=key))

    def week(self, time):
        """ return the latest stat as of for the given week. """
        day1 = self.day(time)
        day2 = self.day(time - timedelta(days=(time.weekday()+1)))
        return day1 - day2

    def update(self, stat, time):
        """ update the stat object for today in the daily list. """
        curkey = time.strftime('%Y-%m-%d')
        if curkey in self.stats_daily: self.stats_daily.get(curkey).delete()
        if curkey in self.stats_total: self.stats_total.get(curkey).delete()

        # previous day, if its non-existent or prev month (ie. again not existent) we're good.
        prevkey = (time - timedelta(days=1)).strftime('%Y-%m-%d')
        prevday = self.stats_total.get(prevkey, EsthenosOrgStatsDay(organisation=self.organisation, key=prevkey))

        stat.key = curkey
        stat.save()
        self.stats_daily.update({curkey: stat})

        total = stat + prevday
        total.key = curkey
        total.save()
        self.stats_total.update({curkey: total})
        self.save()

    def __add__(self, other):
        """ returns sum of month stats, required for charts where users have sparse regions allocated. """
        stat = EsthenosOrgStatsMonth(organisation=self.organisation, key=self.key)
        keys = set(self.stats_daily.keys()).union(other.stats_daily.keys())

        for key in keys:
            stat1 = self.stats_daily.get(key, EsthenosOrgStatsDay(organisation=self.organisation, key=key))
            stat2 = other.stats_daily.get(key, EsthenosOrgStatsDay(organisation=self.organisation, key=key))
            stat.stats_daily.update({key: stat1 + stat2})

            stat1 = self.stats_total.get(key, EsthenosOrgStatsDay(organisation=self.organisation, key=key))
            stat2 = other.stats_total.get(key, EsthenosOrgStatsDay(organisation=self.organisation, key=key))
            stat.stats_total.update({key: stat1 + stat2})
        return stat

    def __eq__(self, other):
        return self.key == other.key \
           and len(self.stats_daily) == len(other.stats_daily) \
           and set(self.stats_daily) == set(other.stats_daily) \
           and reduce(lambda x, y: x == y, [self.stats_daily[key] == other.stats_daily[key] for key in self.stats_daily] + [True])

    def __unicode__(self):
        return "month-stats: %s" % self.key


class EsthenosOrgStatsGeo(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    created = db.DateTimeField(default=datetime.datetime.now)
    updated = db.DateTimeField(default=datetime.datetime.now)

    # k, v = year-month, EsthenosOrgStatsMonth
    stats_monthly = db.DictField(required=False)

    def month(self, time):
        key = time.strftime('%Y-%m')
        return self.stats_monthly.get(key, EsthenosOrgStatsMonth(organisation=self.organisation))

    def update(self, stat, time):
        """ update the stat object for today. """
        # previous month, if its non-existent we're good.
        curkey = time.strftime('%Y-%m')
        curmonth = self.stats_monthly.get(curkey, EsthenosOrgStatsMonth(organisation=self.organisation, key=curkey))
        curmonth.update(stat, time)
        curmonth.save()

        self.stats_monthly.update({curkey: curmonth})
        self.save()

    def __unicode__(self):
        return "geo-stats: %s" % self.id


class EsthenosOrgState(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    name = db.StringField(max_length=60, required=True)
    regions = db.ListField(db.ReferenceField('EsthenosOrgRegion'))
    owner = db.ReferenceField('EsthenosUser', default=None)
    stats = db.ReferenceField(EsthenosOrgStatsGeo)
    def add_region(self, name):
        regions_list = EsthenosOrgRegion.objects.filter(name=name, organisation=self.organisation, parent=self)
        if regions_list:
            return regions_list[0], True
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

    @staticmethod
    def create(organisation, name):
        stats = EsthenosOrgStatsGeo(organisation=organisation)
        stats.save()
        state, status = EsthenosOrgState.objects.get_or_create(
            name=name, organisation=organisation, stats=stats
        )
        state.save()
        return state, status

    def __unicode__(self):
        return self.name


class EsthenosOrgRegion(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgState)
    name = db.StringField(max_length=60, required=True)
    areas = db.ListField(db.ReferenceField('EsthenosOrgArea'))
    stats = db.ReferenceField(EsthenosOrgStatsGeo)
    owner = db.ReferenceField('EsthenosUser', default=None)

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
        areas_list = EsthenosOrgArea.objects.filter(name=name, organisation=self.organisation, parent=self)
        if areas_list:
            return areas_list[0], True
        stats = EsthenosOrgStatsGeo(organisation=self.organisation)
        stats.save()
        area, status = EsthenosOrgArea.objects.get_or_create(
            name=name, organisation=self.organisation, parent=self, stats=stats
        )
        self.areas.append(area)
        self.save()
        return area, status

    @staticmethod
    def create(name, parent):
        return parent.add_region(name)

    def __unicode__(self):
        return self.name


class EsthenosOrgArea(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgRegion)
    name = db.StringField(max_length=60, required=True)
    branches = db.ListField(db.ReferenceField('EsthenosOrgBranch'))
    stats = db.ReferenceField(EsthenosOrgStatsGeo)
    owner = db.ReferenceField('EsthenosUser', default=None)

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
        branches_list = EsthenosOrgBranch.objects.filter(name=name, organisation=self.organisation, parent=self)
        if branches_list:
            return branches_list[0], True

        stats = EsthenosOrgStatsGeo(organisation=self.organisation)
        stats.save()

        branch, status = EsthenosOrgBranch.objects.get_or_create(
            name=name, organisation=self.organisation, parent=self, stats=stats
        )
        self.branches.append(branch)
        self.save()
        return branch, status

    @staticmethod
    def create(name, parent):
        return parent.add_area(name)

    def __unicode__(self):
        return self.name


class EsthenosOrgBranch(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgArea)
    name = db.StringField(max_length=60, required=True)
    centers = db.ListField(db.ReferenceField('EsthenosOrgCenter'))
    stats = db.ReferenceField(EsthenosOrgStatsGeo)
    owner = db.ReferenceField('EsthenosUser', default=None)

    def stats_day(self, time):
        stats = [a.stats(time) for a in self.applications] + [EsthenosOrgStatsApplication()]
        stats = reduce(lambda x, y: x + y, stats)

        daystat = EsthenosOrgStatsDay(organisation=self.organisation, key=time.strftime('%Y-%m-%d'))

        daystat.cb_passed = stats.cb_passed
        daystat.cb_failed = stats.cb_failed
        daystat.cf_passed = stats.cf_passed
        daystat.cf_failed = stats.cf_failed
        daystat.kyc_passed = stats.kyc_passed
        daystat.kyc_failed = stats.kyc_failed
        daystat.cgt1_ready = stats.cgt1_ready
        daystat.cgt1_passed = stats.cgt1_passed
        daystat.cgt1_failed = stats.cgt1_failed
        daystat.cgt2_ready  = stats.cgt2_ready
        daystat.cgt2_passed = stats.cgt2_passed
        daystat.cgt2_failed = stats.cgt2_failed
        daystat.disbursement_tat = stats.disbursement_tat
        daystat.disbursement_done = stats.disbursement_done
        daystat.disbursement_ready = stats.disbursement_ready
        daystat.loans_leaked = stats.loans_leaked
        daystat.loans_applied = stats.loans_applied
        daystat.loans_disbursed = stats.loans_disbursed
        daystat.loans_disbursed_amount = stats.loans_disbursed_amount
        daystat.count_disbursed_groups = 1 if stats.loans_disbursed > 0 else 0
        daystat.count_disbursed_centers = 1 if stats.loans_disbursed > 0 else 0

        daystat.scrutiny_done = stats.scrutiny_done
        daystat.scrutiny_ready = stats.scrutiny_ready
        daystat.scrutiny_failed = stats.scrutiny_failed
        daystat.scrutiny_passed = stats.scrutiny_passed
        daystat.scrutiny_onhold = stats.scrutiny_onhold

        daystat.sanction_done = stats.sanction_done
        daystat.sanction_ready = stats.sanction_ready
        daystat.sanction_failed = stats.sanction_failed
        daystat.sanction_passed = stats.sanction_passed
        daystat.sanction_onhold = stats.sanction_onhold

        return daystat

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
        stat = EsthenosOrgStatsGeo(organisation=self.organisation)
        stat.save()
        center, status = EsthenosOrgCenter.objects.get_or_create(
            name=name, stats=stat, organisation=self.organisation, parent=self,
            center_id=EsthenosOrgCenter.unique_id(self.organisation)
        )
        self.centers.append(center)
        self.save()
        self.organisation.update(inc__center_count=1)
        return center, status

    @staticmethod
    def create(name, parent):
        return parent.add_branch(name)

    def applications(self):
        return EsthenosOrgApplication.objects.filter(branch=self)


    def __unicode__(self):
        return self.name


class EsthenosOrgCenter(db.Document):
    organisation = db.ReferenceField(EsthenosOrg)
    parent = db.ReferenceField(EsthenosOrgBranch)
    name = db.StringField(max_length=60, required=True)
    groups = db.ListField(db.ReferenceField('EsthenosOrgGroup'))
    stats = db.ReferenceField(EsthenosOrgStatsGeo)

    owner = db.ReferenceField('EsthenosUser', default=None)
    officer = db.StringField(max_length=60, required=True, default="")
    officer_phone_number = db.StringField(max_length=60, required=True, default="")

    center_id = db.StringField(max_length=10, required=False)
    center_timeslot = db.DateTimeField(required = False)

    timeslot = db.ReferenceField(EsthenosOrgTimeSlot, required=False)
    location = db.EmbeddedDocumentField(EsthenosOrgLocation, default=EsthenosOrgLocation)


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

    access_states = db.ListField(db.ReferenceField(EsthenosOrgState))
    access_regions = db.ListField(db.ReferenceField(EsthenosOrgRegion))
    access_areas = db.ListField(db.ReferenceField(EsthenosOrgArea))
    access_branches = db.ListField(db.ReferenceField(EsthenosOrgBranch))

    hierarchy = db.ReferenceField(EsthenosOrgHierarchy, required=True)
    organisation = db.ReferenceField(EsthenosOrg, required=True)


    def append_place(self, place):
        if isinstance(place, EsthenosOrgState):
            self.access_states.append(place)

        if isinstance(place, EsthenosOrgRegion):
            self.access_regions.append(place)

        if isinstance(place, EsthenosOrgArea):
            self.access_areas.append(place)

        if isinstance(place, EsthenosOrgBranch):
            self.access_branches.append(place)

        if isinstance(place, EsthenosOrgCenter):
            self.access_centers.append(place)
        place.owner = self
        place.save()
        self.save()

    def is_admin(self):
        return self.hierarchy.is_admin()

    def access_geo(self, place_string):
        level = self.hierarchy.level
        value = -1
        if place_string=="states":
            value = 3
        if place_string=="regions":
            value = 4
        if place_string=="areas":
            value = 5
        if place_string=="branches":
            value = 6
        if place_string=="centers":
            value = 7
        if place_string=="groups":
            value = 8

        return level<=value

    def is_allowed(self, feature):
        # delegating it to hierarchy,
        # so that this may later be fine tuned.
        return self.hierarchy.has_permission(feature)

    @property
    def states(self):
        if self.hierarchy.access=="":
            return EsthenosOrgState.objects.filter(organisation=self.organisation)
        return self.access_states

    @property
    def regions(self):
        if self.hierarchy.access=="":
            return EsthenosOrgRegion.objects.filter(organisation=self.organisation)
        return self.access_regions

    @property
    def areas(self):
        if self.hierarchy.access=="":
            return EsthenosOrgArea.objects.filter(organisation=self.organisation)
        return self.access_areas

    @property
    def branches(self):
        if self.hierarchy.access=="":
            return EsthenosOrgBranch.objects.filter(organisation=self.organisation)
        return self.access_branches

    @property
    def name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def phone_number(self):
        return "%s %s" % (self.postal_tele_code, self.postal_telephone)

    def stats(self, time):
        """ return the aggregate stat object, for all regions assigned to the user. """
        if self.hierarchy.access == "":
            stats = \
              [EsthenosOrgStatsMonth(organisation=self.organisation)] + \
              [geo.stats.month(time) for geo in EsthenosOrgState.objects.filter(organisation=self.organisation) ]

        else:
            stats = \
              [EsthenosOrgStatsMonth(organisation=self.organisation)] + \
              [geo.stats.month(time) for geo in self.states ]  + \
              [geo.stats.month(time) for geo in self.regions]  + \
              [geo.stats.month(time) for geo in self.areas]    + \
              [geo.stats.month(time) for geo in self.branches]

        stats = reduce(lambda x, y: x + y, stats)
        return stats

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

    @property
    def kyc_docs(self):
        return self.pan_docs + self.aadhar_docs + self.voterid_docs

    @property
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

        self.application_cgt1_done = self.calc_status(applications, 190)
        self.application_cgt2_done = self.calc_status(applications, 194)

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


class EsthenosOrgApplication(db.Document):
    owner = db.ReferenceField(EsthenosUser)
    group = db.ReferenceField(EsthenosOrgGroup)
    center = db.ReferenceField(EsthenosOrgCenter)
    branch = db.ReferenceField(EsthenosOrgBranch)
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
    name = db.StringField(max_length=512, required=False,default="")
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
        return self.net_income() / 2 * 60

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

    def stats(self, time):
        date = time.date()
        stats = EsthenosOrgStatsApplication()
        for st in self.timeline:
            code, updated = st.status.status_code, st.updated_on.date()
            if code == 110 and updated == date:
                stats.loan_applied = 1

            if code == 125 and updated == date:
                stats.kyc_passed = 1

            if code == 150 and updated == date:
                stats.cb_passed = 1

            if code == 170 and updated == date:
                stats.cf_passed = 1

            if code == 180 and updated == date:
                stats.cf_failed = 1

            if code == 190 and updated == date:
                stats.scrutiny_ready = 1
            elif code == 192 and updated == date:
                stats.scrutiny_failed = 1
            elif code == 193 and updated == date:
                stats.scrutiny_passed = 1
            elif code == 194 and updated == date:
                stats.scrutiny_onhold = 1

            if code == 200 and updated == date:
                stats.sanction_ready = 1
            elif code == 202 and updated == date:
                stats.sanction_failed = 1
            elif code == 203 and updated == date:
                stats.sanction_passed = 1
            elif code == 204 and updated == date:
                stats.sanction_onhold = 1

            if code == 243 and updated == date:
                stats.loan_amount = self.product.loan_amount
                stats.loan_disbursed = 1
                stats.disbursement_tat = (self.date_created - date).days
                stats.disbursement_done = 1

            stats.loan_leaked = 1 if self.verification else 0

            #todo: add stages for cb/kyc failed.
            stats.cb_failed = 0
            stats.kyc_failed = 0
        return stats


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
    application_id = db.StringField(max_length=255, required=True,default="")
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
