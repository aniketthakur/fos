import os, sys
from esthenos import mainapp
from flask.ext.script import Manager, Server

manager = Manager(mainapp)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',port=8080)
)

from e_deploy.GunicornServer import GunicornServer
manager.add_command("rungunicorn", GunicornServer())

from esthenos import commands
commands.add_commands( manager)

from flask.ext.sauth.views import auth_views
mainapp.register_blueprint( auth_views)

from e_organisation.views import organisation_views
mainapp.register_blueprint( organisation_views)

from e_admin.views import admin_views
mainapp.register_blueprint( admin_views)

from e_tokens.views import token_views
mainapp.register_blueprint( token_views)

from e_reports.views import reports_views
mainapp.register_blueprint( reports_views)


if __name__ == "__main__":
    manager.run()
