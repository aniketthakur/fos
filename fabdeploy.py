import os, sys, requests, json
from fabric.api import *
from slacker import Slacker
from fabric.contrib.files import *
from esthenos.notify import notify
from subprocess import check_output

HOME_DIR = '/home/ubuntu'
DEPLOY_PATH = '%s/esthenos' % HOME_DIR

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
