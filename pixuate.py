#!/usr/bin/python

import sys
import requests
import json

pan_url='http://console.digikyc.com/api/services/read_pan'
vid_url='http://console.digikyc.com/api/services/read_voters_id'
addhaar_url='http://console.digikyc.com/api/services/read_aadhaar_id'
headers={'InstanceToken' : '5BzNLq_3ncuJ4cOPsJLK84YDf0R_HEllq11h0T6EZZA','Accept':'application/json'}

def get_pan_details(path):
    files = {'query': open(path, 'rb')}
    response = requests.post(pan_url, files=files,headers=headers)
    print response.content
    return response.content


def get_vid_details(path):
    files = {'query': open(path, 'rb')}
    response = requests.post(vid_url, files=files,headers=headers)
    print response.content
    return response.content

def get_aadhaar_details(path):
    files = {'query': open(path, 'rb')}
    response = requests.post(addhaar_url, files=files,headers=headers)
    print response.content
    return response.content