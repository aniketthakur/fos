import os, sys
from fabric.api import *
from slacker import Slacker
from fabric.contrib.files import *
from subprocess import check_output

HOME_DIR = '/home/ubuntu'
DEPLOY_PATH = '%s/esthenos' % HOME_DIR

def notify(message, channel="#deploy-fos", username="fab-bot"):
    slack = Slacker('xoxp-6694899808-6694899856-10378717686-a7deb0')
    slack.chat.post_message(channel, message, username=username)

def code():
    # notify slack for deploy start.
    notify("starting auto-deployment {dirname}".format(dirname=DEPLOY_PATH))

    with cd(DEPLOY_PATH):
        local("git pull --rebase")
        local("sudo pip -q install -r requirements.txt")

def reboot():
    local('sudo monit restart esthenos-beats')
    local('sudo monit restart esthenos-celery')
    local('sudo monit restart esthenos-webapp')

    # notify slack for deployment finish
    notify("successfully auto-deployed")
