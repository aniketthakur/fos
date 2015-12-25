from flask.ext.sauth.models import User
from flask.ext.script import Command, Option, prompt_bool

from random import randint
from itertools import permutations
from slacker import Slacker
from esthenos import db, settings
from e_organisation.models import *

counter = 1
def generate_name(prefix, count):
    global counter
    counter = counter + 1
    return "%s%s%s" % (prefix, count, counter)

def notify(message, channel="#general", username="fab-bot"):
    slack = Slacker('xoxp-6694899808-6694899856-10378717686-a7deb0')
    slack.chat.post_message(channel, message, username=username)
    print message

class DropDB(Command):
    """Drop existing database."""

    def run(self):
        if prompt_bool("Are you sure you want to loose all data for {DB}@{HOST}:{PORT}?".format(**settings.MONGODB_SETTINGS)):
            notify("\ndropping db: {DB} on {HOST}:{PORT} started.\n".format(**settings.MONGODB_SETTINGS))
            dbname = settings.MONGODB_SETTINGS["DB"]
            db.connection.drop_database(dbname)
            notify("dropping database {database} successful.".format(database=dbname))

class DescDB(Command):
    """Describes the db"""

    def run(self):
        print "users    count : %s" % EsthenosUser.objects.all().count()
        print "states   count : %s " % EsthenosOrgState.objects.all().count()
        print "regions  count : %s" % EsthenosOrgRegion.objects.all().count()
        print "areas    count : %s " % EsthenosOrgArea.objects.all().count()
        print "branches count : %s" % EsthenosOrgBranch.objects.all().count()
        print "centers  count : %s " % EsthenosOrgCenter.objects.all().count()
        print "groups   count : %s " % EsthenosOrgGroup.objects.all().count()

class InitDB(Command):
    """Initialize new database."""

    def run(self):
        notify("\ninitializing db: {DB} on {HOST}:{PORT}\n".format(**settings.MONGODB_SETTINGS))

        orgz = settings.ORGS_SETTINGS
        org, status = EsthenosOrg.objects.get_or_create(
            name = orgz["name"],
            email = orgz["email"],
            domain = orgz["org"],
            code = "1",
            postal_telephone = orgz["phone"],
            postal_tele_code = orgz["phone-code"],
            postal_address = orgz["postal-address"],
            postal_country = orgz["postal-country"],
            postal_state = orgz["postal-state"],
            postal_city = orgz["postal-city"],
            postal_code = orgz["postal-code"],
        )
        notify("{name} organisation created.".format(name=orgz["name"]))

        EsthenosOrgSettings.objects.get_or_create(organisation=org)
        notify("{name} organisation global settings created.".format(name=orgz["name"]))

        # only create hierarchy where a role is defined.
        hierarchy = filter(lambda x: x["role"] != "", orgz["hierarchy"])
        for item in hierarchy:
            he, st = EsthenosOrgHierarchy.objects.get_or_create(
                organisation = org,
                role=item["role"],
                level=item["level"],
                access=item["access"],
                title=item["title"],
                title_full=item["title_full"]
            )
        notify("{count} {name} hierarchy designations created.".format(count=len(hierarchy), name=orgz["name"]))

        users = orgz["users"]
        for user in users:
            emp = EsthenosUser(
                hierarchy = EsthenosOrgHierarchy.objects.get(role=user["role"]),
                organisation = org,
                active = user["active"],
                email = user["email"],
                last_name = user["lname"],
                first_name = user["fname"],
                date_of_birth = user["dob"],
                postal_city = user["city"],
                postal_state = user["state"],
                postal_country = user["country"],
                postal_address = user["address"],
                postal_telephone = user["telephone"],
                postal_tele_code = user["tele_code"],
            )
            emp.set_password(user["passwd"])
            emp.save()
            org.update(inc__employee_count=1)
        notify("{count} {name} users created.".format(count=len(users), name=orgz["name"]))
        for status in settings.APP_STATUS:
            status_type, temp = EsthenosOrgApplicationStatusType.objects.get_or_create(
                status = status["status"],
                status_code = status["status_code"],
                status_message = status["status_message"],
            )

            if "sub_status" in status:
                status_type.sub_status = status["sub_status"]

            if "sub_status_code" in status:
                status_type.sub_status_code = status["sub_status_code"]

            status_type.save()
        notify("{count} {name} application statuses created".format(count=len(settings.APP_STATUS), name=orgz["name"]))

        # calendar, status = EsthenosOrgCalendar.objects.get_or_create(organisation=org)
        # for day in orgz["calendar"]["days"]:
        #     for time in orgz["calendar"]["times"]:
        #         slot, status = EsthenosOrgTimeSlot.objects.get_or_create(
        #             organisation=org, time=time, day=day
        #         )
        #         calendar.timeslots.append(slot)
        # calendar.save()
        # notify("{count} {name} calendar timeslots created.".format(count=len(calendar.timeslots), name=orgz["name"]))
        notify("\nsuccessfully initialized db:{DB} on {HOST}:{PORT}\n".format(**settings.MONGODB_SETTINGS))

class TestDBApplications(Command):
    """Initialize the test applications"""

    def run(self):
        def create_applications(place):
            for index, offset in enumerate(permutations("abc")):
                application = generate(payload, ''.join(offset), index)
                application["group_id"] = str(place.id)
                application["branch_id"] = str(place.center.id)
                application["area_id"] = str(place.area.id)
                application["region_id"] = str(place.region.id)
                application["state_id"] = str(place.state.id)

        groups = EsthenosOrgGroup.objects.all()
        for group in groups:
            create_applications(group)

class TestDBGeography(Command):
    """Initialize test database."""

    def run(self):
        org = EsthenosOrg.objects.all()[0]
        orgz = settings.ORGS_SETTINGS

        def get_default_parent(level):
            # todo: this looks wierd nasty why are parents not fetched simple ?
            if level == 4:
                return None if EsthenosOrgState.objects.count()==0 else EsthenosOrgState.objects.all()[0]

            if level == 5:
                return None if EsthenosOrgRegion.objects.count()==0 else EsthenosOrgRegion.objects.all()[0]

            if level == 6:
                return None if EsthenosOrgArea.objects.count()==0 else EsthenosOrgArea.objects.all()[0]

            if level == 7:
                return None if EsthenosOrgBranch.objects.count()==0 else EsthenosOrgBranch.objects.all()[0]

            if level == 8:
                return None if EsthenosOrgCenter.objects.count()==0 else EsthenosOrgCenter.objects.all()[0]

            return None

        def level_api_call(level):
            # todo: this looks nasty.
            if level == 3:
                return EsthenosOrgState.objects.all()

            if level == 4:
                return EsthenosOrgRegion.objects.all()

            if level == 5:
                return EsthenosOrgArea.objects.all()

            if level == 6:
                return EsthenosOrgBranch.objects.all()

            if level == 7:
                return EsthenosOrgCenter.objects.all()

            if level == 8:
                return EsthenosOrgGroup.objects.all()

            return []

        def create_geo(name, parent, config):
            geo, access = None, config["access"]
            print name, parent, config

            if access == "states":
                geo, status = EsthenosOrgState.create(name=name, organisation=org)

            if access == "regions":
                geo, status = parent.add_region(name=name)

            if access == "areas":
                geo, status = parent.add_area(name=name)

            if access == "branches":
                geo, status = parent.add_branch(name=name)

            if access == "centers":
                geo, status = parent.add_center(name=name)

            if access == "groups":
                geo, status = parent.add_group(name=name)

            geo.save()
            return geo

        def create_geo_hierarchy(level, parent):
            if level > ( len(orgz["hierarchy"])-1 ):return

            config = orgz["hierarchy"][level]

            for index in range(0, config["test_places"]):
                name = generate_name(config["access"], index)
                place = create_geo(name, parent, config)
                create_geo_hierarchy(level + 1, place)

            if config["test_places"] == 0:
                create_geo_hierarchy(level + 1, get_default_parent(level + 1))

        print "creating groups, state, region, area and branch collections."
        create_geo_hierarchy(0, None)

        print "successfully created test-db:{DB} on {HOST}:{PORT}\n".format(**settings.MONGODB_SETTINGS)

class TestDBUser(Command):
    """initialized test users"""

    def create_user(index, org, hierarchy, email, fname):
        emp = EsthenosUser(
            hierarchy = hierarchy,
            email = email,
            active = True,
            last_name = fname,
            first_name = fname,
            organisation = org,
        )
        emp.set_password("123456")
        emp.save()
        org.update(inc__employee_count=1)
        return emp

    def create_users(self, org, config, domain):
        hierarchy = EsthenosOrgHierarchy.objects.get(
            organisation=org, role=config["role"]
        )
        title, level = hierarchy.title, hierarchy.level
        for index  in range(0, config["test_users"]):
            fname = "%s%s" % (title, index)
            email = "%s@%s" % (fname, domain)

            if EsthenosUser.objects.filter(email=email).count() == 0:
                self.create_user(org, hierarchy, email, fname)

    def run(self):
        org = EsthenosOrg.objects.all()[0]
        orgz = settings.ORGS_SETTINGS
        domain = settings.ORGS_SETTINGS["org"]
        hierarchies = filter(lambda x: x["role"] != "", orgz["hierarchy"])

        for config in hierarchies:
            self.create_users(org, config, domain)

class TestDBUserGeoAssign(Command):
    """assign geo entities to users created before hand."""
    orgz = settings.ORGS_SETTINGS

    def level_api_call(self, level):
        # todo: this looks nasty.
        if level == 3:
            return EsthenosOrgState.objects.all()

        if level == 4:
            return EsthenosOrgRegion.objects.all()

        if level == 5:
            return EsthenosOrgArea.objects.all()

        if level == 6:
            return EsthenosOrgBranch.objects.all()

        if level == 7:
            return EsthenosOrgCenter.objects.all()

        if level == 8:
            return EsthenosOrgGroup.objects.all()

        return []

    def assign_user_geo(self, level, org):
        if level >=( len(self.orgz["hierarchy"])-1 ): return

        config = self.orgz["hierarchy"][level]
        hierarchy = EsthenosOrgHierarchy.objects.get(role=config["role"])
        users = EsthenosUser.objects.filter(organisation=org, hierarchy=hierarchy)
        geos = self.level_api_call(level)

        for index in range(0, len(geos)):
            user = users[index % len(users)]
            geo = geos[index]
            user.append_place(geo)

            geo.owner = user
            geo.save()

        self.assign_user_geo(level+1, org)

    def run(self):
        org = EsthenosOrg.objects.all()[0]
        self.assign_user_geo(0, org)

class TestBootstrap(Command):

    def run(self):
        InitDB().run()
        print "Completed : initdb"
        TestDBGeography().run()
        print "Completed : test geographies creation"
        TestDBUser().run()
        print "Completed : test user creation"
        TestDBUserGeoAssign().run()
        print "Completed : test hierarchy assignment"

class AddUser( Command):
    """Adds a user to the database."""

    option_list = (
        Option( "--name", "-n", dest="name", help="User's name"),
        Option( "--email", "-e", dest="email", help="User's email"),
        Option( "--password", "-p", dest="password", help="User's password"),
    )

    def run( self, name, email, password):
        email = email.lower().strip()
        if( User.objects(email=email).count()):
            print "This email address already exists."
            return

        user = User.create_user( name, email, password)
        print "Created user with slug", user.slug

class AddRole( Command):
    """Adds a role to a user"""

    option_list = (
        Option( "--email", "-e", dest="email", help="User's email"),
        Option( "--role", "-r", dest="role", help="Role to add"),
    )

    def run( self, email, role):
        email = email.lower().strip()
        user = User.objects( email=email).first()
        if( not user):
            print "This email address does not exist."
            return

        user.add_role( role)
        user.save()

class RemoveRole( Command):
    """Removes a role from a user"""

    option_list = (
        Option( "--email", "-e", dest="email", help="User's email"),
        Option( "--role", "-r", dest="role", help="Role to remove"),
    )

    def run( self, email, role):
        email = email.lower().strip()
        user = User.objects( email=email).first()
        if( not user):
            print "This email address does not exist."
            return

        user.remove_role( role)
        user.save()

class RemoveUser( Command):
    """Removes a user from database"""

    option_list = (
        Option( "--email", "-e", dest="email", help="User's email"),
    )

    def run( self, email):
        email = email.lower().strip()
        user = User.objects( email=email).first()
        if( not user):
            print "This email address does not exist."
            return

        user.delete()
        print "user successfully removed."

class ShowRoles( Command):
    """Shows the roles a user has"""

    option_list = (
        Option( "--email", "-e", dest="email", help="User's email"),
    )

    def run( self, email):
        email = email.lower().strip()
        user = User.objects( email=email).first()
        if( not user):
            print "This email address does not exist."
            return

        if( user.roles):
            print "User's roles are:", ' '.join( user.roles)
        else:
            print "No roles found for the user."

class ShowUsers( Command):
    """Show the list of users"""

    def run( self):
        print "Total Users:", User.objects().count()

        for u in User.objects().order_by( "date_joined"):
            print "%s, %s" % (u.email.encode("utf-8"), u.name.encode("utf-8"))


def add_commands( manager):
    manager.add_command( 'initdb', InitDB())
    manager.add_command( 'dropdb', DropDB())
    manager.add_command( 'descdb', DescDB())
    manager.add_command( 'test-users', TestDBUser())
    manager.add_command( 'test-geography', TestDBGeography())
    manager.add_command( 'test-applications', TestDBApplications())
    manager.add_command( 'user-add', AddUser())
    manager.add_command( 'user-remove', RemoveUser())
    manager.add_command( 'user-add-role', AddRole())
    manager.add_command( 'user-remove-role', RemoveRole())
    manager.add_command( 'user-show-roles', ShowRoles())
    manager.add_command( 'user-show-users', ShowUsers())
    manager.add_command( 'assign-geo', TestDBUserGeoAssign() )
    manager.add_command( 'test-bootstrap', TestBootstrap() )
