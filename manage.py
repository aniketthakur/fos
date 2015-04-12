__author__ = 'prathvi'
# Set the path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from flask.ext.script import Manager, Server
from esthenos  import mainapp

manager = Manager(mainapp)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',port=8080)
)

from GunicornServer import GunicornServer
manager.add_command("rungunicorn", GunicornServer())

import flask_sauth.commands
flask_sauth.commands.add_commands( manager)

#never ever copy this to pitaya/__init__.py
#user auth

from flask.ext.sauth.views import auth_views
mainapp.register_blueprint( auth_views)
from e_organisation.views import organisation_views
mainapp.register_blueprint( organisation_views)


from e_admin.views import admin_views
mainapp.register_blueprint( admin_views)

from e_tokens.views import token_views
mainapp.register_blueprint( token_views)


from reports.views import reports_views
mainapp.register_blueprint( reports_views)



from e_admin_reports.views import admin_reports_views
mainapp.register_blueprint( admin_reports_views)

if __name__ == "__main__":
    manager.run()

