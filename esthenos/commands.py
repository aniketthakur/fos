from flask.ext.sauth.models import User
from flask.ext.script import Command, Option, prompt_bool

from slacker import Slacker
from esthenos import db, settings
from e_organisation.models import *


def notify(message, channel="#general", username="fab-bot"):
    slack = Slacker('xoxp-6694899808-6694899856-10378717686-a7deb0')
    print message
    slack.chat.post_message(channel, message, username=username)

class DropDB(Command):
    """Drop existing database."""

    def run(self):
        if prompt_bool("Are you sure you want to loose all data for {DB}@{HOST}:{PORT}?".format(**settings.MONGODB_SETTINGS)):
            notify("\ndropping db: {DB} on {HOST}:{PORT} started.\n".format(**settings.MONGODB_SETTINGS))
            dbname = settings.MONGODB_SETTINGS["DB"]
            db.connection.drop_database(dbname)
            notify("dropping database {database} successful.".format(database=dbname))


class InitDB(Command):
    """Initialize new database."""

    def run(self):
        print "dropping collections & creating new accounts and organization."
        notify("\ninitializing db: {DB} on {HOST}:{PORT}\n".format(**settings.MONGODB_SETTINGS))

        notify("dropping all organisations.")
        EsthenosOrg().drop_collection()
        organisations = settings.ORGS_SETTINGS
        for orgz in organisations:
            print "dropping & creating organization : %s" % orgz["name"]
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

            print "dropping & creating user hierarchy for : %s" % orgz["name"]
            # EsthenosOrgHierarchy().drop_collection()
            hierarchy = orgz["hierarchy"]
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

            notify("dropped all settings.")
            EsthenosOrgSettings.drop_collection()
            EsthenosOrgSettings().save()

            notify("dropped all settings.")
            EsthenosSettings.drop_collection()
            EsthenosSettings().save()

            print "dropping & creating esthenos users."
            EsthenosUser.drop_collection()

            print "dropping & creating users for : %s" % orgz["name"]
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
            print "{count} {name} users created.".format(count=len(users), name=orgz["name"])

            notify("dropping groups, state, region, area and branch collections.")
            EsthenosOrgArea.drop_collection()
            EsthenosOrgState.drop_collection()
            EsthenosOrgGroup.drop_collection()
            EsthenosOrgCenter.drop_collection()
            EsthenosOrgBranch.drop_collection()
            EsthenosOrgRegion.drop_collection()

            def generate_name(prefix, count):
                return "%s%s" % (prefix, count)

        print "dropping & creating application status types."
        EsthenosOrgApplicationStatusType.drop_collection()
        for status in settings.APP_STATUS:
            status_type = EsthenosOrgApplicationStatusType()
            status_type.status = status["status"]
            status_type.status_code = status["status_code"]
            status_type.status_message = status["status_message"]

            if "sub_status" in status:
                status_type.sub_status = status["sub_status"]

            if "sub_status_code" in status:
                status_type.sub_status_code = status["sub_status_code"]

            status_type.save()
        notify("{count} application statuses created".format(count=len(settings.APP_STATUS)))

        notify("dropping all existing applications.")
        EsthenosOrgApplication.drop_collection()

        notify("\nsuccessfully initialized db:{DB} on {HOST}:{PORT}\n".format(**settings.MONGODB_SETTINGS))


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
    manager.add_command( 'user-add', AddUser())
    manager.add_command( 'user-remove', RemoveUser())
    manager.add_command( 'user-add-role', AddRole())
    manager.add_command( 'user-remove-role', RemoveRole())
    manager.add_command( 'user-show-roles', ShowRoles())
    manager.add_command( 'user-show-users', ShowUsers())
