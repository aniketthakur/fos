#!/usr/bin/python

import sys
import requests
import json

pan_url='http://console.digikyc.com/api/services/read_pan'
vid_url='http://console.digikyc.com/api/services/read_voters_id'
addhaar_url='http://console.digikyc.com/api/services/read_aadhaar_id'
headers={'InstanceToken' : 'zvgkH-L1eJ1CucZacS6jsb7Fwx0NEGl-40ZM2vvpW0k','Accept':'application/json'}

def get_pan_details(path):
    files = {'query': open(path, 'rb')}
    response = requests.post(pan_url, files=files,headers=headers)
    print response.content
    return response.content

def get_pan_details_url(path):
    data = {'query_url': path}
    print data
    response = requests.post(pan_url, data=data,headers=headers)
    print response.content
    return response.content

def get_vid_details(path):
    files = {'query': open(path, 'rb')}
    response = requests.post(vid_url, files=files,headers=headers)
    print response.content
    return response.content

def get_vid_details_url(path):
    data = {'query_url': path}
    response = requests.post(vid_url, data=data,headers=headers)
    print response.content
    return response.content

def get_aadhaar_details(path):
    files = {'query': open(path, 'rb')}
    response = requests.post(addhaar_url, files=files,headers=headers)
    print response.content
    return response.content

def get_aadhaar_details_url(path):
    data = {'query_url': path}
    response = requests.post(addhaar_url, data=data,headers=headers)
    print response.content
    return response.content