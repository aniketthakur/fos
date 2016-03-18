import os, sys, requests, json
from fabric.api import *
from slacker import Slacker
from datetime import datetime
from fabric.contrib.files import *
from fabric.contrib.project import rsync_project
from subprocess import check_output
from esthenos import version as ver
from esthenos.notify import notify
from esthenos.settings import SERVER_SETTINGS as client
from esthenos.settings import MONGODB_SETTINGS as database

from jinja2 import Environment, PackageLoader
jinja = Environment(loader=PackageLoader('esthenos', 'templates'))

env.user = client["user-deploy"]
env.hosts = [client["host"]]
env.key_filename = "~/.ssh/esthenos.ops.key"
env.use_ssh_config = True

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = '/home/ubuntu'
PIDS_DIR = '/var/run/esthenos/'
LOGS_DIR = '/var/log/esthenos/'
TIMEZONE = client["timezone"]
DEPLOY_PATH = '%s/esthenos' % HOME_DIR
SLACKURL = "https://hooks.slack.com/services/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"

GIT_BRANCH = check_output(["git status | sed -n 1p | tr '[A-Z]' '[a-z]'"], shell=True).strip('\n ')
GIT_SERVER_DB = "on branch {git-branch}".format(**client)
GIT_SERVER_HOST = "on branch {host}".format(host=client["host"].split('.')[0])
GIT_SERVER_BRANCH = "on branch {DB}".format(**database)
if (GIT_BRANCH != GIT_SERVER_DB) or (GIT_BRANCH != GIT_SERVER_BRANCH) or (GIT_BRANCH != GIT_SERVER_HOST):
    print "\non different branch as compared to server-settings.\nabort.\n"
    print GIT_BRANCH, GIT_SERVER_DB, GIT_SERVER_HOST, GIT_SERVER_BRANCH
    sys.exit(1)


def notify(message, channel="#general", username="fab-bot"):
    payload = {
        "text": message,
        "mrkdwn": "true",
        "channel": channel,
        "username": username,
        "icon_emoji": ":ghost:",
    }
    request = requests.post(SLACKURL, data=json.dumps(payload))
    return request.status_code, request.text


def provision():
    # notify slack channel.
    notify("starting to provision new server for {server}".format(server=env.host))

    # install apt-get packages.
    packages = [
        'git',
        'gcc',
        'g++',
        'htop',
        'monit',
        'nginx',
        'python-dev',
        'python-pip',
        'python-virtualenv',
        'xvfb',
        'zlib1g-dev',
        'wkhtmltopdf',
        'libxml2-dev',
        'libxslt1-dev',
        'rabbitmq-server',
        'build-essential'
    ]
    packages = ' '.join(packages)
    sudo('apt-get update -qq')
    sudo('apt-get install --quiet --assume-yes {packages}'.format(packages=packages))

    # install python pip.
    sudo('pip install -U pip')
    sudo('pip install -U pip --no-use-wheel')

    # setup nginx server.
    nginx()

    # setup scalyr logging.
    scalyr()

    # setup monit service.
    monitrc()

    # setup rabbitmq server.
    rabbitmq()

    # setup IST timezone at server.
    timezone()

    # setup wkhtmltopdf virtual x-server.
    wkhtmltopdf()

    # notify slack channel.
    notify("successfully provisioned new server for {server}".format(server=env.host))

def nginx():
    """setting up nginx server."""

    sudo('rm -f /etc/nginx/sites-enabled/default')
    sudo('rm -f /etc/nginx/sites-enabled/esthenos-webapp')

    put('e_deploy/esthenos-nginx.conf', '/tmp/')
    sudo('mv /tmp/esthenos-nginx.conf /etc/nginx/sites-available/')
    sudo('ln -s /etc/nginx/sites-available/esthenos-nginx.conf /etc/nginx/sites-enabled/esthenos-webapp')

    # restart nginx server.
    sudo('service nginx restart')

def scalyr():
    """ setup scalyr logging agent. """

    sudo('wget -q -nc https://www.scalyr.com/scalyr-repo/stable/latest/scalyr-agent-2_2.0.14_all.deb')
    sudo('dpkg -i scalyr-agent-2_2.0.14_all.deb')

    config = open("e_deploy/esthenos-agent.json").read()
    config = ''.join(config)
    config = config.replace("___HOST_NAME___", env.host)

    with open("/tmp/esthenos-agent.json", "w") as agent:
        agent.write(config)
        agent.close()

    put('/tmp/esthenos-agent.json', '/tmp/')
    sudo("mv /tmp/esthenos-agent.json /etc/scalyr-agent-2/agent.json")

    log = '/var/log/scalyr-agent-2'
    sudo('mkdir -p {d}'.format(d=log))
    sudo('chown -R {user}:{group} {d}'.format(user=env.user, group=env.user, d=log))

    lib = '/var/lib/scalyr-agent-2'
    sudo('chown -R {user}:{group} {d}'.format(user=env.user, group=env.user, d=lib))

    sudo('scalyr-agent-2 start')

def mongodb():
    """setup mongodb for the application server."""
    packages = ' '.join([
      "mongodb"
    ])
    sudo('apt-get update -qq')
    sudo('apt-get install --quiet --assume-yes {packages}'.format(packages=packages))

def monitrc():
    """setting up monitrc manager."""

    put('e_deploy/esthenos-monitrc', '/tmp/')
    sudo("mv /tmp/esthenos-monitrc /etc/monit/monitrc")
    sudo("chmod 0700 /etc/monit/monitrc && chown root:root /etc/monit/monitrc")

    put("e_deploy/esthenos-beats.monitrc", "/tmp/")
    sudo("mv /tmp/esthenos-beats.monitrc /etc/monit/conf.d/")

    put("e_deploy/esthenos-celery.monitrc", "/tmp/")
    sudo("mv /tmp/esthenos-celery.monitrc /etc/monit/conf.d/")

    put("e_deploy/esthenos-webapp.monitrc", "/tmp/")
    sudo("mv /tmp/esthenos-webapp.monitrc /etc/monit/conf.d/")

    sudo('service monit restart')

def rabbitmq():
    """setting up rabbitmq server."""

    sudo('rabbitmqctl add_user esthenos-tasks esthenos')
    sudo('rabbitmqctl add_vhost /esthenos-tasks')
    sudo('rabbitmqctl set_permissions -p /esthenos-tasks esthenos-tasks ".*" ".*" ".*"')

    sudo('service rabbitmq-server restart')

def timezone():
    """setting correct timezone."""

    sudo('timedatectl set-timezone %s' % TIMEZONE)

def wkhtmltopdf():
    sudo("""echo -e '#!/bin/bash\nxvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf $*' > /usr/bin/wkhtmltopdf.sh""")
    sudo("chmod a+x /usr/bin/wkhtmltopdf.sh")
    sudo("ln -s /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf")

def stop(app_name):
    with settings(warn_only=True):
        command = "sudo monit stop {app}".format(app=app_name)
        sudo(command)

def start(app_name):
    with settings(warn_only=True):
        command = "sudo monit start {app}".format(app=app_name)
        sudo(command)

def restart(app_name):
    with settings(warn_only=True):
        command = "sudo monit restart {app}".format(app=app_name)
        sudo(command)

def _ensure_dirs():
    dirs = [PIDS_DIR, LOGS_DIR]
    for d in dirs:
        sudo('mkdir -p {d}'.format(d=d))
        sudo('chown -R {user}:{group} {d}'.format(user=env.user, group=env.user, d=d))

def _requirements(deploy_path=DEPLOY_PATH):
    print "installing webapp python dependencies."
    sudo("pip -q install -r {path}/requirements.txt".format(path=deploy_path))

def deploy():
    # TODO: replace this with
    # - zip up working directory
    # - upload and unzip into DEPLOY_PATH
    dirname = check_output(
        ["echo \"$(date +'%Y-%m-%d')-$(git log --pretty=format:'%h' -n 1)\""], shell=True).strip('\n ')

    # notify slack for deploy start.
    notify("starting deployment of {version} on {server}".format(version=dirname, server=env.host))


    deploy_path = os.path.join(HOME_DIR, dirname)
    run('mkdir -p {}'.format(deploy_path))

    print 'uploading webapp to %s' % deploy_path
    rsync_project(remote_dir=deploy_path, local_dir='./', exclude=['.git', '*.pyc', '*.db', ".DS_Store", '.idea'])

    with cd(deploy_path):
        _ensure_dirs()
        _requirements(deploy_path)

        print 'updating deployment version, this may cause a bit of downtime.'
        run('ln -sfn {new} {current}'.format(new=deploy_path, current=DEPLOY_PATH))

    restart('esthenos-beats')
    restart('esthenos-celery')
    restart('esthenos-webapp')

    # notify slack for deployment finish
    notify("successfully deployed on server {version} on {server}".format(version=dirname, server=env.host))

def version():
    version = prompt("tag version number ?", default=float(ver.__VERSION__) + 0.1)
    updated = datetime.now().strftime("%d.%m.%H.%M")
    git_sha = check_output(
        ["echo \"$(git log --pretty=format:'%h' -n 1)\""], shell=True).strip('\n ')

    context = {
        "version" : version,
        "git_sha" : git_sha,
        "updated" : updated
    }
    template = jinja.get_template('version.py.txt')
    with open('esthenos/version.py', 'w') as f:
        f.write(template.render(context))

    git_tag = "v{version}.{updated}".format(**context)
    local("git tag %s" % git_tag)
    local("git add esthenos/version.py")
    local("git commit -m 'version tagged: %s' && git push && git push --tags" % git_tag)
