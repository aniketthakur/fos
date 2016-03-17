import os, sys, requests, json
from esthenos.settings import SLACKURL

def notify(message, channel="#deployments", username="deploy-bot"):
    payload = {
        "text": message,
        "mrkdwn": "true",
        "channel": channel,
        "username": username,
        "icon_emoji": ":ghost:",
    }
    print message
    request = requests.post(SLACKURL, data=json.dumps(payload))
    return request.status_code, request.text
