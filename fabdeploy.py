import os, sys, requests, json
from fabric.api import *
from slacker import Slacker
from fabric.contrib.files import *
from esthenos.notify import notify
from subprocess import check_output

HOME_DIR = '/home/ubuntu'
DEPLOY_PATH = '%s/esthenos' % HOME_DIR
SLACKURL = "https://hooks.slack.com/services/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"


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

def code():
    # notify slack for deploy start.
    git_sha = check_output(
                ["echo \"$(git log --pretty=format:'%h' -n 1)\""], shell=True).strip('\n ')

    notify("starting auto-deployment esthenos-fos git-sha: %s" % git_sha)

    with cd(DEPLOY_PATH):
        local("git pull --rebase")
        local("sudo pip -q install -r requirements.txt")

def reboot():
    local('sudo monit restart esthenos-beats')
    local('sudo monit restart esthenos-celery')
    local('sudo monit restart esthenos-webapp')

    # notify slack for deployment finish
    notify("successfully auto-deplyed esthenos-fos")
