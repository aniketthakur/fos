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

from p_user.views import dashboard_views
mainapp.register_blueprint( dashboard_views)

from p_tokens.views import token_views
mainapp.register_blueprint( token_views)


from reports.views import reports_views
mainapp.register_blueprint( reports_views)


from p_admin.views import server_views
mainapp.register_blueprint( server_views)

if __name__ == "__main__":
    manager.run()

