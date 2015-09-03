from fabric.api import *
from fabric.contrib.files import *
from fabric.contrib.project import rsync_project
from subprocess import check_output

USER = 'ubuntu'
env.user = USER
env.use_ssh_config = True

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = '/home/ubuntu'
PIDS_DIR = '/var/run/esthenos/'
LOGS_DIR = '/var/log/esthenos/'
DEPLOY_PATH = '%s/esthenos' % HOME_DIR


def provision():
    with open(os.path.expanduser('~/.ssh/esthenos.key.pub')) as f:
        local_ssh_key = f.read().strip('\n')

    # install dependencies.
    put('e_deploy/fabfile.sh', '/tmp/fabfile.sh')
    sudo('LOCAL_SSH_KEY="%s" bash /tmp/fabfile.sh' % local_ssh_key)
    run('rm /tmp/fabfile.sh')

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
    _nginx()

    # setup monit service.
    _monitrc()

    # setup rabbitmq server.
    _rabbitmq()

def _nginx():
    print "setting up nginx server."

    sudo('rm -f /etc/nginx/sites-enabled/default')
    sudo('rm -f /etc/nginx/sites-enabled/esthenos-webapp')
    
    put('e_deploy/esthenos-nginx.conf', '/tmp/')
    sudo('mv /tmp/esthenos-nginx.conf /etc/nginx/sites-available/')
    sudo('ln -s /etc/nginx/sites-available/esthenos-nginx.conf /etc/nginx/sites-enabled/esthenos-webapp')

    # restart nginx server.
    sudo('service nginx restart')

def _monitrc():
    print "setting up monitrc"
    put('e_deploy/monitrc', '/etc/monit/monitrc')

    put("e_deploy/esthenos-beats.monitrc", "/tmp/")
    sudo("mv /tmp/esthenos-beats.monitrc /etc/monit/conf.d/")

    put("e_deploy/esthenos-celery.monitrc", "/tmp/")
    sudo("mv /tmp/esthenos-celery.monitrc /etc/monit/conf.d/")

    put("e_deploy/esthenos-webapp.monitrc", "/tmp/")
    sudo("mv /tmp/esthenos-webapp.monitrc /etc/monit/conf.d/")

    sudo('service monit restart')

def _rabbitmq():
    sudo('rabbitmqctl add_user esthenos-tasks esthenos')
    sudo('rabbitmqctl add_vhost /esthenos-tasks')
    sudo('rabbitmqctl set_permissions -p /esthenos-tasks esthenos-tasks ".*" ".*" ".*"')

    sudo('service rabbitmq-server restart')

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
    
def _ensure_dirs(user):
    env.user = user
    dirs = [PIDS_DIR, LOGS_DIR]
    for d in dirs:
        sudo('mkdir -p {d}'.format(d=d))
        sudo('chown -R {user}:{group} {d}'.format(user=env.user, group=env.user, d=d))

def _requirements(deploy_path=DEPLOY_PATH):
    print "installing webapp python dependencies."
    sudo("pip -q install -r {path}/requirements.txt".format(path=deploy_path))

def deploy(user=USER):
    # TODO: replace this with
    # - zip up working directory
    # - upload and unzip into DEPLOY_PATH
    env.user = user
    dirname = check_output(
        ["echo \"$(date +'%Y-%m-%d')-$(git log --pretty=format:'%h' -n 1)\""], shell=True).strip('\n ')

    deploy_path = os.path.join(HOME_DIR, dirname)
    run('mkdir -p {}'.format(deploy_path))

    print 'uploading webapp to %s' % deploy_path
    rsync_project(remote_dir=deploy_path, local_dir='./', exclude=['.git', '*.pyc', '*.db', ".DS_Store"])

    with cd(deploy_path):
        _ensure_dirs(env.user)
        _requirements(deploy_path)

        print 'updating deployment version, this may cause a bit of downtime.'
        run('ln -sfn {new} {current}'.format(new=deploy_path, current=DEPLOY_PATH))

    restart('esthenos-beats')
    restart('esthenos-celery')
    restart('esthenos-webapp')
    print "Done!"


@parallel
def logs():
    """
    Tail logfiles
    """
    sudo('tail -f {logdir}* /var/log/nginx/*.log'.format(logdir=LOGS_DIR))
